from telethon import events
from telethon.utils import pack_bot_file_id

@tgbot.on(events.NewMessage(pattern="^الايدي"))
async def _(e):
    r = await e.get_reply_message()
    await e.reply(f"الدردشة: {e.chat_id}" + (f"\nالمستخدم: {r.sender_id}" + (f"\nنوع الميديا: {type(r.media).__name__}" if r and r.media else "") if r else ""))
