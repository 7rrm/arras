from telethon import events
import json
import requests
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from l313l.razan.resources.mybot import *

ROZ_PIC = "https://graph.org/file/2e51431a290028d612377-07abd6e9a86fde6949.jpg"
FIRE_EMOJI = "5368324170671202286"  # 🔥 ايموجي بريميوم

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
        
        if query.startswith("السورسس") and user_id == bot.uid:
            # 🎨 أزرار ملونة للإنلاين
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "المطور @lx5x5",
                            "url": "https://t.me/lx5x5",
                            "style": "primary",
                            "icon_custom_emoji_id": FIRE_EMOJI
                        }
                    ],
                    [
                        {
                            "text": "قناة السورس",
                            "url": "https://t.me/your_channel",
                            "style": "success",
                            "icon_custom_emoji_id": FIRE_EMOJI
                        }
                    ],
                    [
                        {
                            "text": "الدعم الفني",
                            "url": "https://t.me/your_support",
                            "style": "danger",
                            "icon_custom_emoji_id": FIRE_EMOJI
                        }
                    ]
                ]
            }
            
            inline_data = {
                "inline_query_id": event.id,
                "results": json.dumps([
                    {
                        "type": "article",
                        "id": "1",
                        "title": "🔥 JoKeRUB - السورس",
                        "description": "السورس الرسمي - اضغط للإرسال",
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
            
            try:
                requests.post(url, json=inline_data)
                print(f"✅ تم إرسال الأزرار للمستخدم {user_id}")
            except Exception as e:
                print(f"❌ خطأ: {e}")

@bot.on(admin_cmd(outgoing=True, pattern="السورس"))
async def repo(event):
    if event.fwd_from:
        return
    
    # ✅ إرسال رسالة عادية بدون إنلاين
    await event.edit("⏱️ جاري عرض السورس...")
    
    # تصميم الأزرار الملونة للرسالة العادية
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "المطور @lx5x5",
                    "url": "https://t.me/lx5x5",
                    "style": "primary",
                    "icon_custom_emoji_id": FIRE_EMOJI
                }
            ],
            [
                {
                    "text": "قناة السورس",
                    "url": "https://t.me/your_channel",
                    "style": "success",
                    "icon_custom_emoji_id": FIRE_EMOJI
                }
            ],
            [
                {
                    "text": "الدعم الفني",
                    "url": "https://t.me/your_support",
                    "style": "danger",
                    "icon_custom_emoji_id": FIRE_EMOJI
                }
            ]
        ]
    }
    
    # إرسال الرسالة عبر REST API مباشرة
    bot_token = Config.TG_BOT_TOKEN
    chat_id = event.chat_id
    
    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    send_data = {
        "chat_id": chat_id,
        "text": ROZ,
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard),
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(send_url, json=send_data)
        if response.status_code == 200:
            await event.delete()  # حذف رسالة "جاري العرض"
            print(f"✅ تم إرسال السورس للمحادثة {chat_id}")
        else:
            await event.edit("❌ حدث خطأ في الإرسال")
            print(f"❌ خطأ: {response.text}")
    except Exception as e:
        await event.edit("❌ حدث خطأ، حاول مرة أخرى")
        print(f"❌ خطأ: {e}")
