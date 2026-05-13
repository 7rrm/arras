from JoKeRUB import l313l
from ..core.managers import edit_or_reply
from datetime import datetime
import random
import asyncio
from telethon import events
plugin_category = "fun"
#str 122939#المليون

Io = [
    "إِنَّ اللَّهَ مَعَ الصَّابِرِينَ - البقرة 153",
    "وَاصْبِرْ وَمَا صَبْرُكَ إِلَّا بِاللَّهِ - النحل 127",
    "وَلَنَبْلُوَنَّكُم بِشَيْءٍ مِنَ الْخَوْفِ وَالْجُوعِ وَنَقْصٍ مِنَ الْأَمْوَالِ وَالْأَنفُسِ وَالثَّمَرَاتِ - البقرة 155",
    "وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا - الطلاق 2",
    "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ - الطلاق 3",
"إِنَّ اللَّهَ يُحِبُّ الْمُتَوَكِّلِينَ - آل عمران 159",
"فَاذْكُرُونِي أَذْكُرْكُمْ - البقرة 152",
"وَتَوَكَّلْ عَلَى الْعَزِيزِ الرَّحِيمِ - الشعراء 217",
"إِنَّ رَبِّي لَسَمِيعُ الدُّعَاء - إبراهيم 39",
"فَسَبِّحْ بِحَمْدِ رَبِّكَ وَكُن مِّنَ السَّاجِدِينَ - الحجر 98",
"وَاستَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ - البقرة 45",
"وَمَا كَانَ اللَّهُ مُعَذِّبَهُمْ وَهُمْ يَسْتَغْفِرُونَ - الأنفال 33",
"وَأَقِيمُوا الصَّلَاةَ وَآتُوا الزَّكَاةَ - البقرة 43",
"فَإِنَّ مَعَ الْعُسْرِ يُسْرًا - الشرح 6",
"وَلَا تَيْأَسُوا مِن رَّوْحِ اللَّهِ - يوسف 87",
]
hadiths = [
    "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ - الكافي",
    "مَنْ صَلَّى عَلَيَّ وَاحِدَةً صَلَّى اللَّهُ عَلَيْهِ عَشْرًا - الكافي",
    "الصَّدَقَةُ تَدْفَعُ مِيتَةَ السُّوءِ - الكافي",
    "صِلْ مَنْ قَطَعَكَ وَأَعْطِ مَنْ حَرَمَكَ وَاعْفُ عَمَّنْ ظَلَمَكَ - الكافي",
    "العِلْمُ خَيْرٌ مِنَ الْمَالِ - الكافي",
"الْعِلْمُ نُورٌ يَقْذِفُهُ اللَّهُ فِي قَلْبِ مَنْ يَشَاءُ - الكافي",
"مَنْ عَرَفَ نَفْسَهُ فَقَدْ عَرَفَ رَبَّهُ - نهج البلاغة",
"الصَّمْتُ بَابٌ مِنْ أَبْوَابِ الْحِكْمَةِ - نهج البلاغة",
"أَفْضَلُ الْجِهَادِ جِهَادُ النَّفْسِ - الكافي",
"الْعَفْوُ عِنْدَ الْمَقْدِرَةِ زِينَةُ الْأَقْوِيَاءِ - نهج البلاغة",
"أَقْرَبُكُمْ مِنِّي مَجْلِسًا أَحَاسِنُكُمْ أَخْلَاقًا - الكافي",
"الصَّبْرُ مِنَ الْإِيمَانِ كَالرَّأْسِ مِنَ الْجَسَدِ - الكافي",
"مَنْ زَارَ قَبْرَ أَخِيهِ الْمُؤْمِنِ كَتَبَ اللَّهُ لَهُ ثَوَابَ حَاجٍّ وَمُعْتَمِرٍ - الكافي",
"أَفْضَلُ الْعِبَادَةِ انْتِظَارُ الْفَرَجِ - الكافي",
"الْجَنَّةُ تَحْتَ أَقْدَامِ الْأُمَّهَاتِ - الكافي",
]

@l313l.ar_cmd(
    pattern="آية$",
    command=("آية", plugin_category),
    info={
        "header": "أمر لجلب آية قرآنية عشوائية.",
        "description": "يُرسل آية قرآنية عشوائية.",
        "usage": "{tr}آية",
    },
)
async def random_quranic_verse(event):
    """ارسال ايات من القران """
    verse = random.choice(Io)
    await edit_or_reply(event, verse)

