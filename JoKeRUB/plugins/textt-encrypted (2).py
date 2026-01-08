
import base64
import zlib
import hashlib
import sys


def __anti_debug():
    import sys
    import inspect
    
    # تحقق إذا كان الكود يجرى في مصحح أخطاء
    try:
        trace_func = sys.gettrace()
        if trace_func is not None:
            print("⚠️ تم الكشف عن مصحح أخطاء!")
            sys.exit(1)
        
        # تحقق من عمق الاستدعاءات (بحد أدنى للبيانات الكبيرة)
        frame_count = len(inspect.stack())
        if frame_count > 50:
            print("⚠️ نشاط مشبوه!")
            sys.exit(1)
    except:
        pass

def __integrity_check(data_hash):
    # فحص سلامة البيانات المخفف
    expected_hash = "f60678f04dfb33ac"
    current_hash = hashlib.sha256(data_hash.encode()).hexdigest()[:16]
    return expected_hash == current_hash

# فحص الحماية (فقط للبيانات الصغيرة)
if True:
    __anti_debug()


def __decrypt_protected(data, layers=1):
    current = data
    
    # فحص سلامة البيانات (مخفف للبيانات الكبيرة)
    if True:
        try:
            expected_hash = "f60678f04dfb33ac"
            current_hash = hashlib.sha256(data.encode()).hexdigest()[:16]
            if expected_hash != current_hash:
                print("⚠️ تحذير: قد يكون الملف تالفاً")
        except:
            pass
    
    for layer in range(layers-1, -1, -1):
        if layer > 0 and True:
            try:
                current = base64.b64decode(current.encode('utf-8')).decode('utf-8')
            except:
                break
        
        # معرفة الفاصل المستخدم
        separators = ['|', '~', '^']
        separator = None
        for sep in separators:
            if sep in current:
                separator = sep
                break
        
        if separator and True:
            # فك التشويش (للبيانات الصغيرة فقط)
            parts = current.split(separator)
            clean_parts = []
            
            for part in parts:
                if ":" in part:
                    segments = part.split(":")
                    if len(segments) >= 2:
                        _, chunk = segments[0], ":".join(segments[1:])
                        clean_parts.append(chunk)
                    else:
                        clean_parts.append(part)
                else:
                    clean_parts.append(part)
            
            clean_parts.reverse()
            current = "".join(clean_parts)
        
        # فك rot47
        decrypted_chars = []
        for i, char in enumerate(current):
            if 33 <= ord(char) <= 126:
                shift = 47 if True else 25 + (layer * 3)
                new_code = ((ord(char) - 33 - shift) % 94) + 33
                decrypted_chars.append(chr(new_code))
            else:
                decrypted_chars.append(char)
        current = ''.join(decrypted_chars)
    
    # فك الضغط
    try:
        decoded = base64.b64decode(current.encode('utf-8'))
        decompressed = zlib.decompress(decoded)
        return decompressed.decode('utf-8')
    except:
        # إذا فشل فك الضغط، حاول كـ base64 عادي
        try:
            decoded = base64.b64decode(current.encode('utf-8'))
            return decoded.decode('utf-8')
        except Exception as e:
            print(f"❌ خطأ في فك التشفير: {str(e)[:50]}")
            return ""

