import base64
import contextlib
import asyncio
import requests
import logging
from asyncio import sleep

from telethon.tl import functions, types
from telethon.errors import UserAdminInvalidError
from telethon import events
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.utils import get_display_name

from . import l313l

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import gvarstatus
from ..helpers import readable_time
from ..helpers.utils import reply_id
from ..utils import is_admin
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper import broadcast_sql as sql
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "البوت"
LOGS = logging.getLogger(__name__)

ZED_BLACKLIST = [
    -1001935599871,
    ]

DEVZ = [
    1895219306,
    5427469031,
]

spam_chats = []
#

ZelzalPRO_cmd = (
    "𓆩 [𝗦𝗼𝘂𝗿𝗰𝗲  𝗮𝗥𝗥𝗮𝗦 - اوامـر الاذا؏ـــة](t.me/lx5x5) 𓆪\n\n"
    "**⎞𝟏⎝** `.للكروبات`  / `.للمجموعات`\n"
    "**بالــࢪد ؏ــلى ࢪســالة نصيــه او وسـائــط تحتهــا نــص**\n"
    "**- لـ اذاعـة رسـالة او ميديـا لكـل المجموعـات اللي انت موجود فيهـا . .**\n\n\n"
    "**⎞𝟐⎝** `.للخاص`\n"
    "**بالــࢪد ؏ــلى ࢪســالة نصيــه او وسـائــط تحتهــا نــص**\n"
    "**- لـ اذاعـة رسـالة او ميديـا لكـل الاشخـاص اللي موجـودين عنـدك خـاص . .**\n"
    "**- في حال اردت اذاعـة رسـالة لـ عـدد محـدد من الموجودين خـاص حتى ماتنحظـر من الشركـه**\n"
    "**ارسـل (.للخاص + عـدد) بالــࢪد ؏ــلى ࢪســالة نصيــه او وسـائــط تحتهــا نــص**\n"
    "**سوف يقوم بالاذاعـة لـ آخـر اشخـاص حسب العـدد لديـك بالخـاص**\n\n\n"
    "**⎞𝟑⎝** `.خاص`\n"
    "**الامـر + معرف الشخص + الرسـاله . .**\n"
    " **- ارسـال رسـاله الى الشخص المحدد بدون الدخول للخاص وقراءة الرسـائل . .**\n\n\n"
    "**⎞4⎝** `.للكل`\n"
    "**بالــࢪد ؏ــلى ࢪســالة نصيــه او وسـائــط تحتهــا نــص**\n"
    " **- ارسـال رسـاله اذاعـة الى جميـع اعضـاء مجموعـة محددة .. قم باستخـدام الامـر داخـل المجموعـة . .**\n\n"
    "\n 𓆩 [𝗦𝗼𝘂𝗿𝗰𝗲  𝗮𝗥𝗥𝗮𝗦](t.me/lx5x5) 𓆪"
)

@l313l.ar_cmd(pattern="الاذاعه")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalPRO_cmd)

@l313l.ar_cmd(pattern=f"للكروبات(?: |$)(.*)")
async def gcast(event):
    zedthon = event.pattern_match.group(1)
    if zedthon:
        await edit_or_reply(event, "**⎉╎بالـࢪد ؏ــلى ࢪسـالة او وسائـط**")
        return
    elif event.is_reply:
        zelzal = await event.get_reply_message()
    else:
        await edit_or_reply(event, "**⎉╎بالـࢪد ؏ــلى ࢪسـالة او وسائـط**")
        return
    zzz = await edit_or_reply(event, "**⎉╎جـاري الاذاعـه في المجموعـات ...الرجـاء الانتظـار**")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            if chat not in ZED_BLACKLIST:
                await event.client.send_message(chat, msg)
                try:
                    if zelzal.text:
                        try:
                            await borg.send_message(chat, zelzal, link_preview=False)
                            done += 1
                        except BaseException:
                            er += 1
                    else:
                        try:
                            await borg.send_file(
                                chat,
                                zelzal,
                                caption=zelzal.caption,
                                link_preview=False,
                            )
                            done += 1
                        except BaseException:
                            er += 1
                except BaseException:
                    er += 1
    await zzz.edit(
        f"**⎉╎تمت الاذاعـه بنجـاح الـى ** `{done}` **من المجموعـات** \n**⎉╎خطـأ في الارسـال الـى ** `{er}` **من المجموعـات**"
    )


