import asyncio
import shutil
import contextlib
from datetime import datetime
import re
import datetime
from asyncio import sleep

from telethon import events
from telethon.utils import get_display_name

from . import l313l
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.katm_sql import (
    add_katm,
    get_katms,
    remove_all_katms,
    remove_katm,
)
from ..sql_helper.mute_sql import is_muted, mute, unmute
from ..utils import Zed_Dev
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event

plugin_category = "الخدمات"
LOGS = logging.getLogger(__name__)
KTMZ = gvarstatus("Z_KTM") or "كتم"

@l313l.ar_cmd(pattern=f"{KTMZ}(?: |$)(.*)")
async def startgmute(event):
    if event.is_private:
        await asyncio.sleep(0.5)
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == l313l.uid:
            return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنك كتــم نفســك ؟!**")
        if user.id in Zed_Dev:
            return await edit_or_reply(event, "**- فكيـو - fuck You 😾🖕**\n**- لاتعيدهـا مـع مطـوࢪين السـورس ...🚧**")
        if user.id == 5427469031:
            return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنك كتــم مطـور السـورس ؟!**")
        userid = user.id 
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == l313l.uid:
            return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنك كتــم نفســك ؟!**")
        if user.id in Zed_Dev:
            return await edit_or_reply(event, "**- فكيـو - fuck You 😾🖕**\n**- لاتعيدهـا مـع مطـوࢪين السـورس ...🚧**")
        if user.id == 5427469031:
            return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنك كتــم مطـور السـورس ؟!**")
        userid = user.id
    try:
        user = await event.client.get_entity(userid)
    except Exception:
        return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنني العثــوࢪ علـى المسـتخــدم ؟!**")
    if is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"**✧╎المستخـدم**  {_format.mentionuser(user.first_name ,user.id)} \n**✧╎مڪتوم سابقـاً**",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**- خطـأ :**\n`{e}`")
    else:
        if reason:
            if gvarstatus("PC_MUTE") is not None:
                await event.client.send_file(
                    event.chat_id,
                    gvarstatus("PC_MUTE"),
                    caption=f"**- المستخـدم :** {_format.mentionuser(user.first_name ,user.id)} .\n**- تـم كتمـه بنجـاح 🔕**\n**- السـبب :** {reason}",
                )
                await event.delete()
            else:
                await edit_or_reply(
                    event,
                    f"**⎉╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}\n**⎉╎تم كتمــه .. بنجــاح 🔕**\n**⎉╎السـبب :** {reason}",
                )
        else:
            if gvarstatus("PC_MUTE") is not None:
                await event.client.send_file(
                    event.chat_id,
                    gvarstatus("PC_MUTE"),
                    caption=f"**✧╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}\n**✧╎تـم كتمــه .. بنجــاح 🔕**",
                )
                await event.delete()
            else:
                await edit_or_reply(
                    event,
                    f"**✧╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}\n**✧╎تـم كتمــه .. بنجــاح 🔕**",
                )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reply:
            await reply.forward_to(BOTLOG_CHATID)
        if reason:
            if add_katm(str(l313l.uid), str(user.id), user.first_name, reason, is_temporary=0) is True:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الكتــم_العـــام 🔕\n\n"
                    f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                    f"**- الايدي** `{user.id}`\n"
                    f"**- الســبب :** `{reason}`\n\n"
                    f"**- تم إضافة المستخدم لـ قائمة المكتوميـن ✅**",
                )
        else:
            reason = "لا يـوجد"
            if add_katm(str(l313l.uid), str(user.id), user.first_name, reason, is_temporary=0) is True:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الكتــم_العـــام 🔕\n\n"
                    f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                    f"**- الايدي** `{user.id}`\n\n"
                    f"**- تم إضافة المستخدم لـ قائمة المكتوميـن ✅**",
                )

