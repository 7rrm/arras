import asyncio
import shutil
import contextlib
from datetime import datetime

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.utils import get_display_name

from . import l313l
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.echo_sql import addecho, get_all_echos, get_echos, is_echo, remove_all_echos, remove_echo, remove_echos
from ..sql_helper import gban_sql_helper as gban_sql
from ..sql_helper.mute_sql import is_muted, mute, unmute
from ..utils import Zed_Dev
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event
plugin_category = "الادمن"

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

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

zel_dev = (5176749470, 5426390871, 6269975462, 1985225531)

@l313l.ar_cmd(
    pattern="ح عام(?:\s|$)([\s\S]*)",
    command=("gban", plugin_category),
    info={
        "header": "To ban user in every group where you are admin.",
        "الـوصـف": "Will ban the person in every group where you are admin only.",
        "الاستخـدام": "{tr}gban <username/reply/userid> <reason (optional)>",
    },
)
async def zedgban(event):  # sourcery no-metrics
    "To ban user in every group where you are admin."
    zede = await edit_or_reply(event, "**╮ ❐... جـاࢪِ حـظـࢪ الشخـص عـام**")
    start = datetime.now()
    user, reason = await get_user_from_event(event, zede)
    if not user:
        return
    if user.id == event.client.uid:
        return await edit_delete(zede, "**⎉╎عـذراً ..لا استطيـع حظـࢪ نفسـي **")
    if user.id in zel_dev:
        return await edit_delete(zede, "**⎉╎عـذراً ..لا استطيـع حظـࢪ احـد المطـورين عـام **")
    if user.id == 925972505 or user.id == 1895219306 or user.id == 2095357462:
        return await edit_delete(zede, "**⎉╎عـذراً ..لا استطيـع حظـࢪ مطـور السـورس عـام **")


    if gban_sql.is_gbanned(user.id):
        await zede.edit(
            f"**⎉╎المسـتخـدم ↠** [{user.first_name}](tg://user?id={user.id}) \n**⎉╎مـوجــود بالفعــل فـي ↠ قائمـة المحظــورين عــام**"
        )
    else:
        gban_sql.zedgban(user.id, reason)
    san = await admin_groups(event.client)
    count = 0
    sandy = len(san)
    if sandy == 0:
        return await edit_delete(zede, "**⎉╎عــذراً .. يجـب ان تكــون مشـرفـاً فـي مجموعـة واحـده ع الأقــل **")
    await zede.edit(
        f"**⎉╎جـاري بـدء حظـر ↠** [{user.first_name}](tg://user?id={user.id}) **\n\n**⎉╎مـن ↠ {len(san)} كــروب**"
    )
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            achat = await event.client.get_entity(san[i])
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**⎉╎عــذراً .. لـيس لـديــك صـلاحيـات فـي ↠**\n**⎉╎كــروب :** {get_display_name(achat)}(`{achat.id}`)",
            )
    end = datetime.now()
    zedtaken = (end - start).seconds
    if reason:
        await zede.edit(
            f"**⎉╎المستخـدم :** [{user.first_name}](tg://user?id={user.id})\n\n**⎉╎تم حـظـࢪه عـام مـن {count} كــࢪوب خـلال {zedtaken} ثـانيـه**\n**⎉╎السـبب :** {reason}"
        )
    else:
        await zede.edit(
            f"**╮ ❐... الشخـص :** [{user.first_name}](tg://user?id={user.id})\n\n**╮ ❐... تـم حـظـࢪه عـام مـن {count} كــࢪوب خـلال {zedtaken} ثـانيـه**"
        )
    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#الحظــࢪ_العـــام\
                \n**المعلـومـات :-**\
                \n**- الشخــص : **[{user.first_name}](tg://user?id={user.id})\
                \n**- الايــدي : **`{user.id}`\
                \n**- الســبب :** `{reason}`\
                \n**- تـم حظـره مـن**  {count}  **كــروب**\
                \n**- الــوقت المسـتغــࢪق :** {zedtaken} **ثــانيـه**",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#الحظــࢪ_العـــام\
                \n**المعلـومـات :-**\
                \n**- الشخــص : **[{user.first_name}](tg://user?id={user.id})\
                \n**- الايــدي : **`{user.id}`\
                \n**- تـم حظـره مـن**  {count}  **كــروب**\
                \n**- الــوقت المسـتغــࢪق :** {zedtaken} **ثــانيـه**",
            )
        with contextlib.suppress(BadRequestError):
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()


