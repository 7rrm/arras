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

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler(event):
        query = event.text
        
        if query.startswith("مساعدة"):
            # تصميم الأزرار الملونة
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "اوامر الادارة 👮",
                            "callback_data": "admin_commands",
                            "style": "primary",
                            "icon_custom_emoji_id": EMOJI_PRIMARY
                        }
                    ],
                    [
                        {
                            "text": "اوامر التنظيف 🧹",
                            "callback_data": "clean_cmd",
                            "style": "success",
                            "icon_custom_emoji_id": EMOJI_SUCCESS
                        },
                        {
                            "text": "اوامر المسح 🗑️",
                            "callback_data": "delete_cmd",
                            "style": "danger",
                            "icon_custom_emoji_id": EMOJI_DANGER
                        }
                    ],
                    [
                        {
                            "text": "اوامر الوقت والتاريخ 📅",
                            "callback_data": "time_date_cmd",
                            "style": "secondary",
                            "icon_custom_emoji_id": EMOJI_SECONDARY
                        }
                    ],
                    [
                        {
                            "text": "اوامر الوقتي 🔄",
                            "callback_data": "timely_cmd",
                            "style": "primary",
                            "icon_custom_emoji_id": EMOJI_PRIMARY
                        },
                        {
                            "text": "اوامر الصلاة 🕌",
                            "callback_data": "prayer_cmd",
                            "style": "success",
                            "icon_custom_emoji_id": EMOJI_SUCCESS
                        }
                    ],
                    [
                        {
                            "text": "اوامر المساعدة 🆘",
                            "callback_data": "help_commands",
                            "style": "warning",
                            "icon_custom_emoji_id": EMOJI_WARNING
                        }
                    ],
                    [
                        {
                            "text": "اوامر الروابط 🔗",
                            "callback_data": "link_commands",
                            "style": "secondary",
                            "icon_custom_emoji_id": EMOJI_SECONDARY
                        },
                        {
                            "text": "اوامر الكشف 🔍",
                            "callback_data": "detect_commands",
                            "style": "primary",
                            "icon_custom_emoji_id": EMOJI_PRIMARY
                        }
                    ],
                    [
                        {
                            "text": "اوامر التسلية والميمز 😂",
                            "callback_data": "fun_meme_commands",
                            "style": "success",
                            "icon_custom_emoji_id": EMOJI_SUCCESS
                        }
                    ],
                    [
                        {
                            "text": "اوامر الاذاعة 📢",
                            "callback_data": "broadcast_commands",
                            "style": "danger",
                            "icon_custom_emoji_id": EMOJI_DANGER
                        },
                        {
                            "text": "اوامر التحويل 🔄",
                            "callback_data": "convert_commands",
                            "style": "secondary",
                            "icon_custom_emoji_id": EMOJI_SECONDARY
                        }
                    ],
                    [
                        {
                            "text": "اوامر الجهات 👥",
                            "callback_data": "contacts_commands",
                            "style": "primary",
                            "icon_custom_emoji_id": EMOJI_PRIMARY
                        }
                    ],
                    [
                        {
                            "text": "اوامر الحساب 👤",
                            "callback_data": "account_commands",
                            "style": "success",
                            "icon_custom_emoji_id": EMOJI_SUCCESS
                        },
                        {
                            "text": "اوامر الفارات ⚙️",
                            "callback_data": "var_commands",
                            "style": "warning",
                            "icon_custom_emoji_id": EMOJI_WARNING
                        }
                    ],
                    [
                        {
                            "text": "اوامر التجميع 💰",
                            "callback_data": "collect_commands",
                            "style": "danger",
                            "icon_custom_emoji_id": EMOJI_DANGER
                        }
                    ],
                    [
                        {
                            "text": "اوامر وعد 🏦",
                            "callback_data": "w3d_commands",
                            "style": "secondary",
                            "icon_custom_emoji_id": EMOJI_SECONDARY
                        },
                        {
                            "text": "اوامر الاذكار 📿",
                            "callback_data": "azkar_commands",
                            "style": "success",
                            "icon_custom_emoji_id": EMOJI_SUCCESS
                        }
                    ]
                ]
            }
            
            # إرسال عبر Bot API
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            
            inline_data = {
                "inline_query_id": event.id,
                "results": json.dumps([
                    {
                        "type": "article",
                        "id": "help_menu_1",
                        "title": "قائمة المساعدة - آراس",
                        "description": "اضغط لعرض قائمة الأوامر",
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
                print(f"❌ خطأ في inline: {e}")