@l313l.ar_cmd(pattern=f"للمجموعات(?: |$)(.*)")
async def gcast(event):
    zedthon = event.pattern_match.group(1)
    if zedthon:
        await edit_or_reply(event, "**⎉╎بالـࢪد ؏ــلى ࢪسـالة او وسائـط**")
        return
    elif event.is_reply:
        zelzal = await event.get_reply_message()
    else:
        await edit_or_reply(event, "**⎉╎بالـࢪد ؏ــلى ࢪسـالة او وسائـط**")
        return
    zzz = await edit_or_reply(event, "**⎉╎جـاري الاذاعـه في المجموعـات ...الرجـاء الانتظـار**")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            if chat not in ZED_BLACKLIST:
                await event.client.send_message(chat, msg)
                try:
                    if zelzal.text:
                        try:
                            await borg.send_message(chat, zelzal, link_preview=False)
                            done += 1
                        except BaseException:
                            er += 1
                    else:
                        try:
                            await borg.send_file(
                                chat,
                                zelzal,
                                caption=zelzal.caption,
                                link_preview=False,
                            )
                            done += 1
                        except BaseException:
                            er += 1
                except BaseException:
                    er += 1
    await zzz.edit(
        f"**⎉╎تمت الاذاعـه بنجـاح الـى ** `{done}` **من المجموعـات** \n**⎉╎خطـأ في الارسـال الـى ** `{er}` **من المجموعـات**"
    )

    
@l313l.ar_cmd(pattern=f"للخاص(?: |$)(.*)")
async def gucast(event):
    zedthon = event.pattern_match.group(1)
    if zedthon.isnumeric() and event.is_reply:
        zelzal = await event.get_reply_message()
        zzz = await edit_or_reply(event, f"**⎉╎جـاري الاذاعـه في الخـاص ...\n⎉╎لـ عـدد {zedthon} شخص\n⎉╎الرجـاء الانتظـار .. لحظات**")
        er = 0
        done = 0
        async for x in event.client.iter_dialogs():
            if x.is_user and not x.entity.bot:
                chat = x.id
                if done == int(zedthon):
                    break
                try:
                    if zelzal.text:
                        try:
                            await borg.send_message(chat, zelzal, link_preview=False)
                            done += 1
                        except BaseException:
                            break
                    else:
                        try:
                            await borg.send_file(
                                chat,
                                zelzal,
                                caption=zelzal.caption,
                                link_preview=False,
                            )
                            done += 1
                        except BaseException:
                            er += 1
                except BaseException:
                    break
        return await zzz.edit(
            f"**⎉╎تمت الاذاعـه بنجـاح الـى ** `{done}` **من الخـاص**\n**⎉╎خطـأ في الارسـال الـى ** `{er}` **من الخـاص**"
        )
    elif event.is_reply and not zedthon:
        zelzal = await event.get_reply_message()
        zzz = await edit_or_reply(event, "**⎉╎جـاري الاذاعـه في الخـاص ...الرجـاء الانتظـار**")
        er = 0
        done = 0
        async for x in event.client.iter_dialogs():
            if x.is_user and not x.entity.bot:
                chat = x.id
                try:
                    if zelzal.text:
                        try:
                            await borg.send_message(chat, zelzal, link_preview=False)
                            done += 1
                        except BaseException:
                            return
                    else:
                        try:
                            await borg.send_file(
                                chat,
                                zelzal,
                                caption=zelzal.caption,
                                link_preview=False,
                            )
                            done += 1
                        except BaseException:
                            er += 1
                except BaseException:
                    return
        return await zzz.edit(
            f"**⎉╎تمت الاذاعـه بنجـاح الـى ** `{done}` **من الخـاص**\n**⎉╎خطـأ في الارسـال الـى ** `{er}` **من الخـاص**"
        )
    else:
        await edit_or_reply(event, "**⎉╎بالـࢪد ؏ــلى ࢪسـالة او وسائـط**")
        return


