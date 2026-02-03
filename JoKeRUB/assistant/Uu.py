from telethon import Button, events
from . import l313l
from ..helpers import reply_id
import html
from markdown import markdown

# تعريف إيموجي بريميوم
PREMIUM_EMOJI_ID = 5368324170671202286  # إيموجي النار 🔥

@l313l.bot_cmd(
    pattern="^/test$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def test_command(event):
    """نسخة مبسطة مطابقة تماماً للكود المطلوب"""
    
    # الحصول على الدردشة
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    # بناء الرسالة بنفس الطريقة تماماً
    message = "🎉 <b>تم بنجاح!</b>\n"
    
    # الطريقة الأولى: باستخدام tg://emoji (تعمل مع Markdown)
    message += f"[🔥](tg://emoji?id={PREMIUM_EMOJI_ID})\n\n"
    message += "للتواصل مع المطور:"
    
    # زر واحد للمطور - مطابق للكود الأصلي
    buttons = [
        [Button.url("👤 تواصل مع المطور", "https://t.me/lx5x5")]
    ]
    
    # إرسال الرسالة - الطريقة الأولى (Markdown)
    try:
        await event.client.send_message(
            chat.id,
            message,
            parse_mode='md',  # استخدام Markdown
            buttons=buttons,
            reply_to=reply_to,
            link_preview=False
        )
    except Exception as e:
        # إذا فشلت، جرب الطريقة الثانية
        
        # الطريقة الثانية: HTML مع emoji tag
        message_html = (
            "🎉 <b>تم بنجاح!</b>\n"
            f'<emoji id="{PREMIUM_EMOJI_ID}">🔥</emoji>\n\n'
            "للتواصل مع المطور:"
        )
        
        try:
            await event.client.send_message(
                chat.id,
                message_html,
                parse_mode='html',  # استخدام HTML
                buttons=buttons,
                reply_to=reply_to,
                link_preview=False
            )
        except Exception as e2:
            # الطريقة الثالثة: إيموجي عادي
            message_fallback = "🎉 <b>تم بنجاح!</b>\n🔥\n\nللتواصل مع المطور:"
            
            await event.client.send_message(
                chat.id,
                message_fallback,
                parse_mode='html',
                buttons=buttons,
                reply_to=reply_to,
                link_preview=False
            )

# ===================================================================
# نسخة خاصة لتجربة الإيموجي فقط
# ===================================================================

@l313l.bot_cmd(
    pattern="^/fire$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def test_fire_emoji(event):
    """تجربة إيموجي النار البريميوم فقط"""
    
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    # إرسال الإيموجي البريميوم فقط بطريقتين
    
    # الطريقة 1: Markdown
    try:
        await event.client.send_message(
            chat.id,
            f"[🔥](tg://emoji?id={PREMIUM_EMOJI_ID})",
            parse_mode='md',
            reply_to=reply_to
        )
    except:
        # الطريقة 2: مع نص إضافي
        await event.client.send_message(
            chat.id,
            f"🔥 الإيموجي البريميوم:\n[🔥](tg://emoji?id={PREMIUM_EMOJI_ID})",
            parse_mode='md',
            reply_to=reply_to
        )

# ===================================================================
# نسخة مطابقة 100% للكود المطلوب مع /start
# ===================================================================

@l313l.bot_cmd(
    pattern="^/starttest$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def start_test_command(event):
    """مطابق 100% للكود المطلوب"""
    
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    # بنفس بناء الرسالة بالضبط
    message = "🎉 <b>تم بنجاح!</b>\n"
    
    # نفس سطر الإيموجي (مع تعديل بسيط للـ Telegram)
    message += f'<emoji id="{PREMIUM_EMOJI_ID}">🔥</emoji>\n\n'
    message += "للتواصل مع المطور:"
    
    # نفس الزر بالضبط
    keyboard = [
        [Button.url("👤 تواصل مع المطور", "https://t.me/lx5x5")]
    ]
    
    # نفس طريقة الإرسال
    await event.client.send_message(
        chat.id,
        message,
        parse_mode='html',  # HTML بدل Markdown للإيموجي
        buttons=keyboard,
        reply_to=reply_to
    )

# ===================================================================
# نسخة مختلطة تعمل مع كل الحالات
# ===================================================================

@l313l.bot_cmd(
    pattern="^/emojitest$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def emoji_test_all_methods(event):
    """تجربة جميع طرق إرسال الإيموجي"""
    
    chat = await event.get_chat()
    
    # اختبار 1: Markdown مع tg://emoji
    await event.client.send_message(
        chat.id,
        "**الطريقة 1: Markdown**\n[🔥](tg://emoji?id=5368324170671202286)",
        parse_mode='md'
    )
    
    # اختبار 2: HTML مع emoji tag
    await event.client.send_message(
        chat.id,
        "**الطريقة 2: HTML**\n<emoji id=\"5368324170671202286\">🔥</emoji>",
        parse_mode='html'
    )
    
    # اختبار 3: نص عادي مع إيموجي
    await event.client.send_message(
        chat.id,
        "**الطريقة 3: نص عادي**\n🔥",
        parse_mode=None
    )

# ===================================================================
# دالة تساعد في الحصول على ID الإيموجيات
# ===================================================================

@l313l.bot_cmd(
    pattern="^/getemojis$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def get_emoji_ids(event):
    """الحصول على معلومات الإيموجيات البريميوم"""
    
    chat = await event.get_chat()
    
    info = (
        "**🎭 معلومات الإيموجيات البريميوم:**\n\n"
        f"**🔥 إيموجي النار:**\n"
        f"```\ntg://emoji?id=5368324170671202286\n```\n"
        f"**استخدامه في Markdown:**\n"
        f"```\n[🔥](tg://emoji?id=5368324170671202286)\n```\n"
        f"**استخدامه في HTML:**\n"
        f"```html\n<emoji id=\"5368324170671202286\">🔥</emoji>\n```\n\n"
        "**📋 مثال كامل:**\n"
        "```python\n"
        'message = "🎉 <b>تم بنجاح!</b>\\n"\n'
        'message += f\'<emoji id=\"5368324170671202286\">🔥</emoji>\\n\\n\'\n'
        'message += "للتواصل مع المطور:"\n'
        "```"
    )
    
    await event.client.send_message(
        chat.id,
        info,
        parse_mode='md'
    )
