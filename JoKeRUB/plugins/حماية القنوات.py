import requests
import asyncio
import random
import os
import sys
import html
import urllib.request
from datetime import datetime, timedelta
from time import sleep

try:
    import unicodedata
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    os.system("pip3 install unicodedata bs4")
    import unicodedata
    from bs4 import BeautifulSoup

from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import Channel, Chat, InputPhoto, User, InputMessagesFilterEmpty

from telethon import events
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import GetHistoryRequest, ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _catutils, reply_id
from ..sql_helper.globals import gvarstatus
from . import ALIVE_NAME, BOTLOG, BOTLOG_CHATID, l313l, edit_delete, get_user_from_event
"""
LOGS = logging.getLogger(__name__)
ANTHAL = gvarstatus("ANTHAL") or "(ايقاف الانتحال|اعادة|اعاده)"
# =========================================================== #
#                                                             𝙕𝙏𝙝𝙤𝙣
# =========================================================== #
WW_CHANGED = "**⎉╎جـارِ الانتحـال . . .**"
ZZ_CHANGED = "**⎉╎تم انتحـال الشخص .. بنجـاح 🥷**"
# =========================================================== #
#                                                             𝙕𝙏𝙝𝙤𝙣
# =========================================================== #

@zedub.zed_cmd(pattern="انتحال(?: |$)(.*)")
async def _(event):
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    zzz = await edit_or_reply(event, WW_CHANGED)
    user_id = replied_user.id
    profile_pic = await event.client.download_profile_photo(user_id, Config.TEMP_DIR)
    first_name = html.escape(replied_user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.last_name
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
    replied_user = (await event.client(GetFullUserRequest(replied_user.id))).full_user
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await event.client(functions.account.UpdateProfileRequest(first_name=first_name))
    await event.client(functions.account.UpdateProfileRequest(last_name=last_name))
    await event.client(functions.account.UpdateProfileRequest(about=user_bio))
    try:
        pfile = await event.client.upload_file(profile_pic)
    except Exception as e:
        return await edit_delete(event, f"**اووبس خطـأ بالانتحـال:**\n__{e}__")
    if profile_pic.endswith((".mp4", ".MP4")):
        size = os.stat(profile_pic).st_size
        if size > 2097152:
            await zzz.edit("⎉╎يجب ان يكون الحجم اقل من 2 ميغا ✅")
            os.remove(profile_pic)
            return
        zpic = None
        zvideo = await event.client.upload_file(profile_pic)
    else:
        zpic = await event.client.upload_file(profile_pic)
        zvideo = None
    try:
        await event.client(
            functions.photos.UploadProfilePhotoRequest(
                file=zpic, video=zvideo, video_start_ts=0.01
            )
        )
    except Exception as e:
        await zzz.edit(f"**خطأ:**\n`{str(e)}`")
    await edit_or_reply(zzz, ZZ_CHANGED)
    try:
        os.remove(profile_pic)
    except Exception as e:
        LOGS.info(str(e))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#الانتحـــال\n**⪼ تم انتحـال حسـاب الشخـص ↫** [{first_name}](tg://user?id={user_id }) **بنجاح ✅**\n**⪼ لـ الغـاء الانتحـال ارسـل** ( `.اعاده` )",
        )


@zedub.zed_cmd(pattern=f"{ANTHAL}$")
async def revert(event):
    firstname = gvarstatus("FIRST_NAME") or ALIVE_NAME
    lastname = gvarstatus("LAST_NAME") or ""
    bio = gvarstatus("DEFAULT_BIO") or "{وَتَوَكَّلْ عَلَى اللَّهِ ۚ وَكَفَىٰ بِاللَّهِ وَكِيلًا}"
    await event.client(
        functions.photos.DeletePhotosRequest(
            await event.client.get_profile_photos("me", limit=1)
        )
    )
    await event.client(functions.account.UpdateProfileRequest(about=bio))
    await event.client(functions.account.UpdateProfileRequest(first_name=firstname))
    await event.client(functions.account.UpdateProfileRequest(last_name=lastname))
    await edit_delete(event, "**⎉╎تمت اعادة الحساب لوضعـه الاصلـي \n⎉╎والغـاء الانتحـال .. بنجـاح ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#الغـاء_الانتحـال\n**⪼ تم الغـاء الانتحـال .. بنجـاح ✅**\n**⪼ تم إعـاده معلـوماتك الى وضعـها الاصـلي**",
        )

# ================================================================================================ #
# =========================================الازعاج================================================= #
# ================================================================================================ #

@zedub.zed_cmd(pattern="مزاد(?: |$)(.*)")
async def _(event):
    reply = await event.get_reply_message()
    args = event.pattern_match.group(1)
    if not reply and not args:
        return
    if reply and not args:
        bot_token = reply.text
    else:
        bot_token = args
    if bot_token.startswith("@"):
        bot_token = bot_token.replace("@", "")
    chat = "@GetUsernameBot" #Code by T.me/zzzzl1l
    zed = await edit_or_reply(event, "**╮ جـارِ الكشـف عـن اليـوزر فـي المـزاد ...𓅫╰**")
    async with borg.conversation(chat) as conv: #Code by T.me/zzzzl1l
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(bot_token) #Code by T.me/zzzzl1l
            await asyncio.sleep(5)
            zedthon = await conv.get_response()
            await zed.delete()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=f"<b>⎉╎اليـوزر -->  @{bot_token}\n⎉╎رابـط اليـوزر ع المـزاد :  <a href = https://fragment.com/username/{bot_token}/1>اضغـط هنـا</a>\n⎉╎تم الكشف بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>",
                parse_mode="html",
            )
        except YouBlockedUserError: #Code by T.me/zzzzl1l
            await zedub(unblock("GetUsernameBot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(bot_token)
            await asyncio.sleep(5)
            zedthon = await conv.get_response()
            await zed.delete()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=f"<b>⎉╎اليـوزر -->  @{bot_token}\n⎉╎رابـط اليـوزر ع المـزاد :  <a href = https://fragment.com/username/{bot_token}/1>اضغـط هنـا</a>\n⎉╎تم الكشف بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>",
                parse_mode="html",
            )



def get_tiktok_user_info(username):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    r = requests.get(f"https://www.tiktok.com/@{username}", headers=headers)
    server_log = str(r.text)

    try:
        soup = BeautifulSoup(server_log, 'html.parser')
        script = soup.find(id='SIGI_STATE').contents
        data = str(script).split('},"UserModule":{"users":{')[1]
        
        user_info = {}
        user_info['user_id'] = data.split('"id":"')[1].split('",')[0]
        user_info['name'] = data.split(',"nickname":"')[1].split('",')[0]
        user_info['followers'] = data.split('"followerCount":')[1].split(',')[0]
        user_info['following'] = data.split('"followingCount":')[1].split(',')[0]
        user_info['user_create_time'] = user_create_time(int(user_info['user_id']))
        user_info['last_change_name'] = datetime.fromtimestamp(int(data.split('"nickNameModifyTime":')[1].split(',')[0]))
        user_info['account_region'] = data.split('"region":"')[1].split('"')[0]
        
        return user_info
    except IndexError:
        return None


def user_create_time(url_id):
    binary = "{0:b}".format(url_id)
    i = 0
    bits = ""
    while i < 31:
        bits += binary[i]
        i += 1
    timestamp = int(bits, 2)
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object


#Code by T.me/zzzzl1l
@zedub.zed_cmd(pattern="tt(?: |$)(.*)")
async def zelzal_gif(event):
    username = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not username and reply:
        username = reply.text
    if not username:
        return await edit_delete(event, "**- ارسـل (.tt) + يـوزر تيـك تـوك او بالـرد ع يـوزر تيـك تـوك**", 10)
    if username.startswith("@"):
        username = username.replace("@", "")
    zed = await edit_or_reply(event, "**⎉╎جـارِ جلب معلومـات TikTok .. انتظر قليلا ▬▭**")
    data = get_tiktok_user_info(username)
    if data:
        id = data['user_id']
        name = data['name']
        followers = data['followers']
        following = data['following']
        time = data['user_create_time']
        last = data['last_change_name']
        acc = data['account_region']
        country_emoji = unicodedata.lookup(f"REGIONAL INDICATOR SYMBOL LETTER {acc[0]}")
        country_emoji += unicodedata.lookup(f"REGIONAL INDICATOR SYMBOL LETTER {acc[1]}")
        zzz = f"𓆩 𝗭𝗧𝗵𝗼𝗻 𝗧𝗶𝗸𝗧𝗼𝗸 𝗜𝗻𝗳𝗼 - **معلومـات تيـك تـوك** 𓆪\n⋆─┄─┄─┄─┄─┄─┄─┄┄─┄─⋆\n**• الاسـم :** {name}\n**• اليـوزر :** {username}\n**• الايـدي :** {id}\n**• المتابعـين :** {followers}\n**• يتابـع :** {following}\n**• الدولـة :** {acc} {country_emoji}\n**• تاريـخ إنشـاء الحسـاب :** {time}"
        pic_z = f"https://graph.org/file/dd383bc88dc1ce1a1971c.jpg"
        try:
            await event.client.send_file(
                event.chat_id,
                pic_z,
                caption=zzz
            )
            await zed.delete()
        except ChatSendMediaForbiddenError as err:
            await edit_or_reply(zed, f"𓆩 𝗭𝗧𝗵𝗼𝗻 𝗧𝗶𝗸𝗧𝗼𝗸 𝗜𝗻𝗳𝗼 - **معلومـات تيـك تـوك** 𓆪\n⋆─┄─┄─┄─┄─┄─┄─┄┄─┄─⋆\n**• الاسـم :** {name}\n**• اليـوزر :** {username}\n**• الايـدي :** {id}\n**• المتابعـين :** {followers}\n**• يتابـع :** {following}\n**• الدولـة :** {acc} {country_emoji}\n**• تاريـخ إنشـاء الحسـاب :** {time}")
            await zed.delete()
    else:
        await zed.edit("**- لم استطـع الكشـف عـن الحسـاب او ان اليـوزر غيـر موجـود**")


@zedub.zed_cmd(pattern="nn(?: |$)(.*)")
async def zelzal_gif(event):
    zelzal = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not zelzal and reply:
        zelzal = reply.text
    if not zelzal:
        return await edit_delete(event, "**- ارسـل (.nn) + يـوزر انستـا او بالـرد ع يـوزر انستـا**", 10)
    if zelzal.startswith("@"):
        zelzal = zelzal.replace("@", "")
    zed = await edit_or_reply(event, "**⎉╎جـارِ جلب معلومـات الانستـا .. انتظر قليلا ▬▭**")
    chat = "@instagram_information_users_bot" # Code by T.me/zzzzl1l
    async with borg.conversation(chat) as conv: # Code by T.me/zzzzl1l
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(zelzal)
            await asyncio.sleep(3)
            zedthon = await conv.get_response()
            malath = zedthon.text
            if "Username : " in zedthon.text: # Code by T.me/zzzzl1l
                zzz = malath.replace("Username : `username`", f"**• اليـوزر :** `{zelzal}`").replace("Name : ", "**• الاسـم :** ").replace("ID : ", "**• الايـدي :** ").replace("Bio : ", "**• البايـو :** ").replace("Posts : ", "**• المنشـورات :** ").replace("Followers : ", "**• المتابعيـن :** ").replace("Following : ", "**• المتابعهـم :** ").replace("\n\n", "\n")
                zz = f"𓆩 𝗭𝗧𝗵𝗼𝗻 𝗜𝗻𝘀𝘁𝗮 𝗜𝗻𝗳𝗼 - **معلومـات انستـا** 𓆪\n⋆─┄─┄─┄─┄─┄─┄─┄┄─┄─⋆\n{zzz}"
                try:
                    await borg.send_file(
                        event.chat_id,
                        zedthon,
                        caption=zz,
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError as err:
                    await borg.send_message(event.chat_id, zz)
                    await zed.delete()
            else:
                await zed.edit("**- لم استطـع الكشـف عـن الحسـاب او ان اليـوزر غيـر موجـود**")
        except YouBlockedUserError: #Code by T.me/zzzzl1l
            await zedub(unblock("instagram_information_users_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(zelzal)
            await asyncio.sleep(3)
            zedthon = await conv.get_response()
            malath = zedthon.text
            if "Username : " in zedthon.text: # Code by T.me/zzzzl1l
                zzz = malath.replace("Username : `username`", f"**• اليـوزر :** `{zelzal}`").replace("Name : ", "**• الاسـم :** ").replace("ID : ", "**• الايـدي :** ").replace("Bio : ", "**• البايـو :** ").replace("Posts : ", "**• المنشـورات :** ").replace("Followers : ", "**• المتابعيـن :** ").replace("Following : ", "**• المتابعهـم :** ").replace("\n\n", "\n")
                zz = f"𓆩 𝗭𝗧𝗵𝗼𝗻 𝗜𝗻𝘀𝘁𝗮 𝗜𝗻𝗳𝗼 - **معلومـات انستـا** 𓆪\n⋆─┄─┄─┄─┄─┄─┄─┄┄─┄─⋆\n{zzz}"
                try:
                    await borg.send_file(
                        event.chat_id,
                        zedthon,
                        caption=zz,
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError as err:
                    await borg.send_message(event.chat_id, zz)
                    await zed.delete()
            else:
                await zed.edit("**- لم استطـع الكشـف عـن الحسـاب او ان اليـوزر غيـر موجـود**")
"""
###############################################################
# Zed-Thon - ZelZal
# Copyright (C) 2022 Zedthon . All Rights Reserved
#
# This file is a part of < https://github.com/Zed-Thon/ZelZal/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/Zed-Thon/ZelZal/blob/master/LICENSE/>.

