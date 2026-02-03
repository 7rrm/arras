from telethon import events
from . import l313l
from ..helpers import reply_id

# تعريف إيموجي بريميوم
PREMIUM_EMOJI_ID = 5368324170671202286  # إيموجي النار 🔥

@l313l.bot_cmd(
    pattern="^/test$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def test_command(event):
    """نسخة مبسطة بدون أزرار - فقط الرسالة"""
    
    # الحصول على الدردشة
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    # بناء الرسالة بالضبط مثل المثال
    message = "🎉 <b>تم بنجاح!</b>\n"
    
    # إضافة الإيموجي البريميوم بنفس الطريقة
    message += f'<a href="emoji/{PREMIUM_EMOJI_ID}">🔥</a>\n\n'
    message += "للتواصل مع المطور:"
    
    # إرسال الرسالة بدون أزرار
    await event.client.send_message(
        chat.id,
        message,
        parse_mode='html',
        reply_to=reply_to,
        link_preview=False
    )

# ==========================================================
# نسخة مطابقة 100% للكود المطلوب
# ==========================================================

@l313l.bot_cmd(
    pattern="^/exact$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def exact_match(event):
    """مطابق 100% للكود المطلوب"""
    
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    # نفس الرسالة حرفياً
    message = "🎉 <b>تم بنجاح!</b>\n"
    
    # نفس سطر الإيموجي بالضبط (معدل للـ Telethon)
    message += f'<a href="emoji/{PREMIUM_EMOJI_ID}">🔥</a>\n\n'
    message += "للتواصل مع المطور:"
    
    # إرسال بدون أي إضافات
    await event.client.send_message(
        chat.id,
        message,
        parse_mode='html',
        reply_to=reply_to
    )

# ==========================================================
# نسخة بإيموجيات متعددة
# ==========================================================

@l313l.bot_cmd(
    pattern="^/multi$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def multi_emojis(event):
    """رسالة مع عدة إيموجيات بريميوم"""
    
    chat = await event.get_chat()
    
    message = "🎭 <b>إيموجيات بريميوم:</b>\n\n"
    
    # إيموجيات متعددة
    message += f'<a href="emoji/5368324170671202286">🔥</a> '
    message += f'<a href="emoji/5368324170671202287">👑</a> '
    message += f'<a href="emoji/5368324170671202288">⚡</a>\n\n'
    
    message += "هذه إيموجيات بريميوم خاصة"
    
    await event.client.send_message(
        chat.id,
        message,
        parse_mode='html'
    )

# ==========================================================
# نسخة مع نص عربي
# ==========================================================

@l313l.bot_cmd(
    pattern="^/arabic$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def arabic_message(event):
    """رسالة عربية مع إيموجي بريميوم"""
    
    chat = await event.get_chat()
    
    message = "🎊 <b>تمت العملية بنجاح!</b>\n"
    message += f'<a href="emoji/{PREMIUM_EMOJI_ID}">🔥</a>\n\n'
    message += "مرحباً بك في البوت الخاص بي\n"
    message += "يمكنك التواصل مع المطور عبر الخاص"
    
    await event.client.send_message(
        chat.id,
        message,
        parse_mode='html'
    )

# ==========================================================
# نسخة لاختبار أنواع مختلفة
# ==========================================================

@l313l.bot_cmd(
    pattern="^/simple$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def simple_test(event):
    """أبسط نسخة ممكنة"""
    
    chat = await event.get_chat()
    
    # فقط الإيموجي البريميوم
    message = f'<a href="emoji/{PREMIUM_EMOJI_ID}">🔥</a>'
    
    await event.client.send_message(
        chat.id,
        message,
        parse_mode='html'
    )

@l313l.bot_cmd(
    pattern="^/textonly$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def text_only(event):
    """نص فقط مع إيموجي بريميوم في المنتصف"""
    
    chat = await event.get_chat()
    
    message = "هذا هو النص الأول\n"
    message += f'<a href="emoji/{PREMIUM_EMOJI_ID}">🔥</a>\n'
    message += "هذا هو النص الثاني"
    
    await event.client.send_message(
        chat.id,
        message,
        parse_mode='html'
    )

# ==========================================================
# دالة مساعدة لعرض جميع الإيموجيات
# ==========================================================

@l313l.bot_cmd(
    pattern="^/showemojis$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def show_all_emojis(event):
    """عرض جميع الإيموجيات البريميوم المتاحة"""
    
    chat = await event.get_chat()
    
    # قائمة الإيموجيات البريميوم
    emojis = [
        {"id": 5368324170671202286, "char": "🔥", "desc": "نار بريميوم"},
        {"id": 5368324170671202287, "char": "👑", "desc": "تاج بريميوم"},
        {"id": 5368324170671202288, "char": "⚡", "desc": "صاعقة بريميوم"},
        {"id": 5210763312597326700, "char": "❤️", "desc": "قلب بريميوم"},
    ]
    
    message = "<b>🎨 الإيموجيات البريميوم المتاحة:</b>\n\n"
    
    for emoji in emojis:
        message += f'<a href="emoji/{emoji["id"]}">{emoji["char"]}</a> - {emoji["desc"]}\n'
    
    message += "\n<b>ملاحظة:</b> تأكد أن البوت يملك هذه الإيموجيات"
    
    await event.client.send_message(
        chat.id,
        message,
        parse_mode='html'
    )

# ==========================================================
# رد على الرسائل العادية (اختياري)
# ==========================================================

@l313l.bot_cmd(
    pattern="^مرحبا$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def hello_response(event):
    """رد تلقائي مع إيموجي بريميوم"""
    
    chat = await event.get_chat()
    
    message = f"مرحباً {chat.first_name} 👋\n"
    message += f'<a href="emoji/{PREMIUM_EMOJI_ID}">🔥</a>\n'
    message += "كيف يمكنني مساعدتك؟"
    
    await event.reply(
        message,
        parse_mode='html'
    )

# ==========================================================
# نسخة نهائية تشبه تماماً المطلوب
# ==========================================================

@l313l.bot_cmd(
    pattern="^/final$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def final_version(event):
    """
    النسخة النهائية المطابقة تماماً للطلب
    بدون أزرار - فقط رسالة - فقط إيموجي
    """
    
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    # الرسالة بالضبط كما طلبت
    message = "🎉 <b>تم بنجاح!</b>\n"
    
    # الإيموجي البريميوم
    message += f'<a href="emoji/5368324170671202286">🔥</a>\n\n'
    
    message += "للتواصل مع المطور:"
    
    # الإرسال النهائي
    await event.client.send_message(
        chat.id,
        message,
        parse_mode='html',
        reply_to=reply_to,
        link_preview=False
    )
