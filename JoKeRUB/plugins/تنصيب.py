from telethon import events
from telethon.tl.functions.messages import SendInlineBotResultRequest
from telethon.tl.types import InputBotInlineResult, InputBotInlineMessageText
import json
import requests
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from l313l.razan.resources.mybot import *

ROZ_PIC = "https://graph.org/file/2e51431a290028d612377-07abd6e9a86fde6949.jpg"
PREMIUM_EMOJI = "5368324170671202286"  # 🎯 إيموجي بريميوم

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
            # 🎨 أزرار مع إيموجي بريميوم
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            
            # تصميم الأزرار مع إيموجي بريميوم
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "المطور @lx5x5",
                            "url": "https://t.me/lx5x5"
                        }
                    ],
                    [
                        {
                            "text": "قناة السورس",
                            "url": "https://t.me/your_channel"
                        }
                    ]
                ]
            }
            
            # إضافة نص الزر مع الإيموجي في الـ text
            keyboard["inline_keyboard"][0][0]["text"] = f"‌‌{PREMIUM_EMOJI}  المطور @lx5x5  {PREMIUM_EMOJI}"
            keyboard["inline_keyboard"][1][0]["text"] = f"‌‌{PREMIUM_EMOJI}  قناة السورس  {PREMIUM_EMOJI}"
            
            # بيانات الإنلاين
            inline_data = {
                "inline_query_id": event.id,
                "results": json.dumps([
                    {
                        "type": "article",
                        "id": "1",
                        "title": f"{PREMIUM_EMOJI} JoKeRUB - السورس الملون {PREMIUM_EMOJI}",
                        "description": "اضغط لعرض السورس مع أزرار بإيموجي بريميوم",
                        "input_message_content": {
                            "message_text": f"{PREMIUM_EMOJI * 3}\n{ROZ}\n{PREMIUM_EMOJI * 3}",
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
                    print(f"✅ تم إرسال الأزرار مع إيموجي بريميوم للمستخدم {user_id}")
                else:
                    print(f"❌ خطأ في الإرسال: {response.text}")
            except Exception as e:
                print(f"❌ خطأ: {e}")

@bot.on(admin_cmd(outgoing=True, pattern="السورس"))
async def repo(event):
    if event.fwd_from:
        return
    TG_BOT = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(TG_BOT, "السورس")
    await response[0].click(event.chat_id)
    await event.delete()
