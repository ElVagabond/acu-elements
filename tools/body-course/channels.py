"""Places the points and traces the course of each channel and vessel on the MakeHuman base mesh (right side, -x).
Arm channels are defined here; legs_points.py and legs_routes.py add the leg channels, CV and GV.
Writes build/data.json: {pts:{id:[pos,normal]}, chans:{CH:[{style,pts}]}} in mesh units (decimetres)."""
import sys,json,os,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from mhbody import Body
b=Body(); J=b.J
n=lambda v:np.asarray(v,float)/np.linalg.norm(v)
orth=lambda v,a:n(np.asarray(v,float)-a*np.dot(v,a))
lerp=lambda a,c,t:np.asarray(a,float)+(np.asarray(c,float)-np.asarray(a,float))*t
mix=lambda *pairs:n(sum(np.asarray(v,float)*w for v,w in pairs))
A=np.asarray
j=lambda k:J[k+'____head']; jt=lambda k:J[k+'____tail']
# ---------- frames ----------
S=j('upperarm01.R'); E=j('lowerarm01.R'); W=j('wrist.R')
f=n(W-E); u=n(E-S)
r=orth(j('finger1-1.R')-j('finger5-1.R'),f)                          # toward the thumb
curl=orth(jt('finger2-3.R')-j('finger2-1.R'),n(j('finger2-2.R')-j('finger2-1.R')))
pn=n(np.cross(f,r)); dor=-pn if np.dot(pn,curl)>0 else pn; pal=-dor; uln=-r
a=orth(f,u); l=n(np.cross(u,a)); l=l if l[0]<0 else -l; med=-l; post=-a      # at the elbow: crease side, lateral, medial, back
cunF=np.linalg.norm(E-W)/12; cunU=(np.linalg.norm(E-S)-0.45)/9
NIP=A([-0.694,3.809,1.593]); cunB=abs(NIP[0])/4                       # nipple is 4 cun from the midline
def finger(nm):  # phalanx segments, base to tip
    p=[j(f'finger{nm}-1.R'),j(f'finger{nm}-2.R'),j(f'finger{nm}-3.R'),jt(f'finger{nm}-3.R')]
    return [(p[i],p[i+1]) for i in range(3)]
META={2:'metacarpal1.R',3:'metacarpal2.R',4:'metacarpal3.R',5:'metacarpal4.R'}
def meta(nm): return j(META[nm]),j(f'finger{nm}-1.R')
def seg_frame(s):
    ax=n(s[1]-s[0]); return ax,orth(dor,ax),orth(r,ax)
P={}
def put(k,o,d):
    h=b.ray(o,d); assert h is not None,k; P[k]=(h[0],h[1])
def put_out(k,target,d,back=3):
    d=n(d); h=b.ray(A(target,float)+d*back,-d); assert h is not None,k; P[k]=(h[0],h[1])
def nail(k,nm,side):   # side +1 radial corner, -1 ulnar corner
    s=finger(nm)[2]; ax,nl,rd=seg_frame(s); put(k,lerp(*s,0.55),mix((rd*side,0.82),(nl,0.57)))
def forearm(k,cun_from_wrist,dw,de):
    t=cun_from_wrist/12; put(k,W+(E-W)*t,mix((dw,1-t),(de,t)))
