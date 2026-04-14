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
            [Button.inline("↩️ رجوع", data="back_to_help")]
        ]
        
        try:
            await event.edit(text, buttons=buttons)
        except Exception as e:
            print(f"❌ خطأ: {e}")

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
            [Button.inline("↩️ رجوع", data="back_to_help")]
        ]
        
        try:
            await event.edit(text, buttons=buttons)
        except Exception as e:
            print(f"❌ خطأ: {e}")

    # =========================================================== #
    # معالج زر الرجوع
    # =========================================================== #
    
    @l313l.tgbot.on(CallbackQuery(data=re.compile(b"back_to_help")))
    @check_owner
    async def back_to_help_handler(event):
        buttons = [
            [Button.inline("🔥 اوامر الادارة 🔥", data="admin_commands")],
            [Button.inline("✨ اوامر التنظيف ✨", data="clean_cmd")]
        ]
        
        try:
            await event.edit(HELP_TEXT, buttons=buttons)
        except Exception as e:
            print(f"❌ خطأ: {e}")

# =========================================================== #
# الأمر الرئيسي مع الدمج
# =========================================================== #

@l313l.ar_cmd(pattern="مساعدة$")
async def help_cmd(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()
    
    chat_id = event.chat_id
    
    # نتحقق إذا كانت محادثة خاصة
    if chat_id < 0:
        # مجموعة - نتحقق من وجود البوت
        try:
            bot_entity = await event.client.get_entity(Config.TG_BOT_USERNAME)
            bot_participant = await event.client.get_permissions(chat_id, bot_entity)
            
            if bot_participant.is_member:
                # ✅ البوت موجود → يرسل أزرار ملونة
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
                
                send_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/sendMessage"
                send_data = {
                    "chat_id": chat_id,
                    "text": HELP_TEXT,
                    "parse_mode": "Markdown",
                    "reply_markup": json.dumps(keyboard),
                    "disable_web_page_preview": True
                }
                requests.post(send_url, json=send_data, timeout=3)
                await event.delete()
            else:
                # ❌ البوت مو موجود → حسابك يرسل أزرار عادية
                buttons = [
                    [Button.inline("🔥 اوامر الادارة 🔥", data="admin_commands")],
                    [Button.inline("✨ اوامر التنظيف ✨", data="clean_cmd")]
                ]
                await event.edit(HELP_TEXT, buttons=buttons)
                
        except Exception:
            # ❌ البوت مو موجود → حسابك يرسل أزرار عادية
            buttons = [
                [Button.inline("🔥 اوامر الادارة 🔥", data="admin_commands")],
                [Button.inline("✨ اوامر التنظيف ✨", data="clean_cmd")]
            ]
            await event.edit(HELP_TEXT, buttons=buttons)
    
    else:
        # محادثة خاصة → حسابك يرسل أزرار عادية
        buttons = [
            [Button.inline("🔥 اوامر الادارة 🔥", data="admin_commands")],
            [Button.inline("✨ اوامر التنظيف ✨", data="clean_cmd")]
        ]
        await event.edit(HELP_TEXT, buttons=buttons)
