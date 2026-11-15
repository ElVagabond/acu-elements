"""Writes channels.html (all channel courses) from build/data.json, meta.py and channels_template.html."""
import json,base64,os,sys,numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from mhbody import load
import meta
sys.path.insert(0,HERE)
REPO=os.environ.get('REPO',os.path.join(HERE,'..','..'))
ATLAS=os.environ.get('SHU_ATLAS_POINTS','')            # optional: data/points.json from arm-pz/acupuncture-element-points
V,F,_=load(); V=V*10; SC=300
q=np.round(V*SC).astype('<i2')
mesh={'s':SC,'q':base64.b64encode(q.tobytes()).decode(),'i':base64.b64encode(F.astype('<u2').tobytes()).decode()}
D=json.load(open(os.path.join(HERE,'build','data.json')))
cm=lambda p:[round(c*10,2) for c in p]
pts={k:[cm(v[0]),[round(c,3) for c in v[1]]] for k,v in D['pts'].items()}
chans={c:[{'style':s['style'],'pts':[cm(p) for p in s['pts']]} for s in segs] for c,segs in D['chans'].items()}
LI=json.load(open(os.path.join(HERE,'li_points.json')))
INFO=meta.build(LI,ATLAS if ATLAS else os.path.join(HERE,'shu_points.json'))
TXT=json.load(open(os.path.join(HERE,'courses.json')))
CH={
 'LU':dict(name='Lung',han='手太陰肺經',group='Metal',ghan='金',line='#5a49b8',n=11,refs=['CV12','LI1'],home=[-30,6,76,[-20,42,6]],hand=[-50,15,'LU9','LU11'],head=[-25,5,34,[-8,48,8]],handLabel='Hand',headLabel='Chest'),
 'LI':dict(name='Large Intestine',han='手陽明大腸經',group='Metal',ghan='金',line='#0b7f8a',n=20,refs=['GV14','ST12','ST4','GV26'],home=[-34,6,76,[-20,42,6]],hand=[-62,12,'LI5','LI1'],head=[-28,4,17,[-2,63,10]],handLabel='Hand',headLabel='Face'),
 'KI':dict(name='Kidney',han='足少陰腎經',group='Water',ghan='水',line='#3a3f9e',n=27,refs=['BL67'],home=[22,3,150,[-6,-17,6]],hand=[70,-40,'KI3','KI1'],head=[0,4,62,[-3,24,8]],handLabel='Foot',headLabel='Trunk'),
 'BL':dict(name='Bladder',han='足太陽膀胱經',group='Water',ghan='水',line='#2b7fb8',n=67,refs=['GV20'],home=[-170,5,175,[-8,0,-4]],hand=[-115,12,'BL60','BL67'],head=[-155,35,30,[-2,76,2]],handLabel='Foot',headLabel='Head'),
 'LR':dict(name='Liver',han='足厥陰肝經',group='Wood',ghan='木',line='#2f8a3c',n=14,refs=[],home=[12,5,150,[-6,-17,6]],hand=[0,40,'LR4','LR1'],head=[-10,4,62,[-5,22,8]],handLabel='Foot',headLabel='Trunk'),
 'GB':dict(name='Gallbladder',han='足少陽膽經',group='Wood',ghan='木',line='#6a9a1a',n=44,refs=['ST12','LR1'],home=[-90,5,175,[-12,0,0]],hand=[-80,25,'GB40','GB44'],head=[-75,10,30,[-4,74,4]],handLabel='Foot',headLabel='Head'),
 'HT':dict(name='Heart',han='手少陰心經',group='Fire',ghan='火',line='#b0306a',n=9,refs=[],home=[0,0,76,[-18,40,6]],hand=[30,-20,'HT7','HT9'],head=[-10,-6,40,[-12,44,6]],handLabel='Hand',headLabel='Chest'),
 'SI':dict(name='Small Intestine',han='手太陽小腸經',group='Fire',ghan='火',line='#6b7a12',n=19,refs=['GV14','ST12','GB1','BL1'],home=[-150,8,78,[-20,46,-2]],hand=[-120,10,'SI5','SI1'],head=[-95,4,22,[-5,66,4]],handLabel='Hand',headLabel='Head'),
 'PC':dict(name='Pericardium',han='手厥陰心包經',group='Fire',ghan='火',line='#c2611f',n=9,refs=['TB1'],home=[-15,2,76,[-18,42,6]],hand=[20,-20,'PC7','PC9'],head=[-15,5,34,[-8,42,8]],handLabel='Hand',headLabel='Chest'),
 'TB':dict(name='Triple Burner',han='手少陽三焦經',group='Fire',ghan='火',line='#2a62b0',n=23,refs=['GB21','ST12'],home=[-130,8,78,[-20,46,0]],hand=[-110,15,'TB4','TB1'],head=[-90,6,20,[-6,70,3]],handLabel='Hand',headLabel='Head'),
 'SP':dict(name='Spleen',han='足太陰脾經',group='Earth',ghan='土',line='#9a6a1f',n=21,refs=[],home=[12,5,150,[-6,-17,6]],hand=[40,15,'SP5','SP1'],head=[-15,4,62,[-6,24,8]],handLabel='Foot',headLabel='Trunk'),
 'ST':dict(name='Stomach',han='足陽明胃經',group='Earth',ghan='土',line='#c9771a',n=45,refs=['BL1','SP1'],home=[-25,5,175,[-10,0,6]],hand=[-30,30,'ST41','ST45'],head=[-25,4,24,[-3,68,8]],handLabel='Foot',headLabel='Face'),
 'CV':dict(name='Conception Vessel',han='任脈',group='Vessels',ghan='奇經',line='#8c2f6e',n=24,refs=['ST1'],home=[-20,5,82,[0,30,8]],hand=[-25,0,'CV22','CV24'],head=[-20,-35,40,[0,4,6]],handLabel='Throat',headLabel='Perineum'),
 'GV':dict(name='Governor Vessel',han='督脈',group='Vessels',ghan='奇經',line='#444f9a',n=28,refs=['CV1'],home=[-160,5,110,[0,38,-3]],hand=[-100,10,'GV20','GV24'],head=[-60,0,24,[0,70,10]],handLabel='Head',headLabel='Face'),
}
out={}
for c,d in CH.items():
    d=dict(d); d['points']=[f'{c}{i}' for i in range(1,d.pop('n')+1)]; d['text']=TXT[c]
    d['sub']=('Midline, ' if c in ('CV','GV') else 'Right side, ')+d['points'][0]+' to '+d['points'][-1]+(' (ends beside the opposite nostril)' if c=='LI' else '')
    out[c]=d
