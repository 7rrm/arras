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
        [Button.inline("‹ : اليوت والفيديـو( البوت ) : ›", data="youtube_commands")],
        [
            Button.inline("‹ : البحـث والفيـديو ( الأنلاين ) : ›", data="inline_search_commands"),
            Button.inline("‹ : السوشيال مَيـديا : ›", data="social_commands")
        ],
        [Button.inline("رجــوع ↩️", data="ZEDHELP")]
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
        [Button.inline("‹ : التحَـديث : ›", data="update_commands")],
        [
            Button.inline("‹ : أعَـادة التشغيل : ›", data="restart_commands"),
            Button.inline("‹ : أيـقاف البوت : ›", data="stop_commands")
        ],
        [Button.inline("‹ : الفحَـص و سَرعة الأنترنت : ›", data="speed_commands")],
        [
            Button.inline("‹ : السَليب : ›", data="sleep_commands"),
            Button.inline("‹ : المـطور المَساعـد : ›", data="assistant_dev_commands")
        ],
        [Button.inline("رجــوع ↩️", data="ZEDHELP")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# قائمة الحساب
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
            Button.inline("‹ : الأسـم الوقَتـي : ›", data="name_commands"),
            Button.inline("‹ : البايـو الوقَتـي : ›", data="bio_commands")
        ],
        [Button.inline("‹ : الصـورة الوقتيـة : ›", data="photo_commands")],
        [
            Button.inline("‹ : قَـنواتـي : ›", data="channels_commands"),
            Button.inline("‹ : كَٕروباتـي : ›", data="groups_commands")
        ],
        [Button.inline("‹ : مَـغادرة القَنـوات والمجموعات : ›", data="leave_commands")],
        [Button.inline("‹ : حَـماية الخَـاص : ›", data="privacy_commands")],
        [
            Button.inline("‹ : رجــوع ↩️ : ›", data="ZEDHELP"),
            Button.inline("‹ : التَالـي : ›", data="account_menu_next")
        ]
    ]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)


# =========================================================== #
# أوامر التحديث (الموجودة مسبقاً)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"update_commands")))
@check_owner
async def update_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التشغيل 𓆪</b>
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
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"restart_commands")))
@check_owner
async def restart_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التشغيل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اعادة التشغيل</code> <b>⦘</b>
❐ إعادة تشغيل البوت
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"stop_commands")))
@check_owner
async def stop_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الاطفاء 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.اطفاء</code> <b>⦘</b>
❐ إيقاف تشغيل البوت
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"speed_commands")))
@check_owner
async def speed_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر المساعدة 𓆪</b>
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
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

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
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

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
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر البحث والتحميل (الموجودة مسبقاً)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"youtube_commands")))
@check_owner
async def youtube_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التحميل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.يوت</code> <b>⦘</b>
❐ البحث عن أغنية
❐ <b>طريقة الاستخدام:</b> <code>.بحث اسم الاغنية</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تفعيل يوت</code> <b>⦘</b>
❐ لتسمح ب استخدام امر يوت للأشخاص الآخرين
❐ <b>طريقة الاستخدام:</b> <code>.تفعيل يوت</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تعطيل يوت</code> <b>⦘</b>
❐ لتعطيل استخدام امر يوت
❐ <b>طريقة الاستخدام:</b> <code>.تعطيل يوت</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.فيديو</code> <b>⦘</b>
❐ البحث عن فيديو
❐ <b>طريقة الاستخدام:</b> <code>.بحث اسم الفيديو</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تفعيل فيديو</code> <b>⦘</b>
❐ لتسمح ب استخدام امر فيديو للأشخاص الآخرين
❐ <b>طريقة الاستخدام:</b> <code>.تفعيل فيديو</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تعطيل فيديو</code> <b>⦘</b>
❐ لتعطيل استخدام امر فيديو
❐ <b>طريقة الاستخدام:</b> <code>.تعطيل فيديو</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="main_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"inline_search_commands")))
@check_owner
async def inline_search_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر البحث والتحميل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.بحث</code> <b>⦘</b>
❐ تحميل( صوت / فيديو ) من يوتيوب 
❐ <b>طريقة الاستخدام:</b> <code>.بحث الكلمة أو الرابط</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="main_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"social_commands")))
@check_owner
async def social_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر السوشيال ميديا 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.فيس</code> <b>⦘</b>
❐ تحميل من الفيس بوك
❐ <b>طريقة الاستخدام:</b> <code>.فيس الرابط</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.تيك</code> <b>⦘</b>
❐ تحميل من تيك توك
❐ <b>طريقة الاستخدام:</b> <code>.تيك الرابط</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.ستوري</code> <b>⦘</b>
❐ تحميل ستوري من التلكرام
❐ <b>طريقة الاستخدام:</b> <code>.ستوري الرابط</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.داون</code> <b>⦘</b>
❐ تحميل من جميع مواقع التواصل
❐ <b>طريقة الاستخدام:</b> <code>.داون الرابط</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="main_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# زر الرجوع النهائي
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"ZEDHELP")))
@check_owner
async def back_to_main(event):
    buttons = [
        [Button.inline("‹ : البحـث والتحميل : ›", data="main_menu")],
        [
            Button.inline("‹ : السـورس : ›", data="source_menu"),
            Button.inline("‹ : الحـساب : ›", data="account_menu")
        ]
    ]
    await event.edit(HELP, buttons=buttons, link_preview=False)

