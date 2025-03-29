#المطور aRRas
import asyncio
from telethon import events
from JoKeRUB import l313l

hussein_enabled = False
aljoker_enabled = False
JOKER_ID = {}

# تعريف الأمرين: .تفكيك و .ت
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^[\.\/](تفكيك|ت) (.*)'))
async def break_word(event):
    # الحصول على النص من الأمر
    text = event.pattern_match.group(2)
    
    # تفكيك النص إلى أحرف
    letters = ' '.join(list(text))
    
    # إرسال النص المفكوك كرسالة جديدة
    await event.respond(letters)
    
    # حذف الرسالة الأصلية (اختياري)
    await event.delete()

import asyncio
import re
from telethon import events
from JoKeRUB import l313l

# تعريف المتغيرات العامة
word_game_enabled = False
word_game_allowed_user_id = None  # معرف الشخص أو البوت المسموح له
word_game_trigger_text = "- اسرع واحد يكتب الكلمه ->"  # النص المحفز الافتراضي

# تفعيل ميزة الكلمات مع معرف الشخص أو البوت
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل كلمات(?: (\d+))?$'))
async def enable_word_game(event):
    global word_game_enabled, word_game_allowed_user_id
    user_id = event.pattern_match.group(1)  # الحصول على المعرف إذا تم إدخالها

    if user_id:
        word_game_allowed_user_id = int(user_id)  # تعيين المعرف المسموح له
    else:
        # إذا لم يتم إدخال معرف، يتم إعلام المستخدم بضرورة إدخال معرف
        await event.edit("**᯽︙ يرجى إدخال معرف صحيح بعد الأمر.**")
        return

    word_game_enabled = True
    await event.edit(f"ش")

# تعطيل ميزة الكلمات
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل كلمات$'))
async def disable_word_game(event):
    global word_game_enabled, word_game_allowed_user_id
    word_game_enabled = False
    word_game_allowed_user_id = None  # إلغاء تعيين المعرف المسموح له
    await event.edit("**᯽︙ تم تعطيل ميزة الكلمات بنجاح ✅**")

# تفعيل نص محفز مخصص
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل نص كلمات (.*)$'))
async def set_word_game_trigger_text(event):
    global word_game_trigger_text
    word_game_trigger_text = event.pattern_match.group(1)  # تعيين النص المحفز المخصص
    await event.edit(f"ش")

# الرد التلقائي على الرسائل
@l313l.on(events.NewMessage(incoming=True))
async def auto_reply_word_game(event):
    global word_game_enabled, word_game_allowed_user_id, word_game_trigger_text
    
    # التحقق من أن الميزة مفعلة وأن الرسالة من المعرف المسموح له
    if word_game_enabled and event.sender_id == word_game_allowed_user_id:
        if word_game_trigger_text in event.raw_text:
            # استخراج الكلمة بين الأقواس (أي من () أو {})
            match = re.search(r'[\({]([^)}]+)[\)}]', event.raw_text)
            if match:
                word = match.group(1).strip()  # إزالة المسافات الزائدة
                # إزالة النقطة من نهاية الكلمة إذا وجدت
                if word.endswith('.'):
                    word = word[:-1]
                # تأخير الرد بـ 1 ثانية
                await asyncio.sleep(1)
                # إرسال رسالة جديدة تحتوي على الكلمة المستخرجة (بدون الرد على الرسالة الأصلية)
                await event.client.send_message(event.chat_id, word)

# باقي الكود الحالي...
                
######المطور arras #####
                                  
import asyncio
from telethon import events
from JoKeRUB import l313l

# تعريف المتغيرات العامة
articles_enabled = False
articles_allowed_user_ids = set()  # مجموعة لتخزين معرفات المستخدمين المسموح لهم
articles_trigger_text = "⌔︙اكتبها بدون فواصل"  # النص المحفز الافتراضي
reply_delay = 2  # تأخير الرد بـ 2 ثانية

