from telethon import events
import json
import requests
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
            # 🎨 أزرار ملونة - زرين فقط للتجربة
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "🔥 اوامر الادارة 🔥",
                            "callback_data": "admin_commands",
                            "style": "primary",
                            "icon_custom_emoji_id": FIRE_EMOJI
                        }
                    ],
                    [
                        {
                            "text": "✨ اوامر التنظيف ✨",
                            "callback_data": "clean_cmd",
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
                print(f"✅ تم إرسال قائمة المساعدة للمستخدم {user_id}")
            except Exception as e:
                print(f"❌ خطأ في inline: {e}")

@l313l.ar_cmd(pattern="مساعدة$")
async def help_cmd(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()
    TG_BOT = Config.TG_BOT_USERNAME
    response = await l313l.inline_query(TG_BOT, "مساعدة")
    await response[0].click(event.chat_id)
    await event.delete()
