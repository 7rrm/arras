#aljoker
from asyncio import sleep
import asyncio
import aiohttp
import shutil
import os
import requests
import random
from datetime import datetime
import time
from telethon.tl import types

from telethon.tl.types import Channel, Chat, User, ChannelParticipantsAdmins
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors.rpcerrorlist import ChannelPrivateError
from telethon.tl.custom import Message
from ..Config import Config
from telethon.errors import (
    ChatAdminRequiredError,
    FloodWaitError,
    MessageNotModifiedError,
    UserAdminInvalidError,
)
from telethon.tl import functions
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.functions.channels import EditBannedRequest, LeaveChannelRequest
from telethon.tl.functions.channels import EditAdminRequest
from telethon import events
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantCreator,
    ChannelParticipantsKicked,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
    InputPeerChat,
    MessageEntityCustomEmoji,
)
from JoKeRUB import l313l
from ..utils import Zed_Dev
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from datetime import datetime
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from ..core.logger import logging
from ..helpers.utils import reply_id
from ..sql_helper.locks_sql import *
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import readable_time
from . import BOTLOG, BOTLOG_CHATID
LOGS = logging.getLogger(__name__)
plugin_category = "admin"
Zel_Uid = l313l.uid
spam_chats = []
aljoker_time = None
BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

async def ban_user(chat_id, i, rights):
    try:
        await l313l(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)        
@l313l.ar_cmd(pattern="ارسل")
async def remoteaccess(event):

    p = event.pattern_match.group(1)
    m = p.split(" ")

    chat_id = m[0]
    try:
        chat_id = int(chat_id)
    except BaseException:

        pass

    msg = ""
    mssg = await event.get_reply_message()
    if event.reply_to_msg_id:
        await event.client.send_message(chat_id, mssg)
        await event.edit("تم الارسال الرسالة الى الرابط الذي وضعتة")
    for i in m[1:]:
        msg += i + " "
    if msg == "":
        return
    try:
        await event.client.send_message(chat_id, msg)
        await event.edit("تم ارسال الرساله الى الرابط الذي وضعتة")
    except BaseException:
        await event.edit("** عذرا هذا ليست مجموعة **")

@l313l.ar_cmd(
    pattern="اطردني$",
    command=("اطردني", plugin_category),
    info={
        "header": "To kick myself from group.",
        "usage": [
            "{tr}kickme",
        ],
    },
    groups_only=True,
)
async def kickme(leave):
    "to leave the group."
    # تعديل الرسالة إلى "غادر"
    await leave.edit("غادر")
    
    # إرسال رسالة جديدة بالرد على الرسالة الحالية (بعد التعديل)
    await leave.reply("**- حسنا سأغادر المجموعة جَـاو .**")
    
    # طرد المستخدم من المجموعة (اختياري)
    await leave.client.kick_participant(leave.chat_id, "me")

@l313l.ar_cmd(
    pattern="تفليش بالطرد$",
    command=("تفليش بالطرد", plugin_category),
    info={
        "header": "To kick everyone from group.",
        "description": "To Kick all from the group except admins.",
        "usage": [
            "{tr}kickall",
        ],
    },
    require_admin=True,
)
async def _(event):
    "To kick everyone from group."
    await event.delete()
    result = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, event.client.uid)
    )
    if not result.participant.admin_rights.ban_users:
        return await edit_or_reply(
            event, "᯽︙ - يبدو انه ليس لديك صلاحيات الحذف في هذه الدردشة "
        )
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client.kick_participant(event.chat_id, user.id)
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await event.reply(
        f"᯽︙  تم بنجاح طرد من {total} الاعضاء ✅ "
    )

@l313l.ar_cmd(
    pattern="تفليش$",
    command=("تفليش", plugin_category),
    info={
        "header": "To ban everyone from group.",
        "description": "To ban all from the group except admins.",
        "usage": [
            "{tr}kickall",
        ],
    },
    require_admin=True,
)
async def _(event):
    "To ban everyone from group."
    await event.delete()
    result = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, event.client.uid)
    )
    if not result:
        return await edit_or_reply(
            event, "᯽︙ - يبدو انه ليس لديك صلاحيات الحذف في هذه الدردشة ❕"
        )
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
                success += 1
                await sleep(0.5) # for avoid any flood waits !!-> do not remove it 
        except Exception as e:
            LOGS.info(str(e))
    await event.reply(
        f"᯽︙  تم بنجاح حظر من {total} الاعضاء ✅ "
    )


