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
from telethon import events
from JoKeRUB import l313l

# تعريف المتغيرات العامة
flags_enabled = False
active_chat_id = None
reply_delay = 0  # التأخير الافتراضي
allowed_ids = set()  # مجموعة لتخزين المعارف المسموح لهم
flags_trigger_text = "↜︙لأي دوله هذا العلم ؟ ↫"  # النص المحفز الافتراضي للأعلام

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
}
# تفعيل ميزة الأعلام
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل اعلام(?: (\d+))?(?: (\d+(?:,\d+)*))?$'))
async def enable_flags(event):
    global flags_enabled, active_chat_id, reply_delay, allowed_ids
    delay = event.pattern_match.group(1)  # الحصول على التأخير إذا تم إدخاله
    ids_input = event.pattern_match.group(2)  # الحصول على المعارف إذا تم إدخالها

    # تعيين التأخير (إذا لم يتم إدخال تأخير، يتم استخدام القيمة الافتراضية 0)
    reply_delay = int(delay) if delay else 0

    # إضافة المعارف إلى المجموعة
    if ids_input:
        allowed_ids.update(map(int, ids_input.split(',')))
    else:
        # إذا لم يتم إدخال معرفات، يتم إعلام المستخدم بضرورة إدخال معرفات
        await event.edit("**᯽︙ يرجى إدخال معرفات صحيحة بعد الأمر.**")
        return

    active_chat_id = event.chat_id  # حفظ معرف الدردشة
    flags_enabled = True
    await event.edit(f"**᯽︙ تم تفعيل ميزة الأعلام في هذه الدردشة بنجاح مع تأخير {reply_delay} ثانية ✅**\n"
                     f"**المعرفات المسموحة:** {', '.join(map(str, allowed_ids))}")

# تعطيل ميزة الأعلام
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل اعلام$'))
async def disable_flags(event):
    global flags_enabled, active_chat_id, allowed_ids
    flags_enabled = False
    active_chat_id = None
    allowed_ids.clear()  # مسح جميع المعارف المسموحة
    await event.edit("**᯽︙ تم تعطيل ميزة الأعلام بنجاح ✅**")

# تفعيل نص مخصص
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل نص اعلام (.*)$'))
async def set_flags_trigger_text(event):
    global flags_trigger_text
    flags_trigger_text = event.pattern_match.group(1)  # تعيين النص المحفز المخصص
    await event.edit(f"**᯽︙ تم تعيين النص المحفز إلى:** `{flags_trigger_text}`")

# الرد التلقائي على الأعلام
@l313l.on(events.NewMessage(incoming=True))
async def auto_reply_flags(event):
    global flags_enabled, active_chat_id, reply_delay, flags_dict, allowed_ids, trigger_text
    
    # التحقق من أن الميزة مفعلة وأن الرسالة في الدردشة المحددة ومن المعرف المسموح
    if flags_enabled and event.chat_id == active_chat_id and event.sender_id in allowed_ids:
        if trigger_text in event.raw_text:  # استخدام النص المحفز المخصص
            for flag, country in flags_dict.items():
                if flag in event.raw_text:
                    await asyncio.sleep(reply_delay)
                    await event.reply(country)
                    break

import asyncio
import re
from telethon import events
from JoKeRUB import l313l

# تعريف المتغيرات العامة
break_enabled = False
active_chat_id = None
allowed_user_ids = set()  # مجموعة لتخزين معرفات المستخدمين المسموح لهم
break_trigger_text = "⌔︙فكك :"  # النص المحفز الافتراضي للتفكيك

# تفعيل تفكيك البوت
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل تفكيك(?: (\d+(?:,\d+)*))?$'))
async def enable_break_bot(event):
    global break_enabled, active_chat_id, allowed_user_ids
    ids_input = event.pattern_match.group(1)  # الحصول على المعرفات إذا تم إدخالها

    # إضافة المعرفات إلى المجموعة
    if ids_input:
        allowed_user_ids.update(map(int, ids_input.split(',')))
    else:
        # إذا لم يتم إدخال معرفات، يتم إعلام المستخدم بضرورة إدخال معرفات
        await event.edit("**᯽︙ يرجى إدخال معرفات صحيحة بعد الأمر.**")
        return

    active_chat_id = event.chat_id  # حفظ معرف المجموعة
    break_enabled = True
    await event.edit(f"**᯽︙ تم تفعيل تفكيك البوت في هذه المجموعة بنجاح ✅**\n"
                     f"**المعرفات المسموحة:** {', '.join(map(str, allowed_user_ids))}")

# تعطيل تفكيك البوت
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل تفكيك$'))
async def disable_break_bot(event):
    global break_enabled, active_chat_id, allowed_user_ids
    active_chat_id = None  # إلغاء تفعيل المجموعة
    break_enabled = False
    allowed_user_ids.clear()  # مسح جميع المعرفات المسموحة
    await event.edit("**᯽︙ تم تعطيل تفكيك البوت في جميع المجموعات بنجاح ✅**")

#تفعيل نص تفكيك
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل نص تفكيك (.*)$'))
async def set_break_trigger_text(event):
    global break_trigger_text
    break_trigger_text = event.pattern_match.group(1)  # تعيين النص المحفز المخصص
    await event.edit(f"**᯽︙ تم تعيين النص المحفز إلى:** `{break_trigger_text}`")

# تفكيك الكلمة التي تلي النص المحفز
@l313l.on(events.NewMessage(incoming=True))
async def break_word_on_trigger(event):
    global break_enabled, active_chat_id, allowed_user_ids, trigger_text
    
    # التحقق من أن الرسالة في المجموعة المفعلة ومن المستخدم المسموح له
    if break_enabled and event.chat_id == active_chat_id and event.sender_id in allowed_user_ids:
        if trigger_text in event.raw_text:
            # البحث عن النص داخل الأقواس (إذا وجد)
            match_with_brackets = re.search(r'\{([^}]+)\}', event.raw_text)
            if match_with_brackets:
                word = match_with_brackets.group(1)
            else:
                # إذا لم يكن هناك أقواس، يتم تفكيك النص الذي يلي النص المحفز مباشرة
                word = event.raw_text.split(trigger_text)[-1].strip()
            
            # تفكيك النص إلى أحرف
            letters = ' '.join(list(word))
            # إرسال النص المفكوك كرسالة جديدة
            await event.respond(letters)

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
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل ايدي معاني(?: (\d+(?:,\d+)*))?$'))
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
    await event.edit(f"**᯽︙ تم تفعيل معاني السمايلات في هذه المجموعة بنجاح ✅**\n"
                     f"**المعرفات المسموحة:** {', '.join(map(str, meanings_allowed_user_ids))}")

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
    await event.edit(f"**᯽︙ تم تعيين النص المحفز إلى:** `{meanings_trigger_text}`")

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
        
