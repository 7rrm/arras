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

async def fetch_prayer_times():
    file_url = 'https://hq.alkafeel.net/Api/init/init.php?timezone=+3&long=44&lati=32&v=jsonPrayerTimes'
    file_location = InputWebFileLocation(url=file_url, access_hash="")
    times_json = await l313l.download_file(file_location)
    return times_json

async def send_prayer_times(event):
    times_json = await fetch_prayer_times()
    times = json.loads(times_json)
    fajr_time = times['fajir']
    hijri_date = times['date']
    chat_id = event.chat_id
    input_file = await l313l.upload_file(bytes(times_json, 'utf-8'), part_size_kb=512)
    await l313l.send_file(chat_id, input_file, caption=f"وقت الفجر: {fajr_time}\nالتاريخ الهجري: {hijri_date}", force_document=True)

@l313l.on(admin_cmd(pattern="صلاه(?: |$)(.*)"))
async def handle_command(event):
    await send_prayer_times(event)

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
        await event.edit("**᯽︙ لا يوجد مستخدمين محظورين في حسابك 🤷🏻**")
        return
    for user in blocked_users.users:
        try:
            await client(functions.contacts.UnblockRequest(
                id=InputPeerUser(user.id, user.access_hash)
            ))
            aljoker_entity = await client.get_entity(user.id)
            aljoker_profile = f"[{aljoker_entity.first_name}](tg://user?id={aljoker_entity.id})"
            await event.edit(f"᯽︙ تم إلغاء حظر المستخدم : {aljoker_profile}")
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

###################################

import requests
from datetime import datetime, timedelta
from telethon import events

# --- إعداد مفاتيح API الخاصة بك ---
FOOTBALL_API_KEY = "b96b04a99b2848fae1ba546bad94feb7"
BASE_URL = "https://v3.football.api-sports.io"
headers = {
    'x-rapidapi-host': 'v3.football.api-sports.io',
    'x-rapidapi-key': FOOTBALL_API_KEY
}

# ==================== دوال المساعدة ====================

def get_arabic_time(match_time):
    """تحويل الوقت للعربية"""
    try:
        dt = datetime.fromisoformat(match_time.replace('Z', '+00:00'))
        days = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
        arabic_day = days[dt.weekday()]
        time_str = dt.strftime("%H:%M")
        date_str = dt.strftime("%Y-%m-%d")
        return f"{arabic_day} {date_str} الساعة {time_str}"
    except:
        return match_time

def get_match_status_arabic(status):
    """ترجمة حالة المباراة"""
    status_map = {
        'NS': '⏳ لم تبدأ',
        '1H': '⏱ الشوط الأول',
        'HT': '⏸ استراحة',
        '2H': '⏱ الشوط الثاني',
        'FT': '✅ انتهت',
        'LIVE': '🔥 مباشرة',
        'PEN': '🎯 ركلات الترجيح',
        'AET': '⏱ وقت إضافي'
    }
    return status_map.get(status, status)

def get_match_statistics(match):
    """استخراج الإحصائيات من بيانات المباراة"""
    try:
        home_stats = {}
        away_stats = {}
        
        if 'statistics' in match:
            for team_stats in match['statistics']:
                team_name = team_stats['team']['name']
                for stat in team_stats['statistics']:
                    if team_name == match['teams']['home']['name']:
                        home_stats[stat['type']] = stat['value']
                    elif team_name == match['teams']['away']['name']:
                        away_stats[stat['type']] = stat['value']
        
        return home_stats, away_stats
    except:
        return {}, {}

def format_statistics(home_stats, away_stats, home_team, away_team):
    """تنسيق الإحصائيات للعرض"""
    if not home_stats or not away_stats:
        return "📊 **لا توجد إحصائيات متاحة حالياً**"
    
    important_stats = [
        'Ball Possession', 'Shots on Goal', 'Total Shots',
        'Corner Kicks', 'Passes %', 'Fouls',
        'Offsides', 'Yellow Cards', 'Red Cards'
    ]
    
    message = "📈 **إحصائيات المباراة:**\n"
    for stat in important_stats:
        if stat in home_stats and stat in away_stats:
            message += f"• **{stat}:** {home_stats[stat]} - {away_stats[stat]}\n"
    
    return message