# تفعيل ميزة المقالات مع معرفات المستخدمين
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل مقالات(?: (\d+(?:,\d+)*))?$'))
async def enable_articles(event):
    global articles_enabled, articles_allowed_user_ids
    ids_input = event.pattern_match.group(1)  # الحصول على المعرفات إذا تم إدخالها

    # إضافة المعرفات إلى المجموعة
    if ids_input:
        articles_allowed_user_ids.update(map(int, ids_input.split(',')))
    else:
        # إذا لم يتم إدخال معرفات، يتم إعلام المستخدم بضرورة إدخال معرفات
        await event.edit("**᯽︙ يرجى إدخال معرفات صحيحة بعد الأمر.**")
        return

    articles_enabled = True
    await event.edit(f"ش")
                    # f"**المعرفات المسموحة:** {', '.join(map(str, articles_allowed_user_ids))}")

# تعطيل ميزة المقالات
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل مقالات$'))
async def disable_articles(event):
    global articles_enabled, articles_allowed_user_ids
    articles_enabled = False
    articles_allowed_user_ids.clear()  # مسح جميع المعرفات المسموحة
    await event.edit("**᯽︙ تم تعطيل ميزة المقالات بنجاح ✅**")

# تفعيل نص محفز مخصص
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل نص مقالات (.*)$'))
async def set_articles_trigger_text(event):
    global articles_trigger_text
    articles_trigger_text = event.pattern_match.group(1)  # تعيين النص المحفز المخصص
    await event.edit(f"ش")

# الرد التلقائي على الرسائل
@l313l.on(events.NewMessage(incoming=True))
async def auto_reply_articles(event):
    global articles_enabled, articles_allowed_user_ids, articles_trigger_text, reply_delay
    
    # التحقق من أن الميزة مفعلة وأن الرسالة من أحد المستخدمين المسموح لهم
    if articles_enabled and event.sender_id in articles_allowed_user_ids:
        if articles_trigger_text in event.raw_text:
            # استخراج النص الذي يحتوي على الفواصل
            text_with_symbols = event.raw_text.split(articles_trigger_text)[0].strip()
            # استبدال الفواصل بمسافات
            cleaned_text = text_with_symbols.replace("*", " ").replace("/", " ")
            # تأخير الرد بـ 2 ثانية
            await asyncio.sleep(reply_delay)
            # الرد على الرسالة
            await event.reply(cleaned_text)

# باقي الكود الحالي...
import asyncio
import re
from telethon import events
from JoKeRUB import l313l

# تعريف المتغيرات العامة
flags_enabled = False
active_chat_id = None
flags_allowed_user_ids = set()  # مجموعة لتخزين معرفات المستخدمين المسموح لهم
flags_trigger_text = "⌔︙اسرع واحد يكتب اسم الدولة للعلم↫"  # النص المحفز الافتراضي

# قاموس الأعلام والبلدان
flags_dict = {
    "🇯🇴": "الأردن",
    "🇪🇸": "إسبانيا",
    "🇷🇺": "روسيا",
    "🇮🇷": "ايران",
    "🇷🇴": "رومانيا",
    "🇺🇦": "أوكرانيا",
    "🇱🇾": "ليبيا",
    "🇶🇦": "قطر",
    "🇲🇦": "المغرب",
    "🇹🇳": "تونس",
    "🇦🇪": "الامارات",
    "🇻🇪": "فنزويلا",
    "🇨🇳": "الصين",
    "🇪🇬": "مصر",
    "🇮🇶": "العراق",
    "🇸🇦": "السعوديه",
    "🇩🇿": "الجزائر",
    "🇰🇵": "كوريا الشمالية",
    "🇸🇩": "السودان",
    "🇵🇰": "باكستان",
    "🇺🇸": "امريكا",
    "🇰🇼": "الكويت",
    "🇧🇷": "البرازيل",
    "🇫🇷": "فرنسا",
    "🇵🇸": "فلسطين",
    "🇧🇭": "البحرين",
    "🇸🇾": "سوريا",
    "🇳🇱": "هولندا",
    "🇸🇪": "السويد",
    "🇾🇪": "اليمن",
    "🇸🇸": "السودان",
    "🇦🇹": "النمسا",
    "🇯🇵": "اليابان",
    "🇱🇧": "لبنان",
    "🇲🇷": "موريتانيا",
    "🇦🇺": "استراليا",
    "🇮🇹": "ايطاليا",
    "🇬🇷": "اليونان",
    "🇬🇧": "بريطانيا",
    "🇷🇴": "رومانيا",
    "🇨🇭": "سويسرا",
}