@l313l.ar_cmd(
    pattern="حديث$",
    command=("حديث", plugin_category),
    info={
        "header": "أمر لجلب حديث عشوائي.",
        "description": "يُرسل حديث عشوائي.",
        "usage": "{tr}حديث",
    },
)
async def random_hadith(event):
    """ارسال احاديث عشوائيه من نهج البلاغه والكافي الشعيه."""
    hadith = random.choice(hadiths)
    await edit_or_reply(event, hadith)
    

@l313l.on(events.NewMessage(pattern='.سباق'))
async def emoji_race(event):
    emojis = ["🍉", "🍎", "🍌", "🍇", "🍓", "🍍", "🍊", "🍐", "🍒", "🥝"]
    race_Emoji = random.choice(emojis)
    Po = datetime.now()
    await edit_or_reply(event,f"اول واحد يرسل هذا الايموجي {race_Emoji} يربح نقطة!")

    async with l313l.conversation(event.chat_id) as conv:
        while True:
            response = await conv.wait_event(events.NewMessage(incoming=True, pattern=race_Emoji))
            if response.sender_id != event.sender_id:
                break

    race_end_time = datetime.now()
    time_taken = (race_end_time - Po).total_seconds()
    Wi = await l313l.get_entity(response.sender_id)
    await response.reply(f"🎉 مبروك [{Wi.first_name}](tg://user?id={Wi.id}) \n- ثواني: {int(time_taken)} !!", parse_mode="md")


from JoKeRUB import l313l
from ..core.managers import edit_or_reply
from datetime import datetime
import random
import asyncio
import json
import requests
import re
from telethon import Button, events
from telethon.events import CallbackQuery
from ..Config import Config
from ..core import check_owner

plugin_category = "fun"

