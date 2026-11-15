import json,os,numpy as np
# MakeHuman data folder (base mesh is CC0): clone https://github.com/makehumancommunity/makehuman and point this at makehuman/data/
MH=os.environ.get('MAKEHUMAN_DATA','makehuman/data').rstrip('/')+'/'
def load():
    V=[];F=[];cur=None
    for line in open(MH+'3dobjs/base.obj'):
        if line.startswith('v '): V.append([float(x) for x in line.split()[1:4]])
        elif line.startswith('g '): cur=line.split()[1]
        elif line.startswith('f ') and cur=='body':
            f=[int(t.split('/')[0])-1 for t in line.split()[1:]]
            F.append([f[0],f[1],f[2]]); 
            if len(f)==4: F.append([f[0],f[2],f[3]])
    V=np.array(V);F=np.array(F)
    used=np.unique(F); remap=-np.ones(len(V),int); remap[used]=np.arange(len(used))
    sk=json.load(open(MH+'rigs/default.mhskel'))
    J={k:V[v].mean(0) for k,v in sk['joints'].items()}
    return V[used],remap[F],J
class Body:
    def __init__(s):
        s.V,s.F,s.J=load()
        A,B,C=(s.V[s.F[:,i]] for i in range(3))
        s.A,s.E1,s.E2=A,B-A,C-A
        fn=np.cross(s.E1,s.E2); s.FN=fn/np.linalg.norm(fn,axis=1,keepdims=True)
        vn=np.zeros_like(s.V)
        for i in range(3): np.add.at(vn,s.F[:,i],fn)
        s.VN=vn/np.linalg.norm(vn,axis=1,keepdims=True)
    def j(s,n): return s.J[n]
    def ray(s,o,d):
        d=np.asarray(d,float); d=d/np.linalg.norm(d); o=np.asarray(o,float)
        p=np.cross(d,s.E2); det=(s.E1*p).sum(1); ok=np.abs(det)>1e-12; inv=np.where(ok,1/np.where(ok,det,1),0)
        tv=o-s.A; u=(tv*p).sum(1)*inv; q=np.cross(tv,s.E1); v=(q*d).sum(1)*inv; t=(s.E2*q).sum(1)*inv
        hit=ok&(u>=0)&(v>=0)&(u+v<=1)&(t>1e-6)
        if not hit.any(): return None
        i=np.argmin(np.where(hit,t,np.inf)); 
        w=np.array([1-u[i]-v[i],u[i],v[i]]); n=(s.VN[s.F[i]]*w[:,None]).sum(0); n/=np.linalg.norm(n)
        return o+d*t[i], n, i
    def closest(s,P):
        # closest point on mesh for each point (brute force over triangles), returns points and normals
        out=[];nout=[]
        for p in np.atleast_2d(P):
            # point-triangle distance (Ericson), vectorised
            a=s.A; ab=s.E1; ac=s.E2; ap=p-a
            d1=(ab*ap).sum(1); d2=(ac*ap).sum(1)
            bp=p-(a+ab); d3=(ab*bp).sum(1); d4=(ac*bp).sum(1)
            cp=p-(a+ac); d5=(ab*cp).sum(1); d6=(ac*cp).sum(1)
            va=d3*d6-d5*d4; vb=d5*d2-d1*d6; vc=d1*d4-d3*d2
            den=va+vb+vc; den=np.where(np.abs(den)<1e-15,1e-15,den)
            v=vb/den; w=vc/den
            res=a+ab*v[:,None]+ac*w[:,None]
            # regions
            m=(d1<=0)&(d2<=0); res[m]=a[m]
            m=(d3>=0)&(d4<=d3); res[m]=(a+ab)[m]
            m=(d6>=0)&(d5<=d6); res[m]=(a+ac)[m]
            vcm=(vc<=0)&(d1>=0)&(d3<=0); t=d1/np.where(d1-d3==0,1,d1-d3); m=vcm&~((d1<=0)&(d2<=0))&~((d3>=0)&(d4<=d3)); res[m]=(a+ab*t[:,None])[m]
            vbm=(vb<=0)&(d2>=0)&(d6<=0); t=d2/np.where(d2-d6==0,1,d2-d6); m=vbm&~((d1<=0)&(d2<=0))&~((d6>=0)&(d5<=d6)); res[m]=(a+ac*t[:,None])[m]
            vam=(va<=0)&((d4-d3)>=0)&((d5-d6)>=0); t=(d4-d3)/np.where((d4-d3)+(d5-d6)==0,1,(d4-d3)+(d5-d6)); m=vam&~((d3>=0)&(d4<=d3))&~((d6>=0)&(d5<=d6)); res[m]=((a+ab)+(ac-ab)*t[:,None])[m]
            dist=np.linalg.norm(res-p,axis=1); i=np.argmin(dist)
            out.append(res[i]); nout.append(s.FN[i])
        return np.array(out),np.array(nout)