def upper(k,cun_above_elbow,d): put(k,E-u*cun_above_elbow*cunU,d)
# thumb frame: radial = away from the index finger
th=finger(1); thax=n(th[2][1]-th[2][0]); thrad=orth(th[2][0]-j('finger2-1.R'),thax)
# ---------- shared landmarks ----------
put('GV14',J['neck01____head'],[0,0.3,-1])
put('ST12',A([-0.75,5.4,0.1]),[0,0.7,0.7])
put('GB21',A([-0.85,5.55,0.0]),[0,1,0.05])
put_out('ST4',[-0.3,6.62,1.3],[-0.3,0,1]); put_out('GV26',[0,6.78,1.5],[0,0,1])
put_out('GB1',[-0.5,7.33,1.15],[-0.75,0,0.65],back=1.5)
put_out('BL1',[-0.13,7.3,1.35],[-0.15,0,1],back=1.5)
put_out('CV12',[0,3.15,1.0],[0,0,1])
# ---------- LI ----------
d5=mix((r,0.75),(dor,0.65)); d11=mix((l,0.85),(a,0.5))
nail('LI1',2,+1)
s=finger(2)[0]; ax,nl,rd=seg_frame(s); put('LI2',lerp(*s,0.15),mix((rd,1),(nl,0.15)))
m=meta(2); ax,nl,rd=seg_frame(m); put('LI3',lerp(*m,0.8),mix((rd,1),(nl,0.1)))
put('LI4',lerp(*m,0.45)+rd*0.1,mix((nl,0.85),(rd,0.45)))
put('LI5',W-f*0.04,d5)
for k,c in [('LI6',3),('LI7',5),('LI8',8),('LI9',9),('LI10',10)]: forearm(k,c,d5,d11)
put('LI11',E,d11); upper('LI12',1,mix((l,0.9),(a,-0.3))); upper('LI13',3,mix((l,0.95),(a,0.1))); upper('LI14',7,mix((l,0.85),(a,0.35)))
put('LI15',S,[-0.7,0.3,0.55]); put('LI16',S+A([0.45,0.15,-0.25]),[-0.1,1,-0.2])
put('LI18',A([0,5.97,0.2]),[-0.8,0,0.6]); put('LI17',A([0,5.77,0.2]),[-0.92,0,0.4])
put_out('LI19',[0.16,6.78,1.45],[0.1,0,1]); put_out('LI20',[0.22,6.88,1.4],[0.25,0,1])
# ---------- LU ----------
dLUw=mix((pal,0.65),(r,0.75)); dLUe=mix((a,0.9),(l,0.45))
put_out('LU2',[-6*cunB,5.28,0.6],[-0.05,0.15,1]); put_out('LU1',[-6*cunB,5.08,0.6],[-0.05,0.05,1])
upper('LU3',6,mix((a,0.8),(l,0.55))); upper('LU4',5,mix((a,0.8),(l,0.55)))
put('LU5',E,dLUe); forearm('LU6',5,dLUw,dLUe)
put('LU7',W-(W-E)*0.0+(E-W)*(1.5/12),mix((r,0.9),(pal,0.3)))
forearm('LU8',1,dLUw,dLUe); put('LU9',W-f*0.02,dLUw)
put('LU10',lerp(th[0][0],th[0][1],0.5),mix((orth(thrad,n(th[0][1]-th[0][0])),0.7),(orth(pal,n(th[0][1]-th[0][0])),0.7)))
put('LU11',lerp(*th[2],0.55),mix((thrad,0.9),(orth(dor,thax),0.45)))
# ---------- HT ----------
dHTw=mix((pal,0.6),(uln,0.8)); dHTe=mix((med,0.85),(a,0.45))
put('HT1',A([-1.38,4.95,0.15]),[0,-1,0])
upper('HT2',3,mix((med,0.8),(a,0.5))); put('HT3',E,dHTe)
for k,c in [('HT4',1.5),('HT5',1),('HT6',0.5)]: forearm(k,c,dHTw,dHTe)
put('HT7',W-f*0.02,dHTw)
m4,m5=meta(4),meta(5); mid=(lerp(*m4,0.7)+lerp(*m5,0.7))/2; ax=n(m5[1]-m5[0]); put('HT8',mid,orth(pal,ax))
nail('HT9',5,+1)
# ---------- PC ----------
dPCw=pal; dPCe=mix((a,0.95),(med,0.25))
put_out('PC1',[NIP[0]-cunB,NIP[1]+0.05,1.2],[-0.35,0,1])
upper('PC2',7,a); put('PC3',E,dPCe)
for k,c in [('PC4',5),('PC5',3),('PC6',2)]: forearm(k,c,dPCw,dPCe)
put('PC7',W-f*0.02,dPCw)
m2,m3=meta(2),meta(3); mid=(lerp(*m2,0.62)+lerp(*m3,0.62))/2; ax=n(m3[1]-m3[0]); put('PC8',mid,orth(pal,ax))
s=finger(3)[2]; put('PC9',lerp(*s,0.8),n(s[1]-s[0]))
# ---------- SI ----------
dSIw=mix((uln,0.85),(dor,0.45)); dSIe=mix((post,0.65),(med,0.75))
nail('SI1',5,-1)
s=finger(5)[0]; ax,nl,rd=seg_frame(s); put('SI2',lerp(*s,0.15),mix((-rd,1),(nl,0.1)))
m=meta(5); ax,nl,rd=seg_frame(m); put('SI3',lerp(*m,0.8),mix((-rd,1),(nl,0.05)))
put('SI4',lerp(*m,0.12),mix((-rd,1),(nl,0.15)))
put('SI5',W-f*0.02,mix((uln,0.9),(dor,0.3)))
forearm('SI6',1,mix((dor,0.75),(uln,0.65)),dSIe); forearm('SI7',5,dSIw,dSIe)
put('SI8',E,dSIe)
put('SI9',S+A([0.1,-0.75,-0.1]),[-0.25,-0.05,-1]); put('SI10',S+A([0.1,-0.1,-0.15]),[-0.25,0.1,-1])
put('SI11',A([-0.85,4.85,-0.2]),[0,0,-1]); put('SI12',A([-0.85,5.45,-0.15]),[0,0.3,-1]); put('SI13',A([-0.55,5.4,-0.15]),[0,0.3,-1])
put('SI14',A([-3*cunB,5.75,-0.1]),[0,0.25,-1]); put('SI15',A([-2*cunB,5.92,-0.05]),[0,0.3,-1])
put('SI16',A([0,5.97,0.1]),[-1,0,-0.15]); put('SI17',A([0,6.5,0.35]),[-1,0,0.1])
put_out('SI18',[-0.42,7.08,1.2],[-0.45,0,1],back=1.5); put_out('SI19',[-0.62,7.1,0.62],[-1,0,0.15],back=1.0)
# ---------- TB ----------
dTBw=dor; dTBe=post
nail('TB1',4,-1)
mid=(j('finger4-1.R')+j('finger5-1.R'))/2-n(j('finger4-2.R')-j('finger4-1.R'))*0.05; put_out('TB2',mid,dor,back=0.8)
mid=(lerp(*meta(4),0.72)+lerp(*meta(5),0.72))/2; put('TB3',mid,dor)
put('TB4',W-f*0.02+uln*0.03,mix((dor,0.95),(uln,0.2)))
for k,c in [('TB5',2),('TB6',3),('TB8',4),('TB9',7)]: forearm(k,c,dTBw,dTBe)
forearm('TB7',3,mix((dor,0.7),(uln,0.7)),mix((post,0.7),(med,0.7)))
upper('TB10',1,post); upper('TB11',2,post); upper('TB12',4.5,mix((post,0.95),(l,0.2))); upper('TB13',6.5,mix((post,0.85),(l,0.45)))
put('TB14',S+A([0,0.1,-0.05]),[-0.75,0.2,-0.6]); put('TB15',A([-0.75,5.55,-0.15]),[0,0.55,-0.85])
put('TB16',A([0,6.4,0.0]),[-1,0,-0.3]); put_out('TB17',[-0.62,6.78,0.3],[-1,0,-0.25],back=1.0)
put_out('TB18',[-0.66,6.98,0.2],[-1,0,-0.45],back=1.0); put_out('TB19',[-0.7,7.3,0.16],[-1,0.1,-0.45],back=1.0)
put_out('TB20',[-0.7,7.66,0.32],[-1,0.25,0],back=1.0)
put_out('TB21',[-0.65,7.24,0.66],[-1,0,0.2],back=1.0); put_out('TB22',[-0.62,7.36,0.78],[-1,0.1,0.25],back=1.0)
put_out('TB23',[-0.5,7.52,1.15],[-0.6,0.1,0.8],back=1.5)
# internal landmarks (inside the body)
IN={'heart':A([0.12,4.25,0.45]),'lung':A([-0.55,4.5,0.35]),'throat':A([0,6.0,0.25]),'navel':A([0,2.55,0.6]),'stomach':A([0,3.25,0.65]),
    'chest':A([0,4.3,0.5]),'eye':A([-0.3,7.28,0.95]),'cv12':P['CV12'][0]-A([0,0,0.35])}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'legs_points.py')).read())
