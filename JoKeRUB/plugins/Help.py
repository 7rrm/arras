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
                            "text": "‹ : أوامـر البحـث والتحميل : ›",
                            "callback_data": "main_menu",
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
        print(f"تم التحميل: {e}")

    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "مساعدة")
    await response[0].click(event.chat_id)
    await event.delete()

# =========================================================== #
# القائمة الرئيسية
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"main_menu")))
@check_owner
async def main_menu(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة البحـث والتحَميـل
‹ : من هنـا يمكنـك إيجـاد شـرح لكـل أوامـر البحـث والتحَمـيل 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [
        [Button.inline("‹ : أوامـر اليوت والفيديـو( البوت ) : ›", data="youtube_commands")],
        [
            Button.inline("‹ : أوامـر البحـث والفيـديو ( الأنلاين ) : ›", data="inline_search_commands"),
            Button.inline("‹ : أوامـر السوشيال مَيـديا : ›", data="social_commands")
        ],
        [Button.inline("رجــوع ↩️", data="ZEDHELP")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر اليوت والفيديو (البوت)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"youtube_commands")))
@check_owner
async def youtube_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التحميل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.يوت</code> <b>⦘</b>
❐ البحث عن أغنية
❐ <b>طريقة الاستخدام:</b> <code>.بحث اسم الاغنية</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تفعيل يوت</code> <b>⦘</b>
❐ لتسمح ب استخدام امر يوت للأشخاص الآخرين
❐ <b>طريقة الاستخدام:</b> <code>.تفعيل يوت</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تعطيل يوت</code> <b>⦘</b>
❐ لتعطيل استخدام امر يوت
❐ <b>طريقة الاستخدام:</b> <code>.تعطيل يوت</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.فيديو</code> <b>⦘</b>
❐ البحث عن فيديو
❐ <b>طريقة الاستخدام:</b> <code>.بحث اسم الفيديو</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تفعيل فيديو</code> <b>⦘</b>
❐ لتسمح ب استخدام امر فيديو للأشخاص الآخرين
❐ <b>طريقة الاستخدام:</b> <code>.تفعيل فيديو</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تعطيل فيديو</code> <b>⦘</b>
❐ لتعطيل استخدام امر فيديو
❐ <b>طريقة الاستخدام:</b> <code>.تعطيل فيديو</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="main_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر البحث والتحميل (الأنلاين)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"inline_search_commands")))
@check_owner
async def inline_search_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر البحث والتحميل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.بحث</code> <b>⦘</b>
❐ تحميل( صوت / فيديو ) من يوتيوب 
❐ <b>طريقة الاستخدام:</b> <code>.بحث الكلمة أو الرابط</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="main_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر السوشيال ميديا
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"social_commands")))
@check_owner
async def social_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر السوشيال ميديا 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.فيس</code> <b>⦘</b>
❐ تحميل من الفيس بوك
❐ <b>طريقة الاستخدام:</b> <code>.فيس الرابط</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تيك</code> <b>⦘</b>
❐ تحميل من تيك توك
❐ <b>طريقة الاستخدام:</b> <code>.تيك الرابط</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.ستوري</code> <b>⦘</b>
❐ تحميل ستوري من التلكرام
❐ <b>طريقة الاستخدام:</b> <code>.ستوري الرابط</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.داون</code> <b>⦘</b>
❐ تحميل من جميع مواقع التواصل
❐ <b>طريقة الاستخدام:</b> <code>.داون الرابط</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="main_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر البحث والتحميل (الرجوع للقائمة الرئيسية)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"search_commands")))
@check_owner
async def search_commands(event):
    await main_menu(event)

# =========================================================== #
# زر الرجوع النهائي (بدون ألوان)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"ZEDHELP")))
@check_owner
async def back_to_main(event):
    buttons = [[Button.inline("‹ : أوامـر البحـث والتحميل : ›", data="main_menu")]]
    await event.edit(HELP, buttons=buttons, link_preview=False)
