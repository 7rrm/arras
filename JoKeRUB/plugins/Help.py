import re
from telethon import Button, events
from telethon.events import CallbackQuery
import json
import requests
from ..core import check_owner
from ..Config import Config
from . import l313l

# إيموجي بريميوم
EMOJI_AWAMER = "5667948420749328402"
EMOJI_OWNER = "5046707123942066452"
EMOJI_HEART = "5220157149103023925"

EMOJI_OWNER = "5667948420749328402"

# رسالة الترحيب المبسطة
WELCOME_TEXT = '''**‹ : مـࢪحبـاً عـزيـزي .**
**‹ : للدخول إلى القائمة اضغط على الزر أدناه**

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''

# رسالة HELP الأصلية (تظهر في ZEDHELP)
HELP = '''**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي**
**🛂┊في قائمـة المسـاعـده والشـروحـات
🛃┊من هنـا يمكنـك ايجـاد شـرح لكـل اوامـر السـورس**

[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️](https://t.me/lx5x5)'''

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler(event):
        if event.text.startswith("مساعدة"):
            # زر واحد فقط
            buttons = [
                [Button.inline("📌 اضغط هَنا", data="ZEDHELP", style="primary", icon_custom_emoji_id="5667948420749328402")],
                [Button.url("👨‍💻 المـطـور", "https://t.me/lx5x5", style="danger")],
            ]
            
            await event.answer(
                [await event.builder.article(
                    title="📚 قائمة المساعدة",
                    text=WELCOME_TEXT,
                    buttons=buttons,
                    link_preview=False,
                )],
                cache_time=0
            )

@l313l.ar_cmd(pattern="مساعدة$")
async def help(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()

    try:
        await event.get_sender()
        await event.get_chat()
    except Exception as e:
        pass

    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "مساعدة")
    await response[0].click(event.chat_id)
    await event.delete()

# =========================================================== #
# القائمة الرئيسية (أوامر البحث والتحميل)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"main_menu")))
@check_owner
async def main_menu(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة البحـث والتحَميـل
‹ : من هنـا يمكنـك إيجـاد شـرح لكـل أوامـر البحـث والتحَمـيل 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [
        [Button.inline("‹ : اليوت والفيديـو( البوت ) : ›", data="youtube_commands", style="primary")],
        [
            Button.inline("‹ : البحـث والفيـديو ( الأنلاين ) : ›", data="inline_search_commands", style="primary"),
            Button.inline("‹ : السوشيال مَيـديا : ›", data="social_commands", style="primary")
        ],
        [Button.inline("رجــوع ↩️", data="ZEDHELP", style="danger")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# قائمة السورس (التحديث والتشغيل)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"source_menu")))
@check_owner
async def source_menu(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة التحديث والتشغيل
‹ : من هنـا يمكنـك إيجـاد شـرح لكـل أوامـر التحديثات 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [
        [Button.inline("‹ : التحَـديث : ›", data="update_commands", style="primary")],
        [
            Button.inline("‹ : أعَـادة التشغيل : ›", data="restart_commands", style="primary"),
            Button.inline("‹ : أيـقاف البوت : ›", data="stop_commands", style="primary")
        ],
        [Button.inline("‹ : الفحَـص و سَرعة الأنترنت : ›", data="speed_commands", style="primary")],
        [
            Button.inline("‹ : السَليب : ›", data="sleep_commands", style="primary"),
            Button.inline("‹ : المـطور المَساعـد : ›", data="assistant_dev_commands", style="primary")
        ],
        [Button.inline("رجــوع ↩️", data="ZEDHELP", style="danger")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# قائمة الحساب (الصفحة 1)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"aaccount_menu")))
@check_owner
async def account_menu(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة الحـساب
‹ : من هنـا يمكنـك إيجـاد شـرح لكـل أوامـر الحـساب 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [
        [
            Button.inline("‹ : الأسـم الوقَتـي : ›", data="name_commands", style="primary"),
            Button.inline("‹ : البايـو الوقَتـي : ›", data="bio_commands", style="primary")
        ],
        [Button.inline("‹ : الصـورة الوقتيـة : ›", data="photo_commands", style="primary")],
        [
            Button.inline("‹ : قَـنواتـي : ›", data="channels_commands", style="primary"),
            Button.inline("‹ : كَٕروباتـي : ›", data="groups_commands", style="primary")
        ],
        [Button.inline("‹ : مَـغادرة القَنـوات والمجموعات : ›", data="lleave_commands", style="primary")],
        [Button.inline("‹ : حَـماية الخَـاص : ›", data="privacy_commands", style="primary")],
        [
            Button.inline("‹ : رجــوع ↩️ : ›", data="ZEDHELP", style="danger"),
            Button.inline("‹ : التَالـي : ›", data="account_menu_next", style="success")
        ]
    ]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# زر الرجوع النهائي
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"ZEDHELP")))
@check_owner
async def back_to_main(event):
    buttons = [
        [Button.inline("‹ : البحـث والتحميل : ›", data="main_menu", style="primary")],
        [
            Button.inline("‹ : السـورس : ›", data="source_menu", style="danger"),
            Button.inline("‹ : الحـساب : ›", data="aaccount_menu", style="danger")
        ],
        [Button.inline("‹ : الأذاعَـة : ›", data="broadcast_main_menu", style="primary")],
        [
            Button.inline("‹ : المجموعَـة ➋ : ›", data="group_menu_2", style="danger"),
            Button.inline("‹ : ➊ المجموعَـة : ›", data="group_menu_1", style="danger")
        ]
    ]
    await event.edit(HELP, buttons=buttons, link_preview=False)

# =========================================================== #
# أوامر الاسم الوقتي
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"name_commands")))
@check_owner
async def name_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الاسم 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اسم وقتي</code> <b>⦘</b>
❐ إضافة اسم وقتي في خانة 1
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اسم وقتي2</code> <b>⦘</b>
❐ إضافة اسم وقتي في خانة 2
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.انهاء اسم وقتي</code> <b>⦘</b>
❐ إنهاء الاسم الوقتي 1 و 2 
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اوامر الاسم الوقتي</code> <b>⦘</b>
❐ لـ عرض الاوامر الخاصه ب اسم الوقتي
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="aaccount_menu", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر البايو الوقتي
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"bio_commands")))
@check_owner
async def bio_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر البايو 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.بايو وقتي</code> <b>⦘</b>
❐ إضافة بايو وقتي
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.انهاء البايو الوقتي</code> <b>⦘</b>
❐ إنهاء البايو الوقتي
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="aaccount_menu", style="success")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الصورة الوقتية
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"photo_commands")))
@check_owner
async def photo_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الصورة 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الصورة الوقتية</code> <b>⦘</b>
❐ وضع صورة تتغير مع الوقت
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.انهاء الصورة الوقتية</code> <b>⦘</b>
❐ إنهاء الصورة الوقتية
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="aaccount_menu", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الكروبات
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"groups_commands")))
@check_owner
async def groups_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الكروبات 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.كروباتي مالك</code> <b>⦘</b>
<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.كروباتي ادمن</code> <b>⦘</b>
<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.كروباتي الكل</code> <b>⦘</b>
❐ لـ عرض قوائم بمجموعاتك

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.انشائي</code> <b>⦘</b>
❐ لـ عرض قائمة بمجموعاتك وقنواتك

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="aaccount_menu", style="success")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر القنوات
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"channels_commands")))
@check_owner
async def channels_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر القنوات 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.قنواتي مالك</code> <b>⦘</b>
<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.قنواتي ادمن</code> <b>⦘</b>
<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.قنواتي الكل</code> <b>⦘</b>
❐ لـ عرض قوائم بقنواتك

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.انشائي</code> <b>⦘</b>
❐ لـ عرض قائمة بمجموعاتك وقنواتك

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="aaccount_menu", style="success")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر مغادرة القنوات والمجموعات
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"lleave_commands")))
@check_owner
async def leave_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر المغادرة 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مغادرة القنوات</code> <b>⦘</b>
<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مغادرة الكروبات</code> <b>⦘</b>

