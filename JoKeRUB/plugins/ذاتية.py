from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
import os
from telethon import events
from JoKeRUB import *

# تفعيل الميزة تلقائياً عند بدء التشغيل
addgvar("savepicforme", "reda")

@l313l.on(admin_cmd(pattern="(جلب الصوره|ذاتيه|ذاتية|احح)"))
async def dato(event):
    if not event.is_reply:
        return await event.edit("..")
    lMl10l = await event.get_reply_message()
    pic = await lMl10l.download_media()
    await bot.send_file(
        "me",
        pic,
        caption=f"""
- تـم حفظ الصـورة بنجـاح ✓ 
- غير مبري الذمه اذا استخدمت الامر للابتزاز
- CH: @aghvv
- Dev: @lx5x5
  """,
    )
    await event.delete()

@l313l.on(events.NewMessage(pattern="(تفعيل الذاتية|تفعيل ذاتية)"))
async def enable_auto_save(event):
    if gvarstatus("savepicforme"):
        await event.reply("**᯽︙حفظ الذاتيات مفعل وليس بحاجة للتفعيل مجدداً **")
    else:
        addgvar("savepicforme", "reda")
        await event.reply("**᯽︙تم تفعيل ميزة حفظ الذاتيات بنجاح ✓**")

@l313l.on(events.NewMessage(pattern="(تعطيل الذاتية|تعطيل ذاتية)"))
async def disable_auto_save(event):
    if gvarstatus("savepicforme"):
        delgvar("savepicforme")
        await event.reply("**᯽︙تم تعطيل حفظ الذاتيات بنجاح ✓**")
    else:
        await event.reply("**᯽︙حفظ الذاتيات معطل بالفعل!**")

def joker_unread_media(message):
    return message.media_unread and (message.photo or message.video)

async def Hussein(event):
    media = await event.download_media()
    sender = await event.get_sender()
    username = f"@{sender.username}" if sender.username else "لا يوجد"
    
    caption = f"""
ᯓ 𝗮𝗥𝗥𝗮𝗦 - حفـظ الصوره الذاتيه 🎙
⋆─┄─┄─┄─┄─┄─┄─⋆
**⌔ مࢪحبـاً .. عـزيـزي 🫂**
**⌔ تـم حفظ البصمه الذاتية .. تلقائياً ☑️ ❝**
**⌔ معلومـات المـرسـل :-**
**• الاسم :** `{sender.first_name}`
**• اليوزر :** {username}
**• الايدي :** `{sender.id}`
    """
    
    await bot.send_file(
        "me",
        media,
        caption=caption,
        parse_mode="markdown"
    )
    os.remove(media)

@l313l.on(events.NewMessage(func=lambda e: e.is_private and joker_unread_media(e) and e.sender_id != bot.uid))
async def Reda(event):
    if gvarstatus("savepicforme"):
        await Hussein(event)
