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
        "note": "To block a sticker, reply to the sticker with the command `.منع`.\nTo block a text message, reply to the message with the command `.منع`.",
        "usage": "{tr}addblacklist <word(s) or sticker or text message>",
        "examples": ["{tr}addblacklist fuck", "{tr}addblacklist <sticker>", "{tr}addblacklist (reply to message)"],
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
        
        # الحالة 1: الرد على ملصق/صورة متحركة
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
        
        # الحالة 2: الرد على رسالة نصية
        if reply_msg.text:
            # نأخذ النص من الرسالة المردود عليها
            text = reply_msg.text.strip()
            
            if not text:
                await edit_or_reply(event, "⌔︙ الرسالة المردود عليها فارغة.")
                return
            
            # نمنع النص الكامل
            sql.add_to_blacklist(event.chat_id, text.lower())
            
            await edit_or_reply(
                event,
                f"⌔︙ تم منع النص التالي:\n`{text}`"
            )
            return
    
    # الحالة 3: ليس هناك رد، نأخذ النص من الأمر نفسه
    text = event.pattern_match.group(1)
    if not text:
        await edit_or_reply(event, "⌔︙ يرجى كتابة الكلمة أو الرد على رسالة لمنعها.")
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


#   ════════════════════════════════════════════════════════════   #
#                ⌔︙ اوامر التحذير ⌔︙   #
#   ════════════════════════════════════════════════════════════   #
"""
import html

from JoKeRUB import l313l
from ..core.managers import edit_or_reply
from ..sql_helper import warns_sql as sql
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

plugin_category = "admin"

#warn
@l313l.ar_cmd(
    pattern="تحذير(?:\s|$)([\s\S]*)",
    command=("تحذير", plugin_category),
    info={
        "header": "لتحذير المستخدم.",
        "description": "سيحذر المستخدم الذي تم الرد عليه.",
        "usage": "تحذير <السبب>",
    },
)
async def _(event):
    "لتحذير المستخدم"
    warn_reason = event.pattern_match.group(1)
    if not warn_reason:
        warn_reason = "- لا يوجد سبب ، 🗒"
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**▸┊يجب الرد على الرسالة لتحذير المستخدم!**")
    
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, reasons = sql.warn_user(
        str(reply_message.sender_id), event.chat_id, warn_reason
    )
    
    if num_warns >= limit:
        sql.reset_warns(str(reply_message.sender_id), event.chat_id)
        user_id = reply_message.sender_id
        message = (
            f"**▸┊بسبب تخطي التحذيرات الـ 3 ، تم اتخاذ الإجراءات التالية ضد المستخدم 👤:**\n\n"
            f"`.كتم {user_id}`\n"
            f"`.طرد {user_id}`\n"
            f"`.تقييد {user_id}`\n"
            f"`.تقييد_مؤقت {user_id} 24h`\n\n"
            f"**يرجى اختيار الإجراء المناسب.**"
        )
        await edit_or_reply(event, message)
    else:
        reply = "**▸┊[ المستخدم 👤](tg://user?id={}) **لديه {}/{} تحذيرات، احذر!**".format(
            reply_message.sender_id, num_warns, limit
        )
        if warn_reason:
            reply += "\n▸┊سبب التحذير الأخير \n{}".format(html.escape(warn_reason))
        await edit_or_reply(event, reply)


@l313l.ar_cmd(
    pattern="التحذيرات",
    command=("التحذيرات", plugin_category),
    info={
        "header": "للحصول على قائمة تحذيرات المستخدمين.",
        "usage": "التحذير <بالرد>",
    },
)
async def _(event):
    "للحصول على قائمة تحذيرات المستخدمين."
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_delete(
            event, "**▸┊قم بالرد ع المستخدم للحصول ع تحذيراته . ☻**"
        )
    result = sql.get_warns(str(reply_message.sender_id), event.chat_id)
    if not result or result[0] == 0:
        return await edit_or_reply(event, "__▸┊هذا المستخدم ليس لديه أي تحذير! ツ__")
    num_warns, reasons = result
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    if not reasons:
        return await edit_or_reply(
            event,
            f"▸┊هذا المستخدم لديه {num_warns} / {limit} تحذيرات ، لكن لا توجد اسباب !",
        )
    text = f"▸┊هذا المستخدم لديه {num_warns} / {limit} تحذيرات ، للأسباب : ↶"
    text += "\r\n"
    text += reasons
    await event.edit(text)


@l313l.ar_cmd(
    pattern="ح(ذف)? ?التحذير$",
    command=("حذف التحذير", plugin_category),
    info={
        "header": "لحذف تحذيرات المستخدم الذي تم الرد عليه",
        "usage": [
            "{tr}ح التحذير",
            "{tr}حذف التحذير",
        ],
    },
)
async def _(event):
    "لحذف او اعادة تحذيرات المستخدم الذي تم الرد عليه"
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**▸┊يجب الرد على المستخدم أولاً!**")
    sql.reset_warns(str(reply_message.sender_id), event.chat_id)
    await edit_or_reply(event, "**▸┊تم إعادة ضبط التحذيرات!**")
""