# ---------- tracing ----------
def wp_ray(o,d): h=b.ray(o,d); assert h is not None; return (h[0],h[1])
def wp_out(t,d,back=3): d=n(d); h=b.ray(A(t,float)+d*back,-d); assert h is not None; return (h[0],h[1])
def trace(ws,step=0.06,lift=0.3):
    out=[]
    for (p0,n0),(p1,n1) in zip(ws[:-1],ws[1:]):
        k=max(2,int(np.ceil(np.linalg.norm(p1-p0)/step)))
        for i in range(k):
            t=i/k; p=p0+(p1-p0)*t; nn=n(n0*(1-t)+n1*t); h=b.ray(p+nn*lift,-nn)
            out.append(h[0] if h is not None else p)
    out.append(ws[-1][0]); out=np.array(out)
    for _ in range(2): out[1:-1]=(out[:-2]+2*out[1:-1]+out[2:])/4
    return out
def straight(ws,step=0.1):
    out=[]
    for p0,p1 in zip(ws[:-1],ws[1:]):
        k=max(2,int(np.ceil(np.linalg.norm(p1-p0)/step)))
        out+= [p0+(p1-p0)*i/k for i in range(k)]
    out.append(ws[-1]); return np.array(out)
g=lambda k:P[k]; seq=lambda *ks:[P[k] for k in ks]
def ua(cun,d): return wp_ray(E-u*cun*cunU,d)
CH={}
CH['LI']=[('surface',trace(seq('LI1','LI2','LI3','LI4','LI5','LI6','LI7','LI8','LI9','LI10','LI11','LI12','LI13','LI14','LI15')+[wp_ray(S+A([0.2,0.1,-0.1]),[-0.3,1,0.05]),g('LI16')],lift=0.25)),
  ('connect',trace([g('LI16'),wp_ray(A([-0.7,5.75,-0.1]),[0,1,-0.3]),g('GV14'),wp_ray(A([-0.35,5.85,0.0]),[-0.5,1,0]),wp_ray(A([-0.6,5.6,0.2]),[-0.2,1,0.4]),g('ST12')])),
  ('surface',trace(seq('ST12','LI17','LI18'))),
  ('connect',trace([g('LI18'),wp_out([-0.62,6.25,0.85],[-0.7,0,0.7]),wp_out([-0.52,6.5,1.05],[-0.6,0,0.8]),g('ST4')])),
  ('surface',trace([g('ST4'),wp_out([-0.18,6.72,1.5],[-0.2,0,1]),g('GV26'),g('LI19'),g('LI20')],step=0.03,lift=0.2)),
  ('internal',straight([P['ST12'][0],IN['lung'],IN['chest'],IN['navel']]))]
