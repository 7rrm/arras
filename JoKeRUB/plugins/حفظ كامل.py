
import asyncio
from telethon import events
from JoKeRUB import l313l

plugin_category = "misc"
  
@l313l.ar_cmd(
    pattern="حفظ كامل(?: |$)(.*)",
    command=("حفظ كامل", plugin_category),
    info={
        "header": "نقل الرسائل من رسالة محددة إلى الأحدث في القناة.",
        "description": "يحفظ الرسائل بدءًا من الرابط المحدد وحتى الأحدث، مع تجنب الرسائل الأقدم.",
        "usage": "{tr}حفظ_كامل <رابط الرسالة>",
    },
)
async def transfer_channel(event):
    input_str = event.pattern_match.group(1).strip()
    if not input_str:
        return await event.edit("**✎┊ يرجى تحديد رابط الرسالة!**")

    await event.edit("**✎┊ جاري التحقق من الرسالة، يرجى الانتظار...**")

    try:
        # الحصول على كائن الرسالة من الرابط
        if "t.me/" in input_str:
            parts = input_str.split("/")
            msg_id = int(parts[-1]) if parts[-1].isdigit() else None
            if not msg_id:
                return await event.edit("**✎┊ الرابط غير صالح! تأكد من وجود ID الرسالة في الرابط.**")

            chat_entity = "/".join(parts[:-1])
            chat = await l313l.get_entity(chat_entity)
            start_msg = await l313l.get_messages(chat, ids=msg_id)
            
            if not start_msg:
                return await event.edit("**✎┊ لا يمكن العثور على الرسالة!**")
        else:
            return await event.edit("**✎┊ الرابط غير صالح! استخدم رابطًا مثل `https://t.me/القناة/123`**")

        target_chat = event.chat_id  # الدردشة الهدف
        transferred_messages = set()  # لتجنب تكرار الرسائل
        success = 0

        # جلب الرسائل الأحدث (التي بعد الرسالة المحددة)
        async for msg in l313l.iter_messages(chat, min_id=start_msg.id - 1, reverse=True):
            if msg.id in transferred_messages:
                continue

            await asyncio.sleep(5)  # تقليل خطر الحظر

            try:
                # 1. معالجة الألبومات (الوسائط المجمعة)
                if hasattr(msg, "grouped_id") and msg.grouped_id:
                    media_files = []
                    caption = msg.text if msg.text else ""
                    
                    # جمع كل الوسائط في الألبوم
                    async for m in l313l.iter_messages(chat, min_id=msg.id - 5, max_id=msg.id + 5):
                        if hasattr(m, "grouped_id") and m.grouped_id == msg.grouped_id and m.media:
                            media_path = await l313l.download_media(m.media)
                            media_files.append(media_path)
                            transferred_messages.add(m.id)

                    # إرسال الألبوم كرسالة واحدة
                    if media_files:
                        await l313l.send_file(
                            target_chat,
                            media_files,
                            caption=caption,
                        )
                        success += 1

                # 2. معالجة الرسائل العادية (صورة واحدة/نص)
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
                    transferred_messages.add(msg.id)

            except Exception as e:
                await event.reply(f"**✎┊ خطأ في حفظ الرسالة {msg.id}: {str(e)}**")

        await event.edit(f"**✎┊ تم نقل {success} رسالة بنجاح بدءًا من الرسالة المحددة! ✅**")
    except Exception as e:
        await event.edit(f"**✎┊ حدث خطأ: {str(e)}**")


import asyncio
from telethon import events
from JoKeRUB import l313l

plugin_category = "misc"

@l313l.ar_cmd(
    pattern="احفظ(?: |$)(.*)",
    command=("احفظ", plugin_category),
    info={
        "header": "جلب رسالة من قناة مقيدة وحفظها في الدردشة الحالية",
        "description": "يحفظ الرسالة من القنوات المقيدة عن طريق التحميل وإعادة الإرسال",
        "usage": "{tr}جلب <رابط الرسالة>",
    },
)
async def bypass_restriction(event):
    input_str = event.pattern_match.group(1).strip()
    if not input_str:
        return await event.edit("**✪╎يُرجى تحديد رابـط الرسـالة!**")

    await event.edit("**✪╎جـاري جلـب الرسـالة من القنـاة المقيدة...**")

    try:
        # الحصول على كائن الرسالة من الرابط
        if "t.me/" in input_str:
            parts = input_str.split("/")
            msg_id = int(parts[-1]) if parts[-1].isdigit() else None
            if not msg_id:
                return await event.edit("**✪╎الرابـط غيـر صالـح! تأكـد من وجـود ID الرسـالة في الرابـط.**")

            chat_entity = "/".join(parts[:-1])
            chat = await l313l.get_entity(chat_entity)
            msg = await l313l.get_messages(chat, ids=msg_id)
            
            if not msg:
                return await event.edit("**✪╎لا يمكـن العثـور على الرسـالة!**")
        else:
            return await event.edit("**✪╎الرابـط غيـر صالـح! استخـدم رابـطًا مثـل `https://t.me/القنـاة/123`**")

        target_chat = event.chat_id  # الدردشة الحالية

        try:
            # إذا كانت الرسالة نصية فقط
            if msg.text and not msg.media:
                await l313l.send_message(target_chat, msg.text)
                await event.edit("**✪╎تم جلـب النـص بنجـاح ✅**")
                return

            # إذا كانت الرسالة تحتوي على ميديا
            if msg.media:
                # تحميل الميديا
                media_path = await l313l.download_media(msg.media)
                caption = msg.text if msg.text else ""
                
                # تحديد نوع الميديا
                if hasattr(msg.media, "photo"):
                    await l313l.send_file(target_chat, media_path, caption=caption)
                elif hasattr(msg.media, "document"):
                    await l313l.send_file(target_chat, media_path, caption=caption)
                elif hasattr(msg.media, "webpage"):
                    await l313l.send_message(target_chat, msg.text)
                else:
                    await l313l.send_file(target_chat, media_path, caption=caption)
                
                await event.edit("**✪╎تم جلـب المحتـوى بنجـاح ✅**")
                return

        except Exception as e:
            await event.edit(f"**✪╎خطـأ في جلـب الرسـالة: {str(e)}**")
            return

    except Exception as e:
        await event.edit(f"**✪╎حـدث خطـأ: {str(e)}**")


