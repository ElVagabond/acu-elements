# ---------- courses: leg channels, CV, GV ----------
def hw(target):                      # scalp/face waypoint, cast from outside the head
    d=n(A(target)-HC); h=b.ray(HC+d*2.5,-d); return (h[0],h[1])
def lw(y,*w):                        # leg waypoint on the skin
    o,fr,la,me,bk=lf(y); D={'fr':fr,'la':la,'me':me,'bk':bk}; d=mix(*[(D[a],x) for a,x in w]); h=b.ray(o,d)
    if h is None or np.linalg.norm(h[0]-o)>1.3: h=b.ray(o+d*0.6,-d)
    return (h[0],h[1])
def mirror(p): return (p[0]*A([-1,1,1]),p[1]*A([-1,1,1]))
S_=lambda *ks:[P[k] for k in ks]
CH['ST']=[('connect',trace([mirror(P['LI20']),wp_out([-0.16,7.12,1.5],[-0.3,0,1],back=1.2),g('BL1'),g('ST1')],step=0.03,lift=0.2)),
  ('surface',trace(S_('ST1','ST2','ST3','ST4')+[wp_out([-0.45,6.45,1.15],[-0.6,-0.4,0.7],back=1.2)]+S_('ST5','ST6','ST7')+[hw([-0.75,7.45,0.95])]+S_('ST8'),lift=0.2)),
  ('surface',trace(S_('ST5','ST9','ST10','ST11','ST12','ST13','ST14','ST15','ST16','ST17','ST18','ST19','ST20','ST21','ST22','ST23','ST24','ST25','ST26','ST27','ST28','ST29','ST30','ST31')+
     [lw(-0.6,('fr',0.85),('la',0.5))]+S_('ST32','ST33','ST34','ST35','ST36','ST37','ST38','ST40','ST39')+[lw(-6.6,('fr',0.9),('la',0.4))]+S_('ST41','ST42','ST43','ST44','ST45'),lift=0.25)),
  ('connect',trace(S_('ST42')+[wp_ray(A([-1.98,-7.85,1.05]),[0.3,1,0])]+S_('SP1'),lift=0.2)),
  ('internal',straight([P['ST12'][0],IN['lung'],IN['stomach'],IN['spleen']]))]
CH['SP']=[('surface',trace(S_('SP1','SP2','SP3','SP4','SP5')+[lw(-7.0,('me',1),('bk',0.2))]+S_('SP6','SP7','SP8','SP9')+[lw(-3.2,('me',0.9),('fr',0.3))]+S_('SP10','SP11')+
     [lw(-0.2,('me',0.6),('fr',0.8))]+S_('SP12','SP13','SP14','SP15','SP16','SP17','SP18','SP19','SP20','SP21'),lift=0.25)),
  ('internal',straight([P['SP16'][0],IN['spleen'],IN['stomach'],IN['chest'],IN['throat'],IN['tongue']]))]
CH['KI']=[('connect',trace(S_('BL67')+[wp_ray(A([-2.45,-7.95,1.0]),[0,-1,0]),wp_ray(A([-2.35,-7.95,0.9]),[0,-1,0])]+S_('KI1'),lift=0.15)),
  ('surface',trace(S_('KI1')+[wp_ray(A([-2.05,-7.95,0.65]),[0.5,-1,0])]+S_('KI2','KI3','KI4','KI5','KI6')+[wp_ray(AK+A([0,-0.1,-0.12]),[1,0,-0.4])]+S_('KI7','KI8','KI9')+
     [lw(-4.6,('me',0.6),('bk',0.8))]+S_('KI10'),lift=0.2)),
  ('internal',straight([P['KI10'][0],A([-0.5,-1.0,-0.2]),A([0,0.35,-0.45]),IN['kidney'],IN['bladder'],P['KI11'][0]])),
  ('surface',trace(S_('KI11','KI12','KI13','KI14','KI15','KI16','KI17','KI18','KI19','KI20','KI21','KI22','KI23','KI24','KI25','KI26','KI27'),lift=0.25)),
  ('internal',straight([IN['kidney'],IN['liver'],IN['lung'],IN['throat'],IN['tongue']]))]
CH['LR']=[('surface',trace(S_('LR1')+[wp_ray(A([-1.98,-7.95,1.6]),[0,1,0])]+S_('LR2','LR3','LR4')+[lw(-6.9,('me',0.8),('fr',0.6))]+S_('LR5','LR6')+[lw(-4.5,('me',0.85),('bk',0.4))]+
     S_('LR7','LR8')+[lw(-1.6,('me',1),('fr',0.1))]+S_('LR9','LR10','LR11','LR12'),lift=0.25)),
  ('internal',straight([P['LR12'][0],IN['uterus'],IN['bladder'],IN['stomach'],P['LR13'][0]])),
  ('surface',trace(S_('LR13','LR14'),lift=0.25)),
  ('internal',straight([P['LR14'][0],IN['liver'],IN['lung'],IN['throat'],IN['eye'],IN['vertex']]))]
