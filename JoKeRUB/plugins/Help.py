import re
from telethon import Button, events
from telethon.events import CallbackQuery
import json
import requests
from ..core import check_owner
from ..Config import Config
from . import l313l

HELP = """**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي**
**🛂┊في قائمـة المسـاعـده والشـروحـات
🛃┊من هنـا يمكنـك ايجـاد شـرح لكـل اوامـر السـورس**

[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️](https://t.me/lx5x5)

"""

# إيموجي بريميوم
EMOJI_DOWNLOAD = "5933974679269151927"  # 📨
EMOJI_CHECK = "5974491287615706239"      # ✅
EMOJI_TIME = "5839380464116175529"       # 🕖
EMOJI_ARROW = "4931832872081294660"      # 📨

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler(event):
        query = event.text
        
        if query.startswith("مساعدة"):
            # ✅ زر واحد فقط - اوامر التحميل
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "📥 اوامر التحميل 📥",
                            "callback_data": "download_commands",
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

# =========================================================== #
# ⚠️ هذا الجزء أساسي - لا تحذفه ⚠️
# =========================================================== #

@l313l.ar_cmd(pattern="مساعدة$")
async def help(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()

    try:
        await event.get_sender()
        await event.get_chat()
    except Exception as e:
        print(f"تم التحميل: {e}")

    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "مساعدة")
    await response[0].click(event.chat_id)
    await event.delete()

# =========================================================== #
# معالج اوامر التحميل مع ايموجي مميز
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"download_commands")))
@check_owner
async def download_cmd(event):
    text = f'''<tg-emoji emoji-id="{EMOJI_DOWNLOAD}">📨</tg-emoji> <b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التحميل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> <b>⦗ `.يوت` ⦘</b>
❐ البحث عن أغنية
❐ طريقة الاستخدام: <code>.بحث اسم الاغنية</code>

<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> <b>⦗ `.تفعيل يوت` ⦘</b>
❐ لتسمح ب استخدام امر يوت للأشخاص الآخرين
❐ طريقة الاستخدام: <code>.تفعيل يوت</code>

<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> <b>⦗ `.تعطيل يوت` ⦘</b>
❐ لتعطيل استخدام امر يوت 
❐ طريقة الاستخدام: <code>.تعطيل يوت</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> <b>⦗ `.فيديو` ⦘</b>
❐ البحث عن فيديو
❐ طريقة الاستخدام: <code>.بحث اسم الفيديو</code>

<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> <b>⦗ `.تفعيل فيديو` ⦘</b>
❐ لتسمح ب استخدام امر فيديو للأشخاص الآخرين
❐ طريقة الاستخدام: <code>.تفعيل فيديو</code>

<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> <b>⦗ `.تعطيل فيديو` ⦘</b>
❐ لتعطيل استخدام امر فيديو 
❐ طريقة الاستخدام: <code>.تعطيل فيديو</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> <b>⦗ `.فيس` ⦘</b>
❐ تحميل من الفيس بوك
❐ طريقة الاستخدام: <code>.فيس الرابط</code>

<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> <b>⦗ `.تيك` ⦘</b>
❐ تحميل من تيك توك
❐ طريقة الاستخدام: <code>.تيك الرابط</code>

<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> <b>⦗ `.ستوري` ⦘</b>
❐ تحميل ستوري من التلكرام
❐ طريقة الاستخدام: <code>.ستوري الرابط</code>

<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> <b>⦗ `.داون` ⦘</b>
❐ تحميل من جميع مواقع التواصل
❐ طريقة الاستخدام: <code>.داون الرابط</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
<tg-emoji emoji-id="{EMOJI_ARROW}">📨</tg-emoji> <b>Dev : @Lx5x5 🦅</b>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="ZEDHELP")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML")

# =========================================================== #
# زر الرجوع - يعيد الأزرار الملونة
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"ZEDHELP")))
@check_owner
async def back_to_main(event):
    # ✅ رجوع مع أزرار ملونة
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "📥 اوامر التحميل 📥",
                    "callback_data": "download_commands",
                    "style": "primary"
                }
            ]
        ]
    }
    
    try:
        edit_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/editMessageText"
        edit_data = {
            "chat_id": event.chat_id,
            "message_id": event.message_id,
            "text": HELP,
            "parse_mode": "Markdown",
            "reply_markup": json.dumps(keyboard),
            "disable_web_page_preview": True
        }
        requests.post(edit_url, json=edit_data, timeout=3)
    except Exception as e:
        print(f"❌ خطأ في الرجوع: {e}")
        # بديل إذا فشل API
        buttons = [[Button.inline("📥 اوامر التحميل 📥", data="download_commands")]]
        await event.edit(HELP, buttons=buttons)
