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
            # أزرار ملونة
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "🔥 اوامر الادارة 🔥",
                            "callback_data": "admin_commands_test",
                            "style": "primary"
                        }
                    ],
                    [
                        {
                            "text": "✨ اوامر التنظيف ✨",
                            "callback_data": "clean_cmd_test",
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
    # معالج زر اوامر الادارة (باستخدام Telethon)
    # =========================================================== #

    @l313l.tgbot.on(CallbackQuery(data=re.compile(b"admin_commands_test")))
    @check_owner
    async def admin_test(event):
        text = """**👮 أوامر الإدارة**

**☑️ ⦗ `.حظر` ⦘**
❐ لحظر عضو من المجموعة

**☑️ ⦗ `.كتم` ⦘**
❐ لكتم عضو في المجموعة

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙Dev : @Lx5x5"""
        
        buttons = [[Button.inline("↩️ رجوع", data="ZEDHELP")]]
        await event.edit(text, buttons=buttons)

    # =========================================================== #
    # معالج زر اوامر التنظيف (باستخدام Telethon)
    # =========================================================== #

    @l313l.tgbot.on(CallbackQuery(data=re.compile(b"clean_cmd_test")))
    @check_owner
    async def clean_test(event):
        text = """**🧹 أوامر التنظيف**

**☑️ ⦗ `.تنظيف` ⦘**
❐ لحذف عدد معين من الرسائل

**☑️ ⦗ `.مسح` ⦘**
❐ لحذف رسالة محددة

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙Dev : @Lx5x5"""
        
        buttons = [[Button.inline("↩️ رجوع", data="ZEDHELP")]]
        await event.edit(text, buttons=buttons)

    # =========================================================== #
    # القائمة الرئيسية (باستخدام Telethon)
    # =========================================================== #

    @l313l.tgbot.on(CallbackQuery(data=re.compile(b"ZEDHELP")))
    @check_owner
    async def back_to_main(event):
        buttons = [
            [Button.inline("🔥 اوامر الادارة 🔥", data="admin_commands_test")],
            [Button.inline("✨ اوامر التنظيف ✨", data="clean_cmd_test")]
        ]
        await event.edit(HELP, buttons=buttons)
