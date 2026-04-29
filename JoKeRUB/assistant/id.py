from telethon import events
from telethon.utils import pack_bot_file_id

@tgbot.on(events.NewMessage(pattern="^الايدي"))
async def _(event):
    chat_id = event.chat_id
    reply_msg = await event.get_reply_message()
    
    if reply_msg:
        user_id = reply_msg.sender_id
        msg = f"⌯︙ايـدي الـدردشة: `{chat_id}`\n⌯︙ايدي المستخدم: `{user_id}`"
        
        if reply_msg.media:
            bot_api_file_id = pack_bot_file_id(reply_msg.media)
            msg += f"\n⌯︙ايـدي الميديا: `{bot_api_file_id}`"
    else:
        msg = f"⌯︙ايـدي الـدردشة: `{chat_id}`"
    
    await event.reply(msg)
