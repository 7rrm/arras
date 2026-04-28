from telethon import events
import asyncio
from datetime import datetime
from ..core.managers import edit_or_reply
from . import l313l

TARGET_BOT = "@e556bot"

@l313l.ar_cmd(pattern="اكتب(?: |$)(.*)")
async def test_write(event):
    """اختبار بوت الدفتر"""
    
    text = event.pattern_match.group(1).strip()
    
    if not text:
        return await edit_or_reply(event, "❌ أرسل النص بعد الأمر\nمثال: `.اكتب مرحباً`")
    
    jokevent = await edit_or_reply(event, "🔄 جاري إنشاء الدفتر...")
    start = datetime.now()
    
    try:
        async with l313l.conversation(TARGET_BOT, timeout=30) as conv:
            # إرسال النص
            await conv.send_message(text)
            
            # انتظار الرد
            response = await conv.get_response()
            
            if response.photo or response.document:
                end = datetime.now()
                ms = (end - start).seconds
                
                await event.client.send_file(
                    event.chat_id,
                    response.media,
                    caption=f"✅ تم إنشاء دفترك!\n📝 النص: {text[:50]}...\n⏰ الوقت: {ms} ثانية"
                )
                await jokevent.delete()
            else:
                await jokevent.edit(f"❌ لم استلم صورة\nرد البوت: {response.text[:100] if response.text else 'لا يوجد'}")
                
    except asyncio.TimeoutError:
        await jokevent.edit("❌ انتهى الوقت")
    except Exception as e:
        await jokevent.edit(f"❌ خطأ: {str(e)}")

from telethon import events
import asyncio
from datetime import datetime
from ..core.managers import edit_or_reply
from . import l313l

TARGET_BOT = "@Nj35bot"

@l313l.ar_cmd(pattern="تغويش(?: |$)(.*)")
async def test_blur(event):
    """اختبار بوت تغويش الصورة"""
    
    # جلب النسبة
    percent = event.pattern_match.group(1).strip()
    
    # التحقق من الرد على صورة
    if not event.is_reply:
        return await edit_or_reply(event, "❌ قم بالرد على صورة")
    
    replied = await event.get_reply_message()
    if not replied.photo:
        return await edit_or_reply(event, "❌ هذا ليس صورة")
    
    if not percent:
        return await edit_or_reply(event, "❌ أرسل نسبة التغويش\nمثال: `.تغويش 50`")
    
    try:
        percent = int(percent)
        if percent < 1 or percent > 100:
            return await edit_or_reply(event, "❌ النسبة بين 1 و 100")
    except:
        return await edit_or_reply(event, "❌ أرسل رقماً صحيحاً")
    
    jokevent = await edit_or_reply(event, f"🔄 جاري تغويش الصورة بنسبة {percent}%...")
    start = datetime.now()
    
    try:
        async with l313l.conversation(TARGET_BOT, timeout=30) as conv:
            # إرسال الصورة
            await conv.send_file(replied.media)
            await asyncio.sleep(2)
            
            # إرسال النسبة
            await conv.send_message(str(percent))
            
            # انتظار الرد
            response = await conv.get_response()
            
            if response.photo or response.document:
                end = datetime.now()
                ms = (end - start).seconds
                
                await event.client.send_file(
                    event.chat_id,
                    response.media,
                    caption=f"✅ تم تغويش الصورة!\n📊 النسبة: {percent}%\n⏰ الوقت: {ms} ثانية"
                )
                await jokevent.delete()
            else:
                await jokevent.edit(f"❌ لم استلم صورة\nرد البوت: {response.text[:100] if response.text else 'لا يوجد'}")
                
    except asyncio.TimeoutError:
        await jokevent.edit("❌ انتهى الوقت")
    except Exception as e:
        await jokevent.edit(f"❌ خطأ: {str(e)}")
