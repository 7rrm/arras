from telethon import events
from telethon.utils import pack_bot_file_id

@tgbot.on(events.NewMessage(pattern="^الايدي"))
async def _(e):
    r = await e.get_reply_message()
    if r:
        txt = f"⌯︙الدردشة: `{e.chat_id}`\n⌯︙المستخدم: `{r.sender_id}`"
        if r.media:
            try:
                txt += f"\n⌯︙الميديا: `{pack_bot_file_id(r.media)}`"
            except:
                txt += f"\n⌯︙الميديا: `خطأ`"
        await e.reply(txt)
    else:
        await e.reply(f"⌯︙الدردشة: `{e.chat_id}`")
