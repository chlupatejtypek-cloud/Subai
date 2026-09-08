"""Track the actual blank tag in every Agnes frame and perspective-print prices.
Original video is unchanged; creates a separate composited derivative, no AI retry.
"""
from pathlib import Path
import cv2,numpy as np,json,subprocess
from scipy.signal import savgol_filter
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).resolve().parent;src=p/'assets/original-hook.mp4';(p/'assets').mkdir(exist_ok=True);(p/'output').mkdir(exist_ok=True)
cap=cv2.VideoCapture(str(src));fps=cap.get(cv2.CAP_PROP_FPS);frames=[];corners=[];areas=[]
def order(pts):
 pts=np.array(pts,dtype=np.float32);s=pts.sum(axis=1);d=np.diff(pts,axis=1).ravel();return np.array([pts[np.argmin(s)],pts[np.argmin(d)],pts[np.argmax(s)],pts[np.argmax(d)]],np.float32)
while True:
 ok,bgr=cap.read()
 if not ok:break
 hsv=cv2.cvtColor(bgr,cv2.COLOR_BGR2HSV);mask=cv2.inRange(hsv,np.array([0,0,210]),np.array([180,65,255]));roi=np.zeros(mask.shape,np.uint8);roi[270:570,100:360]=255;mask=cv2.bitwise_and(mask,roi);mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8));contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 valid=[c for c in contours if 5500<cv2.contourArea(c)<35000];assert valid,'No confident tag contour';cnt=max(valid,key=cv2.contourArea);q=cv2.approxPolyDP(cnt,.018*cv2.arcLength(cnt,True),True).reshape(-1,2)
 if len(q)!=4:q=cv2.boxPoints(cv2.minAreaRect(cnt))
 q=order(q);corners.append(q);areas.append(float(cv2.contourArea(cnt)));frames.append(bgr)
cap.release();Q=np.array(corners);smooth=savgol_filter(Q,5,2,axis=0).astype(np.float32);assert np.max(np.linalg.norm(np.diff(Q.mean(axis=1),axis=0),axis=1))<30
layer=Image.new('RGBA',(180,280),(0,0,0,0));draw=ImageDraw.Draw(layer);font=p/'assets/DejaVuSans-Bold.ttf';draw.text((90,100),'$99',font=ImageFont.truetype(str(font),39),fill=(91,84,71,235),anchor='mm');draw.line((44,97,139,97),fill=(83,69,57,240),width=4);draw.text((90,179),'$49',font=ImageFont.truetype(str(font),62),fill=(20,52,47,255),anchor='mm');rgba=np.array(layer);H,W=frames[0].shape[:2];base=np.array([[0,0],[179,0],[179,279],[0,279]],np.float32)
proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p',str(p/'assets/priced-hook-native.mp4')],stdin=subprocess.PIPE)
for i,(frame,q) in enumerate(zip(frames,smooth)):
 transform=cv2.getPerspectiveTransform(base,q);ink=cv2.warpPerspective(rgba,transform,(W,H),flags=cv2.INTER_CUBIC);alpha=ink[:,:,3:4].astype(np.float32)/255;inkbgr=ink[:,:,:3][:,:,::-1];printed=frame*(1-alpha)+inkbgr*alpha
 # One short focus moment: preserve the tag, soften only its surroundings.
 tm=i/fps;rise=np.clip((tm-.65)/.35,0,1);fall=np.clip((2.7-tm)/.45,0,1);strength=float(min(rise,fall))*.78;strength=strength*strength*(3-2*strength)
 m=np.zeros((H,W),np.uint8);center=q.mean(axis=0);expanded=(center+(q-center)*1.10).astype(np.int32);cv2.fillConvexPoly(m,expanded,255);sharp=cv2.GaussianBlur(m,(0,0),2)[:,:,None]/255;blur=cv2.GaussianBlur(printed.astype(np.uint8),(0,0),4.0);outside=strength*(1-sharp);result=printed*(1-outside)+blur*outside;proc.stdin.write(np.clip(result,0,255).astype(np.uint8).tobytes())
proc.stdin.close();assert proc.wait()==0
subprocess.run(['ffmpeg','-y','-v','error','-i',str(p/'assets/priced-hook-native.mp4'),'-vf','scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,tpad=stop_mode=clone:stop_duration=0.4','-t','4.4','-an','-c:v','libx264','-preset','fast','-crf','18','-threads','2','-pix_fmt','yuv420p',str(p/'assets/priced-hook.mp4')],check=True)
(p/'tracking.json').write_text(json.dumps({'frames':len(frames),'native_fps':fps,'contour_area_range':[min(areas),max(areas)],'max_center_step_px':float(np.max(np.linalg.norm(np.diff(Q.mean(axis=1),axis=0),axis=1))),'method':'HSV constrained-ROI contour; per-frame four-corner homography; 5-frame polynomial corner smoothing; printed ink only','price':'$99 struck out / $49','selective_focus':'0.65–2.7s; outside expanded tag only; final captions added afterward','corners':smooth.tolist()},indent=2));print('Tracked/priced frames:',len(frames))
