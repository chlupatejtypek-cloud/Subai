#!/usr/bin/env python3
"""Render the 9:16 psychology test from Agnes hook, moving stills and Fish timestamps."""
from __future__ import annotations
import json, math, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FPS = 30
AUDIO_DUR = 37.6
SCENES = [
    ("visuals/scene-01-hook-agnes.mp4", 4.04, "agnes"),
    ("visuals/scene-02-assignment.png", 6.76, "push"),
    ("visuals/scene-03-phone-relief.png", 3.68, "pan_lr"),
    ("visuals/scene-04-loop.png", 7.32, "pull"),
    ("visuals/scene-05-future-self.png", 3.36, "pan_lr"),
    ("visuals/scene-06-name-feeling.png", 3.12, "push"),
    ("visuals/scene-07-if-then-clean.png", 5.60, "pan_rl"),
    ("visuals/scene-08-small-start.png", 3.72, "pull"),
]

def run(cmd):
    print("+", " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)

def ass_time(sec):
    cs = max(0, round(sec * 100))
    h, rem = divmod(cs, 360000); m, rem = divmod(rem, 6000); s, c = divmod(rem, 100)
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"

def captions():
    data = json.loads((ROOT / "audio/narration.opus.timestamps.json").read_text())
    # The SSE stream may update a chunk progressively. Keep the richest update per offset.
    best = {}
    for chunk in data["alignment_chunks"]:
        off = float(chunk.get("chunk_audio_offset_sec") or 0)
        segs = chunk.get("alignment", {}).get("segments", [])
        if len(segs) > len(best.get(off, [])): best[off] = segs
    words=[]
    for off,segs in sorted(best.items()):
        for s in segs:
            text=re.sub(r"[^A-Za-z0-9']+", "", s["text"]).upper()
            if not text: continue
            start=off+float(s["start"]); end=off+float(s["end"])
            if end-start < .10: end=start+.10
            words.append((start,min(end,AUDIO_DUR),text))
    header="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Word,DejaVu Sans,60,&H00FFFFFF,&H00FFFFFF,&H800E1720,&H00000000,-1,0,0,0,100,100,0,0,1,3,1,5,20,20,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    # Enforce exactly one visible word. Fish can occasionally assign identical starts
    # to a very short article and the following word; give that article 80 ms first.
    nonoverlap=[]; previous_end=0.0
    for original_start,original_end,text in words:
        start=max(original_start,previous_end)
        end=max(original_end,start+.08)
        nonoverlap.append((start,min(end,AUDIO_DUR),text)); previous_end=end
    highlights={"REWARDING","PROCRASTINATION","RELIEF","DISCOMFORT","MOOD","REPAIR","STRESS","FEELING","PLAN","SENTENCE","SMALL","FEAR"}
    lines=[]
    for start,end,text in nonoverlap:
        color=r"\c&H0049D8FF&" if text in highlights else ""
        anim=r"{\an5\pos(540,1230)\fscx78\fscy78\alpha&H30&\t(0,85,\fscx108\fscy108\alpha&H00&)\t(85,165,\fscx100\fscy100)}"
        lines.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Word,,0,0,0,,{anim}{{{color}}}{text}")
    (ROOT/"captions.ass").write_text(header+"\n".join(lines)+"\n")
    return len(words)

def main():
    temp=ROOT/"output/segments"; temp.mkdir(parents=True,exist_ok=True)
    for i,(src,dur,motion) in enumerate(SCENES,1):
        out=temp/f"{i:02d}.mp4"; frames=round(dur*FPS)
        if motion=="agnes":
            vf=f"scale=1080:2006:flags=lanczos,crop=1080:1920:0:43,fps={FPS},trim=duration={dur},setpts=PTS-STARTPTS"
            cmd=["ffmpeg","-y","-loglevel","error","-i",str(ROOT/src),"-an","-vf",vf,"-r",str(FPS),"-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",str(out)]
        else:
            if motion=="push": z=f"1+0.05*on/{max(frames-1,1)}"; x="iw/2-(iw/zoom/2)"
            elif motion=="pull": z=f"1.05-0.05*on/{max(frames-1,1)}"; x="iw/2-(iw/zoom/2)"
            elif motion=="pan_lr": z="1.08"; x=f"(iw-iw/zoom)*on/{max(frames-1,1)}"
            else: z="1.08"; x=f"(iw-iw/zoom)*(1-on/{max(frames-1,1)})"
            vf=f"scale=1080:1935:flags=lanczos,zoompan=z='{z}':x='{x}':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={FPS},trim=duration={dur},setsar=1"
            cmd=["ffmpeg","-y","-loglevel","error","-loop","1","-i",str(ROOT/src),"-an","-vf",vf,"-frames:v",str(frames),"-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",str(out)]
        run(cmd)
    concat=ROOT/"output/concat.txt"
    concat.write_text("".join(f"file '{(temp/f'{i:02d}.mp4').as_posix()}'\n" for i in range(1,len(SCENES)+1)))
    silent=ROOT/"output/silent.mp4"
    run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(silent)])
    count=captions(); print("caption_words",count)
    # Burn captions at 720p to stay within constrained render RAM, then upscale the
    # completed raster to the required 1080x1920 deliverable.
    captioned=ROOT/"output/captioned-720.mp4"
    final=ROOT/"output/procrastination-relief-final.mp4"
    run(["ffmpeg","-y","-loglevel","error","-i",str(silent),"-i",str(ROOT/"audio/narration.opus"),"-vf",f"scale=720:1280:flags=lanczos,ass={ROOT/'captions.ass'}","-map","0:v:0","-map","1:a:0","-c:v","libx264","-preset","ultrafast","-crf","18","-threads","1","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest",str(captioned)])
    run(["ffmpeg","-y","-loglevel","error","-i",str(captioned),"-vf","scale=1080:1920:flags=lanczos","-c:v","libx264","-preset","ultrafast","-crf","18","-threads","1","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(final)])
    run(["ffprobe","-v","error","-show_entries","stream=codec_name,width,height,r_frame_rate:format=duration,size","-of","json",str(final)])
if __name__=="__main__": main()
