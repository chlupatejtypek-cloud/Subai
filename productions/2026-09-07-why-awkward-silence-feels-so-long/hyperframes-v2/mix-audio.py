from pathlib import Path
import json,subprocess,numpy as np,soundfile as sf,shutil
from scipy.signal import butter,sosfilt
p=Path(__file__).resolve().parent;c=json.loads((p/'cue-times.json').read_text());sr=48000;dest=p/'assets';rng=np.random.default_rng(42)
# Original procedural zoom effects; never attributed to Fish.
n=int(.46*sr);t=np.arange(n)/sr;noise=sosfilt(butter(2,[450,4200],btype='bandpass',fs=sr,output='sos'),rng.normal(size=n));envelope=np.sin(np.pi*t/.46)**2;v=(noise*.65+.075*np.sin(2*np.pi*(180*t+900*t*t)))*envelope;v/=max(abs(v));sf.write(dest/'zoom-in-original.wav',v,sr,subtype='PCM_16');sf.write(dest/'zoom-out-original.wav',v[::-1],sr,subtype='PCM_16')
lib=Path('/home/user/sfx-library/kenney-interface');
if (lib/'License.txt').exists():shutil.copy2(lib/'License.txt',p/'KENNEY-LICENSE.txt')
elif not (p/'KENNEY-LICENSE.txt').exists():raise FileNotFoundError('Kenney CC0 license missing')
for name in ['open_001.ogg','drop_001.ogg','drop_002.ogg']:
 if (lib/name).exists():shutil.copy2(lib/name,dest/name)
 elif not (dest/name).exists():raise FileNotFoundError('Restore Kenney source '+name)
cues=[(.03,'zoom-in-original.wav',.024,'Opening push, original procedural synthesis'),(c['study']+.05,'open_001.ogg',.020,'Research panel, Kenney Interface Sounds CC0'),(c['fact']+.07,'drop_001.ogg',.026,'Fact card landing, Kenney CC0'),(c['guess']+.07,'drop_002.ogg',.023,'Guess card landing, Kenney CC0'),(c['outro']+.04,'zoom-out-original.wav',.022,'Return to same cafe/pull out, original procedural synthesis')]
a=np.zeros(round(c['duration']*sr));report=[]
for at,name,peak,reason in cues:
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(dest/name),'-f','f32le','-ac','1','-ar',str(sr),'-']);x=np.frombuffer(raw,dtype=np.float32).copy();x=x[:int(.65*sr)];x*=peak/(np.max(np.abs(x))+1e-12)
 fade=min(int(.005*sr),len(x)//4);x[:fade]*=np.linspace(0,1,fade);x[-fade:]*=np.linspace(1,0,fade);i=round(at*sr);a[i:i+len(x)]+=x;report.append({'at':at,'source':name,'peak':peak,'purpose_and_rights':reason})
sf.write(p/'audio/sfx.wav',a,sr,subtype='PCM_16');(p/'sfx.json').write_text(json.dumps(report,indent=2))
subprocess.run(['ffmpeg','-y','-v','error','-i',str(p/'audio/narration.wav'),'-i',str(p/'audio/sfx.wav'),'-filter_complex','[0:a]loudnorm=I=-16:TP=-2:LRA=9[v];[v][1:a]amix=inputs=2:normalize=0,alimiter=limit=0.94:level=false[a]','-map','[a]','-ar','48000','-t',str(c['duration']),str(p/'audio/final-mix.wav')],check=True)
# Five labelled-by-order examples in one optional sound-effects audition, not spoken labels.
sampler=np.zeros(6*sr)
for j,name in enumerate(['zoom-in-original.wav','zoom-out-original.wav','open_001.ogg','drop_001.ogg','drop_002.ogg']):
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(dest/name),'-f','f32le','-ac','1','-ar',str(sr),'-']);x=np.frombuffer(raw,dtype=np.float32);x=x[:int(.7*sr)];x=x*.25/(np.max(abs(x))+1e-9);i=round((.3+j*1.1)*sr);sampler[i:i+len(x)]+=x
sf.write('/home/user/sfx-zoom-ui-preview.wav',sampler,sr,subtype='PCM_16');print('Five restrained cues mixed; optional six-second preview created.')