# جميع الأسئلة (40 سؤال)
QUESTIONS = [
    {"aW": "ما هو الحيوان الذي يمتلك أكبر عدد من الأسنان؟", "choices": ["القرش", "التمساح", "الفيل"], "Wa": "القرش"},
    {"aW": "ما هو العنصر الكيميائي الذي يرمز له بـ 'Au'؟", "choices": ["النحاس", "الذهب", "الفضة"], "Wa": "الذهب"},
    {"aW": "ما هي أكبر قارة في العالم؟", "choices": ["أوروبا", "آسيا", "أفريقيا"], "Wa": "آسيا"},
    {"aW": "من هو مؤلف رواية 'البؤساء'؟", "choices": ["شارلز ديكنز", "فيكتور هوغو", "ليو تولستوي"], "Wa": "فيكتور هوغو"},
    {"aW": "ما هي اللغة الرسمية للبرازيل؟", "choices": ["الإسبانية", "البرتغالية", "الإنجليزية"], "Wa": "البرتغالية"},
    {"aW": "ما هو أعمق محيط في العالم؟", "choices": ["المحيط الهندي", "المحيط الهادئ", "المحيط الأطلسي"], "Wa": "المحيط الهادئ"},
    {"aW": "من هو مخترع المصباح الكهربائي؟", "choices": ["ألكسندر جراهام بيل", "توماس إديسون", "نيكولا تسلا"], "Wa": "توماس إديسون"},
    {"aW": "ما هي عاصمة اليابان؟", "choices": ["أوساكا", "طوكيو", "كيوتو"], "Wa": "طوكيو"},
    {"aW": "ما هي الدولة التي تضم مدينة البندقية؟", "choices": ["فرنسا", "إيطاليا", "إسبانيا"], "Wa": "إيطاليا"},
    {"aW": "ما هو أطول نهر في العالم؟", "choices": ["النيل", "المسيسيبي", "الأمازون"], "Wa": "الأمازون"},
    {"aW": "من هو مؤلف كتاب 'الإخوان كارامازوف'؟", "choices": ["ليو تولستوي", "فيودور دوستويفسكي", "أنطون تشيخوف"], "Wa": "فيودور دوستويفسكي"},
    {"aW": "ما هو الطائر الذي يمكنه الطيران للخلف؟", "choices": ["النسر", "الطنان", "البومة"], "Wa": "الطنان"},
    {"aW": "ما هي أصغر دولة في العالم؟", "choices": ["موناكو", "الفاتيكان", "ناورو"], "Wa": "الفاتيكان"},
    {"aW": "من هو مؤلف مسرحية 'هاملت'؟", "choices": ["سوفوكليس", "ويليام شكسبير", "موليير"], "Wa": "ويليام شكسبير"},
    {"aW": "ما هو الكوكب الأصغر في المجموعة الشمسية؟", "choices": ["بلوتو", "عطارد", "المريخ"], "Wa": "عطارد"},
    {"aW": "من هو مؤلف رواية 'الحرب والسلام'؟", "choices": ["فيودور دوستويفسكي", "ليو تولستوي", "أنطون تشيخوف"], "Wa": "ليو تولستوي"},
    {"aW": "ما هو أقدم جامعة في العالم؟", "choices": ["جامعة بولونيا", "جامعة القرويين", "جامعة أكسفورد"], "Wa": "جامعة القرويين"},
    {"aW": "ما هو العنصر الكيميائي الذي يرمز له بـ 'O'؟", "choices": ["أوزون", "أكسجين", "أوسميوم"], "Wa": "أكسجين"},
    {"aW": "ما هي عملة اليابان؟", "choices": ["الوون", "الين", "اليوان"], "Wa": "الين"},
    {"aW": "من هو مؤلف مسرحية 'مكبث'؟", "choices": ["كريستوفر مارلو", "ويليام شكسبير", "بن جونسون"], "Wa": "ويليام شكسبير"},
    {"aW": "ما هو الحيوان الوطني لأستراليا؟", "choices": ["الكوالا", "الكنغر", "الإيمو"], "Wa": "الكنغر"},
    {"aW": "ما هي أكبر دولة في أفريقيا من حيث المساحة؟", "choices": ["السودان", "الجزائر", "ليبيا"], "Wa": "الجزائر"},
    {"aW": "ما هو أطول نفق في العالم؟", "choices": ["نفق سيكان", "نفق سانت غوتارد", "نفق لوشبرغ"], "Wa": "نفق سانت غوتارد"},
    {"aW": "ما هي أكبر جزيرة في العالم؟", "choices": ["نيو غينيا", "غرينلاند", "بورنيو"], "Wa": "غرينلاند"},
    {"aW": "من هو مؤلف كتاب 'الأمير'؟", "choices": ["توماس هوبز", "نيكولو مكيافيلي", "جون لوك"], "Wa": "نيكولو مكيافيلي"},
    {"aW": "من هو مخترع الراديو؟", "choices": ["نيكولا تسلا", "غوليلمو ماركوني", "ألكسندر جراهام بيل"], "Wa": "غوليلمو ماركوني"},
    {"aW": "ما هي عاصمة كندا؟", "choices": ["تورونتو", "أوتاوا", "مونتريال"], "Wa": "أوتاوا"},
    {"aW": "ما هو أقدم علم في العالم؟", "choices": ["علم الرياضيات", "علم الفلك", "علم الكيمياء"], "Wa": "علم الفلك"},
    {"aW": "ما هي أصغر دولة في أفريقيا؟", "choices": ["غامبيا", "سيشيل", "موريشيوس"], "Wa": "سيشيل"},
    {"aW": "ما هو البركان الأكثر نشاطاً في العالم؟", "choices": ["إتنا", "كيلاويا", "فيزوف"], "Wa": "كيلاويا"},
    {"aW": "ما هي اللغة الرسمية للأرجنتين؟", "choices": ["البرتغالية", "الإسبانية", "الإنجليزية"], "Wa": "الإسبانية"},
    {"aW": "ما هو العنصر الكيميائي الذي يرمز له بـ 'Fe'؟", "choices": ["الفلور", "الحديد", "الفرانسيوم"], "Wa": "الحديد"},
    {"aW": "ما هي عاصمة جنوب أفريقيا؟", "choices": ["كيب تاون", "بريتوريا", "جوهانسبرغ"], "Wa": "بريتوريا"},
    {"aW": "ما هو الحيوان الذي يعيش أطول عمراً؟", "choices": ["الفيل", "السلحفاة", "الببغاء"], "Wa": "السلحفاة"},
    {"aW": "ما هي اللغة الرسمية لمصر؟", "choices": ["الإنجليزية", "العربية", "الفرنسية"], "Wa": "العربية"},
    {"aW": "من هو مؤلف كتاب 'الجمهورية'؟", "choices": ["أرسطو", "أفلاطون", "سقراط"], "Wa": "أفلاطون"},
    {"aW": "ما هي عاصمة الهند؟", "choices": ["مومباي", "نيودلهي", "بنغالور"], "Wa": "نيودلهي"},
    {"aW": "كم عدد الكواكب في نظامنا الشمسي؟", "choices": ["9", "8", "10"], "Wa": "8"},
    {"aW": "ما هو أطول جبل في العالم؟", "choices": ["كيليمانجارو", "إيفرست", "ماونت كينيا"], "Wa": "إيفرست"},
    {"aW": "من هو مخترع التلفزيون؟", "choices": ["توماس إديسون", "جون لوجي بيرد", "نيكولا تسلا"], "Wa": "جون لوجي بيرد"},
]
# متغيرات اللعبة
game_sessions = {}
owner_id = l313l.uid

