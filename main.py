import os
from PIL import Image, ImageDraw, ImageFont
W,H=1024,1024; BG=(250,246,235); INK=(20,20,20); RED=(178,34,34); NAVY=(25,45,90); GOLD=(176,132,32); TEAL=(18,110,105); GREY=(110,110,105); LINE=(200,190,170); LAND=(216,205,178); SEA=(198,218,228)
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
SB=lambda s: F('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',s); SN=lambda s: F('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',s); SBN=lambda s: F('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',s)
def wrap(t,f,mx):
    ws=[]
    for w in t.split(' '):
        if not ws or f.getlength(ws[-1]+' '+w)>mx: ws.append(w)
        else: ws[-1]+=' '+w
    return ws
def txt(d,x,y,t,f,c=INK,align='l',mx=None,leading=None):
    if mx:
        ls=wrap(t,f,mx); lh=leading or int(f.size*1.18)
        for i,l in enumerate(ls): d.text((x,y+i*lh),l,font=f,fill=c)
        return y+len(ls)*lh
    if align=='c': x-=f.getlength(t)/2
    if align=='r': x-=f.getlength(t)
    d.text((x,y),t,font=f,fill=c); return y+f.size
def chip(d,x,y,s):
    cols={'CONFIRMED':(34,139,34),'OFFICIAL':(30,90,180),'REPORTED':(90,90,90),'CLAIM':(220,110,0),'ONGOING':(190,150,0)}
    c=cols.get(s,(90,90,90)); f=SBN(8); w=f.getlength(s)+8; d.rounded_rectangle([x,y,x+w,y+13],2,fill=c); d.text((x+4,y+2),s,font=f,fill=(255,255,255)); return x+w+4
