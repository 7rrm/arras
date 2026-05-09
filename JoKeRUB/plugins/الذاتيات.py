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
ᯓ 𝗮𝗥𝗥𝗮𝗦 - حفـظ الصوره الذاتيه 🖼️
⋆─┄─┄─┄─┄─┄─┄─⋆
**⌔ مࢪحبـاً .. عـزيـزي 🫂**
**⌔ تـم حفظ الصورة الذاتية .. تلقائياً ☑️ ❝**
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

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
import os
import asyncio
from telethon import events
from JoKeRUB import *

# أمر جلب الصوت
@l313l.on(admin_cmd(pattern="(جلب الصوت|جلب صوت|صوت)"))
async def dato(event):
    if not event.is_reply:
        return await event.edit("يجب الرد على رسالة صوتية لاستخدام هذا الأمر.")
    
    lMl10l = await event.get_reply_message()
    if not lMl10l.voice:
        return await event.edit("الرد يجب أن يكون على رسالة صوتية.")
    
    voice = await lMl10l.download_media(file="voices/")
    await bot.send_file(
        "me",
        voice,
        caption=f"""
- تـم حفظ الـصوت بنجـاح ✓ 
- غير مبري الذمه اذا استخدمت الامر للابتزاز
- Dev: @Lx5x5
  """,
    )

addgvar("savepicforme", "reda")  # تم تفعيل الميزة تلقائيًا

# تفعيل حفظ الرسائل الصوتية
@l313l.on(admin_cmd(pattern="(الصوت تشغيل|صوت تشغيل)"))
async def reda(event):
    if gvarstatus("savevoiceforme"):
        return await edit_delete(event, "**᯽︙حفظ الرسائل الصوتية مفعل وليس بحاجة للتفعيل مجدداً **")
    else:
        addgvar("savevoiceforme", "reda")
        await edit_delete(event, "**᯽︙تم تفعيل ميزة حفظ الرسائل الصوتية بنجاح ✓**")

# تعطيل حفظ الرسائل الصوتية
@l313l.on(admin_cmd(pattern="(الصوت تعطيل|صوت تعطيل)"))
async def Reda_Is_Here(event):
    if gvarstatus("savevoiceforme"):
        delgvar("savevoiceforme")
        return await edit_delete(event, "**᯽︙تم تعطيل حفظ الرسائل الصوتية بنجاح ✓**")
    else:
        await edit_delete(event, "**᯽︙انت لم تفعل حفظ الرسائل الصوتية لتعطيلها!**")

# دالة للتحقق من وجود رسالة صوتية ذاتية التدمير
def joker_unread_voice(message):
    return message.media_unread and message.voice and message.media.ttl_seconds is not None

# دالة لحفظ الرسائل الصوتية وإرسالها
async def Hussein(event):
    voice = await event.download_media(file="voices/")
    sender = await event.get_sender()
    username = f"@{sender.username}" if sender.username else "لا يوجد"
    
    caption = f"""
ᯓ 𝗮𝗥𝗥𝗮𝗦 - حفـظ البصمه الذاتيه 🎙
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
        voice,
        caption=caption,
        parse_mode="markdown"
    )

# حدث الاستماع للرسائل الصوتية الجديدة
@l313l.on(events.NewMessage(func=lambda e: e.is_private and joker_unread_voice(e) and e.sender_id != bot.uid))
async def Reda(event):
    if gvarstatus("savevoiceforme"):
        await Hussein(event)
