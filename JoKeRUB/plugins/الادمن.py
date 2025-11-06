from asyncio import sleep

from telethon import functions
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
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)
from telethon.extensions import markdown, html
from telethon.tl import types
from telethon.tl.types import MessageEntityCustomEmoji, MessageEntityTextUrl
from JoKeRUB import l313l

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID

# =================== STRINGS ============
PP_TOO_SMOL = "**᯽︙ الصورة صغيرة جدًا** "
PP_ERROR = "**᯽︙ فشل أثناء معالجة الصورة** "
NO_ADMIN = "**᯽︙ أنا لست مشرف هنا!!** "
NO_PERM = "**᯽︙ ليس لدي أذونات كافية!** "
CHAT_PP_CHANGED = "**᯽︙ تم تغيير صورة الدردشة بنجاح ✅**"
INVALID_MEDIA = "**᯽︙ ملحق غير صالح** "
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
#admin plugin for  l313l
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

plugin_category = "aadmin" 
# ================================================
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



@l313l.ar_cmd(
    pattern="الصورة( -وضع| -حذف)$",
    command=("الصورة", plugin_category),
    info={
        "᯽︙ الأسـتخدام": "For changing group display pic or deleting display pic",
        "᯽︙ الشـرح": "Reply to Image for changing display picture",
        "flags": {
            "-s": "To set group pic",
            "-d": "To delete group pic",
        },
        "᯽︙ الأمـر": [
            "{tr}الصورة -وضع <reply to image>",
            "{tr}gpic -حذف",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def set_group_photo(event):  # sourcery no-metrics
    "For changing Group dp"
    flag = (event.pattern_match.group(1)).strip()
    if flag == "-s":
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
                return await edit_delete(event, f"**خـطأ : **`{str(e)}`")
            process = "updated"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edit_delete(event, f"**خـطأ : **`{str(e)}`")
        process = "deleted"
        await edit_delete(event, "**᯽︙ تـم حذف الـصورة بنـجاح ✅")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#صوره_المجموعة\n"
            f"صورة المجموعه {process} بنجاح "
            f"الدردشه: {event.chat.title}(`{event.chat_id}`)",
        )


@l313l.ar_cmd(
    pattern="رفع مشرف(?:\s|$)([\s\S]*)",
    command=("رفع مشرف", plugin_category),
    info={
        "الامر": "᯽︙ لرفع الشخص مشرف مع صلاحيات",
        "الشرح": "᯽︙ لرفع الشخص مشرف بالمجموعه قم بالرد على الشخص\
            \n᯽︙ تـحتاج الصلاحـيات لـهذا الأمـر",
        "الاستخدام": [
            "{tr}رفع مشرف <ايدي/معرف/بالرد عليه>",
            "{tr}رفع مشرف <ايدي/معرف/بالرد عليه> ",
        ],
    },
    groups_only=True,
    require_admin=True,
)#admin plugin for  l313l
async def promote(event):
    "᯽︙ لـرفع مستـخدم مشـرف في الـكروب"
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=False,
        delete_messages=True,
        pin_messages=True,
        manage_call=True,  # إضافة صلاحية بدء المكالمات
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "-"
    if not user:
        return
    catevent = await edit_or_reply(event, "**يـتم الرفـع**")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    await catevent.edit("**تم رفعه مشرف بالمجموعه بنجاح ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#الـرفـع\
            \nالـمستخـدم: [{user.first_name}](tg://user?id={user.id})\
            \nالـدردشـة: {event.chat.title} (`{event.chat_id}`)",
        )
@l313l.ar_cmd(
    pattern="(تنزيل الكل|تك)(?:\s|$)([\s\S]*)",  # يتطابق مع "تنزيل الكل" أو "تك"
    command=("تنزيل الكل", plugin_category),
    info={
        "الامر": "᯽︙ لتنزيل الشخص من الاشراف",
        "الشرح": "᯽︙ يقوم هذا الامر بحذف جميع صلاحيات المشرف\
            \n᯽︙ ملاحظه :**لازم تكون انت الشخص الي رفعه او تكون مالك المجموعه حتى تنزله**",
        "الاستخدام": [
            "{tr}تنزيل الكل <الايدي/المعرف/بالرد عليه>",
            "{tr}تك <الايدي/المعرف/بالرد عليه>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def demote(event):
    "᯽︙ لـتنزيـل شـخص من الأشـراف"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "**᯽︙ يـتم التنزيل من الاشراف**")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
        manage_call=None,
    )
    rank = "-"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    await catevent.edit("**᯽︙ تـم تنزيله من قائمه الادمنيه بنجاح ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#تنزيل_مشرف\
            \nالمعرف: [{user.first_name}](tg://user?id={user.id})\
            \nالدردشه: {event.chat.title}(`{event.chat_id}`)",
        )
@l313l.ar_cmd(
    pattern="طرد(?:\s|$)([\s\S]*)",
    command=("طرد", plugin_category),
    info={
        "header": "لـطرد شـخض من الـكروب",
        "description": "لـطرد شخص من المـجموعة يستطيع الأنضـمام مرة اخـرى.\nتـحتاج الصلاحـيات لـهذا الأمـر.",
        "usage": [
            "{tr}طرد <الايدي/المعرف/بالرد عليه>",
            "{tr}طرد <الايدي/المعرف/بالرد عليه> <السبب> ",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def endmute(event):
    "لـطرد شـخض من الـكروب"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == 5427469031:
        return await edit_delete(event, "**- لا يمڪنني حظر مطـوري دي لك**")
    catevent = await edit_or_reply(event, "**✾╎ يـتم طـرد الـمستخدم أنتـظر**")
    try:
        await event.client.kick_participant(event.chat_id, user.id)
    except Exception as e:
        return await catevent.edit(NO_PERM + f"\n{str(e)}")
    if reason:
        await catevent.edit(
            f"<b>✾╎ المسـتخدم</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n<b>✾╎ تـم طرده بنجاح</b> <a href='emoji/5348135243104664976'>❤️</a>\n<b>✾╎ السـبب :</b> <code>{reason}</code>",
            parse_mode=CustomParseMode("html")
        )
    else:
        await catevent.edit(
            f"<b>✾╎ المسـتخدم</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n<b>✾╎ تـم طرده بنجاح</b> <a href='emoji/5348135243104664976'>❤️</a>",
            parse_mode=CustomParseMode("html")
        )

@l313l.ar_cmd(
    pattern="حظر(?:\s|$)([\s\S]*)",
    command=("حظر", plugin_category),
    info={
        "header": "يقـوم بـحظر شخـص في الـكروب الذي تـم اسـتخدام الأمر فيـه.",
        "description": "لحـظر شخـص من الكـروب ومـنعه من الأنـضمام مجـددا. تـحتاج الصلاحـيات لـهذا الأمـر.",
        "usage": [
            "{tr}حظر <الايدي/المعرف/بالرد عليه>",
            "{tr}حظر <الايدي/المعرف/بالرد عليه> <السبب>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def jokerban(event):
    "لحـظر شخص في كـروب مـعين"
    await event.delete()
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == 5427469031:
        return await edit_delete(event, "**- لا يمڪنني حظر مطـوري دي لك**")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await edit_or_reply(event, NO_PERM)
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await edit_or_reply(event, "**✾╎ليـس لـدي جـميع الصـلاحيـات لكـن سيـبقى محـظور**")
    
    if reason:
        await event.client.send_message(
            event.chat_id,
            f"<b>✾╎ المسـتخدم</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n<b>✾╎ تـم حـظره بنـجاح</b> <a href='emoji/5348135243104664976'>✅</a>\n<b>✾╎السبب :</b> <code>{reason}</code>",
            parse_mode=CustomParseMode("html")
        )
    else:
        await event.client.send_message(
            event.chat_id,
            f"<b>✾╎ المسـتخدم</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n<b>✾╎ تـم حـظره بنـجاح</b> <a href='emoji/5348135243104664976'>✅</a>",
            parse_mode=CustomParseMode("html")
        )
    
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"** #الحـظر**\n"
                f"**✾╎ المسـتخدم:** [{user.first_name}](tg://user?id={user.id})\n"
                f"**✾╎ الـدردشـة:** {event.chat.title}\n"
                f"**✾╎ ايدي الكروب:** `{event.chat_id}`\n"
                f"**✾╎ السبـب:** {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"** #الحـظر**\n"
                f"**✾╎ المسـتخدم:** [{user.first_name}](tg://user?id={user.id})\n"
                f"**✾╎ الـدردشـة:** {event.chat.title}\n"
                f"**✾╎ ايـدي الكـروب:** `{event.chat_id}`",
            )

@l313l.ar_cmd(
    pattern="الغاء حظر(?:\s|$)([\s\S]*)",
    command=("الغاء حظر", plugin_category),
    info={
        "header": "يقـوم بـالغاء حـظر الشـخص في الـكروب الذي اسـتخدمت فيـه الامر.",
        "description": "لألـغاء حـظر شخـص من الكـروب والسـماح له من الأنـضمام مجـددا\nتـحتاج الصلاحـيات لـهذا الأمـر.",
        "usage": [
            "{tr}الغاء حظر <الايدي/المعرف/بالرد عليه>",
            "{tr}الغاء حظر <الايدي/المعرف/بالرد عليه> <السبب> ",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def nothanos(event):
    "لألـغاء الـحظر لـشخص في كـروب مـعين"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "**✾╎ جـار الـغاء الـحظر أنتـظر رجـاءا**")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await catevent.edit(
            f"<b>✾╎ المسـتخدم</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n<b>✾╎ تـم الـغاء حـظره بنـجاح</b> <a href='emoji/5348135243104664976'>❤️</a>",
            parse_mode=CustomParseMode("html")
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"** #الـغاء_الـحظر**\n"
                f"**✾╎ المسـتخدم:** [{user.first_name}](tg://user?id={user.id})\n"
                f"**✾╎ الـدردشـة:** {event.chat.title}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await catevent.edit("**✾╎ يـبدو أن هذه الـعمليـة تم إلغاؤهـا**")
    except Exception as e:
        await catevent.edit(f"**✾╎ خـطأ :**\n`{e}`")

@l313l.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


from asyncio import sleep
import requests
import os
from telethon import events
from telethon.tl.functions.messages import SetChatWallPaperRequest
from telethon.tl.types import InputWallPaperUploaded, WallPaperSettings
from telethon.tl.functions.account import UploadWallPaperRequest

@l313l.ar_cmd(
    pattern="خلفية$"
)
async def test_wallpaper(event):
    # رد فوري للتأكد أن الأمر يعمل
    await event.reply("**᯽︙ الأمر يعمل! جاري المعالجة...**")
    
    try:
        # التأكد من محادثة خاصة
        if not event.is_private:
            await event.reply("**᯽︙ هذا الأمر للمحادثات الخاصة فقط**")
            return
        
        # إرسال الصورة مباشرة
        await event.reply("**᯽︙ جاري إرسال الخلفية...**")
        
        await event.client.send_file(
            event.chat_id,
            "https://graph.org/file/bc958f1d9cbede9fdba3c-ef281c7c94420807e6.jpg",
            caption="**᯽︙ هذه هي الخلفية المطلوبة**"
        )
        
    except Exception as e:
        await event.reply(f"**᯽︙ حدث خطأ: {str(e)}**")


@l313l.ar_cmd(
    pattern="تست$"
)
async def test_command(event):
    await event.reply("**✅ الأمر يعمل! البوت يستجيب.**")