# =========================================================== #
# قائمة الحساب التالية (صفحة 2) - بعد الضغط على "التالي"
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"account_menu_next")))
@check_owner
async def account_menu_next(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة الحـساب (صفحة 2)
‹ : من هنـا يمكنـك إيجـاد شـرح لكـل أوامـر الحـساب 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [
        [Button.inline("‹ : أوامـر البروفايـل : ›", data="profile_commands")],
        [
            Button.inline("‹ : أحَصائياتي : ›", data="stats_commands"),
            Button.inline("‹ : الكشـف : ›", data="detect_commands")
        ],
        [Button.inline("‹ : التخَزيـن والمَراقبـة : ›", data="storage_commands")],
        [
            Button.inline("‹ : الكـتم : ›", data="mute_commands"),
            Button.inline("‹ : الحَـظر : ›", data="ban_commands")
        ],
        [Button.inline("‹ : سَـجل الأسمـاء : ›", data="history_commands")],
        [
            Button.inline("‹ : رجــوع ↩️ : ›", data="account_menu"),
            Button.inline("‹ : التَالـي : ›", data="account_menu_nextt")
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الإحصائيات
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"stats_commands")))
@check_owner
async def stats_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الحساب 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الحساب</code> <b>⦘</b>
❐ لـ عرض معلومات حسابك من دردشاتك قنوات إلخ ...
❐ <b>طريقة الاستخدام:</b> أرسال الامر فقط .

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.معلوماتي</code> <b>⦘</b>
❐ لـ عرض معلومات حسابك بشكل مفصل 
❐ <b>طريقة الاستخدام:</b> أرسل الامر فقط 

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الكتم
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"mute_commands")))
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الحظر
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"ban_commands")))
@check_owner
async def ban_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الحظر 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.حظر</code> <b>⦘</b>
❐ حظر عضو من المجموعة
❐ <b>طريقة الاستخدام:</b> <code>.حظر</code> بالرد على العضو

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.الغاء حظر</code> <b>⦘</b>
❐ إلغاء حظر عضو محظور
❐ <b>طريقة الاستخدام:</b> <code>.الغاء حظر</code> بالرد على العضو

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_next")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# قائمة الحساب التالية (صفحة 3)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"account_menu_nextt")))
@check_owner
async def account_menu_nextt(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة الحـساب (صفحة 3)
‹ : من هنـا يمكنـك إيجـاد شـرح لكـل أوامـر الحـساب 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [
        [
            Button.inline("‹ : التقليـد : ›", data="fake_commands"),
            Button.inline("‹ : الأنتحَـال : ›", data="spoof_commands")
        ],
        [Button.inline("‹ : الأذاعَـة : ›", data="broadcast_commands2")],
        [
            Button.inline("‹ : المحَظورين : ›", data="blocked_commands"),
            Button.inline("‹ : حَذف دردشـة : ›", data="delete_chat_commands")
        ],
        [
            Button.inline("‹ : رجــوع ↩️ : ›", data="account_menu_next")
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_nextt")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_nextt")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الاذاعة
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"broadcast_commands2")))
@check_owner
async def broadcast_commands2(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الإذاعة 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.وجه</code> <b>⦘</b>
❐ إذاعة نص للمجموعات
❐ <b>طريقة الاستخدام:</b> <code>.وجه النص</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">☑️</tg-emoji> <b>⦗</b> <code>.حول</code> <b>⦘</b>
❐ إذاعة نص للخاص
❐ <b>طريقة الاستخدام:</b> <code>.حول النص</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_nextt")]]
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
❐ لـ عرض الاشخص إلي حاضرهم في حسابك


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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_nextt")]]
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
    
    buttons = [[Button.inline("↩️ رجوع", data="account_menu_nextt")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)
