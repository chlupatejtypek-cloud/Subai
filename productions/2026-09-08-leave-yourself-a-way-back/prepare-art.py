from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,cv2,json
p=Path(__file__).resolve().parent;im=np.array(Image.open(p/'assets/focused.png').convert('RGB'));ink=Image.new('RGBA',(210,350),(0,0,0,0));d=ImageDraw.Draw(ink);col=(52,76,65,225)
d.arc((57,45,155,143),175,365,fill=col,width=5);d.line([(57,96),(63,125),(83,149),(83,174),(127,174),(127,150),(148,119),(154,97)],fill=col,width=5);d.line((84,186,125,186),fill=col,width=5);d.line((91,197,119,197),fill=col,width=5)
for a,b in [((105,12),(105,29)),((34,38),(48,51)),((163,42),(180,26)),((18,95),(36,95)),((174,94),(193,94))]:d.line([a,b],fill=col,width=4)
for y,w in [(245,137),(270,108),(295,126)]:d.line((35,y,w+35,y),fill=(70,88,72,180),width=3)
H=cv2.getPerspectiveTransform(np.float32([[0,0],[209,0],[209,349],[0,349]]),np.float32([[74,583],[268,579],[307,901],[112,929]]));layer=cv2.warpPerspective(np.array(ink),H,(im.shape[1],im.shape[0]));a=layer[:,:,3:]/255;out=(im*(1-a)+layer[:,:,:3]*a).astype('uint8');Image.fromarray(out).crop((27,32,741,1344)).save(p/'assets/focused-ready.png');print('Removed generated picture frame; authored perspective-aligned idea sketch on actual easel paper.')
