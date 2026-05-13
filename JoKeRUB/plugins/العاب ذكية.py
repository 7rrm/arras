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



import asyncio
import random
from datetime import datetime
from telethon import events
from telethon.tl.types import InputMediaDice
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from ..core.managers import edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import l313l
from telethon.tl import types


points = {}
is_game_started = False
is_word_sent = False
word = ''

async def get_bot_entity():
    return await l313l.get_entity('me')
    


@l313l.ar_cmd(pattern="اسرع")
async def handle_start(event):
    global is_game_started, is_word_sent, word, bot_entity
    is_game_started = True
    is_word_sent = False
    word = event.text.split(maxsplit=1)[1]
    chat_id = event.chat_id
    await event.edit(f"**اول من يكتب ( {word} ) سيفوز**")

@l313l.on(events.NewMessage(incoming=True))
async def handle_winner(event):
    global is_game_started, is_word_sent, winner_id, word, points
    if is_game_started and not is_word_sent and word.lower() in event.raw_text.lower():
        if event.chat_id:
            bot_entity = await get_bot_entity()
            if bot_entity and event.sender_id != bot_entity.id:
                is_word_sent = True
                winner_id = event.sender_id
                if winner_id not in points:
                    points[winner_id] = 0
                points[winner_id] += 1
                sender = await event.get_sender()
                sender_first_name = sender.first_name if sender else 'مجهول'
                sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
                points_text = '\n'.join([f'{i+1}• {(await l313l.get_entity(participant_id)).first_name}: {participant_points}' for i, (participant_id, participant_points) in enumerate(sorted_points)])
                await l313l.send_message(event.chat_id, f'الف مبرووووك 🎉 الاعب ( {sender_first_name} ) فاز! \n اصبحت نقاطة: {points[winner_id]}\nنقاط المشاركين:\n{points_text}')


import random
from telethon import events

joker = [
    "تلعب وخوش تلعب 👏🏻",
    "لكَ عاش يابطل أستمر 💪🏻",
    "على كيفك ركزززز أنتَ كدها 🤨",
    "لك وعلي ذيييب 😍",
]