# نصوص اللعبة
GAME_TEXT = """ ‹ : لعبة من سيربح المليون .

• أهلاً بك في اللعبة!
• سوف يظهر لك سؤال و 3 خيارات
• اختر الإجابة الصحيحة للفوز

• **المستوى:** {level}/{total}
• **النتيجة:** {score} ✔️
• **الوسائل المساعدة:** {help_used}/2

﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎
**• اختر إجابتك من الأزرار أدناه:**"""

WIN_TEXT = """**🎉 فوز! 🎉**

• إجابتك صحيحة ✓
• انتقلت إلى المستوى التالي

• **المستوى:** {level}/{total}
• **النتيجة:** {score} ✔️
• **الوسائل المساعدة:** {help_used}/2"""

LOSE_TEXT = """**❌ خسارة! ❌**

• إجابتك خاطئة ✗
• الإجابة الصحيحة هي: **{correct}**

• **المستوى:** {level}/{total}
• **النتيجة:** {score} ✔️"""

END_TEXT = """**🏆 انتهت اللعبة! 🏆**

• **النتيجة النهائية:** {score}/{total}
• **النسبة المئوية:** {percent}%

﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎
• شكراً للعب! 🎉"""

# =========================================================== #
# أمر المليون
# =========================================================== #

@l313l.ar_cmd(pattern="المليون$")
async def million_game_cmd(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()

    try:
        await event.get_sender()
        await event.get_chat()
    except Exception as e:
        pass

    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "المليون")
    await response[0].click(event.chat_id)
    await event.delete()

# =========================================================== #
# الاستعلام المضمن للعبة
# =========================================================== #

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    @check_owner
    async def million_inline_handler(event):
        query = event.text
        
        if query.startswith("المليون"):
            buttons = [
                [Button.inline("🎮 ابدأ اللعبة", data="ready_to_start", style="success")],
                [Button.inline("❌ إلغاء", data="cancel_game", style="danger")]
            ]
            
            await event.answer(
                [await event.builder.article(
                    title="🎮 لعبة من سيربح المليون",
                    description="اضغط لبدء اللعبة",
                    text="**🎮 لعبة من سيربح المليون 🎮**\n\n• اضغط على زر 'ابدأ اللعبة' للبدء",
                    buttons=buttons,
                    link_preview=False,
                )],
                cache_time=0
            )

# =========================================================== #
# دوال اللعبة
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"ready_to_start")))
async def ready_to_start(event):
    """عند الضغط على زر بدء اللعبة"""
    user_id = event.query.user_id
    
    all_questions = QUESTIONS.copy()
    random.shuffle(all_questions)
    
    game_sessions[user_id] = {
        "questions": all_questions,
        "current": 0,
        "score": 0,
        "total": len(all_questions),
        "help_used": 0,
        "skip_used": False,
        "fifty_used": False,
        "message_id": event.message_id,
        "chat_id": event.chat_id,
        "current_choices": None
    }
    
    await send_question(event, user_id)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"answer_(\\d+)_(\\d+)_(\\d+)")))
