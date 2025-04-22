import base64
import asyncio
from datetime import datetime
from telethon import events
from telethon.errors import BadRequestError, UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights
from telethon.utils import get_display_name

from JoKeRUB import l313l

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format
from ..sql_helper import gban_sql_helper as gban_sql
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.katm_sql import (
    add_katm,
    get_katms,
    remove_all_katms,
    remove_katm,
)
plugin_category = "admin"
joker_users = []

LOGS = logging.getLogger(__name__)
joker_mute = "https://telegra.ph/file/c5ef9550465a47845c626.jpg"
joker_unmute = "https://telegra.ph/file/e9473ddef0b58cdd7f9e7.jpg"

@l313l.ar_cmd(pattern="كتم مؤقت(?:\s|$)([\s\S]*)")
async def temp_mute(event):
    if event.is_private:
        await event.edit("**⪼ هذا الأمر يعمل فقط في المجموعات!**")
        return
    
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await event.edit("**⪼ يجب تحديد مدة الكتم مثل: `.كتم مؤقت 5m سبب`**")
    
    split_args = input_str.split(maxsplit=2)
    if len(split_args) < 2:
        return await event.edit("**⪼ صيغة خاطئة! استخدم: `.كتم مؤقت الوقت سبب`**")
    
    time_value = split_args[0]
    reason = split_args[1] if len(split_args) > 1 else "لا يوجد سبب"
    
    try:
        time_amount = int(time_value[:-1])
        time_unit = time_value[-1].lower()
        
        if time_unit == 'm':
            mute_duration = timedelta(minutes=time_amount)
        elif time_unit == 'h':
            mute_duration = timedelta(hours=time_amount)
        elif time_unit == 'd':
            mute_duration = timedelta(days=time_amount)
        else:
            return await event.edit("**⪼ وحدة الوقت غير صالحة! استخدم m للدقائق, h للساعات, d للأيام**")
    except Exception as e:
        return await event.edit(f"**⪼ خطأ في تحديد الوقت: {str(e)}**")
    
    user, _ = await get_user_from_event(event)
    if not user:
        return
    
    if user.id == l313l.uid:
        return await edit_delete(event, "**⪼ لا يمكنك كتم نفسك!**")
    
    if user.id == 5427469031:
        return await edit_delete(event, "**⪼ لا يمكنني كتم مطور السورس!**")
    
    try:
        mute(user.id, "temp_mute")
        await event.client.send_file(
            event.chat_id,
            joker_mute,
            caption=f"**⎉╎تم كتم المستخدم مؤقتاً**\n**⎉╎المدة: {time_value}**\n**⎉╎السبب: {reason}**",
        )
        
        await asyncio.sleep(mute_duration.total_seconds())
        unmute(user.id, "temp_mute")
        await event.client.send_file(
            event.chat_id,
            joker_unmute,
            caption=f"**⎉╎تم إلغاء كتم المستخدم**\n**⎉╎انتهت مدة الكتم: {time_value}**",
        )
        
    except Exception as e:
        await event.edit(f"**⪼ حدث خطأ: {str(e)}**")

@l313l.ar_cmd(pattern="كتم(?:\s|$)([\s\S]*)")
async def startgmute(event):
    if event.is_private:
        await asyncio.sleep(0.5)
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == l313l.uid:
            return await edit_or_reply(event, "**⪼ لا يمكنك كتم نفسك!**")
        if user.id == 5427469031:
            return await edit_or_reply(event, "**⪼ لا يمكنني كتم مطور السورس!**")
        userid = user.id 
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == l313l.uid:
            return await edit_or_reply(event, "**⪼ لا يمكنك كتم نفسك!**")
        if user.id == 5427469031:
            return await edit_or_reply(event, "**⪼ لا يمكنني كتم مطور السورس!**")
        userid = user.id
    
    try:
        user = await event.client.get_entity(userid)
    except Exception:
        return await edit_or_reply(event, "**⪼ لا يمكنني العثور على المستخدم!**")
    
    if is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"**⎉╎المستخـدم** {_format.mentionuser(user.first_name ,user.id)} \n**⎉╎مڪتوم سابقـاً**",
        )
    
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**⪼ خطأ: {e}**")
    else:
        if reason:
            await event.client.send_file(
                event.chat_id,
                joker_mute,
                caption=f"**⎉╎المستخـدم:** {_format.mentionuser(user.first_name ,user.id)}\n**⎉╎تم كتمــه .. بنجــاح 🔕**\n**⎉╎السـبب:** {reason}",
            )
        else:
            await event.client.send_file(
                event.chat_id,
                joker_mute,
                caption=f"**⎉╎المستخـدم:** {_format.mentionuser(user.first_name ,user.id)}\n**⎉╎تم كتمــه .. بنجــاح 🔕**",
            )
    
    if BOTLOG:
        if reason:
            if add_katm(str(l313l.uid), str(user.id), user.first_name, reason) is True:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الكــتم_العــام 🔕\n\n"
                    f"**- المستخدم:** {_format.mentionuser(user.first_name ,user.id)}\n"
                    f"**- الايدي:** `{user.id}`\n"
                    f"**- السبب:** `{reason}`\n\n"
                    f"**⎉╎تم إضافة المستخدم لقائمة المكتومين**",
                )
        else:
            reason = "لا يوجد"
            if add_katm(str(l313l.uid), str(user.id), user.first_name, reason) is True:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الكــتم_العــام 🔕\n\n"
                    f"**- المستخدم:** {_format.mentionuser(user.first_name ,user.id)}\n"
                    f"**- الايدي:** `{user.id}`\n\n"
                    f"**⎉╎تم إضافة المستخدم لقائمة المكتومين**",
                )

