import re
from telethon.utils import get_display_name
from telethon.tl.types import DocumentAttributeSticker, DocumentAttributeAnimated
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from JoKeRUB import l313l
from ..core.managers import edit_or_reply
from ..sql_helper import blacklist_sql as sql
from ..utils import is_admin

plugin_category = "admin"

#copyright for JoKeRUB © 2021
@l313l.ar_cmd(incoming=True)
async def on_new_message(event):
    # تخطي الرسائل في القنوات
    if event.is_channel and not event.is_group:
        return
    
    # التحقق من أن الرسالة هي ملصق أو صورة متحركة
    if event.message.media:
        if hasattr(event.message.media, 'document'):
            attributes = event.message.media.document.attributes
            for attr in attributes:
                if isinstance(attr, DocumentAttributeSticker) or isinstance(attr, DocumentAttributeAnimated):
                    # الحصول على معرف الملف (File ID) للملصق أو الصورة المتحركة
                    file_id = event.message.media.document.id
                    # التحقق مما إذا كان المعرف موجودًا في قائمة المنع
                    if str(file_id) in sql.get_chat_blacklist(event.chat_id):
                        try:
                            await event.delete()
                            await event.reply("⌔︙ تم حذف الملصق/الصورة المتحركة لأنها محظورة.")
                        except Exception:
                            try:
                                await event.client.send_message(
                                    BOTLOG_CHATID,
                                    f"⌔︙ ليـس لدي صـلاحيات الـحذف في {get_display_name(await event.get_chat())}.\
                                    لذا سأقوم بإزالة الملصقات المحظورة من هذه الدردشة",
                                )
                            except:
                                pass
                            # إصلاح: إنشاء قائمة منفصلة قبل التعديل
                            blacklist_items = list(sql.get_chat_blacklist(event.chat_id))
                            for word in blacklist_items:
                                sql.rm_from_blacklist(event.chat_id, word.lower())
                        return

    # المنطق الأصلي لمنع الكلمات
    name = event.raw_text
    snips = sql.get_chat_blacklist(event.chat_id)
    
    # التحقق من الصلاحيات في المجموعات فقط
    if event.is_group:
        try:
            catadmin = await is_admin(event.client, event.chat_id, event.client.uid)
            if not catadmin:
                return
        except Exception:
            return
    
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                await event.delete()
                if event.is_private:
                    await event.reply("⌔︙ تم حذف الرسالة لأنها تحتوي على كلمات محظورة.")
            except Exception:
                try:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"⌔︙ ليـس لدي صـلاحيات الـحذف في {get_display_name(await event.get_chat())}.\
                        لذا سأقوم بإزالة الكلمات المحظورة من هذه الدردشة",
                    )
                except:
                    pass
                # إصلاح: إنشاء قائمة منفصلة قبل التعديل
                blacklist_items = list(snips)
                for word in blacklist_items:
                    sql.rm_from_blacklist(event.chat_id, word.lower())
            break

@l313l.ar_cmd(
    pattern="منع(?:\s|$)([\s\S]*)",
    command=("منع", plugin_category),
    info={
        "header": "To add blacklist words or stickers to database",
        "description": "The given word or sticker ID will be added to blacklist in that specific chat if any user sends then the message gets deleted.",
        "note": "To block a sticker, reply to the sticker with the command `.منع`.",
        "usage": "{tr}addblacklist <word(s) or sticker>",
        "examples": ["{tr}addblacklist fuck", "{tr}addblacklist <sticker>"],
    },
    require_admin=True,
)
async def _(event):
    "To add blacklist words or stickers to database"
    # التحقق من الصلاحيات في المجموعات فقط
    if event.is_group:
        try:
            from ..utils import is_admin
            if not await is_admin(event.client, event.chat_id, event.client.uid):
                await edit_or_reply(event, "⌔︙ هذا الأمر يتطلب صلاحيات مشرف في المجموعة.")
                return
        except Exception:
            await edit_or_reply(event, "⌔︙ حدث خطأ في التحقق من الصلاحيات.")
            return
    
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        if reply_msg.media:
            if hasattr(reply_msg.media, 'document'):
                attributes = reply_msg.media.document.attributes
                for attr in attributes:
                    if isinstance(attr, DocumentAttributeSticker) or isinstance(attr, DocumentAttributeAnimated):
                        file_id = reply_msg.media.document.id
                        sql.add_to_blacklist(event.chat_id, str(file_id))
                        await edit_or_reply(
                            event,
                            f"⌔︙ تم إضافة الملصق/الصورة المتحركة بقائمة المنع (ID: {file_id})."
                        )
                        return
    
    text = event.pattern_match.group(1)
    if not text:
        await edit_or_reply(event, "⌔︙ يرجى كتابة الكلمة أو الكلمات لمنعها.")
        return
    
    to_blacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )

    for trigger in to_blacklist:
        sql.add_to_blacklist(event.chat_id, trigger.lower())
    await edit_or_reply(
        event,
        f"⌔︙ تم اضافة {len(to_blacklist)} كلمة/كلمات في قائمة المنع بنجاح"
    )

