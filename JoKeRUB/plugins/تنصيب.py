from telethon import events
import json
import requests
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from l313l.razan.resources.mybot import *

ROZ_PIC = "https://graph.org/file/2e51431a290028d612377-07abd6e9a86fde6949.jpg"
FIRE_EMOJI = "5368324170671202286"  # 🔥

# نص السورس
ROZ = (
    f"╭───────• 𝗔𝗥𝗔𝗦 •───────╮\n"
    f"│ **● ʙᴏᴛ sᴛᴀᴛᴜs: ʀᴜɴɴɪɴɢ ✅**\n"
    f"├──────────────────────\n"
    f"│ **● ᴘʟᴀᴛғᴏʀᴍ ᴅᴇᴛᴀɪʟs:**\n"
    f"│ • ᴛᴇʟᴇᴛʜᴏɴ: `1.23.0`\n"
    f"│ • sᴏᴜʀᴄᴇ: `4.0.1`\n"
    f"│ • ʙᴏᴛ: `@{Config.TG_BOT_USERNAME}`\n"
    f"│ • ᴘʏᴛʜᴏɴ: `3.9.6`\n"
    f"│ • ᴜsᴇʀ: {mention}\n"
    f"╰──────────────────────╯"
)

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        query = event.text
        user_id = event.query.user_id
        
        await bot.get_me()
        
        if query.startswith("السورس") and user_id == bot.uid:
            # 🎨 زر واحد فقط - المطور بلون أزرق
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "🔥 المطور @lx5x5 🔥",
                            "url": "https://t.me/lx5x5",
                            "style": "primary",  # 🔵 أزرق
                            "icon_custom_emoji_id": FIRE_EMOJI
                        }
                    ]
                ]
            }
            
            # بيانات الإنلاين
            inline_data = {
                "inline_query_id": event.id,
                "results": json.dumps([
                    {
                        "type": "article",
                        "id": "1",
                        "title": "🔥 JoKeRUB - السورس",
                        "description": "المطور @lx5x5",
                        "input_message_content": {
                            "message_text": ROZ,
                            "parse_mode": "Markdown"
                        },
                        "reply_markup": keyboard
                    }
                ]),
                "cache_time": 0,
                "is_personal": True
            }
            
            # إرسال الطلب
            try:
                requests.post(url, json=inline_data)
                print(f"✅ تم إرسال الزر الأزرق للمستخدم {user_id}")
            except Exception as e:
                print(f"❌ خطأ: {e}")

@bot.on(admin_cmd(outgoing=True, pattern="السورس"))
async def repo(event):
    if event.fwd_from:
        return
    TG_BOT = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    
    # ✅ الحل النهائي لمشكلة Entity - نرسل الرسالة مباشرة بدون click
    chat = await event.get_input_chat()
    await bot.send_message(chat, f"@{TG_BOT} السورس")
    await event.delete()
