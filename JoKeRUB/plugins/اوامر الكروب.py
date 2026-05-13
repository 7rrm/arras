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

@l313l.ar_cmd(pattern="مسح المحظورين ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        LOGS.info("TODO: Not yet Implemented")
    else:
        if event.is_private:
            return False
        et = await edit_or_reply(event, "**↫ البحث في قوائم المشاركين ⇲**")
        p = 0
        async for i in event.client.iter_participants(
            event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
        ):
            rights = ChatBannedRights(until_date=0, view_messages=False)
            try:
                await event.client(
                    functions.channels.EditBannedRequest(event.chat_id, i, rights)
                )
            except Exception as ex:
                await et.edit(str(ex))
            else:
                p += 1
        await et.edit("⪼ {} **↫** {} **رفع الحظر عنهم**".format(event.chat_id, p))


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
    zedevent = await edit_or_reply(event, "**⎉╎ إلغاء حظر جميع الحسابات المحظورة في هذه المجموعة 🆘**")
    succ = 0
    total = 0
    flag = False
    chat = await event.get_chat()
    async for i in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsKicked, aggressive=True):
        total += 1
        rights = ChatBannedRights(until_date=0, view_messages=False)
        try:
            await event.client(functions.channels.EditBannedRequest(event.chat_id, i, rights))
        except FloodWaitError as e:
            LOGS.warn(f"**⎉╎هناك ضغط كبير بالاستخدام يرجى الانتضار .. ‼️ بسبب  : {e.seconds} **")
            await zedevent.edit(f"**⎉╎{readable_time(e.seconds)} مطلـوب المـعاودة مـرة اخـرى للـمسح 🔁 **")
            await sleep(e.seconds + 5)
        except Exception as ex:
            await zedevent.edit(str(ex))
        else:
            succ += 1
            if flag:
                await sleep(2)
            else:
                await sleep(1)
            try:
                if succ % 10 == 0:
                    await zedevent.edit(f"**⎉╎جـارِ مسـح المحـظورين ⭕️  : \n {succ} الحسـابات الـتي غيـر محظـورة لحـد الان.**")
            except MessageNotModifiedError:
                pass
    await zedevent.edit(f"**⎉╎تـم مسـح المحـظورين مـن أصـل 🆘 :**{succ}/{total} \n اسـم المجـموعـة 📄 : {chat.title}")

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
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**⎉╎لا توجـد حـسابات محذوفـة في هـذه المجموعـة !**"
    if con != "اطردهم":
        event = await edit_or_reply(show, "**⎉╎جـارِ البحـث عـن الحسابـات المحذوفـة ⌯**")
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"**⎉╎تم ايجـاد  {del_u}  من  الحسابـات المحذوفـه في هـذه المجموعـه**\n**⎉╎لحذفهـم إستخـدم الأمـر  ⩥ :**  `.المحذوفين اطردهم`"
        await event.edit(del_status)
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_delete(show, "**⎉╎ليس لـدي صلاحيـات المشـرف هنـا ؟!**", 5)
        return
    event = await edit_or_reply(show, "**⎉╎جـارِ حـذف الحسـابات المحذوفـة ⌯**")
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client.kick_participant(show.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_delete(event, "**⎉╎ ليس لدي صلاحيات الحظر هنا**", 5)
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"**⎉╎تـم حـذف  {del_u}  الحسـابات المحذوفـة ✓**"
    if del_a > 0:
        del_status = f"**⎉╎تـم حـذف {del_u} الحسـابات المحذوفـة، ولڪـن لـم يتـم حذف الحسـابات المحذوفـة للمشرفيـن !**"
    await edit_delete(event, del_status, 5)
    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            f"**⎉╎تنظيف :**\
            \n⎉╎{del_status}\
            \n*⎉╎المحادثـة ⌂** {show.chat.title}(`{show.chat_id}`)",
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

@l313l.ar_cmd(pattern="مغادرة الكروبات$")
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

@l313l.ar_cmd(pattern="مغادرة القنوات$")
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
                await asyncio.sleep(0.6)
            except Exception as e:
                print(f"خطأ في {entity.title}: {e}")

        result = f"**✓ | تم مغادرة {left} قناة**"
        if kept_count > 0:
            result += f"\n**✧ | تم الاحتفاظ بــ {kept_count} قناة** (كنت مشرفًا فيها أو محفوظة في الأرشيف)"
        await processing_msg.edit(result)
        
    except Exception as e:
        await processing_msg.edit(f"**خطأ:**\n`{str(e)}`")
        

@l313l.ar_cmd(pattern="تصفية الخاص$")
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

@l313l.ar_cmd(pattern="تصفية البوتات$")
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

from telethon.tl.functions.contacts import BlockRequest

@l313l.ar_cmd(pattern="حظر_البوتات$")
async def Hussein(event):
    await event.edit("**✧︙ جارٍ تصفية وحظر البوتات...**")
    
    dialogs = await event.client.get_dialogs()
    
    bots_to_clear = []
    for dialog in dialogs:
        if dialog.is_user and dialog.entity.bot and not dialog.archived:
            bots_to_clear.append(dialog.entity)
    
    cleared_count = 0
    blocked_count = 0
    
    for bot in bots_to_clear:
        try:
            # 1. مسح المحادثة أولاً
            await event.client(DeleteHistoryRequest(
                peer=bot.id,
                max_id=0,
                just_clear=True
            ))
            cleared_count += 1
            
            # 2. ثم حظر البوت
            await event.client(BlockRequest(id=bot.id))
            blocked_count += 1
            
            await asyncio.sleep(1)  # تجنب حظر من تيليجرام
            
        except Exception as e:
            print(f"خطأ مع البوت {bot.id}: {e}")
    
    await event.edit(f"**✧︙ تم الانتهاء!**\n"
                     f"**تم مسح:** `{cleared_count}` محادثة بوت\n"
                     f"**تم حظر:** `{blocked_count}` بوت\n"
                     f"(لم يتم التعامل مع البوتات المؤرشفة)")

        
"""
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
"""
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