async def handle_answer(event):
    match = re.match(r"answer_(\d+)_(\d+)_(\d+)", event.data.decode())
    if not match:
        return
    
    user_id = int(match.group(1))
    question_index = int(match.group(2))
    choice_index = int(match.group(3))
    
    if event.query.user_id != user_id:
        await event.answer("⚠️ هذه اللعبة ليست لك!", alert=True)
        return
    
    session = game_sessions.get(user_id)
    if not session:
        await event.edit("❌ انتهت الجلسة! ابدأ لعبة جديدة")
        return
    
    if session["current"] != question_index:
        await event.answer("⏳ هذا السؤال قديم!", alert=True)
        return
    
    question = session["questions"][question_index]
    
    current_choices = session.get("current_choices")
    if current_choices:
        selected_choice = current_choices[choice_index]
    else:
        selected_choice = question["choices"][choice_index]
    
    if selected_choice == question["Wa"]:
        session["score"] += 1
        session["current"] += 1
        session["current_choices"] = None
        
        current = session["current"]
        total = session["total"]
        score = session["score"]
        help_used = session["help_used"]
        
        if current >= total:
            percent = int(score / total * 100)
            await event.edit(
                END_TEXT.format(score=score, total=total, percent=percent),
                buttons=[[Button.inline("🔄 العب مرة أخرى", data=f"restart_game_{user_id}", style="primary")]],
                parse_mode="Markdown"
            )
            del game_sessions[user_id]
        else:
            await event.edit(
                WIN_TEXT.format(level=current+1, total=total, score=score, help_used=help_used),
                buttons=[[Button.inline("‹ : ➡️ التَالـي : ›", data=f"next_question_{user_id}", style="primary")]],
                parse_mode="Markdown"
            )
    else:
        current = session["current"]
        total = session["total"]
        score = session["score"]
        
        await event.edit(
            LOSE_TEXT.format(correct=question["Wa"], level=current+1, total=total, score=score),
            buttons=[
                [Button.inline("🔄 العب مرة أخرى", data=f"restart_game_{user_id}", style="primary")],
                [Button.inline("‹ : ❌ إنهاء اللعبـة : ›", data=f"force_end_game_{user_id}", style="danger")]
            ],
            parse_mode="Markdown"
        )
        del game_sessions[user_id]

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"fifty_fifty_(\\d+)_(\\d+)")))
async def fifty_fifty_handler(event):
    match = re.match(r"fifty_fifty_(\d+)_(\d+)", event.data.decode())
    if not match:
        return
    
    user_id = int(match.group(1))
    question_index = int(match.group(2))
    
    if event.query.user_id != user_id:
        await event.answer("⚠️ هذه اللعبة ليست لك!", alert=True)
        return
    
    session = game_sessions.get(user_id)
    if not session:
        await event.answer("❌ انتهت الجلسة!", alert=True)
        return
    
    if session["help_used"] >= 2:
        await event.answer("❌ لقد استنفذت جميع وسائل المساعدة!", alert=True)
        return
    
    if session["fifty_used"]:
        await event.answer("❌ لقد استخدمت هذه المساعدة بالفعل!", alert=True)
        return
    
    if session["current"] != question_index:
        await event.answer("⏳ هذا السؤال قديم!", alert=True)
        return
    
    question = session["questions"][question_index]
    correct = question["Wa"]
    wrong_choices = [c for c in question["choices"] if c != correct]
    random.shuffle(wrong_choices)
    
    remaining = [correct, wrong_choices[0]]
    random.shuffle(remaining)
    
    session["current_choices"] = remaining
    session["fifty_used"] = True
    session["help_used"] += 1
    
    await send_question(event, user_id)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"skip_question_(\\d+)_(\\d+)")))
async def skip_question_handler(event):
    match = re.match(r"skip_question_(\d+)_(\d+)", event.data.decode())
    if not match:
        return
    
    user_id = int(match.group(1))
    question_index = int(match.group(2))
    
    if event.query.user_id != user_id:
        await event.answer("⚠️ هذه اللعبة ليست لك!", alert=True)
        return
    
    session = game_sessions.get(user_id)
    if not session:
        await event.answer("❌ انتهت الجلسة!", alert=True)
        return
    
    if session["help_used"] >= 2:
        await event.answer("❌ لقد استنفذت جميع وسائل المساعدة!", alert=True)
        return
    
    if session["skip_used"]:
        await event.answer("❌ لقد استخدمت هذه المساعدة بالفعل!", alert=True)
        return
    
    if session["current"] != question_index:
        await event.answer("⏳ هذا السؤال قديم!", alert=True)
        return
    
    session["score"] += 1
    session["current"] += 1
    session["skip_used"] = True
    session["help_used"] += 1
    session["current_choices"] = None
    
    current = session["current"]
    total = session["total"]
    score = session["score"]
    help_used = session["help_used"]
    
    if current >= total:
        percent = int(score / total * 100)
        await event.edit(
            END_TEXT.format(score=score, total=total, percent=percent),
            buttons=[[Button.inline("🔄 العب مرة أخرى", data=f"restart_game_{user_id}", style="primary")]],
            parse_mode="Markdown"
        )
        del game_sessions[user_id]
    else:
        await event.edit(
            WIN_TEXT.format(level=current+1, total=total, score=score, help_used=help_used),
            buttons=[[Button.inline("‹ : ➡️ التَالـي : ›", data=f"next_question_{user_id}", style="primary")]],
            parse_mode="Markdown"
        )

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"cancel_game")))
async def cancel_game(event):
    user_id = event.query.user_id
    
    # فقط المطور يمكنه إلغاء اللعبة
    if user_id != owner_id:
        await event.answer("⚠️ فقط المطور يمكنه إلغاء اللعبة!", alert=True)
        return
    
    if user_id in game_sessions:
        del game_sessions[user_id]
    
    await event.edit("❌ تم إلغاء اللعبة!", buttons=None, parse_mode="Markdown")
    
