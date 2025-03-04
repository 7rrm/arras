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

# متغيرات التخزين
break_trigger = None
active_chat_id = None  # لتخزين معرف الدردشة المفعلة

# تفعيل الأمر في دردشة محددة
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^.تفعيل تفكيك البوت$'))
async def enable_break_bot(event):
    global active_chat_id
    active_chat_id = event.chat_id  # حفظ معرف الدردشة
    await event.edit("**᯽︙ تم تفعيل تفكيك البوت في هذه الدردشة بنجاح ✅**")

# تعطيل الأمر
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^.تعطيل تفكيك البوت$'))
async def disable_break_bot(event):
    global active_chat_id
    active_chat_id = None  # إلغاء تفعيل الدردشة
    await event.edit("**᯽︙ تم تعطيل تفكيك البوت في جميع الدردشات بنجاح ✅**")

# تفعيل تفكيك الكلمات عند تلقي الرسالة المحفزة
@l313l.on(events.NewMessage(incoming=True))
async def auto_break_word(event):
    global break_trigger, active_chat_id
    
    # التحقق من أن الرسالة في الدردشة المفعلة
    if active_chat_id is not None and event.chat_id == active_chat_id:
        if 'break_trigger' in globals() and break_trigger in event.raw_text:
            # الحصول على النص بعد النص المحفز
            text = event.raw_text.split(break_trigger, 1)[-1].strip()
            
            # التحقق مما إذا كانت الكلمة مفكوكة بالفعل (تحتوي على مسافات بين الأحرف)
            if ' ' in text:
                # إذا كانت الكلمة مفكوكة، يتم إرسالها كما هي
                await event.client.send_message(event.chat_id, text)
            else:
                # إذا لم تكن مفكوكة، يتم تفكيكها
                letters = ' '.join(list(text))
                await event.client.send_message(event.chat_id, letters)

# تعريف الأمر: تفكيك_بالبوت
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^.تفكيك_بالبوت (.*)'))
async def set_break_trigger(event):
    global break_trigger
    break_trigger = event.pattern_match.group(1)
    await event.edit(f"**᯽︙ تم تعيين النص المحفز لتفكيك الكلمات إلى: {break_trigger}**")
    
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