# ==================== الأوامر الرئيسية ====================

# --- الأمر: مباريات اليوم مع ID ---
@l313l.on(events.NewMessage(pattern=r"\.مباريات اليوم"))
async def today_matches_with_id(event):
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        url = f"{BASE_URL}/fixtures"
        params = {'date': today}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            await event.reply("⚠️ حدث خطأ في الاتصال بالخادم.")
            return
            
        data = response.json()
        matches = data.get('response', [])
        
        if not matches:
            await event.reply(f"📅 لا توجد مباريات بتاريخ اليوم ({today}).")
            return
        
        message = f"📅 *مباريات اليوم ({today}):*\n" + "="*50 + "\n"
        
        for match in matches[:15]:  # عرض أول 15 مباراة
            fixture = match['fixture']
            teams = match['teams']
            league = match['league']
            
            match_id = fixture['id']
            home_team = teams['home']['name']
            away_team = teams['away']['name']
            league_name = league['name']
            
            match_time = get_arabic_time(fixture['date'])
            status = get_match_status_arabic(fixture['status']['short'])
            
            # إضافة ID للمباراة
            message += f"🆔 **ID:** `{match_id}`\n"
            message += f"🏆 **{league_name}**\n"
            message += f"🕒 {match_time} | {status}\n"
            message += f"⚽ **{home_team}** 🆚 **{away_team}**\n"
            
            # إضافة نتيجة إذا كانت المباراة جارية أو منتهية
            if fixture['status']['short'] in ['FT', 'HT', '1H', '2H', 'LIVE']:
                goals = match['goals']
                home_goals = goals.get('home', 0) or 0
                away_goals = goals.get('away', 0) or 0
                message += f"📊 **النتيجة:** {home_goals} - {away_goals}\n"
            
            message += "─" * 40 + "\n"
        
        message += "\n📌 **استخدم:** `.لعبة ID` لعرض إحصائيات مباراة محددة"
        
        await event.reply(message, parse_mode='markdown')
        
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {str(e)}")

# --- الأمر: البحث عن مباراة بالإسم أو ID ---
@l313l.on(events.NewMessage(pattern=r"\.بحثث (.*)"))
async def search_match(event):
    try:
        search_query = event.pattern_match.group(1)
        
        # جلب مباريات اليوم
        today = datetime.now().strftime('%Y-%m-%d')
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        url = f"{BASE_URL}/fixtures"
        params = {'date': today}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            await event.reply("⚠️ حدث خطأ في الاتصال بالخادم.")
            return
            
        data = response.json()
        matches = data.get('response', [])
        
        # إذا لم توجد مباريات اليوم، جلب مباريات الغد
        if not matches:
            params = {'date': tomorrow}
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            matches = data.get('response', [])
        
        if not matches:
            await event.reply("⚽ لا توجد مباريات للبحث فيها.")
            return
        
        # البحث في المباريات
        found_matches = []
        
        for match in matches:
            fixture = match['fixture']
            teams = match['teams']
            league = match['league']
            
            match_id = str(fixture['id'])
            home_team = teams['home']['name'].lower()
            away_team = teams['away']['name'].lower()
            league_name = league['name'].lower()
            
            search_lower = search_query.lower()
            
            # البحث بالإسم أو ID
            if (search_lower in home_team or 
                search_lower in away_team or 
                search_lower in league_name or 
                search_lower == match_id):
                found_matches.append(match)
        
        if not found_matches:
            await event.reply(f"🔍 **لم أجد نتائج لـ:** {search_query}")
            return
        
        message = f"🔍 **نتائج البحث عن '{search_query}':**\n" + "="*50 + "\n"
        
        for match in found_matches[:10]:  # عرض أول 10 نتائج
            fixture = match['fixture']
            teams = match['teams']
            league = match['league']
            
            match_id = fixture['id']
            home_team = teams['home']['name']
            away_team = teams['away']['name']
            league_name = league['name']
            
            match_time = get_arabic_time(fixture['date'])
            status = get_match_status_arabic(fixture['status']['short'])
            
            message += f"🆔 **ID:** `{match_id}`\n"
            message += f"🏆 **{league_name}**\n"
            message += f"🕒 {match_time} | {status}\n"
            message += f"⚽ **{home_team}** 🆚 **{away_team}**\n"
            message += "─" * 40 + "\n"
        
        message += "\n📌 **استخدم:** `.لعبة ID` لعرض إحصائيات أي مباراة"
        
        await event.reply(message, parse_mode='markdown')
        
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {str(e)}")

