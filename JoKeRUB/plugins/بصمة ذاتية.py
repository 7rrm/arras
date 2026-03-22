from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
import os
import asyncio
from telethon import events
from JoKeRUB import *


from . import BOTLOG, BOTLOG_CHATID, mention

vocself = True

@l313l.ar_cmd(pattern="(تفعيل البصمه الذاتيه|تفعيل البصمه الذاتية|تفعيل البصمة الذاتيه|تفعيل البصمة الذاتية)")
async def start_datea(event):
    global vocself

    if vocself:
        return await edit_or_reply(event, "**⎉╎حفظ البصمة الذاتية التلقائي 🎙**\n**⎉╎مفعلـه .. مسبقًـا ✅**")
    vocself = True
    await edit_or_reply(event, "**⎉╎تم تفعيل حفظ البصمة الذاتية 🎙**\n**⎉╎تلقائيًّـا .. بنجاح ✅**")

@l313l.ar_cmd(pattern="(ايقاف البصمه الذاتيه|ايقاف البصمه الذاتية|ايقاف البصمة الذاتيه|ايقاف البصمة الذاتية)")
async def stop_datea(event):
    global vocself
    
    if vocself:
        vocself = False
        return await edit_or_reply(event, "**⎉╎تم تعطيل حفظ البصمة الذاتية 🎙**\n**⎉╎الان صارت مو شغالة .. ✅**")
    await edit_or_reply(event, "**⎉╎حفظ البصمة الذاتية التلقائي 🎙**\n**⎉╎معطلـه .. مسبقـاً ✅**")

@l313l.on(events.NewMessage(func=lambda e: e.is_private and (e.audio or e.voice) and e.media_unread))
async def sddm(event):
    global vocself
  
    if vocself:
        sender = await event.get_sender()
        username = f"@{sender.username}" if sender.username else "لا يوجد"
        chat = await event.get_chat()
        voc = await event.download_media()
       
        await l313l.send_file("me", voc, caption=f"[ᯓ 𝗮𝗥𝗥𝗮𝗦  ⌁ - حفـظ البصمـة الذاتيــة 🎙\n⋆─┄─┄─┄─┄─┄─┄─⋆\n⌔ مࢪحبـًا .. عـزيـزي 🫂\n⌔ تـم حفظ البصمة الذاتية .. تلقائيًّـا ☑️ ❝\n⌔ معلومـات المـرسـل :-\n• الاسم : {_format.mentionuser(sender.first_name , sender.id)}\n• اليوزر : {username}\n• الايدي : {sender.id}")
