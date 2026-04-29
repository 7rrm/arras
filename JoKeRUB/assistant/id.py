from telethon import events

@tgbot.on(events.NewMessage(pattern="^الايدي"))
async def _(e):
    r = await e.get_reply_message()
    if r:
        txt = f"الدردشة: {e.chat_id}\nالمستخدم: {r.sender_id}"
        if r.media and hasattr(r.media, 'id'):
            txt += f"\nالميديا: {r.media.id}"
        await e.reply(txt)
    else:
        await e.reply(f"الدردشة: {e.chat_id}")