def scene(d,x,y,w,h,k):
    skies={'tower':(30,30,60),'gate':(140,40,40),'court':(35,55,95),'drone':(20,25,50),'trophy':(25,90,60),'ship':(25,70,110),'chart':(25,45,90),'server':(120,20,20),'heli':(90,110,140),'market':(150,90,40),'desert':(190,150,80),'strike':(140,60,30),'rocket':(15,20,45)}; d.rectangle([x,y,x+w,y+h],fill=skies.get(k,(60,60,60)))
    if k=='tower':
        d.rectangle([x+w*0.42,y+h*0.15,x+w*0.58,y+h*0.95],fill=(200,190,170)); d.polygon([(x+w*0.42,y+h*0.15),(x+w*0.5,y+h*0.02),(x+w*0.58,y+h*0.15)],fill=(230,220,200)); d.ellipse([x+w*0.62,y+h*0.08,x+w*0.82,y+h*0.28],fill=(255,180,60)); d.ellipse([x+w*0.66,y+h*0.12,x+w*0.86,y+h*0.32],fill=(255,120,40)); d.rectangle([x+w*0.1,y+h*0.7,x+w*0.3,y+h*0.95],fill=(120,115,110)); d.rectangle([x+w*0.72,y+h*0.6,x+w*0.92,y+h*0.95],fill=(100,95,90))
    elif k=='gate':
        d.rectangle([x,y+h*0.55,x+w,y+h*0.95],fill=(90,30,30)); d.rectangle([x+w*0.35,y+h*0.3,x+w*0.65,y+h*0.95],fill=(160,50,50)); d.polygon([(x+w*0.3,y+h*0.32),(x+w*0.5,y+h*0.12),(x+w*0.7,y+h*0.32)],fill=(200,170,60)); d.rectangle([x+w*0.05,y+h*0.5,x+w*0.2,y+h*0.95],fill=(120,40,40)); d.rectangle([x+w*0.8,y+h*0.5,x+w*0.95,y+h*0.95],fill=(120,40,40))
    elif k=='court':
        d.rectangle([x,y+h*0.7,x+w,y+h*0.95],fill=(180,170,150)); d.polygon([(x+w*0.1,y+h*0.25),(x+w*0.5,y+h*0.05),(x+w*0.9,y+h*0.25)],fill=(220,210,190))
        for i in range(5): d.rectangle([x+w*(0.12+i*0.17),y+h*0.28,x+w*(0.2+i*0.17),y+h*0.7],fill=(240,235,220))
        d.ellipse([x+w*0.72,y+h*0.08,x+w*0.9,y+h*0.26],fill=(255,215,0))
    elif k in ('drone','heli'):
        d.ellipse([x+w*0.7,y+h*0.1,x+w*0.95,y+h*0.35],fill=(255,200,80)); d.rectangle([x+w*0.08,y+h*0.75,x+w*0.92,y+h*0.95],fill=(40,40,45)); d.rectangle([x+w*0.15,y+h*0.45,x+w*0.35,y+h*0.75],fill=(70,70,75)); d.rectangle([x+w*0.6,y+h*0.5,x+w*0.85,y+h*0.75],fill=(90,90,95)); d.polygon([(x+w*0.42,y+h*0.35),(x+w*0.5,y+h*0.2),(x+w*0.58,y+h*0.35)],fill=(200,200,200))
    elif k=='trophy':
        d.ellipse([x+w*0.38,y+h*0.15,x+w*0.62,y+h*0.45],fill=(255,215,0)); d.rectangle([x+w*0.46,y+h*0.45,x+w*0.54,y+h*0.7],fill=(220,180,0)); d.rectangle([x+w*0.35,y+h*0.7,x+w*0.65,y+h*0.8],fill=(200,170,0)); d.rectangle([x,y+h*0.85,x+w,y+h*0.95],fill=(20,120,70))
    elif k=='ship':
        d.polygon([(x+w*0.1,y+h*0.6),(x+w*0.9,y+h*0.6),(x+w*0.8,y+h*0.85),(x+w*0.2,y+h*0.85)],fill=(150,50,40)); d.rectangle([x+w*0.2,y+h*0.3,x+w*0.75,y+h*0.6],fill=(60,90,130)); d.rectangle([x+w*0.3,y+h*0.15,x+w*0.45,y+h*0.3],fill=(200,200,200)); d.ellipse([x+w*0.75,y+h*0.1,x+w*0.92,y+h*0.27],fill=(255,150,50))
    elif k=='chart':
        d.rectangle([x,y+h*0.75,x+w,y+h*0.95],fill=(240,235,220)); d.line([(x+w*0.05,y+h*0.6),(x+w*0.3,y+h*0.5),(x+w*0.5,y+h*0.55),(x+w*0.7,y+h*0.25),(x+w*0.95,y+h*0.12)],fill=(255,255,255),width=4); d.ellipse([x+w*0.68,y+h*0.2,x+w*0.74,y+h*0.3],fill=(255,215,0)); d.rectangle([x+w*0.05,y+h*0.05,x+w*0.3,y+h*0.2],fill=(25,45,90))
    elif k=='server':
        for i in range(3): d.rectangle([x+w*0.15,y+h*(0.12+i*0.28),x+w*0.85,y+h*(0.3+i*0.28)],fill=(40,40,48)); d.ellipse([x+w*0.7,y+h*0.15,x+w*0.78,y+h*0.25],fill=(255,60,60)); d.ellipse([x+w*0.7,y+h*0.43,x+w*0.78,y+h*0.53],fill=(255,200,0))
    elif k=='market':
        d.rectangle([x+w*0.1,y+h*0.5,x+w*0.9,y+h*0.9],fill=(120,70,30)); d.polygon([(x+w*0.05,y+h*0.5),(x+w*0.5,y+h*0.2),(x+w*0.95,y+h*0.5)],fill=(220,60,50)); d.ellipse([x+w*0.7,y+h*0.05,x+w*0.92,y+h*0.27],fill=(255,220,120))
    elif k in ('desert','strike'):
        d.ellipse([x+w*0.72,y+h*0.08,x+w*0.92,y+h*0.28],fill=(255,200,100)); d.polygon([(x,y+h*0.95),(x+w*0.3,y+h*0.55),(x+w*0.6,y+h*0.95)],fill=(200,170,110)); d.polygon([(x+w*0.5,y+h*0.95),(x+w*0.75,y+h*0.6),(x+w,y+h*0.95)],fill=(180,150,95)); d.rectangle([x+w*0.1,y+h*0.7,x+w*0.25,y+h*0.9],fill=(90,70,50))
    elif k=='rocket':
        d.polygon([(x+w*0.45,y+h*0.05),(x+w*0.55,y+h*0.05),(x+w*0.58,y+h*0.5),(x+w*0.42,y+h*0.5)],fill=(240,240,240)); d.polygon([(x+w*0.42,y+h*0.5),(x+w*0.32,y+h*0.7),(x+w*0.42,y+h*0.6)],fill=(220,60,50)); d.polygon([(x+w*0.58,y+h*0.5),(x+w*0.68,y+h*0.7),(x+w*0.58,y+h*0.6)],fill=(220,60,50)); d.ellipse([x+w*0.42,y+h*0.68,x+w*0.58,y+h*0.9],fill=(255,180,60)); d.ellipse([x+w*0.75,y+h*0.1,x+w*0.9,y+h*0.25],fill=(255,255,255))
    else:
        d.rectangle([x+w*0.1,y+h*0.6,x+w*0.9,y+h*0.95],fill=(120,120,115)); d.ellipse([x+w*0.7,y+h*0.08,x+w*0.9,y+h*0.28],fill=(255,200,80))
