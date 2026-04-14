from telethon import events, Button 
from telethon.events import CallbackQuery
import json
import requests
import re
from ..Config import Config
from ..core import check_owner
from . import l313l

HELP_TEXT = "**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي**\n**🛂┊قائمـة المسـاعـده (نسخة تجريبية)**\n\n[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️](https://t.me/lx5x5)\n\n"

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    
    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler(event):
        query = event.text
        
        if query.startswith("مساعدة"):
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            
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
            
            inline_data = {
                "inline_query_id": event.id,
                "results": json.dumps([
                    {
                        "type": "article",
                        "id": "help_menu_1",
                        "title": "📚 قائمة المساعدة - آراس",
                        "description": "اضغط لعرض الأوامر المتاحة",
                        "input_message_content": {
                            "message_text": HELP_TEXT,
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
                print(f"❌ خطأ في inline: {e}")

    # =========================================================== #
    # معالج زر اوامر الادارة
    # =========================================================== #
    
    @l313l.tgbot.on(CallbackQuery(data=re.compile(b"admin_commands")))
    @check_owner
    async def admin_commands_handler(event):
        text = """**👮 أوامر الإدارة**

**☑️ ⦗ `.حظر` ⦘**
❐ لحظر عضو من المجموعة

**☑️ ⦗ `.كتم` ⦘**
❐ لكتم عضو في المجموعة

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙Dev : @Lx5x5"""
        
        buttons = [
            [
                {
                    "text": "↩️ رجوع",
                    "callback_data": "back_to_help",
                    "style": "danger"
                }
            ]
        ]
        
        # استخدام event.edit مع buttons عادية
        fallback_buttons = [[Button.inline("↩️ رجوع", data="back_to_help")]]
        
        try:
            # محاولة API
            edit_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/editMessageText"
            edit_data = {
                "chat_id": event.chat_id,
                "message_id": event.message_id,
                "text": text,
                "parse_mode": "Markdown",
                "reply_markup": json.dumps({"inline_keyboard": buttons})
            }
            response = requests.post(edit_url, json=edit_data, timeout=3)
            if response.status_code != 200:
                # فشل API -> استخدم Telethon
                await event.edit(text, buttons=fallback_buttons)
        except Exception as e:
            print(f"❌ خطأ: {e}")
            await event.edit(text, buttons=fallback_buttons)

    # =========================================================== #
    # معالج زر اوامر التنظيف
    # =========================================================== #
    
    @l313l.tgbot.on(CallbackQuery(data=re.compile(b"clean_cmd")))
    @check_owner
    async def clean_commands_handler(event):
        text = """**🧹 أوامر التنظيف**

**☑️ ⦗ `.تنظيف` ⦘**
❐ لحذف عدد معين من الرسائل
❐ طريقة الاستخدام: `.تنظيف 10`

**☑️ ⦗ `.مسح` ⦘**
❐ لحذف رسالة محددة
❐ طريقة الاستخدام: بالرد على الرسالة

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙Dev : @Lx5x5"""
        
        buttons = [
            [
                {
                    "text": "↩️ رجوع",
                    "callback_data": "back_to_help",
                    "style": "danger"
                }
            ]
        ]
        
        fallback_buttons = [[Button.inline("↩️ رجوع", data="back_to_help")]]
        
        try:
            edit_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/editMessageText"
            edit_data = {
                "chat_id": event.chat_id,
                "message_id": event.message_id,
                "text": text,
                "parse_mode": "Markdown",
                "reply_markup": json.dumps({"inline_keyboard": buttons})
            }
            response = requests.post(edit_url, json=edit_data, timeout=3)
            if response.status_code != 200:
                await event.edit(text, buttons=fallback_buttons)
        except Exception as e:
            print(f"❌ خطأ: {e}")
            await event.edit(text, buttons=fallback_buttons)

    # =========================================================== #
    # معالج زر الرجوع
    # =========================================================== #
    
    @l313l.tgbot.on(CallbackQuery(data=re.compile(b"back_to_help")))
    @check_owner
    async def back_to_help_handler(event):
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
        
        fallback_buttons = [
            [Button.inline("🔥 اوامر الادارة 🔥", data="admin_commands")],
            [Button.inline("✨ اوامر التنظيف ✨", data="clean_cmd")]
        ]
        
        try:
            edit_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/editMessageText"
            edit_data = {
                "chat_id": event.chat_id,
                "message_id": event.message_id,
                "text": HELP_TEXT,
                "parse_mode": "Markdown",
                "reply_markup": json.dumps(keyboard),
                "disable_web_page_preview": True
            }
            response = requests.post(edit_url, json=edit_data, timeout=3)
            if response.status_code != 200:
                await event.edit(HELP_TEXT, buttons=fallback_buttons)
        except Exception as e:
            print(f"❌ خطأ: {e}")
            await event.edit(HELP_TEXT, buttons=fallback_buttons)

@l313l.ar_cmd(pattern="مساعدة$")
async def help_cmd(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()
    TG_BOT = Config.TG_BOT_USERNAME
    response = await l313l.inline_query(TG_BOT, "مساعدة")
    await response[0].click(event.chat_id)
    await event.delete()