# --- الأمر: عرض مباراة بالإحصائيات الكاملة (ID) ---
@l313l.on(events.NewMessage(pattern=r"\.لعبه (\d+)"))
async def match_by_id_handler(event):
    try:
        match_id = event.pattern_match.group(1)
        
        url = f"{BASE_URL}/fixtures"
        params = {'id': match_id}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            await event.reply(f"⚠️ خطأ {response.status_code} في الاتصال بالخادم.")
            return
            
        data = response.json()
        matches = data.get('response', [])
        
        if not matches:
            await event.reply(f"❌ **لم أجد مباراة بالـID:** `{match_id}`")
            return
        
        match = matches[0]  # أول نتيجة
        
        # استخراج البيانات الأساسية
        fixture = match['fixture']
        teams = match['teams']
        goals = match['goals']
        league = match['league']
        score = match.get('score', {})
        
        # البيانات الأساسية
        match_id = fixture['id']
        home_team = teams['home']['name']
        away_team = teams['away']['name']
        league_name = league['name']
        league_country = league.get('country', '')
        
        home_goals = goals.get('home', 0) or 0
        away_goals = goals.get('away', 0) or 0
        
        # الوقت والحالة
        match_time = get_arabic_time(fixture['date'])
        status = get_match_status_arabic(fixture['status']['short'])
        elapsed = fixture['status'].get('elapsed', '')
        venue = fixture.get('venue', {}).get('name', 'غير معروف')
        referee = fixture.get('referee', 'غير معروف')
        
        # بناء الرسالة الأساسية
        message = f"🏆 **{league_name}**"
        if league_country:
            message += f" ({league_country})"
        message += f"\n" + "="*50 + "\n\n"
        
        message += f"⚽ **{home_team}** 🆚 **{away_team}**\n"
        message += f"🆔 **معرف المباراة:** `{match_id}`\n"
        message += f"🕒 **الموعد:** {match_time}\n"
        message += f"📍 **الملعب:** {venue}\n"
        message += f"👨‍⚖️ **الحكم:** {referee}\n"
        message += f"📊 **الحالة:** {status}"
        if elapsed:
            message += f" (الدقيقة {elapsed})"
        message += "\n\n"
        
        # النتيجة
        if status in ['✅ انتهت', '⏱ الشوط الأول', '⏸ استراحة', '⏱ الشوط الثاني', '🔥 مباشرة']:
            message += f"🎯 **النتيجة:** **{home_goals} - {away_goals}**\n\n"
            
            # نتائج الشوط الأول إذا متاحة
            halftime = score.get('halftime', {})
            if halftime:
                ht_home = halftime.get('home', 0)
                ht_away = halftime.get('away', 0)
                message += f"⏱ **نتيجة الشوط الأول:** {ht_home} - {ht_away}\n\n"
        
        # إحصائيات المباراة
        home_stats, away_stats = get_match_statistics(match)
        stats_message = format_statistics(home_stats, away_stats, home_team, away_team)
        message += stats_message + "\n"
        
        # معلومات إضافية
        message += "\n📋 **معلومات إضافية:**\n"
        message += f"• **الجولة:** {league.get('round', 'غير معروف')}\n"
        
        # رابط المباراة
        message += "\n🔗 **للمتابعة:**\n"
        message += f"استخدم `.بحث {home_team}` أو `.بحث {away_team}` للبحث عن المزيد"
        
        await event.reply(message, parse_mode='markdown')
        
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {str(e)}")