# تفعيل ميزة الأعلام
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل اعلام(?: (\d+(?:,\d+)*))?$'))
async def enable_flags(event):
    global flags_enabled, active_chat_id, flags_allowed_user_ids
    ids_input = event.pattern_match.group(1)  # الحصول على المعرفات إذا تم إدخالها

    # إضافة المعرفات إلى المجموعة
    if ids_input:
        flags_allowed_user_ids.update(map(int, ids_input.split(',')))
    else:
        # إذا لم يتم إدخال معرفات، يتم إعلام المستخدم بضرورة إدخال معرفات
        await event.edit("**᯽︙ يرجى إدخال معرفات صحيحة بعد الأمر.**")
        return

    active_chat_id = event.chat_id  # حفظ معرف الدردشة
    flags_enabled = True
    await event.edit(f"ش")
                   #  f"**المعرفات المسموحة:** {', '.join(map(str, flags_allowed_user_ids))}")

# تعطيل ميزة الأعلام
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل اعلام$'))
async def disable_flags(event):
    global flags_enabled, active_chat_id, flags_allowed_user_ids
    flags_enabled = False
    active_chat_id = None
    flags_allowed_user_ids.clear()  # مسح جميع المعرفات المسموحة
    await event.edit("**᯽︙ تم تعطيل ميزة الأعلام بنجاح ✅**")

# تفعيل نص محفز مخصص
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل نص اعلام (.*)$'))
async def set_flags_trigger_text(event):
    global flags_trigger_text
    flags_trigger_text = event.pattern_match.group(1)  # تعيين النص المحفز المخصص
    await event.edit(f"ش")

# الرد التلقائي على الأعلام
@l313l.on(events.NewMessage(incoming=True))
async def auto_reply_flags(event):
    global flags_enabled, active_chat_id, flags_allowed_user_ids, flags_trigger_text, flags_dict
    
    # التحقق من أن الميزة مفعلة وأن الرسالة في الدردشة المحددة ومن المعرف المسموح
    if not (flags_enabled and event.chat_id == active_chat_id and event.sender_id in flags_allowed_user_ids):
        return

    if flags_trigger_text not in event.raw_text:
        return

    # البحث عن العلم داخل الأقواس (إذا وجد)
    flag_with_brackets = re.search(r'[\({]([^})]+)[\)}]', event.raw_text)
    if flag_with_brackets:
        flag = flag_with_brackets.group(1).strip()  # إزالة المسافات الزائدة
        # تجاهل النقطة في النهاية إذا وجدت
        if flag.endswith('.'):
            flag = flag[:-1]
    else:
        # إذا لم يكن هناك أقواس، يتم البحث عن العلم مباشرة
        flag = event.raw_text.split(flags_trigger_text)[-1].strip()
    
    # البحث عن العلم في القاموس
    if flag in flags_dict:
        country = flags_dict[flag]
        await asyncio.sleep(1)  # تأخير لمدة ثانية واحدة
        await event.reply(country)

import asyncio
import re
from telethon import events
from JoKeRUB import l313l

