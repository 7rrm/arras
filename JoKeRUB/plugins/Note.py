from telethon import events
import asyncio
from datetime import datetime
from ..core.managers import edit_or_reply
from . import l313l

TARGET_BOT = "@e556bot"

@l313l.ar_cmd(pattern="اكتب(?: |$)([\s\S]*)")
async def write_note(event):
    # جلب النص الكامل (يدعم السطور الجديدة)
    text = event.pattern_match.group(1).strip() if event.pattern_match.group(1) else ""
    
    # إذا لم يكتب نصاً، يطلب منه إرساله
    if not text:
        return await edit_or_reply(event, "❌ **الرجاء كتابة النص بعد الأمر**\n\nمثال: `.اكتب مرحباً`\nأو قم بالرد على رسالة تحتوي نص")
    
    jokevent = await edit_or_reply(event, "⌔︙جـار إنشاء الدفتر...")
    start = datetime.now()
    
    try:
        async with l313l.conversation(TARGET_BOT, timeout=30) as conv:
            # إرسال النص الكامل
            await conv.send_message(text)
            
            response = await conv.get_response()
            
            if response.photo or response.document:
                end = datetime.now()
                ms = (end - start).seconds
                
                await event.client.send_file(
                    event.chat_id,
                    response.media,
                    caption=f"**- تم إنشاء دفترك!**\n- **الوقت:** `{ms} ثانية`"
                )
                await jokevent.delete()
                
                async for msg in l313l.iter_messages(TARGET_BOT, limit=5):
                    await msg.delete()
            else:
                await jokevent.edit(f"**❌ لم يتم استلام صورة**")
                
    except asyncio.TimeoutError:
        await jokevent.edit("**⌔︙انتهى الوقت**")
    except Exception as e:
        await jokevent.edit(f"**⌔︙خطأ:**\n`{str(e)}`")

from telethon import events
import asyncio
from datetime import datetime
from ..core.managers import edit_or_reply
from . import l313l

TARGET_BLUR_BOT = "@Nj35bot"

@l313l.ar_cmd(pattern="تغويش(?: |$)([\s\S]*)")
async def blur_image(event):
    # جلب النسبة
    percent = event.pattern_match.group(1).strip() if event.pattern_match.group(1) else ""
    
    if not event.is_reply:
        return await edit_or_reply(event, "❌ **الرجاء الرد على صورة**\nمثال: قم بالرد على صورة وأرسل `.تغويش 50`")
    
    replied = await event.get_reply_message()
    if not replied.photo:
        return await edit_or_reply(event, "❌ **الرد يجب أن يكون على صورة**")
    
    if not percent:
        return await edit_or_reply(event, "❌ **الرجاء تحديد نسبة التغويش**\nمثال: `.تغويش 50`")
    
    try:
        percent = int(percent)
        if percent < 1 or percent > 100:
            return await edit_or_reply(event, "❌ **النسبة بين 1 و 100**")
    except:
        return await edit_or_reply(event, "❌ **أدخل رقماً صحيحاً**")
    
    jokevent = await edit_or_reply(event, f"⌔︙جـار تغويش الصورة بنسبة {percent}%...")
    start = datetime.now()
    
    try:
        async with l313l.conversation(TARGET_BLUR_BOT, timeout=30) as conv:
            await conv.send_file(replied.media)
            await asyncio.sleep(2)
            await conv.send_message(str(percent))
            
            response = await conv.get_response()
            
            if response.photo or response.document:
                end = datetime.now()
                ms = (end - start).seconds
                
                await event.client.send_file(
                    event.chat_id,
                    response.media,
                    caption=f"**- تم تغويش الصورة!**\n- **النسبة:** `{percent}%`\n- **الوقت:** `{ms} ثانية`"
                )
                await jokevent.delete()
                
                async for msg in l313l.iter_messages(TARGET_BLUR_BOT, limit=10):
                    await msg.delete()
            else:
                await jokevent.edit(f"**❌ فشل في تغويش الصورة**")
                
    except asyncio.TimeoutError:
        await jokevent.edit("**⌔︙انتهى الوقت**")
    except Exception as e:
        await jokevent.edit(f"**⌔︙خطأ:**\n`{str(e)}`")


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