correct_answer = None
game_board = [["👊"] * 6]
numbers_board = [["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]]
original_game_board = [["👊"] * 6]
group_game_status = {}
points = {}

# تعريف المعرفات - يجب تعديل هذا حسب معرفات المستخدمين الفعلية
MY_UID = l313l.uid  # ضع معرف حسابك هنا
OTHER_USER = 6373993992 #الآخر
ALLOWED_USERS = [MY_UID, OTHER_USER]  # المستخدمون المسموح لهم ببدء اللعبة

def count_closed_hands(board):
    """تحسب عدد الأيدي المغلقة (👊)"""
    return board[0].count("👊")

async def handle_clue(event):
    global correct_answer, group_game_status
    chat_id = event.chat_id
    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'is_game_started': False, 'joker_player': None}
    
    if not group_game_status[chat_id]['is_game_started']:
        group_game_status[chat_id]['is_game_started'] = True
        group_game_status[chat_id]['joker_player'] = None
        correct_answer = random.randint(1, 6)
        await event.reply("**أول مـن سَيرسݪ ڪلمه ( `انا` ) سَيشارك فيِ لـعَبة محيبس**")

@l313l.on(events.NewMessage(pattern=r'^محيبس$'))
async def start_game(event):
    if event.sender_id not in ALLOWED_USERS:
        return
    
    chat_id = event.chat_id
    if chat_id in group_game_status:
        group_game_status[chat_id]['is_game_started'] = False
    await handle_clue(event)

@l313l.on(events.NewMessage(pattern=r'طك (\d+)'))
async def handle_strike(event):
    global group_game_status, correct_answer, game_board
    chat_id = event.chat_id
    
    # التحقق من أن اللعبة بدأت وأن اللاعب هو المشارك
    if chat_id not in group_game_status or not group_game_status[chat_id]['is_game_started'] or event.sender_id != group_game_status[chat_id]['joker_player']:
        return
    
    # التحقق: إذا تبقى عضمتين فقط، لا يسمح باستخدام طك
    closed_hands = count_closed_hands(game_board)
    if closed_hands <= 2:
        await event.reply(f"**👤 عَزيزي أستخدم أمر جيب <رقم> لأنك وصلت لأخر عظمتين .**\n{format_board(game_board, numbers_board)}")
        return
    
    strike_position = int(event.pattern_match.group(1))
    
    # التحقق من أن الرقم المدخل سليم
    if strike_position < 1 or strike_position > 6:
        await event.reply("**❌ الرجاء إدخال رقم بين 1 و 6**")
        return
    
    # التحقق من أن اليد لم تفتح من قبل
    if game_board[0][strike_position - 1] != "👊":
        await event.reply("**❌ هذه اليد مفتوحة بالفعل، اختر يد أخرى**")
        return
    
    if strike_position == correct_answer:
        # إذا ضرب اليد التي فيها المحبس يخسر
        game_board = [["💍" if i == correct_answer - 1 else "🖐️" for i in range(6)]]
        await event.reply(f"**خَسرت عَزيزي ليش مستعجل !\n{format_board(game_board, numbers_board)}**")
        reset_game(chat_id)
    else:
        # فتح اليد
        game_board[0][strike_position - 1] = '🖐️'
        
        # بعد فتح اليد، تحقق إذا تبقى عضمتين فقط
        closed_hands = count_closed_hands(game_board)
        if closed_hands == 2:
            await event.reply(f"**- تبقى عضمتين فقط! الآن يجب استخدام أمر جيب <رقم> للبحث عن المحبس**\n{format_board(game_board, numbers_board)}")
        else:
            await event.reply(f"**{random.choice(joker)}**\n{format_board(game_board, numbers_board)}")

@l313l.on(events.NewMessage(pattern=r'جيب (\d+)'))
async def handle_guess(event):
    global group_game_status, correct_answer, game_board, points
    chat_id = event.chat_id
    
    # التحقق من أن اللعبة بدأت وأن اللاعب هو المشارك
    if chat_id not in group_game_status or not group_game_status[chat_id]['is_game_started'] or event.sender_id != group_game_status[chat_id]['joker_player']:
        return
    
    guess = int(event.pattern_match.group(1))
    
    # التحقق من أن الرقم المدخل سليم
    if guess < 1 or guess > 6:
        await event.reply("**❌ الرجاء إدخال رقم بين 1 و 6**")
        return
    
    # التحقق من أن اليد لم تفتح من قبل
    if game_board[0][guess - 1] != "👊":
        await event.reply("**❌ هَذه اليد مفتوحةة بالفعل، لأ يُمكنك أسَتخدام الأمر عَليها .**")
        return
    
    if guess == correct_answer:
        # فاز اللاعب
        winner_id = event.sender_id
        points[winner_id] = points.get(winner_id, 0) + 1
        sender = await event.get_sender()
        sender_first_name = sender.first_name if sender else 'مجهول'
        
        # ترتيب النقاط
        sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
        points_text = ""
        for i, (participant_id, participant_points) in enumerate(sorted_points):
            try:
                participant = await l313l.get_entity(participant_id)
                participant_name = participant.first_name if participant else 'مجهول'
                points_text += f'{i+1}• {participant_name}: {participant_points}\n'
            except:
                points_text += f'{i+1}• مجهول: {participant_points}\n'
        
        # عرض النتيجة
        game_board = [["💍" if i == correct_answer - 1 else "🖐️" for i in range(6)]]
        result_message = f'🎉 الف مبروووك! الاعب ( {sender_first_name} ) وجد المحبس 💍!\n{format_board(game_board, numbers_board)}\n\n'
        result_message += f'🏆 نقاط الاعب: {points[winner_id]}\n'
        result_message += f'📊 ترتيب المشاركين:\n{points_text}'
        
        await event.reply(result_message)
        reset_game(chat_id)
    else:
        # خسر اللاعب (اختار يد خطأ)
        game_board = [["💍" if i == correct_answer - 1 else "🖐️" for i in range(6)]]
        await event.reply(f"**😔 ضاع البات ماضن بعد تلگونة ☹️\n{format_board(game_board, numbers_board)}**")
        reset_game(chat_id)

@l313l.on(events.NewMessage(pattern=r'انا'))
async def handle_incoming_message(event):
    global group_game_status
    chat_id = event.chat_id
    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'is_game_started': False, 'joker_player': None}
    
    if group_game_status[chat_id]['is_game_started'] and not group_game_status[chat_id]['joker_player']:
        group_game_status[chat_id]['joker_player'] = event.sender_id
        await event.reply(f"**تم تسجيلك في المسابقة ، 💬 أرسل طك <رقم> لفتح يد، أو جيب <رقم> لمحاولة كشف المحبس!**\n{format_board(game_board, numbers_board)}")

def format_board(game_board, numbers_board):
    """تنسيق لوحة اللعب بالشكل المطلوب"""
    return f"\n•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n{' '.join(numbers_board[0])}\n{' '.join(game_board[0])}"

def reset_game(chat_id):
    global game_board, group_game_status
    game_board = [row[:] for row in original_game_board]
    group_game_status[chat_id]['is_game_started'] = False
    group_game_status[chat_id]['joker_player'] = None

@l313l.ar_cmd(pattern="تصفير")
async def reset_points(event):
    global points
    points = {}
    await event.edit('**تم تصفير نقاط المشاركين بنجاح!**')