# تعريف المتغيرات العامة
break_enabled = False
active_chat_id = None
break_allowed_user_ids = set()
break_trigger_text = "⌔︙فكك :"
reply_mode = False  # متغير جديد لتحديد وضع الرد

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.(/?)تفعيل تفكيك(?:\s+(\d+))?(?:\s+(-?\d+))?$'))
async def enable_break_bot(event):
    global break_enabled, active_chat_id, break_allowed_user_ids, reply_mode
    user_id = event.pattern_match.group(2)
    group_id = event.pattern_match.group(3)
    is_reply_mode = bool(event.pattern_match.group(1))  # إذا كان هناك / قبل الأمر
    
    if not user_id:
        await event.edit("**⚠️ يرجى إدخال معرف المستخدم/البوت بعد الأمر**\nمثال: `.تفعيل تفكيك 123456789`\nأو `.تفعيل تفكيك` للوضع العادي")
        return
    
    break_allowed_user_ids.add(int(user_id))
    reply_mode = is_reply_mode  # تعيين وضع الرد
    
    if group_id:
        active_chat_id = int(group_id)
    else:
        active_chat_id = event.chat_id
    
    break_enabled = True
    mode_text = "وضع الرد" if is_reply_mode else "الوضع العادي"
    await event.edit(f"**✅ تم تفعيل التفكيك بنجاح**\n"
                    f"المجموعة: `{active_chat_id}`\n"
                    f"المستخدم المسموح: `{user_id}`\n"
                    f"الوضع: `{mode_text}`")

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل تفكيك$'))
async def disable_break_bot(event):
    global break_enabled, active_chat_id, break_allowed_user_ids, reply_mode
    break_enabled = False
    active_chat_id = None
    break_allowed_user_ids.clear()
    reply_mode = False
    await event.edit("**✅ تم تعطيل التفكيك بنجاح**")

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل نص تفكيك (.*)$'))
async def set_break_trigger_text(event):
    global break_trigger_text
    break_trigger_text = event.pattern_match.group(1)
    await event.edit(f"**✅ تم تعيين نص التفكيك إلى:** `{break_trigger_text}`")

@l313l.on(events.NewMessage(incoming=True))
async def break_word_on_trigger(event):
    global break_enabled, active_chat_id, break_allowed_user_ids, break_trigger_text, reply_mode
    
    if not break_enabled or event.chat_id != active_chat_id or event.sender_id not in break_allowed_user_ids:
        return
    
    # التحقق من وضع الرد
    if reply_mode:
        if not event.is_reply or not event.reply_to_msg_id:
            return
        # الحصول على الرسالة الأصلية التي تم الرد عليها
        original_message = await event.get_reply_message()
        if original_message.sender_id != l313l.uid:
            return
        
        # التحقق مما إذا كانت الرسالة الأصلية تحتوي على النص المحفز
        if break_trigger_text not in original_message.text:
            return
        
        delay = 1  # تأخير 1 ثانية في وضع الرد
    else:
        if break_trigger_text not in event.raw_text:
            return
        delay = 2  # تأخير 2 ثانية في الوضع العادي
    
    # تعبير عادي سريع ومحدد للأقواس {} و () فقط
    text_to_search = event.raw_text
    match = re.search(r'[{(]([^})]+)[})]', text_to_search.split(break_trigger_text)[-1] if not reply_mode else text_to_search, re.DOTALL)
    if match:
        word = match.group(1).strip()
        # إزالة أي فواصل أو مسافات زائدة
        word = re.sub(r'[\s\n]+', '', word)
        if word:
            letters = ' '.join(list(word))
            await asyncio.sleep(delay)  # استخدام التأخير المناسب حسب الوضع
            await event.reply(letters)


import asyncio
from telethon import events
from JoKeRUB import l313l

# تعريف المتغيرات العامة
meanings_enabled = False
active_chat_id = None
meanings_allowed_user_ids = set()  # مجموعة لتخزين معرفات المستخدمين المسموح لهم
meanings_trigger_text = "⌔︙اسرع واحد يدز معنى السمايل ~ "  # النص المحفز الافتراضي للمعاني

# قاموس السمايلات ومعانيها
smiley_meanings = {
    "🐭": "فأر",
    "🍎": "تفاحه",
    "🦁": "اسد",
    "🐓": "ديك",
    "🐄": "بقره",
    "🦂": "عقرب",
    "🦉": "بومه",
    "🐫": "جمل",
    "🦋": "ف��اشه",
    "🐟": "سمكه",
    "🐔": "دجاجه",
    "🦈": "قرش",
    "🐺": "ذئب",
    "🐧": "بطريق",
    "🐝": "نحله",
    "🐸": "ضفدع",
    "🐬": "دولفين",
    "🐅": "نمر",
    "🦇": "خفاش",
    # يمكنك إضافة المزيد من السمايلات ومعانيها هنا
}

