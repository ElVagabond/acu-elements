CHECK={}
def put(k,o,d,maxd=1.3):
    # ray from inside; if the start is outside the skin (no hit, or a hit too far away), cast a short ray from just outside instead
    o=A(o,float); d=n(d); h=b.ray(o,d)
    if h is None or np.linalg.norm(h[0]-o)>maxd:
        h=b.ray(o+d*0.6,-d); assert h is not None,k
    P[k]=(h[0],h[1]); CHECK[k]=float(np.dot(h[1],d))
# ---------- trunk, head, leg landmarks (right side = -x; y up; z forward; decimetres) ----------
NAV_Y=2.6; PUB_Y=0.8; XIP_Y=3.6
cAbU=(XIP_Y-NAV_Y)/8; cAbL=(NAV_Y-PUB_Y)/5            # abdominal cun above / below the navel
ICS={1:5.05,2:4.64,3:4.22,4:3.81,5:3.45,6:3.09,7:2.73}  # intercostal spaces, front of chest
C7=P['GV14'][0][1]
VERT={'T%d'%i:C7-i*0.2347 for i in range(1,13)}; T12=VERT['T12']
VERT.update({'L%d'%i:T12-i*0.3286 for i in range(1,6)}); VERT.update({'S1':1.30,'S2':1.08,'S3':0.88,'S4':0.70,'CO':0.45})
H=j('upperleg01.R'); K=j('lowerleg01.R'); AK=j('foot.R')
def legax(y):
    if y>=K[1]: t=(H[1]-y)/(H[1]-K[1]); return H+(K-H)*t, n(K-H)
    t=(K[1]-y)/(K[1]-AK[1]); return K+(AK-K)*t, n(AK-K)
def lf(y):
    o,ax=legax(y); fr=orth([0,0,1],ax); la=orth([-1,0,0],ax); return o,fr,la,-la,-fr
def leg(k,y,*w):     # w: pairs of (name,weight) with names fr, la, me, bk
    o,fr,la,me,bk=lf(y); D={'fr':fr,'la':la,'me':me,'bk':bk}
    put(k,o,mix(*[(D[a],x) for a,x in w]))
POP=K[1]+0.0                       # knee crease height
cTh=(0.4-POP)/19; cShL=(POP-AK[1])/16; cShM=(POP-0.35-(AK[1]+0.1))/13
MALM=AK[1]+0.1; MALL=AK[1]
def front(k,x,y,d=(0,0,1)): put_out(k,[x,y,0.5],d,back=3)
def backp(k,x,y,d=(0,0,-1)): put(k,A([x,y,0.0]),d)
# head: angles over the scalp from a centre inside the head
HC=A([0,7.55,0.45])
def ang(p): return np.arctan2(p[1]-HC[1],p[2]-HC[2])
aF=ang(A([0,7.95,1.43])); aB=ang(A([0,6.95,-0.23]))+2*np.pi if ang(A([0,6.95,-0.23]))<0 else ang(A([0,6.95,-0.23]))
def head(k,cun_from_front,lat_cun):
    al=aF+(aB-aF)*cun_from_front/12; be=lat_cun*0.30
    d=A([-np.sin(be),np.cos(be)*np.sin(al),np.cos(be)*np.cos(al)]); h=b.ray(HC+d*2.5,-d); P[k]=(h[0],h[1]); CHECK[k]=float(np.dot(h[1],d))
def headto(k,target):
    d=n(A(target)-HC); h=b.ray(HC+d*2.5,-d); P[k]=(h[0],h[1]); CHECK[k]=float(np.dot(h[1],d))
# toes
def toe(nm,i): return J[f'toe{nm}-{i}.R____head'], J[f'toe{nm}-{i}.R____tail']
UPv=A([0,1,0]); MEDv=A([1,0,0])
def tnail(k,nm,i,side):     # side +1 medial corner, -1 lateral corner
    s=toe(nm,i); ax=n(s[1]-s[0]); put(k,lerp(*s,0.55),mix((orth(MEDv*side,ax),0.82),(orth(UPv,ax),0.57)))
