from telethon import events
from telethon.utils import pack_bot_file_id

@tgbot.on(events.NewMessage(pattern="^الايدي"))
async def _(event):
    reply = await event.get_reply_message()
    if reply:
        text = f"⌯︙الدردشة: `{event.chat_id}`\n⌯︙المستخدم: `{reply.sender_id}`"
        if reply.media:
            text += f"\n⌯︙الميديا: `{pack_bot_file_id(reply.media)}`"
    else:
        text = f"⌯︙الدردشة: `{event.chat_id}`"
    
    await event.reply(text)
