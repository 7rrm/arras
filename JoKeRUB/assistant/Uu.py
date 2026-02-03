from telethon import Button, events
from telethon.tl.types import MessageEntityTextUrl, MessageEntityCustomEmoji
from . import l313l
from ..helpers import reply_id

# تعريف إيموجي بريميوم للتجربة
PREMIUM_EMOJI_ID = 5368324170671202286  # إيموجي النار 🔥

@l313l.bot_cmd(
    pattern="^/test$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def test_command(event):
    """نسخة مبسطة مع زر واحد - بنفس طريقة كود الأوامر"""
    
    # الحصول على الدردشة والرد
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    # بناء الرسالة بنفس الطريقة تماماً (مثل كود الأوامر)
    message = f'<b>🎉 تم بنجاح!</b>\n'
    
    # إضافة الإيموجي البريميوم بنفس طريقة <a href="emoji/ID">
    message += f'<a href="emoji/{PREMIUM_EMOJI_ID}">🔥</a>\n\n'
    message += "للتواصل مع المطور:"
    
    # زر واحد للمطور
    buttons = [
        [Button.url("👤 تواصل مع المطور", "https://t.me/lx5x5")]
    ]
    
    # إرسال الرسالة
    try:
        await event.client.send_message(
            chat.id,
            message,
            parse_mode='html',
            buttons=buttons,
            reply_to=reply_to,
            link_preview=False
        )
    except Exception as e:
        # نسخة احتياطية
        fallback_message = "🎉 <b>تم بنجاح!</b>\n🔥\n\nللتواصل مع المطور:"
        
        await event.client.send_message(
            chat.id,
            fallback_message,
            parse_mode='html',
            buttons=buttons,
            reply_to=reply_to,
            link_preview=False
        )

# ===================================================================
# نسخة متقدمة تشبه كود الأوامر تماماً
# ===================================================================

@l313l.bot_cmd(
    pattern="^/premium$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def premium_demo(event):
    """عرض متقدم يشبه كود الأوامر"""
    
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    # بناء رسالة متعددة الإيموجيات مثل كود الأوامر
    caption = f'<b>🎭 عرض الإيموجيات البريميوم</b>\n\n'
    
    # سطر من إيموجيات بريميوم متعددة
    caption += (
        f'<a href="emoji/5368324170671202286">🔥</a>'
        f'<a href="emoji/5368324170671202287">👑</a>'
        f'<a href="emoji/5368324170671202288">⚡</a>\n\n'
    )
    
    # قائمة مع إيموجيات بريميوم
    caption += (
        f'<a href="emoji/5368324170671202286">🔥</a> <code>.test</code> ⦙ تجربة الإيموجي البريميوم\n'
        f'<a href="emoji/5368324170671202287">👑</a> <code>.start</code> ⦙ بدء استخدام البوت\n'
        f'<a href="emoji/5368324170671202288">⚡</a> <code>.help</code> ⦙ عرض المساعدة\n\n'
    )
    
    # سطر ختامي مع إيموجيات
    caption += (
        f'<a href="emoji/5368324170671202286">🔥</a>'
        f'<a href="emoji/5368324170671202287">👑</a>'
        f'<a href="emoji/5368324170671202288">⚡</a>\n\n'
    )
    
    caption += f'<b>المطور: @Lx5x5</b>'
    
    buttons = [
        [Button.inline("🎭 تجربة أخرى", data="more_emojis")],
        [Button.url("📞 تواصل مع المطور", "https://t.me/lx5x5")]
    ]
    
    await event.client.send_message(
        chat.id,
        caption,
        parse_mode='html',
        buttons=buttons,
        reply_to=reply_to,
        link_preview=False
    )

# ===================================================================
# نسخة للبوت الخاص (مشابهة لكود الأوامر)
# ===================================================================

@l313l.bot_cmd(
    pattern="^/startbot$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def bot_start_premium(event):
    """نسخة متطورة لبدء البوت مع إيموجيات بريميوم"""
    
    chat = await event.get_chat()
    user = await l313l.get_me()
    reply_to = await reply_id(event)
    
    # معلومات المستخدم
    mention = f"[{chat.first_name}](tg://user?id={chat.id})"
    my_mention = f"[{user.first_name}](tg://user?id={user.id})"
    first = chat.first_name
    last = chat.last_name
    fullname = f"{first} {last}" if last else first
    my_fullname = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
    
    # التحقق إذا كان المستخدم لديه بريميوم
    try:
        user_premium = (await event.client.get_entity(chat.id)).premium
    except:
        user_premium = False
    
    # بناء الرسالة بناءً على حالة البريميوم
    if user_premium or chat.id == 5427469031:  # المطور أو بريميوم
        message = f'<b>🎉 مـرحبـاً بـك عـزيـزي {mention}</b>\n\n'
        
        # إيموجي بريميوم خاص
        if chat.id == 5427469031:  # المطور
            message += f'<a href="emoji/5368324170671202287">👑</a>\n\n'
            message += f'<b>✨ أهـلاً بـك يـا مـالـك الـبـوت</b>\n'
        else:
            message += f'<a href="emoji/5368324170671202286">🔥</a>\n\n'
            message += f'<b>✨ أنـا الـبـوت الـخـاص بـ {my_fullname}</b>\n'
        
        message += (
            f'<a href="emoji/5368324170671202288">⚡</a> يمكنك التواصـل مـع مـالكـي مـن هنـا\n'
            f'<a href="emoji/5368324170671202286">🔥</a> فقـط ارسـل رسـالتك وانتظـر الـرد\n'
            f'<a href="emoji/5368324170671202287">👑</a> إننـي ايضـاً بـوت زخرفـة & حـذف حسابات\n'
            f'<a href="emoji/5368324170671202288">⚡</a> لـ الزخرفـة او الحـذف استخـدم الازرار\n\n'
        )
        
        # سطر من الإيموجيات
        message += (
            f'<a href="emoji/5368324170671202286">🔥</a>'
            f'<a href="emoji/5368324170671202287">👑</a>'
            f'<a href="emoji/5368324170671202288">⚡</a>\n'
        )
    else:
        # نسخة للمستخدمين العاديين
        message = f'<b>🎉 مـرحبـاً بـك عـزيـزي {mention}</b>\n\n'
        message += '🔥\n\n'  # إيموجي عادي
        message += f'<b>✨ أنـا الـبـوت الـخـاص بـ {my_fullname}</b>\n'
        message += (
            f'💌 يمكنك التواصـل مـع مـالكـي مـن هنـا\n'
            f'📨 فقـط ارسـل رسـالتك وانتظـر الـرد\n'
            f'🎨 إننـي ايضـاً بـوت زخرفـة & حـذف حسابات\n\n'
        )
    
    message += f'<b>المطور: @Lx5x5</b>'
    
    # أزرار
    buttons = [
        [Button.inline("🗳 اضغـط لـ التواصـل", data="ttk_bot-1")],
        [Button.inline("🎡 زخـارف تمبلـر", data="decor_main_menu")],
        [Button.inline("⚠️ لـ حـذف حسـابك", data="zzk_bot-5")],
        [Button.inline("💎 الأوامـر المدفوعـة", data="paid_commands_menu")],
        [Button.url("📱 قنـاة المـطور", "https://t.me/lx5x5")]
    ]
    
    await event.client.send_message(
        chat.id,
        message,
        parse_mode='html',
        buttons=buttons,
        reply_to=reply_to,
        link_preview=False
    )

# ===================================================================
# دالة المعالجة لـ CallbackQuery
# ===================================================================

@l313l.tgbot.on(events.CallbackQuery(pattern=r"more_emojis"))
async def handle_more_emojis(event):
    """معالجة زر تجربة أخرى"""
    chat = await event.get_chat()
    
    # رسالة مع إيموجيات بريميوم إضافية
    more_msg = (
        f'<b>🎭 المزيد من الإيموجيات البريميوم:</b>\n\n'
        f'<a href="emoji/5368324170671202286">🔥</a> إيموجي النار البريميوم\n'
        f'<a href="emoji/5368324170671202287">👑</a> إيموجي التاج البريميوم\n'
        f'<a href="emoji/5368324170671202288">⚡</a> إيموجي الصاعقة البريميوم\n\n'
        f'<a href="emoji/5368324170671202286">🔥</a>'
        f'<a href="emoji/5368324170671202287">👑</a>'
        f'<a href="emoji/5368324170671202288">⚡</a>\n\n'
        f'<b>للحصول على إيموجيات بريميوم:</b>\n'
        f'1. اشترك في Telegram Premium\n'
        f'2. أضف الإيموجيات إلى حسابك\n'
        f'3. استخدم الـ ID الخاص بها'
    )
    
    await event.edit(
        more_msg,
        parse_mode='html',
        buttons=[
            [Button.inline("🔙 رجوع", data="back_to_main")],
            [Button.url("🛒 Telegram Premium", "https://t.me/premium")]
        ]
    )

@l313l.tgbot.on(events.CallbackQuery(pattern=r"back_to_main"))
async def handle_back(event):
    """معالجة زر الرجوع"""
    await premium_demo(event)

# ===================================================================
# دالة لاختبار عدة طرق
# ===================================================================

@l313l.bot_cmd(
    pattern="^/emojiways$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def test_emoji_methods(event):
    """اختبار جميع طرق الإيموجيات"""
    
    chat = await event.get_chat()
    
    methods = [
        ("الطريقة 1: <a href>", f'<a href="emoji/5368324170671202286">🔥</a>'),
        ("الطريقة 2: [link]", f'[🔥](tg://emoji?id=5368324170671202286)'),
        ("الطريقة 3: <emoji>", f'<emoji id="5368324170671202286">🔥</emoji>'),
        ("الطريقة 4: إيموجي عادي", "🔥"),
    ]
    
    for title, emoji_code in methods:
        try:
            test_msg = f'<b>{title}</b>\n{emoji_code}\n'
            
            await event.client.send_message(
                chat.id,
                test_msg,
                parse_mode='html' if 'href' in emoji_code or 'emoji' in emoji_code else None,
                link_preview=False
            )
        except Exception as e:
            await event.client.send_message(
                chat.id,
                f'<b>{title} - فشل</b>\n❌ {str(e)[:50]}',
                parse_mode='html'
)