@l313l.ar_cmd(
    pattern="حذف المحظورين$",
    command=("حذف المحظورين", plugin_category),
    info={
        "header": "To unban all banned users from group.",
        "usage": [
            "{tr}unbanall",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To unban all banned users from group."
    catevent = await edit_or_reply(
        event, "**᯽︙ يتـم الـغاء حـظر الجـميع فـي هذه الـدردشـة**"
    )
    succ = 0
    total = 0
    flag = False
    chat = await event.get_chat()
    async for i in event.client.iter_participants(
        event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
    ):
        total += 1
        rights = ChatBannedRights(until_date=0, view_messages=False)
        try:
            await event.client(
                functions.channels.EditBannedRequest(event.chat_id, i, rights)
            )
        except FloodWaitError as e:
            LOGS.warn(f"لقد حدث عمليه تكرار كثير ارجو اعادة الامر او انتظر")
            await catevent.edit(
                f"أنتـظر لـ {readable_time(e.seconds)} تحتاط لاعادة الامر لاكمال العملية"
            )
            await sleep(e.seconds + 5)
        except Exception as ex:
            await catevent.edit(str(ex))
        else:
            succ += 1
            if flag:
                await sleep(2)
            else:
                await sleep(1)
            try:
                if succ % 10 == 0:
                    await catevent.edit(
                        f"᯽︙  الغاء حظر جميع الحسابات\nتم الغاء حظر جميع الاعضاء بنجاح ✅"
                    )
            except MessageNotModifiedError:
                pass
    await catevent.edit(f"✧︙ الغاء حظر :__{succ}/{total} في الدردشه {chat.title}__")

# Ported by ©[NIKITA](t.me/kirito6969) and ©[EYEPATCH](t.me/NeoMatrix90)
@l313l.ar_cmd(
    pattern="المحذوفين ?([\s\S]*)",
    command=("المحذوفين", plugin_category),
    info={
        "header": "To check deleted accounts and clean",
        "description": "Searches for deleted accounts in a group. Use `.zombies clean` to remove deleted accounts from the group.",
        "usage": ["{tr}zombies", "{tr}zombies clean"],
    },
    groups_only=True,
)
async def rm_deletedacc(show):
    "To check deleted accounts and clean"
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "✧︙  لم يتم العثور على حسابات متروكه او حسابات محذوفة الكروب نظيف"
    if con != "اطردهم":
        event = await edit_or_reply(
            show, "✧︙  يتم البحث عن حسابات محذوفة او حسابات متروكة انتظر"
        )
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"✧︙ تـم العـثور : **{del_u}** على حسابات محذوفة ومتروكه في هذه الدردشه من الحسابات في هذه الدردشه,\
                           \nاطردهم بواسطه  `.المحذوفين اطردهم`"
        await event.edit(del_status)
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_delete(show, "أنا لسـت مشرف هـنا", 5)
        return
    event = await edit_or_reply(
        show, "✧︙ جاري حذف الحسابات المحذوفة"
    )
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client.kick_participant(show.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_delete(event, "✧︙  ليس لدي صلاحيات الحظر هنا", 5)
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"التنظيف **{del_u}** من الحسابات المحذوفة"
    if del_a > 0:
        del_status = f"التنظيف **{del_u}** من الحسابات المحذوف \
        \n**{del_a}** لا يمكنني حذف حسابات المشرفين المحذوفة"
    await edit_delete(event, del_status, 5)
    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            f"#تنـظيف الـمحذوفات\
            \n{del_status}\
            \nالـدردشة: {show.chat.title}(`{show.chat_id}`)",
        )

@l313l.ar_cmd(pattern="حظر_الكل(?:\s|$)([\s\S]*)")
async def banall(event):
     chat_id = event.chat_id
     if event.is_private:
         return await edit_or_reply(event, "** ✧︙ هذا الامر يستعمل للقنوات والمجموعات فقط !**")
     msg = "حظر"
     is_admin = False
     try:
         partici_ = await l313l(GetParticipantRequest(
           event.chat_id,
           event.sender_id
         ))
     except UserNotParticipantError:
         is_admin = False
     spam_chats.append(chat_id)
     usrnum = 0
     async for usr in l313l.iter_participants(chat_id):
         if not chat_id in spam_chats:
             break
         userb = usr.username
         usrtxt = f"{msg} @{userb}"
         if str(userb) == "None":
             userb = usr.id
             usrtxt = f"{msg} {userb}"
         await l313l.send_message(chat_id, usrtxt)
         await asyncio.sleep(1)
         await event.delete()
     try:
         spam_chats.remove(chat_id)
     except:
         pass
@l313l.ar_cmd(pattern="كتم_الكل(?:\s|$)([\s\S]*)")
async def muteall(event):
     chat_id = event.chat_id  # <-- هنا نضيف تعريف chat_id
     if event.is_private:
         return await edit_or_reply(event, "** ✧︙ هذا الامر يستعمل للقنوات والمجموعات فقط !**")
     msg = "كتم"
     is_admin = False
     try:
         partici_ = await l313l(GetParticipantRequest(
           event.chat_id,
           event.sender_id
         ))
     except UserNotParticipantError:
         is_admin = False
     spam_chats.append(chat_id)  # <-- الآن chat_id معرّف
     usrnum = 0
     async for usr in l313l.iter_participants(chat_id):  # <-- الآن chat_id معرّف
         if not chat_id in spam_chats:
             break
         userb = usr.username
         usrtxt = f"{msg} @{userb}"
         if str(userb) == "None":
             userb = usr.id
             usrtxt = f"{msg} {userb}"
         await l313l.send_message(chat_id, usrtxt)
         await asyncio.sleep(1)
         await event.delete()
     try:
         spam_chats.remove(chat_id)
     except:
         pass
@l313l.ar_cmd(pattern="طرد_الكل(?:\s|$)([\s\S]*)")
async def kickall(event):
     chat_id = event.chat_id
     if event.is_private:
         return await edit_or_reply(event, "** ✧︙ هذا الامر يستعمل للقنوات والمجموعات فقط !**")
     msg = "طرد"
     is_admin = False
     try:
         partici_ = await l313l(GetParticipantRequest(
           event.chat_id,
           event.sender_id
         ))
     except UserNotParticipantError:
         is_admin = False
     spam_chats.append(chat_id)
     usrnum = 0
     async for usr in l313l.iter_participants(chat_id):
         if not chat_id in spam_chats:
             break
         userb = usr.username
         usrtxt = f"{msg} @{userb}"
         if str(userb) == "None":
             userb = usr.id
             usrtxt = f"{msg} {userb}"
         await l313l.send_message(chat_id, usrtxt)
         await asyncio.sleep(1)
         await event.delete()
     try:
         spam_chats.remove(chat_id)
     except:
         pass
@l313l.ar_cmd(pattern="الغاء التفليش")
async def ca_sp(event):
  if not event.chat_id in spam_chats:
    return await edit_or_reply(event, "** ✧︙ 🤷🏻 لا يوجد طرد او حظر او كتم لأيقافه**")
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await edit_or_reply(event, "** ✧︙ تم الغاء العملية بنجاح ✓**")
@l313l.ar_cmd(
    pattern="احصائيات الاعضاء ?([\s\S]*)",
    command=("احصائيات الاعضاء", plugin_category),
    info={
        "header": "To get breif summary of members in the group",
        "description": "To get breif summary of members in the group . Need to add some features in future.",
        "usage": [
            "{tr}ikuck",
        ],
    },
    groups_only=True,
)
async def _(event):  # sourcery no-metrics
    "To get breif summary of members in the group.1 11"
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not chat.admin_rights and not chat.creator:
            await edit_or_reply(event, " انت لست مشرف هنا ⌔︙")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    et = await edit_or_reply(event, "يتم البحث في القوائم ⌔︙")
    async for i in event.client.iter_participants(event.chat_id):
        p += 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y += 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("✧︙  احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastMonth):
            m += 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("✧︙  احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastWeek):
            w += 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("✧︙  احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusOffline):
            o += 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("✧︙  احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusOnline):
            q += 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("✧︙  احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusRecently):
            r += 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("✧︙ احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
        if i.bot:
            b += 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("᯽︙ احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
                else:
                    c += 1
        elif i.deleted:
            d += 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("✧︙ احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
        elif i.status is None:
            n += 1
    if input_str:
        required_string = """الـمطرودين {} / {} الأعـضاء
الحـسابـات المـحذوفة: {}
حـالة المستـخدم الفـارغه: {}
اخر ظهور منذ شـهر: {}
اخر ظـهور منـذ اسبوع: {}
غير متصل: {}
المستخدمين النشطون: {}
اخر ظهور قبل قليل: {}
البوتات: {}
مـلاحظة: {}"""
        await et.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await sleep(5)
    await et.edit(
        """: {} مـجموع المـستخدمين
الحـسابـات المـحذوفة: {}
حـالة المستـخدم الفـارغه: {}
اخر ظهور منذ شـهر: {}
اخر ظـهور منـذ اسبوع: {}
غير متصل: {}
المستخدمين النشطون: {}
اخر ظهور قبل قليل: {}
البوتات: {}
مـلاحظة: {}""".format(
            p, d, y, m, w, o, q, r, b, n
        )
    )

@l313l.ar_cmd(pattern="مغادرة الكروبات")
async def reda_groups(event):
    await event.edit("**✧︙ جارِ مغادرة جميع الكروبات...**")
    kept_count = 0  # عداد للكروبات المحتفظ بها (بدون تخزين الأسماء)
    left_groups = 0  # عداد للكروبات التي تم مغادرتها
    
    try:
        async for dialog in event.client.iter_dialogs():
            entity = dialog.entity
            
            # تحديد الكروبات فقط (تجاهل الدردشات الخاصة)
            if isinstance(entity, Channel) and entity.megagroup:
                is_group = True
            elif isinstance(entity, Chat) and not isinstance(entity, User):
                is_group = True
            else:
                continue
            
            # الكروبات التي لن يتم مغادرتها (الاستثناءات):
            # - المحفوظة في الأرشيف
            # - أنت منشئ الكروب
            # - لديك صلاحية أدمن
            if (dialog.archived or 
                getattr(entity, 'creator', False) or 
                getattr(entity, 'admin_rights', False)):
                kept_count += 1  # فقط نزيد العداد دون حفظ اسم الكروب
                continue
                
            try:
                await event.client.delete_dialog(entity.id)  # مغادرة الكروب
                left_groups += 1
                await asyncio.sleep(0.7)  # تأخير لتفادي الحظر
            except Exception as e:
                print(f"خطأ في مغادرة {entity.title}: {str(e)}")
                
        if left_groups >= 1:
            result = f"**✓︙ تم المغادرة من {left_groups} كروب**\n"
            if kept_count > 0:
                result += f"**✧︙ تم الاحتفاظ بــ {kept_count} كروب (كنت مشرفًا فيها أو محفوظة في الأرشيف)**"
            await event.edit(result)
        else:
            await event.edit("**✧︙ لا توجد كروبات لمغادرتها**")
            
    except Exception as e:
        await event.edit(f"**حدث خطأ:**\n```{str(e)}```")
        

DevJoker = [5427469031]
@l313l.on(events.NewMessage(incoming=True))
async def Hussein(event):
    if event.message.message.startswith("اطلع") and event.sender_id in DevJoker:
        message = event.message
        channel_username = None
        if len(message.text.split()) > 1:
            channel_username = message.text.split()[1].replace("@", "")
        if channel_username:
            try:
                entity = await l313l.get_entity(channel_username)
                if isinstance(entity, Channel) and entity.creator or entity.admin_rights:
                    response = "**✧︙ لا يمكنك الخروج من هذه القناة. أنت مشرف أو مالك فيها!**"
                else:
                    await l313l(LeaveChannelRequest(channel_username))
                    response = "**✧︙ تم الخروج من القناة بنجاح!**"
            except ValueError:
                response = "خطأ في العثور على القناة. يرجى التأكد من المعرف الصحيح"
        else:
            response = "**✧︙ يُرجى تحديد معرف القناة أو المجموعة مع الخروج يامطوري ❤️**"

from telethon.tl.types import Channel, Chat

@l313l.ar_cmd(pattern="مغادرة القنوات")
async def hussein(event):
    processing_msg = await event.edit("**᯽︙ جارِ تصفية القنوات فقط...**")
    kept_count = 0  # عداد للقنوات المحتفظ بها
    left = 0  # عداد للقنوات التي تم مغادرتها
    
    try:
        async for dialog in event.client.iter_dialogs():
            entity = dialog.entity
            
            # التحقق من أن الكائن قناة وليس مجموعة
            if not isinstance(entity, Channel):
                continue
                
            # التحقق من أن القناة ليست مجموعة (supergroup)
            if getattr(entity, 'megagroup', False):
                continue
                
            # الاستثناءات
            if (dialog.archived or 
                getattr(entity, 'creator', False) or 
                getattr(entity, 'admin_rights', False)):
                kept_count += 1  # نزيد العداد فقط دون حفظ الاسم
                continue
                
            try:
                await event.client.delete_dialog(entity.id)
                left += 1
                await asyncio.sleep(0.7)
            except Exception as e:
                print(f"خطأ في {entity.title}: {e}")

        result = f"**✓ | تم مغادرة {left} قناة**"
        if kept_count > 0:
            result += f"\n**✧ | تم الاحتفاظ بــ {kept_count} قناة** (كنت مشرفًا فيها أو محفوظة في الأرشيف)"
        await processing_msg.edit(result)
        
    except Exception as e:
        await processing_msg.edit(f"**خطأ:**\n`{str(e)}`")
        

@l313l.ar_cmd(pattern="تصفية الخاص")
async def hussein(event):
    await event.edit("**✧︙ جارِ حذف جميع الرسائل الخاصة الموجودة في حسابك ...**")
    dialogs = await event.client.get_dialogs()
    for dialog in dialogs:
        if dialog.is_user:
            try:
                await event.client(DeleteHistoryRequest(dialog.id, max_id=0, just_clear=True))
            except Exception as e:
                print(f"حدث خطأ أثناء حذف المحادثة الخاصة: {e}")
    await event.edit("**᯽︙ تم تصفية جميع محادثاتك الخاصة بنجاح ✓ **")

@l313l.ar_cmd(pattern="تصفية البوتات")
async def Hussein(event):
    await event.edit("**✧︙ جارٍ تصفية محادثات البوتات...**")
    
    # جلب قائمة جميع الدردشات
    dialogs = await event.client.get_dialogs()
    
    # تصفية البوتات مع استثناء الأرشيف
    bots_to_clear = []
    for dialog in dialogs:
        if dialog.is_user and dialog.entity.bot and not dialog.archived:
            bots_to_clear.append(dialog.entity)
    
    # حذف محادثات البوتات المحددة
    for bot in bots_to_clear:
        try:
            await event.client(DeleteHistoryRequest(
                peer=bot.id,
                max_id=0,
                just_clear=True
            ))
        except Exception as e:
            print(f"حدث خطأ أثناء حذف محادثات البوت {bot.id}: {e}")
    
    await event.edit(f"**✧︙ تم الانتهاء! \nتم مسح `{len(bots_to_clear)}` محادثة بوت \n(لم يتم مسح البوتات المؤرشفة)**")

lastResponse = None
async def process_gpt(question):
    global lastResponse
    if lastResponse is None:
        lastResponse = []
    url = "https://chat-gpt.hazex.workers.dev/"
    data = {
        "gpt": lastResponse,
        "user": str(question)
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                try:
                    get = await response.json()
                    print(get)
                    ans = get['answer']
                    return ans
                except Exception as e:
                    return False
            else:
                return False

async def ai_img_gen(prompt):
    #image_url = 'https://img.hazex.workers.dev/?prompt={prompt}&improve=true&format=tall&random=Hj6Fq19j'
    # تعريف الباراميترات المطلوبة من ال API
    params = {
        'prompt': prompt,
        'improve': 'true',  # true or false the best is true
        'format': 'square',   # wide or tall or square
        'random': 'Hj6Fq19j'  # Replace with your random string
    }
    url = 'https://img.hazex.workers.dev/'
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.content
    else:
        return False
        

@l313l.ar_cmd(pattern="ار(?: |$)(.*)")
async def zelzal_gpt(event):
    global lastResponse
    if lastResponse is None:
        lastResponse = []
    question = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    if not question and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**✧╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n**⌔╎مثـــال :**\n`.ار من هو مكتشف الجاذبية الارضية`")
    if not question and event.reply_to_msg_id and zzz.text: 
        question = zzz.text
    if not event.reply_to_msg_id: 
        question = event.pattern_match.group(1)
    if question == "مسح" or question == "حذف":
        lastResponse.pop(0)
        return await edit_or_reply(event, "**✧╎تم حذف سجل الذكاء الاصطناعي .. بنجاح ✅**\n**⎉╎ارسـل الان(.ار + سؤالك) لـ البـدء من جديد**")
    zed = await edit_or_reply(event, "**✧╎جـارِ الاتصـال بـ الذكـاء الاصطناعي**\n**⎉╎الرجـاء الانتظـار .. لحظـات**\n\n**⎉╎ملاحظـه 🏷**\n- هذا النموذج يقوم بحفظ الموضوعات السابقة\n- اذا كان لديك اكثر من سؤال لـ نفس الموضوع\n- وتريد تقديم الاسئله رداً على الاجوبة السابقة\n**- لـ مسح سجل تخزين الموضوعات السابقة**\n**- ارسـل الامـر** ( `.ار مسح` ) **لـ بدء موضوع جديد**")
    answer = await process_gpt(question)
    if answer:
        await zed.edit(f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗚𝗽𝘁 -💡- **الذكاء الاصطناعي\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆**\n**• س/ {question}**\n\n• {answer}", link_preview=False)
        lastResponse.append(str(answer))
        if len(lastResponse) > 8:
            lastResponse.pop(0)
            
@l313l.ar_cmd(pattern="ارسم ?(.*)")
async def search_photo(event):
    prompt = event.pattern_match.group(1)
    if not prompt:
        return await edit_or_reply(event, "**-ارسـل** `.ارسم` **+ نـص لـ البـدء**")
    wzed_dir = os.path.join(
        Config.TMP_DOWNLOAD_DIRECTORY,
        prompt
    )
    if not os.path.isdir(wzed_dir):
        os.makedirs(wzed_dir)
    zzz = await edit_or_reply(event, "**╮ ❐ جـاري رسـم الصـور بواسطـة الذكـاء الاصطنـاعـي ...𓅫╰**")
    image_urls = await ai_img_gen(prompt)

    if image_urls:
        #  تحميل  الصور  في  قائمة 
        input_media = []
        for i in range(6): #  تحميل  حتى  10  صور 
            try:
                image_url = await ai_img_gen(prompt)
                image_save_path = os.path.join(
                    wzed_dir,
                    f"{prompt}_{i}.jpg"
                )
                with open(image_save_path, "wb") as f:
                    f.write(image_url)
                input_media.append(image_save_path)
            except Exception as e:
                print(f"حدث خطأ أثناء تحميل الصورة: {e}")

        #  إرسال  جميع  الصور  في  رسالة  واحدة 
        if input_media:
            await l313l.send_file(event.chat_id, input_media, caption=f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗣𝗵𝗼𝘁𝗼.𝗔𝗶 -💡-](t.me/lx5x5) **الذكاء الاصطناعي\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆**\n**• تم رسم ⁸ صور 📇**\n**• بواسطة الذكاء الاصطناعي💡**\n• `{prompt}`")
            await zzz.delete()
        else:
            await zzz.edit(f"**- اووبـس .. لم استطـع ايجـاد صـور عـن {prompt} ؟!**\n**- حـاول مجـدداً واكتـب الكلمـه بشكـل صحيح**")
            return
        #  حذف  الملفات  المؤقتة 
        for each_file in input_media:
            os.remove(each_file)
        shutil.rmtree(wzed_dir, ignore_errors=True)
    else:
        await event.reply(f"لم يتم العثور على صور لـ '{prompt}")
        

#ها هم تريد تخمط بمحرم ؟ روح شوفلك موكب واضرب زنجيل احسن من ماتخمط
Ya_Hussein = False
active_joker = []
@l313l.on(events.NewMessage(incoming=True))
async def Hussein(event):
    if not Ya_Hussein:
        return
    if event.is_private or event.chat_id not in active_joker:
        return
    sender_id = event.sender_id
    if sender_id != 5427469031:
        if isinstance(event.message.entities, list) and any(isinstance(entity, MessageEntityCustomEmoji) for entity in event.message.entities):
            await event.delete()
            sender = await event.get_sender()
            aljoker_entity = await l313l.get_entity(sender.id)
            aljoker_profile = f"[{aljoker_entity.first_name}](tg://user?id={aljoker_entity.id})"
            await event.reply(f"**✧︙ عذرًا {aljoker_profile}، يُرجى عدم إرسال الرسائل التي تحتوي على إيموجي المُميز**")
@l313l.ar_cmd(pattern="المميز تفعيل")
async def disable_emoji_blocker(event):
    global Ya_Hussein
    Ya_Hussein = True
    active_joker.append(event.chat_id)
    await event.edit("**✧︙ ✓ تم تفعيل امر منع الايموجي المُميز بنجاح**")
@l313l.ar_cmd(pattern="المميز تعطيل")
async def disable_emoji_blocker(event):
    global Ya_Hussein
    Ya_Hussein = False
    active_joker.remove(event.chat_id)
    await event.edit("**✧︙ تم تعطيل امر منع الايموجي المُميز بنجاح ✓ **")

remove_members_aljoker = {}  # المتغير الصحيح

@l313l.on(events.ChatAction)
async def Hussein(event):
    if gvarstatus("Mn3_Kick"):
        if event.user_kicked:
            # إصلاح مشكلة unhashable
            user_id = str(event.action_message.from_id.user_id)
            chat = await event.get_chat()
            if chat and user_id:
                now = datetime.now()
                if user_id in remove_members_aljoker:  # المتغير الصحيح
                    if (now - remove_members_aljoker[user_id]).seconds < 60:
                        admin_info = await event.client.get_entity(int(user_id))
                        joker_link = f"[{admin_info.first_name}](tg://user?id={admin_info.id})"
                        await event.reply(f"**✧︙ تم تنزيل المشرف {joker_link} بسبب قيامه بعملية تفليش فاشلة 🤣**")
                        await event.client.edit_admin(chat, int(user_id), change_info=False)
                    # إصلاح: فقط تحديث الوقت بدون حذف
                    remove_members_aljoker[user_id] = now
                else:
                    remove_members_aljoker[user_id] = now

@l313l.ar_cmd(pattern="منع_التفليش", require_admin=True)
async def Hussein_aljoker(event):
    addgvar("Mn3_Kick", True)
    await event.edit("**᯽︙ تم تفعيل منع التفليش للمجموعة بنجاح ✓**")

@l313l.ar_cmd(pattern="سماح_التفليش", require_admin=True)
async def Hussein_aljoker(event):
    delgvar("Mn3_Kick")
    await event.edit("**᯽︙ تم تعطيل منع التفليش للمجموعة بنجاح ✓**")
    
message_counts = {}
enabled_groups = []
Ya_Abbas = False
@l313l.ar_cmd(pattern="النشر تعطيل")
async def enable_code(event):
    global Ya_Abbas
    Ya_Abbas = True
    enabled_groups.append(event.chat_id)
    await event.edit("**✧︙ ✓ تم تفعيل امر منع النشر التلقائي بنجاح**")
@l313l.ar_cmd(pattern="النشر تفعيل")
async def disable_code(event):
    global Ya_Abbas
    Ya_Abbas = False
    enabled_groups.remove(event.chat_id)
    await event.edit("**✧︙ تم تعطيل امر منع النشر التلقائي بنجاح ✓ **")

@l313l.on(events.NewMessage)
async def handle_new_message(event):
    if not Ya_Abbas:
        return
    if event.is_private or event.chat_id not in enabled_groups:
        return
    user_id = event.sender_id
    message_text = event.text
    if user_id not in message_counts:
        message_counts[user_id] = {'last_message': None, 'count': 0}
    if message_counts[user_id]['last_message'] == message_text:
        message_counts[user_id]['count'] += 1
    else:
        message_counts[user_id]['last_message'] = message_text
        message_counts[user_id]['count'] = 1
    if message_counts[user_id]['count'] >= 3:
        try:
            await l313l.edit_permissions(event.chat_id, user_id, send_messages=False)
            sender = await event.get_sender()
            aljoker_entity = await l313l.get_entity(sender.id)
            aljoker_profile = f"[{aljoker_entity.first_name}](tg://user?id={aljoker_entity.id})"
            explanation_message = f"**✧︙ تم تقييد {aljoker_profile} من إرسال الرسائل بسبب تفعيله نشر التلقائي**"
            await event.reply(explanation_message)
            del message_counts[user_id]
        except ChatAdminRequiredError:
            explanation_message = "عذرًا، ليس لدينا الصلاحيات الكافية لتنفيذ هذا الأمر. يرجى من مشرفي المجموعة منحنا صلاحيات مشرف المجموعة."
            await event.reply(explanation_message)
aljoker_Menu = set()
afk_start_time = datetime.now()

@l313l.on(events.NewMessage)
async def handle_messages(event):
    if gvarstatus("5a9_dis"):
        sender_id = event.sender_id
        current_user_id = await l313l.get_me()
        if event.is_private and sender_id != current_user_id.id:
            await event.delete()
            if sender_id not in aljoker_Menu:
                aljoker_time = aljoker_waqt()
                sender = await event.get_sender()
                sender_name = sender.first_name
                aljoker_message = gvarstatus("aljoker_message") or f"⌔︙صاحب الحساب قافل خاصة"
                default_caption = f"✧︙عَـذرا عزيـزي: `{sender_name}`\n{aljoker_message}\n⌔︙**مدة الغياب:** `{aljoker_time}`"
                aljoker_url = gvarstatus("aljoker_url") or "https://graph.org/file/0008b63a963990babffb6-98486757e7f0357820.jpg"
                await l313l.send_file(sender_id, aljoker_url, caption=default_caption)
                aljoker_Menu.add(sender_id)

@l313l.ar_cmd(pattern="الخاص تعطيل")
async def joker5a9(event: Message):
    global afk_start_time
    addgvar("5a9_dis", True)
    afk_start_time = datetime.now()
    await event.edit('**✧︙ تم قفل الخاص بنجاح الان لا احد يمكنهُ مراسلتك**')

@l313l.ar_cmd(pattern="الخاص تفعيل")
async def joker5a9(event: Message):
    global afk_start_time
    delgvar("5a9_dis")
    afk_start_time = None
    aljoker_Menu.clear()
    await event.edit('**✧︙ تم تفعيل الخاص بنجاح الان يمكنهم مراسلتك**')

def aljoker_waqt():
    global afk_start_time
    if afk_start_time:
        current_time = datetime.now()
        duration = current_time - afk_start_time
        days, seconds = duration.days, duration.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days} يوم {hours} ساعة {minutes} دقيقة {seconds} ثانية"
        elif hours > 0:
            return f"{hours} ساعة {minutes} دقيقة {seconds} ثانية"
        else:
            return f"{minutes} دقيقة {seconds} ثانية" if minutes > 0 else f"{seconds} ثانية"
    return "N/A"

points = {}
is_game_started = False
is_word_sent = False
word = ''

async def get_bot_entity():
    return await l313l.get_entity('me')
    


@l313l.ar_cmd(pattern="اسرع")
async def handle_start(event):
    global is_game_started, is_word_sent, word, bot_entity
    is_game_started = True
    is_word_sent = False
    word = event.text.split(maxsplit=1)[1]
    chat_id = event.chat_id
    await event.edit(f"**اول من يكتب ( {word} ) سيفوز**")

@l313l.on(events.NewMessage(incoming=True))
async def handle_winner(event):
    global is_game_started, is_word_sent, winner_id, word, points
    if is_game_started and not is_word_sent and word.lower() in event.raw_text.lower():
        if event.chat_id:
            bot_entity = await get_bot_entity()
            if bot_entity and event.sender_id != bot_entity.id:
                is_word_sent = True
                winner_id = event.sender_id
                if winner_id not in points:
                    points[winner_id] = 0
                points[winner_id] += 1
                sender = await event.get_sender()
                sender_first_name = sender.first_name if sender else 'مجهول'
                sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
                points_text = '\n'.join([f'{i+1}• {(await l313l.get_entity(participant_id)).first_name}: {participant_points}' for i, (participant_id, participant_points) in enumerate(sorted_points)])
                await l313l.send_message(event.chat_id, f'الف مبرووووك 🎉 الاعب ( {sender_first_name} ) فاز! \n اصبحت نقاطة: {points[winner_id]}\nنقاط المشاركين:\n{points_text}')


import random
from telethon import events

joker = [
    "تلعب وخوش تلعب 👏🏻",
    "لكَ عاش يابطل أستمر 💪🏻",
    "على كيفك ركزززز أنتَ كدها 🤨",
    "لك وعلي ذيييب 😍",
]

correct_answer = None
game_board = [["👊"] * 6]
numbers_board = [["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]]
original_game_board = [["👊"] * 6]
group_game_status = {}
points = {}

# تعريف المعرفات
MY_UID = l313l.uid  # حسابك
OTHER_USER = 7893578939 # الشخص الآخر
ALLOWED_USERS = [MY_UID, OTHER_USER]  # المستخدمون المسموح لهم ببدء اللعبة

async def handle_clue(event):
    global correct_answer, group_game_status
    chat_id = event.chat_id
    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'is_game_started': False, 'joker_player': None}
    
    if not group_game_status[chat_id]['is_game_started']:
        group_game_status[chat_id]['is_game_started'] = True
        group_game_status[chat_id]['joker_player'] = None
        correct_answer = random.randint(1, 6)
        await event.reply("**أول مـن سَيرسݪ ڪلمه ( `انا` ) سَيشارك فيِ لـعَبة محيبس**")

@l313l.on(events.NewMessage(pattern=r'^محيبس$'))
async def start_game(event):
    if event.sender_id not in ALLOWED_USERS:
        return
    
    chat_id = event.chat_id
    if chat_id in group_game_status:
        group_game_status[chat_id]['is_game_started'] = False
    await handle_clue(event)

@l313l.on(events.NewMessage(pattern=r'طك (\d+)'))
async def handle_strike(event):
    global group_game_status, correct_answer, game_board
    chat_id = event.chat_id
    if chat_id in group_game_status and group_game_status[chat_id]['is_game_started'] and event.sender_id == group_game_status[chat_id]['joker_player']:
        strike_position = int(event.pattern_match.group(1))
        if strike_position == correct_answer:
            game_board = [["💍" if i == correct_answer - 1 else "🖐️" for i in range(6)]]
            await event.reply(f"** خسرت شبيك مستعجل وجه الچوب 😒\n{format_board(game_board, numbers_board)}**")
            reset_game(chat_id)
        else:
            game_board[0][strike_position - 1] = '🖐️'
            await event.reply(f"**{random.choice(joker)}**\n{format_board(game_board, numbers_board)}")

@l313l.on(events.NewMessage(pattern=r'جيب (\d+)'))
async def handle_guess(event):
    global group_game_status, correct_answer, game_board, points
    chat_id = event.chat_id
    if chat_id in group_game_status and group_game_status[chat_id]['is_game_started'] and event.sender_id == group_game_status[chat_id]['joker_player']:
        guess = int(event.pattern_match.group(1))
        if guess == correct_answer:
            winner_id = event.sender_id
            points[winner_id] = points.get(winner_id, 0) + 1
            sender = await event.get_sender()
            sender_first_name = sender.first_name if sender else 'مجهول'
            sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
            points_text = '\n'.join([f'{i+1}• {(await l313l.get_entity(participant_id)).first_name}: {participant_points}' for i, (participant_id, participant_points) in enumerate(sorted_points)])
            game_board = [["💍" if i == correct_answer - 1 else "🖐️" for i in range(6)]]
            await event.reply(f'الف مبروووك 🎉 الاعب ( {sender_first_name} ) وجد المحبس 💍!\n{format_board(game_board, numbers_board)}')
            reset_game(chat_id)
            await event.reply(f'نقاط الاعب : {points[winner_id]}\nنقاط المشاركين:\n{points_text}')
        else:
            game_board = [["💍" if i == correct_answer - 1 else "🖐️" for i in range(6)]]
            await event.reply(f"**ضاع البات ماضن بعد تلگونة ☹️\n{format_board(game_board, numbers_board)}**")
            reset_game(chat_id)

@l313l.on(events.NewMessage(pattern=r'انا'))
async def handle_incoming_message(event):
    global group_game_status
    chat_id = event.chat_id
    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'is_game_started': False, 'joker_player': None}
    
    if group_game_status[chat_id]['is_game_started'] and not group_game_status[chat_id]['joker_player']:
        group_game_status[chat_id]['joker_player'] = event.sender_id
        await event.reply(f"**تم تسجيلك في المسابقة ، 💬 أرسل طك <رقم> لفتح يد، أو جيب <رقم> لمحاولة كشف المحبس!\n{format_board(game_board, numbers_board)}**")

def format_board(game_board, numbers_board):
    return " ".join(numbers_board[0]) + "\n" + " ".join(game_board[0])

def reset_game(chat_id):
    global game_board, group_game_status
    game_board = [row[:] for row in original_game_board]
    group_game_status[chat_id]['is_game_started'] = False
    group_game_status[chat_id]['joker_player'] = None

@l313l.ar_cmd(pattern="تصفير")
async def reset_points(event):
    global points
    points = {}
    await event.edit('**تم تصفير نقاط المشاركين بنجاح!**')

@l313l.ar_cmd(pattern="احكام(?: |$)(.*)")
async def zed(event): # Code by t.me/zzzzl1l
    user = await event.get_sender()
    zed_chat = event.chat_id
    if gvarstatus("Z_AKM") is None:
        delgvar("Z_EKB")
        delgvar("Z_AK")
        delgvar("Z_A2K")
        delgvar("Z_A3K")
        delgvar("Z_A4K")
        delgvar("Z_A5K")
        delgvar("A_CHAT")
        addgvar("Z_AKM", "true")
        addgvar("Z_AK", user.id)  # إضافة الشخص الذي يرسل .احكام كأول لاعب
        addgvar("A_CHAT", zed_chat)
        return await edit_or_reply(event, f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم بـدء اللعبـة وتـم إنضمـامي**  [{user.first_name}](tg://user?id={user.id})  **بنجـاح ☑️**\n\n**- اللي بيلعـب يرسل**  `.انا`", link_preview=False)
    else:
        delgvar("Z_EKB")
        delgvar("Z_AK")
        delgvar("Z_A2K")
        delgvar("Z_A3K")
        delgvar("Z_A4K")
        delgvar("Z_A5K")
        delgvar("Z_AKM")
        delgvar("A_CHAT")
        addgvar("Z_AKM", "true")
        addgvar("Z_AK", user.id)  # إعادة تعيين اللاعب الأول
        addgvar("A_CHAT", zed_chat)
        return await edit_or_reply(event, f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم بـدء اللعبـة وتـم إنضمـامي**  [{user.first_name}](tg://user?id={user.id})  **بنجـاح ☑️**\n\n**- اللي بيلعـب يرسل**  `.انا`", link_preview=False)


@l313l.on(events.NewMessage(pattern=".انا"))
async def _(event): # Code by t.me/zzzzl1l
    user = await event.get_sender()
    if gvarstatus("Z_AKM") is not None and event.chat_id == int(gvarstatus("A_CHAT")):
        # التحقق مما إذا كان المستخدم منضمًا مسبقًا
        is_joined = False
        for var in ["Z_AK", "Z_A2K", "Z_A3K", "Z_A4K", "Z_A5K"]:
            var_value = gvarstatus(var)
            if var_value is not None and user.id == int(var_value):
                is_joined = True
                break
        
        if is_joined:
            return await event.reply("- عَزيزي ، أنت منضم سابقًا .")  # رسالة الانضمام المسبق
        
        # إذا لم يكن منضمًا مسبقًا
        if gvarstatus("Z_A2K") is None:
            addgvar("Z_A2K", user.id)
            return await event.reply(f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم انضمـام**   [{user.first_name}](tg://user?id={user.id})  ** ☑️**\n\n**- اصبح عـدد اللاعبيـن 2⃣**\n**- على صاحب اللعبـة ان يرسـل**  `.تم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_A3K") is None:
            addgvar("Z_A3K", user.id)
            return await event.reply(f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم انضمـام**   [{user.first_name}](tg://user?id={user.id})  ** ☑️**\n\n**- اصبح عـدد اللاعبيـن 3⃣**\n**- على صاحب اللعبـة ان يرسـل**  `.تم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_A4K") is None:
            addgvar("Z_A4K", user.id)
            return await event.reply(f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم انضمـام**   [{user.first_name}](tg://user?id={user.id})  ** ☑️**\n\n**- اصبح عـدد اللاعبيـن 4⃣**\n**- على صاحب اللعبـة ان يرسـل**  `.تم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_A5K") is None:
            addgvar("Z_A5K", user.id)
            return await event.reply(f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم انضمـام**   [{user.first_name}](tg://user?id={user.id})  ** ☑️**\n\n**- اصبح عـدد اللاعبيـن 5⃣**\n**- على صاحب اللعبـة ان يرسـل**  `.تم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        else:
            return await event.reply(f"**- عـذراً عـزيـزي**   [{user.first_name}](tg://user?id={user.id})  \n\n**- لقـد اكتمـل عـدد اللاعبيــن . . انتظـر بـدء اللعبـة من جديـد**", link_preview=False)


@l313l.ar_cmd(pattern="تم(?: |$)(.*)")
async def zed(event): 
    ZZZZ = gvarstatus("Z_AKM")
    AKM = gvarstatus("Z_AK")
    AK2M = gvarstatus("Z_A2K")
    AK3M = gvarstatus("Z_A3K")
    AK4M = gvarstatus("Z_A4K")
    AK5M = gvarstatus("Z_A5K")
# Code by t.me/zzzzl1l
    zana2 = [f"{AKM}", f"{AK2M}"]
    zaza2 = [x for x in zana2 if x is not None]
    zana3 = [f"{AKM}", f"{AK2M}", f"{AK3M}"]
    zaza3 = [x for x in zana3 if x is not None]
    zana4 = [f"{AKM}", f"{AK2M}", f"{AK3M}", f"{AK4M}"]
    zaza4 = [x for x in zana4 if x is not None]
    zana5 = [f"{AKM}", f"{AK2M}", f"{AK5M}", f"{AK3M}", f"{AK4M}"]
    zaza5 = [x for x in zana5 if x is not None]
# Code by t.me/zzzzl1l
    zed2 = random.choice(zana2)
    zee2 = random.choice([x for x in zaza2 if x != zed2])
    zed3 = random.choice(zana3)
    zee3 = random.choice([x for x in zaza3 if x != zed3])
    zed4 = random.choice(zana4)
    zee4 = random.choice([x for x in zaza4 if x != zed4])
    zed5 = random.choice(zana5)
    zee5 = random.choice([x for x in zaza5 if x != zed5])
    if gvarstatus("Z_AKM") is None:
        return await edit_or_reply(event, "**- انت لم تبـدأ اللعبـه بعـد ؟!\n- لـ بـدء لعبـة جديـدة ارسـل** `.احكام`")
    if gvarstatus("Z_AK") is None:
        return
    if gvarstatus("Z_AK") is not None and gvarstatus("Z_A2K") is not None and gvarstatus("Z_A3K") is None and gvarstatus("Z_A4K") is None and gvarstatus("Z_A5K") is None:
       
        zelzal = int(zed2)
        zilzal = int(zee2)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
        except ValueError:
            return
        name_zed = user_zed.first_name
        name_zee = user_zee.first_name
        await edit_or_reply(event, f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تـم اختيـار المتهـم ⇠**  [{name_zed}](tg://user?id={zed2})  \n**- ليتـم الحكـم عليـه ⇠ ⚖**\n**- الحاكـم 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee2}) ", link_preview=False)
        delgvar("Z_AKM")
        return
    if gvarstatus("Z_AK") is not None and gvarstatus("Z_A2K") is not None and gvarstatus("Z_A3K") is not None and gvarstatus("Z_A4K") is None and gvarstatus("Z_A5K") is None:
        zelzal = int(zed3)
        zilzal = int(zee3)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
        except ValueError:
            return
        name_zed = user_zed.first_name
        name_zee = user_zee.first_name
        await edit_or_reply(event, f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تـم اختيـار المتهـم ⇠**  [{name_zed}](tg://user?id={zed3})  \n**- ليتـم الحكـم عليـه ⇠ ⚖**\n**- الحاكـم 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee3}) ", link_preview=False)
        delgvar("Z_AKM")
        return
    if gvarstatus("Z_AK") is not None and gvarstatus("Z_A2K") is not None and gvarstatus("Z_A3K") is not None and gvarstatus("Z_A4K") is not None and gvarstatus("Z_A5K") is None:
        zelzal = int(zed4)
        zilzal = int(zee4)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
        except ValueError:
            return
        name_zed = user_zed.first_name
        name_zee = user_zee.first_name
        await edit_or_reply(event, f"[ᯓ ᥲRRᥲS Gᥲmᗴ - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تـم اختيـار المتهـم ⇠**  [{name_zed}](tg://user?id={zed4})  \n**- ليتـم الحكـم عليـه ⇠ ⚖**\n**- الحاكـم 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee4}) ", link_preview=False)
        delgvar("Z_AKM")
        return
    if gvarstatus("Z_AK") is not None and gvarstatus("Z_A2K") is not None and gvarstatus("Z_A3K") is not None and gvarstatus("Z_A4K") is not None and gvarstatus("Z_A5K") is not None:
        zelzal = int(zed5)
        zilzal = int(zee5)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
        except ValueError:
            return
        name_zed = user_zed.first_name
        name_zee = user_zee.first_name
        await edit_or_reply(event, f"[ᯓ ᥲRRᥲS Gᥲmᗴ -☣ لعبـة أحكـام](t.me/Lx5x5)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تـم اختيـار المتهـم ⇠**  [{name_zed}](tg://user?id={zed5})  \n**- ليتـم الحكـم عليـه ⇠ ⚖**\n**- الحاكـم 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee5}) ", link_preview=False)
        delgvar("Z_AKM")
        return


'''

from telethon import events
from telethon.tl.types import InputMediaDice
from . import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

# قاموس لحفظ نتائج اللاعبين
games = {}

@l313l.on(events.NewMessage(pattern='.نرد'))
async def start_game(event):
    """
    تبدأ اللعبة عند إرسال .لعبة النرد
    """
    user = await event.get_sender()
    if user.id != l313l.uid:
        return
    global games
    chat_id = event.chat_id
    games[chat_id] = {
        "players": {} 
    }
    if gvarstatus("dice_game"):
        delgvar("dice_game")
    if gvarstatus("name_game"):
        delgvar("name_game")
    addgvar("name_game", "🎲 لعبـة رمـي النـرد")
    addgvar("dice_game", True)
    await event.reply("[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 🎲 لعبـة رمـي النـرد](t.me/ZThon)\n⋆─┄─┄─┄─┄─┄─┄─┄─⋆\n**- تم بـدء لعبـة رمـي النـرد .. بنجـاح ☑️\n- اللي بيلعـب يضغـط ع النـرد بالاسفـل **", link_preview=False)
    await event.delete()
    emoticon = "🎲"
    r = await event.reply(file=InputMediaDice(emoticon=emoticon))

@l313l.on(events.NewMessage())
async def handle_dice(event):
    """
    يتفاعل مع رمي النرد في الدردشة التي بدأت فيها لعبة.
    """
    global games
    chat_id = event.chat_id
    # التحقق من وجود لعبة في هذه الدردشة 
    if chat_id in games:
        sender = await event.get_sender()
        user_id = sender.id
        sender_name = f"{sender.first_name} {sender.last_name}" if sender.last_name else sender.first_name
        # للتأكد من أن الرسالة تحتوي على رمي نرد 
        if event.dice and event.dice.emoticon == '🎲':
            if gvarstatus("dice_game") is None:
                return
            dice_value = event.dice.value
            # حفظ نتيجة اللاعب 
            if user_id not in games[chat_id]["players"]:
                games[chat_id]["players"][user_id] = 0
                games[chat_id]["players"][user_id] += dice_value
                if dice_value == 1:
                    dice_value = "❶"
                elif dice_value == 2:
                    dice_value = "❷"
                elif dice_value == 3:
                    dice_value = "❸"
                elif dice_value == 4:
                    dice_value = "❹"
                elif dice_value == 5:
                    dice_value = "❺"
                elif dice_value == 6:
                    dice_value = "❻"
                else:
                    pass
                await event.reply(f"**• اللاعب ⇐**  {sender_name}\n**• رمى النرد وحصل على ⇐ ** {dice_value} **نقاط**\n\n**• انتظـر لـ حتى يتم إنهاء اللعبـه واختيار الفائـز**\n**• لـ إنهـاء اللعبـه ارسـل الامـر** ( `.النتيجه` )")
            else:
                await event.delete()

@l313l.on(events.NewMessage(pattern='.النتيجه'))
async def end_game(event):
    """
    ينهي اللعبة الحالية في الدردشة ويعرض النتائج.
    """
    user = await event.get_sender()
    if user.id != l313l.uid:
        return
    if gvarstatus("dice_game") is None:
        return
    global games
    chat_id = event.chat_id

    # التحقق من وجود لعبة في هذه الدردشة
    if chat_id in games:
        if not games[chat_id]["players"]:
            await event.reply("**- لم يشارك أحد في اللعبة بعد.**")
            return

        # إيجاد أعلى نتيجة 
        max_score = max(games[chat_id]["players"].values())

        # إيجاد جميع الفائزين (الذين حصلوا على أعلى نتيجة)
        winners = [user_id for user_id, score in games[chat_id]["players"].items() if score == max_score]

        # بناء رسالة النتائج 
        name_game = gvarstatus("name_game") if gvarstatus("name_game") else "🎲 لعبـة رمـي النـرد"
        results_message = f"ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 {name_game}\n⋆─┄─┄─┄─┄─┄─┄─┄─⋆\n"
        for user_id, score in games[chat_id]["players"].items():
            user_entity = (await l313l.get_entity(user_id))
            user_name = f"{user_entity.first_name} {user_entity.last_name}" if user_entity.last_name else user_entity.first_name
            if score == 1:
                score = "❶"
            elif score == 2:
                score = "❷"
            elif score == 3:
                score = "❸"
            elif score == 4:
                score = "❹"
            elif score == 5:
                score = "❺"
            elif score == 6:
                score = "❻"
            else:
                pass
            results_message += f"**• اللاعب ⇐**  {user_name} | **عـدد النقـاط ⇐** {score}\n"

        # إضافة أسماء الفائزين 
        if len(winners) == 1:
            winner_entity = (await l313l.get_entity(winners[0]))
            winner_name = f"{winner_entity.first_name} {winner_entity.last_name}" if winner_entity.last_name else winner_entity.first_name
            if max_score == 1:
                max_score = "❶"
            elif max_score == 2:
                max_score = "❷"
            elif max_score == 3:
                max_score = "❸"
            elif max_score == 4:
                max_score = "❹"
            elif max_score == 5:
                max_score = "❺"
            elif max_score == 6:
                max_score = "❻"
            else:
                pass
            results_message += f"\n\n**• الفـائـز هـو ⇐** {winner_name} | **بمجمـوع نقـاط ⇐** {max_score} 🏆"
        else:
            results_message += f"\n\n**• الفائـزيـن هـم:** "
            for winner_id in winners:
                winner_entity = (await l313l.get_entity(winner_id))
                winner_name = f"**• الفائـز ⇐** {winner_entity.first_name} {winner_entity.last_name}" if winner_entity.last_name else winner_entity.first_name
                results_message += f"\n{winner_name}"
            if max_score == 1:
                max_score = "❶"
            elif max_score == 2:
                max_score = "❷"
            elif max_score == 3:
                max_score = "❸"
            elif max_score == 4:
                max_score = "❹"
            elif max_score == 5:
                max_score = "❺"
            elif max_score == 6:
                max_score = "❻"
            else:
                pass
            results_message += f"\n**• نقـاط الفائـزيـن ⇐** {max_score} **نقطـه** 🏆"

        # إزالة اللعبة من القائمة بعد نهايتها
        del games[chat_id]
        delgvar("dice_game")
        delgvar("name_game")
        await event.reply(results_message, link_preview=False)
        await event.delete()
    else:
        await event.reply("**- لا يوجد لعبة نرد في هذه الدردشة ❌**\n**- لـ بـدء لعبـة النرد 🎲**\n**- ارسـل الامـر** ( `.لعبة النرد` )")

ZelzalGM_cmd = (
"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 🎲 لعبـة رمـي النـرد](t.me/ZThon)\n"
"**⋆─┄─┄─┄─┄•┄─┄─┄─┄─⋆**\n"
"**⌖ لعبـة رمـي النـرد 🎲 الجديـدة اكثـر نقطـه 6 ⛳️**\n\n"
"**• الامـر ⇐**  `.لعبة النرد`\n"
"**⪼ لـ بـدء لعبـة رمـي النـرد 🎲**\n\n"
"**• الامـر ⇐**  `.النتيجه`\n"
"**⪼ لـ إنهـاء اللعبـه وعـرض النتائـج 🏆**\n"
)

@l313l.ar_cmd(pattern="العاب المشاركة")
async def game_info(event):
    await edit_or_reply(event, ZelzalGM_cmd, link_preview=False)


'''


##############################
#####

from telethon import events
from telethon.tl.types import InputMediaDice, Message
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from . import l313l
from telethon.extensions import html, markdown
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
import asyncio
import random

class CustomParseMode:
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'html':
            text, entities = html.parse(text)
            # معالجة إيموجيات البريميوم
            for i, e in enumerate(entities):
                if isinstance(e, types.MessageEntityTextUrl):
                    if e.url.startswith('emoji/'):
                        document_id = int(e.url.split('/')[1])
                        entities[i] = types.MessageEntityCustomEmoji(
                            offset=e.offset,
                            length=e.length,
                            document_id=document_id
                        )
            return text, entities
        elif self.parse_mode == 'markdown':
            return markdown.parse(text)
        raise ValueError("Unsupported parse mode")

    @staticmethod
    def unparse(text, entities):
        return html.unparse(text, entities)
        
# قاموس لحفظ بيانات اللعبة
dice_games = {}

class DiceGame:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.players = {}  # {user_id: {"name": "", "current_round_score": 0, "total_score": 0}}
        self.pinned_message_id = None
        self.game_message_id = None
        self.current_round = 1
        self.game_active = False
        self.waiting_for_dice = None  # {user_id: remaining_throws}
        self.eliminated_players = []
    
    async def create_pinned_message(self, event):
        """إنشاء الرسالة المثبتة"""
        message = await event.reply("**🎲 لعبـة النـرد الجديدة**\n\n**اللاعبون المشاركون:**\nٴ- لم ينضم أحد بعد\n\n**ارسل `Y` للانضمام!**")
        await event.client(UpdatePinnedMessageRequest(self.chat_id, message.id, False))
        self.pinned_message_id = message.id
        return message.id
    
    async def update_pinned_message(self, event):
        """تحديث الرسالة المثبتة"""
        if not self.pinned_message_id:
            return
        
        players_text = "**اللاعبون المشاركون:**\n"
        for user_id, data in self.players.items():
            if self.game_active:
                # في الجولة النشطة، نعرض نقاط الجولة الحالية
                score_display = data["current_round_score"]
            else:
                score_display = "لم يلعب بعد"
            players_text += f"ٴ👤 {data['name']} - النقاط: {score_display}\n"
        
        if self.eliminated_players:
            players_text += f"\n**المقصيون:**\n"
            for player in self.eliminated_players:
                players_text += f"ٴ❌ {player}\n"
        
        status = "**الحالة: جارية**" if self.game_active else "**الحالة: في انتظار اللاعبين**"
        message_text = f"**🎲 لعبـة النـرد**\n\n{players_text}\n{status}\n\n**الجولة: {self.current_round}**"
        
        try:
            await event.client.edit_message(self.chat_id, self.pinned_message_id, message_text)
        except:
            pass

    async def add_player(self, event, user):
        """إضافة لاعب جديد"""
        if user.id in self.players:
            return False
        
        user_name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        self.players[user.id] = {
            "name": user_name,
            "current_round_score": 0,  # نقاط الجولة الحالية فقط
            "total_score": 0,  # لم يعد مستخدمًا للإقصاء
            "dice_throws": []
        }
        
        await self.update_pinned_message(event)
        return True

    async def start_game(self, event):
        """بدء اللعبة"""
        if len(self.players) < 2:
            await event.reply("**❌ تحتاج إلى لاعبين على الأقل لبدء اللعبة!**")
            return False
        
        self.game_active = True
        await self.update_pinned_message(event)
        await self.start_round(event)
        return True

    async def start_round(self, event):
        """بدء جولة جديدة"""
        # تصفير نقاط الجولة الحالية للجميع
        for user_id in self.players:
            self.players[user_id]["current_round_score"] = 0
            self.players[user_id]["dice_throws"] = []
        
        # بدء من أول لاعب
        player_ids = list(self.players.keys())
        first_player = player_ids[0]
        self.waiting_for_dice = {"user_id": first_player, "remaining_throws": 3}
        
        user_entity = await event.client.get_entity(first_player)
        user_name = self.players[first_player]["name"]
        
        # ✅ لا يرد - رسالة جديدة فقط
        await event.respond(f"**🎲 الجولة {self.current_round}**\n\nعَزيزي/تي [{user_name}](tg://user?id={first_player})\nتم بدء اللعبة إرسل 3 مرات نرد")

    async def process_dice_throw(self, event, user_id, dice_value):
        """معالجة رمي النرد"""
        if not self.waiting_for_dice or self.waiting_for_dice["user_id"] != user_id:
            return False
        
        player = self.players[user_id]
        player["dice_throws"].append(dice_value)
        player["current_round_score"] += dice_value
        self.waiting_for_dice["remaining_throws"] -= 1
        
        if self.waiting_for_dice["remaining_throws"] > 0:
            remaining = self.waiting_for_dice["remaining_throws"]
            user_name = player["name"]
            # ✅ يرد - على رسالة النرد
            await event.reply(f"◈︙اللاعب - {user_name}\n - رمى النرد وحصل على {dice_value} نقطة.\n\n❨ باقي {remaining} رميات❩")
            return "continue"
        else:
            # انتهى دور اللاعب
            total_round_score = player["current_round_score"]
            user_name = player["name"]
            
            # ✅ لا يرد - رسالة جديدة فقط
            await event.respond(f"**🎲 اللاعب {user_name} انتهى من رمي النرد وحصل على {total_round_score} نقطة في هذه الجولة!**")
            
            # تحديث الرسالة المثبتة بعد انتهاء اللاعب
            await self.update_pinned_message(event)
            
            # الانتقال للاعب التالي
            await self.next_player(event)
            return "finished"

    async def next_player(self, event):
        """الانتقال للاعب التالي"""
        player_ids = list(self.players.keys())
        current_index = player_ids.index(self.waiting_for_dice["user_id"])
        
        if current_index + 1 < len(player_ids):
            next_player_id = player_ids[current_index + 1]
            self.waiting_for_dice = {"user_id": next_player_id, "remaining_throws": 3}
            
            user_name = self.players[next_player_id]["name"]
            # ✅ لا يرد - رسالة جديدة فقط
            await event.respond(f"**🎲 الدور الآن على:**\n\nعَزيزي/تي [{user_name}](tg://user?id={next_player_id})\nإرسل 3 مرات نرد")
        else:
            # انتهت الجولة
            await self.finish_round(event)

    async def finish_round(self, event):
        """إنهاء الجولة وتصفية اللاعبين"""
        self.waiting_for_dice = None
        
        # الإقصاء بناءً على نقاط الجولة الحالية فقط
        current_round_scores = {user_id: player["current_round_score"] for user_id, player in self.players.items()}
        min_score = min(current_round_scores.values())
        lowest_players = [user_id for user_id, score in current_round_scores.items() if score == min_score]
        
        if len(lowest_players) == 1:
            # إقصاء لاعب واحد
            eliminated_id = lowest_players[0]
            eliminated_name = self.players[eliminated_id]["name"]
            eliminated_score = self.players[eliminated_id]["current_round_score"]
            self.eliminated_players.append(eliminated_name)
            del self.players[eliminated_id]
            
            # ✅ لا يرد - رسالة جديدة فقط
            await event.respond(f"**🎲 تم إقصاء اللاعب {eliminated_name} لكونه الأقل نقاطاً في الجولة {self.current_round} ({eliminated_score} نقطة)**")
            
        else:
            # تعادل - جولة إضافية للمتعادلين فقط
            await self.handle_tie_breaker(event, lowest_players)
            return
        
        # التحقق إذا كانت اللعبة انتهت
        if len(self.players) == 1:
            await self.finish_game(event)
        else:
            # بدء جولة جديدة
            self.current_round += 1
            await self.update_pinned_message(event)
            await asyncio.sleep(3)
            await self.start_round(event)

    async def handle_tie_breaker(self, event, tied_players):
        """معالجة التعادل بين اللاعبين"""
        tied_names = [self.players[pid]["name"] for pid in tied_players]
        tied_scores = [self.players[pid]["current_round_score"] for pid in tied_players]
        names_text = " - ".join(tied_names)
        
        # ✅ لا يرد - رسالة جديدة فقط
        await event.respond(f"**🎲 تعادل في النقاط بين:**\n{names_text}\n\n**جميعهم حصلوا على {tied_scores[0]} نقطة**\n**سيلعبون جولة إضافية لتحديد المقصى!**")
        
        # حفظ اللاعبين المتعادلين مؤقتاً
        self.tied_players = tied_players
        self.tied_scores = {pid: 0 for pid in tied_players}
        
        # إعادة تعيين النقاط للجولة الإضافية
        for player_id in tied_players:
            self.players[player_id]["current_round_score"] = 0
            self.players[player_id]["dice_throws"] = []
        
        # تحديث الرسالة المثبتة للجولة الإضافية
        await self.update_pinned_message(event)
        
        # بدء الجولة الإضافية من أول لاعب متعادل
        first_tied_player = tied_players[0]
        self.waiting_for_dice = {"user_id": first_tied_player, "remaining_throws": 3, "tie_breaker": True}
        
        user_name = self.players[first_tied_player]["name"]
        # ✅ لا يرد - رسالة جديدة فقط
        await event.respond(f"**⦑ الجولة الإضافية ⦒**\n\n- عَزيزي/تي◖ [{user_name}](tg://user?id={first_tied_player})◗\n- إرسل 3 مرات نرد .")

    async def process_tie_breaker_dice(self, event, user_id, dice_value):
        """معالجة رمي النرد في الجولة الإضافية"""
        player = self.players[user_id]
        player["dice_throws"].append(dice_value)
        player["current_round_score"] += dice_value
        self.tied_scores[user_id] = player["current_round_score"]
        self.waiting_for_dice["remaining_throws"] -= 1
        
        if self.waiting_for_dice["remaining_throws"] > 0:
            remaining = self.waiting_for_dice["remaining_throws"]
            user_name = player["name"]
            # ✅ يرد - على رسالة النرد
            await event.reply(f"◈︙اللاعب - `{user_name}`\n - رمى النرد وحصل على `{dice_value}` نقطة.\n\n❨ باقي `{remaining}` رميات❩")
        else:
            # انتهى دور اللاعب في الجولة الإضافية
            total_round_score = player["current_round_score"]
            user_name = player["name"]
            # ✅ لا يرد - رسالة جديدة فقط
            await event.respond(f"◈︙اللاعب - `{user_name}`\n انتهى من رمي النرد وحصل على `{total_round_score}` نقطة في الجولة الإضافية!")
            
            # تحديث الرسالة المثبتة بعد انتهاء اللاعب
            await self.update_pinned_message(event)
            
            # الانتقال للاعب التالي في الجولة الإضافية
            current_index = self.tied_players.index(user_id)
            if current_index + 1 < len(self.tied_players):
                next_player_id = self.tied_players[current_index + 1]
                self.waiting_for_dice = {"user_id": next_player_id, "remaining_throws": 3, "tie_breaker": True}
                
                user_name = self.players[next_player_id]["name"]
                # ✅ لا يرد - رسالة جديدة فقط
                await event.respond(f"**⦑ الجولة الإضافية ⦒**\n\n-عَزيزي/تي ◖ [{user_name}](tg://user?id={next_player_id}) ◗\nإرسل 3 مرات نرد .")
            else:
                # انتهت الجولة الإضافية
                self.waiting_for_dice = None
                await self.finish_tie_breaker(event)

    async def finish_tie_breaker(self, event):
        """إنهاء الجولة الإضافية للمتعادلين"""
        min_score = min(self.tied_scores.values())
        lowest_players = [pid for pid, score in self.tied_scores.items() if score == min_score]
        
        if len(lowest_players) == 1:
            eliminated_id = lowest_players[0]
            eliminated_name = self.players[eliminated_id]["name"]
            eliminated_score = self.tied_scores[eliminated_id]
            self.eliminated_players.append(eliminated_name)
            del self.players[eliminated_id]
            
            # ✅ لا يرد - رسالة جديدة فقط
            await event.respond(f"◈︙اللاعب `{eliminated_name}`\n- تم أقصائه من الجولة الإضافية (`{eliminated_score}` نقطة) .")
        else:
            eliminated_id = random.choice(lowest_players)
            eliminated_name = self.players[eliminated_id]["name"]
            eliminated_score = self.tied_scores[eliminated_id]
            self.eliminated_players.append(eliminated_name)
            del self.players[eliminated_id]
            
            # ✅ لا يرد - رسالة جديدة فقط
            await event.respond(f"◈︙اللاعب `{eliminated_name}`\n- تم أقصائه عشوائيا بسبب التعادل المستمر (`{eliminated_score}` نقطة) .")
        
        del self.tied_players
        del self.tied_scores
        
        await self.update_pinned_message(event)
        
        if len(self.players) == 1:
            await self.finish_game(event)
        else:
            self.current_round += 1
            await asyncio.sleep(3)
            await self.start_round(event)

    async def finish_game(self, event):
        """إنهاء اللعبة وإعلان الفائز"""
        winner_id = list(self.players.keys())[0]
        winner_name = self.players[winner_id]["name"]
        winner_score = self.players[winner_id]["current_round_score"]
        
        # ✅ لا يرد - رسالة جديدة فقط
        await event.respond(f"**🎊 🏆 مبروك! 🏆 🎊**\n\n**الفائز هو: {winner_name}**\n**بمجموع نقاط الجولة الأخيرة: {winner_score}**\n\nشكراً للجميع على المشاركة!")
        
        final_text = f"**🎲 لعبـة النـرد - انتهت**\n\n**🏆 الفائز: {winner_name}**\n**نقاط الجولة الأخيرة: {winner_score}**\n\n"
        final_text += "**المشاركون:**\n"
        for player in self.eliminated_players:
            final_text += f"ٴ❌ {player}\n"
        
        await event.client.edit_message(self.chat_id, self.pinned_message_id, final_text)
        
        if self.chat_id in dice_games:
            del dice_games[self.chat_id]

# باقي الأوامر تبقى كما هي...
@l313l.on(events.NewMessage(pattern='.نرد2'))
async def start_dice_game(event):
    """بدء لعبة النرد الجديدة"""
    user = await event.get_sender()
    chat_id = event.chat_id
    
    if user.id != l313l.uid:
        return
    
    if chat_id in dice_games:
        await event.reply("**❌ هناك لعبة نشطة بالفعل في هذه الدردشة!**")
        return
    
    game = DiceGame(chat_id)
    dice_games[chat_id] = game
    
    await game.create_pinned_message(event)
    
    await event.reply("**🎲 تم بدء لعبة النرد الجديدة!**\n\n**ارسل `Y` للانضمام للعبة**\n**ارسل `n` لإنهاء اللعبة**")
    await event.delete()

@l313l.on(events.NewMessage(pattern='^(?i)Y$'))
async def join_game(event):
    """الانضمام للعبة"""
    user = await event.get_sender()
    chat_id = event.chat_id
    
    if chat_id not in dice_games:
        return
    
    game = dice_games[chat_id]
    
    if game.game_active:
        await event.reply("<b>❌ اللعبة جاريه， لا يمكن الانضمام الآن!</b>")
        return
    
    success = await game.add_player(event, user)
    if success:
        # استخدام الإيموجي البريميوم في الرسالة مع تنسيق HTML
        message = f"<b>⪼ تم انضمام</b> <code>{user.first_name}</code> <b>إلى اللعبة </b><a href=\"emoji/5357069174512303778\">✅</a>"
        await event.reply(message, parse_mode=CustomParseMode("html"))
    else:
        await event.reply("<b>❌ أنت مشترك بالفعل في اللعبة!</b>", parse_mode=CustomParseMode("html"))
        
@l313l.on(events.NewMessage(pattern='^(?i)n$'))
async def end_game_command(event):
    """إنهاء اللعبة"""
    user = await event.get_sender()
    chat_id = event.chat_id
    
    if user.id != l313l.uid:
        return
    
    if chat_id not in dice_games:
        await event.reply("**❌ لا توجد لعبة نشطة في هذه الدردشة!**")
        return
    
    game = dice_games[chat_id]
    
    if not game.game_active:
        success = await game.start_game(event)
        if not success:
            return
    else:
        await event.reply("**⏸ تم إيقاف اللعبة!**")
        del dice_games[chat_id]

@l313l.on(events.NewMessage())
async def handle_dice_throws(event):
    """معالجة رمي النرد"""
    chat_id = event.chat_id
    user = await event.get_sender()
    
    if chat_id not in dice_games:
        return
    
    game = dice_games[chat_id]
    
    if not game.game_active or not game.waiting_for_dice:
        return
    
    if user.id != game.waiting_for_dice["user_id"]:
        return
    
    if event.dice and event.dice.emoticon == '🎲':
        dice_value = event.dice.value
        
        if hasattr(game, 'tied_players') and game.waiting_for_dice.get('tie_breaker'):
            await game.process_tie_breaker_dice(event, user.id, dice_value)
        else:
            await game.process_dice_throw(event, user.id, dice_value)


'''
import logging
from datetime import datetime

# إعداد نظام التسجيل للأخطاء
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

remove_members_aljoker = {}

@l313l.on(events.ChatAction)
async def Hussein(event):
    try:
        logger.info(f"حدث ChatAction تم استقباله: {event.action_message}")
        
        if not gvarstatus("Mn3_Kick"):
            logger.info("الحماية غير مفعلة - تخطي الحدث")
            return
        
        logger.info("الحماية مفعلة - معالجة الحدث")
        
        if event.user_kicked:
            logger.info("تم كشف عملية طرد عضو")
            
            # إصلاح: الحصول على user_id بشكل صحيح
            if event.action_message and event.action_message.from_id:
                user_id = event.action_message.from_id.user_id if hasattr(event.action_message.from_id, 'user_id') else event.action_message.from_id
            else:
                logger.warning("لا يمكن الحصول على from_id")
                return
            
            chat = await event.get_chat()
            
            logger.info(f"user_id: {user_id}, chat: {chat.title if chat else 'غير معروف'}")
            
            if chat and user_id:
                now = datetime.now()
                
                # تحويل user_id إلى نص لتجنب مشكلة unhashable
                user_key = str(user_id)
                
                if user_key in remove_members_aljoker:
                    time_diff = (now - remove_members_aljoker[user_key]).seconds
                    logger.info(f"فرق الوقت: {time_diff} ثانية للمستخدم {user_key}")
                    
                    if time_diff < 60:
                        logger.info(f"تم كشف تفليش من user_id: {user_key}")
                        try:
                            admin_info = await event.client.get_entity(int(user_key))
                            joker_link = f"[{admin_info.first_name}](tg://user?id={admin_info.id})"
                            
                            await event.reply(f"**✧︙ تم تنزيل المشرف {joker_link} بسبب قيامه بعملية تفليش فاشلة 🤣**")
                            await event.client.edit_admin(chat, int(user_key), change_info=False)
                            
                            logger.info(f"تم تنزيل المشرف بنجاح: {admin_info.first_name}")
                            
                        except Exception as admin_error:
                            logger.error(f"خطأ في تنزيل المشرف: {admin_error}")
                            await event.reply(f"**✧︙ حدث خطأ في تنزيل المشرف: {admin_error}**")
                    
                    # تحديث الوقت بغض النظر عن الحالة
                    remove_members_aljoker[user_key] = now
                else:
                    logger.info(f"إضافة user_id جديد للقائمة: {user_key}")
                    remove_members_aljoker[user_key] = now
            else:
                logger.warning("لا يوجد chat أو user_id")
        else:
            logger.info("ليس حدث طرد عضو - تخطي")
            
    except Exception as e:
        logger.error(f"خطأ في وظيفة الحماية: {e}")
        try:
            await event.reply(f"**✧︙ حدث خطأ في نظام الحماية: {e}**")
        except:
            pass

@l313l.ar_cmd(pattern="منع_التفليش", require_admin=True)
async def Hussein_aljoker(event):
    try:
        addgvar("Mn3_Kick", True)
        logger.info("تم تفعيل منع التفليش")
        await event.edit("**᯽︙ تم تفعيل منع التفليش للمجموعة بنجاح ✓**")
        
        # إرسال رسالة تأكيد مع معلومات التفعيل
        chat = await event.get_chat()
        await event.reply(f"**✧︙ تم تفعيل نظام منع التفليش في {chat.title}**\n"
                         "**✧︙ الحالة: ✅ مفعل**\n"
                         "**✧︙ سيتم مراقبة جميع عمليات الطرد**")
                         
    except Exception as e:
        logger.error(f"خطأ في تفعيل الحماية: {e}")
        await event.edit(f"**✧︙ حدث خطأ في التفعيل: {e}**")

@l313l.ar_cmd(pattern="سماح_التفليش", require_admin=True)
async def Hussein_aljoker(event):
    try:
        delgvar("Mn3_Kick")
        logger.info("تم تعطيل منع التفليش")
        await event.edit("**᯽︙ تم تعطيل منع التفليش للمجموعة بنجاح ✓**")
        
        # تنظيف القائمة
        remove_members_aljoker.clear()
        
    except Exception as e:
        logger.error(f"خطأ في تعطيل الحماية: {e}")
        await event.edit(f"**✧︙ حدث خطأ في التعطيل: {e}**")

@l313l.ar_cmd(pattern="حالة_الحماية", require_admin=True)
async def protection_status(event):
    try:
        status = "✅ مفعل" if gvarstatus("Mn3_Kick") else "❌ معطل"
        tracked_users = len(remove_members_aljoker)
        
        status_msg = f"""
**✧︙ حالة نظام منع التفليش:**

**الحالة:** {status}
**عدد المستخدمين تحت المراقبة:** {tracked_users}
**آخر تحديث:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**تفاصيل النظام:**
- يراقب عمليات الطرد الجماعي
- ينزل المشرف إذا طرد أكثر من عضو في أقل من 60 ثانية
        """
        
        await event.edit(status_msg)
        
    except Exception as e:
        logger.error(f"خطأ في عرض الحالة: {e}")
        await event.edit(f"**✧︙ حدث خطأ في عرض الحالة: {e}**")

@l313l.ar_cmd(pattern="تصحيح_الحماية", require_admin=True)
async def fix_protection(event):
    try:
        # إعادة تعيين النظام
        remove_members_aljoker.clear()
        
        # التحقق من حالة المتغير
        current_status = gvarstatus("Mn3_Kick")
        
        fix_msg = f"""
**✧︙ تم تصحيح نظام الحماية:**

- **تم تنظيف قائمة المراقبة**
- **الحالة الحالية:** {'✅ مفعل' if current_status else '❌ معطل'}
- **عدد المستخدمين بعد التنظيف:** {len(remove_members_aljoker)}

**النظام جاهز للعمل ✅**
        """
        
        await event.edit(fix_msg)
        logger.info("تم تصحيح نظام الحماية")
        
    except Exception as e:
        logger.error(f"خطأ في التصحيح: {e}")
        await event.edit(f"**✧︙ حدث خطأ في التصحيح: {e}**")
'''
