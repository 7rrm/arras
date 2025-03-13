from JoKeRUB import l313l
from ..core.managers import edit_or_reply
from datetime import datetime
import random
import asyncio
import akinator
from telethon import events
plugin_category = "fun"
#str 122939#المليون

    
import random
from telethon import events

# قائمة الأسئلة
A_qq = [
    {"aW": "ما هو الحيوان الذي يمتلك أكبر عدد من الأسنان؟", "choices": ["التمساح", "القرش", "الفيل"], "Wa": "القرش"},
    {"aW": "ما هو العنصر الكيميائي الذي يرمز له بـ 'Au'؟", "choices": ["الذهب", "الفضة", "النحاس"], "Wa": "الذهب"},
    {"aW": "ما هي أكبر قارة في العالم؟", "choices": ["آسيا", "أفريقيا", "أوروبا"], "Wa": "آسيا"},
    {"aW": "من هو مؤلف رواية 'البؤساء'؟", "choices": ["فيكتور هوغو", "شارلز ديكنز", "ليو تولستوي"], "Wa": "فيكتور هوغو"},
    {"aW": "ما هي اللغة الرسمية للبرازيل؟", "choices": ["البرتغالية", "الإسبانية", "الإنجليزية"], "Wa": "البرتغالية"},
    {"aW": "ما هو أعمق محيط في العالم؟", "choices": ["المحيط الهادئ", "المحيط الأطلسي", "المحيط الهندي"], "Wa": "المحيط الهادئ"},
    {"aW": "من هو مخترع المصباح الكهربائي؟", "choices": ["توماس إديسون", "ألكسندر جراهام بيل", "نيكولا تسلا"], "Wa": "توماس إديسون"},
    {"aW": "ما هي عاصمة اليابان؟", "choices": ["طوكيو", "أوساكا", "كيوتو"], "Wa": "طوكيو"},
    {"aW": "من هو مؤلف كتاب 'الإخوان كارامازوف'؟", "choices": ["فيودور دوستويفسكي", "ليو تولستوي", "أنطون تشيخوف"], "Wa": "فيودور دوستويفسكي"},
    {"aW": "ما هو الطائر الذي يمكنه الطيران للخلف؟", "choices": ["الطنان", "النسر", "البومة"], "Wa": "الطنان"},
    {"aW": "ما هي أصغر دولة في العالم؟", "choices": ["الفاتيكان", "موناكو", "ناورو"], "Wa": "الفاتيكان"},
    {"aW": "ما هو أطول نهر في العالم؟", "choices": ["نهر النيل", "نهر الأمازون", "نهر يانغتسي"], "Wa": "نهر النيل"},
    {"aW": "من هو مؤلف مسرحية 'هاملت'؟", "choices": ["ويليام شكسبير", "سوفوكليس", "موليير"], "Wa": "ويليام شكسبير"},
    {"aW": "ما هو الكوكب الأصغر في المجموعة الشمسية؟", "choices": ["عطارد", "بلوتو", "المريخ"], "Wa": "عطارد"},
    {"aW": "من هو مؤلف رواية 'الحرب والسلام'؟", "choices": ["ليو تولستوي", "فيودور دوستويفسكي", "أنطون تشيخوف"], "Wa": "ليو تولستوي"},
    {"aW": "ما هو أقدم جامعة في العالم؟", "choices": ["جامعة القرويين", "جامعة بولونيا", "جامعة أكسفورد"], "Wa": "جامعة القرويين"},
    {"aW": "ما هو العنصر الكيميائي الذي يرمز له بـ 'O'؟", "choices": ["أكسجين", "أوزون", "أوسميوم"], "Wa": "أكسجين"},
    {"aW": "ما هي عملة اليابان؟", "choices": ["الين", "الوون", "اليوان"], "Wa": "الين"},
    {"aW": "من هو مؤلف مسرحية 'مكبث'؟", "choices": ["ويليام شكسبير", "كريستوفر مارلو", "بن جونسون"], "Wa": "ويليام شكسبير"},
    {"aW": "ما هو الحيوان الوطني لأستراليا؟", "choices": ["الكنغر", "الكوالا", "الإيمو"], "Wa": "الكنغر"},
    {"aW": "ما هي أكبر دولة في أفريقيا من حيث المساحة؟", "choices": ["الجزائر", "السودان", "ليبيا"], "Wa": "الجزائر"},
    {"aW": "ما هو أطول نفق في العالم؟", "choices": ["نفق سانت غوتارد", "نفق سيكان", "نفق لوشبرغ"], "Wa": "نفق سانت غوتارد"},
    {"aW": "ما هي أكبر جزيرة في العالم؟", "choices": ["غرينلاند", "نيو غينيا", "بورنيو"], "Wa": "غرينلاند"},
    {"aW": "من هو مؤلف كتاب 'الأمير'؟", "choices": ["نيكولو مكيافيلي", "توماس هوبز", "جون لوك"], "Wa": "نيكولو مكيافيلي"},
    {"aW": "ما هي الدولة التي تضم مدينة البندقية؟", "choices": ["إيطاليا", "فرنسا", "إسبانيا"], "Wa": "إيطاليا"},
    {"aW": "من هو مخترع الراديو؟", "choices": ["غوليلمو ماركوني", "نيكولا تسلا", "ألكسندر جراهام بيل"], "Wa": "غوليلمو ماركوني"},
    {"aW": "ما هي عاصمة كندا؟", "choices": ["أوتاوا", "تورونتو", "مونتريال"], "Wa": "أوتاوا"},
    {"aW": "ما هو أقدم علم في العالم؟", "choices": ["علم الرياضيات", "علم الفلك", "علم الكيمياء"], "Wa": "علم الفلك"},
    {"aW": "ما هي أصغر دولة في أفريقيا؟", "choices": ["سيشيل", "غامبيا", "موريشيوس"], "Wa": "سيشيل"},
    {"aW": "ما هو البركان الأكثر نشاطاً في العالم؟", "choices": ["كيلاويا", "إتنا", "فيزوف"], "Wa": "كيلاويا"},
    {"aW": "ما هي اللغة الرسمية للأرجنتين؟", "choices": ["الإسبانية", "البرتغالية", "الإنجليزية"], "Wa": "الإسبانية"},
    {"aW": "ما هو العنصر الكيميائي الذي يرمز له بـ 'Fe'؟", "choices": ["الحديد", "الفلور", "الفرانسيوم"], "Wa": "الحديد"},
    {"aW": "ما هي عاصمة جنوب أفريقيا؟", "choices": ["بريتوريا", "كيب تاون", "جوهانسبرغ"], "Wa": "بريتوريا"},
    {"aW": "من هو مؤلف كتاب 'الأخوة كارامازوف'؟", "choices": ["فيودور دوستويفسكي", "ليو تولستوي", "أنطون تشيخوف"], "Wa": "فيودور دوستويفسكي"},
    {"aW": "ما هو الحيوان الذي يعيش أطول عمراً؟", "choices": ["السلحفاة", "الفيل", "الببغاء"], "Wa": "السلحفاة"},
    {"aW": "ما هو أصغر كوكب في المجموعة الشمسية؟", "choices": ["عطارد", "بلوتو", "المريخ"], "Wa": "عطارد"},
    {"aW": "ما هي اللغة الرسمية لمصر؟", "choices": ["العربية", "الإنجليزية", "الفرنسية"], "Wa": "العربية"},
    {"aW": "من هو مؤلف كتاب 'الجمهورية'؟", "choices": ["أفلاطون", "أرسطو", "سقراط"], "Wa": "أفلاطون"},
    {"aW": "ما هي عاصمة الهند؟", "choices": ["نيودلهي", "مومباي", "بنغالور"], "Wa": "نيودلهي"}
]

