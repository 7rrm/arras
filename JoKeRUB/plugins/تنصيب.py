from telethon import events, Button
from telethon.events import CallbackQuery
import json
import requests
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
    
    # ✅ إرسال مباشر عبر API عشان الإيموجي المميز يشتغل
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
    
    send_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/sendMessage"
    send_data = {
        "chat_id": event.chat_id,
        "text": ROZ,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(keyboard),
        "disable_web_page_preview": True
    }
    
    try:
        requests.post(send_url, json=send_data, timeout=3)
        await event.delete()
    except Exception as e:
        print(f"❌ خطأ: {e}")
        await event.edit(ROZ, buttons=[[Button.url("‹ : المـطـور : ›", "https://t.me/lx5x5")]])
