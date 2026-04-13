import re
import json
import requests
from telethon import events
from telethon.events import CallbackQuery
from ..core import check_owner
from ..Config import Config
from . import l313l

HELP = "**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي**\n**🛂┊في قائمـة المسـاعـده والشـروحـات\n🛃┊من هنـا يمكنـك ايجـاد شـرح لكـل اوامـر السـورس**\n\n[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️](https://t.me/lx5x5)\n\n"

# إيموجيات ملونة للأزرار
EMOJI_PRIMARY = "5258215850745275216"      # ✨
EMOJI_SUCCESS = "5411580731929411768"      # ✅
EMOJI_DANGER = "5350477112677515642"       # 🔥
EMOJI_SECONDARY = "5408997493784467607"    # 💎
EMOJI_WARNING = "5188619457651567219"      # ⚠️

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @l313l.tgbot.on(CallbackQuery(data=re.compile(b"test_buttons")))
@check_owner
async def test_buttons(event):
    buttons = [
        [
            {
                "text": "اوامر الادارة 👮",
                "callback_data": "admin_commands",
                "style": "primary",
                "icon_custom_emoji_id": "5258215850745275216"
            }
        ],
        [
            {
                "text": "اوامر التنظيف 🧹",
                "callback_data": "clean_cmd",
                "style": "success",
                "icon_custom_emoji_id": "5411580731929411768"
            }
        ],
        [
            {
                "text": "رجوع ↩️",
                "callback_data": "back_menu",
                "style": "danger",
                "icon_custom_emoji_id": "5350477112677515642"
            }
        ]
    ]
    
    try:
        edit_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/editMessageText"
        edit_data = {
            "chat_id": event.chat_id,
            "message_id": event.message_id,
            "text": "**📍 اختر الأمر الذي تريد معرفته:**",
            "parse_mode": "Markdown",
            "reply_markup": json.dumps({"inline_keyboard": buttons})
        }
        requests.post(edit_url, json=edit_data, timeout=3)
    except Exception as e:
        # fallback
        await event.edit(
            "**📍 اختر الأمر الذي تريد معرفته:**",
            buttons=[
                [Button.inline("اوامر الادارة 👮", data="admin_commands")],
                [Button.inline("اوامر التنظيف 🧹", data="clean_cmd")],
                [Button.inline("رجوع ↩️", data="back_menu")]
            ]
        )
