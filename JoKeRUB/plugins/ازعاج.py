import random
from telethon import events, functions, types
from JoKeRUB import l313l
from ..Config import Config
from ..core.managers import edit_or_reply

iz3aj_active = {}
emoje = ["😂", "🤯", "👍", "😅", "💋"]

@l313l.ar_cmd(
    pattern="ازعاج (.*)",
    command=("ازعاج", "fun"),
    info={
        "header": "إزعاج شخص ما باستخدام الايموجي",
        "usage": "{tr}ازعاج <emoji> بالرد على رسالة.",
    }
)
async def start_iz3aj(event):
    emoji = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not reply:
        return await edit_or_reply(event, "⌔∮ يرجى الرد على رسالة الشخص.")
    
    user_id = reply.sender_id

    if user_id in Config.Dev:
        return await edit_or_reply(event, "⌔∮ لا يمكن إزعاج المطورين.")
    
    iz3aj_active[user_id] = emoji or random.choice(emoje)
    await edit_or_reply(event, f"⌔∮ تم تفعيل الإزعاج بهذا الإيموجي {emoji} للشخص.")

@l313l.ar_cmd(
    pattern="حذف_ازعاج",
    command=("حذف_ازعاج", "fun"),
    info={
        "header": "لإلغاء إزعاج شخص ما.",
        "usage": "{tr}حذف_ازعاج بالرد على رسالة الشخص.",
    }
)
async def stop_iz3aj(event):
    reply = await event.get_reply_message()
    if not reply:
        return await edit_or_reply(event, "⌔∮ يرجى الرد على رسالة الشخص.")
    
    user_id = reply.sender_id

    if user_id in iz3aj_active:
        del iz3aj_active[user_id]
        await edit_or_reply(event, "⌔∮ تم إلغاء الإزعاج للشخص.")
    else:
        await edit_or_reply(event, "⌔∮ لا يوجد إزعاج مفعّل لهذا الشخص.")

@l313l.on(events.NewMessage())
async def iz3a(event):
    user_id = event.sender_id
    if user_id in iz3aj_active:
        if user_id in Config.Dev:
            return

        emoji = iz3aj_active.get(user_id) or random.choice(emoje)

        try:
            await l313l(functions.messages.SendReactionRequest(
                peer=event.chat_id,
                msg_id=event.id,
                big=False,  
                add_to_recent=True,
                reaction=[types.ReactionEmoji(
                    emoticon=emoji
                )]
            ))
        except Exception as e:
            await edit_or_reply(event, f"⌔∮ خطأ: {str(e)}")