@l313l.ar_cmd(
    pattern="الغاء ح عام(?:\s|$)([\s\S]*)",
    command=("الغاء ح عام", plugin_category),
    info={
        "header": "To unban the person from every group where you are admin.",
        "الـوصـف": "will unban and also remove from your gbanned list.",
        "الاستخـدام": "{tr}ungban <username/reply/userid>",
    },
)
async def zedgban(event):
    "To unban the person from every group where you are admin."
    zede = await edit_or_reply(event, "**╮ ❐  جـاري الغــاء الحظـر العــام ❏╰**")
    start = datetime.now()
    user, reason = await get_user_from_event(event, zede)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.catungban(user.id)
    else:
        return await edit_delete(
            zede,
            f"**⎉╎المسـتخـدم ↠** [{user.first_name}](tg://user?id={user.id}) **\n\n**⎉╎ليـس مـوجــود فـي ↠ قائمـة المحظــورين عــام**",
        )
    san = await admin_groups(event.client)
    count = 0
    sandy = len(san)
    if sandy == 0:
        return await edit_delete(zede, "**⎉╎عــذراً .. يجـب ان تكــون مشـرفـاً فـي مجموعـة واحـده ع الأقــل **")
    await zede.edit(
        f"**⎉╎جـاري الغــاء حظـر ↠** [{user.first_name}](tg://user?id={user.id}) **\n\n**⎉╎مـن ↠ {len(san)} كــروب**"
    )
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            achat = await event.client.get_entity(san[i])
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**⎉╎عــذراً .. لـيس لـديــك صـلاحيـات فـي ↠**\n**⎉╎كــروب :** {get_display_name(achat)}(`{achat.id}`)",
            )
    end = datetime.now()
    zedtaken = (end - start).seconds
    if reason:
        await zede.edit(
            f"**⎉╎المستخـدم :** [{user.first_name}](tg://user?id={user.id})\n\n**⎉╎تم الغــاء حـظـࢪه عـام مـن {count} كــࢪوب خـلال {zedtaken} ثـانيـه**\n**⎉╎السـبب :** {reason}"
        )
    else:
        await zede.edit(
            f"**⎉╎المستخـدم :** [{user.first_name}](tg://user?id={user.id})\n\n**⎉╎تم الغــاء حـظـࢪه عـام مـن {count} كــࢪوب خـلال {zedtaken} ثـانيـه**"
        )

    if BOTLOG and count != 0:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#الغـــاء_الحظــࢪ_العـــام\
                \n**المعلـومـات :-**\
                \n**- الشخــص : **[{user.first_name}](tg://user?id={user.id})\
                \n**- الايــدي : **`{user.id}`\
                \n**- الســبب :** `{reason}`\
                \n**- تـم الغــاء حظـره مـن  {count} كــروب**\
                \n**- الــوقت المسـتغــࢪق :** {zedtaken} **ثــانيـه**",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#الغـــاء_الحظــࢪ_العـــام\
                \n**المعلـومـات :-**\
                \n**- الشخــص : **[{user.first_name}](tg://user?id={user.id})\
                \n**- الايــدي : **`{user.id}`\
                \n**- تـم الغــاء حظـره مـن  {count} كــروب**\
                \n**- الــوقت المسـتغــࢪق :** {zedtaken} **ثــانيـه**",
            )


