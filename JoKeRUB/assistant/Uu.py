from telethon import Button, events
from telethon.tl.types import MessageEntityTextUrl, MessageEntityCustomEmoji
from . import l313l
from ..helpers import reply_id

@l313l.bot_cmd(
    pattern="^/start$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def start_command(event):
    """نسخة مطابقة لـ python-telegram-bot"""
    
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    # نفس الرسالة حرفياً
    message = "🎉 <b>تم بنجاح!</b>\n"
    
    # محاولة الإيموجي البريميوم - الطريقة التي تعمل مع Telethon
    # استخدم <a href="emoji/ID"> بدل <tg-emoji emoji-id="ID">
    message += f'<a href="emoji/5368324170671202286">🔥</a>\n\n'
    message += "للتواصل مع المطور:"
    
    # زر واحد للمطور
    buttons = [
        [Button.url("👤 تواصل مع المطور", "https://t.me/lx5x5")]
    ]
    
    # إرسال الرسالة
    await event.client.send_message(
        chat.id,
        message,
        parse_mode='html',
        buttons=buttons,
        reply_to=reply_to,
        link_preview=False
    )

# ==========================================================
# إذا لم تعمل الطريقة الأولى، جرب هذه الطرق البديلة:
# ==========================================================

@l313l.bot_cmd(
    pattern="^/start2$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def start_method2(event):
    """الطريقة الثانية - باستخدام MessageEntity مباشرة"""
    
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    # النص بدون HTML
    message_text = "🎉 تم بنجاح!\n🔥\n\nللتواصل مع المطور:"
    
    # إنشاء entities يدوياً
    from telethon.tl.types import MessageEntityBold, MessageEntityCustomEmoji
    
    entities = [
        # جعل "تم بنجاح!" عريض
        MessageEntityBold(offset=2, length=9),
        # إضافة إيموجي بريميوم
        MessageEntityCustomEmoji(
            offset=len("🎉 تم بنجاح!\n"),
            length=len("🔥"),
            document_id=5368324170671202286
        )
    ]
    
    buttons = [
        [Button.url("👤 تواصل مع المطور", "https://t.me/lx5x5")]
    ]
    
    await event.client.send_message(
        chat.id,
        message_text,
        entities=entities,
        buttons=buttons,
        reply_to=reply_to
    )

@l313l.bot_cmd(
    pattern="^/start3$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def start_method3(event):
    """الطريقة الثالثة - محاكاة كاملة"""
    
    chat = await event.get_chat()
    
    # إذا كان الإيموجي البريميوم لا يعمل، استخدم هذا الحل:
    
    # الحل 1: استخدام صورة بدلاً من إيموجي
    try:
        # أولاً أرسل الرسالة النصية
        message = "🎉 <b>تم بنجاح!</b>\n\nللتواصل مع المطور:"
        
        buttons = [
            [Button.url("👤 تواصل مع المطور", "https://t.me/lx5x5")]
        ]
        
        await event.client.send_message(
            chat.id,
            message,
            parse_mode='html',
            buttons=buttons
        )
        
        # ثم أرسل الإيموجي كرسالة منفصلة
        await event.client.send_message(
            chat.id,
            "🔥",  # إيموجي عادي
            parse_mode='html'
        )
        
    except Exception as e:
        # الحل 2: استخدام Unicode إيموجي مميز
        message = "🎉 <b>تم بنجاح!</b>\n"
        message += "🔥\n\n"  # إيموجي Unicode عادي
        message += "للتواصل مع المطور:"
        
        buttons = [
            [Button.url("👤 تواصل مع المطور", "https://t.me/lx5x5")]
        ]
        
        await event.client.send_message(
            chat.id,
            message,
            parse_mode='html',
            buttons=buttons
        )

# ==========================================================
# دالة لتشخيص المشكلة
# ==========================================================

@l313l.bot_cmd(
    pattern="^/checkemoji$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def check_emoji_problem(event):
    """تشخيص مشكلة الإيموجي البريميوم"""
    
    chat = await event.get_chat()
    
    # اختبار 1: إيموجي عادي
    await event.reply("🔥 إيموجي عادي (يجب أن يعمل)")
    
    # اختبار 2: إيموجي بريميوم بطريقة Telethon
    try:
        await event.client.send_message(
            chat.id,
            '<a href="emoji/5368324170671202286">🔥</a> إيموجي بريميوم',
            parse_mode='html'
        )
        await event.reply("✅ الإيموجي البريميوم يعمل!")
    except Exception as e:
        await event.reply(f"❌ فشل الإيموجي البريميوم:\n{str(e)}")
    
    # اختبار 3: معرف إذا كان البوت بريميوم
    try:
        bot_entity = await event.client.get_entity("me")
        if hasattr(bot_entity, 'premium'):
            await event.reply(f"🔍 حالة البوت:\nPremium: {bot_entity.premium}")
        else:
            await event.reply("🔍 لا يمكن التحقق من حالة البوت")
    except Exception as e:
        await event.reply(f"🔍 خطأ في التحقق: {str(e)}")

# ==========================================================
# الحل النهائي: استخدام إيموجيات خاصة بدلاً من البريميوم
# ==========================================================

@l313l.bot_cmd(
    pattern="^/finalstart$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def final_solution(event):
    """الحل النهائي - أفضل بديل"""
    
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    # استخدام إيموجيات Unicode مميزة بدلاً من البريميوم
    message = "✨ <b>تم بنجاح!</b>\n"
    
    # إيموجيات Unicode مميزة (ليست بريميوم ولكنها جذابة)
    special_emojis = "🔥🌟⭐🎯🎖️🏆💫🎭"
    
    # اختر إيموجي عشوائي
    import random
    selected_emoji = random.choice(special_emojis)
    
    message += f"{selected_emoji}\n\n"
    message += "للتواصل مع المطور:"
    
    buttons = [
        [Button.url("👤 تواصل مع المطور", "https://t.me/lx5x5")]
    ]
    
    await event.client.send_message(
        chat.id,
        message,
        parse_mode='html',
        buttons=buttons,
        reply_to=reply_to,
        link_preview=False
    )

# ==========================================================
# إذا أردت نفس الكود بالضبط مع التعديل البسيط
# ==========================================================

@l313l.bot_cmd(
    pattern="^/exactcopy$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def exact_copy(event):
    """
    أقرب نسخة ممكنة للكود الأصلي
    فقط استبدل <tg-emoji> بـ <a href="emoji/">
    """
    
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    # الكود الأصلي مع تعديل بسيط
    message = "🎉 <b>تم بنجاح!</b>\n"
    
    # في python-telegram-bot: '<tg-emoji emoji-id="5368324170671202286">🔥</tg-emoji>'
    # في Telethon: '<a href="emoji/5368324170671202286">🔥</a>'
    message += '<a href="emoji/5368324170671202286">🔥</a>\n\n'
    
    message += "للتواصل مع المطور:"
    
    # زر واحد للمطور
    keyboard = [[Button.url("👤 تواصل مع المطور", "https://t.me/lx5x5")]]
    
    await event.client.send_message(
        chat.id,
        message,
        parse_mode='html',
        buttons=keyboard,
        reply_to=reply_to
    )
