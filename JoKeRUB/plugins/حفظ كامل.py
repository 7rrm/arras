import asyncio
from telethon import events
from JoKeRUB import l313l

plugin_category = "misc"

@l313l.ar_cmd(
    pattern="حفظ كامل(?: |$)(.*)",
    command=("حفظ كامل", plugin_category),
    info={
        "header": "نقل جميع الرسائل من قناة معينة مع الحفاظ على تنسيق الوسائط المتعددة.",
        "description": "يحفظ كل الرسائل من قناة/مجموعة مع الاحتفاظ بالصور المتعددة في رسالة واحدة.",
        "usage": "{tr}حفظ_كامل <رابط/معرف/ID القناة>",
    },
)
async def transfer_channel(event):
    input_str = event.pattern_match.group(1).strip()
    if not input_str:
        return await event.edit("**✎┊ يرجى تحديد رابط القناة أو المعرف أو الـ ID!**")

    await event.edit("**✎┊ جاري التحقق من القناة، يرجى الانتظار...**")

    try:
        if input_str.startswith(("https://t.me/", "t.me/", "@")):
            channel_entity = input_str.split("/")[-1].replace("@", "")
            chat = await l313l.get_entity(channel_entity)
        elif input_str.isdigit():
            chat = await l313l.get_entity(int(input_str))
        else:
            return await event.edit("**✎┊ الرابط أو المعرف غير صالح!**")
    except Exception as e:
        return await event.edit(f"**✎┊ خطأ أثناء جلب القناة: {str(e)}**")

    target_chat = event.chat_id  # الدردشة الهدف (حيث سيتم حفظ الرسائل)

    try:
        messages = await l313l.get_messages(chat, limit=5000, reverse=True)
        total = len(messages)
        success = 0

        for msg in messages:
            await asyncio.sleep(5)  # تقليل خطر الحظر

            try:
                # إذا كانت الرسالة تحتوي على وسائط متعددة (مثل ألبوم صور)
                if msg.media and hasattr(msg, "grouped_id"):
                    media_files = []
                    caption = msg.text if msg.text else ""

                    # تحميل جميع الوسائط في الألبوم
                    async for m in l313l.iter_messages(chat, ids=range(msg.id, msg.id + 10)):
                        if m.grouped_id == msg.grouped_id and m.media:
                            media_path = await l313l.download_media(m.media)
                            media_files.append(media_path)

                    # إرسالها كمجموعة واحدة
                    if media_files:
                        await l313l.send_file(
                            target_chat,
                            media_files,
                            caption=caption,
                        )
                        success += 1

                # إذا كانت رسالة عادية (نص أو صورة واحدة)
                else:
                    if msg.text and not msg.media:
                        await l313l.send_message(target_chat, msg.text)
                        success += 1
                    elif msg.media:
                        caption = msg.text if msg.text else ""
                        media_path = await l313l.download_media(msg.media)
                        await l313l.send_file(
                            target_chat,
                            media_path,
                            caption=caption,
                        )
                        success += 1

            except Exception as e:
                await event.reply(f"**✎┊ خطأ في حفظ الرسالة {msg.id}: {str(e)}**")

        await event.edit(f"**✎┊ تم نقل {success}/{total} رسالة بنجاح! ✅**")
    except Exception as e:
        await event.edit(f"**✎┊ حدث خطأ أثناء جلب الرسائل: {str(e)}**")
