import re
from telethon import Button, events
from telethon.events import CallbackQuery
import json
import requests
from ..core import check_owner
from ..Config import Config
from . import l313l

HELP = "**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي**\n**🛂┊في قائمـة المسـاعـده والشـروحـات\n🛃┊من هنـا يمكنـك ايجـاد شـرح لكـل اوامـر السـورس**\n\n[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️](https://t.me/lx5x5)\n\n"

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler(event):
        query = event.text
        
        if query.startswith("مساعدة"):
            # ✅ أزرار ملونة
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "🔥 اوامر الادارة 🔥",
                            "callback_data": "admin_commands",
                            "style": "primary"
                        }
                    ],
                    [
                        {
                            "text": "✨ اوامر التنظيف ✨",
                            "callback_data": "clean_cmd",
                            "style": "success"
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
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "مساعدة")
    await response[0].click(event.chat_id)
    await event.delete()

# =========================================================== #
# معالج الأزرار (بدون ألوان عشان يشتغل بسرعة)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"admin_commands")))
@check_owner
async def admin_cmd(event):
    text = """**👮 أوامر الإدارة**

**☑️ ⦗ `.حظر` ⦘**
❐ لحظر عضو من المجموعة

**☑️ ⦗ `.كتم` ⦘**
❐ لكتم عضو في المجموعة

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙Dev : @Lx5x5"""
    
    buttons = [[Button.inline("↩️ رجوع", data="ZEDHELP")]]
    await event.edit(text, buttons=buttons)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"clean_cmd")))
@check_owner
async def clean_cmd(event):
    text = """**🧹 أوامر التنظيف**

**☑️ ⦗ `.تنظيف` ⦘**
❐ لحذف عدد معين من الرسائل

**☑️ ⦗ `.مسح` ⦘**
❐ لحذف رسالة محددة

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙Dev : @Lx5x5"""
    
    buttons = [[Button.inline("↩️ رجوع", data="ZEDHELP")]]
    await event.edit(text, buttons=buttons)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"ZEDHELP")))
@check_owner
async def back_to_main(event):
    buttons = [
        [Button.inline("🔥 اوامر الادارة 🔥", data="admin_commands")],
        [Button.inline("✨ اوامر التنظيف ✨", data="clean_cmd")]
    ]
    await event.edit(HELP, buttons=buttons)
