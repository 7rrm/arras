"""QuotLy: Avaible commands: .تحويل
"""
import datetime
import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from JoKeRUB.utils import admin_cmd

@borg.on(admin_cmd(pattern="تحويل نص ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("᯽︙ يـجب. الرد علـى رسـالة الـمستخدم )")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("᯽︙ يـجب. الرد علـى رسـالة الـمستخدم )")
       return
    chat = "@QuotLyBot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("᯽︙ يـجب. الرد علـى رسـالة الـمستخدم )")
       return
    await event.edit("᯽︙ جار تحويل النص الى ملصق")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=1031952739))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock me (@QuotLyBot) u Nigga```")
              return
          if response.text.startswith("Hi!"):
             await event.edit("᯽︙ يجـب الغاء خصـوصية التوجيـه اولا")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message)

@borg.on(admin_cmd(pattern="دزها ?(.*)"))
async def send_sticker(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.delete()  # حذف رسالة الأمر
        await event.respond("᯽︙ يـجب الرد على الملصق المراد إرساله.")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.sticker:
        await event.delete()  # حذف رسالة الأمر
        await event.respond("᯽︙ يـجب الرد على ملصق.")
        return
    if not event.pattern_match.group(1):
        await event.delete()  # حذف رسالة الأمر
        await event.respond("᯽︙ يـجب إضافة رابط الرسالة المراد الرد عليها.")
        return
    try:
        # استخراج معرف الرسالة من الرابط
        link = event.pattern_match.group(1).strip()
        if "t.me" not in link:
            await event.delete()
            await event.respond("᯽︙ الرابط غير صالح.")
            return
        parts = link.split("/")
        msg_id = int(parts[-1])
        chat_id = parts[-2]
        if chat_id.isdigit():
            chat_id = int(chat_id)
        else:
            chat_entity = await event.client.get_entity(chat_id)
            chat_id = chat_entity.id
        # إرسال الملصق كرد على الرسالة
        await event.delete()  # حذف رسالة الأمر
        await event.client.send_file(chat_id, reply_message.sticker, reply_to=msg_id)
    except Exception as e:
        await event.respond(f"᯽︙ حدث خطأ: {str(e)}")

# Copyright (C) 2021 JoKeRUB TEAM
# FILES WRITTEN BY  @lMl10l
# Copyright (C) 2021 JoKeRUB TEAM
# FILES WRITTEN BY  @lMl10l