# ---------- ST ----------
put_out('ST1',[-0.31,7.17,1.3],[-0.1,-0.1,1],back=1.5); put_out('ST2',[-0.31,7.04,1.3],[-0.15,0,1],back=1.5); put_out('ST3',[-0.31,6.86,1.3],[-0.2,0,1],back=1.5)
P['ST4']=P['ST4']
put_out('ST5',[-0.52,6.42,0.95],[-0.75,-0.3,0.6],back=1.2); put_out('ST6',[-0.62,6.62,0.75],[-0.9,0,0.4],back=1.2)
put_out('ST7',[-0.7,7.05,0.86],[-1,0,0.25],back=1.0); head('ST8',-0.5,4.5)
put('ST9',A([0,5.97,0.3]),[-0.45,0,0.9]); put('ST10',A([0,5.72,0.3]),[-0.4,0.1,0.92]); put('ST11',A([-0.2,5.5,0.3]),[-0.15,0.45,1])
for k,y in [('ST13',5.25),('ST14',ICS[1]),('ST15',ICS[2]),('ST16',ICS[3]),('ST18',ICS[5])]: front(k,-4*cunB,y,(-0.15,0,1))
put_out('ST17',NIP+A([0,0,0.3]),[0,0,1],back=1)
for i,k in enumerate(['ST19','ST20','ST21','ST22','ST23','ST24']): front(k,-2*cunB,NAV_Y+(6-i)*cAbU)
front('ST25',-2*cunB,NAV_Y)
for i,k in enumerate(['ST26','ST27','ST28','ST29','ST30']): front(k,-2*cunB,NAV_Y-(i+1)*cAbL)
leg('ST31',0.45,('fr',0.9),('la',0.45))
PAT=K[1]+0.5
for k,c in [('ST32',6),('ST33',3),('ST34',2)]: leg(k,PAT+c*cTh,('fr',0.8),('la',0.6))
leg('ST35',POP-0.15,('fr',0.85),('la',0.5)); S35=POP-0.15
for k,c,w in [('ST37',6,0.5),('ST38',8,0.5),('ST39',9,0.5),('ST40',8,0.85)]: leg(k,S35-c*cShL,('fr',0.85),('la',w))
leg('ST36',S35-3*cShL,('fr',0.85),('la',0.5))
put('ST41',AK+A([0,0.0,0.05]),[0,0.25,1])
put('ST42',A([-2.15,-7.8,0.55]),[0,1,0.15]); put('ST43',A([-2.24,-7.9,1.05]),[0,1,0.1]); put_out('ST44',[-2.26,-7.95,1.42],[0,1,0],back=0.6)
tnail('ST45',2,3,-1)
# ---------- SP ----------
tnail('SP1',1,2,+1)
s=toe(1,1); ax=n(s[1]-s[0]); put('SP2',lerp(*s,0.25),mix((orth(MEDv,ax),1),(orth(-UPv,ax),0.2)))
put('SP3',s[0]-ax*0.25,mix((MEDv,1),(-UPv,0.25))); put('SP4',s[0]-ax*0.62+A([0,0.05,0]),mix((MEDv,0.9),(-UPv,0.35)))
put('SP5',AK+A([0.05,-0.25,0.25]),mix((MEDv,0.9),((0,0,1),0.35)))
for k,c in [('SP6',3),('SP7',6)]: leg(k,MALM+c*cShM,('me',1),('bk',0.25))
SP9Y=POP-0.35; leg('SP9',SP9Y,('me',0.9),('bk',0.25)); leg('SP8',SP9Y-3*cShM,('me',1),('bk',0.25))
leg('SP10',PAT+0.3+2*cTh,('me',0.85),('fr',0.5)); leg('SP11',PAT+0.3+8*cTh,('me',0.9),('fr',0.3))
front('SP12',-3.5*cunB,0.78,(-0.2,0.2,1)); front('SP13',-4*cunB,0.92,(-0.25,0.2,1)); front('SP14',-4*cunB,NAV_Y-1.3*cAbL,(-0.3,0,1))
front('SP15',-4*cunB,NAV_Y,(-0.3,0,1)); front('SP16',-4*cunB,NAV_Y+3*cAbU,(-0.3,0,1))
for k,i in [('SP17',5),('SP18',4),('SP19',3),('SP20',2)]: front(k,-6*cunB,ICS[i],(-0.45,0,1))
put('SP21',A([-0.6,3.75,0.25]),[-1,0,0.05])
# ---------- KI ----------
put('KI1',A([-2.25,-7.9,0.8]),[0,-1,0])
put('KI2',A([-2.0,-7.85,0.55]),mix((MEDv,1),(-UPv,0.35)))
put('KI3',AK+A([0,0.0,-0.1]),mix((MEDv,0.75),((0,0,-1),0.65)))
put('KI4',AK+A([0,-0.2,-0.25]),mix((MEDv,0.55),((0,0,-1),0.85))); put('KI5',AK+A([0,-0.33,-0.1]),mix((MEDv,0.85),((0,0,-1),0.45)))
put('KI6',AK+A([0,-0.33,0.05]),mix((MEDv,1),((0,-1,0),0.1)))
leg('KI7',AK[1]+2*cShM,('me',0.6),('bk',0.8)); leg('KI8',AK[1]+2*cShM,('me',0.9),('bk',0.35)); leg('KI9',AK[1]+5*cShM,('me',0.55),('bk',0.85))
leg('KI10',POP,('bk',0.75),('me',0.66))
front('KI11',-0.5*cunB,PUB_Y)
for i,k in enumerate(['KI12','KI13','KI14','KI15']): front(k,-0.5*cunB,NAV_Y-(4-i)*cAbL)
front('KI16',-0.5*cunB-0.05,NAV_Y)
for i,k in enumerate(['KI17','KI18','KI19','KI20','KI21']): front(k,-0.5*cunB,NAV_Y+(i+2)*cAbU)
for k,i in [('KI22',5),('KI23',4),('KI24',3),('KI25',2),('KI26',1)]: front(k,-2*cunB,ICS[i],(-0.1,0,1))
front('KI27',-2*cunB,5.27,(-0.1,0.25,1))
# ---------- LR ----------
tnail('LR1',1,2,-1); put_out('LR2',[-2.02,-7.95,1.36],[0,1,0],back=0.6); put('LR3',A([-2.02,-7.82,0.95]),[0,1,0.1])
put('LR4',AK+A([0.05,-0.1,0.2]),mix(((0,0,1),0.7),(MEDv,0.7)))
leg('LR5',MALM+5*cShM,('me',0.8),('fr',0.6)); leg('LR6',MALM+7*cShM,('me',0.8),('fr',0.6)); leg('LR7',SP9Y-0.05,('me',0.7),('bk',0.7))
leg('LR8',POP+0.05,('me',0.95),('bk',0.3)); leg('LR9',POP+0.25+4*cTh,('me',1),('bk',0.1))
def legout(k,y,*w,r=0.55):
    o,fr,la,me,bk=lf(y); D={'fr':fr,'la':la,'me':me,'bk':bk}; d=mix(*[(D[a],x) for a,x in w]); h=b.ray(o+d*(r+0.3),-d); P[k]=(h[0],h[1]); CHECK[k]=float(np.dot(h[1],d))