@l313l.ar_cmd(pattern="الغاء كتم(?: |$)(.*)")
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
            return await edit_or_reply(event, "**- عــذࢪاً .. انت غيـر مكتـوم**")
        userid = user.id
    try:
        user = await event.client.get_entity(userid)
    except Exception:
        return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنني العثــوࢪ علـى المسـتخــدم ؟!**")
    if not is_muted(userid, "gmute"):
        return await edit_or_reply(
            event, f"**✧╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}\n\n**✧╎غيـر مكتـوم عــام ✓**"
        )
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**- خطـأ :**\n`{e}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"**✧╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}\n**✧╎تم الغـاء كتمــه .. بنجــاح 🔔**\n**✧╎السـبب :** {reason}",
            )
        else:
            await edit_or_reply(
                event,
                f"**✧╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}\n\n**✧╎تم الغـاء كتمــه .. بنجــاح 🔔**",
            )
    if BOTLOG:
        remove_katm(str(l313l.uid), str(user.id))
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغـــاء_الكتــم_العـــام 🔔\n\n"
                f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**- الايدي** `{user.id}`\n"
                f"**- الســبب :** `{reason}`\n\n"
                f"**- تم إزالة المستخدم من قائمة المكتوميـن ✅**",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغـــاء_الكتــم_العـــام 🔔\n\n"
                f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**- الايدي** `{user.id}`\n\n"
                f"**- تم إزالة المستخدم من قائمة المكتوميـن ✅**",
            )



@l313l.ar_cmd(incoming=True, forword=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()


@l313l.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()

@l313l.ar_cmd(pattern="المكتومين$")
async def on_mute_list(event):
    # Get permanent mutes
    perm_mutes = get_katms(l313l.uid, is_temporary=0)
    # Get temporary mutes
    temp_mutes = get_katms(l313l.uid, is_temporary=1)
    
    if not perm_mutes and not temp_mutes:
        return await edit_or_reply(event, "**- لايــوجـد لديــك أي مكتوميــن بعــد 🔔**")
    
    output = "𓆩 𝗠𝘂𝗳𝗳𝗹𝗲𝗱 𝗮𝗥𝗥𝗮𝗦 - قائمـة المكتوميــن 🔕𓆪\n"
    output += f"**• إجمالي عـدد المكتوميـن:** {len(perm_mutes) + len(temp_mutes)}\n"
    output += "⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n"
    
    if perm_mutes:
        output += "**✧ الكـتم العـام 🔕:**\n"
        for i, mute in enumerate(perm_mutes, start=1):
            output += f"**{i}.** - المستـخدم : [{mute.f_name}](tg://user?id={mute.ktm_id})\n"
            output += f"- السـبب : `{mute.f_reason}`\n\n"
    
    if temp_mutes:
        output += "**✧ الكـتم المؤقـت ⏳:**\n"
        for i, mute in enumerate(temp_mutes, start=1):
            output += f"**{i}.** - المستـخدم : [{mute.f_name}](tg://user?id={mute.ktm_id})\n"
            output += f"- المـدة : `{mute.mute_time}`\n"
            output += f"- السـبب : `{mute.f_reason}`\n\n"
    
    await edit_or_reply(
        event,
        output,
        caption="**⧗╎قائمـة المكتوميــن 🔕**",
        file_name="mktoms.text",
    )

@l313l.ar_cmd(pattern="مسح المكتومين$")
async def on_all_muted_delete(event):
    mktomers = get_katms(l313l.uid)
    count = 1
    if mktomers:
        zed = await edit_or_reply(event, "**⪼ جـارِ مسـح المكتوميـن .. انتظـر ⏳**")
        for mktoom in mktomers:
            unmute(mktoom.ktm_id, "gmute")
            count += 1
        remove_all_katms(l313l.uid)
        await zed.edit("**⪼ تم حـذف جميـع المكتوميـن .. بنجـاح ✅**")
    else:
        OUT_STR = "**- لايــوجـد لديــك أي مكتوميــن بعــد 🔔**"
        await edit_or_reply(event, OUT_STR)

@l313l.ar_cmd(pattern="كتم_مؤقت(?:\s|$)([\s\S]*)")
async def temporary_mute(event):
    # Parse the input
    input_str = event.pattern_match.group(1)
    args = input_str.split()
    
    if len(args) < 1:
        return await edit_or_reply(event, "**⪼ استخـدم الأمـر بالشكـل التالـي:**\n`.كتم مؤقت + المدة + (السبب اختياري) + بالرد أو المعرف`")
    
    # Extract time and reason (default to "لا يوجد" if no reason provided)
    time_amount = args[0]
    reason = ' '.join(args[1:]) if len(args) > 1 else "لا يـوجد"
    
    # Get user from event
    user, _ = await get_user_from_event(event)
    if not user:
        return
    
    # Check permissions
    if user.id == l313l.uid:
        return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنك كتــم نفســك ؟!**")
    if user.id in Zed_Dev:
        return await edit_or_reply(event, "**- فكيـو - fuck You 😾🖕**\n**- لاتعيدهـا مـع مطـوࢪين السـورس ...🚧**")
    if user.id == 5427469031:
        return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنك كتــم مطـور السـورس ؟!**")
    
    # Parse time
    time_letter = time_amount[-1]
    time_number = time_amount[:-1]
    
    if not time_number.isdigit():
        return await edit_or_reply(event, "**- رقـم الوقت غيـر صحيـح!**")
    
    time_number = int(time_number)
    
    time_dict = {
        's': time_number,
        'm': time_number * 60,
        'h': time_number * 3600,
        'd': time_number * 86400
    }
    
    mute_time = time_dict.get(time_letter.lower())
    if not mute_time:
        return await edit_or_reply(event, "**- وحـدة الوقت غيـر صحيحـة! استخـدم:**\n`s` للثواني, `m` للدقائق, `h` للساعات, `d` للأيام")
    
    # Mute the user
    try:
        mute(user.id, "gmute")
    except Exception as e:
        return await edit_or_reply(event, f"**- خطـأ في الكتـم:**\n`{e}`")
    
    # Add to database with temporary flag
    add_katm(str(l313l.uid), str(user.id), user.first_name, reason, is_temporary=1, mute_time=time_amount)
    
    # Send confirmation
    await edit_or_reply(
        event,
        f"**✧╎تم كتـم المستخـدم مؤقتـاً 🔕**\n"
        f"**✧╎المستخـدم:** {_format.mentionuser(user.first_name, user.id)}\n"
        f"**✧╎المـدة:** `{time_amount}`\n"
        f"**✧╎السبـب:** `{reason}`"
    )
    
    # Log to BOTLOG
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#الكتم_المؤقت ⏳\n\n"
            f"**- المستخـدم:** {_format.mentionuser(user.first_name, user.id)}\n"
            f"**- الايـدي:** `{user.id}`\n"
            f"**- المـدة:** `{time_amount}`\n"
            f"**- السبـب:** `{reason}`\n\n"
            f"**- تم كتم المستخدم مؤقتاً ✅**"
        )
    
    # Unmute after time expires
    await asyncio.sleep(mute_time)
    
    try:
        unmute(user.id, "gmute")
        remove_katm(str(l313l.uid), str(user.id))
    except Exception as e:
        LOGS.error(f"Error unmuting user: {e}")
    
    # Send unmute notification
    unmute_msg = (
        f"**»╎انتهـى الوقـت المحدد للكتم المؤقـت 🔔**\n"
        f"**✧╎المستخـدم:** {_format.mentionuser(user.first_name, user.id)}\n"
        f"**✧╎الايـدي:** `{user.id}`\n"
        f"**✧╎اليـوزر:** @{user.username if user.username else 'لا يوجد'}\n"
        f"**✧╎المـدة:** `{time_amount}`\n"
        f"**✧╎السبـب:** `{reason}`"
    )
    
    await event.client.send_message(event.chat_id, unmute_msg)
    
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#انتهاء_الكتم_المؤقت 🔔\n\n"
            f"**- المستخـدم:** {_format.mentionuser(user.first_name, user.id)}\n"
            f"**- الايـدي:** `{user.id}`\n"
            f"**- اليوزر:** @{user.username if user.username else 'لا يوجد'}\n"
            f"**- المـدة:** {time_amount}\n"
            f"**- السبـب:** {reason}\n\n"
            f"**- تم الغاء الكتم تلقائياً بعد انتهاء المدة ✅**"
        )