""" 
اوامـر حمـاية القنـوات بالمسـح والطـرد والتقييـد
حقـوق : @ZedThon
@zzzzl1l - كتـابـة الملـف :  زلــزال الهيبــه

"""
import contextlib
import base64
import asyncio
import io
import re
from asyncio import sleep
from datetime import datetime
from math import sqrt

from telethon.events import InlineQuery, callbackquery
from telethon import Button
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
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.types import (
    ChatAdminRights,
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChannelParticipantsKicked,
    ChatBannedRights,
    MessageActionChannelMigrateFrom,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)
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


plugin_category = "الادمن"


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
    pattern="قفل(?: |$)(.*)",
    command=("قفل", plugin_category),
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
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة الطـرد والتحذيـر •**".format(input_str))
    if input_str == "المعرفات" or input_str == "اليوزرات":
        update_lock(zed_id, "button", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الصور":
        update_lock(zed_id, "photo", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الملصقات":
        update_lock(zed_id, "sticker", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الفيديو":
        update_lock(zed_id, "video", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الصوت" or input_str == "البصمات":
        update_lock(zed_id, "audio", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الدخول":
        update_lock(zed_id, "voice", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "المتحركات":
        update_lock(zed_id, "gif", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "تعديل الميديا":
        update_lock(zed_id, "document", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الملفات":
        update_lock(zed_id, "contact", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "التوجيه":
        update_lock(zed_id, "forward", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الدردشه" or input_str == "الدردشة":
        update_lock(zed_id, "game", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الانلاين":
        update_lock(zed_id, "inline", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الميديا" or input_str == "الوسائط":
        update_lock(zed_id, "location", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الفشار" or input_str == "السب":
        update_lock(zed_id, "rtl", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الروابط":
        update_lock(zed_id, "url", True)
        return await edit_or_reply(event, "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎تـم قفـل {} بنجـاح ✅ •**\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
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
    pattern="فتح(?: |$)(.*)",
    command=("فتح", plugin_category),
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
    res = "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n**- اليك إعـدادات حماية القنـاة ⚓**\n**- ❌ ⇽ مغلـق | ✅ ⇽ مفتـوح**\n\n"
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

@l313l.ar_cmd(
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
    res = "ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n**- اليك إعـدادات حماية القنـاة ⚓**\n**- ❌ ⇽ مغلـق | ✅ ⇽ مفتـوح**\n\n"
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
    zed_dev = (5427469031, 1895219306, 925972505, 1346542270, 1885375980, 1721284724, 1951523146, 1243462298, 1037828349, 1985711199, 2028523456, 2045039090, 1764272868, 2067387667, 294317157, 2066568220, 1403932655, 1389046667, 444672531, 2055451976, 294317157, 2134101721, 1719023510, 1985225531, 2107283646, 2146086267)
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
                zzz = await event.reply("ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع الفشـار والسب هنـا ⚠️**")
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
                zzz = await event.reply("ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال الرسـائل النصيـه هنـا ⚠️**")
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
                zzz = await event.reply("ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع التوجيـه هنـا ⚠️**")
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
                zzz = await event.reply("ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال المعـرفات هنـا ⚠️**")
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
                zzz = await event.reply("ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال الصـور هنـا ⚠️**")
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
                zzz = await event.reply("ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال الميـديـا هنـا ⚠️**")
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
                zzz = await event.reply("ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال الملصقـات هنـا ⚠️**")
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
                zzz = await event.reply("ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال مقـاطـع الفيـديـو هنـا ⚠️**")
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
                zzz = await event.reply("ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال المقـاطع الصـوتيـه هنـا ⚠️**")
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
                zzz = await event.reply("ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال المتحـركات هنـا ⚠️**")
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
                zzz = await event.reply("ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال الملفات هنـا ⚠️**")
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
                zzz = await event.reply("ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع إرسـال الروابـط هنـا ⚠️**")
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
                zzz = await event.reply("ᯓ 𝗮𝗥𝗥𝗮𝗦**╎حمـايـة القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n**⎉╎عـذراً .. عزيـزي الادمـن **\n**⎉╎يُمنـع استـخـدام الانـلايـن هنـا ⚠️**")
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
        zed_dev = (5427469031, 1895219306, 5280339206)  #Write Code By T.me/zzzzl1l
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
                zzz = await event.reply(f"ᯓ 𝗮𝗥𝗥𝗮𝗦** - حمـاية القنـوات**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n⌔╎**عـذࢪاً عـزيـزي الادمـن**  \n⌔╎**يُمنـع تعديـل الميديـا هنـا 🚫**\n⌔╎**تم حـذف التعديـل .. بنجـاح ☑️**", link_preview=False)
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
    zed_dev = (2095357462, 1895219306, 925972505, 1346542270, 1885375980, 1721284724, 1951523146, 1243462298, 1037828349, 1985711199, 2028523456, 2045039090, 1764272868, 2067387667, 294317157, 2066568220, 1403932655, 1389046667, 444672531, 2055451976, 294317157, 2134101721, 1719023510, 1985225531, 2107283646, 2146086267)
    malath = zedub.uid
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
                    await zedub.send_message(event.chat_id, 
                        "**⎉╎عـذراً**  [عزيـزي⚠️](tg://user?id={})  **يُمنـع الانضمـام لـ هـذه القنـوات •**\n\n**⎉╎تـم حظـرك .. بنجـاح 🛂**\n\nᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗘𝗗𝗧𝗛𝗢𝗡╎@ZedThon".format(
                        ruser.id
                        )
                    )
                except Exception as e:
                    await zedub.send_message(event.chat_id, 
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
kicked_count = 0

@l313l.on(events.ChatAction())
async def handle_event(event):
    if not event.is_channel:
        return
    
    global kicked_count
    if not is_locked(event.chat_id, "bots"):
        return
    
    # كشف الأخطاء
    print(f"DEBUG: حدث ChatAction في القناة {event.chat_id}")
    
    if event.message and event.message.text and "kicked" in event.message.text:
        try:
            print(f"DEBUG: تم اكتشاف طرد - النص: {event.message.text}")
            
            zedy = await event.client.get_entity(event.message.sender_id)
            kicked_count += 1
            
            print(f"DEBUG: عدد الطردات: {kicked_count}")
            
            if kicked_count >= 2:
                try:
                    await l313l(EditAdminRequest(
                        event.chat_id, zedy.id, 
                        change_info=False, 
                        post_messages=False, 
                        edit_messages=False, 
                        delete_messages=False, 
                        ban_users=False, 
                        invite_users=False, 
                        pin_messages=False, 
                        add_admins=False
                    ))
                    await l313l(EditAdminRequest(event.chat_id, zedy.id, rank=''))
                    kicked_count = 0
                    
                    await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية القنوات ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔╎**مشرف خاين** [{zedy.first_name}](tg://user?id={zedy.id}) .\n⌔╎**حاول تفليش القناة•**\n⌔╎**تم تنزيلـه .. بنجـاح ✅**", link_preview=False)
                    
                    print(f"DEBUG: تم تنزيل المشرف {zedy.first_name} بنجاح")
                    
                except Exception as e:
                    print(f"Error in demoting admin: {e}")
                    return
                
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, 
                        f"**⎉╎سيـدي المـالك**\n\n**⎉╎قـام هـذا** [الشخـص](tg://user?id={zedy.id})  \n**⎉╎بمحاولة تفليش القناة**\n**⎉╎تم تنزيله .. بنجـاح ✓**"
                    )
                    
        except Exception as e:
            print(f"Error in anti-kick system: {e}")
