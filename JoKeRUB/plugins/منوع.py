import asyncio
import time
from telethon import functions
from collections import deque
from random import choice
from telethon.tl.types import InputPeerUser
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc
from JoKeRUB import l313l
from ..core.managers import edit_delete, edit_or_reply
import os
import tempfile
import json
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

Citation1_morning = [
    "** أكثر شيء يُسكِت الطفل برأيك؟ **",
    "** تخيّل لو أنك سترسم شيء وحيد فيصبح حقيقة، ماذا سترسم؟ **",
    "** قناة الكرتون المفضلة في طفولتك ؟ **",
    "** الحرية لـ ... ؟ **",
    "** كلمة للصُداع؟ **",
    "** ما الشيء الذي يُفارقك؟ **",
    "** ما الشيء الذي يُفارقك؟ **",
    "** موقف مميز فعلته مع شخص ولايزال يذكره لك؟ **",
    "** أيهما ينتصر، الكبرياء أم الحب؟ **",
    "** كت تويت | بعد ١٠ سنين شنو تصير ؟ **",
    "** مِن أغرب وأجمل الأسماء التي مرت عليك؟ **",
    "** عمرك شلت مصيبة عن شخص برغبتك ؟ **",
    "** أكثر سؤال وجِّه إليك مؤخرًا؟ **",
    "** ما هو الشيء الذي يجعلك تشعر بالخوف؟ **",
    "** شنو الي يفسد الصداقة؟ **",
    "** شخص لاترفض له طلبا ؟ **",
    "** كم مره خسرت شخص تحبه؟ **",
    "** كيف تتعامل مع الاشخاص السلبيين ؟ **",
    "** كلمة تشعر بالخجل اذا قيلت لك؟ **",
    "** جسمك اكبر من عٌمرك او العكسّ ؟ **",
    "** أقوى كذبة مشت عليك ؟ **",
    "** تتأثر بدموع شخص يبكي قدامك قبل تعرف السبب ؟ **",
    "** هل حدث وضحيت من أجل شخصٍ أحببت؟ **",
    "** أكثر تطبيق تستخدمه مؤخرًا؟ **",
    "** ‏اكثر شي يرضيك اذا زعلت بدون تفكير ؟ **",
    "** شنو محتاج حتى تكون مبسوط ؟ **",
    "** مطلبك الوحيد الحين ؟ **",
    "** هل حدث وشعرت بأنك ارتكبت أحد الذنوب أثناء الصيام؟ **",
    "** اكثر مطور تحبه بالجوكر منو ؟ **",
    "** من هو الممثل المفضل لديك؟ **",
    "** من ستختار من بين الموجودين ليمسح دموعك ويخفف أحزانك؟ **",
    "** إذا رأيتِ أحد أجمل منكِ هل يمكن أن تشعري بالغيرة منها؟ **",
    "** كم علبة سجائر تقوم بتدخينها يومياً؟ **",
    "** هل أنت شخصية مغرورة؟ **",
    "** كم ساعة تقضيها على الإنترنت يومياً؟ **",
    "** ما هي عادتك اليومية المفضلة؟ **",
    "** ما هي العادة اليومية التي تقوم بها وتكرهها وتريد تغييرها؟ **",
    "** هل تخبر صديقك بكل أسرارك أم تحتفظ ببضع منها لنفسك؟ **",
    "** كيف ستتصرف إن قام صديقك المقرب بالابتعاد عنك بدون سبب؟ **",
    "** أي سنة من سنين حياتك كانت الأجمل، وما الذي حدث فيها؟ **",
    "** من الشخص الذي تحلم به كثيرًا عندما تنام؟ **",
    "** هل قمت بالكذب على أصدقائك من قبل ، ولماذا؟ **",
    "** هل أنت شخص عنيد؟ **",
    "** من الصديق الذي ستأخذه معه عند سفرك لقضاء عطلتك في أي بلد بعيدة؟ **",
    "** من هو آخر شخص تقوم بالتفكير فيه قبل نومك؟ **",
]


@l313l.on(admin_cmd(pattern="كت$"))
async def ithker(knopis):
    await knopis.edit(choice(Citation1_morning))

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