@l313l.ar_cmd(pattern="الغاء كتم(?:\s|$)([\s\S]*)")
async def endgmute(event):
    if event.is_private:
        await asyncio.sleep(0.5)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == l313l.uid:
            return await edit_or_reply(event, "**⪼ أنت غير مكتوم أصلاً!**")
        userid = user.id
    
    try:
        user = await event.client.get_entity(userid)
    except Exception:
        return await edit_or_reply(event, "**⪼ لا يمكنني العثور على المستخدم!**")
    
    if not is_muted(userid, "gmute"):
        return await edit_or_reply(
            event, f"**⎉╎المستخـدم:** {_format.mentionuser(user.first_name ,user.id)}\n\n**⎉╎غيـر مكتـوم عــام ✓**"
        )
    
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**⪼ خطأ: {e}**")
    else:
        if reason:
            await event.client.send_file(
                event.chat_id,
                joker_unmute,
                caption=f"**⎉╎المستخـدم:** {_format.mentionuser(user.first_name ,user.id)}\n**⎉╎تم الغـاء كتمــه .. بنجــاح 🔔**\n**⎉╎السـبب:** {reason}",
            )
        else:
            await event.client.send_file(
                event.chat_id,
                joker_unmute,
                caption=f"**⎉╎المستخـدم:** {_format.mentionuser(user.first_name ,user.id)}\n\n**⎉╎تم الغـاء كتمــه .. بنجــاح 🔔**",
            )
    
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغــاء_الكــتم_العــام 🔔\n\n"
                f"**- المستخدم:** {_format.mentionuser(user.first_name ,user.id)}\n"
                f"**- السبب:** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغــاء_الكــتم_العــام 🔔\n\n"
                f"**- المستخدم:** {_format.mentionuser(user.first_name ,user.id)}\n",
            )

@l313l.ar_cmd(pattern="المكتومين$")
async def on_mute_list(event):
    mktoms = get_katms(l313l.uid)
    if not mktoms:
        return await edit_or_reply(event, "**⪼ لا يوجد مستخدمين مكتومين حالياً!**")
    
    msg = "**𓆩 قائمـة المكتوميــن 𓆪**\n\n"
    for count, mktoom in enumerate(mktoms, start=1):
        msg += f"**{count} -** [{mktoom.f_name}](tg://user?id={mktoom.ktm_id})\n**السبب:** {mktoom.f_reason}\n\n"
    
    await edit_or_reply(event, msg)

@l313l.ar_cmd(pattern="مسح المكتومين$")
async def on_all_muted_delete(event):
    mktomers = get_katms(l313l.uid)
    if not mktomers:
        return await edit_or_reply(event, "**⪼ لا يوجد مستخدمين مكتومين حالياً!**")
    
    zed = await edit_or_reply(event, "**⪼ جاري مسح جميع المكتومين...**")
    for mktoom in mktomers:
        unmute(mktoom.ktm_id, "gmute")
    
    remove_all_katms(l313l.uid)
    await zed.edit("**⪼ تم مسح جميع المكتومين بنجاح!**")

@l313l.on(events.NewMessage(incoming=True))
async def watcher(event):
    if is_muted(event.sender_id, "gmute") or is_muted(event.sender_id, "temp_mute"):
        await event.delete()