HEROES=[(1,'RIYADH · MIDDLE EAST','CONFIRMED',"Houthi drone hits Riyadh's tallest tower again, 11 hurt",'A Houthi drone struck the PIF tower, Riyadh\u2019s tallest, a second time in a week, injuring 11: 2 Saudis, 2 Indians, 3 Nepalis, 4 Egyptians.','tower','Saudi officials · 14:27 UTC'),(2,'SHANGHAI · ASIA','OFFICIAL','China probes Shanghai party chief Chen Jining','Chen Jining, 62, the Shanghai party chief, is probed for \u201cserious violations\u201d, the fourth Politburo member to fall this year.','gate','CCDI · OFFICIAL'),(3,'NEW YORK · US / TECH','CONFIRMED','Huawei guilty on 10 of 12 counts','A US jury found Huawei guilty on 10 of 12 counts, including trade-secret theft and bank fraud, clearing it of racketeering.','court','US court · 20:41 UTC')]
CARDS=[(4,'ZAPORIZHZHIA · EUROPE / WAR','REPORTED','Russian attacks kill 9 across Ukraine in a day','Russia fired 96 drones, 73 downed; attacks killed 9 and wounded 81.','drone','Kyiv officials · 11:37 UTC'),(5,'CAS · AFRICA / SPORT','OFFICIAL','CAS hands Senegal back the AFCON title','CAS gave Senegal the AFCON title; Morocco forfeited 3\u20130, final 1\u20130.','trophy','CAS · OFFICIAL'),(6,'HORMUZ · MIDDLE EAST','REPORTED','IRGC attacks container ship in Hormuz','IRGC hit a container ship in Hormuz at 18:58 UTC, disabling its navigation.','ship','UKMTO · wires'),(7,'NEW YORK · WORLD / MARKETS','CONFIRMED','Dow closes above 50,000 for the first time','Dow 50,018, first above 50,000; Nasdaq -1.5%, Taiex +8.99%.','chart','Market close'),(8,'REDMOND · WORLD / TECH','REPORTED',"Microsoft declares 'Code Red' after historic outage",'After a 24-hour outage, Microsoft declared \u201cCode Red\u201d.','server','Reuters'),(9,'ESKISEHIR · EUROPE','REPORTED','Turkish military helicopter crash kills 5','Turkish AS-532 crashed in Eskisehir, killing all 5 on board.','heli','Turkish officials · 19:52 UTC'),(10,'CARTAGENA · AMERICAS','REPORTED','Supermarket hostages: 25 held in Cartagena','25 hostages held in a Cartagena supermarket; 5 elderly women freed.','market','Colombian officials · 17:35 UTC'),(11,'ADEN · MIDDLE EAST','REPORTED','Houthis advance within 60 km of Aden','Houthi forces advanced to within 60 km of Aden, Yemen, near the port.','desert','Wires · 16:51 UTC'),(12,'LAHJ · MIDDLE EAST','REPORTED','Saudi strikes kill 25, wound 6 in Yemen','Saudi strikes in Wadi Maabaq, Lahj, killed or left missing 25 and wounded 6.','strike','Yemeni officials · 10:42 UTC'),(13,'JIUQUAN · WORLD / SPACE','OFFICIAL','China names first foreign astronaut for Tiangong',"Shenzhou-24 crew named: Pakistan's Ali, first foreigner for Tiangong.",'rocket','CMSA · OFFICIAL')]
ALSO=[(14,'Ankara','Haftar visits Turkey for the first time.'),(15,'London','UK sanctions Houthis + 4 officials.'),(16,'Villavicencio','Car bomb injures 23.'),(17,'Gaza','Israel kills Hamas internal security chief.'),(18,'Baghdad','Iraq orders federal control of Kurdish oilfields.'),(19,'Gaza','Meningitis epidemic alert: 272 cases in Oct.'),(20,'DR Congo','Missing Cessna 208; rebels claim shootdown.'),(21,'Hanoi','Hot-pot explosion kills at least 6.'),(22,'Gulf of Finland','Ukraine hits Russian ship Sparta II.'),(23,'Kuala Lumpur','Malaysia to return thousands of migrants.'),(24,'Ulleungdo','S. Korea shelter order as jets enter ADIZ.'),(25,'Dhaka','Hasina plans return on 16 Dec.'),(26,'The Hague','14 nations endorse ICJ Myanmar ruling.'),(27,'Jakarta','Indonesia nominates 2 VP candidates.'),(28,'Beijing','China sentences official Ma to death for spying.'),(29,'Brussels','NATO vows defence against space threat.'),(30,'Mexico City','El Chapo Isidro: US drone aided capture; Mexico to try him.'),(31,'San Salvador','Bukele names 3 soldiers killed in Haiti.'),(32,'Ottawa','Pentagon rebukes Canada: only 41.9% of air fleet ready.'),(33,'Washington','US adds Megaspeed to trade blacklist.'),(34,'Kyiv','Zelensky urges Ukraine/Russia/US/Europe talks soon.'),(35,'Ras Al Khaimah','UAE bus-truck crash kills 13.'),(36,'London','England record 5,258 heat deaths, summer 2026.'),(37,'Kourou','Ariane 6 lofts 36 Amazon satellites.'),(38,'Cikande','Factory-fire toll rises to 26.')]
UTC=[('02:15','NATO vows space defence'),('08:16','Hanoi hot-pot blast'),('10:42','Saudi strikes Yemen'),('14:27','Riyadh tower hit'),('16:51','Houthis 60 km from Aden'),('18:58','Hormuz ship attack'),('20:41','Huawei guilty')]
NUMS=[('11','hurt in Riyadh'),('9','killed in Ukraine'),('50,018','Dow close'),('+8.99%','Taiex record'),('25','killed/missing, Yemen'),('26','Cikande toll'),('10/12','Huawei counts'),('96','drones at Ukraine')]
REGS=[('Europe',9,(178,34,34)),('Middle East',8,(200,120,30)),('Asia',8,(30,90,180)),('Africa',2,(25,120,70)),('Americas',7,(120,60,140)),('World/Space',4,(90,90,90))]
PINS=[(1,24.7,46.7),(2,31.2,121.5),(3,40.7,-74.0),(4,47.8,35.2),(5,14.7,-17.4),(6,26.5,56.0),(7,40.7,-74.0),(8,47.7,-122.1),(9,39.8,30.5),(10,10.4,-75.5),(11,12.8,45.0),(12,13.0,44.9),(13,39.7,98.5)]
NA=[(-168,66),(-140,70),(-125,71),(-110,68),(-95,69),(-85,66),(-80,73),(-65,60),(-55,52),(-60,46),(-70,42),(-75,35),(-80,32),(-81,26),(-90,21),(-97,16),(-92,15),(-83,9),(-79,9),(-90,14),(-97,16),(-105,20),(-110,23),(-117,33),(-125,40),(-124,48),(-135,58),(-155,58),(-165,60)]
SA=[(-79,9),(-77,4),(-80,-3),(-81,-6),(-77,-12),(-70,-18),(-70,-23),(-65,-30),(-62,-38),(-65,-45),(-68,-52),(-66,-55),(-70,-50),(-62,-42),(-58,-35),(-52,-32),(-48,-27),(-41,-22),(-35,-9),(-35,-6),(-42,0),(-50,0),(-52,4),(-60,8),(-68,11),(-75,10)]
AF=[(-17,15),(-10,30),(-5,35),(10,37),(20,32),(32,31),(35,28),(38,22),(43,12),(51,11),(48,0),(40,-10),(35,-18),(32,-26),(28,-33),(20,-35),(15,-27),(12,-18),(13,-10),(9,4),(4,6),(-8,5),(-13,8),(-17,15)]
EU=[(-10,36),(-9,43),(-2,48),(-4,50),(0,51),(5,53),(8,57),(10,59),(18,56),(21,55),(24,59),(30,60),(28,65),(30,70),(40,68),(45,66),(50,68),(55,68),(60,69),(65,68),(60,60),(55,55),(48,50),(40,47),(35,45),(30,46),(28,44),(23,40),(22,37),(19,42),(12,44),(8,44),(3,42),(0,38),(-9,37)]
AS=[(30,70),(40,68),(50,68),(60,69),(70,72),(80,73),(90,75),(110,76),(130,72),(150,70),(160,66),(162,60),(158,52),(142,50),(140,40),(135,35),(130,33),(127,35),(122,38),(120,32),(122,28),(118,25),(110,20),(108,12),(105,9),(100,8),(98,12),(95,16),(92,21),(88,22),(85,19),(80,13),(77,8),(75,12),(72,20),(68,22),(62,25),(57,26),(54,26),(52,28),(50,30),(48,30),(44,29),(40,31),(36,36),(35,33),(32,31),(30,36)]
AU=[(113,-22),(114,-30),(115,-35),(120,-34),(129,-32),(132,-32),(135,-35),(140,-38),(147,-39),(150,-37),(153,-32),(153,-27),(150,-22),(146,-19),(142,-15),(142,-11),(137,-12),(135,-15),(132,-12),(130,-13),(126,-14),(122,-17),(118,-20),(113,-22)]
GL=[(-45,60),(-40,65),(-30,68),(-22,70),(-25,76),(-35,80),(-55,80),(-58,75),(-52,70),(-45,60)]
def main():
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im); d.rectangle([0,0,W,6],fill=RED)
    txt(d,12,12,'THE WORLD ON ONE DAY',SBN(11),RED); txt(d,1012,12,'38 STORIES \u00b7 6 REGIONS \u00b7 13 FIELDS',SBN(11),RED,align='r')
    txt(d,512,26,'Tuesday 24 November 2026',SB(34),align='c'); txt(d,512,64,'Riyadh tower hit again \u00b7 Shanghai party chief probed \u00b7 Huawei guilty on 10 of 12 counts',SB(13),RED,align='c')
    x=12
    for name,n,c in REGS:
        w=140; d.rectangle([x,84,x+w,102],fill=c); txt(d,x+w/2,87,f'{name} {n}',SBN(10),(255,255,255),align='c'); x+=w+4
    d.rectangle([12,108,1012,110],fill=LINE); txt(d,12,114,'THE DAY IN UTC',SBN(10),RED)
    ux=12
    for t,e in UTC:
        txt(d,ux,128,t,SBN(10),NAVY); txt(d,ux,140,e,SN(9)); ux+=143
    d.rectangle([12,158,1012,160],fill=LINE); txt(d,12,164,'THE DAY IN NUMBERS',SBN(10),RED)
    nx=12
    for v,l in NUMS:
        txt(d,nx,178,v,SB(20),NAVY); txt(d,nx,202,l,SN(9)); nx+=125
    hy=224; hw=326; hx=12
    for n,kick,ch,head,deck,kind,src in HEROES:
        scene(d,hx,hy,hw,64,kind); d.rectangle([hx,hy+64,hx+hw,hy+174],fill=(255,255,255)); d.rectangle([hx,hy+64,hx+hw,hy+174],outline=LINE)
        txt(d,hx+8,hy+68,f'{n}  {kick}',SBN(9),RED); chip(d,hx+8,hy+84,ch); txt(d,hx+8,hy+100,head,SB(14),mx=hw-16,leading=16); txt(d,hx+8,hy+134,deck,SN(9),mx=hw-16,leading=11); txt(d,hx+8,hy+160,src,SN(8),GREY); hx+=hw+8
    cy=406; cw=194; cx=12
    for n,kick,ch,head,deck,kind,src in CARDS[:5]:
        scene(d,cx,cy,cw,52,kind); d.rectangle([cx,cy+52,cx+cw,cy+140],fill=(255,255,255)); d.rectangle([cx,cy+52,cx+cw,cy+140],outline=LINE)
        txt(d,cx+6,cy+56,f'{n}  {kick}',SBN(7),RED); txt(d,cx+6,cy+68,head,SB(11),mx=cw-12,leading=13); txt(d,cx+6,cy+96,deck,SN(9),mx=cw-12,leading=11); chip(d,cx+6,cy+120,ch); cx+=cw+8
    cy=554; cx=12
    for n,kick,ch,head,deck,kind,src in CARDS[5:]:
        scene(d,cx,cy,cw,52,kind); d.rectangle([cx,cy+52,cx+cw,cy+140],fill=(255,255,255)); d.rectangle([cx,cy+52,cx+cw,cy+140],outline=LINE)
        txt(d,cx+6,cy+56,f'{n}  {kick}',SBN(7),RED); txt(d,cx+6,cy+68,head,SB(11),mx=cw-12,leading=13); txt(d,cx+6,cy+96,deck,SN(9),mx=cw-12,leading=11); chip(d,cx+6,cy+120,ch); cx+=cw+8
    mx,my,mw,mh=12,698,648,150; d.rectangle([mx,my,mx+mw,my+mh],fill=SEA); d.rectangle([mx,my,mx+mw,my+mh],outline=LINE)
    def pt(lon,lat): return (mx+(lon+180)/360*mw,my+(75-lat)/130*mh)
    for poly in (NA,SA,AF,EU,AS,AU,GL): d.polygon([pt(lo,la) for lo,la in poly],fill=LAND,outline=(150,140,115))
    txt(d,mx+6,my+4,'WORLD MAP \u2014 13 STORIES PINNED',SBN(9),NAVY)
    off={3:(0,-16),7:(14,10),11:(0,-16),12:(16,8),1:(0,-14),2:(0,-14)}
    for n,lat,lon in PINS:
        px,py=pt(lon,lat); dx,dy=off.get(n,(0,-13)); lx,ly=px+dx,py+dy
        if (dx,dy)!=(0,-13): d.line([(px,py),(lx,ly)],fill=RED,width=1)
        d.ellipse([lx-8,ly-8,lx+8,ly+8],fill=RED,outline=(255,255,255)); txt(d,lx,ly-5,str(n),SBN(9),(255,255,255),align='c')
    lx=676; txt(d,lx,my+2,'MAP LEGEND',SBN(10),RED); ly=my+20
    for i,(n,kick,ch,head,deck,kind,src) in enumerate(HEROES+CARDS):
        colx=lx+(170 if i>=7 else 0); yy=ly+(i%7)*12; txt(d,colx,yy,f'{n}  {kick.title()}',SBN(8))
    txt(d,lx,ly+92,'Red pin = story number. Pins 3 & 7 share',SN(9),GREY); txt(d,lx,ly+104,'New York; pins 11 & 12 share the Aden',SN(9),GREY); txt(d,lx,ly+116,'coast \u2014 offset with leader lines.',SN(9),GREY)
    txt(d,12,852,'ALSO ON TUESDAY 24 NOVEMBER \u2014 25 MORE STORIES',SBN(11),RED)
    colw=330; ay=866
    for i,(n,city,head) in enumerate(ALSO):
        col=i//9; row=i%9; ax=12+col*colw; yy=ay+row*10; txt(d,ax,yy,f'{n}. {city}: {head}',SN(8),mx=colw-6,leading=10)
    d.rectangle([12,958,1012,1000],fill=(255,235,235),outline=RED)
    txt(d,20,962,'DATE CHECK \u2014 Every story above happened or was first reported on Tuesday 24 November 2026. Wires read up to 23:00 UTC.',SBN(9),RED,mx=980,leading=11)
    txt(d,20,976,'LEFT OUT (not 24 Nov): Hormuz mine claims (23 Nov) \u00b7 Nvidia CEO return (23 Nov) \u00b7 EU sanctions (23 Nov) \u00b7 COP31 no deal (22 Nov) \u00b7 Merkury sunk (22 Nov) \u00b7 El Chapo arrested (Fri 20 Nov) \u00b7 Cikande fire began (Sat 21 Nov).',SN(8),mx=980,leading=10)
    txt(d,20,988,'NOT YET: Shenzhou-24 launch (Wed 25 Nov 00:18 UTC) \u00b7 MPR session picks VP (11 Dec) \u00b7 Huawei sentencing (Sep 2027) \u00b7 Hasina returns (16 Dec).',SN(8),mx=980,leading=10)
    txt(d,12,1006,'Sources: dailysummaryof.com \u00b7 Reuters \u00b7 AP \u00b7 UKMTO \u00b7 CAS \u00b7 CMSA \u00b7 CCDI. CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on record \u00b7 REPORTED = one outlet. Scenes are drawn, not photos.',SN(8),GREY,mx=1000,leading=10)
    out=os.path.join(os.environ.get('MAKEFUN_OUTPUT_DIR','out'),'entry.png'); os.makedirs(os.path.dirname(out),exist_ok=True); im.save(out,optimize=True); print(out,os.path.getsize(out))
if __name__=='__main__': main()
