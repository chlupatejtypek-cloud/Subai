# One-off retouch provenance. Do not rerun on already repaired Cloudinary assets.
from pathlib import Path
from PIL import Image,ImageDraw
import cv2,numpy as np
P=Path(__file__).resolve().parent/'visuals'
# Remove only the third forearm/hand. The two hands at the phone remain attached.
p=P/'01.png';im=cv2.imread(str(p));mask=np.zeros(im.shape[:2],dtype=np.uint8)
cv2.polylines(mask,[np.array([(605,785),(615,832),(624,866),(633,900),(641,931)],np.int32)],False,255,23)
cv2.fillPoly(mask,[np.array([(611,924),(650,909),(699,918),(724,938),(734,960),(723,979),(688,980),(658,966),(627,962),(603,968),(590,954),(594,939)],np.int32)],255)
mask=cv2.dilate(mask,np.ones((3,3),np.uint8))
fixed=cv2.inpaint(im,mask,5,cv2.INPAINT_TELEA);cv2.imwrite(str(p),fixed)
# Flatten the unwanted spherical head shading to canonical illustrated treatment.
p=P/'09.png';im=Image.open(p).convert('RGB');a=np.array(im);h,w=a.shape[:2];Y,X=np.mgrid[:h,:w];cx,cy=501,470;rx,ry=171,175
inside=((X-cx)/rx)**2+((Y-cy)/ry)**2<=1
rng=np.random.default_rng(9);noise=rng.normal(0,1.4,(h,w,1));beige=np.clip(np.array([218,187,137])+noise,0,255).astype('uint8');a[inside]=beige[inside]
im=Image.fromarray(a);d=ImageDraw.Draw(im);d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),outline=(24,30,33),width=7)
d.ellipse((404,484,420,508),fill=(24,30,33));d.ellipse((490,483,506,507),fill=(24,30,33));d.arc((390,457,438,486),190,325,fill=(24,30,33),width=5);d.arc((477,456,522,485),195,327,fill=(24,30,33),width=5);d.line((433,544,477,543),fill=(24,30,33),width=5)
im.save(p)
print('Local anatomy cleanup and flat head repair complete; no new generated images.')
