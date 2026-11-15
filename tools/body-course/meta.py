"""Names, categories and locations for the channel course page. Shu-point text comes from the Shu Atlas data file when present."""
import json,os
HAN={'LU1':'中府','LU2':'雲門','LU3':'天府','LU4':'俠白','LU5':'尺澤','LU6':'孔最','LU7':'列缺','LU8':'經渠','LU9':'太淵','LU10':'魚際','LU11':'少商',
 'HT1':'極泉','HT2':'青靈','HT3':'少海','HT4':'靈道','HT5':'通里','HT6':'陰郄','HT7':'神門','HT8':'少府','HT9':'少衝',
 'PC1':'天池','PC2':'天泉','PC3':'曲澤','PC4':'郄門','PC5':'間使','PC6':'內關','PC7':'大陵','PC8':'勞宮','PC9':'中衝',
 'SI1':'少澤','SI2':'前谷','SI3':'後溪','SI4':'腕骨','SI5':'陽谷','SI6':'養老','SI7':'支正','SI8':'小海','SI9':'肩貞','SI10':'臑俞','SI11':'天宗','SI12':'秉風',
 'SI13':'曲垣','SI14':'肩外俞','SI15':'肩中俞','SI16':'天窗','SI17':'天容','SI18':'顴髎','SI19':'聽宮',
 'TB1':'關衝','TB2':'液門','TB3':'中渚','TB4':'陽池','TB5':'外關','TB6':'支溝','TB7':'會宗','TB8':'三陽絡','TB9':'四瀆','TB10':'天井','TB11':'清冷淵','TB12':'消濼',
 'TB13':'臑會','TB14':'肩髎','TB15':'天髎','TB16':'天牖','TB17':'翳風','TB18':'瘈脈','TB19':'顱息','TB20':'角孫','TB21':'耳門','TB22':'耳和髎','TB23':'絲竹空'}