qq = [
    {"aW": "ما هو أطول نهر في العالم؟", "choices": ["النيل", "الأمازون", "المسيسيبي"], "Wa": "الأمازون"},
    {"aW": "من هو مؤلف رواية 'البؤساء'؟", "choices": ["فيكتور هوغو", "تشارلز ديكنز", "ليو تولستوي"], "Wa": "فيكتور هوغو"},
    {"aW": "كم عدد الكواكب في نظامنا الشمسي؟", "choices": ["8", "9", "10"], "Wa": "8"},
]

import random
from telethon import events

# قاموس لتخزين الرصيد لكل مستخدم
user_balances = {}

# قاموس لتخزين حالة المشاركة لكل مستخدم
user_participation = {}

# ID المطور
DEVELOPER_ID = 5427469031

@l313l.ar_cmd(
    pattern="المليون$",
    command=("المليون", plugin_category),
    info={
        "header": "Play a million game.",
        "description": "لعبه مثل مال من سيربح المليون",
        "usage": "{tr}المليون",
    },
)
async def million(event):
    user_id = event.sender_id

    # التحقق من مشاركة المستخدم
    if user_id not in user_participation:
        await edit_or_reply(event, "يجب عليك المشاركة أولاً بإرسال `.اشارك`.")
        return

    # التحقق من وجود الرصيد
    if user_id not in user_balances:
        user_balances[user_id] = 0

    # اختيار سؤال عشوائي
    Bq = qq + A_qq  # تأكد من وجود qq و A_qq في الكود الأصلي
    aW = random.choice(Bq)
    choices = aW["choices"][:]
    random.shuffle(choices)
    choices_text = "\n".join([f"{i+1}. {choice}" for i, choice in enumerate(choices)])
    await edit_or_reply(event, f"{aW['aW']}\n\n{choices_text}\n\nاكتب رقم الإجابة الصحيحة:")

    async with l313l.conversation(event.chat_id) as conv:
        response = await conv.wait_event(events.NewMessage(pattern=r'^[1-3]$', from_users=event.sender_id))
        Wa_index = int(response.text) - 1
        if choices[Wa_index] == aW["Wa"]:
            user_balances[user_id] += 200
            await response.reply(f"🎉 صحيح! إجابتك صحيحة.\nتم إضافة 200$ إلى رصيدك.\nرصيدك الكلي: {user_balances[user_id]}$")

            # التحقق إذا وصل الرصيد إلى 600$
            if user_balances[user_id] >= 600:
                await response.reply(
                    "الآن أصبح رصيدك 600$.\n"
                    "هل تريد الانسحاب أم الاستمرار؟\n"
                    "ارسل (`.انسحب`) للانسحاب\n"
                    "ارسل (`.استمر`) للاستمرار"
                )
        else:
            await response.reply(f"❌ خطأ! الإجابة الصحيحة هي: {aW['Wa']}")