import asyncio
from telethon import events
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import MessageEntityBlockquote, MessageMediaPhoto, InputMediaUploadedPhoto, MessageMediaDocument
from telethon.tl.custom import Message
from . import l313l
from ..Config import Config
from ..core.managers import edit_or_reply
from . import BOTLOG, BOTLOG_CHATID

async def copy_message_with_all_features(dest_entity, message, source_channel_username):
    """نسخ الرسالة مع جميع مميزاتها (اقتباس، تشويش، تنسيق)"""
    
    # تجهيز النص مع الحفاظ على التنسيق والاقتباسات
    text = message.message or ""
    entities = message.entities or []
    
    # التأكد من الحفاظ على الاقتباسات (blockquotes)
    blockquote_entities = [e for e in entities if isinstance(e, MessageEntityBlockquote)]
    
    # تجهيز الميديا مع دعم التشويش
    media = None
    if message.media:
        if hasattr(message.media, 'spoiler') and message.media.spoiler:
            # إذا كانت الصورة مشوشة في الأصل
            if isinstance(message.media, MessageMediaPhoto):
                # تحميل الصورة وإعادة إرسالها مع تشويش
                photo_data = await message.download_media(bytes)
                uploaded_file = await l313l.upload_file(photo_data)
                media = InputMediaUploadedPhoto(
                    file=uploaded_file,
                    spoiler=True  # تفعيل التشويش
                )
            elif isinstance(message.media, MessageMediaDocument):
                # للمستندات أو الفيديو مع تشويش
                file_data = await message.download_media(bytes)
                uploaded_file = await l313l.upload_file(file_data)
                media = await l313l.send_file(dest_entity, uploaded_file, spoiler=True)
                return media  # نرجع هنا لأن send_file تعمل مباشرة
        else:
            # ميديا عادية بدون تشويش
            file_media = f"https://t.me/{source_channel_username}/{message.id}"
            media = file_media
    
    # إرسال الرسالة كاملة
    if media:
        if isinstance(media, str) and media.startswith('http'):
            # حالة الرابط المباشر
            return await l313l.send_file(dest_entity, media, caption=text, formatting_entities=entities)
        else:
            # حالة الميديا المرفوعة
            return await l313l.send_file(dest_entity, media, caption=text)
    else:
        # رسالة نصية فقط مع الحفاظ على التنسيق
        return await l313l.send_message(dest_entity, text, formatting_entities=entities)

async def start_copier(destination_channel_username, source_channel_username):
    try:
        # الحصول على معلومات القنوات
        source_channel = await l313l.get_entity(source_channel_username)
        destination_channel = await l313l.get_entity(destination_channel_username)
        destination_channel_id = destination_channel.id

        # الحصول على جميع المنشورات من القناة المصدر
        posts = await l313l(GetHistoryRequest(
            peer=source_channel,
            limit=10000,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0,
        ))

        # عكس ترتيب الرسائل لنقلها من الأقدم إلى الأحدث
        posts.messages.reverse()

        # نقل المنشورات إلى القناة المستهدفة
        for message in posts.messages:
            try:
                await copy_message_with_all_features(destination_channel_id, message, source_channel_username)
                
                await asyncio.sleep(1)
                await l313l.send_message(BOTLOG_CHATID, 
                    f"**- تم نقل المنشور .. بنجاح✅**\n"
                    f"**- رابـط المنشور:**\n"
                    f"- https://t.me/{source_channel_username}/{message.id}", 
                    link_preview=False)
                await asyncio.sleep(1)

            except Exception as e:
                await l313l.send_message(BOTLOG_CHATID, 
                    f"**- خطـأ بنقـل المنشـور ❌**\n"
                    f"**- رابـط المنشور:**\n"
                    f"- https://t.me/{source_channel_username}/{message.id}\n"
                    f"**- تفاصيـل الخطـأ:**\n"
                    f"- {e}", 
                    link_preview=False)

    except Exception as e:
        await l313l.send_message(BOTLOG_CHATID, 
            f"**- حدث خطـأ ❌**\n"
            f"**- تفاصيـل الخطـأ:**\n"
            f"- {e}")

@l313l.ar_cmd(pattern="كوبي(?:\s|$)([\s\S]*)")
async def channel_copier(event):
    catty = event.pattern_match.group(1)
    channel_username = str(catty.split(" ")[0])
    if channel_username.startswith("@"):
        channel_username = channel_username.replace("@", "")
    
    # دعم تحديد العدد
    parts = catty.split()
    if len(parts) > 1:
        try:
            limit = int(parts[1])
        except:
            limit = 10000
    else:
        limit = 10000
    
    await edit_or_reply(event, 
        f"**- جـارِ نقـل منشـورات الميديـا . . .**\n"
        f"**- مـن القنـاة @{channel_username}**\n"
        f"**- عدد المنشورات: {limit}**\n\n"
        f"**- انتظـر .. قد تستمـر العمليـة بضـع دقائـق**")
    
    copier_start = await start_copier(event.chat_id, channel_username)
  