CH['LU']=[('internal',straight([IN['cv12'],IN['navel'],IN['stomach'],IN['lung'],IN['throat'],P['LU1'][0]])),
  ('surface',trace(seq('LU1','LU2')+[wp_ray(S+A([0.05,-0.1,0.1]),[-0.3,0,1]),ua(7.5,mix((a,0.8),(l,0.55)))]+seq('LU3','LU4','LU5','LU6','LU7','LU8','LU9','LU10','LU11'),lift=0.25)),
  ('connect',trace([g('LU7'),wp_ray(W+(E-W)*0.05,mix((r,0.6),(dor,0.8))),g('LI4'),g('LI3'),g('LI2'),g('LI1')],lift=0.25))]
CH['HT']=[('internal',straight([IN['heart'],IN['chest'],IN['navel']])),('internal',straight([IN['heart'],IN['throat'],IN['eye']])),
  ('internal',straight([IN['heart'],IN['lung'],P['HT1'][0]])),
  ('surface',trace(seq('HT1')+[ua(6,mix((med,0.8),(a,0.4)))]+seq('HT2','HT3','HT4','HT5','HT6','HT7')+[wp_ray(lerp(*meta(5),0.25),orth(pal,n(meta(5)[1]-meta(5)[0])))]+seq('HT8')+
    [wp_ray(lerp(*finger(5)[0],0.5),mix((orth(pal,n(finger(5)[0][1]-finger(5)[0][0])),0.5),(seg_frame(finger(5)[0])[2],0.85))),wp_ray(lerp(*finger(5)[1],0.5),seg_frame(finger(5)[1])[2])]+seq('HT9'),lift=0.25))]
