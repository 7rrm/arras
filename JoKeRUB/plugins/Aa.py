import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import User
from JoKeRUB import l313l
from ..core.managers import edit_or_reply
from ..Config import Config
import os
import sqlite3

plugin_category = "tools"

# قاموس لتخزين الجلسات
user_sessions = {}

# إنشاء مجلد الجلسات إذا لم يكن موجوداً
sessions_dir = "sessions"
if not os.path.exists(sessions_dir):
    os.makedirs(sessions_dir, mode=0o755)

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
    session_file = os.path.join(sessions_dir, f"{session_name}.session")
    
    if session_name in user_sessions:
        return await edit_or_reply(event, f"**⎉╎الجلسة `{session_name}` مشغلة مسبقاً**")
    
    try:
        # التأكد من صلاحيات الملف
        if os.path.exists(session_file):
            os.chmod(session_file, 0o644)
        
        # إنشاء عميل جديد
        client = TelegramClient(
            session=session_file,
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH
        )
        
        # بدء الجلسة
        await client.start()
        
        # الحصول على معلومات المستخدم
        me = await client.get_me()
        owner_username = me.username if me.username else f"user{me.id}"
        
        # تخزين العميل في القاموس
        user_sessions[session_name] = {
            'client': client,
            'forwarding_map': {},
            'owner_username': owner_username,
            'owner_id': me.id
        }
        
        # إضافة المعالجات للأحداث
        @client.on(events.NewMessage(incoming=True))
        async def handle_new_message(event):
            if not event.is_private or event.out:
                return
                
            session_data = user_sessions.get(session_name)
            if not session_data:
                return
                
            # تجاهل الرسائل من المطور نفسه
            if event.sender_id == session_data['owner_id']:
                return
                
            try:
                # إعادة توجيه الرسالة إلى المطور
                forwarded_msg = await event.forward_to(session_data['owner_id'])
                session_data['forwarding_map'][forwarded_msg.id] = event.sender_id
                print(f"📩 جلسة {session_name}: تم توجيه رسالة من {event.sender_id}")
            except Exception as e:
                print(f"❌ خطأ في التوجيه: {e}")

        @client.on(events.NewMessage(outgoing=True))
        async def handle_outgoing_message(event):
            if not event.is_private or not event.is_reply:
                return
                
            session_data = user_sessions.get(session_name)
            if not session_data:
                return
                
            reply_msg = await event.get_reply_message()
            forwarding_map = session_data['forwarding_map']
            original_user_id = forwarding_map.get(reply_msg.id)
            
            if original_user_id:
                try:
                    # إرسال الرد إلى المستخدم الأصلي
                    await client.send_message(original_user_id, event.text)
                    await event.reply("✅ تم إرسال ردك بنجاح")
                    print(f"📤 جلسة {session_name}: تم إرسال رد إلى {original_user_id}")
                except Exception as e:
                    await event.reply(f"❌ فشل إرسال الرد: {e}")
            else:
                await event.reply("⚠️ لم أتمكن من العثور على المرسل الأصلي")
        
        await edit_or_reply(event, f"**⎉╎تم تشغيل جلسة الردود بنجاح 🧑🏻‍💻**\n**⎉╎رقم الجلسة:** `{session_name}`\n**⎉╎البوت:** @{(await client.get_me()).username}\n**⎉╎الجلسة الآن تعمل وتستقبل الرسائل**")
        
    except sqlite3.OperationalError as e:
        await edit_or_reply(event, f"**⎉╎خطأ في قاعدة البيانات:** `{e}`\n**⎉╎حاول تغيير رقم الجلسة**")
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
        me = await session_data['client'].get_me()
        sessions_list += f"**• الجلسة:** `{session_name}`\n"
        sessions_list += f"**• البوت:** @{me.username}\n"
        sessions_list += f"**• عدد الرسائل المخزنة:** `{len(session_data['forwarding_map'])}`\n\n"
    
    await edit_or_reply(event, sessions_list)

@l313l.ar_cmd(
    pattern="مسح الجلسات$",
    command=("مسح الجلسات", plugin_category),
    info={
        "header": "لـ مسح جميع الجلسات",
        "الاستـخـدام": "{tr}مسح الجلسات",
    },
)
async def clear_all_sessions(event):
    "لـ مسح جميع الجلسات"
    if not user_sessions:
        return await edit_or_reply(event, "**⎉╎لا توجد جلسات نشطة حالياً**")
    
    # إيقاف جميع الجلسات
    for session_name in list(user_sessions.keys()):
        try:
            await user_sessions[session_name]['client'].disconnect()
            del user_sessions[session_name]
        except Exception as e:
            print(f"خطأ في إيقاف الجلسة {session_name}: {e}")
    
    await edit_or_reply(event, "**⎉╎تم مسح جميع الجلسات بنجاح 🗑️**")
