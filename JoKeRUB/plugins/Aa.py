import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import User
from JoKeRUB import l313l
from ..core.managers import edit_or_reply
from ..Config import Config
import os

plugin_category = "tools"

# قاموس لتخزين الجلسات
user_sessions = {}

@l313l.ar_cmd(
    pattern="جلسة(?:\s|$)([\s\S]*)",
    command=("جلسة", plugin_category),
    info={
        "header": "لـ إنشـاء جلسـة ردود تلقائيـة",
        "الاستـخـدام": "{tr}جلسة + رقم الجلسة\nمثال: .جلسة 123456789",
    },
)
async def create_session_bot(event):
    "لـ إنشـاء جلسـة ردود تلقائيـة"
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edit_or_reply(event, "**⎉╎يجب عليك إدخال رقم الجلسة\nمثال:** `.جلسة 123456789`")
    
    session_name = input_str.strip()
    
    if session_name in user_sessions:
        return await edit_or_reply(event, f"**⎉╎الجلسة `{session_name}` مشغلة مسبقاً**")
    
    try:
        # إنشاء عميل جديد
        client = TelegramClient(
            session=f"sessions/{session_name}",
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH
        )
        
        # بدء الجلسة
        await client.start()
        
        # تخزين العميل في القاموس
        user_sessions[session_name] = {
            'client': client,
            'forwarding_map': {},
            'owner_username': (await event.client.get_me()).username
        }
        
        # إضافة المعالجات للأحداث
        @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and not e.out and e.sender.username != user_sessions[session_name]['owner_username']))
        async def forward_to_owner(event):
            try:
                owner_username = user_sessions[session_name]['owner_username']
                forwarded_msg = await event.forward_to(owner_username)
                user_sessions[session_name]['forwarding_map'][forwarded_msg.id] = event.sender_id
                print(f"📩 جلسة {session_name}: تم توجيه رسالة من {event.sender_id}")
            except Exception as e:
                print(f"❌ خطأ في التوجيه: {e}")

        @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.out and e.sender.username == user_sessions[session_name]['owner_username'] and e.is_reply))
        async def send_reply_to_user(event):
            reply_msg = await event.get_reply_message()
            forwarding_map = user_sessions[session_name]['forwarding_map']
            original_user_id = forwarding_map.get(reply_msg.id)
            
            if original_user_id:
                try:
                    await client.send_message(original_user_id, event.text)
                    await event.reply("✅ تم إرسال ردك بنجاح")
                    print(f"📤 جلسة {session_name}: تم إرسال رد إلى {original_user_id}")
                except Exception as e:
                    await event.reply(f"❌ فشل إرسال الرد: {e}")
            else:
                await event.reply("⚠️ لم أتمكن من العثور على المرسل الأصلي")
        
        await edit_or_reply(event, f"**⎉╎تم تشغيل جلسة الردود بنجاح 🧑🏻‍💻**\n**⎉╎رقم الجلسة:** `{session_name}`\n**⎉╎الجلسة الآن تعمل وتستقبل الرسائل**")
        
    except Exception as e:
        await edit_or_reply(event, f"**⎉╎خطأ في إنشاء الجلسة:** `{e}`")

@l313l.ar_cmd(
    pattern="ايقاف جلسة(?:\s|$)([\s\S]*)",
    command=("ايقاف جلسة", plugin_category),
    info={
        "header": "لـ إيقاف جلسة ردود",
        "الاستـخـدام": "{tr}ايقاف جلسة + رقم الجلسة\nمثال: .ايقاف جلسة 123456789",
    },
)
async def stop_session_bot(event):
    "لـ إيقاف جلسة ردود"
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edit_or_reply(event, "**⎉╎يجب عليك إدخال رقم الجلسة\nمثال:** `.ايقاف جلسة 123456789`")
    
    session_name = input_str.strip()
    
    if session_name not in user_sessions:
        return await edit_or_reply(event, f"**⎉╎الجلسة `{session_name}` غير موجودة**")
    
    try:
        # إيقاف العميل
        await user_sessions[session_name]['client'].disconnect()
        # حذف من القاموس
        del user_sessions[session_name]
        
        await edit_or_reply(event, f"**⎉╎تم إيقاف جلسة الردود بنجاح 🛑**\n**⎉╎رقم الجلسة:** `{session_name}`")
        
    except Exception as e:
        await edit_or_reply(event, f"**⎉╎خطأ في إيقاف الجلسة:** `{e}`")

@l313l.ar_cmd(
    pattern="الجلسات$",
    command=("الجلسات", plugin_category),
    info={
        "header": "لـ عرض الجلسات النشطة",
        "الاستـخـدام": "{tr}الجلسات",
    },
)
async def list_sessions(event):
    "لـ عرض الجلسات النشطة"
    if not user_sessions:
        return await edit_or_reply(event, "**⎉╎لا توجد جلسات نشطة حالياً**")
    
    sessions_list = "**⎉╎الجلسات النشطة حالياً:**\n\n"
    for session_name, session_data in user_sessions.items():
        sessions_list += f"**• الجلسة:** `{session_name}`\n"
        sessions_list += f"**• عدد الرسائل المخزنة:** `{len(session_data['forwarding_map'])}`\n\n"
    
    await edit_or_reply(event, sessions_list)

# إنشاء مجلد الجلسات إذا لم يكن موجوداً
if not os.path.exists("sessions"):
    os.makedirs("sessions")
