import sys,json,numpy as np; sys.path.insert(0,'.')
import points as PT
from points import b,n,P
def wp_ray(o,d):
    h=b.ray(o,d); assert h is not None; return (h[0],h[1])
def wp_out(target,d):
    d=n(d); h=b.ray(np.asarray(target,float)+d*3,-d); assert h is not None; return (h[0],h[1])
def trace(ws,step=0.06,lift=0.3):
    out=[]
    for (a,na),(c,nc) in zip(ws[:-1],ws[1:]):
        k=max(2,int(np.ceil(np.linalg.norm(c-a)/step)))
        for i in range(k):
            t=i/k; p=a+(c-a)*t; nn=n(na*(1-t)+nc*t)
            h=b.ray(p+nn*lift,-nn)
            out.append(h[0] if h is not None else p)
    out.append(ws[-1][0]); out=np.array(out)
    # light smoothing, keep ends
    for _ in range(2): out[1:-1]=(out[:-2]+2*out[1:-1]+out[2:])/4
    return out
g=lambda k:P[k]
main=[g('LI1'),g('LI2'),g('LI3'),g('LI4'),g('LI5'),g('LI6'),g('LI7'),g('LI8'),g('LI9'),g('LI10'),g('LI11'),g('LI12'),g('LI13'),g('LI14'),g('LI15'),
      wp_ray(PT.S+np.array([0.2,0.1,-0.1]),[-0.3,1,0.05]),g('LI16')]
connect=[g('LI16'),wp_ray(np.array([-0.7,5.75,-0.1]),[0,1,-0.3]),g('GV14'),wp_ray(np.array([-0.35,5.85,0.0]),[-0.5,1,0]),wp_ray(np.array([-0.6,5.6,0.2]),[-0.2,1,0.4]),g('ST12')]
neck=[g('ST12'),g('LI17'),g('LI18')]
cheek=[g('LI18'),wp_out([-0.62,6.25,0.85],[-0.7,0,0.7]),wp_out([-0.52,6.5,1.05],[-0.6,0,0.8]),g('ST4')]
lip=[g('ST4'),wp_out([-0.18,6.72,1.5],[-0.2,0,1]),g('GV26'),g('LI19'),g('LI20')]
segs={'main':trace(main,lift=0.25),'connect':trace(connect),'neck':trace(neck),'cheek':trace(cheek),'lip':trace(lip,step=0.03,lift=0.2)}
json.dump({k:v.tolist() for k,v in segs.items()},open('build/paths.json','w'))
if __name__=='__main__':
    d=json.load(open('build/dbg.json')); cols={'main':0x0b7f8a,'connect':0xaa5500,'neck':0x0b7f8a,'cheek':0xaa5500,'lip':0x0b7f8a}
    d['lines']=[{'pts':v.tolist(),'c':cols[k]} for k,v in segs.items()]; json.dump(d,open('build/dbg.json','w'))
    print({k:len(v) for k,v in segs.items()})
