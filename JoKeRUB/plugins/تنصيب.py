from telethon import events, Button
from telethon.events import CallbackQuery
import json
import requests
import html
import asyncio
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from JoKeRUB.plugins import mention

# الكليشة مع الإيموجي المميز
ROZ = f"""╭───────• 𝗔𝗥𝗔𝗦 •───────╮
│ ● ʙᴏᴛ sᴛᴀᴛᴜs: ʀᴜɴɴɪɴɢ <tg-emoji emoji-id="5974491287615706239">✅</tg-emoji>
├──────────────────────
│ ● ᴘʟᴀᴛғᴏʀᴍ ᴅᴇᴛᴀɪʟs:
│ • ᴛᴇʟᴇᴛʜᴏɴ: <code>1.23.0</code>
│ • sᴏᴜʀᴄᴇ: <code>4.0.1</code>
│ • ʙᴏᴛ: <code>@{Config.TG_BOT_USERNAME}</code> <tg-emoji emoji-id="5778296180807046576">📨</tg-emoji>
│ • ᴘʏᴛʜᴏɴ: <code>3.9.10</code>
│ • ᴜsᴇʀ: {mention}
╰──────────────────────╯"""

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        await bot.get_me()
        
        if query.startswith("السورس") and event.query.user_id == bot.uid:
            # أزرار ملونة
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "‹ : المـطـور : ›",
                            "url": "https://t.me/lx5x5",
                            "style": "primary"
                        }
                    ]
                ]
            }
            
            # إرسال عبر API
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            inline_data = {
                "inline_query_id": event.id,
                "results": json.dumps([
                    {
                        "type": "article",
                        "id": "sorous_1",
                        "title": "🔥 JoKeRUB - السورس",
                        "description": "السورس الرسمي - اضغط للإرسال",
                        "input_message_content": {
                            "message_text": ROZ,
                            "parse_mode": "HTML"
                        },
                        "reply_markup": keyboard
                    }
                ]),
                "cache_time": 0,
                "is_personal": True
            }
            
            try:
                requests.post(url, json=inline_data)
            except Exception:
                pass

@bot.on(admin_cmd(outgoing=True, pattern="السورس"))
async def repo(event):
    if event.fwd_from:
        return
    
    # حل مشكلة PeerUser
    try:
        await event.get_sender()
        await event.get_chat()
    except Exception:
        pass
    
    TG_BOT = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(TG_BOT, "السورس")
    await response[0].click(event.chat_id)
    await event.delete()