@l313l.ar_cmd(
    pattern="العام$",
    command=("العام", plugin_category),
    info={
        "header": "Shows you the list of all gbanned users by you.",
        "الاستخـدام": "{tr}listgban",
    },
)
async def gablist(event):
    "Shows you the list of all gbanned users by you."
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "- قائمـة المحظـورين عــام :\n\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"**⎉╎المستخـدم :**  [{a_user.chat_id}](tg://user?id={a_user.chat_id}) \n**⎉╎سـبب الحظـر : {a_user.reason} ** \n\n"
            else:
                GBANNED_LIST += (
                    f"**⎉╎المستخـدم :**  [{a_user.chat_id}](tg://user?id={a_user.chat_id}) \n**⎉╎سـبب الحظـر : لا يـوجـد ** \n\n"
                )
    else:
        GBANNED_LIST = "**- لايــوجـد محظــورين عــام بعــد**"
    await edit_or_reply(event, GBANNED_LIST)


@l313l.ar_cmd(
    pattern="ط عام(?:\s|$)([\s\S]*)",
    command=("ط عام", plugin_category),
    info={
        "header": "kicks the person in all groups where you are admin.",
        "الاستخـدام": "{tr}gkick <username/reply/userid> <reason (optional)>",
    },
)
async def catgkick(event):  # sourcery no-metrics
    "kicks the person in all groups where you are admin"
    zede = await edit_or_reply(event, "**╮ ❐ ... جــاࢪِ طــرد الشخــص عــام ... ❏╰**")
    start = datetime.now()
    user, reason = await get_user_from_event(event, zede)
    if not user:
        return
    if user.id == event.client.uid:
        return await edit_delete(zede, "**╮ ❐ ... عــذراً لا استطــيع طــرد نفســي ... ❏╰**")
    if user.id in zel_dev:
        return await edit_delete(zede, "**╮ ❐ ... عــذࢪاً .. لا استطــيع طــرد المطـورين ... ❏╰**")
    if user.id == 925972505 or user.id == 1895219306 or user.id == 2095357462:
        return await edit_delete(zede, "**╮ ❐ ... عــذࢪاً .. لا استطــيع طــرد مطـور السـورس ... ❏╰**")
    san = await admin_groups(event.client)
    count = 0
    sandy = len(san)
    if sandy == 0:
        return await edit_delete(zede, "**⎉╎عــذراً .. يجـب ان تكــون مشـرفـاً فـي مجموعـة واحـده ع الأقــل **")
    await zede.edit(
        f"**⎉╎بـدء طـرد ↠** [{user.first_name}](tg://user?id={user.id}) **\n\n**⎉╎فـي ↠ {len(san)} كــروب**"
    )
    for i in range(sandy):
        try:
            await event.client.kick_participant(san[i], user.id)
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            achat = await event.client.get_entity(san[i])
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**⎉╎عــذراً .. لـيس لـديــك صـلاحيـات فـي ↠**\n**⎉╎كــروب :** {get_display_name(achat)}(`{achat.id}`)",
            )
    end = datetime.now()
    zedtaken = (end - start).seconds
    if reason:
        await zede.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was gkicked in {count} groups in {zedtaken} seconds`!!\n**- الســبب :** `{reason}`"
        )
    else:
        await zede.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was gkicked in {count} groups in {zedtaken} seconds`!!"
        )

    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#الطــࢪد_العـــام\
                \n**المعلـومـات :-**\
                \n**- الشخــص : **[{user.first_name}](tg://user?id={user.id})\
                \n**- الايــدي : **`{user.id}`\
                \n**- الســبب :** `{reason}`\
                \n**- تـم طــرده مـن**  {count}  **كــروب**\
                \n**- الــوقت المسـتغــࢪق :** {zedtaken} **ثــانيـه**",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#الطــࢪد_العـــام\
                \n**المعلـومـات :-**\
                \n**- الشخــص : **[{user.first_name}](tg://user?id={user.id})\
                \n**- الايــدي : **`{user.id}`\
                \n**- تـم طــرده مـن**  {count}  **كــروب**\
                \n**- الــوقت المسـتغــࢪق :** {zedtaken} **ثــانيـه**",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)