# --- الأمر: المباريات الحية مع ID ---
@l313l.on(events.NewMessage(pattern=r"\.مباريات حية"))
async def live_matches_with_id_handler(event):
    try:
        url = f"{BASE_URL}/fixtures"
        params = {'live': 'all'}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            await event.reply("⚠️ حدث خطأ في الاتصال بالخادم.")
            return
            
        data = response.json()
        matches = data.get('response', [])
        
        if not matches:
            await event.reply("⚽ لا توجد مباريات حية الآن.")
            return
        
        message = "🔥 *المباريات الحية الآن:*\n" + "="*50 + "\n\n"
        
        for match in matches[:20]:
            fixture = match['fixture']
            teams = match['teams']
            goals = match['goals']
            league = match['league']
            
            match_id = fixture['id']
            home_team = teams['home']['name']
            away_team = teams['away']['name']
            league_name = league.get('name', 'دوري غير معروف')
            
            home_goals = goals.get('home', 0) or 0
            away_goals = goals.get('away', 0) or 0
            elapsed = fixture['status'].get('elapsed', '')
            status = get_match_status_arabic(fixture['status']['short'])
            
            message += f"🆔 **ID:** `{match_id}`\n"
            message += f"🏆 **{league_name}**\n"
            message += f"🕒 {status}"
            if elapsed:
                message += f" ({elapsed}')"
            message += f"\n⚽ **{home_team}** {home_goals} - {away_goals} **{away_team}**\n"
            message += "─" * 40 + "\n"
        
        message += "\n📌 **استخدم:** `.لعبة ID` لعرض إحصائيات أي مباراة حية"
        
        await event.reply(message, parse_mode='markdown')
        
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {str(e)}")

# --- الأمر: مباريات الغد مع ID ---
@l313l.on(events.NewMessage(pattern=r"\.مباريات الغد"))
async def tomorrow_matches_with_id_handler(event):
    try:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        url = f"{BASE_URL}/fixtures"
        params = {'date': tomorrow}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            await event.reply("⚠️ حدث خطأ في الاتصال بالخادم.")
            return
            
        data = response.json()
        matches = data.get('response', [])
        
        if not matches:
            await event.reply(f"📅 لا توجد مباريات بتاريخ الغد ({tomorrow}).")
            return
        
        message = f"📅 *مباريات الغد ({tomorrow}):*\n" + "="*50 + "\n\n"
        
        for match in matches[:20]:
            fixture = match['fixture']
            teams = match['teams']
            league = match['league']
            
            match_id = fixture['id']
            home_team = teams['home']['name']
            away_team = teams['away']['name']
            league_name = league['name']
            league_country = league.get('country', '')
            
            match_time = get_arabic_time(fixture['date'])
            status = get_match_status_arabic(fixture['status']['short'])
            
            message += f"🆔 **ID:** `{match_id}`\n"
            message += f"🏆 **{league_name}**"
            if league_country:
                message += f" ({league_country})"
            message += f"\n🕒 {match_time} | {status}\n"
            message += f"⚽ **{home_team}** 🆚 **{away_team}**\n"
            message += "─" * 40 + "\n"
        
        message += "\n📌 **استخدم:** `.لعبة ID` لعرض إحصائيات أي مباراة"
        
        await event.reply(message, parse_mode='markdown')
        
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {str(e)}")

# --- الأمر: مساعدة (عرض جميع الأوامر) ---
@l313l.on(events.NewMessage(pattern=r"\.مساعدة"))
async def help_command(event):
    help_text = """
📋 **أوامر بوت كرة القدم:** ⚽

🔍 **البحث والعرض:**
`.مباريات اليوم` - عرض جميع مباريات اليوم مع ID
`.مباريات الغد` - عرض جميع مباريات الغد مع ID
`.مباريات حية` - المباريات الحية الآن مع ID
`.بحث برشلونة` - البحث عن مباراة بالإسم
`.لعبة 592872` - عرض إحاصئيات مباراة بالـID

📊 **مثال على استخدام ID:**
1. استخدم `.مباريات اليوم` لرؤية جميع مباريات اليوم مع ID
2. اختر ID مباراة (مثال: `592872`)
3. استخدم `.لعبة 592872` لعرض إحصائياتها الكاملة

🎯 **الإحصائيات المتاحة:**
• ملكية الكرة • التصويبات على المرمى
• إجمالي التصويبات • الركلات الركنية
• نسبة التمريرات • الأخطاء
• التسلل • البطاقات

🤖 **مطور البوت:** @اسمك
"""
    await event.reply(help_text, parse_mode='markdown')
