mport contextlib
import base64
import asyncio
import io
import re
from asyncio import sleep
from datetime import datetime
from math import sqrt

from telethon.events import InlineQuery, callbackquery
from telethon import Button
from telethon.tl.functions.channels import EditAdminRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.messages import ExportChatInviteRequest, SendMediaRequest
from telethon.tl.functions.users import GetFullUserRequest

from telethon import events, functions, types
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import ChatBannedRights, MessageActionChannelCreate
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest, GetAdminLogRequest, CreateChannelRequest, CheckUsernameRequest
from telethon.tl.functions.messages import GetFullChatRequest, GetHistoryRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.channels import EditPhotoRequest
from telethon.tl.types import ChatAdminRights
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.tl.types import ChannelParticipantsBots
from telethon.tl.types import ChannelParticipantsKicked
from telethon.tl.types import MessageActionChannelMigrateFrom
from telethon.tl.types import UserStatusEmpty
from telethon.tl.types import UserStatusLastMonth
from telethon.tl.types import UserStatusLastWeek
from telethon.tl.types import UserStatusOffline
from telethon.tl.types import UserStatusOnline
from telethon.tl.types import UserStatusRecently


from telethon.errors import (
    ChatAdminRequiredError,
    UserAdminInvalidError,
)
from . import l313l
from ..utils import is_admin
from ..sql_helper.locks_sql import get_locks, is_locked, update_lock
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type, meme_type, progress, thumb_from_audio
from ..helpers.utils import reply_id, _format
from ..sql_helper.fsub_sql import *

from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event
# All Rights Reserved for "Zed-Thon - ZelZal" "زلـزال الهيبـه"
ANTI_DDDD_ZEDTHON_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_media=True, send_stickers=True, send_gifs=True
)
from ..Config import Config

plugin_category = "admin"


async def is_admin(event, user):
    try:
        sed = await event.client.get_permissions(event.chat_id, user)
        if sed.is_admin:
            is_mod = True
        else:
            is_mod = False
    except:
        is_mod = False
    return is_mod