used=sorted(set(k for d in out.values() for k in d["points"]+d["refs"]))
missing=[k for k in used if k not in pts or k not in INFO]; assert not missing,missing
arm=open(os.path.join(REPO,'arm.html')).read(); css=arm[arm.index('<style>')+7:arm.index('</style>')]
t=open(os.path.join(HERE,'channels_template.html')).read()
# markers drawn smaller where points crowd together (closer than 2.2 cm to another point of the same channel)
small=set()
for c,d in out.items():
    ids=d['points']; Pc=np.array([pts[k][0] for k in ids])
    for i,k in enumerate(ids):
        dd=np.linalg.norm(Pc-Pc[i],axis=1); dd[i]=1e9
        if dd.min()<2.2: small.add(k)
t=t.replace('/*CSS*/',css.strip()).replace('/*DATA*/',json.dumps({'mesh':mesh,'pts':{k:pts[k] for k in used},'chans':chans,'small':sorted(small)},separators=(',',':')))
t=t.replace('/*POINTS*/',json.dumps({k:INFO[k] for k in used},ensure_ascii=False)).replace('/*CHANNELS*/',json.dumps(out,ensure_ascii=False))
open(os.path.join(REPO,'channels.html'),'w').write(t)
open(os.path.join(REPO,'li-channel.html'),'w').write('''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Large Intestine Channel</title>
<meta http-equiv="refresh" content="0; url=channels.html#LI"></head>
<body><p>The Large Intestine course has moved to <a href="channels.html#LI">channels.html#LI</a>.</p></body></html>
''')
print('channels.html bytes',len(t.encode()))