@l313l.ar_cmd(
    pattern="اشارك$",
    command=("اشارك", plugin_category),
    info={
        "header": "Join the game.",
        "description": "للاشتراك في اللعبة",
        "usage": "{tr}اشارك",
    },
)
async def join(event):
    user_id = event.sender_id
    user_participation[user_id] = True
    user_balances[user_id] = 0
    await edit_or_reply(event, "تمت مشاركتك في اللعبة. يمكنك الآن إرسال `.المليون` للبدء.")

@l313l.ar_cmd(
    pattern="رصيدي$",
    command=("رصيدي", plugin_category),
    info={
        "header": "Check your balance.",
        "description": "لعرض رصيدك الحالي",
        "usage": "{tr}رصيدي",
    },
)
async def balance(event):
    user_id = event.sender_id
    if user_id in user_balances:
        await edit_or_reply(event, f"رصيدك الحالي: {user_balances[user_id]}$")
    else:
        await edit_or_reply(event, "رصيدك الحالي: 0$")

@l313l.ar_cmd(
    pattern="انسحب$",
    command=("انسحب", plugin_category),
    info={
        "header": "Withdraw from the game.",
        "description": "للانسحاب من اللعبة",
        "usage": "{tr}انسحب",
    },
)
async def withdraw(event):
    user_id = event.sender_id
    if user_id in user_balances:
        if user_balances[user_id] >= 600:
            await edit_or_reply(event, f"تم الانسحاب. رصيدك النهائي: {user_balances[user_id]}$")
            user_balances[user_id] = 0
            user_participation.pop(user_id, None)
        else:
            await edit_or_reply(event, "لا يمكنك الانسحاب إلا إذا كان رصيدك 600$ أو أكثر.")
    else:
        await edit_or_reply(event, "لم تشارك في اللعبة بعد.")

@l313l.ar_cmd(
    pattern="استمر$",
    command=("استمر", plugin_category),
    info={
        "header": "Continue the game.",
        "description": "للاستمرار في اللعبة",
        "usage": "{tr}استمر",
    },
)
async def continue_game(event):
    user_id = event.sender_id
    if user_id in user_balances and user_balances[user_id] >= 600:
        await edit_or_reply(event, "ستستمر اللعبة. يمكنك إرسال `.المليون` للبدء.")
    else:
        await edit_or_reply(event, "لا يمكنك الاستمرار إلا إذا كان رصيدك 600$ أو أكثر.")

@l313l.ar_cmd(
    pattern="انهاء$",
    command=("انهاء", plugin_category),
    info={
        "header": "End the game for a user.",
        "description": "لإنهاء اللعبة للمستخدم الحالي (للمطور فقط)",
        "usage": "{tr}انهاء",
    },
)
async def end_game(event):
    user_id = event.sender_id
    if user_id == DEVELOPER_ID:
        target_user_id = event.chat_id
        if target_user_id in user_balances:
            user_balances.pop(target_user_id, None)
            user_participation.pop(target_user_id, None)
            await edit_or_reply(event, "تم إنهاء اللعبة للمستخدم الحالي.")
        else:
            await edit_or_reply(event, "المستخدم الحالي ليس مشاركًا في اللعبة.")
    else:
        await edit_or_reply(event, "هذا الأمر متاح للمطور فقط.")


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
    

@l313l.on(events.NewMessage(pattern='.اصابع'))
async def rock_paper_scissors(event):
    choices = {
        "حجرة": "ورقة",
        "ورقة": "مقص",
        "مقص": "حجرة"
    }
    user_choice = event.text.split()[-1]

    if user_choice not in choices:
        await edit_or_reply(event, "يرجى اختيار واحد من الخيارات التالية: حجرة، ورقة، أو مقص.")
        return

    bot_choice = random.choice(list(choices.keys()))
    if user_choice == bot_choice:
        result = "تعادل!"
    elif choices[bot_choice] == user_choice:
        result = "🎉 مبروك! لقد فزت."
    else:
        result = "😢 لقد خسرت. حاول مرة أخرى."

    await edit_or_reply(event, f"اختيارك: {user_choice}\nاختيار الساحر: {bot_choice}\nنتيجة اللعبة: {result}")
