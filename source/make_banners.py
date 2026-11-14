from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from scipy import ndimage
B='/home/claude/f2f/'
FONT=B+'fonts/cinzel900.ttf'
rng=np.random.default_rng(7)

def background(W,H,glow_center):
    a=np.zeros((H,W,3),float); a[...]=(14,12,10)
    yy,xx=np.mgrid[0:H,0:W]
    cx,cy=glow_center
    d=np.sqrt(((xx-cx)/(W*.45))**2+((yy-cy)/(H*.7))**2)
    g=np.clip(1-d,0,1)**1.8
    a+=g[...,None]*np.array([150,55,10])*0.55
    # bottom coal glow
    b=np.clip(1-(H-yy)/(H*.35),0,1)**2.2
    a+=b[...,None]*np.array([200,70,10])*0.35
    # hammered texture
    n=ndimage.gaussian_filter(rng.normal(0,1,(H//4,W//4)),3); n=np.kron(n,np.ones((4,4)))[:H,:W]
    a*=1+n[...,None]*0.18
    img=Image.fromarray(np.clip(a,0,255).astype(np.uint8)).convert('RGBA')
    # embers
    e=Image.new('RGBA',(W,H),(0,0,0,0)); d2=ImageDraw.Draw(e)
    for _ in range(int(W*H/30000)):
        x,y=rng.uniform(0,W),rng.uniform(0,H)**1.0
        y=H-(rng.uniform(0,1)**1.6)*H
        r=rng.uniform(0.8,2.4)*W/2560*2
        c=(255,int(rng.uniform(110,190)),int(rng.uniform(20,60)),int(rng.uniform(70,200)))
        d2.ellipse((x-r,y-r,x+r,y+r),fill=c)
    eg=e.filter(ImageFilter.GaussianBlur(W/1100)); img.alpha_composite(eg); img.alpha_composite(e)
    return img

def gold3d(txt,size,depth=None):
    font=ImageFont.truetype(FONT,size)
    bb=font.getbbox(txt); w,h=bb[2]+8,bb[3]+8
    depth=depth or max(3,size//14)
    pad=depth+size//3
    m=Image.new('L',(w+2*pad,h+2*pad),0); ImageDraw.Draw(m).text((pad,pad),txt,font=font,fill=255)
    M=np.array(m).astype(float)/255; H,W=M.shape
    out=Image.new('RGBA',(W,H),(0,0,0,0))
    # outer glow
    gl=Image.new('RGBA',(W,H),(255,120,30,0)); gl.putalpha(m.filter(ImageFilter.GaussianBlur(size/6)).point(lambda v:int(v*.45))); out.alpha_composite(gl)
    # drop shadow
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(size/14)).point(lambda v:int(v*.8)))
    out.alpha_composite(sh,(0,int(depth*1.8)))
    # extrusion
    cols=[(194,88,10),(154,63,7),(122,46,5),(90,32,3),(61,21,2)]
    for k in range(depth,0,-1):
        c=cols[min(len(cols)-1,int((k-1)/depth*len(cols)))]
        layer=Image.new('RGBA',(W,H),c+(255,)); layer.putalpha(m)
        out.alpha_composite(layer,(0,k))
    # face: gradient + hammered
    ys=np.where(M.any(1))[0]; y0,y1=ys.min(),ys.max()
    t=np.clip((np.arange(H)-y0)/max(1,y1-y0),0,1)[:,None]*np.ones((1,W))
    stops=[(0,(255,244,201)),(.2,(255,215,110)),(.42,(255,171,46)),(.62,(232,101,15)),(.8,(255,154,46)),(1,(255,224,138))]
    col=np.zeros((H,W,3))
    for i in range(len(stops)-1):
        p0,c0=stops[i];p1,c1=stops[i+1];sel=(t>=p0)&(t<=p1);f=((t-p0)/(p1-p0))[...,None]
        col[sel]=(np.array(c0)*(1-f)+np.array(c1)*f)[sel]
    n=ndimage.gaussian_filter(rng.normal(0,1,(H,W)),size/40)
    gy,gx=np.gradient(n); shade=np.clip(0.5+(-gy-gx)*size*0.9,0,1)
    col=col*(0.82+0.32*shade[...,None])
    face=Image.fromarray(np.dstack([np.clip(col,0,255),M*255]).astype(np.uint8))
    out.alpha_composite(face)
    return out.crop(out.getbbox())

def wordmark(size):
    f1=gold3d('FORGE',size)
    two=Image.open(B+'logo3/F2F-two.png').convert('RGBA')
    th=int(size*1.95); two=two.resize((int(two.width*th/two.height),th),Image.LANCZOS)
    tw=Image.new('RGBA',(two.width+40,two.height+40),(0,0,0,0))
    s=Image.new('RGBA',two.size,(0,0,0,0)); s.putalpha(two.split()[3].filter(ImageFilter.GaussianBlur(size/16)).point(lambda v:int(v*.75)))
    tw.alpha_composite(s,(20+size//30,20+size//14)); tw.alpha_composite(two,(20,20))
    gap=-int(size*.16)
    W=f1.width*2+tw.width+2*gap; H=max(f1.height,tw.height)
    c=Image.new('RGBA',(W,H),(0,0,0,0))
    cy=H//2
    c.alpha_composite(f1,(0,cy-f1.height//2+size//10))
    c.alpha_composite(tw,(f1.width+gap,cy-tw.height//2))
    c.alpha_composite(f1,(f1.width+tw.width+2*gap,cy-f1.height//2+size//10))
    return c.crop(c.getbbox())

def text(draw,xy,s,size,fill,font=FONT,anchor='la'):
    draw.text(xy,s,font=ImageFont.truetype(font,size),fill=fill,anchor=anchor)

TAG1="Just a couple of messed-up guys, livin’ in a messed-up world,"
TAG2="talkin’ about how we do it all for the glory of God."
ITAL='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf'
shield=Image.open(B+'logo3/F2F-logo-glow.png').convert('RGBA')

def youtube():
    W,H=2560,1440; img=background(W,H,(W/2-420,H/2))
    # safe area 1546x423 centered
    sx0=(W-1546)//2; sy0=(H-423)//2
    sh=shield.copy(); sh.thumbnail((470,470),Image.LANCZOS)
    img.alpha_composite(sh,(sx0+10,H//2-sh.height//2))
    wm=wordmark(118); wm.thumbnail((960,400),Image.LANCZOS)
    tx=sx0+500; img.alpha_composite(wm,(tx,sy0+40))
    d=ImageDraw.Draw(img)
    y=sy0+40+wm.height+18
    text(d,(tx+4,y),TAG1,29,(236,230,222),ITAL); text(d,(tx+4,y+40),TAG2,29,(236,230,222),ITAL)
    text(d,(tx+4,y+98),"WITH JEFF NEEDHAM & TYLER JONES  ·  FORGE2FORGE.COM",26,(255,166,43))
    return img

def facebook():
    W,H=1640,624; img=background(W,H,(W/2-300,H/2))
    sh=shield.copy(); sh.thumbnail((430,430),Image.LANCZOS)
    x0=230; img.alpha_composite(sh,(x0,H//2-sh.height//2-10))
    wm=wordmark(96); wm.thumbnail((820,330),Image.LANCZOS)
    tx=x0+470; ty=150; img.alpha_composite(wm,(tx,ty))
    d=ImageDraw.Draw(img); y=ty+wm.height+16
    text(d,(tx+4,y),TAG1,27,(236,230,222),ITAL); text(d,(tx+4,y+37),TAG2,27,(236,230,222),ITAL)
    text(d,(tx+4,y+92),"WITH JEFF NEEDHAM & TYLER JONES  ·  FORGE2FORGE.COM",23,(255,166,43))
    return img

yt=youtube(); yt.convert('RGB').save(B+'brand/youtube-banner-2560x1440.png')
fb=facebook(); fb.convert('RGB').save(B+'brand/facebook-cover-1640x624.png')
# previews with safe areas
p=yt.convert('RGB').copy(); dr=ImageDraw.Draw(p); dr.rectangle(((2560-1546)//2,(1440-423)//2,(2560+1546)//2,(1440+423)//2),outline=(80,200,255),width=4)
p.resize((1280,720)).save('/tmp/yt.jpg',quality=85)
fb.convert('RGB').resize((1230,468)).save('/tmp/fb.jpg',quality=85)