# البيانات المشفرة
__encrypted_data = """314:!Bpl|455:b^p9Az|460:;H7Fz+|725:5C<GGB|487:thq?s;|545:KA!a74|782:b{$>?@|760:cw\";be|579:~yexK_|537:=H4?\":|453:J&Bgc2|223:@AfB=%|454:AFtHE{|586:z#*)_H|397:?8;wIB|119:a7}qI^|726:;c;f\";|121:s#9@:c|951:#q_:g9|941:uE:x9s|964:=rt:s#|883:\'5#^Aq|870:w)KF!B|994:f;|cs!|993:rdhZ7v|747:#g3FyK|521:zte6p>|222:Z|qd8s|829:h4C{<v|949:z2F?2(|744:FB&(&4|221:<#s(5B|759:a%4IwB|250:AwbE$b|496:2>E2E<|595:h;GE+C|334:b(s!$d|257:5~C>*h|638:>`a4`<|547:aDc7\'K|275:h4sC<=|102:=e\'9bs|716:\'t`\"}G|798:`G}w|;|912:A~7C^*|974:f+q)7\"|617:ZAe3>C|587:yxZE2p|689:^?2K8=|617:$;88~B|851:srfAe`|696:>_b=wc|119:$G}#4s|700:qt4hF(|253:$<t^3y|639:3\"7|!F|740:Ac+EZ:|696:7q{_^b|780:Fg~<~5|561:2x+9gc|933:ybg|}Z|215:A~`G&t|309:s{x%^?|765:%%Fs~~|386:g>#x5a|302:9bZ2{;|946:A?C$?z|718:y>>\'46|541:a{zBZ;|415:Fb<bI2|616:Gh>~&\"|164:}&ea$B|390:8*!%r+|901:>s(6?4|971:6waft#|710:A<wpc$|846:r}*q3H|173:?btzw6|665:_h|$B:|830:yf^~+e|823:|u2Ib9|116:GI&(|+|342:~h32x@|276:(v%(f:|969:)Jhsy!|839:3I{tF3|466:}}D:>a|735:pcI>Hw|543:IBhJ!*|651:}4ww|#|710:#{|@s>|389:?{a@Z)|614:G%#y{2|342:~r5{`!|933:Hegq?q|609:gd8?t3|805:sE4zd||845:+6|4&4|654:h22yB5|462:73Z$2t|838:sE*3p`|920:>~g7=C|337:g$G{hg|180:6hfF(@|451:~5GB<!|422:@u}$q=|262:+\'C\'5K|662:x~rD~z|115:584bCw|843:BJu6B_|696:5&t5`e|535:<F6tB<|529:&Bvs6v|827:8y{wdK|856:GxHrZE|600:`sb2yB|722:x}}ety|389:ytw)ZE|121:=:9rrG|507:)u##a:|724::F4q_+|607:A>&fDH|948:%E|C$K|222:C4Z???|342:Bu%@vx|332:q&c?:8|298:Z\"zG(`|195:^G?|_u|379:KEuIFF|872:)pw2E2|308:$=x!Gy|809:`D}I)6|966:)cfA35|651:6cw{{B|601:h!;&wZ|265:q_J=)3|369:!+a6be|208:757&B#|676:}cs@JF|932:eaKh\'&|767:?w?IHb|999:$aaFgu|449:Fy7vKd|559:ca4hr#|426:$u5*Cu|335:bZ8!<`|656:;tc+B4|906:$5GE#f|324:yG<e@~|763:~B&%)>|231:c4^?8}|781:vc=r=f|394:3e4h5C|127:(dw5A\'|475:fEEb8K|793:g%cp\'p|116:e_q8E}|220:<)_G@\"|780:(ZBgd9|174:!8F4^r|372:%*}%`a|736:72}732|519:$e$<@8|702:2$}Apy|314:x&?DE||773:t\'=$>9|557:cZepC:|611:5Bb5ah|500:{vt5;F|247:&^#23A|550:Z!>Gr4|359:*)u=;r|441:ga9Iy*|581:>dHZG\'|729:Fe95*%|334:+#\'*{$|610:wJtKAK|106:)F&!Ga|270:~5B3%B|558:&{:;p^|464:I&fAfd|691:2=\"\'?!|337:3\"\'CZI|184:Jy|7$x|932:2(FG~h|337:t3f%~C|134:u%G9#z|782:22~8d:|746:ey`y_b|694:By9$2u|358:\'e?53d|676:|gv:~7|319:2\'(3dx|739:;$F|)r|628:Bewb3)|585:<G@>e{|950:87<p$)|351:t#A%<7|347:g`g^x_|691:_#AZr\"|275:#x=aaD|603:Ez3CDu|985:95>HxC|144:%A9+uZ|533:}rg*Bt|239:\"a=\'C_|393:K@=K<t|290:D7cJ{c|657:AJD$;:|974:D2KaEG|645:w4@h5`|141:|Gh_$J|101:p#s)6%|233:`=xAqf|727:A8\'a;J|110:yB?$%\"|750:!>{8(&|392:)Kg|ch|253:@8G854|192:u}K?@K|141:c3deBg|401:c&Cw7~|856:4qD?!Z|163:Gs:\'|t|359:^I=6uD|121:f`b@KG|883:bvvf{\"|410:g72~^d|459:\'z^4z4|759:HBZ%`A|154:@%bGF3|101:(s!*s!|981:AD*$<w|906:Zbae^q|667:}w_5J;|704:@B_#26|407:8;Hh)>|944:p?>G~4|292:5aq+yd|511:wEwB`#|558:z\'sfKZ|513:g_dpC5|380:u?zev2|401:Iw8hp5|395:*32dr%|209:c*dA2b|568:=H:\":<|982:\"FsDJ$|779:{;cas\'|613:?4I:qu|881:Z%H4(p|476:?3y)qC|546:(6@a+s|553:bF4a6z|181:sFuZDK|493:\"6C5a=|692:#hh6h{|853:&s`CEJ|963::~df(r|159:`$A>xu|284:@`2d>J|931:5=4fxF|982:h{(`q\'|289:G4a#;y|805:\'duw\"=|182:}?ehsb|958:_`I|c5|956:q^=p&w|922:_7}c_z|244:edbg!5|915:t;E;7@|564:8I!z6h|624:;BKB:~|241:$395Ja|844:`_\'p;p|157:x}I*+:|983:G)63<h|435:eKJxy+|956:}_4\'zD|239:yaz|8t|409:chu{eA|733:!Z&^?I|427:#!AhqD|946:=(?Z*3|575:bAeF{c|728:77+_f?|187:~K8&te|404:*E75w3|323:`9H=Bc|700:b?hACB|722:&x|qB$|616::<BJBu|909:t^x!r<|904:y7Ba*g|244:$Cp+=v|732:f#Z}\"&|322:+6v(({|471:e^@DCq|796:3I^b!Z|219:>p\"7w+|344:yA=$s8|140:d(t(h*|174:G9wq<\"|326:bJE$I)|462:+fs=z;|309:?E\'pIJ|732:AB@q:%|859:&E=hZZ|971:G`EcZA|313:AH9&|}|139:Dgsf\"\'|206:!9&+26|286:&BJ}|4|103:+9qG4Z|131:>w{^\'E|237:aJ_IJ$|596:#c<G($|703:Dcz)~>|598:\"8\'6)Z|579:+uG2bI|893:y\"r*4%|446:$v39_E|941:Kf>)E`|189:<7D{e7|403:8c)IJ=|508:rHA982|443:`&+a`D|465:*F`4&I|334:K5vJK+|567:!Ba=tD|637:?4s2z(|713:\'3gGE8|714:@Bq2@u|119:\"vr(`t|973:Eb>Et%|417:t(E\"Dv|760:4AH%C7|637:y:2pc\'|660:Z>rHKx|229:|bFb?v|514:@sa5Gz|638:8+*H(>|130:p{>gC5|364:<EB!HI|532:2B{<G9|579:K7g?p4|434:Z6d73G|209:qqA|av|912:|Bq*u=|380:*3\'qbI|179:9({xwr|768:D)(\"}%|613:>\'~qE:|647:9uC\'sy|791:K:D@h?|972:wqGp)u|133:he+z`B|915:vZBbr\'|813:@%t|@~|672:??h66z|234:E_^}B_|629:2:y&:;|543:9=u3b9|233:~JBdKa|407:;F((@3|182:#}6rt9|434:aI`6yf|679:{<6}5s|373:\'E\'8bd|480:FdrsyZ|909:85|#+t|276:E~5gJJ|823:v(\"Cw<|724:`yKJ|b|111:Hu!v*h|271:w\'6g=I|307:x<hEK7|365:a&4Js*|348:B&b~&d|332:)23\"Z}|212:;8&s#H|821:\"3{2Bh|397:Z`\"bdy|454:`>u#u\'|684:3hhz7G|179:E(B;(^|446:z=}sI*|161:28&&bK|374:Ah()^w|123:$^(Jc^|801:2bfC{J|261:H:?z`z|497:@e\"e\"\'|539:sv^}Gp|897:(5H_J=|470:98D3H<|174:{&qzx(|354:$+v~r!|132:D3*9v7|430:dB333>|988:Be(\'*e|120:gAFJFs|838:h@C%5J|626:`|$xK_|922:3?`tq~|803:|$@rb>|688:=B)~Ex|915:d\'x\'\"6|229:x4>6Fb|821:74<f{=|990:3Z^ABd|441:^h7d+y|134:!^`Feb|356:D&gK6}|962:3t%\'aK|294:)C2D^q|892:;>Ad;%|306:>vsp=C|986:J^F?eb|877:^3Zh|!|160:t^Cb_}|149:+B:p{~|769:)g~%6>|967:qewz{H|846:#J|q2=|195:B~%D\"?|754:hrzJJH|999:Z:@#E#|618:~}z^e~|310:IZ^|JG|174:^IChZx|792:^?^<Zu|246:?@Jy8!|481:`$cK~>|960:9p|hp<|627:<%;<d!|537:G^t8~s|895:@>_&?4|635:I~zB}H|930:s{!^=\"|922:Hx`\"KJ|455:~#9axc|883:6#x3u(|981:Z^II66|794:ZGyq3c|691:?4wd@+|505:|_g^e\"|976:C8uc}s|713:E6+*9>|878:#:h^HB|705:5s:+;r|744:rr>@^p|535:v74(H)|612:;G84^b|193:(&!@qd|561:J=2G*:|430:J%gICJ|718:9|&czG|353:$F%2cg|882:|&@uKA|768::`\'$\"#|387:c=a^r\"|990:Bud{Bf|719:rFEysK|827:>45!5:|751:qBAu&J|844:!;aq93|292:u`4)u<|329:\"F:w38|630:;K%)7d|193:>(A&7h|842:ebF$=8|831:z!=$g&|869:K$=xp)|155:v9$pB~|845:rgt9<y|587:xxd9w%|805:=#gDzA|383:|868$B|807::C`\'>(|838:)~$@`r|958:t+{uwA|733:8zHf4r|996:)\"x&6u|267:zd9(u:|900:;!EZ?!|712:8B#tw||190:;@:>vw|712:a#I4=+|710:e<!+>(|474:x(8q3?|265:4rtgB)|577:{&B!~_|626:3*KIAu|951:~*G{px|515:z+8?%!|792:\'g9~6>|625:9qugEz|818:?Bz83q|551:ErHB+&|362:b5C9~&|764:%rwr;t|601:dtDpdH|687:}>a3H$|857:{4*J!b|642:8Ks@H!|243:C;<tvK|229:y=A5c4|512:a4hqKw|430:HF2Ewb|908:dy\'e&q|761:;!)GJ~|334:7^Kb;^|390:E\')@s7|356:Fcx\'ax|782:267#)$|318:&3$eZ\"|336:}~;(ZD|850:x|Jp?w|800:;@rtFA|740:(zdJ4B|866:(:?zzu|223:gq\'*3A|872:dpr9rx|650:C{tf4;|425:eu!#sH|429:q)G=5v|606:zrw)3p|854:`&Ku>)|569:)?E_s3|885:Cu(HJh|845:qe\'@Jp|353:~ZGpJ(|652::4C*C(|599:5_s%<=|709:4)+r7||979:D@?:z5|479:B)=^z\"|132:FxEHD:|300:x)s(*(|704:Z=9>e\"|264:x<H9fr|358:^8|Bp%|706:x>;$98|570:zz}J8!|630:$y>:%9|674:`%t(3~|326:s=deer|582:=g8$2D|354:88zxdy|659:y#;b;8|625:xx|>)4|121:JJ6uw$|627:y>vBw||381:34(6hK|797:Au87&q|100:BEDE8D|743:|s^<:3|410:c&$d&!|226:5\'2%zr|862:?Jp@|4|939:8he:f3|762:h(v{hg|634::<D}d{|476:$g\'zA(|944:{pxE*~|807:{H}h#v|158:#{_;tp|221:yhF\'a2|596:*F\"*p8|456:9?q62e|909:y}?\'c\'|905:srF*>E|317:qvDvZK|922:|A:)`@|790:9gq)BD|925:v+!92+|202:#wF!B4|835:|`#=I@|456:I`=:;3|150:`7A3K`|565:_du`zI|556:CtF\'Iz|113:aZCyu$|630:uc+6u8|431:v%qzJr|800:st}|Eb|443:K<(%88|271:HKtF2F|689:|EeC>x|130:;qe&&b|946:p\"C^{}|658:Gy&dg\'|861:hr:q(9|637:35zqZz|454:r$CA)w|669:p&9ys;|484:;48hq8|237:$|Ex*{|659:$&Gutr|874:fF7EuJ|379:I\"I2gr|880:\'=Zu9<|823:d=J{h||126:q4!7\"F|938:~&fq7\"|667:yxDF$J|195:$p?6<+|992:?Zz?6H|159:vZ#vpB|416:hp*{?\'|543:z2*`>v|184:6FI~s&|506:C%=I<)|216:|!t9v#|293:@^6t*@|667:9$d8:\"|967:~D++y:|155:h;yFfg|888:#@CdsZ|531:{e@^>2|234:<H}rp@|826:B9z+tH|904:4wZyH\"|465:>#x|st|325:>B(\'\'8|447:dq3A5E|365:*tp\'<9|739:a43h}&|436:IB;<{H|439:>|#!)a|380:*dw!z$|291:9%vg9c|157:6\"#?c8|417:~Ftw++|199:&sZ)3+|144:yqG({8|323:Ke!f_\"|976:e(t#ta|104:=H(d(D|212:q@Dx{;|722:|<7I!(|127::9{vK^|504:^r}`+y|789:rv*K3e|676:}IJyvb|495:KDx!:#|955:(|epFc|713:$!~rD7|164:;(!bvd|604:Z{{?Dv|462:`Z{BHr|828:}`4I+D|670:I+8)c+|722:\'y9}v@|730:+@r!`q|147:C6$%D^|675:(?c%?C|186:#`?wZy|774:qBFuIJ|386:Eh6D:C|784:|I|x+8|233:f{Jh2||165:s;){w)|994:Id`DKJ|614:b*(&uv|542:|2J:f:|898:E:dH!(|619:7Ds|(2|300:<y\"q:\"|109:f^Dt^G|792:?xIrJF|131:t73f7x|547:=^dwtJ|932:??8:f8|514:K9+v\"g|296:;De~_h|609:yaIF63|791:tK!y4w|248:bAI9Zu|657:#Z}795|670:\"e<8:~|183:_6vy$w|239:624F*G|280:yJ{%_$|790:xdwtg||609:+bI<3s|244:euIJ|y|687:#r\"cu*|272:IBKB!I|966:;5c|b*|878:BD8&*^|222:+vIc5v|809::rg};&|186:>dJ|K>|318:4^^;xc|815::!g>g@|319:(g<DZZ|214:sJ7w}2|455:2s?g5;|768:(wIz&8|841:6FtFw*|317:<\'9JIB|610:J#uyuw|553:I~%&5s|326:$$?x;w|137:?I{y$s|668:^!hKp#|452::4?<td|589:8Gxe~K|776:I!g4$*|688:}7!#u7|919:+s\"+v#|366:%Gt^u<|441:%ZI6=g|215:p:es5q|746:&5}G\"g|938:98\'\"y`|620:Ih^7<u|293:Eh^\"|g|795:6Zs~f%|378:vsx;#H|795:>}5!?||648:`5a#(c|606:$uE\';s|550:9{<:_H|746:9h2>Gr|298:>C2~`+|599:|4*Ba%|551:t&vvw?|639:~J!H+p|393:ZDGgps|433:757t%K|208:8A~a`?|934:a;=f\"5|890:9=2hDB|118:apE(&\'|686:d+\')u5|100:H:hCb_|151:pKh@z5|786:cZ!#:C|807:D>%=^h|548:?s}bf{|657:7~64f{|844:p^76|a|663:Dz(w&&|419:F54a?>|929:^\"ddJ+|905:*^<sa+|434:CBbf;b|483:vp7|>f|597:+I:*_s|519:\'AD__;|527:Dbc$({|620:DI{vvq|837:IB%yA@|955:{K9p2a|733:)\'%Jtr|855:B{2E\'w|634:9#\'h`Z|414:}J*9yt|415:)a8_t3|815:^Fd7|)|609:`!(g<\'|571:6yK}(a"""

# تنفيذ فك التشفير والتشغيل
try:
    __result = __decrypt_protected(__encrypted_data)
    exec(__result)
except SystemExit:
    pass
except Exception as e:
    print(f"❌ خطأ تنفيذي: {str(e)[:100]}")
