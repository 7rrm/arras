from telethon import events
from telethon.tl.functions.messages import SendInlineBotResultRequest
from telethon.tl.types import InputBotInlineResult, InputBotInlineMessageText
import json
import requests
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from l313l.razan.resources.mybot import *

ROZ_PIC = "https://graph.org/file/2e51431a290028d612377-07abd6e9a86fde6949.jpg"

# 🎯 ايموجي بريميوم حقيقي - هذا هو المطلوب
PREMIUM_FIRE_EMOJI = "5368324170671202286"  # 🔥 ايموجي نار بريميوم
FIRE_EMOJI = "5951810621887484519"  # 🔥 ايموجي عادي احتياطي

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
            # 🎨 أزرار ملونة مع ايموجي بريميوم
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            
            # تصميم الأزرار مع ايموجي بريميوم 5368324170671202286
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "المطور @lx5x5",
                            "url": "https://t.me/lx5x5",
                            "style": "primary",  # 🔵 أزرق
                            "icon_custom_emoji_id": PREMIUM_FIRE_EMOJI  # ✅ ايموجي بريميوم
                        }
                    ],
                    [
                        {
                            "text": "قناة السورس",
                            "url": "https://t.me/your_channel",
                            "style": "success",  # 🟢 أخضر
                            "icon_custom_emoji_id": PREMIUM_FIRE_EMOJI  # ✅ ايموجي بريميوم
                        }
                    ],
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
                        "description": "مع ايموجي بريميوم 🔥",
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
                response = requests.post(url, json=inline_data)
                if response.status_code == 200:
                    print(f"✅ تم إرسال الأزرار مع ايموجي بريميوم للمستخدم {user_id}")
                else:
                    print(f"❌ خطأ: {response.text}")
            except Exception as e:
                print(f"❌ خطأ: {e}")

@bot.on(admin_cmd(outgoing=True, pattern="السورس"))
async def repo(event):
    if event.fwd_from:
        return
    TG_BOT = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    
    # ✅ إرسال الأمر مع معالجة الأخطاء
    try:
        await bot.send_message(event.chat_id, f"@{TG_BOT} السورس")
        await event.delete()
    except Exception as e:
        print(f"❌ خطأ في إرسال الأمر: {e}")
        await event.edit("❌ حدث خطأ، حاول مرة أخرى")