@l313l.tgbot.on(CallbackQuery(data=re.compile(b"next_question_(\\d+)")))
async def next_question(event):
    match = re.match(r"next_question_(\d+)", event.data.decode())
    if not match:
        return
    
    user_id = int(match.group(1))
    
    if event.query.user_id != user_id:
        await event.answer("⚠️ هذه اللعبة ليست لك!", alert=True)
        return
    
    session = game_sessions.get(user_id)
    if not session:
        await event.edit("❌ انتهت الجلسة! ابدأ لعبة جديدة")
        return
    
    await send_question(event, user_id)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"restart_game_(\\d+)")))
async def restart_game(event):
    match = re.match(r"restart_game_(\d+)", event.data.decode())
    if not match:
        return
    
    user_id = int(match.group(1))
    
    if event.query.user_id != user_id:
        await event.answer("⚠️ هذه اللعبة ليست لك!", alert=True)
        return
    
    all_questions = QUESTIONS.copy()
    random.shuffle(all_questions)
    
    game_sessions[user_id] = {
        "questions": all_questions,
        "current": 0,
        "score": 0,
        "total": len(all_questions),
        "help_used": 0,
        "skip_used": False,
        "fifty_used": False,
        "message_id": event.message_id,
        "chat_id": event.chat_id,
        "current_choices": None
    }
    
    await send_question(event, user_id)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"force_end_game_(\\d+)")))
async def force_end_game(event):
    match = re.match(r"force_end_game_(\d+)", event.data.decode())
    if not match:
        return
    
    user_id = int(match.group(1))
    current_user = event.query.user_id
    
    # اللاعب ينهي لعبته الخاصة أو المطور ينهي أي لعبة
    if current_user != user_id and current_user != owner_id:
        await event.answer("⚠️ هذه اللعبة ليست لك ولا يمكنك إنهائها!", alert=True)
        return
    
    if user_id in game_sessions:
        del game_sessions[user_id]
    
    await event.edit("❌ تم إلغاء اللعبة!", buttons=None, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"cancel_game")))
async def cancel_game(event):
    user_id = event.query.user_id
    
    session = game_sessions.get(user_id)
    if session and session.get("chat_id") == event.chat_id:
        del game_sessions[user_id]
        await event.edit("❌ تم إلغاء اللعبة!", buttons=None, parse_mode="Markdown")
    else:
        await event.answer("⚠️ هذه اللعبة ليست لك!", alert=True)

async def send_question(event, user_id):
    """إرسال السؤال الحالي"""
    session = game_sessions.get(user_id)
    if not session:
        return
    
    current = session["current"]
    questions = session["questions"]
    total = session["total"]
    score = session["score"]
    help_used = session["help_used"]
    
    question = questions[current]
    
    if session.get("current_choices"):
        choices = session["current_choices"]
    else:
        choices = question["choices"]
    
    buttons_row = []
    for i, choice in enumerate(choices):
        emoji = ["❶", "❷", "❸"][i]
        buttons_row.append(Button.inline(f"{emoji} {choice}", data=f"answer_{user_id}_{current}_{i}", style="primary"))
    
    buttons = [buttons_row]
    
    help_buttons = []
    if not session["skip_used"] and help_used < 2:
        help_buttons.append(Button.inline("‹ : تَخطـي : ›", data=f"skip_question_{user_id}_{current}", style="success"))
    if not session["fifty_used"] and help_used < 2:
        help_buttons.append(Button.inline("‹ : حذف أجابـة : ›", data=f"fifty_fifty_{user_id}_{current}", style="success"))
    
    if help_buttons:
        buttons.append(help_buttons)
    
    buttons.append([Button.inline("‹ : ❌ إنهاء اللعبـة : ›", data=f"force_end_game_{user_id}", style="danger")])
    
    text = f"**❓ {question['aW']}**\n\n"
    text += f"• **المستوى:** {current + 1}/{total}\n"
    text += f"• **النتيجة:** {score} ✔️\n"
    text += f"• **الوسائل المساعدة:** {help_used}/2\n\n"
    text += f"• اختر إجابتك من الأزرار أدناه:"
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")
