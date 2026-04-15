import re
from telethon import Button, events
from telethon.events import CallbackQuery
import json
import requests
from ..core import check_owner
from ..Config import Config
from . import l313l

HELP = '''**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي**
**🛂┊في قائمـة المسـاعـده والشـروحـات
🛃┊من هنـا يمكنـك ايجـاد شـرح لكـل اوامـر السـورس**

[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️](https://t.me/lx5x5)

'''

# إيموجي بريميوم
EMOJI_AWAMER = "5667948420749328402"   # قبل كل امر
EMOJI_OWNER = "5046707123942066452"    # عند اسم المطور
EMOJI_HEART = "5220157149103023925"    # قلب

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler(event):
        query = event.text
        
        if query.startswith("مساعدة"):
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "‹ : البحـث والتحميل : ›",
                            "callback_data": "main_menu",
                            "style": "danger"
                        }
                    ],
                    [
                        {
                            "text": "‹ : السـورس : ›",
                            "callback_data": "source_menu",
                            "style": "primary"
                        },
                        {
                            "text": "‹ : الحـساب : ›",
                            "callback_data": "account_menu",
                            "style": "primary"
                        }
                    ],
                    [
                        {
                            "text": "‹ : الأذاعَـة : ›",
                            "callback_data": "broadcast_main_menu",
                            "style": "danger"
                        }
                    ]
                        
                ]
            }
            
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            inline_data = {
                "inline_query_id": event.id,
                "results": json.dumps([
                    {
                        "type": "article",
                        "id": "help_menu_1",
                        "title": "📚 قائمة المساعدة - آراس",
                        "description": "اضغط لعرض الأوامر",
                        "input_message_content": {
                            "message_text": HELP,
                            "parse_mode": "Markdown",
                            "disable_web_page_preview": True
                        },
                        "reply_markup": keyboard
                    }
                ]),
                "cache_time": 0,
                "is_personal": True
            }
            
            try:
                requests.post(url, json=inline_data)
            except Exception as e:
                print(f"❌ خطأ: {e}")

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
            Button.inline("‹ : البحـث والفيـديو ( الأنلاين ) : ›", data="inline_search_commands", style="success"),
            Button.inline("‹ : السوشيال مَيـديا : ›", data="social_commands", style="success")
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
            Button.inline("‹ : أعَـادة التشغيل : ›", data="restart_commands", style="success"),
            Button.inline("‹ : أيـقاف البوت : ›", data="stop_commands", style="danger")
        ],
        [Button.inline("‹ : الفحَـص و سَرعة الأنترنت : ›", data="speed_commands", style="primary")],
        [
            Button.inline("‹ : السَليب : ›", data="sleep_commands", style="success"),
            Button.inline("‹ : المـطور المَساعـد : ›", data="assistant_dev_commands", style="primary")
        ],
        [Button.inline("رجــوع ↩️", data="ZEDHELP", style="danger")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# قائمة الحساب (الصفحة 1)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"account_menu")))
@check_owner
async def account_menu(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة الحـساب
‹ : من هنـا يمكنـك إيجـاد شـرح لكـل أوامـر الحـساب 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [
        [
            Button.inline("‹ : الأسـم الوقَتـي : ›", data="name_commands", style="primary"),
            Button.inline("‹ : البايـو الوقَتـي : ›", data="bio_commands", style="success")
        ],
        [Button.inline("‹ : الصـورة الوقتيـة : ›", data="photo_commands", style="primary")],
        [
            Button.inline("‹ : قَـنواتـي : ›", data="channels_commands", style="success"),
            Button.inline("‹ : كَٕروباتـي : ›", data="groups_commands", style="success")
        ],
        [Button.inline("‹ : مَـغادرة القَنـوات والمجموعات : ›", data="leave_commands", style="danger")],
        [Button.inline("‹ : حَـماية الخَـاص : ›", data="privacy_commands", style="danger")],
        [
            Button.inline("‹ : رجــوع ↩️ : ›", data="ZEDHELP", style="primary"),
            Button.inline("‹ : التَالـي : ›", data="account_menu_next", style="primary")
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
        [Button.inline("‹ : البحـث والتحميل : ›", data="main_menu", style="danger")],
        [
            Button.inline("‹ : السـورس : ›", data="source_menu", style="primary"),
            Button.inline("‹ : الحـساب : ›", data="account_menu", style="primary")
        ],
        [Button.inline("‹ : الأذاعَـة : ›", data="broadcast_main_menu", style="danger")]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu", style="primary")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu", style="success")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu", style="primary")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu", style="success")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu", style="success")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر مغادرة القنوات والمجموعات
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"leave_commands")))
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu", style="danger")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu", style="danger")]]
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