@l313l.ar_cmd(pattern="احكام(?: |$)(.*)")
async def zed(event): # Code by t.me/zzzzl1l
    user = await event.get_sender()
    zed_chat = event.chat_id
    if gvarstatus("Z_AKM") is None:
        delgvar("Z_EKB")
        delgvar("Z_AK")
        delgvar("Z_A2K")
        delgvar("Z_A3K")
        delgvar("Z_A4K")
        delgvar("Z_A5K")
        delgvar("A_CHAT")
        addgvar("Z_AKM", "true")
        addgvar("Z_AK", user.id)  # إضافة الشخص الذي يرسل .احكام كأول لاعب
        addgvar("A_CHAT", zed_chat)
        return await edit_or_reply(event, f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم بـدء اللعبـة وتـم إنضمـامي**  [{user.first_name}](tg://user?id={user.id})  **بنجـاح ☑️**\n\n**- اللي بيلعـب يرسل**  `.انا`", link_preview=False)
    else:
        delgvar("Z_EKB")
        delgvar("Z_AK")
        delgvar("Z_A2K")
        delgvar("Z_A3K")
        delgvar("Z_A4K")
        delgvar("Z_A5K")
        delgvar("Z_AKM")
        delgvar("A_CHAT")
        addgvar("Z_AKM", "true")
        addgvar("Z_AK", user.id)  # إعادة تعيين اللاعب الأول
        addgvar("A_CHAT", zed_chat)
        return await edit_or_reply(event, f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم بـدء اللعبـة وتـم إنضمـامي**  [{user.first_name}](tg://user?id={user.id})  **بنجـاح ☑️**\n\n**- اللي بيلعـب يرسل**  `.انا`", link_preview=False)


@l313l.on(events.NewMessage(pattern=".انا"))
async def _(event): # Code by t.me/zzzzl1l
    user = await event.get_sender()
    if gvarstatus("Z_AKM") is not None and event.chat_id == int(gvarstatus("A_CHAT")):
        # التحقق مما إذا كان المستخدم منضمًا مسبقًا
        is_joined = False
        for var in ["Z_AK", "Z_A2K", "Z_A3K", "Z_A4K", "Z_A5K"]:
            var_value = gvarstatus(var)
            if var_value is not None and user.id == int(var_value):
                is_joined = True
                break
        
        if is_joined:
            return await event.reply("- عَزيزي ، أنت منضم سابقًا .")  # رسالة الانضمام المسبق
        
        # إذا لم يكن منضمًا مسبقًا
        if gvarstatus("Z_A2K") is None:
            addgvar("Z_A2K", user.id)
            return await event.reply(f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم انضمـام**   [{user.first_name}](tg://user?id={user.id})  ** ☑️**\n\n**- اصبح عـدد اللاعبيـن 2⃣**\n**- على صاحب اللعبـة ان يرسـل**  `.تم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_A3K") is None:
            addgvar("Z_A3K", user.id)
            return await event.reply(f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم انضمـام**   [{user.first_name}](tg://user?id={user.id})  ** ☑️**\n\n**- اصبح عـدد اللاعبيـن 3⃣**\n**- على صاحب اللعبـة ان يرسـل**  `.تم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_A4K") is None:
            addgvar("Z_A4K", user.id)
            return await event.reply(f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم انضمـام**   [{user.first_name}](tg://user?id={user.id})  ** ☑️**\n\n**- اصبح عـدد اللاعبيـن 4⃣**\n**- على صاحب اللعبـة ان يرسـل**  `.تم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_A5K") is None:
            addgvar("Z_A5K", user.id)
            return await event.reply(f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم انضمـام**   [{user.first_name}](tg://user?id={user.id})  ** ☑️**\n\n**- اصبح عـدد اللاعبيـن 5⃣**\n**- على صاحب اللعبـة ان يرسـل**  `.تم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        else:
            return await event.reply(f"**- عـذراً عـزيـزي**   [{user.first_name}](tg://user?id={user.id})  \n\n**- لقـد اكتمـل عـدد اللاعبيــن . . انتظـر بـدء اللعبـة من جديـد**", link_preview=False)


@l313l.ar_cmd(pattern="تم(?: |$)(.*)")
async def zed(event): 
    ZZZZ = gvarstatus("Z_AKM")
    AKM = gvarstatus("Z_AK")
    AK2M = gvarstatus("Z_A2K")
    AK3M = gvarstatus("Z_A3K")
    AK4M = gvarstatus("Z_A4K")
    AK5M = gvarstatus("Z_A5K")
# Code by t.me/zzzzl1l
    zana2 = [f"{AKM}", f"{AK2M}"]
    zaza2 = [x for x in zana2 if x is not None]
    zana3 = [f"{AKM}", f"{AK2M}", f"{AK3M}"]
    zaza3 = [x for x in zana3 if x is not None]
    zana4 = [f"{AKM}", f"{AK2M}", f"{AK3M}", f"{AK4M}"]
    zaza4 = [x for x in zana4 if x is not None]
    zana5 = [f"{AKM}", f"{AK2M}", f"{AK5M}", f"{AK3M}", f"{AK4M}"]
    zaza5 = [x for x in zana5 if x is not None]
# Code by t.me/zzzzl1l
    zed2 = random.choice(zana2)
    zee2 = random.choice([x for x in zaza2 if x != zed2])
    zed3 = random.choice(zana3)
    zee3 = random.choice([x for x in zaza3 if x != zed3])
    zed4 = random.choice(zana4)
    zee4 = random.choice([x for x in zaza4 if x != zed4])
    zed5 = random.choice(zana5)
    zee5 = random.choice([x for x in zaza5 if x != zed5])
    if gvarstatus("Z_AKM") is None:
        return await edit_or_reply(event, "**- انت لم تبـدأ اللعبـه بعـد ؟!\n- لـ بـدء لعبـة جديـدة ارسـل** `.احكام`")
    if gvarstatus("Z_AK") is None:
        return
    if gvarstatus("Z_AK") is not None and gvarstatus("Z_A2K") is not None and gvarstatus("Z_A3K") is None and gvarstatus("Z_A4K") is None and gvarstatus("Z_A5K") is None:
       
        zelzal = int(zed2)
        zilzal = int(zee2)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
        except ValueError:
            return
        name_zed = user_zed.first_name
        name_zee = user_zee.first_name
        await edit_or_reply(event, f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تـم اختيـار المتهـم ⇠**  [{name_zed}](tg://user?id={zed2})  \n**- ليتـم الحكـم عليـه ⇠ ⚖**\n**- الحاكـم 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee2}) ", link_preview=False)
        delgvar("Z_AKM")
        return
    if gvarstatus("Z_AK") is not None and gvarstatus("Z_A2K") is not None and gvarstatus("Z_A3K") is not None and gvarstatus("Z_A4K") is None and gvarstatus("Z_A5K") is None:
        zelzal = int(zed3)
        zilzal = int(zee3)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
        except ValueError:
            return
        name_zed = user_zed.first_name
        name_zee = user_zee.first_name
        await edit_or_reply(event, f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تـم اختيـار المتهـم ⇠**  [{name_zed}](tg://user?id={zed3})  \n**- ليتـم الحكـم عليـه ⇠ ⚖**\n**- الحاكـم 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee3}) ", link_preview=False)
        delgvar("Z_AKM")
        return
    if gvarstatus("Z_AK") is not None and gvarstatus("Z_A2K") is not None and gvarstatus("Z_A3K") is not None and gvarstatus("Z_A4K") is not None and gvarstatus("Z_A5K") is None:
        zelzal = int(zed4)
        zilzal = int(zee4)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
        except ValueError:
            return
        name_zed = user_zed.first_name
        name_zee = user_zee.first_name
        await edit_or_reply(event, f"[ᯓ ᥲRRᥲS Gᥲmᗴ - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تـم اختيـار المتهـم ⇠**  [{name_zed}](tg://user?id={zed4})  \n**- ليتـم الحكـم عليـه ⇠ ⚖**\n**- الحاكـم 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee4}) ", link_preview=False)
        delgvar("Z_AKM")
        return
    if gvarstatus("Z_AK") is not None and gvarstatus("Z_A2K") is not None and gvarstatus("Z_A3K") is not None and gvarstatus("Z_A4K") is not None and gvarstatus("Z_A5K") is not None:
        zelzal = int(zed5)
        zilzal = int(zee5)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
        except ValueError:
            return
        name_zed = user_zed.first_name
        name_zee = user_zee.first_name
        await edit_or_reply(event, f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تـم اختيـار المتهـم ⇠**  [{name_zed}](tg://user?id={zed5})  \n**- ليتـم الحكـم عليـه ⇠ ⚖**\n**- الحاكـم 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee5}) ", link_preview=False)
        delgvar("Z_AKM")
        return


'''

from telethon import events
from telethon.tl.types import InputMediaDice
from . import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

# قاموس لحفظ نتائج اللاعبين
games = {}

@l313l.on(events.NewMessage(pattern='.نرد'))
async def start_game(event):
    """
    تبدأ اللعبة عند إرسال .لعبة النرد
    """
    user = await event.get_sender()
    if user.id != l313l.uid:
        return
    global games
    chat_id = event.chat_id
    games[chat_id] = {
        "players": {} 
    }
    if gvarstatus("dice_game"):
        delgvar("dice_game")
    if gvarstatus("name_game"):
        delgvar("name_game")
    addgvar("name_game", "🎲 لعبـة رمـي النـرد")
    addgvar("dice_game", True)
    await event.reply("[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 🎲 لعبـة رمـي النـرد](t.me/ZThon)\n⋆─┄─┄─┄─┄─┄─┄─┄─⋆\n**- تم بـدء لعبـة رمـي النـرد .. بنجـاح ☑️\n- اللي بيلعـب يضغـط ع النـرد بالاسفـل **", link_preview=False)
    await event.delete()
    emoticon = "🎲"
    r = await event.reply(file=InputMediaDice(emoticon=emoticon))

@l313l.on(events.NewMessage())
async def handle_dice(event):
    """
    يتفاعل مع رمي النرد في الدردشة التي بدأت فيها لعبة.
    """
    global games
    chat_id = event.chat_id
    # التحقق من وجود لعبة في هذه الدردشة 
    if chat_id in games:
        sender = await event.get_sender()
        user_id = sender.id
        sender_name = f"{sender.first_name} {sender.last_name}" if sender.last_name else sender.first_name
        # للتأكد من أن الرسالة تحتوي على رمي نرد 
        if event.dice and event.dice.emoticon == '🎲':
            if gvarstatus("dice_game") is None:
                return
            dice_value = event.dice.value
            # حفظ نتيجة اللاعب 
            if user_id not in games[chat_id]["players"]:
                games[chat_id]["players"][user_id] = 0
                games[chat_id]["players"][user_id] += dice_value
                if dice_value == 1:
                    dice_value = "❶"
                elif dice_value == 2:
                    dice_value = "❷"
                elif dice_value == 3:
                    dice_value = "❸"
                elif dice_value == 4:
                    dice_value = "❹"
                elif dice_value == 5:
                    dice_value = "❺"
                elif dice_value == 6:
                    dice_value = "❻"
                else:
                    pass
                await event.reply(f"**• اللاعب ⇐**  {sender_name}\n**• رمى النرد وحصل على ⇐ ** {dice_value} **نقاط**\n\n**• انتظـر لـ حتى يتم إنهاء اللعبـه واختيار الفائـز**\n**• لـ إنهـاء اللعبـه ارسـل الامـر** ( `.النتيجه` )")
            else:
                await event.delete()

@l313l.on(events.NewMessage(pattern='.النتيجه'))
async def end_game(event):
    """
    ينهي اللعبة الحالية في الدردشة ويعرض النتائج.
    """
    user = await event.get_sender()
    if user.id != l313l.uid:
        return
    if gvarstatus("dice_game") is None:
        return
    global games
    chat_id = event.chat_id

    # التحقق من وجود لعبة في هذه الدردشة
    if chat_id in games:
        if not games[chat_id]["players"]:
            await event.reply("**- لم يشارك أحد في اللعبة بعد.**")
            return

        # إيجاد أعلى نتيجة 
        max_score = max(games[chat_id]["players"].values())

        # إيجاد جميع الفائزين (الذين حصلوا على أعلى نتيجة)
        winners = [user_id for user_id, score in games[chat_id]["players"].items() if score == max_score]

        # بناء رسالة النتائج 
        name_game = gvarstatus("name_game") if gvarstatus("name_game") else "🎲 لعبـة رمـي النـرد"
        results_message = f"ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 {name_game}\n⋆─┄─┄─┄─┄─┄─┄─┄─⋆\n"
        for user_id, score in games[chat_id]["players"].items():
            user_entity = (await l313l.get_entity(user_id))
            user_name = f"{user_entity.first_name} {user_entity.last_name}" if user_entity.last_name else user_entity.first_name
            if score == 1:
                score = "❶"
            elif score == 2:
                score = "❷"
            elif score == 3:
                score = "❸"
            elif score == 4:
                score = "❹"
            elif score == 5:
                score = "❺"
            elif score == 6:
                score = "❻"
            else:
                pass
            results_message += f"**• اللاعب ⇐**  {user_name} | **عـدد النقـاط ⇐** {score}\n"

        # إضافة أسماء الفائزين 
        if len(winners) == 1:
            winner_entity = (await l313l.get_entity(winners[0]))
            winner_name = f"{winner_entity.first_name} {winner_entity.last_name}" if winner_entity.last_name else winner_entity.first_name
            if max_score == 1:
                max_score = "❶"
            elif max_score == 2:
                max_score = "❷"
            elif max_score == 3:
                max_score = "❸"
            elif max_score == 4:
                max_score = "❹"
            elif max_score == 5:
                max_score = "❺"
            elif max_score == 6:
                max_score = "❻"
            else:
                pass
            results_message += f"\n\n**• الفـائـز هـو ⇐** {winner_name} | **بمجمـوع نقـاط ⇐** {max_score} 🏆"
        else:
            results_message += f"\n\n**• الفائـزيـن هـم:** "
            for winner_id in winners:
                winner_entity = (await l313l.get_entity(winner_id))
                winner_name = f"**• الفائـز ⇐** {winner_entity.first_name} {winner_entity.last_name}" if winner_entity.last_name else winner_entity.first_name
                results_message += f"\n{winner_name}"
            if max_score == 1:
                max_score = "❶"
            elif max_score == 2:
                max_score = "❷"
            elif max_score == 3:
                max_score = "❸"
            elif max_score == 4:
                max_score = "❹"
            elif max_score == 5:
                max_score = "❺"
            elif max_score == 6:
                max_score = "❻"
            else:
                pass
            results_message += f"\n**• نقـاط الفائـزيـن ⇐** {max_score} **نقطـه** 🏆"

        # إزالة اللعبة من القائمة بعد نهايتها
        del games[chat_id]
        delgvar("dice_game")
        delgvar("name_game")
        await event.reply(results_message, link_preview=False)
        await event.delete()
    else:
        await event.reply("**- لا يوجد لعبة نرد في هذه الدردشة ❌**\n**- لـ بـدء لعبـة النرد 🎲**\n**- ارسـل الامـر** ( `.لعبة النرد` )")

ZelzalGM_cmd = (
"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 🎲 لعبـة رمـي النـرد](t.me/ZThon)\n"
"**⋆─┄─┄─┄─┄•┄─┄─┄─┄─⋆**\n"
"**⌖ لعبـة رمـي النـرد 🎲 الجديـدة اكثـر نقطـه 6 ⛳️**\n\n"
"**• الامـر ⇐**  `.لعبة النرد`\n"
"**⪼ لـ بـدء لعبـة رمـي النـرد 🎲**\n\n"
"**• الامـر ⇐**  `.النتيجه`\n"
"**⪼ لـ إنهـاء اللعبـه وعـرض النتائـج 🏆**\n"
)

@l313l.ar_cmd(pattern="العاب المشاركة")
async def game_info(event):
    await edit_or_reply(event, ZelzalGM_cmd, link_preview=False)


'''


##############################
#####

from telethon import events
from telethon.tl.types import InputMediaDice, Message
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from . import l313l
from telethon.extensions import html, markdown
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
import asyncio
import random

class CustomParseMode:
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'html':
            text, entities = html.parse(text)
            # معالجة إيموجيات البريميوم
            for i, e in enumerate(entities):
                if isinstance(e, types.MessageEntityTextUrl):
                    if e.url.startswith('emoji/'):
                        document_id = int(e.url.split('/')[1])
                        entities[i] = types.MessageEntityCustomEmoji(
                            offset=e.offset,
                            length=e.length,
                            document_id=document_id
                        )
            return text, entities
        elif self.parse_mode == 'markdown':
            return markdown.parse(text)
        raise ValueError("Unsupported parse mode")

    @staticmethod
    def unparse(text, entities):
        return html.unparse(text, entities)
        
# قاموس لحفظ بيانات اللعبة
dice_games = {}

class DiceGame:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.players = {}  # {user_id: {"name": "", "current_round_score": 0, "total_score": 0}}
        self.pinned_message_id = None
        self.game_message_id = None
        self.current_round = 1
        self.game_active = False
        self.waiting_for_dice = None  # {user_id: remaining_throws}
        self.eliminated_players = []
    
    async def create_pinned_message(self, event):
        """إنشاء الرسالة المثبتة"""
        message = await event.reply("**🎲 لعبـة النـرد الجديدة**\n\n**اللاعبون المشاركون:**\nٴ- لم ينضم أحد بعد\n\n**ارسل `Y` للانضمام!**")
        await event.client(UpdatePinnedMessageRequest(self.chat_id, message.id, False))
        self.pinned_message_id = message.id
        return message.id
    
    async def update_pinned_message(self, event):
        """تحديث الرسالة المثبتة"""
        if not self.pinned_message_id:
            return
        
        players_text = "**اللاعبون المشاركون:**\n"
        for user_id, data in self.players.items():
            if self.game_active:
                # في الجولة النشطة، نعرض نقاط الجولة الحالية
                score_display = data["current_round_score"]
            else:
                score_display = "لم يلعب بعد"
            players_text += f"ٴ👤 {data['name']} - النقاط: {score_display}\n"
        
        if self.eliminated_players:
            players_text += f"\n**المقصيون:**\n"
            for player in self.eliminated_players:
                players_text += f"ٴ❌ {player}\n"
        
        status = "**الحالة: جارية**" if self.game_active else "**الحالة: في انتظار اللاعبين**"
        message_text = f"**🎲 لعبـة النـرد**\n\n{players_text}\n{status}\n\n**الجولة: {self.current_round}**"
        
        try:
            await event.client.edit_message(self.chat_id, self.pinned_message_id, message_text)
        except:
            pass

    async def add_player(self, event, user):
        """إضافة لاعب جديد"""
        if user.id in self.players:
            return False
        
        user_name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        self.players[user.id] = {
            "name": user_name,
            "current_round_score": 0,  # نقاط الجولة الحالية فقط
            "total_score": 0,  # لم يعد مستخدمًا للإقصاء
            "dice_throws": []
        }
        
        await self.update_pinned_message(event)
        return True

    async def start_game(self, event):
        """بدء اللعبة"""
        if len(self.players) < 2:
            await event.reply("**❌ تحتاج إلى لاعبين على الأقل لبدء اللعبة!**")
            return False
        
        self.game_active = True
        await self.update_pinned_message(event)
        await self.start_round(event)
        return True

    async def start_round(self, event):
        """بدء جولة جديدة"""
        # تصفير نقاط الجولة الحالية للجميع
        for user_id in self.players:
            self.players[user_id]["current_round_score"] = 0
            self.players[user_id]["dice_throws"] = []
        
        # بدء من أول لاعب
        player_ids = list(self.players.keys())
        first_player = player_ids[0]
        self.waiting_for_dice = {"user_id": first_player, "remaining_throws": 3}
        
        user_entity = await event.client.get_entity(first_player)
        user_name = self.players[first_player]["name"]
        
        # ✅ لا يرد - رسالة جديدة فقط
        await event.respond(f"**⦑ الجولة {self.current_round} ⦒**\n\n- عَزيزي/تي ◗ [{user_name}](tg://user?id={first_player}) ◖\nتم بدء اللعبة إرسل 3 مرات نرد .")

    async def process_dice_throw(self, event, user_id, dice_value):
        """معالجة رمي النرد"""
        if not self.waiting_for_dice or self.waiting_for_dice["user_id"] != user_id:
            return False
        
        player = self.players[user_id]
        player["dice_throws"].append(dice_value)
        player["current_round_score"] += dice_value
        self.waiting_for_dice["remaining_throws"] -= 1
        
        if self.waiting_for_dice["remaining_throws"] > 0:
            remaining = self.waiting_for_dice["remaining_throws"]
            user_name = player["name"]
            # ✅ يرد - على رسالة النرد
            await event.reply(f"◈︙اللاعب - {user_name}\n - رمى النرد وحصل على {dice_value} نقطة.\n\n❨ باقي {remaining} رميات❩")
            return "continue"
        else:
            # انتهى دور اللاعب
            total_round_score = player["current_round_score"]
            user_name = player["name"]
            
            # ✅ لا يرد - رسالة جديدة فقط
            await event.respond(f"**🎲 اللاعب {user_name} انتهى من رمي النرد وحصل على {total_round_score} نقطة في هذه الجولة!**")
            
            # تحديث الرسالة المثبتة بعد انتهاء اللاعب
            await self.update_pinned_message(event)
            
            # الانتقال للاعب التالي
            await self.next_player(event)
            return "finished"

    async def next_player(self, event):
        """الانتقال للاعب التالي"""
        player_ids = list(self.players.keys())
        current_index = player_ids.index(self.waiting_for_dice["user_id"])
        
        if current_index + 1 < len(player_ids):
            next_player_id = player_ids[current_index + 1]
            self.waiting_for_dice = {"user_id": next_player_id, "remaining_throws": 3}
            
            user_name = self.players[next_player_id]["name"]
            # ✅ لا يرد - رسالة جديدة فقط
            await event.respond(f"**🎲 الدور الآن على:**\n\n- عَزيزي/تي ◗ [{user_name}](tg://user?id={next_player_id}) ◖\nإرسل 3 مرات نرد .")
        else:
            # انتهت الجولة
            await self.finish_round(event)

    async def finish_round(self, event):
        """إنهاء الجولة وتصفية اللاعبين"""
        self.waiting_for_dice = None
        
        # الإقصاء بناءً على نقاط الجولة الحالية فقط
        current_round_scores = {user_id: player["current_round_score"] for user_id, player in self.players.items()}
        min_score = min(current_round_scores.values())
        lowest_players = [user_id for user_id, score in current_round_scores.items() if score == min_score]
        
        if len(lowest_players) == 1:
            # إقصاء لاعب واحد
            eliminated_id = lowest_players[0]
            eliminated_name = self.players[eliminated_id]["name"]
            eliminated_score = self.players[eliminated_id]["current_round_score"]
            self.eliminated_players.append(eliminated_name)
            del self.players[eliminated_id]
            
            # ✅ لا يرد - رسالة جديدة فقط
            await event.respond(f"**🎲 تم إقصاء اللاعب ◗ `{eliminated_name}` ◖ لكونه الأقل نقاطاً في الجولة {self.current_round} ({eliminated_score} نقطة)**")
            
        else:
            # تعادل - جولة إضافية للمتعادلين فقط
            await self.handle_tie_breaker(event, lowest_players)
            return
        
        # التحقق إذا كانت اللعبة انتهت
        if len(self.players) == 1:
            await self.finish_game(event)
        else:
            # بدء جولة جديدة
            self.current_round += 1
            await self.update_pinned_message(event)
            await asyncio.sleep(3)
            await self.start_round(event)

    async def handle_tie_breaker(self, event, tied_players):
        """معالجة التعادل بين اللاعبين"""
        tied_names = [self.players[pid]["name"] for pid in tied_players]
        tied_scores = [self.players[pid]["current_round_score"] for pid in tied_players]
        names_text = " - ".join(tied_names)
        
        # ✅ لا يرد - رسالة جديدة فقط
        await event.respond(f"**🎲 تعادل في النقاط بين:**\n{names_text}\n\n**جميعهم حصلوا على {tied_scores[0]} نقطة**\n**سيلعبون جولة إضافية لتحديد المقصى!**")
        
        # حفظ اللاعبين المتعادلين مؤقتاً
        self.tied_players = tied_players
        self.tied_scores = {pid: 0 for pid in tied_players}
        
        # إعادة تعيين النقاط للجولة الإضافية
        for player_id in tied_players:
            self.players[player_id]["current_round_score"] = 0
            self.players[player_id]["dice_throws"] = []
        
        # تحديث الرسالة المثبتة للجولة الإضافية
        await self.update_pinned_message(event)
        
        # بدء الجولة الإضافية من أول لاعب متعادل
        first_tied_player = tied_players[0]
        self.waiting_for_dice = {"user_id": first_tied_player, "remaining_throws": 3, "tie_breaker": True}
        
        user_name = self.players[first_tied_player]["name"]
        # ✅ لا يرد - رسالة جديدة فقط
        await event.respond(f"**⦑ الجولة الإضافية ⦒**\n\n- عَزيزي/تي ◗ [{user_name}](tg://user?id={first_tied_player}) ◖\n- إرسل 3 مرات نرد .")

    async def process_tie_breaker_dice(self, event, user_id, dice_value):
        """معالجة رمي النرد في الجولة الإضافية"""
        player = self.players[user_id]
        player["dice_throws"].append(dice_value)
        player["current_round_score"] += dice_value
        self.tied_scores[user_id] = player["current_round_score"]
        self.waiting_for_dice["remaining_throws"] -= 1
        
        if self.waiting_for_dice["remaining_throws"] > 0:
            remaining = self.waiting_for_dice["remaining_throws"]
            user_name = player["name"]
            # ✅ يرد - على رسالة النرد
            await event.reply(f"◈︙اللاعب - `{user_name}`\n - رمى النرد وحصل على `{dice_value}` نقطة.\n\n❨ باقي `{remaining}` رميات❩")
        else:
            # انتهى دور اللاعب في الجولة الإضافية
            total_round_score = player["current_round_score"]
            user_name = player["name"]
            # ✅ لا يرد - رسالة جديدة فقط
            await event.respond(f"◈︙اللاعب - `{user_name}`\n انتهى من رمي النرد وحصل على `{total_round_score}` نقطة في الجولة الإضافية!")
            
            # تحديث الرسالة المثبتة بعد انتهاء اللاعب
            await self.update_pinned_message(event)
            
            # الانتقال للاعب التالي في الجولة الإضافية
            current_index = self.tied_players.index(user_id)
            if current_index + 1 < len(self.tied_players):
                next_player_id = self.tied_players[current_index + 1]
                self.waiting_for_dice = {"user_id": next_player_id, "remaining_throws": 3, "tie_breaker": True}
                
                user_name = self.players[next_player_id]["name"]
                # ✅ لا يرد - رسالة جديدة فقط
                await event.respond(f"**⦑ الجولة الإضافية ⦒**\n\n-عَزيزي/تي ◗ [{user_name}](tg://user?id={next_player_id}) ◖\nإرسل 3 مرات نرد .")
            else:
                # انتهت الجولة الإضافية
                self.waiting_for_dice = None
                await self.finish_tie_breaker(event)

    async def finish_tie_breaker(self, event):
        """إنهاء الجولة الإضافية للمتعادلين"""
        min_score = min(self.tied_scores.values())
        lowest_players = [pid for pid, score in self.tied_scores.items() if score == min_score]
        
        if len(lowest_players) == 1:
            eliminated_id = lowest_players[0]
            eliminated_name = self.players[eliminated_id]["name"]
            eliminated_score = self.tied_scores[eliminated_id]
            self.eliminated_players.append(eliminated_name)
            del self.players[eliminated_id]
            
            # ✅ لا يرد - رسالة جديدة فقط
            await event.respond(f"◈︙اللاعب `{eliminated_name}`\n- تم أقصائه من الجولة الإضافية (`{eliminated_score}` نقطة) .")
        else:
            eliminated_id = random.choice(lowest_players)
            eliminated_name = self.players[eliminated_id]["name"]
            eliminated_score = self.tied_scores[eliminated_id]
            self.eliminated_players.append(eliminated_name)
            del self.players[eliminated_id]
            
            # ✅ لا يرد - رسالة جديدة فقط
            await event.respond(f"◈︙اللاعب `{eliminated_name}`\n- تم أقصائه عشوائيا بسبب التعادل المستمر (`{eliminated_score}` نقطة) .")
        
        del self.tied_players
        del self.tied_scores
        
        await self.update_pinned_message(event)
        
        if len(self.players) == 1:
            await self.finish_game(event)
        else:
            self.current_round += 1
            await asyncio.sleep(3)
            await self.start_round(event)

    async def finish_game(self, event):
        """إنهاء اللعبة وإعلان الفائز"""
        winner_id = list(self.players.keys())[0]
        winner_name = self.players[winner_id]["name"]
        winner_score = self.players[winner_id]["current_round_score"]
        
        # ✅ لا يرد - رسالة جديدة فقط
        await event.respond(f"**🎊 🏆 مبروك! 🏆 🎊**\n\nالفائز هو:◗ {winner_name} ◖\nبمجموع نقاط الجولة الأخيرة: `{winner_score}`\n\nشكراً للجميع على المشاركة .")
        
        final_text = f"**🎲 لعبـة النـرد - انتهت**\n\n🏆 الفائز:◗ {winner_name} ◖\nنقاط الجولة الأخيرة: `{winner_score}`\n\n"
        final_text += "**المشاركون:**\n"
        for player in self.eliminated_players:
            final_text += f"ٴ❌ {player}\n"
        
        await event.client.edit_message(self.chat_id, self.pinned_message_id, final_text)
        
        if self.chat_id in dice_games:
            del dice_games[self.chat_id]

# باقي الأوامر تبقى كما هي...
@l313l.on(events.NewMessage(pattern='.نرد2'))
async def start_dice_game(event):
    """بدء لعبة النرد الجديدة"""
    user = await event.get_sender()
    chat_id = event.chat_id
    
    if user.id != l313l.uid:
        return
    
    if chat_id in dice_games:
        await event.reply("**❌ هناك لعبة نشطة بالفعل في هذه الدردشة!**")
        return
    
    game = DiceGame(chat_id)
    dice_games[chat_id] = game
    
    await game.create_pinned_message(event)
    
    await event.reply("**🎲 تم بدء لعبة النرد الجديدة!**\n\n**ارسل `Y` للانضمام للعبة**\n**ارسل `n` لإنهاء اللعبة**")
    await event.delete()

@l313l.on(events.NewMessage(pattern='^(?i)Y$'))
async def join_game(event):
    """الانضمام للعبة"""
    user = await event.get_sender()
    chat_id = event.chat_id
    
    if chat_id not in dice_games:
        return
    
    game = dice_games[chat_id]
    
    if game.game_active:
        await event.reply("<b>❌ اللعبة جاريه， لا يمكن الانضمام الآن!</b>")
        return
    
    success = await game.add_player(event, user)
    if success:
        # استخدام الإيموجي البريميوم في الرسالة مع تنسيق HTML
        message = f"<b>⪼ تم انضمام</b> <code>{user.first_name}</code> <b>إلى اللعبة </b><a href=\"emoji/5357069174512303778\">✅</a>"
        await event.reply(message, parse_mode=CustomParseMode("html"))
    else:
        await event.reply("<b>❌ أنت مشترك بالفعل في اللعبة!</b>", parse_mode=CustomParseMode("html"))
        
@l313l.on(events.NewMessage(pattern='^(?i)n$'))
async def end_game_command(event):
    """إنهاء اللعبة"""
    user = await event.get_sender()
    chat_id = event.chat_id
    
    if user.id != l313l.uid:
        return
    
    if chat_id not in dice_games:
        await event.reply("**❌ لا توجد لعبة نشطة في هذه الدردشة!**")
        return
    
    game = dice_games[chat_id]
    
    if not game.game_active:
        success = await game.start_game(event)
        if not success:
            return
    else:
        await event.reply("**⏸ تم إيقاف اللعبة!**")
        del dice_games[chat_id]

@l313l.on(events.NewMessage())
async def handle_dice_throws(event):
    """معالجة رمي النرد"""
    chat_id = event.chat_id
    user = await event.get_sender()
    
    if chat_id not in dice_games:
        return
    
    game = dice_games[chat_id]
    
    if not game.game_active or not game.waiting_for_dice:
        return
    
    if user.id != game.waiting_for_dice["user_id"]:
        return
    
    if event.dice and event.dice.emoticon == '🎲':
        dice_value = event.dice.value
        
        if hasattr(game, 'tied_players') and game.waiting_for_dice.get('tie_breaker'):
            await game.process_tie_breaker_dice(event, user.id, dice_value)
        else:
            await game.process_dice_throw(event, user.id, dice_value)
