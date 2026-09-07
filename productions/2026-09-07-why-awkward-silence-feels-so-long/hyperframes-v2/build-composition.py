from pathlib import Path
import json,shutil,math
import soundfile as sf
p=Path(__file__).resolve().parent
w=json.loads((p/'audio/words.json').read_text())['words']
t=lambda i:round(w[i]['start']*30)/30
voice,sr=sf.read(p/'audio/narration.wav');duration=math.ceil((len(voice)/sr+.3)*30)/30
cues={'study':t(14),'add':t(29),'rejected':t(40),'estimates':t(42),'twist':t(57),'proof':t(69),'limit':t(74),'factScene':t(88),'fact':t(97),'guess':t(100),'outro':t(110),'question':t(116),'verdict':t(120),'duration':duration}
(p/'cue-times.json').write_text(json.dumps(cues,indent=2))
(p/'assets').mkdir(exist_ok=True)
shutil.copy2('/home/user/hyperframes-runtime/node_modules/gsap/dist/gsap.min.js',p/'assets/gsap.min.js')
shutil.copy2('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',p/'assets/DejaVuSans-Bold.ttf')
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>A Pause Is Not a Verdict</title><style>
@font-face{font-family:Stiles;src:url('assets/DejaVuSans-Bold.ttf')}*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#102b2d;color:#f4ead5;font-family:Stiles, sans-serif}#root{position:relative;width:1080px;height:1920px;overflow:hidden}.scene{position:absolute;inset:0;overflow:hidden}.photo{width:100%;height:100%;object-fit:cover;position:absolute;inset:0}.cafe-photo{background:url(assets/cafe.png) center/cover}.study-photo{background:url(assets/study.png) center/cover}.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,26,29,.85),rgba(6,26,29,.05) 51%,rgba(6,26,29,.42))}.brand{position:absolute;left:80px;top:96px;letter-spacing:7px;font-size:27px;opacity:.76;z-index:20}.eyebrow{font-size:29px;letter-spacing:5px;color:#dec58f;margin-bottom:30px}h1{font-size:88px;letter-spacing:-3px;line-height:1.1;margin:0;font-weight:700}.heading{position:absolute;top:218px;left:80px;right:80px}.gold{color:#edc980}.foot{position:absolute;left:84px;right:84px;top:1460px;font-size:35px;line-height:1.45;color:#dedcca}.small{font-size:29px;line-height:1.5;color:#becbc3}.bgui{background:#102b2d}.ghost{opacity:.12;filter:saturate(.5)}.tint{position:absolute;inset:0;background:linear-gradient(135deg,rgba(11,43,44,.35),rgba(5,27,32,.83))}.line{height:2px;background:#d8c594;opacity:.28;position:absolute;left:80px;right:80px;top:1795px}.chip{display:inline-block;border:2px solid #547675;border-radius:30px;padding:17px 24px;font-size:28px;letter-spacing:2px}.card{position:absolute;left:80px;right:80px;border:2px solid #bfa779;border-radius:26px;padding:38px 44px;background:#eee3c9;color:#183436;box-shadow:0 16px 40px #00171833}.card .label{font-size:27px;letter-spacing:5px;color:#426568;margin-bottom:18px}.card .value{font-size:54px;letter-spacing:-1.4px}.darkcard{background:#1a3b3d;color:#f3e4c8;border-color:#527574}.darkcard .label{color:#d9bd87}.source{position:absolute;left:80px;right:80px;top:1635px;font-size:28px;line-height:1.55;color:#afc4bd}.stat{position:absolute;left:80px;right:80px;top:640px}.bubble{background:#efe3c8;color:#173738;border-radius:32px;padding:32px 38px;font-size:48px;line-height:1.25;position:absolute;left:80px;top:486px;max-width:900px}.bubble:after{content:'';position:absolute;left:80px;bottom:-26px;border:16px solid transparent;border-top-color:#efe3c8;border-bottom:0}.progress{position:absolute;bottom:0;left:0;height:5px;background:#d7b675;width:1080px;transform-origin:left;z-index:30}
#research,#meaning,#facts,#outro,#plot,#flowMark,#pauseMark,#delayNote,#notProof,#limitCard,#factCard,#guessCard,#question,#landing{opacity:0;visibility:hidden}</style></head><body><div id="root" data-composition-id="silence" data-width="1080" data-height="1920" data-start="0" data-duration="DURATION" data-fps="30">
<div id="hero" class="scene clip" data-start="0" data-duration="DURATION" data-track-index="0"><div id="heroPhoto" class="photo cafe-photo"></div><div class="shade"></div><div class="heading"><div class="eyebrow">THE SOCIAL SIGNAL</div><h1>A pause.<br><span class="gold">Not a verdict.</span></h1></div><div class="foot" id="heroFoot">A feeling is not the whole story.</div></div>
<div id="research" class="scene bgui clip" data-start="0" data-duration="DURATION" data-track-index="1"><div class="photo ghost study-photo"></div><div class="tint"></div><div class="heading"><div class="eyebrow">THE EXPERIMENT · 2011</div><h1>One conversation.<br><span class="gold">Two versions.</span></h1><div class="chip" style="margin-top:42px">WATCHING + IMAGINING PARTICIPATION</div></div>
<div id="plot" class="stat"><div style="font-size:36px;margin-bottom:18px">Felt rejection <span style="color:#aabfb5;font-size:27px">· mean rating, 1–7</span></div>
<svg width="920" height="520" viewBox="0 0 920 520" aria-label="Mean rejection 1.90 in flow and 2.80 after a four-second pause; full scale one to seven">
<g fill="#e9e1cf" font-family="Stiles" font-size="31"><text x="10" y="36">Smooth flow</text><text x="10" y="236">4-second pause</text></g>
<g stroke="#678481" stroke-width="4" stroke-linecap="round"><path d="M30 125H880"/><path d="M30 325H880"/></g>
<g fill="#aebfb8" font-family="Stiles" font-size="27"><text x="24" y="177">1</text><text x="442" y="177">4</text><text x="870" y="177">7</text><text x="24" y="377">1</text><text x="442" y="377">4</text><text x="870" y="377">7</text></g>
<g id="flowMark"><circle cx="157.5" cy="125" r="17" fill="#e4eee4"/><text x="157.5" y="107" dy="-20" text-anchor="middle" fill="#e4eee4" font-family="Stiles" font-size="35">1.90</text></g>
<g id="pauseMark"><circle cx="285" cy="325" r="19" fill="#edc980"/><text x="285" y="307" dy="-20" text-anchor="middle" fill="#edc980" font-family="Stiles" font-size="35">2.80</text></g>
</svg></div>
<div id="delayNote" class="card darkcard" style="top:1370px;padding:28px 36px"><div style="font-size:30px;color:#ddc58e;margin-bottom:12px">THE UNEXPECTED PART</div><div style="font-size:36px;line-height:1.3">Estimated delay?<br>No significant group difference.</div></div><div class="source">Two video conditions · Study 2<br>Koudenburg, Postmes &amp; Gordijn (2011)</div></div>
<div id="meaning" class="scene bgui clip" data-start="0" data-duration="DURATION" data-track-index="2"><div class="photo ghost study-photo"></div><div class="tint"></div><div class="heading"><div class="eyebrow">WHAT IT MEANS</div><h1>A signal.<br><span class="gold">Not a verdict.</span></h1></div>
<svg style="position:absolute;left:165px;top:610px" width="750" height="270" viewBox="0 0 750 270"><g fill="none" stroke="#d5c7a3" stroke-width="6"><path d="M10 45Q10 10 45 10H230Q265 10 265 45V135Q265 170 230 170H95L55 210V170H45Q10 170 10 135Z"/><path d="M485 45Q485 10 520 10H705Q740 10 740 45V135Q740 170 705 170H665V210L620 170H520Q485 170 485 135Z"/></g><path id="bridge" d="M286 90H464" stroke="#eac87e" stroke-width="6" stroke-dasharray="12 13"/></svg>
<div style="position:absolute;left:80px;right:80px;top:940px;text-align:center;font-size:51px;color:#eed8a7">Feels disconnected</div><div id="notProof" style="position:absolute;left:80px;right:80px;top:1030px;text-align:center;font-size:43px">≠ proof of rejection</div>
<div id="limitCard" class="card darkcard" style="top:1370px"><div style="font-size:39px;color:#edc980">4 seconds ≠ a universal limit</div><div style="font-size:30px;margin-top:20px">One specific experimental setup.</div></div></div>
<div id="facts" class="scene bgui clip" data-start="0" data-duration="DURATION" data-track-index="3"><div class="photo ghost study-photo"></div><div class="tint"></div><div class="heading"><div class="eyebrow">TRY THIS INSTEAD</div><h1>Separate the fact<br>from <span class="gold">the story.</span></h1><div style="font-size:33px;margin-top:38px;color:#becdc4">Before you apologize…</div></div><div id="factCard" class="card" style="top:620px"><div class="label">01 / FACT</div><div class="value">“They paused.”</div></div><div id="guessCard" class="card darkcard" style="top:920px"><div class="label">02 / GUESS</div><div class="value">“They’re judging me.”</div></div><div class="foot" style="top:1440px">An interpretation is not an observation.</div></div>
<div id="outro" class="scene clip" data-start="0" data-duration="DURATION" data-track-index="4"><div id="outroPhoto" class="photo cafe-photo"></div><div class="shade"></div><div class="heading"><div class="eyebrow">LEAVE ROOM FOR A REPLY</div><h1>Give it<br><span class="gold">a moment.</span></h1></div><div id="question" class="bubble">“What do you think?”</div><div id="landing" class="foot" style="font-size:48px;top:1430px">Missing information.<br><span class="gold">Not a verdict.</span></div></div>
<div id="brand" class="brand clip" data-start="0" data-duration="DURATION" data-track-index="10">STILES / PSYCHOLOGY</div><div id="progress" class="progress clip" data-start="0" data-duration="DURATION" data-track-index="11"></div>
<script src="assets/gsap.min.js"></script><script>
const C=CUES;const tl=gsap.timeline({paused:true});
gsap.set(['#research','#meaning','#facts','#outro'],{autoAlpha:0},0);
gsap.set(['#plot','#flowMark','#pauseMark','#delayNote','#notProof','#limitCard','#factCard','#guessCard','#question','#landing'],{autoAlpha:0},0);
tl.fromTo('#heroPhoto',{scale:1},{scale:1.045,duration:C.study,ease:'none'},0);
tl.fromTo('#hero .heading',{y:18,opacity:0},{y:0,opacity:1,duration:.6,ease:'power2.out'},0);
function scene(id,start,previous){tl.to(previous+' > :not(.photo):not(.shade):not(.tint)',{opacity:0,duration:.14,ease:'power1.out'},start);tl.to(id,{autoAlpha:1,duration:.26,ease:'power1.inOut'},start+.14);tl.to(previous,{autoAlpha:0,duration:.26,ease:'power1.inOut'},start+.14);}
scene('#research',C.study,'#hero');
tl.fromTo('#plot',{y:25,autoAlpha:0},{y:0,autoAlpha:1,duration:.55,ease:'power2.out'},C.add);
tl.fromTo('#flowMark',{x:-127.5,autoAlpha:0},{x:0,autoAlpha:1,duration:.85,ease:'power2.out'},C.add+.3);
tl.fromTo('#pauseMark',{x:-255,autoAlpha:0},{x:0,autoAlpha:1,duration:.85,ease:'power2.out'},C.rejected-.25);
tl.fromTo('#delayNote',{y:22,autoAlpha:0},{y:0,autoAlpha:1,duration:.45,ease:'power2.out'},C.estimates);
scene('#meaning',C.twist,'#research');tl.fromTo('#bridge',{strokeDashoffset:80},{strokeDashoffset:0,duration:3,ease:'power1.out'},C.twist+.4);
tl.fromTo('#notProof',{y:15,autoAlpha:0},{y:0,autoAlpha:1,duration:.45},C.proof);
tl.fromTo('#limitCard',{y:24,autoAlpha:0},{y:0,autoAlpha:1,duration:.45,ease:'power2.out'},C.limit);
scene('#facts',C.factScene,'#meaning');
tl.fromTo('#factCard',{x:-34,autoAlpha:0},{x:0,autoAlpha:1,duration:.42,ease:'power2.out'},C.fact);
tl.fromTo('#guessCard',{x:34,autoAlpha:0},{x:0,autoAlpha:1,duration:.42,ease:'power2.out'},C.guess);
scene('#outro',C.outro,'#facts');tl.fromTo('#outroPhoto',{scale:1.045},{scale:1,duration:C.duration-C.outro,ease:'power1.out'},C.outro);
tl.fromTo('#question',{y:20,autoAlpha:0},{y:0,autoAlpha:1,duration:.4,ease:'power2.out'},C.question);
tl.fromTo('#landing',{y:14,autoAlpha:0},{y:0,autoAlpha:1,duration:.4},C.verdict);
tl.fromTo('.progress',{scaleX:0},{scaleX:1,duration:C.duration,ease:'none'},0);
window.__timelines=window.__timelines||{};window.__timelines.silence=tl;
</script></div></body></html>'''
html=html.replace('DURATION',str(duration)).replace('CUES',json.dumps(cues))
(p/'index.html').write_text(html)
(p/'storyboard.json').write_text(json.dumps({'duration':duration,'unique_illustrations':2,'new_image_generations':0,'reuse':'Exact approved source cafe 01 and study 04, not new variants','phases':[{'name':name,'start':a,'end':b} for name,a,b in [('hook',0,cues['study']),('study and sourced dot plot',cues['study'],cues['twist']),('interpretation and caveat',cues['twist'],cues['factScene']),('fact versus guess cards',cues['factScene'],cues['outro']),('same cafe and follow-up',cues['outro'],duration)]]},indent=2))
print(json.dumps(cues,indent=2))
