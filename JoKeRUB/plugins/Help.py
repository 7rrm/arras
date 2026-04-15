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

