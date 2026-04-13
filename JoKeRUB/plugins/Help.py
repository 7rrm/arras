from telethon import events
from telethon.events import CallbackQuery
import json
import requests
import re
from ..Config import Config
from ..core import check_owner
from . import l313l

HELP_TEXT = "**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي**\n**🛂┊قائمـة المسـاعـده (نسخة تجريبية)**\n\n[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️](https://t.me/lx5x5)\n\n"

# إيموجيات ملونة
FIRE_EMOJI = "5368324170671202286"      # 🔥
STAR_EMOJI = "5258215850745275216"      # ✨

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    
    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler(event):
        query = event.text
        user_id = event.query.user_id
        
        if query.startswith("مساعدة"):
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "🔥 اوامر الادارة 🔥",
                            "callback_data": "admin_commands_test",
                            "style": "primary",
                            "icon_custom_emoji_id": FIRE_EMOJI
                        }
                    ],
                    [
                        {
                            "text": "✨ اوامر التنظيف ✨",
                            "callback_data": "clean_cmd_test",
                            "style": "success",
                            "icon_custom_emoji_id": STAR_EMOJI
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
                print(f"❌ خطأ: {e}")

    # =========================================================== #
    # معالج الزر الأول: اوامر الادارة
    # =========================================================== #
    
    @l313l.tgbot.on(CallbackQuery(data=re.compile(b"admin_commands_test")))
    @check_owner
    async def admin_commands_handler(event):
        buttons = [
            [
                {
                    "text": "🔥 امر الحظر",
                    "callback_data": "ban_cmd_detail",
                    "style": "danger",
                    "icon_custom_emoji_id": FIRE_EMOJI
                },
                {
                    "text": "✨ امر الكتم",
                    "callback_data": "mute_cmd_detail",
                    "style": "primary",
                    "icon_custom_emoji_id": STAR_EMOJI
                }
            ],
            [
                {
                    "text": "↩️ رجوع",
                    "callback_data": "back_to_help",
                    "style": "secondary",
                    "icon_custom_emoji_id": FIRE_EMOJI
                }
            ]
        ]
        
        try:
            edit_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/editMessageText"
            edit_data = {
                "chat_id": event.chat_id,
                "message_id": event.message_id,
                "text": "**👮 أوامر الإدارة**\n\nاختر الأمر الذي تريد معرفة شرحه:",
                "parse_mode": "Markdown",
                "reply_markup": json.dumps({"inline_keyboard": buttons})
            }
            requests.post(edit_url, json=edit_data, timeout=3)
        except Exception as e:
            print(f"❌ خطأ: {e}")

    # =========================================================== #
    # شرح امر الحظر
    # =========================================================== #
    
    @l313l.tgbot.on(CallbackQuery(data=re.compile(b"ban_cmd_detail")))
    @check_owner
    async def ban_cmd_detail(event):
        text = """**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أمر الحظر 𓆪**
━━━━━━━━━━━━━━━━━━━━

**☑️ ⦗ `.حظر` ⦘**
❐ لحظر عضو من المجموعة
❐ طريقة الاستخدام: `.حظر` بالرد على العضو او كتابة يوزره

**☑️ ⦗ `.الغاء حظر` ⦘**
❐ لإلغاء حظر عضو محظور
❐ طريقة الاستخدام: `.الغاء حظر` بالرد على العضو

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙Dev : @Lx5x5"""
        
        buttons = [
            [
                {
                    "text": "↩️ رجوع لأوامر الادارة",
                    "callback_data": "admin_commands_test",
                    "style": "secondary",
                    "icon_custom_emoji_id": FIRE_EMOJI
                }
            ],
            [
                {
                    "text": "🏠 القائمة الرئيسية",
                    "callback_data": "back_to_help",
                    "style": "primary",
                    "icon_custom_emoji_id": STAR_EMOJI
                }
            ]
        ]
        
        try:
            edit_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/editMessageText"
            edit_data = {
                "chat_id": event.chat_id,
                "message_id": event.message_id,
                "text": text,
                "parse_mode": "Markdown",
                "reply_markup": json.dumps({"inline_keyboard": buttons})
            }
            requests.post(edit_url, json=edit_data, timeout=3)
        except Exception as e:
            print(f"❌ خطأ: {e}")

    # =========================================================== #
    # شرح امر الكتم
    # =========================================================== #
    
    @l313l.tgbot.on(CallbackQuery(data=re.compile(b"mute_cmd_detail")))
    @check_owner
    async def mute_cmd_detail(event):
        text = """**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أمر الكتم 𓆪**
━━━━━━━━━━━━━━━━━━━━

**☑️ ⦗ `.كتم` ⦘**
❐ لكتم عضو في المجموعة
❐ طريقة الاستخدام: `.كتم` بالرد على العضو

**☑️ ⦗ `.الغاء كتم` ⦘**
❐ لإلغاء كتم عضو مكتوم
❐ طريقة الاستخدام: `.الغاء كتم` بالرد على العضو

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙Dev : @Lx5x5"""
        
        buttons = [
            [
                {
                    "text": "↩️ رجوع لأوامر الادارة",
                    "callback_data": "admin_commands_test",
                    "style": "secondary",
                    "icon_custom_emoji_id": STAR_EMOJI
                }
            ],
            [
                {
                    "text": "🏠 القائمة الرئيسية",
                    "callback_data": "back_to_help",
                    "style": "primary",
                    "icon_custom_emoji_id": FIRE_EMOJI
                }
            ]
        ]
        
        try:
            edit_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/editMessageText"
            edit_data = {
                "chat_id": event.chat_id,
                "message_id": event.message_id,
                "text": text,
                "parse_mode": "Markdown",
                "reply_markup": json.dumps({"inline_keyboard": buttons})
            }
            requests.post(edit_url, json=edit_data, timeout=3)
        except Exception as e:
            print(f"❌ خطأ: {e}")
