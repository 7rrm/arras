import asyncio
from telethon import events
from JoKeRUB import l313l

plugin_category = "misc"

@l313l.ar_cmd(
    pattern=r"حفظ كامل (-?\d+)",  
    command=("حفظ كامل", plugin_category),
    info={
        "header": "نقل جميع الرسائل من قناة معينة حتى لو كانت محمية.",
        "description": "ينقل كل المحتوى من قناة معينة أو مجموعة إلى المكان الذي يتم كتابة الأمر فيه، مع الحفاظ على الترتيب من الأقدم إلى الأحدث.",
        "usage": "{tr}حفظ_كامل <ID القناة أو المجموعة>",
    },
)
async def transfer_channel(event):
    channel_id = int(event.pattern_match.group(1))
    if not channel_id:
        return await event.edit("**✎┊‌ يرجى تحديد ID القناة أو المجموعة!**")

    await event.edit("**✎┊‌ جاري التحقق من القناة، يرجى الانتظار...**")

    try:
        chat = await l313l.get_entity(channel_id)
    except Exception as e:
        return await event.edit(f"**✎┊‌ خطأ أثناء جلب القناة/المجموعة: {str(e)}**")

    chat_id = event.chat_id  # المكان اللي راح تنحفظ بيه الرسائل

    try:
        messages = await l313l.get_messages(chat, limit=5000, reverse=True)

        for msg in messages:
            await asyncio.sleep(1)  # منع الحظر بسبب السرعة العالية

            try:
                # إرسال النصوص العادية
                if msg.text:
                    await l313l.send_message(chat_id, f"{msg.text}")

                # إعادة رفع الوسائط بدون إعادة توجيه
                if msg.media:
                    media_caption = msg.text if msg.text else "📎 صورة محفوظة"  # تعليق تلقائي للصور بدون نص
                    file_path = await l313l.download_media(msg.media)  # تحميل الملف محليًا
                    await l313l.send_file(chat_id, file_path, caption=media_caption)  # إعادة الرفع
                    await asyncio.sleep(1)  # تأخير لمنع الضغط على السيرفر

            except Exception as e:
                await l313l.send_message(chat_id, f"✎┊‌ خطأ أثناء حفظ الرسالة: {str(e)}")

        await event.edit("**✎┊‌ تم نقل جميع الرسائل بنجاح! ✅**")
    except Exception as e:
        await event.edit(f"✎┊‌ حدث خطأ أثناء جلب الرسائل. الخطأ: {str(e)}")