CH['PC']=[('internal',straight([IN['chest'],IN['stomach'],IN['navel']])),('internal',straight([IN['chest'],P['PC1'][0]])),
  ('surface',trace(seq('PC1')+[wp_out([-1.2,4.55,1.0],[-0.4,0.2,1],back=1.5),ua(8.5,a)]+seq('PC2')+[ua(4,a)]+seq('PC3','PC4','PC5','PC6','PC7','PC8')+
    [wp_ray(lerp(*finger(3)[0],0.5),orth(pal,n(finger(3)[0][1]-finger(3)[0][0]))),wp_ray(lerp(*finger(3)[1],0.5),orth(pal,n(finger(3)[1][1]-finger(3)[1][0])))]+seq('PC9'),lift=0.25)),
  ('connect',trace([g('PC8'),wp_ray(lerp(*finger(4)[0],0.3),mix((orth(pal,n(finger(4)[0][1]-finger(4)[0][0])),0.6),(-seg_frame(finger(4)[0])[2],0.8))),
    wp_ray(lerp(*finger(4)[1],0.5),-seg_frame(finger(4)[1])[2]),g('TB1')],lift=0.2))]
CH['SI']=[('surface',trace(seq('SI1')+[wp_ray(lerp(*finger(5)[1],0.5),mix((-seg_frame(finger(5)[1])[2],1),(seg_frame(finger(5)[1])[1],0.1)))]+seq('SI2','SI3','SI4','SI5','SI6','SI7','SI8')+
    [ua(3,mix((post,0.75),(med,0.55))),ua(6.5,mix((post,0.9),(med,0.3)))]+seq('SI9','SI10','SI11','SI12','SI13','SI14','SI15'),lift=0.25)),
  ('connect',trace([g('SI15'),g('GV14'),wp_ray(A([-0.35,5.85,0.0]),[-0.5,1,0]),wp_ray(A([-0.6,5.6,0.2]),[-0.2,1,0.4]),g('ST12')])),
  ('internal',straight([P['ST12'][0],IN['heart'],IN['stomach'],IN['navel']])),
  ('surface',trace(seq('ST12','SI16','SI17')+[wp_out([-0.62,6.85,0.95],[-0.8,0,0.6],back=1.5)]+seq('SI18','GB1')+[wp_out([-0.62,7.3,0.85],[-1,0,0.3],back=1.0)]+seq('SI19'),lift=0.25)),
  ('connect',trace(seq('SI18')+[wp_out([-0.26,7.15,1.35],[-0.2,0,1],back=1.5)]+seq('BL1'),lift=0.2))]
CH['TB']=[('surface',trace(seq('TB1')+[wp_ray(lerp(*finger(4)[1],0.5),mix((-seg_frame(finger(4)[1])[2],0.8),(seg_frame(finger(4)[1])[1],0.6)))]+seq('TB2','TB3','TB4','TB5','TB6','TB7','TB8','TB9','TB10','TB11','TB12','TB13','TB14','TB15'),lift=0.25)),
  ('connect',trace(seq('TB15','GB21')+[wp_ray(A([-0.6,5.6,0.2]),[-0.2,1,0.4])]+seq('ST12'))),
  ('internal',straight([P['ST12'][0],IN['chest'],IN['stomach'],IN['navel']])),
  ('surface',trace(seq('ST12','TB16','TB17','TB18','TB19','TB20'),lift=0.25)),
  ('connect',trace(seq('TB17')+[wp_out([-0.7,7.0,0.62],[-1,0,0.15],back=1.0)]+seq('TB21'),lift=0.2)),
  ('surface',trace(seq('TB21','TB22')+[wp_out([-0.55,7.45,0.98],[-0.85,0.1,0.5],back=1.2)]+seq('TB23'),lift=0.2))]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'legs_routes.py')).read())
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)),'build'),exist_ok=True)
json.dump({'pts':{k:[v[0].tolist(),v[1].tolist()] for k,v in P.items()},
           'chans':{c:[{'style':s,'pts':np.asarray(p).tolist()} for s,p in segs] for c,segs in CH.items()}},open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'build','data.json'),'w'))
print('points',len(P),'| segs',{c:len(v) for c,v in CH.items()})
