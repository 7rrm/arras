from telethon import events
import asyncio
from datetime import datetime
from ..core.managers import edit_or_reply
from . import l313l

TARGET_BOT = "@Nj35bot"

@l313l.ar_cmd(pattern="اكتب(?: |$)([\s\S]*)")
async def write_note(event):
    text = event.pattern_match.group(1).strip()
    
    # إذا لم يكتب نصاً، يطلب منه إرساله
    if not text:
        await edit_or_reply(event, "❌ **الرجاء إرسال النص بعد الأمر**\n\nمثال: `.اكتب مرحباً`\nأو قم بالرد على رسالة تحتوي على نص")
        return
    
    jokevent = await edit_or_reply(event, "⌔︙جـار إنشاء الدفتر...")
    start = datetime.now()
    
    try:
        async with l313l.conversation(TARGET_BOT, timeout=30) as conv:
            # إرسال النص إلى البوت
            await conv.send_message(text)
            
            # انتظار الرد (الصورة)
            response = await conv.get_response()
            
            if response.photo or response.document:
                end = datetime.now()
                ms = (end - start).seconds
                
                await event.client.send_file(
                    event.chat_id,
                    response.media,
                    caption=f"- **تم إنشاء دفترك!**\n- **الوقت:** `{ms} ثانية`"
                )
                await jokevent.delete()
                
                # حذف المحادثة مع البوت
                async for msg in l313l.iter_messages(TARGET_BOT, limit=5):
                    await msg.delete()
            else:
                await jokevent.edit(f"**❌ لم يتم استلام صورة من البوت**")
                
    except asyncio.TimeoutError:
        await jokevent.edit("**⌔︙انتهى الوقت، البوت لم يرد**")
    except Exception as e:
        await jokevent.edit(f"**⌔︙حدث خطأ:**\n`{str(e)}`")


@l313l.ar_cmd(pattern="تغويش(?: |$)(\d*)(?: |$)([\s\S]*)")
async def blur_image(event):
    """تغويش صورة بنسبة معينة"""
    
    # جلب النسبة المئوية
    percent = event.pattern_match.group(1).strip()
    text = event.pattern_match.group(2).strip()
    
    # التحقق من وجود رد على صورة
    if not event.is_reply:
        return await edit_or_reply(event, "❌ **الرجاء الرد على صورة**")
    
    replied = await event.get_reply_message()
    if not replied.photo:
        return await edit_or_reply(event, "❌ **الرد يجب أن يكون على صورة**")
    
    # إذا لم يحدد النسبة، يطلبها
    if not percent:
        return await edit_or_reply(event, "❌ **الرجاء تحديد نسبة التغويش**\n\nمثال: `.تغويش 50`")
    
    # التحقق من أن النسبة بين 1 و 100
    try:
        percent = int(percent)
        if percent < 1 or percent > 100:
            return await edit_or_reply(event, "❌ **النسبة يجب أن تكون بين 1 و 100**")
    except ValueError:
        return await edit_or_reply(event, "❌ **الرجاء إدخال رقم صحيح**")
    
    jokevent = await edit_or_reply(event, f"⌔︙جـار تغويش الصورة بنسبة {percent}%...")
    start = datetime.now()
    
    try:
        # إرسال الصورة إلى البوت مع النسبة
        async with l313l.conversation(TARGET_BOT, timeout=30) as conv:
            # إرسال الصورة
            await conv.send_file(replied.media)
            
            # انتظار الرد
            response = await conv.get_response()
            
            # إرسال النسبة (إذا كان البوت يطلبها)
            await conv.send_message(str(percent))
            
            # انتظار الصورة النهائية
            response2 = await conv.get_response()
            
            if response2.photo or response2.document:
                end = datetime.now()
                ms = (end - start).seconds
                
                await event.client.send_file(
                    event.chat_id,
                    response2.media,
                    caption=f"- **تم تغويش الصورة!**\n- **النسبة:** `{percent}%`\n- **الوقت:** `{ms} ثانية`"
                )
                await jokevent.delete()
                
                # حذف المحادثة
                async for msg in l313l.iter_messages(TARGET_BOT, limit=10):
                    await msg.delete()
            else:
                await jokevent.edit(f"**❌ فشل في تغويش الصورة**")
                
    except asyncio.TimeoutError:
        await jokevent.edit("**⌔︙انتهى الوقت، البوت لم يرد**")
    except Exception as e:
        await jokevent.edit(f"**⌔︙حدث خطأ:**\n`{str(e)}`")