❐ لـمغادرة قنواتك ومجموعاتك (ماعدى التي مالكها انت )
❐ إذا أردت دردشة معينة لاتنشمل في التصفية، قم بوضعها في الأرشيف

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="aaccount_menu", style="danger")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر حماية الخاص
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"privacy_commands")))
@check_owner
async def privacy_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الحماية 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الحماية</code> <b>⦘</b>
❐ تفعيل/تعطيل الحماية في الخاص
❐ <b>طريقة الاستخدام:</b> <code>.الحماية تعطيل/تفعيل</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.سماح</code> / <code>.قبول</code> <b>⦘</b>
❐ السماح للشخص بالتكلم في الخاص
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.رفض</code> / <code>.ر</code> <b>⦘</b>
❐ رفض الشخص من الخاص
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.عقوبة الخاص</code> <b>⦘</b>
❐ بالكتم / بالحظر 
❐ لتحديد نوع العقوبة عندما يتجاوز التحذيرات
❐ <b>طريقة الاستخدام:</b> <code>.عقوبة الخاص بالكتم</code> او <code>.عقوبة الخاص بالحظر</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.المقبولين</code> <b>⦘</b>
❐ عرض قائمة المسموح
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح المقبولين</code> <b>⦘</b>
❐ لـ مسح قائمة المسموح
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح حماية الخاص</code> <b>⦘</b>
❐ لمسح جميع المتغيرات التي اضفتها
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.المميز تفعيل</code> <b>⦘</b>
❐ لمنع ارسال المميز في خاصك
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.المميز تعطيل</code> <b>⦘</b>
❐ للسماح ارسال المميز في خاصك
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الخاص تفعيل</code> <b>⦘</b>
❐ لـ فتح الخاص والسماح بالأشخاص بمراسلتك 
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الخاص تعطيل</code> <b>⦘</b>
❐ لـ منع الاشخاص من مراسلتك 
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="aaccount_menu", style="danger")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر التحديث
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"update_commands")))
@check_owner
async def update_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التحديث 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تحديث</code> <b>⦘</b>
❐ التحقق من التحديثات
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تحديث الان</code> <b>⦘</b>
❐ لتحديث السورس
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.التحديثات تشغيل</code> <b>⦘</b>
❐ تشغيل الرسالة التجريبية
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.التحديثات ايقاف</code> <b>⦘</b>
❐ إيقاف الرسالة التجريبية
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر إعادة التشغيل
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"restart_commands")))
@check_owner
async def restart_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر إعادة التشغيل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اعادة التشغيل</code> <b>⦘</b>
❐ إعادة تشغيل البوت
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu", style="success")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر إيقاف البوت
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"stop_commands")))
@check_owner
async def stop_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر إيقاف البوت 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اطفاء</code> <b>⦘</b>
❐ إيقاف تشغيل البوت
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu", style="danger")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر فحص السرعة
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"speed_commands")))
@check_owner
async def speed_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر فحص السرعة 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.سرعة النت</code> <b>⦘</b>
❐ قياس سرعة الانترنت
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.بنك</code> <b>⦘</b>
❐ قياس سرعة البنك
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.فحص</code> <b>⦘</b>
❐ لعرض معلومات التشغيل
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر السليب
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"sleep_commands")))
@check_owner
async def sleep_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر السليب 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.سليب</code> <b>⦘</b>
❐ وضعك في وضع غير المتصل
❐ <b>طريقة الاستخدام:</b> <code>.سليب السبب</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.سليب_ميديا</code> <b>⦘</b>
❐ سليب مع صورة أو متحركة
❐ <b>طريقة الاستخدام:</b> <code>.سليب_ميديا السبب بالرد</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu", style="success")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر المطور المساعد
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"assistant_dev_commands")))
@check_owner
async def assistant_dev_commands(event):
    text = f'''<b>ᯓ اوامــر المطـور المســاعد .</b>

⎉╎قائـمـه اوامـر رفـع المطـور المسـاعـد 🧑🏻‍💻✅ 🦾 : 
- اضغـط ع الامـر للنسـخ ثـم استخـدمهـا بالتـرتيـب 

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.رفع مطور</code> <b>⦘</b>
- لـ رفـع الشخـص مطـور مسـاعـد معـك بالبـوت 

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تنزيل مطور</code> <b>⦘</b>
- لـ تنزيـل الشخـص مطـور مسـاعـد مـن البـوت 

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.المطورين</code> <b>⦘</b>
- لـ عـرض قائمـة بمطـورين البـوت الخـاص بـك 🧑🏻‍💻📑 

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.امر المطور تفعيل</code> <b>⦘</b>
- لـ تفعيـل وضـع المطـورين المسـاعدين 

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.امر المطور تعطيل</code> <b>⦘</b>
- لـ تعطيـل وضـع المطـورين المسـاعدين 

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تحكم كامل</code> <b>⦘</b>
- اعطـاء المطـورين المرفـوعيـن صلاحيـة التحكـم الكـاملـه بالاوامــر ✓ 

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تحكم آمن</code> <b>⦘</b>
- اعطـاء المطـورين المرفـوعيـن صلاحيـة التحكـم الآمـن لـ الاوامــر الامنـه فقـط ✓ 

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تحكم + اسم الامـر</code> <b>⦘</b>
- اعطـاء المطـورين المرفـوعيـن صلاحيـة التحكـم بأمـر واحـد فقـط او عـدة اوامـر معينـه ✓ .. مثـال (<code>.تحكم ايدي</code>) او (<code>.تحكم ايدي فحص كتم</code>)

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ايقاف تحكم كامل</code> <b>⦘</b>
- ايقـاف صلاحيـة التحكـم الكـاملـه بالاوامــر للمطـورين المرفـوعيـن ✓ 

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ايقاف تحكم آمن</code> <b>⦘</b>
- ايقـاف صلاحيـة التحكـم الآمـن لـ الاوامــر الآمنـه للمطـورين المرفـوعيـن ✓ 

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ايقاف تحكم + اسم الامـر</code> <b>⦘</b>
- ايقـاف صلاحيـة التحكـم المعطـاه لـ امـر واحـد فقـط او عـدة اوامـر للمطـورين المرفـوعيـن ✓ .. مثـال (<code>.ايقاف تحكم ايدي</code>) او (<code>.ايقاف تحكم ايدي فحص كتم</code>)

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.التحكم</code> / <code>.التحكم المعطل</code> <b>⦘</b>
- لـ عـرض قائمـة بالاوامـر المسمـوحـه والغيـر مسمـوحـه للمطـوريـن التحكـم فيهـا 🛃🚷 

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)



# =========================================================== #
# أوامر اليوتيوب (البوت)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"youtube_commands")))
@check_owner
async def youtube_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التحميل من يوتيوب 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.يوت</code> <b>⦘</b>
❐ البحث عن أغنية من يوتيوب
❐ <b>طريقة الاستخدام:</b> <code>.يوت اسم الاغنية</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تفعيل يوت</code> <b>⦘</b>
❐ لتسمح ب استخدام امر يوت للأشخاص الآخرين
❐ <b>طريقة الاستخدام:</b> <code>.تفعيل يوت</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تعطيل يوت</code> <b>⦘</b>
❐ لتعطيل استخدام امر يوت
❐ <b>طريقة الاستخدام:</b> <code>.تعطيل يوت</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.فيديو</code> <b>⦘</b>
❐ البحث عن فيديو من يوتيوب
❐ <b>طريقة الاستخدام:</b> <code>.فيديو اسم الفيديو</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تفعيل فيديو</code> <b>⦘</b>
❐ لتسمح ب استخدام امر فيديو للأشخاص الآخرين
❐ <b>طريقة الاستخدام:</b> <code>.تفعيل فيديو</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تعطيل فيديو</code> <b>⦘</b>
❐ لتعطيل استخدام امر فيديو
❐ <b>طريقة الاستخدام:</b> <code>.تعطيل فيديو</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="main_menu", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر البحث والتحميل (أنلاين)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"inline_search_commands")))
@check_owner
async def inline_search_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر البحث والتحميل (أنلاين) 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.بحث</code> <b>⦘</b>
❐ تحميل (صوت / فيديو) من يوتيوب عبر الأنلاين
❐ <b>طريقة الاستخدام:</b> <code>.بحث الكلمة أو الرابط</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="main_menu", style="success")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر السوشيال ميديا
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"social_commands")))
@check_owner
async def social_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر السوشيال ميديا 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.فيس</code> <b>⦘</b>
❐ تحميل فيديو من الفيس بوك
❐ <b>طريقة الاستخدام:</b> <code>.فيس الرابط</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تيك</code> <b>⦘</b>
❐ تحميل فيديو من تيك توك
❐ <b>طريقة الاستخدام:</b> <code>.تيك الرابط</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ستوري</code> <b>⦘</b>
❐ تحميل ستوري من التلكرام
❐ <b>طريقة الاستخدام:</b> <code>.ستوري الرابط</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.داون</code> <b>⦘</b>
❐ تحميل من جميع مواقع التواصل
❐ <b>طريقة الاستخدام:</b> <code>.داون الرابط</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="main_menu", style="success")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# قائمة الحساب التالية (صفحة 2)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"account_menu_next")))
@check_owner
async def account_menu_next(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة الحـساب (صفحة 2)
‹ : من هنـا يمكنـك إيجـاد شـرح لكـل أوامـر الحـساب 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [
        [Button.inline("‹ : أوامـر البروفايـل : ›", data="profile_commands", style="primary")],
        [
            Button.inline("‹ : أحَصائياتي : ›", data="stats_commands", style="primary"),
            Button.inline("‹ : الكشـف : ›", data="detect_commands", style="primary")],
        [Button.inline("‹ : التخَزيـن والمَراقبـة : ›", data="storage_commands", style="primary")],
        [
            Button.inline("‹ : الكـتم : ›", data="mmute_commands", style="primary"),
            Button.inline("‹ : الحَـظر : ›", data="bban_commands", style="primary")
        ],
        [Button.inline("‹ : سَـجل الأسمـاء : ›", data="history_commands", style="primary")],
        [
            Button.inline("‹ : رجــوع ↩️ : ›", data="aaccount_menu", style="danger"),
            Button.inline("‹ : التَالـي : ›", data="account_mmenu_next", style="success")
        ]
    ]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر البروفايل
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"profile_commands")))
@check_owner
async def profile_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر البروفايل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.البايو وضع</code> <b>⦘</b>
<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الصوره وضع</code> <b>⦘</b>
<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الاسم وضع</code> <b>⦘</b>
<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.المعرف وضع</code> <b>⦘</b>

❐ لـ وضع كل من ( بايو ، اسم ، المعرف ، الصوره ) لحسابك
❐ <b>طريقة الاستخدام:</b> الأمر + الاسم ، البايو ، المعرف ( الصورة بالرد )
•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الصوره حذف</code> <b>⦘</b>
❐ لـ حذف صوره حسابك ( تستطيع أرسال رقم الصوره التي في حسابك لحذفها ) 

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الصوره حذف الكل</code> <b>⦘</b>
❐ لـ حذف جميع الصور في حسابك 

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الإحصائيات
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"stats_commands")))
@check_owner
async def stats_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الإحصائيات 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الحساب</code> <b>⦘</b>
❐ لـ عرض معلومات حسابك من دردشاتك قنوات إلخ ...
❐ <b>طريقة الاستخدام:</b> أرسال الامر فقط .

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.معلوماتي</code> <b>⦘</b>
❐ لـ عرض معلومات حسابك بشكل مفصل 
❐ <b>طريقة الاستخدام:</b> أرسل الامر فقط 

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next", style="success")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الكشف
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"detect_commands")))
@check_owner
async def detect_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الكشف 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الايدي</code> <b>⦘</b>
❐ عرض معلومات الكروب
❐ <b>طريقة الاستخدام:</b> أرسل الامر في الكروب

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ايدي</code> <b>⦘</b>
❐ عرض معلومات العضو بشكل مبسط
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ا</code> او <code>.i</code> <b>⦘</b>
❐ عرض معلومات العضو بشكل مبسط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.كشف</code> <b>⦘</b>
❐ عرض معلومات العضو
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.لايك</code> <b>⦘</b>
❐ عرض معلوماتك
❐ <b>طريقة الاستخدام:</b> ارسل الامر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.المعجبين</code> <b>⦘</b>
❐ لـ عرض معجبينك
❐ <b>طريقة الاستخدام:</b> ارسل الامر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح المعجبين</code> <b>⦘</b>
❐ لـ مسح معجبينك
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر التخزين والمراقبة
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"storage_commands")))
@check_owner
async def storage_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التخزين والمراقبة 𓆪</b>
━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.خزن</code> <b>⦘</b>
❐ لحفظ الرسالة في مجموعة التخزين
❐ <b>طريقة الاستخدام:</b> قم بالرد على الرسالة التي تريد حفظها ثم أرسل .خزن

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مراقبة</code> <b>⦘</b>
❐ لبدء مراقبة مستخدم معين في جميع المجموعات المشتركة
❐ <b>طريقة الاستخدام:</b> <code>.مراقبة ايدي_المستخدم او معرفه</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء مراقبة</code> <b>⦘</b>
❐ لإيقاف مراقبة مستخدم معين
❐ <b>طريقة الاستخدام:</b> <code>.الغاء مراقبة ايدي_المستخدم او معرفه</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تفعيل التخزين</code> <b>⦘</b>
❐ لتفعيل تخزين الرسائل من الدردشة الحالية
❐ <b>طريقة الاستخدام:</b> .تفعيل التخزين (يتم كتابته في الدردشة المطلوبة)

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تعطيل التخزين</code> <b>⦘</b>
❐ لتعطيل تخزين الرسائل من الدردشة الحالية
❐ <b>طريقة الاستخدام:</b> .تعطيل التخزين (يتم كتابته في الدردشة المطلوبة)

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تخزين الخاص تفعيل</code> <b>⦘</b>
❐ لتفعيل تخزين رسائل الخاص في مجموعة التخزين
❐ <b>طريقة الاستخدام:</b> .تخزين الخاص تفعيل

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تخزين الخاص تعطيل</code> <b>⦘</b>
❐ لتعطيل تخزين رسائل الخاص في مجموعة التخزين
❐ <b>طريقة الاستخدام:</b> .تخزين الخاص تعطيل

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تخزين الكروبات تفعيل</code> <b>⦘</b>
❐ لتفعيل تخزين التاكات في المجموعات
❐ <b>طريقة الاستخدام:</b> .تخزين الكروبات تفعيل

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تخزين الكروبات تعطيل</code> <b>⦘</b>
❐ لتعطيل تخزين التاكات في المجموعات
❐ <b>طريقة الاستخدام:</b> .تخزين الكروبات تعطيل

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الكتم
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"mmute_commands")))
@check_owner
async def mute_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الكتم 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.كتم</code> <b>⦘</b>
❐ كتم عضو في المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.كتم</code> بالرد على العضو او كتابة يوزره

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء كتم</code> <b>⦘</b>
❐ إلغاء كتم عضو مكتوم
❐ <b>طريقة الاستخدام:</b> <code>.الغاء كتم</code> بالرد على العضو او كتابة يوزره

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.كتم_مؤقت</code> <b>⦘</b>
❐ كتم عضو مؤقتاً لمدة محددة
❐ <b>طريقة الاستخدام:</b> <code>.كتم_مؤقت 1h السبب</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.المكتومين</code> <b>⦘</b>
❐ لـ عرض قائمة المكتومين
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح المكتومين</code> <b>⦘</b>
❐ حذف جميع المكتومين
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next", style="danger")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الحظر
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"bban_command")))
@check_owner
async def ban_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الحظر 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.بلوك</code> <b>⦘</b>
❐ لـ حظر شخص من خاصك
❐ <b>طريقة الاستخدام:</b> <code>.بلوك</code> في محادثة الشخص

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء بلوك</code> <b>⦘</b>
❐ إلغاء حظر الشخص
❐ <b>طريقة الاستخدام:</b> <code>.الغاء حظر</code> بكتابه يوزره

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.حظر</code> <b>⦘</b>
❐ حظر عضو من المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.حظر</code> بالرد على العضو

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء حظر</code> <b>⦘</b>
❐ إلغاء حظر عضو محظور
❐ <b>طريقة الاستخدام:</b> <code>.الغاء حظر</code> بالرد على العضو

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next", style="danger")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر سجل الأسماء
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"history_commands")))
@check_owner
async def history_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر سجل الاسماء 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الاسماء</code> <b>⦘</b>
❐ لـ عرض قائمة بجميع أسماء الشخص السابقه 
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص او كتابة الايدي الخاص به 

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# قائمة الحساب التالية (صفحة 3)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"account_mmenu_next")))
@check_owner
async def account_menu_nextt(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة الحـساب (صفحة 3)
‹ : من هنـا يمكنـك إيجـاد شـرح لكـل أوامـر الحـساب 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [
        [
            Button.inline("‹ : التقليـد : ›", data="fake_commands", style="primary"),
            Button.inline("‹ : الأنتحَـال : ›", data="spoof_commands", style="primary")
        ],
        [Button.inline("‹ : الأذاعَـة : ›", data="broadcast_commands2", style="primary")],
        [
            Button.inline("‹ : المحَظورين : ›", data="blocked_commands", style="primary"),
            Button.inline("‹ : حَذف دردشـة : ›", data="delete_chat_commands", style="primary")
        ],
        [
            Button.inline("‹ : رجــوع ↩️ : ›", data="account_menu_next", style="danger")
        ]
    ]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر التقليد
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"fake_commands")))
@check_owner
async def fake_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التقليد 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تقليد</code> <b>⦘</b>
❐ تقليد جميع رسائل الشخص
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء التقليد</code> <b>⦘</b>
❐ إيقاف تقليد الشخص
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.المقلدهم</code> <b>⦘</b>
❐ عرض قائمة الأشخاص المقلدهم
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح المقلدهم</code> <b>⦘</b>
❐ مسح قائمة المقلدهم
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_mmenu_next", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الانتحال
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"spoof_commands")))
@check_owner
async def spoof_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الانتحال 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.انتحال</code> <b>⦘</b>
❐ نسخ حساب شخص بالكامل
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اعادة</code> <b>⦘</b>
❐ إرجاع الحساب إلى وضعه الطبيعي
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.انتحال_الدردشه</code> <b>⦘</b>
❐ انتحال دردشة معينة
❐ <b>طريقة الاستخدام:</b> <code>.انتحال_الدردشه معرف</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اعادة_الدردشه</code> <b>⦘</b>
❐ إرجاع الدردشة إلى وضعها الطبيعي
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_mmenu_next", style="danger")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الاذاعة (صفحة الحساب)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"broadcast_commands2")))
@check_owner
async def broadcast_commands2(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الإذاعة 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الاذاعه</code> <b>⦘</b>
❐ لعَرض أوامر الاذاعة
❐ <b>طريقة الاستخدام:</b> <code>.الاذاعه</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_mmenu_next", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر المحظورين
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"blocked_commands")))
@check_owner
async def blocked_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر المحظورين 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الحاظرهم</code> <b>⦘</b>
❐ لـ عرض الاشخاص إلي حاضرهم في حسابك

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح الحاظرهم</code> <b>⦘</b>
❐ لـ مسح جميع المحظورين في حسابك

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح المحظورين</code> <b>⦘</b>
❐ لرفع الحظر عن جميع الأعضاء المحظورين في القناة
❐ ملاحظة: هذا الأمر للقنوات فقط ويتطلب صلاحيات المشرف

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.حذف المحظورين</code> <b>⦘</b>
❐ لمسح وإلغاء حظر جميع الحسابات المحظورة في المجموعة
❐ ملاحظة: هذا الأمر للمجموعات فقط ويتطلب صلاحيات المشرف

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_mmenu_next", style="danger")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر حذف الدردشة
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"delete_chat_commands")))
@check_owner
async def delete_chat_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الحذف 𓆪</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.احذف</code> <b>⦘</b>
❐ لحذف الدردشة مع أي شخص من الطرفين في الخاص
❐ <b>طريقة الاستخدام:</b> <code>.احذف + معرف الشخص</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_mmenu_next", style="danger")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# قائمة الأذاعة الرئيسية
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"broadcast_main_menu")))
@check_owner
async def broadcast_main_menu(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الإذاعة 𓆪</b>
━━━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الاذاعه</code> <b>⦘</b>
❐ لعرض قائمة أوامر الإذاعة المتاحة
❐ <b>طريقة الاستخدام:</b> <code>.الاذاعه</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.للكروبات</code> / <code>.للمجموعات</code> <b>⦘</b>
❐ لإذاعة رسالة أو ميديا لجميع المجموعات التي أنت موجود فيها
❐ <b>طريقة الاستخدام:</b> قم بالرد على الرسالة أو الوسائط ثم أرسل <code>.للكروبات</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.للخاص</code> <b>⦘</b>
❐ لإذاعة رسالة أو ميديا لجميع الأشخاص في الخاص
❐ <b>طريقة الاستخدام:</b> قم بالرد على الرسالة أو الوسائط ثم أرسل <code>.للخاص</code>
❐ ملاحظة: يمكنك تحديد عدد محدد (<code>.للخاص + عدد</code>) لآخر أشخاص حسب العدد لديك بالخاص

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.خاص</code> <b>⦘</b>
❐ لإرسال رسالة إلى شخص محدد بدون الدخول للخاص
❐ <b>طريقة الاستخدام:</b> <code>.خاص + معرف الشخص + الرسالة</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.للكل</code> <b>⦘</b>
❐ لإذاعة رسالة لجميع أعضاء المجموعة الحالية
❐ <b>طريقة الاستخدام:</b> قم بالرد على الرسالة أو الوسائط داخل المجموعة ثم أرسل <code>.للكل</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ايقاف للكل</code> <b>⦘</b>
❐ لإيقاف إذاعة <code>.للكل</code> الجارية في نفس المجموعة فقط
❐ <b>طريقة الاستخدام:</b> <code>.ايقاف للكل</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="ZEDHELP", style="danger")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# قائمة المجموعة الرئيسية (صفحة 1)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"group_menu_1")))
@check_owner
async def group_menu_1(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة المجموعـة (صفحة 1)
‹ : من هنـا يمكنـك إيجـاد شـرح لكـل أوامـر المجموعـة 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [
        [Button.inline("‹ : تـاگ/ all : ›", data="tag_commands", style="primary"),
         Button.inline("‹ : الرابط : ›", data="link_commands", style="primary")],
        [Button.inline("‹ : الأشـراف : ›", data="admin_commands_group", style="primary")],
        [Button.inline("‹ : رسائلي/ رسائله : ›", data="my_msgs_commands", style="primary"),
         Button.inline("‹ : اسمي/اسمه : ›", data="my_name_commands", style="primary")],
        [Button.inline("‹ : مسح رسـائلي/رسائله : ›", data="del_my_msgs_commands", style="primary")],
        [Button.inline("‹ : الأحـداث : ›", data="events_commands", style="primary"),
         Button.inline("‹ : المعلومات : ›", data="info_commands", style="primary")],
        [Button.inline("‹ : الأعضـاء : ›", data="members_commands", style="primary"),
         Button.inline("‹ : المشرفين : ›", data="admins_list_commands", style="primary"),
         Button.inline("‹ : البوتـات : ›", data="bots_commands", style="primary")],
        [Button.inline("‹ : تغَيير الصورة : ›", data="group_photo_commands", style="primary"),
         Button.inline("‹ : التثبيت : ›", data="pin_commands", style="primary")],
        [Button.inline("‹ : المَحذوفين : ›", data="deleted_accounts_commands", style="primary"),
         Button.inline("‹ : مسح المحَظورين : ›", data="unban_all_commands", style="primary")],
        [Button.inline("رجــوع ↩️", data="ZEDHELP", style="danger")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر التاك والمنشن
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"tag_commands")))
@check_owner
async def tag_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر المنشن والتاك 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تاك</code> / <code>.all</code> <b>⦘</b>
❐ لعمل تاك لجميع أعضاء المجموعة 
❐ يرسل 5 أشخاص في كل رسالة
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على رسالة: <code>.تاك</code>
   - مع نص: <code>.تاك وينكم</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ايقاف التاك</code> <b>⦘</b>
❐ لإيقاف عملية التاك الجارية في المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.ايقاف التاك</code>
•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اذكر</code> <b>⦘</b>
❐ لجلب اسم الشخص بشكل ماركدون (منشن)
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على شخص: <code>.اذكر</code>
   - مع معرف الشخص: <code>.اذكر @username</code>
   - مع ايدي الشخص: <code>.اذكر 123456789</code>
•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.منشن</code> <b>⦘</b>
❐ لمنشن جميع أعضاء المجموعة مع رسالة محددة
❐ يرسل كل شخص في رسالة منفصلة (مقطع)
❐ <b>طريقة الاستخدام:</b> <code>.منشن + الرسالة المطلوبة</code>
❐ مثال: <code>.منشن مرحباً بالجميع</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء منشن</code> <b>⦘</b>
❐ لإلغاء عملية المنشن الجارية في المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.الغاء منشن</code>
•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.منشن_كل_5دقايق</code> <b>⦘</b>
❐ لمنشن جميع أعضاء المجموعة كل 5 دقائق مع كليشات عشوائية من القناة
❐ <b>طريقة الاستخدام:</b> <code>.منشن_كل_5دقايق + الرسالة</code>
❐ ملاحظة: يجب أن تكون القناة عامة أو البوت عضو فيها

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء_منشن_كل_5دقايق</code> <b>⦘</b>
❐ لإلغاء عملية المنشن التلقائي الجارية
❐ <b>طريقة الاستخدام:</b> <code>.الغاء_منشن_كل_5دقايق</code>
•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الرابط
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"link_commands")))
@check_owner
async def link_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الرابط 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الرابط</code> <b>⦘</b>
❐ للحصول ع رابط المجموعة او القناة
❐ <b>طريقة الاستخدام:</b> <code>.الرابط</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الاشراف (الرفع والتنزيل)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"admin_commands_group")))
@check_owner
async def admin_commands_group(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الرفع والتنزيل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.رفع مشرف</code> <b>⦘</b>
❐ لرفع عضو إلى مشرف بصلاحيات محدودة
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على الشخص: <code>.رفع مشرف</code>
   - مع معرف الشخص: <code>.رفع مشرف @username</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تنزيل مشرف</code> <b>⦘</b>
❐ لتنزيل مشرف من رتبته
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على المشرف: <code>.تنزيل مشرف</code>
   - مع معرف المشرف: <code>.تنزيل مشرف @username</code>
•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.رفع مالك</code> <b>⦘</b>
❐ لرفع عضو إلى مشرف بكل الصلاحيات ( ليس تحويل الملكية )
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على الشخص: <code>.رفع مالك</code>
   - مع معرف الشخص: <code>.رفع مالك @username</code>
•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.رفع م عام</code> <b>⦘</b>
❐ لرفع مستخدم مشرف عام في جميع المجموعات التي أنت أدمن فيها
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على الشخص: <code>.رفع م عام</code>
   - مع ايدي المستخدم: <code>.رفع م عام 123456789</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تنزيل م عام</code> <b>⦘</b>
❐ لتنزيل مستخدم من المشرف العام في جميع المجموعات
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على الشخص: <code>.تنزيل م عام</code>
   - مع ايدي المستخدم: <code>.تنزيل م عام 123456789</code>
•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اخفاء</code> <b>⦘</b>
❐ لرفع عضو إلى مشرف مع تفعيل خاصية الإخفاء (المنشن التخفي)
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على الشخص: <code>.اخفاء</code>
   - مع معرف الشخص: <code>.اخفاء @username</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر رسائلي / رسائله
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"my_msgs_commands")))
@check_owner
async def my_msgs_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر عرض الرسائل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.رسائلي</code> <b>⦘</b>
❐ لعرض عدد رسائلك في المجموعة
❐ <b>طريقة الاستخدام:</b> 
   - <code>.رسائلي</code> (يتم كتابته داخل المجموعة)

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.رسائله</code> <b>⦘</b>
❐ لعرض عدد رسائل شخص معين في المجموعة
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على الشخص: <code>.رسائله</code>
   - مع معرف الشخص: <code>.رسائله @username</code>
   - مع ايدي الشخص: <code>.رسائله 123456789</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر اسمي / اسمه
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"my_name_commands")))
@check_owner
async def my_name_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر عرض الأسماء 𓆪</b>
━━━━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اسمي</code> <b>⦘</b>
❐ لعرض اسمك في المجموعة
❐ <b>طريقة الاستخدام:</b> 
   - <code>.اسمي</code> (يتم كتابته داخل المجموعة)

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اسمه</code> <b>⦘</b>
❐ لعرض اسم شخص معين في المجموعة
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على الشخص فقط: <code>.اسمه</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر مسح رسائلي
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"del_my_msgs_commands")))
@check_owner
async def del_my_msgs_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر حذف الرسائل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح رسائلي</code> <b>⦘</b>
❐ لحذف جميع رسائلك في الخاص أو المجموعة
❐ <b>طريقة الاستخدام:</b> 
   - في المجموعة: <code>.مسح رسائلي</code>
   - في الخاص: <code>.مسح رسائلي</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح رسائله</code> <b>⦘</b>
❐ لحذف جميع رسائل الشخص في الخاص أو المجموعة
❐ <b>طريقة الاستخدام:</b> 
   - في المجموعة بالرد: <code>.مسح رسائله</code>
   - في الخاص بالرد: <code>.مسح رسائله</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الأحداث
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"events_commands")))
@check_owner
async def events_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الأحداث 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الاحداث</code> <b>⦘</b>
❐ لجلب آخر الرسائل المحذوفة من الأحداث بالعدد المطلوب
❐ <b>طريقة الاستخدام:</b> <code>.الاحداث &lt;عدد&gt;</code>
❐ مثال: <code>.الاحداث 7</code>
❐ ملاحظة: أقصى عدد هو 15

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الاحداث م</code> <b>⦘</b>
❐ لجلب آخر رسائل الميديا المحذوفة من الأحداث بالعدد المطلوب
❐ <b>طريقة الاستخدام:</b> <code>.الاحداث م &lt;عدد&gt;</code>
❐ مثال: <code>.الاحداث م 7</code>

📌 ملاحظة: الأوامر للمجموعات فقط وتتطلب صلاحيات المشرف

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر المعلومات
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"info_commands")))
@check_owner
async def info_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - معلومات المجموعة 𓆪</b>
━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.معلومات</code> <b>⦘</b>
❐ لعرض معلومات المجموعة بشكل مفصل
❐ <b>طريقة الاستخدام:</b> <code>.معلومات</code> (يتم كتابته داخل المجموعة)

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الأعضاء
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"members_commands")))
@check_owner
async def members_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الأعضاء 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الاعضاء</code> <b>⦘</b>
❐ لعرض قائمة أعضاء المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.الاعضاء</code> (يتم كتابته داخل المجموعة)

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.احصائيات الاعضاء</code> <b>⦘</b>
❐ لعرض إحصائيات الأعضاء في المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.احصائيات الاعضاء</code> (يتم كتابته داخل المجموعة)

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر المشرفين
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"admins_list_commands")))
@check_owner
async def admins_list_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر المشرفين 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.المشرفين</code> <b>⦘</b>
❐ لعرض قائمة مشرفين المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.المشرفين</code> (يتم كتابته داخل المجموعة)

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر البوتات
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"bots_commands")))
@check_owner
async def bots_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر البوتات 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.البوتات</code> <b>⦘</b>
❐ لعرض قائمة البوتات الموجودة في المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.البوتات</code> (يتم كتابته داخل المجموعة)

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.البوتات طرد</code> <b>⦘</b>
❐ لطرد جميع البوتات الموجودة في المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.البوتات طرد</code> (يتم كتابته داخل المجموعة)

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر تغيير صورة المجموعة
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"group_photo_commands")))
@check_owner
async def group_photo_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر صورة المجموعة 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الصورة وضع</code> <b>⦘</b>
❐ لوضع صورة للمجموعة
❐ <b>طريقة الاستخدام:</b> قم بالرد على الصورة ثم أرسل <code>.الصورة وضع</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الصورة حذف</code> <b>⦘</b>
❐ لحذف صورة المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.الصورة حذف</code>

📌 ملاحظة: الأوامر للمجموعات فقط وتتطلب صلاحيات المشرف

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر التثبيت
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"pin_commands")))
@check_owner
async def pin_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التثبيت 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تثبيت</code> <b>⦘</b>
❐ لتثبيت رسالة في المجموعة
❐ <b>طريقة الاستخدام:</b> قم بالرد على الرسالة ثم أرسل <code>.تثبيت</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تثبيت بالاشعار</code> <b>⦘</b>
❐ لتثبيت رسالة في المجموعة مع إرسال إشعار للجميع
❐ <b>طريقة الاستخدام:</b> قم بالرد على الرسالة ثم أرسل <code>.تثبيت بالاشعار</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء تثبيت</code> <b>⦘</b>
❐ لإلغاء تثبيت رسالة محددة في المجموعة
❐ <b>طريقة الاستخدام:</b> قم بالرد على الرسالة ثم أرسل <code>.الغاء تثبيت</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء تثبيت الكل</code> <b>⦘</b>
❐ لإلغاء تثبيت جميع الرسائل في المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.الغاء تثبيت الكل</code>

📌 ملاحظة: الأوامر للمجموعات فقط وتتطلب صلاحيات المشرف

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الحسابات المحذوفة
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"deleted_accounts_commands")))
@check_owner
async def deleted_accounts_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الحسابات المحذوفة 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.المحذوفين</code> <b>⦘</b>
❐ لعرض الحسابات المحذوفة في المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.المحذوفين</code> (يتم كتابته داخل المجموعة)

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.المحذوفين اطردهم</code> <b>⦘</b>
❐ لطرد جميع الحسابات المحذوفة من المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.المحذوفين اطردهم</code> (يتم كتابته داخل المجموعة)

📌 ملاحظة: الأوامر للمجموعات فقط وتتطلب صلاحيات المشرف

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر مسح المحظورين
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"unban_all_commands")))
@check_owner
async def unban_all_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الحظر والمحظورين 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.حذف المحظورين</code> <b>⦘</b>
❐ لمسح وإلغاء حظر جميع الحسابات المحظورة في المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.حذف المحظورين</code>

📌 ملاحظة: الأوامر للمجموعات فقط وتتطلب صلاحيات المشرف

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_1", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)


# =========================================================== #
# قائمة المجموعة 2
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"group_menu_2")))
@check_owner
async def group_menu_2(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة المجموعـة (صفحة 2)
‹ : من هنـا يمكنـك إيجـاد شـرح لكـل أوامـر المجموعـة 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [
        [Button.inline("‹ : الحَـظـر : ›", data="ban_commands_group", style="primary"),
         Button.inline("‹ : الكـتـم : ›", data="mute_commands_group", style="primary")],
        [Button.inline("‹ : الطَـرد : ›", data="kick_commands", style="primary"),
         Button.inline("‹ : التقييد : ›", data="restrict_commands", style="primary")],
        [Button.inline("‹ : المـغَـادرة : ›", data="leave_commands_group", style="primary")],
        [Button.inline("‹ : مكافَـح التكرار : ›", data="antiflood_commands", style="primary"),
         Button.inline("‹ : المنـع : ›", data="block_commands", style="primary")],
        [Button.inline("‹ : الأضافـة والتفليش : ›", data="add_flood_commands", style="primary"),
         Button.inline("‹ : التنظيف : ›", data="clean_commands", style="primary")],
        [Button.inline("‹ : الترحَـيب : ›", data="welcome_commands", style="primary")],
        [Button.inline("‹ : الـردود : ›", data="replay_commands", style="primary"),
         Button.inline("‹ : التـحَذيرات : ›", data="warn_commands", style="primary")],
        [Button.inline("رجــوع ↩️", data="ZEDHELP", style="danger")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الحظر (المجموعة)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"ban_commands_group")))
@check_owner
async def ban_commands_group(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الحظر 𓆪</b>
━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.حظر</code> <b>⦘</b>
❐ لحظر عضو في المجموعة
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على الشخص: <code>.حظر</code>
   - مع معرف الشخص: <code>.حظر @username</code>
   - مع ايدي الشخص: <code>.حظر 123456789</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء حظر</code> <b>⦘</b>
❐ لإلغاء حظر عضو في المجموعة
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على الشخص: <code>.الغاء حظر</code>
   - مع معرف الشخص: <code>.الغاء حظر @username</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.حظر_مؤقت</code> <b>⦘</b>
❐ لحظر عضو لمدة زمنية محددة
❐ <b>طريقة الاستخدام:</b> <code>.حظر_مؤقت</code> + بالرد على الشخص + المدة + سبب
❐ مثال: <code>.حظر_مؤقت 2d سبب الحظر</code>
❐ وحدات الوقت: s (ثانية)، m (دقيقة)، h (ساعة)، d (يوم)، w (أسبوع)
•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ح عام</code> <b>⦘</b>
❐ لحظر عضو في جميع المجموعات التي أنت مشرف فيها
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على الشخص: <code>.ح عام</code>
   - مع معرف الشخص: <code>.ح عام @username</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء ح عام</code> <b>⦘</b>
❐ لإلغاء الحظر العام عن عضو
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على الشخص: <code>.الغاء ح عام</code>
   - مع معرف الشخص: <code>.الغاء ح عام @username</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.العام</code> <b>⦘</b>
❐ لعرض قائمة المحظورين عام
❐ <b>طريقة الاستخدام:</b> <code>.العام</code>

📌 ملاحظة: أوامر الحظر والطرد للمجموعات فقط وتتطلب صلاحيات المشرف

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_2", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الطرد
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"kick_commands")))
@check_owner
async def kick_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الطرد 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.طرد</code> <b>⦘</b>
❐ لطرد شخص من المجموعة (ليس حظر)
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص او + معرف/ايدي

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ط عام</code> <b>⦘</b>
❐ لطرد شخص من جميع المجموعات التي أنت مشرف فيها
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص او + معرف/ايدي

📌 ملاحظة: أوامر الحظر والطرد للمجموعات فقط وتتطلب صلاحيات المشرف

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_2", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الكتم (المجموعة)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"mute_commands_group")))
@check_owner
async def mute_commands_group(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الكتم 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.كتم</code> <b>⦘</b>
❐ كتم عضو في المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.كتم</code> بالرد على العضو او كتابة يوزره

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء كتم</code> <b>⦘</b>
❐ إلغاء كتم عضو مكتوم
❐ <b>طريقة الاستخدام:</b> <code>.الغاء كتم</code> بالرد على العضو او كتابة يوزره

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.كتم_مؤقت</code> <b>⦘</b>
❐ كتم عضو مؤقتاً لمدة محددة
❐ <b>طريقة الاستخدام:</b> <code>.كتم_مؤقت 1h السبب</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.المكتومين</code> <b>⦘</b>
❐ لـ عرض قائمة المكتومين
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح المكتومين</code> <b>⦘</b>
❐ حذف جميع المكتومين
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_2", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر التقييد
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"restrict_commands")))
@check_owner
async def restrict_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التقييد 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تقييد</code> <b>⦘</b>
❐ لتقييد عضو في المجموعة (منع الإرسال)
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص او + معرف/ايدي

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء تقييد</code> <b>⦘</b>
❐ لإلغاء تقييد عضو في المجموعة
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص او + معرف/ايدي

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تقييد_مؤقت</code> <b>⦘</b>
❐ لتقييد عضو لمدة زمنية محددة
❐ <b>طريقة الاستخدام:</b> <code>.تقييد_مؤقت</code> + بالرد على الشخص + المدة + سبب
❐ مثال: <code>.تقييد_مؤقت 2d سبب التقييد</code>
❐ وحدات الوقت: s (ثانية)، m (دقيقة)، h (ساعة)، d (يوم)، w (أسبوع)

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_2", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر المغادرة (المجموعة)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"leave_commands_group")))
@check_owner
async def leave_commands_group(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر المغادرة 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اطردني</code> <b>⦘</b>
❐ لمغادرة المجموعة تلقائياً
❐ <b>طريقة الاستخدام:</b> إرسال الأمر في المجموعة

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_2", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر مكافحة التكرار
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"antiflood_commands")))
@check_owner
async def antiflood_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر مكافحة التكرار 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ضع تكرار</code> <b>⦘</b>
❐ لوضع عدد الرسائل المسموح بتكرارها
❐ <b>طريقة الاستخدام:</b> <code>.ضع تكرار + عدد</code>
❐ مثال: <code>.ضع تكرار 5</code>

❐ ملاحظة: لتعطيل الميزة استخدم <code>.ضع تكرار 99999</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_2", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر المنع
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"block_commands")))
@check_owner
async def block_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر المنع 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.منع</code> <b>⦘</b>
❐ لمنع كلمة أو ملصق أو صورة متحركة
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على رسالة نصية: <code>.منع</code>
   - بالرد على ملصق: <code>.منع</code>
   - كتابة الكلمة: <code>.منع كلمة</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء منع</code> <b>⦘</b>
❐ لإلغاء منع كلمة أو ملصق
❐ <b>طريقة الاستخدام:</b> 
   - بالرد على رسالة: <code>.الغاء منع</code>
   - كتابة الكلمة: <code>.الغاء منع كلمة</code>
•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.قائمة المنع</code> <b>⦘</b>
❐ لعرض قائمة الكلمات والملصقات الممنوعة
❐ <b>طريقة الاستخدام:</b> <code>.قائمة المنع</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح قائمة المنع</code> <b>⦘</b>
❐ لمسح جميع الكلمات الممنوعة
❐ <b>طريقة الاستخدام:</b> <code>.مسح قائمة المنع</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_2", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الإضافة والتفليش
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"add_flood_commands")))
@check_owner
async def add_flood_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التفليش 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تفليش بالطرد</code> <b>⦘</b>
❐ طرد جميع أعضاء المجموعة
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تفليش</code> <b>⦘</b>
❐ حظر جميع أعضاء المجموعة
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء تفليش</code> <b>⦘</b>
❐ لألغاء التفليش
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.حظر_الكل</code> <b>⦘</b>
❐ حظر الكل عن طريق بوت الحماية
❐ بدون صلاحيات إشراف

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.طرد_الكل</code> <b>⦘</b>
❐ طرد الكل عن طريق بوت الحماية
❐ بدون صلاحيات إشراف

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.كتم_الكل</code> <b>⦘</b>
❐ كتم الكل عن طريق بوت الحماية
❐ بدون صلاحيات إشراف
•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ضيف</code> <b>⦘</b>
❐ إضافة أعضاء من مجموعة أخرى
❐ <b>طريقة الاستخدام:</b> <code>.ضيف رابط المجموعة</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_2", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر التنظيف والمسح
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"clean_commands")))
@check_owner
async def clean_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التنظيف والمسح 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح</code> <b>⦘</b>
❐ لحذف الرسالة المقروء عليها
❐ <b>طريقة الاستخدام:</b> بالرد على رسالة + <code>.مسح</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تنظيف</code> <b>⦘</b>
❐ حذف عدد معين من الرسائل
❐ <b>طريقة الاستخدام:</b> <code>.تنظيف 10</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تنظيف -ح</code> <b>⦘</b>
❐ تنظيف حسب النوع

<b>الاضافات:</b>
- (-ب): حذف الرسائل الصوتية
- (-م): حذف الملفات
- (-ح): حذف المتحركة
- (-ص): حذف الصور
- (-غ): حذف الأغاني
- (-ق): حذف الملصقات
- (-ر): حذف الروابط
- (-ف): حذف الفيديوهات

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_2", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الترحيب
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"welcome_commands")))
@check_owner
async def welcome_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الترحيب 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الترحيب1</code> <b>⦘</b>
❐ نظام ترحيب بواسطة البوت في المجموعة
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تفعيل ترحيب الايدي</code> <b>⦘</b>
❐ لتفعيل الترحيب بكليشات مختلفة
❐ <b>طريقة الاستخدام:</b> <code>.تفعيل ترحيب الايدي</code> داخل المجموعة

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تعطيل ترحيب الايدي</code> <b>⦘</b>
❐ لتعطيل ترحيب الايدي
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ترحيب</code> <b>⦘</b>
❐ لوضع ترحيب للأعضاء الجدد
❐ <b>طريقة الاستخدام:</b> <code>.ترحيب اهلاً وسهلاً</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.حذف الترحيب</code> <b>⦘</b>
❐ لحذف جميع الترحيبات
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الترحيب</code> <b>⦘</b>
❐ لعرض الترحيبات الحالية
❐ <b>طريقة الاستخدام:</b> إرسال الأمر في المجموعة

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الترحيب السابق</code> <b>⦘</b>
❐ لتشغيل/إيقاف آخر ترحيب
❐ <b>طريقة الاستخدام:</b> <code>.الترحيب السابق تشغيل/ايقاف</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.رحب</code> <b>⦘</b>
❐ لترحيب في الخاص عند الانضمام
❐ <b>طريقة الاستخدام:</b> <code>.رحب مرحباً بك</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.حذف رحب</code> <b>⦘</b>
❐ لحذف الترحيب في الخاص
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_2", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر التحذيرات
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"warn_commands")))
@check_owner
async def warn_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التحذيرات 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تحذير</code> <b>⦘</b>
❐ تحذير عضو مع سبب
❐ <b>طريقة الاستخدام:</b> <code>.تحذير السبب</code> بالرد

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.التحذيرات</code> <b>⦘</b>
❐ عرض تحذيرات العضو
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح التحذيرات</code> <b>⦘</b>
❐ حذف تحذيرات العضو
❐ <b>طريقة الاستخدام:</b> بالرد على الشخص

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_2", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الردود
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"replay_commands")))
@check_owner
async def replay_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الردود 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.رد</code> <b>⦘</b>
❐ إضافة رد تلقائي
❐ <b>طريقة الاستخدام:</b> مثال <code>.رد سلام عليكم</code> بالرد على رساله <code>وعليكم السلام</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح رد</code> <b>⦘</b>
❐ لـ حذف رد معيين 
❐ <b>طريقة الاستخدام:</b> ارسل الامر + الرد إلي تريد تحذفه

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الردود</code> <b>⦘</b>
❐ عرض قائمة الردود الحالية
❐ <b>طريقة الاستخدام:</b> في المجموعة

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.مسح الردود</code> <b>⦘</b>
❐ حذف جميع الردود المضافة
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="group_menu_2", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)