@l313l.ar_cmd(
    pattern="الغاء منع(?:\s|$)([\s\S]*)",
    command=("الغاء منع", plugin_category),
    info={
        "header": "To remove blacklist words or stickers from database",
        "description": "The given word or sticker ID will be removed from blacklist in that specific chat",
        "note": "To unblock a sticker, reply to the sticker with the command `.الغاء منع`.",
        "usage": "{tr}rmblacklist <word(s) or sticker>",
        "examples": ["{tr}rmblacklist fuck", "{tr}rmblacklist <sticker>"],
    },
    require_admin=True,
)
async def _(event):
    "To Remove Blacklist Words or Stickers from Database."
    # التحقق من الصلاحيات في المجموعات فقط
    if event.is_group:
        try:
            from ..utils import is_admin
            if not await is_admin(event.client, event.chat_id, event.client.uid):
                await edit_or_reply(event, "⌔︙ هذا الأمر يتطلب صلاحيات مشرف في المجموعة.")
                return
        except Exception:
            await edit_or_reply(event, "⌔︙ حدث خطأ في التحقق من الصلاحيات.")
            return
    
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        if reply_msg.media:
            if hasattr(reply_msg.media, 'document'):
                attributes = reply_msg.media.document.attributes
                for attr in attributes:
                    if isinstance(attr, DocumentAttributeSticker) or isinstance(attr, DocumentAttributeAnimated):
                        file_id = reply_msg.media.document.id
                        if sql.rm_from_blacklist(event.chat_id, str(file_id)):
                            await edit_or_reply(
                                event,
                                f"⌔︙ تم إزالة الملصق/الصورة المتحركة من قائمة المنع (ID: {file_id})."
                            )
                        else:
                            await edit_or_reply(
                                event,
                                "⌔︙ الملصق/الصورة المتحركة غير موجودة في قائمة المنع."
                            )
                        return
    
    text = event.pattern_match.group(1)
    if not text:
        await edit_or_reply(event, "⌔︙ يرجى كتابة الكلمة أو الكلمات لإزالتها من المنع.")
        return
    
    to_unblacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )
    successful = sum(
        bool(sql.rm_from_blacklist(event.chat_id, trigger.lower()))
        for trigger in to_unblacklist
    )
    await edit_or_reply(
        event, f"⌔︙ تم ازالة {successful} / {len(to_unblacklist)} كلمة/كلمات من قائمة المنع بنجاح"
    )

@l313l.ar_cmd(
    pattern="قائمة المنع$",
    command=("قائمة المنع", plugin_category),
    info={
        "header": "To show the blacklist words or stickers",
        "description": "Shows you the list of blacklist words or stickers in that specific chat",
        "usage": "{tr}listblacklist",
    },
    require_admin=True,
)
async def _(event):
    "To show the blacklist words or stickers in that specific chat"
    # التحقق من الصلاحيات في المجموعات فقط
    if event.is_group:
        try:
            from ..utils import is_admin
            if not await is_admin(event.client, event.chat_id, event.client.uid):
                await edit_or_reply(event, "⌔︙ هذا الأمر يتطلب صلاحيات مشرف في المجموعة.")
                return
        except Exception:
            await edit_or_reply(event, "⌔︙ حدث خطأ في التحقق من الصلاحيات.")
            return
    
    all_blacklisted = sql.get_chat_blacklist(event.chat_id)
    OUT_STR = "⌔︙ قائمة المنع في الدردشة الحالية :\n"
    if len(all_blacklisted) > 0:
        for i, trigger in enumerate(all_blacklisted, 1):
            if trigger.isdigit() and len(trigger) > 5:
                OUT_STR += f"{i}👈 [ملصق/صورة متحركة] (ID: {trigger})\n"
            else:
                OUT_STR += f"{i}👈 `{trigger}`\n"
    else:
        OUT_STR = "⌔︙ لم تقم باضافة كلمات أو ملصقات سوداء. ارسل  `.منع` لمنع كلمة أو ملصق."
    await edit_or_reply(event, OUT_STR)

@l313l.ar_cmd(
    pattern="مسح قائمة المنع$",
    command=("مسح قائمة المنع", plugin_category),
    info={
        "header": "To clear all blacklist items from database",
        "description": "Removes all blacklisted words and stickers from the current chat",
        "usage": "{tr}clearblacklist",
    },
    require_admin=True,
)
async def _(event):
    "To clear all blacklist items from database"
    # التحقق من الصلاحيات في المجموعات فقط
    if event.is_group:
        try:
            from ..utils import is_admin
            if not await is_admin(event.client, event.chat_id, event.client.uid):
                await edit_or_reply(event, "⌔︙ هذا الأمر يتطلب صلاحيات مشرف في المجموعة.")
                return
        except Exception:
            await edit_or_reply(event, "⌔︙ حدث خطأ في التحقق من الصلاحيات.")
            return
    
    # الحصول على نسخة من القائمة قبل التعديل لتجنب الخطأ
    all_blacklisted = list(sql.get_chat_blacklist(event.chat_id))
    
    if not all_blacklisted:
        await edit_or_reply(event, "⌔︙ قائمة المنع فارغة بالفعل.")
        return
    
    # مسح جميع العناصر
    count = 0
    for item in all_blacklisted:
        if sql.rm_from_blacklist(event.chat_id, item):
            count += 1
    
    await edit_or_reply(event, f"⌔︙ تم مسح {count} عنصر من قائمة المنع بنجاح.")
