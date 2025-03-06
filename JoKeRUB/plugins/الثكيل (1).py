import asyncio
import re
from telethon import events
from JoKeRUB import l313l

# معرف المستخدم المسموح له (يتم تعيينه يدويًا في الكود)
allowed_user_id = 6945878804  # قم بتغيير هذا الرقم إلى معرف المستخدم المسموح له

# معرف المجموعة المفعلة
active_chat_id = None

# تفعيل تفكيك البوت
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل تفكيك$'))
async def enable_break_bot(event):
    global active_chat_id
    active_chat_id = event.chat_id  # حفظ معرف المجموعة
    await event.edit("**᯽︙ تم تفعيل تفكيك البوت في هذه المجموعة بنجاح ✅**")

# تعطيل تفكيك البوت
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل تفكيك$'))
async def disable_break_bot(event):
    global active_chat_id
    active_chat_id = None  # إلغاء تفعيل المجموعة
    await event.edit("**᯽︙ تم تعطيل تفكيك البوت في جميع المجموعات بنجاح ✅**")

# تفكيك الكلمة التي تلي النص "⌔︙فكك :"
@l313l.on(events.NewMessage(incoming=True))
async def break_word_on_trigger(event):
    global active_chat_id, allowed_user_id
    
    # التحقق من أن الرسالة في المجموعة المفعلة ومن المستخدم المسموح له
    if active_chat_id is not None and event.chat_id == active_chat_id and event.sender_id == allowed_user_id:
        if "⌔︙فكك :" in event.raw_text:
            # استخراج النص داخل الأقواس
            match = re.search(r'\{([^}]+)\}', event.raw_text)
            if match:
                word = match.group(1)
                # تفكيك النص إلى أحرف
                letters = ' '.join(list(word))
                # إرسال النص المفكوك كرسالة جديدة
                await event.respond(letters)
                

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
    "🦋": "فراشه",
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

# النص المحفز
trigger_text = "↜︙ما معنى هذا السمايل ؟ ↫"

# معرف المجموعة المفعلة
active_chat_id = None

# معرف المستخدم المسموح له
allowed_user_id = None  # سيتم تعيينه عند التفاعل مع الأمر

# تفعيل الأمر في مجموعة محددة
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^.تفعيل معاني$'))
async def enable_meanings_bot(event):
    global active_chat_id
    active_chat_id = event.chat_id  # حفظ معرف المجموعة
    await event.edit("**᯽︙ تم تفعيل معاني السمايلات في هذه المجموعة بنجاح ✅**")

# تعطيل الأمر
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^.تعطيل معاني$'))
async def disable_meanings_bot(event):
    global active_chat_id
    active_chat_id = None  # إلغاء تفعيل المجموعة
    await event.edit("**᯽︙ تم تعطيل معاني السمايلات في جميع المجموعات بنجاح ✅**")

# تفعيل الرد التلقائي على السمايلات
@l313l.on(events.NewMessage(incoming=True))
async def auto_reply_meanings(event):
    global active_chat_id, trigger_text, smiley_meanings, allowed_user_id
    
    # التحقق من أن الرسالة في المجموعة المفعلة ومن المستخدم المسموح له
    if (active_chat_id is not None and event.chat_id == active_chat_id and
        event.sender_id == allowed_user_id):  # التحقق من معرف المستخدم
        if trigger_text in event.raw_text:
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