@l313l.ar_cmd(pattern="خاص ?(.*)")
async def pmto(event):
    r = event.pattern_match.group(1)
    p = r.split(" ")
    chat_id = p[0]
    try:
        chat_id = int(chat_id)
    except BaseException:
        pass
    zelzal = ""
    for i in p[1:]:
        zelzal += i + " "
    if zelzal == "":
        return
    try:
        await l313l.send_message(chat_id, zelzal)
        await event.edit("**⎉╎تـم ارسال الرسـالة بنجـاح ✓**\n**⎉╎بـدون الدخـول للخـاص**")
    except BaseException:
        await event.edit("**⎉╎اووبس .. لقـد حدث خطـأ مـا .. اعـد المحـاوله**")

Warn = "تخمـط بـدون ذكـر المصـدر - ابلعــك نعــال وراح اهينــك"
ZTHON_BEST_SOURCE = "[ᯓ  𝗮𝗥𝗥𝗮𝗦 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 - اذاعـة خـاص 🚹](t.me/lx5x5) .\n\n**- جـارِ الاذاعـه خـاص لـ أعضـاء الكـروب 🛗\n- الرجـاء الانتظـار .. لحظـات ⏳**"
ZELZAL_PRO_DEV = "[ᯓ  𝗮𝗥𝗥𝗮𝗦 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 - اذاعـة زاجـل 🕊](t.me/lx5x5) .\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⎉╎قائمـة الاذاعـه فارغـه ؟! ❌**\n**⎉╎قم باضافة يوزرات عبـر الامر**\n`.اضف فار زاجل` **بالـرد ع عدة يوزرات تفصل بينهم مسافات**"

@l313l.ar_cmd(pattern=f"للكل(?: |$)(.*)", groups_only=True)
async def malath(event):
    zedthon = event.pattern_match.group(1)
    if zedthon:
        await edit_or_reply(event, "**⎉╎بالـࢪد ؏ــلى ࢪسـالة او وسائـط**")
        return
    elif event.is_reply:
        zilzal = await event.get_reply_message()
    else:
        await edit_or_reply(event, "**⎉╎بالـࢪد ؏ــلى ࢪسـالة او وسائـط**")
        return
    chat_id = event.chat_id
    is_admin = False
    try:
        await l313l(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        pass
    spam_chats.append(chat_id)
    zzz = await edit_or_reply(event, ZTHON_BEST_SOURCE, link_preview=False)
    total = 0
    success = 0
    async for usr in event.client.iter_participants(event.chat_id):
        total += 1
        if not chat_id in spam_chats:
            break
        username = usr.username
        magtxt = f"@{username}"
        if str(username) == "None":
            idofuser = usr.id
            magtxt = f"{idofuser}"
        if zilzal.text:
            try:
                await borg.send_message(magtxt, zilzal, link_preview=False)
                success += 1
            except BaseException:
                return
        else:
            try:
                await borg.send_file(
                    magtxt,
                    zilzal,
                    caption=zilzal.caption,
                    link_preview=False,
                )
                success += 1
            except BaseException:
                return
    ZELZAL_BEST_DEV = f"[ᯓ  𝗮𝗥𝗥𝗮𝗦 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 - اذاعـة خـاص 🚹](t.me/lx5x5) .\n\n**⎉╎تمت الاذاعـه لـ اعضـاء الكـروب .. بنجـاح  ✅**\n**⎉╎عـدد {success} عضـو**"
    await zzz.edit(ZELZAL_BEST_DEV, link_preview=False)
    try:
        spam_chats.remove(chat_id)
    except:
        pass

@l313l.ar_cmd(pattern="ايقاف للكل", groups_only=True)
async def unmalath(event):
    if not event.chat_id in spam_chats:
        return await event.edit("**- لاتوجـد عمليـة اذاعـه للاعضـاء هنـا لـ إيقافـها ؟!**")
    else:
        try:
            spam_chats.remove(event.chat_id)
        except:
            pass
        return await event.edit("**⎉╎تم إيقـاف عمليـة الاذاعـه للاعضـاء هنـا .. بنجـاح✓**")
