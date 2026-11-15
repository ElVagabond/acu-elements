import json,base64,re,numpy as np
from mhbody import load
V,F,_=load(); V=V*10          # decimetres -> cm
SC=300
q=np.round(V*SC).astype('<i2'); assert np.abs(V*SC).max()<32767
mesh={'s':SC,'q':base64.b64encode(q.tobytes()).decode(),'i':base64.b64encode(F.astype('<u2').tobytes()).decode()}
pts={k:[[round(c*10,2) for c in v[0]],[round(c,3) for c in v[1]]] for k,v in json.load(open('build/points.json')).items()}
paths={k:[[round(c*10,2) for c in p] for p in v] for k,v in json.load(open('build/paths.json')).items()}
# lift lines slightly off the skin along the local normal estimate (towards the outside: use point-to-point smoothing of nothing) -> handled by tube radius
P=[
 ("LI1","Shangyang","商陽","Shang Yang","well","metal",None,"On the radial side of the index finger, about 0.1 cun from the corner of the nail."),
 ("LI2","Erjian","二間","Second Space","spring","water",None,"On the radial side of the index finger, in the hollow just distal to the second knuckle, where the red and white skin meet."),
 ("LI3","Sanjian","三間","Third Space","stream","wood",None,"On the radial side of the hand, in the hollow just proximal to the head of the second metacarpal."),
 ("LI4","Hegu","合谷","Union Valley",None,None,"Yuan-source","On the back of the hand, between the first and second metacarpals, level with the middle of the second metacarpal on its radial side."),
 ("LI5","Yangxi","陽谿","Yang Stream","river","fire",None,"On the radial side of the wrist, in the anatomical snuffbox between the tendons of extensor pollicis longus and brevis."),
 ("LI6","Pianli","偏歷","Veering Passage",None,None,"Luo-connecting","On the line from LI5 to LI11, 3 cun above the wrist crease."),
 ("LI7","Wenliu","溫溜","Warm Flow",None,None,"Xi-cleft","On the line from LI5 to LI11, 5 cun above the wrist crease."),
 ("LI8","Xialian","下廉","Lower Ridge",None,None,None,"On the line from LI5 to LI11, 4 cun below LI11."),
 ("LI9","Shanglian","上廉","Upper Ridge",None,None,None,"On the line from LI5 to LI11, 3 cun below LI11."),
 ("LI10","Shousanli","手三里","Arm Three Li",None,None,None,"On the line from LI5 to LI11, 2 cun below LI11."),
 ("LI11","Quchi","曲池","Pool at the Bend","sea","earth",None,"With the elbow bent, at the outer end of the elbow crease, midway between LU5 and the lateral epicondyle of the humerus."),
 ("LI12","Zhouliao","肘髎","Elbow Bone-Hole",None,None,None,"With the elbow bent, 1 cun above and outside LI11, on the edge of the humerus."),
 ("LI13","Shouwuli","手五里","Arm Five Li",None,None,None,"On the line from LI11 to LI15, 3 cun above LI11."),
 ("LI14","Binao","臂臑","Upper Arm",None,None,None,"At the lower end of the deltoid, on the line from LI11 to LI15, 7 cun above LI11."),
 ("LI15","Jianyu","肩髃","Shoulder Bone",None,None,None,"In front of and below the acromion, in the hollow that appears when the arm is raised."),
 ("LI16","Jugu","巨骨","Great Bone",None,None,None,"On the top of the shoulder, in the hollow between the outer end of the clavicle and the spine of the scapula."),
 ("LI17","Tianding","天鼎","Heaven's Tripod",None,None,None,"On the side of the neck, at the back edge of sternocleidomastoid, 1 cun below LI18."),
 ("LI18","Futu","扶突","Support the Prominence",None,None,None,"On the side of the neck, level with the Adam's apple, between the two heads of sternocleidomastoid."),
 ("LI19","Kouheliao","口禾髎","Mouth Grain Bone-Hole",None,None,None,"On the upper lip, directly below the outer edge of the nostril, level with GV26. On the opposite side of the face from where the channel starts."),
 ("LI20","Yingxiang","迎香","Welcome Fragrance",None,None,"End point","In the groove beside the nose, level with the middle of the outer edge of the nostril. On the opposite side of the face: the channel crosses at GV26."),
]
X=[
 ("GV14","Dazhui","大椎","Great Vertebra","Governor Vessel","Below the spinous process of the seventh neck vertebra. The Large Intestine channel meets the other yang channels here."),
 ("ST12","Quepen","缺盆","Empty Basin","Stomach channel","In the hollow above the middle of the clavicle. A branch goes inward from here to the lung, through the diaphragm, to the large intestine."),
 ("ST4","Dicang","地倉","Earth Granary","Stomach channel","Beside the corner of the mouth. The channel passes here on its way from the lower gums around the upper lip."),
 ("GV26","Shuigou","水溝","Water Trough","Governor Vessel","In the groove of the upper lip, a third of the way down from the nose. The left and right Large Intestine channels cross here."),
]
pl=[]
for c,py,hz,en,shu,el,role,loc in P:
    d={'id':c,'ch':'LI','py':py,'han':hz,'en':en,'loc':loc}
    if shu: d['shu']=shu; d['el']=el
    if role: d['role']=role
    if c in('LI19','LI20'): d['side']='Left (opposite side)'
    pl.append(d)
for c,py,hz,en,role,loc in X: pl.append({'id':c,'ch':c[:2],'py':py,'han':hz,'en':en,'role':role,'loc':loc})
arm=open('../../arm.html').read()
css=arm[arm.index('<style>')+7:arm.index('</style>')]
t=open('li_template.html').read()
t=t.replace('/*CSS*/',css.strip()).replace('/*DATA*/',json.dumps({'mesh':mesh,'pts':pts,'paths':paths},separators=(',',':'))).replace('/*POINTS*/',json.dumps(pl,ensure_ascii=False))
open('../../li-channel.html','w').write(t)
print('bytes',len(t.encode()))