@l313l.ar_cmd(
    pattern="اقفل(?: |$)(.*)",
    command=("اقفل", plugin_category),
    info={
        "header": "اوامــر قفـل الحمـاية الخـاصه بـ القنـوات",
        "الوصـف": "اوامـر ذكيـه لـ قفـل / فتـح حمـاية القنـوات بالمسـح والطـرد والتقييـد لـ اول مـره فقـط ع سـورس زدثــون",
        "الاوامـر": {
            "الدردشه": "- لـ قفـل ارسـال الرسـائل فقـط",
            "التوجيه": "- لـ قفـل التـوجيـه",
            "الروابط": "- لـ قفـل ارسـال الروابـط",
            "المعرفات": "- لـ قفـل ارسـال المعـرفات",
            "الميديا": "- لـ قفـل ارسـال الوسـائط",
            "الصور": "- لـ قفـل الصـور",
            "الملصقات": "- لـ قفـل الملصقـات",
            "المتحركات": "- لـ قفـل المتحـركـات",
            "الفيديو": "- لـ قفـل الفيـديـو",
            "الصوت": "- لـ قفـل المقـاطـع الصـوتيـه",
            "البصمات": "- لـ قفـل البصمـات",
            "الفشار": "- لـ قفـل الفشـار والسـب",
            "الانلاين": "- لـ قفـل انـلاين البـوتـات",
            "البوتات": "- لـ قفـل اضـافة البـوتـات",
            "الكل": "- لـ قفـل كـل الاوامـر",
        },
        "الاسـتخـدام": "{tr}اقفل + الامــر",
    },
)
async def _(event):
    if event.is_private or event.is_group:
        return
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    zed_id = event.chat_id
    # All Rights Reserved for "Zed-Thon - ZelZal" "زلـزال الهيبـه"
    chat_per = (await event.get_chat()).default_banned_rights
    if input_str == "التفليش" or input_str == "التصفير":
        update_lock(zed_id, "bots", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة الطـرد والتحذيـر •**".format(input_str))
    if input_str == "المعرفات" or input_str == "اليوزرات":
        update_lock(zed_id, "button", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الصور":
        update_lock(zed_id, "photo", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الملصقات":
        update_lock(zed_id, "sticker", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الفيديو":
        update_lock(zed_id, "video", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الصوت" or input_str == "البصمات":
        update_lock(zed_id, "audio", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الدخول":
        update_lock(zed_id, "voice", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "المتحركات":
        update_lock(zed_id, "gif", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "تعديل الميديا":
        update_lock(zed_id, "document", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الملفات":
        update_lock(zed_id, "contact", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "التوجيه":
        update_lock(zed_id, "forward", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الدردشه" or input_str == "الدردشة":
        update_lock(zed_id, "game", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الانلاين":
        update_lock(zed_id, "inline", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الميديا" or input_str == "الوسائط":
        update_lock(zed_id, "location", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الفشار" or input_str == "السب":
        update_lock(zed_id, "rtl", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الروابط":
        update_lock(zed_id, "url", True)
        return await edit_or_reply(event, "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الكل":
        update_lock(zed_id, "bots", True)
        update_lock(zed_id, "location", True)
        update_lock(zed_id, "game", True)
        update_lock(zed_id, "forward", True)
        update_lock(zed_id, "egame", True)
        update_lock(zed_id, "rtl", True)
        update_lock(zed_id, "url", True)
        update_lock(zed_id, "contact", True)
        update_lock(zed_id, "document", True)
        update_lock(zed_id, "location", True)
        update_lock(zed_id, "button", True)
        update_lock(zed_id, "inline", True)
        update_lock(zed_id, "video", True)
        update_lock(zed_id, "photo", True)
        update_lock(zed_id, "gif", True)
        update_lock(zed_id, "sticker", True)
        update_lock(zed_id, "audio", True)
        update_lock(zed_id, "voice", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح - الطـرد - التقييـد - التحذيـر •**".format(input_str))
    else:
        if input_str:
            return await edit_delete(
                event, f"**⎉╎عذراً لايـوجـد امـر بـ اسـم :** `{input_str}`\n**⎉╎لعـرض اوامـر القفـل والفتـح ارسـل** `.م4`", time=10
            )

        return await edit_or_reply(event, "**⎉╎عـذراً عـزيـزي .. لايمكنك قفـل اي شي هنـا ...𓆰**")


@l313l.ar_cmd(
    pattern="افتح(?: |$)(.*)",
    command=("افتح", plugin_category),
    info={
        "header": "اوامــر فتـح الحمـاية الخـاصه بـ القنـوات",
        "الوصـف": "اوامـر ذكيـه لـ قفـل / فتـح حمـاية القنـوات بالمسـح والطـرد والتقييـد لـ اول مـره فقـط ع سـورس زدثــون",
        "الاوامـر": {
            "الدردشه": "- لـ فتـح ارسـال الرسـائل فقـط",
            "التوجيه": "- لـ فتـح التـوجيـه",
            "الروابط": "- لـ فتـح ارسـال الروابـط",
            "المعرفات": "- لـ فتـح ارسـال المعـرفات",
            "الميديا": "- لـ فتـح ارسـال الوسـائط",
            "الصور": "- لـ فتـح الصـور",
            "الملصقات": "- لـ فتـح الملصقـات",
            "المتحركات": "- لـ فتـح المتحـركـات",
            "الفيديو": "- لـ فتـح الفيـديـو",
            "الصوت": "- لـ فتـح المقـاطـع الصـوتيـه",
            "البصمات": "- لـ فتـح البصمـات",
            "الفشار": "- لـ فتـح الفشـار والسـب",
            "الانلاين": "- لـ فتـح انـلاين البـوتـات",
            "البوتات": "- لـ فتـح اضـافة البـوتـات",
            "الكل": "- لـ فتـح كـل الاوامـر",
        },
        "الاسـتخـدام": "{tr}افتح + الامــر",
    },
)
async def _(event):
    if event.is_private or event.is_group:
        return
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    zed_id = event.chat_id
   # All Rights Reserved for "Zed-Thon - ZelZal" "زلـزال الهيبـه"
    #if event.is_group or event.is_private:
        #return await edit_delete(event, "**- عـذراً .. هـذه ليست قنـاة لقفـل الأشيـاء**")
    chat_per = (await event.get_chat()).default_banned_rights
    if input_str == "التفليش" or input_str == "التصفير":
        update_lock(zed_id, "bots", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "الصور":
        update_lock(zed_id, "photo", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "الملصقات":
        update_lock(zed_id, "sticker", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "المتحركات":
        update_lock(zed_id, "gif", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "تعديل الميديا":
        update_lock(zed_id, "document", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "الملفات":
        update_lock(zed_id, "contact", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "التوجيه":
        update_lock(zed_id, "forward", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "الفيديو":
        update_lock(zed_id, "video", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "الصوت" or input_str == "البصمات":
        update_lock(zed_id, "audio", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "الدخول":
        update_lock(zed_id, "voice", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "الفشار" or input_str == "السب":
        update_lock(zed_id, "rtl", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "الروابط":
        update_lock(zed_id, "url", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "الدردشه" or input_str == "الدردشة":
        update_lock(zed_id, "game", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "المعرفات" or input_str == "اليوزرات":
        update_lock(zed_id, "button", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "الانلاين":
        update_lock(zed_id, "inline", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "الكل":
        update_lock(zed_id, "bots", False)
        update_lock(zed_id, "game", False)
        update_lock(zed_id, "forward", False)
        update_lock(zed_id, "egame", False)
        update_lock(zed_id, "rtl", False)
        update_lock(zed_id, "url", False)
        update_lock(zed_id, "contact", False)
        update_lock(zed_id, "document", False)
        update_lock(zed_id, "location", False)
        update_lock(zed_id, "button", False)
        update_lock(zed_id, "inline", False)
        update_lock(zed_id, "video", False)
        update_lock(zed_id, "photo", False)
        update_lock(zed_id, "gif", False)
        update_lock(zed_id, "sticker", False)
        update_lock(zed_id, "audio", False)
        update_lock(zed_id, "voice", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    if input_str == "الميديا" or input_str == "الوسائط":
        update_lock(zed_id, "location", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **.. بنجـاح ✅**".format(input_str))
    else:
        if input_str:
            return await edit_delete(
                event, f"**⎉╎عذراً لايـوجـد امـر بـ اسـم :** `{input_str}`\n**⎉╎لعـرض اوامـر القفـل والفتـح ارسـل** `.م4`", time=10
            )

        return await edit_or_reply(event, "**⎉╎عـذراً عـزيـزي .. لايمكنك اعـادة فتـح اي شي هنـا ...𓆰**")


@l313l.ar_cmd(
    pattern="حماية القناة$",
    command=("حماية القناة", plugin_category),
    info={
        "header": "لـ عـرض اعـدادات حمـاية القنـاة الخـاصـه ببـوت زدثــون",
        "الاسـتخـدام": "{tr}حماية القناة",
    },
)
async def _(event):
    if event.is_group or event.is_private:
        return await edit_or_reply(event, "**- عـذراً .. هـذه ليست قنـاة لقفـل الأشيـاء**")
    if event.fwd_from:
        return
   # All Rights Reserved for "Zed-Thon - ZelZal" "زلـزال الهيبـه"
    res = "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n**- اليك إعـدادات حماية القنـاة ⚓**\n**- ❌ ⇽ مغلـق | ✅ ⇽ مفتـوح**\n\n"
    ubots = "❌" if is_locked(event.chat_id, "bots") else "✅"
    uegame = "❌" if is_locked(event.chat_id, "egame") else "✅"
    uphoto = "❌" if is_locked(event.chat_id, "photo") else "✅"
    uvideo = "❌" if is_locked(event.chat_id, "video") else "✅"
    ugif = "❌" if is_locked(event.chat_id, "gif") else "✅"
    urtl = "❌" if is_locked(event.chat_id, "rtl") else "✅"
    uforward = "❌" if is_locked(event.chat_id, "forward") else "✅"
    ubutton = "❌" if is_locked(event.chat_id, "button") else "✅"
    uurl = "❌" if is_locked(event.chat_id, "url") else "✅"
    ugame = "❌" if is_locked(event.chat_id, "game") else "✅"
    udocument = "❌" if is_locked(event.chat_id, "document") else "✅"
    usticker = "❌" if is_locked(event.chat_id, "sticker") else "✅"
    ulocation = "❌" if is_locked(event.chat_id, "location") else "✅"
    ucontact = "❌" if is_locked(event.chat_id, "contact") else "✅"
    ubutton = "❌" if is_locked(event.chat_id, "button") else "✅"
    uinline = "❌" if is_locked(event.chat_id, "inline") else "✅"
    uaudio = "❌" if is_locked(event.chat_id, "audio") else "✅"
    uvoice = "❌" if is_locked(event.chat_id, "voice") else "✅"
    res += f"**⎉╎الدردشـة :** {ugame}\n"
    res += f"**⎉╎الصـور :** {uphoto}\n"
    res += f"**⎉╎الملصقـات :** {usticker}\n"
    res += f"**⎉╎المتحـركـات :** {ugif}\n"
    res += f"**⎉╎الفيـديـو :** {uvideo}\n"
    res += f"**⎉╎الصـوت :** {uaudio}\n"
    #res += f"**⎉╎الدخـول :** {uvoice}\n"
    res += f"**⎉╎الـروابـط :** {uurl}\n"
    res += f"**⎉╎المعـرفـات :** {ubutton}\n"
    res += f"**⎉╎التـوجيـه :** {uforward}\n"
    res += f"**⎉╎الميديا :** {ulocation}\n"
    res += f"**⎉╎تعديـل الميديـا :** {udocument}\n"
    res += f"**⎉╎الفشار :** {urtl}\n"
    #res += f"**⎉╎التصفيـر :** {ubots}\n"
    res += f"**⎉╎الانـلايـن :** {uinline}\n"
    await edit_or_reply(event, res)

@l313l.ar._cmd(
    pattern="الاعدادات$",
    command=("الاعدادات", plugin_category),
    info={
        "header": "لـ عـرض اعـدادات حمـاية القنـاة الخـاصـه ببـوت زدثــون",
        "الاسـتخـدام": "{tr}الاعدادات",
    },
)
async def _(event):
    if event.is_group or event.is_private:
        return #await edit_or_reply(event, "**- عـذراً .. هـذه ليست قنـاة لقفـل الأشيـاء**")
    if event.fwd_from:
        return
   # All Rights Reserved for "Zed-Thon - ZelZal" "زلـزال الهيبـه"
    res = "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n**- اليك إعـدادات حماية القنـاة ⚓**\n**- ❌ ⇽ مغلـق | ✅ ⇽ مفتـوح**\n\n"
    ubots = "❌" if is_locked(event.chat_id, "bots") else "✅"
    uegame = "❌" if is_locked(event.chat_id, "egame") else "✅"
    uphoto = "❌" if is_locked(event.chat_id, "photo") else "✅"
    uvideo = "❌" if is_locked(event.chat_id, "video") else "✅"
    ugif = "❌" if is_locked(event.chat_id, "gif") else "✅"
    urtl = "❌" if is_locked(event.chat_id, "rtl") else "✅"
    uforward = "❌" if is_locked(event.chat_id, "forward") else "✅"
    ubutton = "❌" if is_locked(event.chat_id, "button") else "✅"
    uurl = "❌" if is_locked(event.chat_id, "url") else "✅"
    ugame = "❌" if is_locked(event.chat_id, "game") else "✅"
    udocument = "❌" if is_locked(event.chat_id, "document") else "✅"
    usticker = "❌" if is_locked(event.chat_id, "sticker") else "✅"
    ulocation = "❌" if is_locked(event.chat_id, "location") else "✅"
    ucontact = "❌" if is_locked(event.chat_id, "contact") else "✅"
    ubutton = "❌" if is_locked(event.chat_id, "button") else "✅"
    uinline = "❌" if is_locked(event.chat_id, "inline") else "✅"
    uaudio = "❌" if is_locked(event.chat_id, "audio") else "✅"
    uvoice = "❌" if is_locked(event.chat_id, "voice") else "✅"
    res += f"**⎉╎الدردشـة :** {ugame}\n"
    res += f"**⎉╎الصـور :** {uphoto}\n"
    res += f"**⎉╎الملصقـات :** {usticker}\n"
    res += f"**⎉╎المتحـركـات :** {ugif}\n"
    res += f"**⎉╎الفيـديـو :** {uvideo}\n"
    res += f"**⎉╎الصـوت :** {uaudio}\n"
    #res += f"**⎉╎الدخـول :** {uvoice}\n"
    res += f"**⎉╎الـروابـط :** {uurl}\n"
    res += f"**⎉╎المعـرفـات :** {ubutton}\n"
    res += f"**⎉╎التـوجيـه :** {uforward}\n"
    res += f"**⎉╎الميديا :** {ulocation}\n"
    res += f"**⎉╎تعديـل الميديـا :** {udocument}\n"
    res += f"**⎉╎الفشار :** {urtl}\n"
    #res += f"**⎉╎التصفيـر :** {ubots}\n"
    res += f"**⎉╎الانـلايـن :** {uinline}\n"
    await edit_or_reply(event, res)

@l313l.ar_cmd(incoming=True, forword=None)
async def check_incoming_messages(event):
    if event.is_private or event.is_group:
        return
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    zed_dev = (5427469031, 1234567890)  # أرقام أخرى للمطورين الإضافيين
    zelzal = event.sender_id
    malath = l313l.uid
    hhh = event.message.text
    mmm = event.message
    zed_id = event.chat_id
    mediatype = await meme_type(mmm)
    if is_locked(zed_id, "rtl") and ("خرا" in hhh or "كسها" in hhh or "كسمك" in hhh or "كسختك" in hhh or "عيري" in hhh or "كسخالتك" in hhh or "خرا بالله" in hhh or "عير بالله" in hhh or "كسخواتكم" in hhh or "اختك" in hhh or "بڪسسخخت" in hhh or "كحاب" in hhh or "مناويج" in hhh or "كحب" in hhh or " كواد " in hhh or "كواده" in hhh or "تبياته" in hhh or "تبياتة" in hhh or "فرخ" in hhh or "كحبة" in hhh or "فروخ" in hhh or "طيز" in hhh or "آإيري" in hhh or "اختج" in hhh or "سالب" in hhh or "موجب" in hhh or "فحل" in hhh or "كسي" in hhh or "كسك" in hhh or "كسج" in hhh or "مكوم" in hhh or "نيج" in hhh or "نتنايج" in hhh or "كس " in hhh or "ديوث" in hhh or "دياث" in hhh or "اديث" in hhh or "محارم" in hhh or "سكس" in hhh or "مصي" in hhh or "اعرب" in hhh or "أعرب" in hhh or "قحب" in hhh or "قحاب" in hhh or "عراب" in hhh or "كسم" in hhh or "عربك" in hhh or "مخنث" in hhh or "مخنوث" in hhh or "فتال" in hhh or "زاني" in hhh or "زنا" in hhh or "لقيط" in hhh or "بنات شوارع" in hhh or "بنت شوارع" in hhh or "نيك" in hhh or "منيوك" in hhh or "منيوج" in hhh or "نايك" in hhh or "قواد" in hhh or "زب" in hhh or "اير" in hhh or "ممحو" in hhh or "بنت شارع" in hhh or " است " in hhh or "اسات" in hhh or "زوب" in hhh or "عيير" in hhh or "كس " in hhh or "مربرب" in hhh or " خول " in hhh or "عرص" in hhh or "قواد" in hhh or "اهلاتك" in hhh or "جلخ" in hhh or "ورع" in hhh or "شرمو" in hhh or "فرك" in hhh or "رهط" in hhh):
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete()
                zzz = await event.reply("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع الفشـار والسب هنـا ⚠️**")
                await sleep(5)
                await zzz.delete()
            except Exception as e:
                return
    if is_locked(zed_id, "game") and event.message.text:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete()
                zzz = await event.reply("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال الرسـائل النصيـه هنـا ⚠️**")
                await sleep(5)
                await zzz.delete()
            except Exception as e:
                return
    if is_locked(zed_id, "forward") and (event.fwd_from or event.message.forward):
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete()
                zzz = await event.reply("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع التوجيـه هنـا ⚠️**")
                await sleep(5)
                await zzz.delete()
            except Exception as e:
                return
    if is_locked(zed_id, "button") and "@" in hhh:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete()
                zzz = await event.reply("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال المعـرفات هنـا ⚠️**")
                await sleep(5)
                await zzz.delete()
            except Exception as e:
                return
    if is_locked(zed_id, "photo") and event.message.media and mediatype == "Photo":
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete()
                zzz = await event.reply("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال الصـور هنـا ⚠️**")
                await sleep(5)
                await zzz.delete()
            except Exception as e:
                return
    if is_locked(zed_id, "location") and event.message.media:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete()
                zzz = await event.reply("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال الميـديـا هنـا ⚠️**")
                await sleep(5)
                await zzz.delete()
            except Exception as e:
                return
    if is_locked(zed_id, "sticker") and event.message.media and mediatype in ["Video Sticker", "Animated Sticker", "Static Sticker"]:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete()
                zzz = await event.reply("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال الملصقـات هنـا ⚠️**")
                await sleep(5)
                await zzz.delete()
            except Exception as e:
                return
    if is_locked(zed_id, "video") and event.message.media and mediatype == "Video":
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete()
                zzz = await event.reply("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال مقـاطـع الفيـديـو هنـا ⚠️**")
                await sleep(5)
                await zzz.delete()
            except Exception as e:
                return
    if is_locked(zed_id, "audio") and (event.message.audio or event.message.voice):
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete()
                zzz = await event.reply("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال المقـاطع الصـوتيـه هنـا ⚠️**")
                await sleep(5)
                await zzz.delete()
            except Exception as e:
                return
    if is_locked(zed_id, "gif") and event.message.gif:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete()
                zzz = await event.reply("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال المتحـركات هنـا ⚠️**")
                await sleep(5)
                await zzz.delete()
            except Exception as e:
                return
    if is_locked(zed_id, "contact") and event.message.document:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete()
                zzz = await event.reply("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال الملفات هنـا ⚠️**")
                await sleep(5)
                await zzz.delete()
            except Exception as e:
                return
    if is_locked(zed_id, "url") and "http" in hhh:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete()
                zzz = await event.reply("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال الروابـط هنـا ⚠️**")
                await sleep(5)
                await zzz.delete()
            except Exception as e:
                return
    if is_locked(zed_id, "inline") and event.message.via_bot:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete()
                zzz = await event.reply("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع استـخـدام الانـلايـن هنـا ⚠️**")
                await sleep(5)
                await zzz.delete()
            except Exception as e:
                return


# Copyright (C) 2022 Zed-Thon
@l313l.on(events.MessageEdited)
async def check_edit_media(event):
    if not event.is_channel:
        return
    if is_locked(event.chat_id, "document") and event.message.media: #Write Code By T.me/zzzzl1l
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        zed_dev = (5427469031, 1234567890)  # أرقام أخرى للمطورين الإضافيين
        zelzal = event.sender_id
        malath = l313l.uid
        hhh = event.message.text
        #zed_id = event.chat_id
        user = await event.get_sender()
        if zelzal == malath or zelzal in zed_dev:
            return
        else:
            try:
                await event.delete() #Write Code By T.me/zzzzl1l
                zzz = await event.reply(f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡** - حمـاية القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n⌔╎**عـذࢪاً عـزيـزي الادمـن**  \n⌔╎**يُمنـع تعديـل الميديـا هنـا 🚫**\n⌔╎**تم حـذف التعديـل .. بنجـاح ☑️**", link_preview=False)
                await sleep(5)
                await zzz.delete()
            except Exception:  #Write Code By T.me/zzzzl1l
                return


# Copyright (C) 2022 Zed-Thon
"""@events.register(events.ChatAction(func=lambda e: e.action_message is None))
async def chat_action_empty(event: events.ChatAction.Event):
    if event.is_private:
        return
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
    # All Rights Reserved for "Zed-Thon - ZelZal" "زلـزال الهيبـه"
    zed_dev = (5427469031, 1234567890)  # أرقام أخرى للمطورين الإضافيين
    malath = l313l.uid
    adminlog = await event.client.get_admin_log(event.chat_id, limit=1, ban=True)
    if is_locked(event.chat_id, "bots"):
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
        is_ban_able = False
        async for event in client.iter_admin_log(event.chat_id, ban=True, limit=1):
            is_ban_able = True
            if ruser.id == malath or ruser.id in zed_dev:
                return
            else:
                try:
                    await event.client.kick_participant(event.chat_id, ruser.id)
                    await l313l.send_message(event.chat_id, 
                        "**⎉╎عـذراً**  [عزيـزي⚠️](tg://user?id={})  **يُمنـع الانضمـام لـ هـذه القنـوات •**\n\n**⎉╎تـم حظـرك .. بنجـاح 🛂**\n\nᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗘𝗗𝗧𝗛𝗢𝗡╎@ZedThon".format(
                        ruser.id
                        )
                    )
                except Exception as e:
                    await l313l.send_message(event.chat_id, 
                        "**⎉╎عـذراً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا 𓆰** \n`{}`".format(
                            str(e)
                        )
                    )
                    update_lock(event.chat_id, "bots", False)
                    return
        if BOTLOG and is_ban_able:
            await event.client.send_message(BOTLOG_CHATID,
                "**⎉╎سيـدي المـالك**\n\n**⎉╎قـام هـذا** [الشخـص](tg://user?id={})  \n**⎉╎بالانضمـام للقنـاة**\n**⎉╎تم تحذيـر الشخـص وطـرده .. بنجـاح ✓𓆰**".format(
                    zedy.id
                )
            )
"""

@l313l.on(events.ChatAction())
async def _(event):
    if not is_locked(event.chat_id, "voice"):
        return
    if event.is_channel:  # التحقق من أن الحدث يأتي من قناة
        channel = await event.get_chat()
        admin = channel.admin_rights
        creator = channel.creator
        if not admin and not creator:
            return
        zed_dev = (5427469031, 1234567890)  # أرقام أخرى للمطورين الإضافيين
        if event.user_joined: 
            zedy = await event.client.get_entity(event.user_id)
            is_ban_able = True
            rights = types.ChatBannedRights(until_date=None, view_messages=True)
            if zedy.id in zed_dev:
                return
            try:
                await event.client(
                    functions.channels.EditBannedRequest(
                        event.chat_id, zedy.id, rights
                    )
                )
                zzz = await event.reply(f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية القنـاة \n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n⌔╎عـذࢪاً {zedy.first_name} \n⌔╎يُمنـع الانضمـام لـ هـذه القناة 🚷•\n⌔╎تـم حظـࢪه .. بنجـاح ☑️", link_preview=False)
                await sleep(3)
                await zzz.delete()
            except Exception:
                return
            if BOTLOG and is_ban_able:
                ban_reason_msg = await event.client.send_message(BOTLOG_CHATID,
                    "**⎉╎سيـدي المـالك**\n\n**⎉╎قـام هـذا** [الشخـص](tg://user?id={})  \n**⎉╎بالانضمـام للقنـاة**\n**⎉╎تم تحذيـر الشخـص وطـرده .. بنجـاح ✓𓆰**".format(
                        zedy.id
                    )
                )

# Copyright (C) 2022 Zed-Thon
@l313l.on(events.ChatAction())
async def handle_event(event):
    global kicked_count
    if not is_locked(event.chat_id, "bots"):
        return
    if "kicked" in event.message.message:
        zedy = await event.client.get_entity(event.message.sender_id)
        kicked_count += 1
        if kicked_count == 3:
            try:
                await l313l(EditAdminRequest(event.chat_id, zedy.id, change_info=False, post_messages=False, edit_messages=False, delete_messages=False, ban_users=False, invite_users=False, pin_messages=False, add_admins=False))
                await l313l(EditAdminRequest(event.chat_id, zedy.id, rank=''))
                kicked_count = 0
                await edit_or_reply(event, f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية القنـوات ](t.me/ZThon)\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n⌔╎**مشرف خاين** [{zedy.first_name}](tg://user?id={zedy.id}) .\n⌔╎**حاول تفليش القنـوات•**\n⌔╎**تم تنزيلـه .. بنجـاح ✅**", link_preview=False)
            except Exception as e:
                return
            if BOTLOG:
                await event.client.send_message(BOTLOG_CHATID, "**⎉╎سيـدي المـالك**\n\n**⎉╎قـام هـذا** [الشخـص](tg://user?id={})  \n**⎉╎باضـافة بـوت للقنـاة**\n**⎉╎تم تحذيـر الشخـص وطـرد البـوت .. بنجـاح ✓𓆰**".format(zedy.id))