# id: (pinyin, English, role or None, location) for the points that are not five-shu points
OTHER={
 'LU1':('Zhongfu','Central Treasury','Front-Mu of the lung','On the front of the chest, 6 cun from the midline in the first intercostal space, 1 cun below LU2.'),
 'LU2':('Yunmen','Cloud Gate',None,'In the hollow below the outer end of the clavicle, 6 cun from the midline.'),
 'LU3':('Tianfu','Heavenly Storehouse',None,'On the outer edge of the biceps, 3 cun below the front armpit fold.'),
 'LU4':('Xiabai','Guarding White',None,'On the outer edge of the biceps, 4 cun below the front armpit fold.'),
 'LU6':('Kongzui','Maximum Opening','Xi-cleft','On the line from LU5 to LU9, 7 cun above the wrist crease.'),
 'LU7':('Lieque','Broken Sequence','Luo-connecting','Above the styloid process of the radius, 1.5 cun above the wrist crease.'),
 'HT1':('Jiquan','Summit Spring',None,'At the centre of the armpit, beside the axillary artery.'),
 'HT2':('Qingling','Blue-Green Spirit',None,'3 cun above the inner end of the elbow crease, in the groove on the inner side of the biceps.'),
 'HT5':('Tongli','Penetrating the Interior','Luo-connecting','1 cun above the wrist crease, on the radial side of the flexor carpi ulnaris tendon.'),
 'HT6':('Yinxi','Yin Cleft','Xi-cleft','0.5 cun above the wrist crease, on the radial side of the flexor carpi ulnaris tendon.'),
 'PC1':('Tianchi','Heavenly Pool',None,'In the fourth intercostal space, 1 cun outside the nipple.'),
 'PC2':('Tianquan','Heavenly Spring',None,'2 cun below the front armpit fold, between the two heads of the biceps.'),
 'PC4':('Ximen','Cleft Gate','Xi-cleft','5 cun above the wrist crease, between the tendons of palmaris longus and flexor carpi radialis.'),
 'PC6':('Neiguan','Inner Pass','Luo-connecting','2 cun above the wrist crease, between the tendons of palmaris longus and flexor carpi radialis.'),
 'SI4':('Wangu','Wrist Bone','Yuan-source','On the outer edge of the hand, in the hollow between the base of the fifth metacarpal and the hamate.'),
 'SI6':('Yanglao','Support the Aged','Xi-cleft','On the back of the wrist, in the hollow on the radial side of the head of the ulna.'),
 'SI7':('Zhizheng','Branch to the Correct','Luo-connecting','On the line from SI5 to SI8, 5 cun above the wrist crease.'),
 'SI9':('Jianzhen','True Shoulder',None,'Behind the shoulder joint, 1 cun above the back armpit fold.'),
 'SI10':('Naoshu','Upper Arm Shu',None,'Directly above SI9, in the hollow below the spine of the scapula.'),
 'SI11':('Tianzong','Heavenly Gathering',None,'In the middle of the infraspinous fossa, a third of the way from the spine of the scapula to its lower angle.'),
 'SI12':('Bingfeng','Grasping the Wind',None,'In the middle of the suprascapular fossa, directly above SI11.'),
 'SI13':('Quyuan','Crooked Wall',None,'At the inner end of the suprascapular fossa.'),
 'SI14':('Jianwaishu','Outer Shoulder Shu',None,'3 cun from the midline, level with the lower border of the first thoracic vertebra.'),
 'SI15':('Jianzhongshu','Middle Shoulder Shu',None,'2 cun from the midline, level with the lower border of the seventh neck vertebra.'),
 'SI16':('Tianchuang','Heavenly Window',None,'On the side of the neck, at the back edge of sternocleidomastoid, level with the Adam\'s apple.'),
 'SI17':('Tianrong','Heavenly Appearance',None,'Behind the angle of the jaw, at the front edge of sternocleidomastoid.'),
 'SI18':('Quanliao','Cheek Bone-Hole',None,'Directly below the outer corner of the eye, in the hollow under the cheekbone.'),
 'SI19':('Tinggong','Palace of Hearing','End point','In front of the tragus, in the hollow that forms when the mouth is open.'),
 'TB4':('Yangchi','Yang Pool','Yuan-source','On the back of the wrist crease, in the hollow on the ulnar side of the extensor digitorum tendon.'),
 'TB5':('Waiguan','Outer Pass','Luo-connecting','2 cun above the back of the wrist crease, between the radius and the ulna.'),
 'TB7':('Huizong','Convergence and Gathering','Xi-cleft','3 cun above the back of the wrist crease, on the radial edge of the ulna, beside TB6.'),
 'TB8':('Sanyangluo','Three Yang Connection',None,'4 cun above the back of the wrist crease, between the radius and the ulna.'),
 'TB9':('Sidu','Four Rivers',None,'5 cun below the point of the elbow, between the radius and the ulna.'),
 'TB11':('Qinglengyuan','Clear Cold Abyss',None,'2 cun above the point of the elbow, on the line to TB14.'),
 'TB12':('Xiaoluo','Dispersing Riverbed',None,'On the back of the upper arm, midway between TB11 and TB13.'),
 'TB13':('Naohui','Upper Arm Convergence',None,'On the back edge of the deltoid, 3 cun below TB14.'),
 'TB14':('Jianliao','Shoulder Bone-Hole',None,'Behind and below the acromion, in the hollow that appears when the arm is raised.'),
 'TB15':('Tianliao','Heavenly Bone-Hole',None,'Above the upper angle of the scapula, midway between GB21 and SI13.'),
 'TB16':('Tianyou','Window of Heaven',None,'On the side of the neck, behind sternocleidomastoid, level with the angle of the jaw.'),
 'TB17':('Yifeng','Wind Screen',None,'Behind the earlobe, in the hollow between the mastoid process and the jaw.'),
 'TB18':('Chimai','Spasm Vessel',None,'Behind the ear, a third of the way along the curve from TB17 to TB20.'),
 'TB19':('Luxi','Skull\'s Rest',None,'Behind the ear, two thirds of the way along the curve from TB17 to TB20.'),
 'TB20':('Jiaosun','Minute Angle',None,'Directly above the top of the ear, at the hairline.'),
 'TB21':('Ermen','Ear Gate',None,'In front of the notch above the tragus, in the hollow that forms when the mouth is open.'),
 'TB22':('Erheliao','Ear Harmony Bone-Hole',None,'In front of the root of the ear, level with its upper attachment, behind the temporal artery.'),
 'TB23':('Sizhukong','Silk Bamboo Hollow','End point','In the hollow at the outer end of the eyebrow.'),
}
SHU_ROLE={'LU9':'Yuan-source','HT7':'Yuan-source','PC7':'Yuan-source'}
REFS={
 'GV14':('Dazhui','大椎','Great Vertebra','Governor Vessel','Below the spinous process of the seventh neck vertebra, where the yang channels of the arm meet.'),
 'ST12':('Quepen','缺盆','Empty Basin','Stomach channel','In the hollow above the middle of the clavicle. Branches go inward from here to the chest.'),
 'ST4':('Dicang','地倉','Earth Granary','Stomach channel','Beside the corner of the mouth. The Large Intestine channel passes here on its way around the upper lip.'),
 'GV26':('Shuigou','水溝','Water Trough','Governor Vessel','In the groove of the upper lip, a third of the way down from the nose. The left and right Large Intestine channels cross here.'),
 'CV12':('Zhongwan','中脘','Central Venter','Conception Vessel','On the midline, 4 cun above the navel. The Lung channel begins internally here, in the middle burner.'),
 'GB21':('Jianjing','肩井','Shoulder Well','Gallbladder channel','On the top of the shoulder, midway between GV14 and the acromion. The Triple Burner channel crosses the shoulder here.'),
 'GB1':('Tongziliao','瞳子髎','Pupil Bone-Hole','Gallbladder channel','Beside the outer corner of the eye. The Small Intestine channel reaches here before turning back into the ear.'),
 'BL1':('Jingming','睛明','Bright Eyes','Bladder channel','Just inside the inner corner of the eye. A short branch of the Small Intestine channel ends here.'),
}
KIND={'Jing-Well':'well','Ying-Spring':'spring','Shu-Stream':'stream','Jing-River':'river','He-Sea':'sea'}
def build(li_points,atlas_json):
    out={p['id']:p for p in li_points}            # LI text as written for the LI page
    atlas={p['code']:p for p in json.load(open(atlas_json))['points']} if atlas_json and os.path.exists(atlas_json) else {}
    import legs_meta
    OTHER.update({k:(v[0],v[2],v[3],v[4]) for k,v in legs_meta.LEG.items()}); HAN.update({k:v[1] for k,v in legs_meta.LEG.items()}); HAN.update(legs_meta.SHU_HAN)
    SHU_ROLE.update({k:v for k,v in legs_meta.SHU_ROLE_LEG.items() if v})
    for ch,count in [('LU',11),('HT',9),('PC',9),('SI',19),('TB',23),('ST',45),('SP',21),('KI',27),('LR',14),('GB',44),('BL',67),('CV',24),('GV',28)]:
        for i in range(1,count+1):
            k=f'{ch}{i}'; d={'id':k,'ch':ch,'han':HAN[k]}
            if k in OTHER:
                py,en,role,loc=OTHER[k]; d.update(py=py,en=en,loc=loc)
                if role: d['role']=role
            else:
                a=atlas[k]; d.update(py=a['py'],en=a['en'],loc=a['loc'],shu=KIND[a['shu']],el=a['elem'].lower())
                if k in SHU_ROLE: d['role']=SHU_ROLE[k]
            out[k]=d
    for k,(py,hz,en,role,loc) in REFS.items():
        if k not in out: out[k]={'id':k,'ch':k[:2],'py':py,'han':hz,'en':en,'role':role,'loc':loc}
    return out