CH['GB']=[('surface',trace(S_('GB1','GB2','GB3','GB4','GB5','GB6','GB7','GB8','GB9','GB10','GB11','GB12')+[hw([-0.75,7.75,0.25]),hw([-0.7,7.95,0.7]),hw([-0.55,7.95,1.1])]+
     S_('GB13','GB14','GB15','GB16','GB17','GB18','GB19','GB20')+[wp_ray(A([-0.25,6.6,0.0]),[-0.6,0,-0.8])],lift=0.2)),
  ('surface',trace([wp_ray(A([-0.25,6.6,0.0]),[-0.6,0,-0.8]),wp_ray(A([-0.4,6.1,0.05]),[-0.7,0.3,-0.6])]+S_('GB21'),lift=0.25)),
  ('connect',trace(S_('GB21')+[wp_ray(A([-0.6,5.6,0.2]),[-0.2,1,0.4])]+S_('ST12'))),
  ('internal',straight([P['ST12'][0],IN['chest'],IN['liver'],A([-0.7,0.9,0.4])])),
  ('connect',trace(S_('ST12')+[wp_ray(A([-1.0,5.0,0.4]),[-0.5,0,1]),wp_ray(A([-1.0,4.6,0.25]),[-1,0,0.3])]+S_('GB22'),lift=0.25)),
  ('surface',trace(S_('GB22','GB23','GB24','GB25','GB26','GB27','GB28','GB29','GB30')+[lw(-0.6,('la',1),('bk',0.2))]+S_('GB31','GB32','GB33','GB34','GB35','GB36','GB37','GB38','GB39','GB40','GB41','GB42','GB43','GB44'),lift=0.25)),
  ('connect',trace(S_('GB41')+[wp_ray(A([-2.2,-7.85,1.1]),[0,1,0])]+S_('LR1'),lift=0.2))]
CH['BL']=[('surface',trace(S_('BL1','BL2','BL3','BL4','BL5','BL6','BL7','BL8','BL9','BL10'),lift=0.2)),
  ('connect',trace(S_('BL7','GV20'),lift=0.2)),('internal',straight([P['BL7'][0],IN['brain']])),
  ('surface',trace(S_('BL10','BL11','BL12','BL13','BL14','BL15','BL16','BL17','BL18','BL19','BL20','BL21','BL22','BL23','BL24','BL25','BL26','BL27','BL28','BL29','BL30',
     'BL31','BL32','BL33','BL34','BL35','BL36','BL37','BL38','BL39','BL40'),lift=0.25)),
  ('surface',trace(S_('BL10')+[backp_w for backp_w in [wp_ray(A([-0.45,5.75,0.0]),[0,0.3,-1])]]+S_('BL41','BL42','BL43','BL44','BL45','BL46','BL47','BL48','BL49','BL50','BL51','BL52','BL53','BL54')+
     [lw(-0.3,('bk',0.8),('la',0.6)),lw(-2.2,('bk',0.85),('la',0.5))]+S_('BL40'),lift=0.25)),
  ('surface',trace(S_('BL40','BL55','BL56','BL57','BL58','BL59','BL60','BL61','BL62','BL63','BL64','BL65','BL66','BL67'),lift=0.25)),
  ('internal',straight([P['BL23'][0],IN['kidney'],IN['bladder']]))]
CH['CV']=[('internal',straight([IN['uterus'],A([0,0.4,0.3]),P['CV1'][0]])),
  ('surface',trace(S_('CV1')+[wp_out([0,0.3,1.25],[0,-0.6,0.8],back=1.0)]+S_('CV2','CV3','CV4','CV5','CV6','CV7','CV8','CV9','CV10','CV11','CV12','CV13','CV14','CV15','CV16','CV17','CV18','CV19','CV20','CV21','CV22','CV23')+
     [wp_out([0,6.22,1.3],[0,-0.7,0.7],back=1.0)]+S_('CV24'),lift=0.2)),
  ('internal',straight([P['CV24'][0],IN['lips'],IN['eye']]))]
CH['GV']=[('internal',straight([IN['uterus'],A([0,0.4,0.3]),P['CV1'][0]])),('connect',trace(S_('CV1','GV1'),lift=0.15)),
  ('surface',trace(S_('GV1','GV2','GV3','GV4','GV5','GV6','GV7','GV8','GV9','GV10','GV11','GV12','GV13','GV14','GV15','GV16','GV17','GV18','GV19','GV20','GV21','GV22','GV23','GV24')+
     [hw([0,7.6,1.6]),wp_out([0,7.25,1.65],[0,0.1,1],back=1.0)]+S_('GV25','GV26','GV27'),lift=0.2)),
  ('connect',trace(S_('GV27','GV28'),lift=0.05)),('internal',straight([P['GV20'][0],IN['brain']]))]
