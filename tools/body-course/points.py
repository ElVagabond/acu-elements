import sys,json,numpy as np; sys.path.insert(0,'.')
from mhbody import Body
b=Body(); J=b.J
n=lambda v:np.asarray(v,float)/np.linalg.norm(v)
orth=lambda v,a:n(np.asarray(v,float)-a*np.dot(v,a))
lerp=lambda a,c,t:a+(c-a)*t
mix=lambda *pairs:n(sum(np.asarray(v,float)*w for v,w in pairs))
S=J['upperarm01.R____head'];E=J['lowerarm01.R____head'];W=J['wrist.R____head']
f=n(W-E); u=n(E-S)
r=orth(J['finger1-1.R____head']-J['finger5-1.R____head'],f)
p0,p1,p2,p3,tip=(J[k] for k in ['finger2-1.R____head','finger2-2.R____head','finger2-3.R____head','finger2-3.R____tail','finger2-3.R____tail'])
curl=orth(tip-p0,n(p1-p0)); pn=n(np.cross(f,r)); dorsal=-pn if np.dot(pn,curl)>0 else pn
meta=J['metacarpal2.R____head']
ant=orth(f,u); lat=n(np.cross(u,ant)); lat=lat if lat[0]<0 else -lat
cunF=np.linalg.norm(E-W)/12; cunU=(np.linalg.norm(E-S)-0.45)/9
def dist_ax(a,c): return n(c-a)
def put_out(k,target,d):
    # cast from outside the skin inward, so cavities behind the face are never hit first
    d=n(d); h=b.ray(np.asarray(target,float)+d*3,-d); assert h is not None,k; P[k]=(h[0],h[1])
P={}; SIDE={}
def put(k,o,d):
    h=b.ray(o,d); assert h is not None,k; P[k]=(h[0],h[1])
dax=dist_ax(p2,p3); put('LI1',lerp(p2,p3,0.55),mix((orth(r,dax),0.8),(orth(dorsal,dax),0.6)))
pax=dist_ax(p0,p1); put('LI2',lerp(p0,p1,0.15),mix((orth(r,pax),1),(orth(dorsal,pax),0.15)))
max_=dist_ax(meta,p0); put('LI3',lerp(meta,p0,0.8),mix((orth(r,max_),1),(orth(dorsal,max_),0.1)))
put('LI4',lerp(meta,p0,0.45)+orth(r,max_)*0.1,mix((orth(dorsal,max_),0.85),(orth(r,max_),0.45)))
d5=mix((r,0.75),(dorsal,0.65)); d11=mix((lat,0.85),(ant,0.5))
put('LI5',W+(-f)*0.04,d5)
for k,c in [('LI6',3),('LI7',5),('LI8',8),('LI9',9),('LI10',10)]:
    t=c/12; put(k,W+(E-W)*t,mix((d5,1-t),(d11,t)))
put('LI11',E,d11)
put('LI12',E-u*cunU,mix((lat,0.9),(ant,-0.3)))
put('LI13',E-u*3*cunU,mix((lat,0.95),(ant,0.1)))
put('LI14',E-u*7*cunU,mix((lat,0.85),(ant,0.35)))
put('LI15',S,[-0.7,0.3,0.55])
put('LI16',S+np.array([0.45,0.15,-0.25]),[-0.1,1,-0.2])
put('GV14',J['neck01____head'],[0,0.3,-1])
put('ST12',np.array([-0.75,5.4,0.1]),[0,0.7,0.7])
put('LI18',np.array([0,5.97,0.2]),[-0.8,0,0.6])
put('LI17',np.array([0,5.77,0.2]),[-0.92,0,0.4])
put_out('ST4',[-0.3,6.62,1.3],[-0.3,0,1])
put_out('GV26',[0,6.78,1.5],[0,0,1])
put_out('LI19',[0.16,6.78,1.45],[0.1,0,1])
put_out('LI20',[0.22,6.88,1.4],[0.25,0,1])
json.dump({k:[v[0].tolist(),v[1].tolist()] for k,v in P.items()},open('build/points.json','w'))
PTS=P
if __name__=='__main__':
    C={'LI1':0xeeeeee,'LI2':0x2b6fd6,'LI3':0x3f9b4b,'LI5':0xd8402f,'LI11':0xe0a81c}
    json.dump({'pts':[{'p':v[0].tolist(),'r':0.045,'c':C.get(k,0xff00ff if not k.startswith('LI') else 0x222222)} for k,v in P.items()]},open('build/dbg.json','w'))
    print({k:np.round(v[0],2).tolist() for k,v in P.items()})