put_out('LR10',[-0.62,0.8-3*0.24,0.55],[0.35,0,1],back=2.0); put_out('LR11',[-0.6,0.8-2*0.24,0.6],[0.35,0,1],back=2.0)
for k in ('LR10','LR11'): CHECK[k]=float(np.dot(P[k][1],n([0.35,0,1])))
front('LR12',-2.5*cunB,0.72,(-0.15,0.1,1)); put('LR13',A([-0.6,2.8,0.4]),[-0.85,0,0.5]); front('LR14',-4*cunB,ICS[6],(-0.2,0,1))
# ---------- GB ----------
put_out('GB2',[-0.62,6.97,0.66],[-1,0,0.15],back=1.0); put_out('GB3',[-0.72,7.25,0.86],[-1,0,0.25],back=1.0)
put_out('GB7',[-0.72,7.66,0.6],[-1,0.15,0.2],back=1.0)
st8,gb7=P['ST8'][0],P['GB7'][0]
for k,t in [('GB4',0.25),('GB5',0.5),('GB6',0.75)]: headto(k,lerp(st8,gb7,t)+A([-0.05,0,0]))
headto('GB8',A([-0.6,8.05,0.32])); headto('GB9',A([-0.6,7.98,0.16])); headto('GB10',A([-0.66,7.6,-0.02])); headto('GB11',A([-0.64,7.25,-0.06]))
put_out('GB12',[-0.58,6.9,-0.04],[-0.8,-0.1,-0.6],back=1.0)
head('GB13',0.5,3); put_out('GB14',[-0.31,7.62,1.42],[-0.15,0.15,1],back=1.0)
head('GB15',0.5,2.25); head('GB16',1.5,2.25); head('GB17',2.5,2.25); head('GB18',4,2.25); head('GB19',9.5,2.25)
put('GB20',A([0,7.12,0.2]),[-0.5,0,-0.85])
put('GB22',A([-1.0,4.35,0.2]),[-1,0,0.05]); put('GB23',A([-1.0,4.25,0.35]),[-0.85,0,0.5])
front('GB24',-4*cunB,ICS[7],(-0.2,0,1)); put('GB25',A([-0.6,2.65,0.1]),[-0.75,0,-0.65]); put('GB26',A([-0.6,NAV_Y,0.25]),[-1,0,0.1])
put('GB27',A([-0.8,NAV_Y-3*cAbL,0.4]),[-0.6,0,0.8]); put('GB28',A([-0.8,NAV_Y-3.5*cAbL,0.5]),[-0.5,0,0.85])
put('GB29',A([-1.1,1.0,0.25]),[-1,0,0.15]); put('GB30',A([-1.1,0.48,0.0]),[-0.45,0,-1])
for k,y in [('GB31',POP+7*cTh),('GB32',POP+5*cTh)]: leg(k,y,('la',1),('bk',0.05))
GB34Y=POP-0.35; leg('GB33',GB34Y+3*cShL+0.1,('la',0.95),('bk',0.15)); leg('GB34',GB34Y,('la',0.85),('fr',0.5))
leg('GB35',MALL+7*cShL,('la',0.85),('bk',0.5)); leg('GB36',MALL+7*cShL,('la',0.85),('fr',0.5))
leg('GB37',MALL+5*cShL,('la',0.8),('fr',0.6)); leg('GB38',MALL+4*cShL,('la',0.85),('fr',0.5)); leg('GB39',MALL+3*cShL,('la',0.85),('fr',0.5))
put('GB40',AK+A([0,-0.15,0.2]),mix((-MEDv,0.8),((0,0,1),0.55)))
put('GB41',A([-2.48,-7.85,0.75]),mix((UPv,1),(-MEDv,0.35))); put('GB42',A([-2.45,-7.92,1.02]),mix((UPv,1),(-MEDv,0.25)))
put_out('GB43',[-2.52,-7.98,1.32],[0,1,0],back=0.6); tnail('GB44',4,3,-1)
# ---------- BL ----------
put_out('BL2',[-0.14,7.45,1.42],[-0.15,0.1,1],back=1.0)
head('BL3',0.5,0.7); head('BL4',0.5,1.5); head('BL5',1,1.5); head('BL6',2.5,1.5); head('BL7',4,1.5); head('BL8',5.5,1.5); head('BL9',9.5,1.3)
put('BL10',A([-0.22,6.95,0.1]),[0,0,-1])
inner=['BL11','BL12','BL13','BL14','BL15','BL16','BL17','BL18','BL19','BL20','BL21','BL22','BL23','BL24','BL25','BL26']
lev=['T1','T2','T3','T4','T5','T6','T7','T9','T10','T11','T12','L1','L2','L3','L4','L5']
for k,v in zip(inner,lev): backp(k,-1.5*cunB,VERT[v]-0.05)
for k,v in zip(['BL27','BL28','BL29','BL30'],['S1','S2','S3','S4']): backp(k,-1.5*cunB,VERT[v],(0,-0.3,-1))
for k,v,x in zip(['BL31','BL32','BL33','BL34'],['S1','S2','S3','S4'],[-0.2,-0.17,-0.15,-0.13]): backp(k,x,VERT[v],(0,-0.3,-1))
backp('BL35',-0.5*cunB,VERT['CO'],(0,-0.3,-1))
outer=['BL41','BL42','BL43','BL44','BL45','BL46','BL47','BL48','BL49','BL50','BL51','BL52']
lev2=['T2','T3','T4','T5','T6','T7','T9','T10','T11','T12','L1','L2']
for k,v in zip(outer,lev2): backp(k,-3*cunB,VERT[v]-0.05)
backp('BL53',-3*cunB,VERT['S2'],(0,-0.3,-1)); backp('BL54',-3*cunB,VERT['S4'],(0,-0.3,-1))
GLU=-0.05; leg('BL36',GLU,('bk',1)); leg('BL37',GLU-6*cTh,('bk',1))
leg('BL39',POP,('bk',0.7),('la',0.7)); leg('BL38',POP+1*cTh,('bk',0.75),('la',0.65)); leg('BL40',POP,('bk',1))
for k,c in [('BL55',2),('BL56',5),('BL57',8)]: leg(k,POP-c*cShL,('bk',1))
leg('BL58',MALL+7*cShL,('bk',0.7),('la',0.7)); leg('BL59',MALL+3*cShL,('bk',0.75),('la',0.65))
put('BL60',AK+A([0,0,-0.1]),mix((-MEDv,0.7),((0,0,-1),0.7))); put('BL61',AK+A([0,-0.38,-0.2]),mix((-MEDv,0.75),((0,0,-1),0.55)))
put('BL62',AK+A([0,-0.33,0.02]),-MEDv); put('BL63',AK+A([0,-0.45,0.3]),mix((-MEDv,1),((0,-1,0),0.15)))
put('BL64',A([-2.4,-7.95,0.6]),mix((-MEDv,1),(-UPv,0.3))); put('BL65',A([-2.5,-7.98,1.02]),mix((-MEDv,1),(-UPv,0.2)))
s=toe(5,1); put('BL66',lerp(*s,0.3),mix((-MEDv,1),(-UPv,0.1))); tnail('BL67',5,3,-1)
# ---------- CV ----------
put('CV1',A([0,0.05,0.2]),[0,-1,0.1])
front('CV2',0,PUB_Y); 
for i,k in enumerate(['CV3','CV4','CV5']): front(k,0,NAV_Y-(4-i)*cAbL)
front('CV6',0,NAV_Y-1.5*cAbL); front('CV7',0,NAV_Y-cAbL); put_out('CV8',[0,NAV_Y,1.6],[0,0,1],back=1)
for i,k in enumerate(['CV9','CV10','CV11','CV12','CV13','CV14','CV15']): front(k,0,NAV_Y+(i+1)*cAbU)
front('CV16',0,XIP_Y+0.08); front('CV17',0,ICS[4]+0.35); front('CV18',0,ICS[3]); front('CV19',0,ICS[2]); front('CV20',0,ICS[1]); front('CV21',0,5.2,(0,0.2,1))
put('CV22',A([0,5.45,0.4]),[0,0.35,1]); put('CV23',A([0,6.12,0.6]),[0,-0.4,1]); put_out('CV24',[0,6.42,1.45],[0,0,1],back=1.2)
# ---------- GV ----------
put('GV1',A([0,0.25,-0.3]),[0,-0.6,-0.8])
backp('GV2',0,VERT['CO']+0.15,(0,-0.3,-1))
for k,v in [('GV3','L4'),('GV4','L2'),('GV5','L1'),('GV6','T11'),('GV7','T10'),('GV8','T9'),('GV9','T7'),('GV10','T6'),('GV11','T5'),('GV12','T3'),('GV13','T1')]: backp(k,0,VERT[v]-0.05)
for k,c in [('GV15',11.5),('GV16',11),('GV17',9.5),('GV18',8),('GV19',6.5),('GV20',5),('GV21',3.5),('GV22',2),('GV23',1),('GV24',0.5)]: head(k,c,0)
put_out('GV25',[0,6.92,1.8],[0,0,1],back=1); put_out('GV27',[0,6.69,1.7],[0,0,1],back=1)
put('GV28',A([0,6.7,1.15]),[0,0.35,1])
# internal landmarks for the leg channels and the vessels
IN.update({'spleen':A([0.55,3.4,0.3]),'liver':A([-0.45,3.35,0.5]),'kidney':A([-0.35,2.6,-0.05]),'bladder':A([0,1.0,0.6]),'tongue':A([0,6.55,0.95]),
  'brain':A([0,7.75,0.4]),'uterus':A([0,1.25,0.45]),'lips':A([0,6.6,1.25]),'vertex':P['GV20'][0]-A([0,0.25,0])})

bad={k:round(v,2) for k,v in CHECK.items() if v<0.25 and k!='GV28'}
print('points whose surface faces away from the intended direction:',bad)