# ================================================================================================ #
# ================================================================================================ #
# ================================================================================================ #
'''
import contextlib
import shutil

from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)
from telethon.utils import get_display_name


from ..core.data import _sudousers_list
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper.mute_sql import is_muted, mute, unmute
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.echo_sql import addecho, get_all_echos, get_echos, is_echo, remove_all_echos, remove_echo, remove_echos
from . import BOTLOG, BOTLOG_CHATID

# =================== STRINGS ============
PP_TOO_SMOL = "**⪼ الصورة صغيرة جدا**"
PP_ERROR = "**⪼ فشل اثناء معالجة الصورة**"
NO_ADMIN = "**⪼ أحتـاج الى صلاحيـات المشـرف هنـا!! 𓆰**"
NO_PERM = "**⪼ ليست لدي صلاحيـات كافيـه في هـذه المجمـوعـة**"
CHAT_PP_CHANGED = "**⪼ تم تغييـر صـورة المجمـوعـة .. بنجـاح ✓**"
INVALID_MEDIA = "**⪼ ابعاد الصورة غير صالحة**"

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

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

LOGS = logging.getLogger(__name__)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
zel_dev = (5176749470, 5426390871, 6269975462, 1985225531)

plugin_category = "الادمن"

ADMZ = gvarstatus("Z_ADMIN") or "رفع مشرف"
UNADMZ = gvarstatus("Z_UNADMIN") or "تنزيل مشرف"
BANN = gvarstatus("Z_BAN") or "حظر"
UNBANN = gvarstatus("Z_UNBAN") or "الغاء حظر"
MUTE = gvarstatus("Z_MUTE") or "كتم"
UNMUTE = gvarstatus("Z_UNMUTE") or "الغاء كتم"
KICK = gvarstatus("Z_KICK") or "طرد"

PC_BANE = gvarstatus("PC_BANE")
# ================================================

@l313l.ar_cmd(
    pattern="الصورة (وضع|حذف)$",
    command=("الصورة", plugin_category),
    info={
        "header": "لـ وضـع صــوره لـ المجمـوعـه",
        "الوصــف": "بالــرد ع صــوره",
        "امـر مضـاف": {
            "وضع": "- لتغييـر صـورة المجمـوعـة",
            "حذف": "- لحـذف صـورة المجمـوعـة",
        },
        "الاسـتخـدام": [
            "{tr}الصورة وضع بالــرد ع صــوره",
            "{tr}الصورة حذف بالــرد ع صــوره",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def set_group_photo(event):  # sourcery no-metrics
    "لـ وضـع صــوره لـ المجمـوعـه"
    flag = (event.pattern_match.group(1)).strip()
    if flag == "وضع":
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await edit_delete(event, INVALID_MEDIA)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await edit_delete(event, CHAT_PP_CHANGED)
            except PhotoCropSizeSmallError:
                return await edit_delete(event, PP_TOO_SMOL)
            except ImageProcessFailedError:
                return await edit_delete(event, PP_ERROR)
            except Exception as e:
                return await edit_delete(event, f"**- خطــأ : **`{str(e)}`")
            process = "تم تغييرهـا"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edit_delete(event, f"**- خطــأ : **`{e}`")
        process = "تم حذفهـا"
        await edit_delete(event, "**- صورة الدردشـه {process} . . بنجـاح ✓**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#صـورة_المجمـوعـة\n"
            f"صورة المجموعه {process} بنجاح ✓ "
            f"الدردشة: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@l313l.ar_cmd(pattern=f"{ADMZ}(?:\s|$)([\s\S]*)")
async def promote(event):
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(event, NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=False,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "admin"
    if not user:
        return
    zzevent = await edit_or_reply(event, "**╮ ❐  جـارِ  ࢪفعـه مشـرف  . . .❏╰**")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await zzevent.edit(NO_PERM)
    await zzevent.edit(f"**⎉╎المستخـدم** [{user.first_name}](tg://user?id={user.id}) \n**⎉╎تم رفعـه مشـرفـاً .. بنجـاح✓**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#رفــع_مشــرف\
            \n**⎉╎الشخـص :** [{user.first_name}](tg://user?id={user.id})\
            \n**⎉╎المجمــوعــه :** {get_display_name(await event.get_chat())} (`{event.chat_id}`)",
        )


@l313l.ar_cmd(pattern="رفع مالك(?:\s|$)([\s\S]*)")
async def promote(event):
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(event, NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        manage_call=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "admin"
    if not user:
        return
    zzevent = await edit_or_reply(event, "**╮ ❐  جـاري ࢪفعه مشـرف بكـل الصـلاحيـات  ❏╰**")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await zzevent.edit(NO_PERM)
    await zzevent.edit(f"**⎉╎المستخـدم** [{user.first_name}](tg://user?id={user.id}) \n**⎉╎تم رفعـه مشـرفـاً بكل الصلاحيـات ✓**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#رفــع_مشــرف\
            \n**⎉╎الشخـص :** [{user.first_name}](tg://user?id={user.id})\
            \n**⎉╎المجمــوعــه :** {get_display_name(await event.get_chat())} (`{event.chat_id}`)",
        )


@l313l.ar_cmd(pattern="اخفاء(?:\s|$)([\s\S]*)")
async def promote(event):
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(event, NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        manage_call=True,
        anonymous=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "admin"
    if not user:
        return
    zzevent = await edit_or_reply(event, "**╮ ❐  ا . . .  ❏╰**")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await zzevent.edit(NO_PERM)
    await zzevent.edit("**- ❝ ⌊   تم  . . .𓆰**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#رفــع_مشــرف\
            \n**⎉╎الشخـص :** [{user.first_name}](tg://user?id={user.id})\
            \n**⎉╎المجمــوعــه :** {get_display_name(await event.get_chat())} (`{event.chat_id}`)",
        )


@l313l.ar_cmd(pattern=f"{UNADMZ}(?:\s|$)([\s\S]*)")
async def demote(event):
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(event, NO_ADMIN)
        return
    user, _ = await get_user_from_event(event)
    if not user:
        return
    zzevent = await edit_or_reply(event, "↮")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "مشرف"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await zzevent.edit(NO_PERM)
    await zzevent.edit(f"**⎉╎المستخـدم** [{user.first_name}](tg://user?id={user.id}) \n**⎉╎تم تنـزيلـه مشـرف .. بنجـاح✓**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#تنـزيــل_مشــرف\
            \n**⎉╎الشخـص : ** [{user.first_name}](tg://user?id={user.id})\
            \n**⎉╎المجمــوعــه :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@l313l.ar_cmd(pattern=f"{BANN}(?:\s|$)([\s\S]*)")
async def _ban_person(event):
    user, reason = await get_user_from_event(event)
    if reason and reason == "عام":
        return await edit_delete(event, "**⪼ لـ الحظـر العـام ارسـل** `.ح عام`")
    if not user:
        return
    if user.id == event.client.uid:
        return await edit_delete(event, "**⪼ عـذراً ..لا استطيـع حظـࢪ نفسـي 𓆰**")
    if user.id == 5427469031:
        return await edit_delete(event, "**╮ ❐ دي لا يمڪنني حظـر مطـور السـورس  ❏╰**")
    zedevent = await edit_or_reply(event, "**╮ ❐... جـاࢪِ الحـظـࢪ ...❏╰**")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await zedevent.edit(NO_PERM)
    reply = await event.get_reply_message()
    if reason:
        if gvarstatus("PC_BANE") is not None:
            await event.client.send_file(
                event.chat_id,
                gvarstatus("PC_BANE"),
                caption=f"**⎉╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}  \n**⎉╎تم حظـࢪه بنجـاح ☑️**\n\n**⎉╎السـبب :** `{reason}`",
            )
            await zedevent.delete()
        else:
            await zedevent.edit(
                f"**⎉╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}  \n**⎉╎تم حظـࢪه بنجـاح ☑️**\n\n**⎉╎السـبب :** `{reason}`",
            )
    else:
        if gvarstatus("PC_BANE") is not None:
            await event.client.send_file(
                event.chat_id,
                gvarstatus("PC_BANE"),
                caption=f"**⎉╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}  \n**⎉╎تم حظــࢪه بنجـاح ☑️**\n\n"
            )
            await zedevent.delete()
        else:
            await zedevent.edit(
                f"**⎉╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}  \n**⎉╎تم حظــࢪه بنجـاح ☑️**\n\n"
            )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#الحظــࢪ\
                \n**⎉╎المحظـور :** [{user.first_name}](tg://user?id={user.id})\
                \n**⎉╎الدردشــه :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \n**⎉╎السـبب :** {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#الحظــࢪ\
                \n**⎉╎المحظـور :** [{user.first_name}](tg://user?id={user.id})\
                \n**⎉╎الدردشــه :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )
        try:
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()
        except BadRequestError:
            return await zedevent.edit(
                "`I dont have message nuking rights! But still he is banned!`"
            )


@l313l.ar_cmd(pattern=f"{UNBANN}(?:\s|$)([\s\S]*)")
async def nothanos(event):
    user, _ = await get_user_from_event(event)
    if not user:
        return
    zedevent = await edit_or_reply(event, "**╮ ❐.. جـاري الغاء حـظࢪه ..❏╰**")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await zedevent.edit(
            f"**⎉╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}  \n**⎉╎تم الغـاء حظــࢪه .. بنجــاح✓**"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغــاء_الحظــࢪ\n"
                f"**⎉╎المستخـدم :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**⎉╎الدردشــه :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await zedevent.edit("`Uh oh my unban logic broke!`")
    except Exception as e:
        await zedevent.edit(f"**- خطــأ :**\n`{e}`")


@l313l.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


@l313l.ar_cmd(pattern=f"{KICK}(?:\s|$)([\s\S]*)")
async def kick(event):
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == 5427469031:
        return await edit_delete(event, "**╮ ❐ دي . . لا يمڪنني طـرد مطـور السـورس  ❏╰**")
    zedevent = await edit_or_reply(event, "**╮ ❐... جـاࢪِ الطــࢪد ...❏╰**")
    try:
        await event.client.kick_participant(event.chat_id, user.id)
    except Exception as e:
        return await zedevent.edit(f"{NO_PERM}\n{e}")
    if reason:
        await zedevent.edit(
            f"**⎉╎تم طــࢪد**. [{user.first_name}](tg://user?id={user.id})  **بنجــاح ✓**\n\n**⎉╎السـبب :** {reason}"
        )
    else:
        await zedevent.edit(f"**⎉╎تم طــࢪد**. [{user.first_name}](tg://user?id={user.id})  **بنجــاح ✓**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#الـطــࢪد\n"
            f"**⎉╎الشخـص**: [{user.first_name}](tg://user?id={user.id})\n"
            f"**⎉╎الدردشــه** : {get_display_name(await event.get_chat())}(`{event.chat_id}`)\n",
        )


@l313l.ar_cmd(
    pattern="تثبيت( بالاشعار|$)",
    command=("تثبيت", plugin_category),
    info={
        "header": "لـ تثبيـت الرسـائـل فـي الكــروب",
        "امـر مضـاف": {"لود": "To notify everyone without this.it will pin silently"},
        "الاسـتخـدام": [
            "{tr}تثبيت <بالــرد>",
            "{tr}تثبيت لود <بالــرد>",
        ],
    },
)
async def pin(event):
    "لـ تثبيـت الرسـائـل فـي الكــروب"
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await edit_delete(event, "**- بالــرد ع رسـالـه لـ تثبيتـهـا...**", 5)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{e}`", 5)
    await edit_delete(event, "**⎉╎تم تثبيـت الرسـالـه .. بنجــاح ✓**", 3)
    sudo_users = _sudousers_list()
    if event.sender_id in sudo_users:
        with contextlib.suppress(BadRequestError):
            await event.delete()
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#تثبيــت_رســالـه\
                \n**⎉╎تم تثبيــت رســالـه فـي المجمـوعـة**\
                \n**⎉╎الدردشــه :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \n**⎉╎الإشعـار :** {is_silent}",
        )


@l313l.ar_cmd(
    pattern="الغاء تثبيت( الكل|$)",
    command=("الغاء تثبيت", plugin_category),
    info={
        "header": "لـ الغــاء تثبيـت الرسـائـل فـي الكــروب",
        "امـر مضـاف": {"الكل": "لـ الغــاء تثبيـت كــل الرسـائـل فـي الكــروب"},
        "الاسـتخـدام": [
            "{tr}الغاء تثبيت <بالــرد>",
            "{tr}الغاء تثبيت الكل",
        ],
    },
)
async def unpin(event):
    "لـ الغــاء تثبيـت الرسـائـل فـي الكــروب"
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "الكل":
        return await edit_delete(
            event,
            "**- بالــرد ع رســالـه لـ الغــاء تثبيتـهــا او اسـتخـدم امـر .الغاء تثبيت الكل**",
            5,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "الكل":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edit_delete(
                event, "**- بالــرد ع رســالـه لـ الغــاء تثبيتـهــا او اسـتخـدم امـر .الغاء تثبيت الكل**", 5
            )
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{e}`", 5)
    await edit_delete(event, "**⎉╎تم الغـاء تثبيـت الرسـالـه/الرسـائـل .. بنجــاح ✓**", 3)
    sudo_users = _sudousers_list()
    if event.sender_id in sudo_users:
        with contextlib.suppress(BadRequestError):
            await event.delete()
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#الغــاء_تثبيــت_رســالـه\
                \n**⎉╎تم الغــاء تثبيــت رســالـه فـي الدردشــه**\
                \n**⎉╎الدردشــه** : {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@l313l.ar_cmd(
    pattern="الاحداث( م)?(?: |$)(\d*)?",
    command=("الاحداث", plugin_category),
    info={
        "header": "لـ جـلب آخـر الرسـائـل المحـذوفـه مـن الاحـداث بـ العـدد",
        "امـر مضـاف": {
            "م": "{tr}الاحداث م لجـلب رسـائل الميديـا المحذوفـة من الاحـداث"
        },
        "الاسـتخـدام": [
            "{tr}الاحداث <عدد>",
            "{tr}الاحداث م <عـدد>",
        ],
        "مثــال": [
            "{tr}الاحداث 7",
            "{tr}الاحداث م 7 لـ جـلب آخـر 7 رسـائل ميديـا من الاحـداث",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _iundlt(event):  # sourcery no-metrics
    "لـ جـلب آخـر الرسـائـل المحـذوفـه مـن الاحـداث بـ العـدد"
    zedevent = await edit_or_reply(event, "**- جـاري البحث عـن آخـر الاحداث انتظــر ...🔍**")
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        lim = min(lim, 15)
        if lim <= 0:
            lim = 1
    else:
        lim = 5
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"**- اليـك آخـر {lim} رسـائـل محذوفــه لـ هـذا الكــروب 🗑 :**"
    if not flag:
        for msg in adminlog:
            ruser = await event.client.get_entity(msg.old.from_id)
            _media_type = await media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n**🖇┊الرسـاله :** {msg.old.message} \n\n**🛂┊المرسـل** {_format.mentionuser(ruser.first_name ,ruser.id)}"
            else:
                deleted_msg += f"\n**🖇┊الميديـا :** {_media_type} \n\n**🛂┊المرسـل** {_format.mentionuser(ruser.first_name ,ruser.id)}"
        await edit_or_reply(zedevent, deleted_msg)
    else:
        main_msg = await edit_or_reply(zedevent, deleted_msg)
        for msg in adminlog:
            ruser = await event.client.get_entity(msg.old.from_id)
            _media_type = await media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"\n**🖇┊الرسـاله :** {msg.old.message} \n\n**🛂┊المرسـل** {_format.mentionuser(ruser.first_name ,ruser.id)}"
                )
            else:
                await main_msg.reply(
                    f"\n**🖇┊الرسـاله :** {msg.old.message} \n\n**🛂┊المرسـل** {_format.mentionuser(ruser.first_name ,ruser.id)}",
                    file=msg.old.media,
                )

from telethon.tl.functions.messages import SetChatWallPaperRequest
from telethon.tl.types import InputWallPaper, WallPaperSettings
from telethon import events
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

# معلومات الخلفية المحددة
WALLPAPER_ID = 5028783469501612253
WALLPAPER_HASH = 4499875478888955654

@l313l.ar_cmd(
    pattern="تفعيل الخلفية التلقائية$",
    command=("تفعيل الخلفية التلقائية", plugin_category),
    info={
        "᯽︙ الأسـتخدام": "تفعيل النظام التلقائي لتعيين الخلفية",
        "᯽︙ الشـرح": "بتفعيل هذا النظام، سيتم تعيين الخلفية تلقائياً لأي شخص يراسلك",
    },
)
async def enable_auto_wallpaper(event):
    "تفعيل النظام التلقائي لتعيين الخلفية"
    addgvar("auto_wallpaper", "true")
    await edit_delete(event, "**᯽︙ تم تفعيل النظام التلقائي لتعيين الخلفية ✓**")

@l313l.ar_cmd(
    pattern="تعطيل الخلفية التلقائية$",
    command=("تعطيل الخلفية التلقائية", plugin_category),
    info={
        "᯽︙ الأسـتخدام": "تعطيل النظام التلقائي لتعيين الخلفية",
    },
)
async def disable_auto_wallpaper(event):
    "تعطيل النظام التلقائي لتعيين الخلفية"
    delgvar("auto_wallpaper")
    await edit_delete(event, "**᯽︙ تم تعطيل النظام التلقائي لتعيين الخلفية**")

def is_user_processed(user_id):
    """التحقق إذا تم معالجة المستخدم مسبقاً"""
    processed_users = gvarstatus("wallpaper_users") or ""
    return str(user_id) in processed_users.split(",")

def add_user_to_processed(user_id):
    """إضافة مستخدم إلى القائمة"""
    processed_users = gvarstatus("wallpaper_users") or ""
    users_list = processed_users.split(",")
    if str(user_id) not in users_list:
        users_list.append(str(user_id))
        addgvar("wallpaper_users", ",".join(users_list))

@l313l.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    """معالجة الرسائل الواردة وتطبيق الخلفية تلقائياً"""
    
    # التحقق من تفعيل النظام
    if not gvarstatus("auto_wallpaper"):
        return
    
    if not event.is_private:
        return
    
    if event.message.out:
        return
    
    sender = await event.get_sender()
    if not sender or sender.bot:
        return
    
    user_id = sender.id
    chat_id = event.chat_id
    
    # التحقق إذا كان المستخدم جديد
    if not is_user_processed(user_id):
        try:
            wallpaper = InputWallPaper(
                id=WALLPAPER_ID,
                access_hash=WALLPAPER_HASH
            )
            
            await event.client(SetChatWallPaperRequest(
                peer=chat_id,
                wallpaper=wallpaper,
                for_both=True,
                settings=WallPaperSettings(
                    blur=True,
                    motion=False,
                    background_color=0x000000,
                    intensity=50
                )
            ))
            
            # إضافة المستخدم إلى القائمة
            add_user_to_processed(user_id)
            
            print(f"✅ تم تعيين الخلفية تلقائياً للمستخدم: {user_id}")
            
        except Exception as e:
            print(f"❌ خطأ في تعيين الخلفية التلقائية: {e}")

@l313l.ar_cmd(
    pattern="قائمة الخلفيات$",
    command=("قائمة الخلفيات", plugin_category),
    info={
        "᯽︙ الأسـتخدام": "عرض المستخدمين الذين تم تعيين الخلفية لهم",
    },
)
async def wallpaper_list(event):
    "عرض قائمة المستخدمين الذين تم تعيين الخلفية لهم"
    processed_users = gvarstatus("wallpaper_users") or ""
    users_count = len(processed_users.split(",")) if processed_users else 0
    
    if users_count == 0:
        await edit_delete(event, "**᯽︙ لا توجد بيانات مخزنة**")
    else:
        await edit_delete(event, f"**᯽︙ عدد المستخدمين الذين تم تعيين الخلفية لهم: {users_count}**")

@l313l.ar_cmd(
    pattern="مسح قائمة الخلفيات$",
    command=("مسح قائمة الخلفيات", plugin_category),
    info={
        "᯽︙ الأسـتخدام": "مسح جميع المستخدمين من القائمة",
    },
)
async def clear_wallpaper_list(event):
    "مسح قائمة المستخدمين"
    delgvar("wallpaper_users")
    await edit_delete(event, "**᯽︙ تم مسح قائمة المستخدمين بنجاح**")

from telethon.tl.functions.account import UploadWallPaperRequest
from telethon.tl.types import WallPaperSettings, MessageMediaPhoto
import requests
import os


@l313l.ar_cmd(
    pattern="جلب_id$",
    command=("جلب_id", plugin_category),
    info={
        "᯽︙ الأسـتخدام": "لجلب id و access_hash للصورة",
        "᯽︙ الشـرح": "الرد على صورة لجلب معلوماتها",
        "᯽︙ الأمـر": "{tr}جلب_id",
    },
)
async def get_wallpaper_info(event):
    "لجلب id و access_hash للصورة"
    replymsg = await event.get_reply_message()
    
    if not replymsg or not replymsg.media:
        return await edit_delete(event, "**᯽︙ يرجى الرد على صورة**")
    
    try:
        # تحميل الصورة
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await event.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await event.client.download_file(replymsg.media.document)
        else:
            return await edit_delete(event, "**᯽︙ يرجى الرد على صورة فقط**")
        
        # رفع الصورة كخلفية
        uploaded_file = await event.client.upload_file(photo)
        result = await event.client(UploadWallPaperRequest(
            file=uploaded_file,
            mime_type='image/jpeg',
            settings=WallPaperSettings()
        ))
        
        # إظهار النتائج
        info_text = f"""
**⌔︙ تم جلب معلومات الصورة بنجاح ✓**

**🆔 الـ ID:** `{result.id}`
**🔑 الـ Access Hash:** `{result.access_hash}`

**📝 ملاحظة:** يمكنك استخدام هذه المعلومات في الأوامر الأخرى
        """
        
        await edit_delete(event, info_text)
        
    except Exception as e:
        await edit_delete(event, f"**᯽︙ خطأ في جلب المعلومات: **`{str(e)}`")
    finally:
        # تنظيف الملف المؤقت
        if 'photo' in locals() and os.path.exists(photo):
            os.remove(photo)

'''
