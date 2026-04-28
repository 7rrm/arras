from telethon import events
import asyncio
from datetime import datetime
from ..core.managers import edit_or_reply
from . import l313l

TARGET_BOT = "@e556bot"

@l313l.ar_cmd(pattern="اكتب ([\s\S]*)")
async def write_note(event):
    # جلب النص الكامل (يدعم السطور الجديدة)
    text = event.pattern_match.group(1).strip()
    
    if not text:
        return await edit_or_reply(event, "❌ الرجاء كتابة النص بعد الأمر\nمثال: `.اكتب مرحباً`")
    
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
                    caption=f"**📸 تم إنشاء دفترك!**\n⏰ **الوقت:** `{ms} ثانية`\n\n**📝 النص:**\n`{text[:200]}...`"
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