# تفعيل ميزة المعاني
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل معاني(?: (\d+(?:,\d+)*))?$'))
async def enable_meanings_bot(event):
    global meanings_enabled, active_chat_id, meanings_allowed_user_ids
    ids_input = event.pattern_match.group(1)  # الحصول على المعرفات إذا تم إدخالها

    # إضافة المعرفات إلى المجموعة
    if ids_input:
        meanings_allowed_user_ids.update(map(int, ids_input.split(',')))
    else:
        # إذا لم يتم إدخال معرفات، يتم إعلام المستخدم بضرورة إدخال معرفات
        await event.edit("**᯽︙ يرجى إدخال معرفات صحيحة بعد الأمر.**")
        return

    active_chat_id = event.chat_id  # حفظ معرف المجموعة
    meanings_enabled = True
    await event.edit(f"ش")
                   #  f"**المعرفات المسموحة:** {', '.join(map(str, meanings_allowed_user_ids))}")

# تعطيل ميزة المعاني
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل معاني$'))
async def disable_meanings_bot(event):
    global meanings_enabled, active_chat_id, meanings_allowed_user_ids
    active_chat_id = None  # إلغاء تفعيل المجموعة
    meanings_enabled = False
    meanings_allowed_user_ids.clear()  # مسح جميع المعرفات المسموحة
    await event.edit("**᯽︙ تم تعطيل معاني السمايلات في جميع المجموعات بنجاح ✅**")

# تفعيل نص محفز مخصص
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل نص معاني (.*)$'))
async def set_meanings_trigger_text(event):
    global meanings_trigger_text
    meanings_trigger_text = event.pattern_match.group(1)  # تعيين النص المحفز المخصص
    await event.edit(f"ش")

# الرد التلقائي على السمايلات
@l313l.on(events.NewMessage(incoming=True))
async def auto_reply_meanings(event):
    global meanings_enabled, active_chat_id, meanings_allowed_user_ids, meanings_trigger_text, smiley_meanings
    
    # التحقق من أن الرسالة في المجموعة المفعلة ومن المستخدم المسموح له
    if meanings_enabled and event.chat_id == active_chat_id and event.sender_id in meanings_allowed_user_ids:
        if meanings_trigger_text in event.raw_text:
            # البحث عن السمايل في الرسالة
            for smiley, meaning in smiley_meanings.items():
                if smiley in event.raw_text:
                    # إرسال معنى السمايل كرسالة جديدة (بدون رد)
                    await event.client.send_message(event.chat_id, f"{meaning}")
                    break

                    
@l313l.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def mark_as_read(event):
    global aljoker_enabled, JOKER_ID
    sender_id = event.sender_id
    if aljoker_enabled and sender_id in JOKER_ID:
        joker_time = JOKER_ID[sender_id]
        if joker_time > 0:
            await asyncio.sleep(joker_time)
        await event.mark_read()

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.التكبر تعطيل$'))
async def Hussein(event):
    global aljoker_enabled
    aljoker_enabled = False
    await event.edit('**᯽︙ تم تعطيل امر التكبر بنجاح ✅**')

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.التكبر (\d+) (\d+)$'))
async def Hussein(event):
    global aljoker_enabled, JOKER_ID
    joker_time = int(event.pattern_match.group(1))
    user_id = int(event.pattern_match.group(2)) 
    JOKER_ID[user_id] = joker_time
    aljoker_enabled = True
    await event.edit(f'**᯽︙ تم تفعيل امر التكبر بنجاح مع  {joker_time} ثانية للمستخدم {user_id}**')

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.مود التكبر تعطيل$'))
async def Hussein(event):
    global hussein_enabled
    hussein_enabled = False
    await event.edit('**᯽︙ تم تعطيل امر التكبر على الجميع بنجاح ✅**')
    
@l313l.on(admin_cmd(pattern=f"مود التكبر (\d+)"))
async def Hussein(event):
    global hussein_enabled, hussein_time
    hussein_time = int(event.pattern_match.group(1))
    hussein_enabled = True
    await event.edit(f'**᯽︙ تم تفعيل امر التكبر بنجاح مع  {hussein_time} ثانية**')

@l313l.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def Hussein(event):
    global hussein_enabled
    if hussein_enabled:
        await asyncio.sleep(hussein_time)
        await event.mark_read()
        
