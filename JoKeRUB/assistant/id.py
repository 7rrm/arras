from telethon import events
from telethon.utils import pack_bot_file_id

@tgbot.on(events.NewMessage(pattern="^الايدي"))
async def _(e):
    r = await e.get_reply_message()
    if r:
        txt = f"الدردشة: {e.chat_id}\nالمستخدم: {r.sender_id}"
        if r.media:
            txt += f"\nالميديا: {pack_bot_file_id(r.media)}"
        await e.reply(txt)
    else:
        await e.reply(f"الدردشة: {e.chat_id}")
