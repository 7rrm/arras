import asyncio
import contextlib
import re
import html
import shutil
import os
import base64
import requests
from requests import get

from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import MessageEntityMentionName, EmojiStatusEmpty
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import pack_bot_file_id
from telethon.errors.rpcerrorlist import YouBlockedUserError, ChatSendMediaForbiddenError
from telethon import events, types
from telethon.extensions import markdown, html
#from .xtelethonimport CustomParseMode  # TODO: Call the class from custom module
from . import l313l
from ..Config import Config
from ..utils import Zed_Vip, Zed_Dev
from ..helpers import reply_id
from ..helpers.utils import _format
from ..core.logger import logging
from ..core.managers import edit_or_reply, edit_delete
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.echo_sql import addecho, get_all_echos, get_echos, is_echo, remove_all_echos, remove_echo, remove_echos
from . import BOTLOG, BOTLOG_CHATID, spamwatch

plugin_category = "utils"
LOGS = logging.getLogger(__name__)

zed_dev = (5176749470, 5427469031, 925972505, 5280339206, 5426390871, 6269975462, 1985225531)
zel_dev = (5176749470, 5427469031, 6269975462, 1985225531)
zelzal = (925972505, 5427469031, 5280339206)
Zel_Uid = l313l.uid
#zedub.parse_mode = CustomParseMode('markdown')  # TODO: Choose parsemode

ZED_BLACKLIST = [
    -1001935599871,
    ]


class InvalidFormatException(Exception):
    pass


class CustomParseMode:
    """
    Example using Markdown:

    - client.send_message('me', 'hello this is a [Text](spoiler), with custom emoji [❤️](emoji/10002345) !')

    Example using HTML:

    - client.send_message('me', 'hello this is a <a href="spoiler">Text</a>, with custom emoji <a href="emoji/10002345">❤️</a> !')

    `Sending spoilers and custom emoji <https://github.com/LonamiWebs/Telethon/wiki/Sending-more-than-just-messages#sending-spoilers-and-custom-emoji>`_
    :param parse_mode: The format to use for parsing text.
                       Can be either 'markdown' for Markdown formatting
                       or 'html' for HTML formatting.
    """
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'markdown':
            text, entities = markdown.parse(text)
        elif self.parse_mode == 'html':
            text, entities = html.parse(text)
        else:
            raise InvalidFormatException("Invalid parse mode. Choose either Markdown or HTML.")

        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith('emoji/'):
                    entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, int(e.url.split('/')[1]))
        return text, entities

    @staticmethod
    def unparse(text, entities):
        for i, e in enumerate(entities or []):
            if isinstance(e, types.MessageEntityCustomEmoji):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, f'emoji/{e.document_id}')
            if isinstance(e, types.MessageEntitySpoiler):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, 'spoiler')
        return html.unparse(text, entities)


async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        if isinstance(user, int) or user.startswith("@"):
            user_obj = await event.client.get_entity(user)
            return user_obj
        try:
            user_object = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_object

async def fetch_zelzal(user_id):
    """إرجاع تاريخ ثابت 2022 بدلاً من الاتصال بالخدمة الخارجية"""
    return "2022"  # تاريخ ثابت بدلاً من التاريخ الحقيقي


async def zzz_info(zthon_user, event):
    FullUser = (await event.client(GetFullUserRequest(zthon_user.id))).full_user
    first_name = zthon_user.first_name
    full_name = FullUser.private_forward_name
    user_id = zthon_user.id
    zelzal_sinc = "2022"  # استخدام التاريخ الثابت مباشرة
    username = zthon_user.username
    verified = zthon_user.verified
    zilzal = (await event.client.get_entity(user_id)).premium
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("هذا المستخدم ليس له اسم أول")
    )
    full_name = full_name or first_name
    username = "@{}".format(username) if username else ("لا يـوجـد")
    zzzsinc = zelzal_sinc  # لن نتحقق من وجود قيمة لأنها ثابتة
    
    ZThon = f'<a href="T.me/ZThon">ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗗𝗮𝘁𝗮 📟</a>'
    ZThon += f"\n<b>⋆─┄─┄─┄─┄─┄─┄─⋆</b>\n\n"
    ZThon += f"<b>• معلومـات إنشـاء حسـاب تيليجـرام 📑 :</b>\n"
    ZThon += f"<b>- الاسـم    ⤎ </b> "
    ZThon += f'<a href="tg://user?id={user_id}">{full_name}</a>'
    ZThon += f"\n<b>- الايــدي   ⤎ </b> <code>{user_id}</code>"
    ZThon += f"\n<b>- اليـوزر    ⤎  {username}</b>\n"
    if zilzal == True or user_id in zelzal: 
        ZThon += f"<b>- الحساب  ⤎  بـريميـوم</b> "
        ZThon += f'<a href="emoji/5834880210268329130">❤️</a> \n'
    ZThon += f"<b>- الإنشـاء   ⤎</b>  {zzzsinc}  🗓" 
    return ZThon


async def fetch_info(replied_user, event):
    """وظيفة لجمع المعلومات مع استخدام التاريخ الثابت"""
    FullUser = (await event.client(GetFullUserRequest(replied_user.id))).full_user
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(user_id=replied_user.id, offset=42, max_id=0, limit=80)
    )
    replied_user_profile_photos_count = "لا يـوجـد بروفـايـل"
    dc_id = "Can't get dc id"
    with contextlib.suppress(AttributeError):
        replied_user_profile_photos_count = replied_user_profile_photos.count
        dc_id = replied_user.photo.dc_id
    
    user_id = replied_user.id
    zelzal_sinc = "2022"  # التاريخ الثابت هنا أيضاً
    first_name = replied_user.first_name
    last_name = replied_user.last_name
    full_name = f"{first_name} {last_name}" if last_name else first_name
    common_chat = FullUser.common_chats_count
    username = replied_user.username
    user_bio = FullUser.about
    is_bot = replied_user.bot
    restricted = replied_user.restricted
    verified = replied_user.verified
    zilzal = (await event.client.get_entity(user_id)).premium
    mypremium = (await event.client.get_entity(Zel_Uid)).premium
    #zid = int(gvarstatus("ZThon_Vip"))
    if zilzal == True or user_id in zelzal:
        zpre = "ℙℝ𝔼𝕄𝕀𝕌𝕄 🌟"
    else:
        zpre = "𝕍𝕀ℝ𝕋𝕌𝔸𝕃 ✨"
    if user_id in Zed_Dev:
        zvip = "𝕍𝕀ℙ 💎"
    elif gvarstatus("ZThon_Vip") and user_id == int(gvarstatus("ZThon_Vip")):
        zvip = "𝕍𝕀ℙ 💎"
    else:
        zvip = "ℕ𝕆ℕ𝔼"
    if (zilzal == True and mypremium == True):
        emoji_status = (await event.client.get_entity(user_id)).emoji_status
        if isinstance(emoji_status, EmojiStatusEmpty): 
            emoji_id = 5834880210268329130
        else:
            try:
                emoji_id = emoji_status.document_id
                if emoji_id is None:
                    emoji_id = 5834880210268329130
            except Exception:
                    emoji_id = 5834880210268329130
    photo = await event.client.download_profile_photo(
        user_id,
        Config.TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg",
        download_big=True,
    )
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("هذا المستخدم ليس له اسم أول")
    )
    #full_name = full_name or first_name
    username = "@{}".format(username) if username else ("لا يـوجـد")
    user_bio = "لا يـوجـد" if not user_bio else user_bio
    zzzsinc = zelzal_sinc if zelzal_sinc else ("غيـر معلـوم")
    zmsg = await bot.get_messages(event.chat_id, 0, from_user=user_id) 
    zzz = zmsg.total
    if zzz < 100: 
        zelzzz = "غير متفاعل  🗿"
    elif zzz > 200 and zzz < 500:
        zelzzz = "ضعيف  🗿"
    elif zzz > 500 and zzz < 700:
        zelzzz = "شد حيلك  🏇"
    elif zzz > 700 and zzz < 1000:
        zelzzz = "ماشي الحال  🏄🏻‍♂"
    elif zzz > 1000 and zzz < 2000:
        zelzzz = "ملك التفاعل  🎖"
    elif zzz > 2000 and zzz < 3000:
        zelzzz = "امبراطور التفاعل  🥇"
    elif zzz > 3000 and zzz < 4000:
        zelzzz = "غنبله  💣"
    else:
        zelzzz = "نار وشرر  🏆"
################# Dev ZilZal #################
    if user_id in zelzal: 
        rotbat = "مطـور السـورس 𓄂" 
    elif user_id in zel_dev:
        rotbat = "مـطـور 𐏕" 
    elif user_id == (await event.client.get_me()).id:
        rotbat = "مـالك الحساب 𓀫" 
    else:
        rotbat = "العضـو 𓅫"
################# Dev ZilZal #################
    #zid = int(gvarstatus("ZThon_Vip"))
    ZED_TEXT = gvarstatus("CUSTOM_ALIVE_TEXT") or "•⎚• مـعلومـات المسـتخـدم مـن بـوت زدثــون"  
    ZEDM = gvarstatus("CUSTOM_ALIVE_EMOJI") or "✦ " 
    ZEDF = gvarstatus("CUSTOM_ALIVE_FONT") or "⋆─┄─┄─┄─ ᶻᵗʰᵒᶰ ─┄─┄─┄─⋆" 
    if gvarstatus("ZID_TEMPLATE") is None:
        if Zel_Uid in Zed_Dev or (gvarstatus("ZThon_Vip") and Zel_Uid == int(gvarstatus("ZThon_Vip"))):
            if mypremium == True:
                caption = f"<b>✦ مـعلومـات المسـتخـدم سـورس آراس </b>"
                caption += f'<a href="emoji/4909197170365695119">❤️</a>\n'
                caption += f'<a href="emoji/6323136954380585694">❤️</a>'
                caption += f'<a href="emoji/6325684673145997914">❤️</a>'
                caption += f'<a href="emoji/6323205570778107774">❤️</a>'
                caption += f'<a href="emoji/6323518746908428943">❤️</a>'
                caption += f'<a href="emoji/5834774412338927340">❤️</a>'
                caption += f'<a href="emoji/6325480992911919689">❤️</a>'
                caption += f'<a href="emoji/6323564170482551899">❤️</a>'
                caption += f'<a href="emoji/6323191058083613275">❤️</a>'
                caption += f'<a href="emoji/6325310787652946500">❤️</a>\n'
                caption += f"<b>{ZEDM}الاســم    ⤎ </b> "
                caption += f'<a href="tg://user?id={user_id}">{full_name}</a> '
                if zilzal == True:
                    caption += f'<a href="emoji/{emoji_id}">❤️</a>'
                caption += f"\n<b>{ZEDM}اليـوزر    ⤎  {username}</b>"
                caption += f"\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
                caption += f"<b>{ZEDM}الرتبــه    ⤎ {rotbat} </b>\n"
                if zilzal == True:
                    caption += f"<b>{ZEDM}الحساب  ⤎  بـريميـوم</b>"
                    caption += f'<a href="emoji/5832422209074762334">❤️</a>\n'
                if user_id in Zed_Dev or (gvarstatus("ZThon_Vip") and user_id == int(gvarstatus("ZThon_Vip"))):
                    if zilzal == True or user_id in zelzal:
                        caption += f"<b>{ZEDM}الاشتراك ⤎ </b>"
                        caption += f'<a href="emoji/5832653669157310552">❤️</a> \n'
                caption += f"<b>{ZEDM}الصـور    ⤎</b>  {replied_user_profile_photos_count}\n"
                caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz} "
                caption += f'<a href="emoji/5253742260054409879">❤️</a>\n'
                caption += f"<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n" 
                if user_id != (await event.client.get_me()).id: 
                    caption += f"<b>{ZEDM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
                caption += f"<b>{ZEDM}الإنشـاء  ⤎</b>  {zzzsinc}  🗓\n" 
                caption += f"<b>{ZEDM}البايـو     ⤎  {user_bio}</b>\n"
                caption += f'<a href="emoji/6323136954380585694">❤️</a>'
                caption += f'<a href="emoji/6325684673145997914">❤️</a>'
                caption += f'<a href="emoji/6323205570778107774">❤️</a>'
                caption += f'<a href="emoji/6323518746908428943">❤️</a>'
                caption += f'<a href="emoji/5834774412338927340">❤️</a>'
                caption += f'<a href="emoji/6325480992911919689">❤️</a>'
                caption += f'<a href="emoji/6323564170482551899">❤️</a>'
                caption += f'<a href="emoji/6323191058083613275">❤️</a>'
                caption += f'<a href="emoji/6325310787652946500">❤️</a>\n'
            else:
                caption = f"<b> {ZED_TEXT} </b>\n"
                caption += f"ٴ<b>{ZEDF}</b>\n"
                caption += f"<b>{ZEDM}الاســم    ⤎ </b> "
                caption += f'<a href="tg://user?id={user_id}">{full_name}</a>'
                caption += f"\n<b>{ZEDM}اليـوزر    ⤎  {username}</b>"
                caption += f"\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
                caption += f"<b>{ZEDM}الرتبــه    ⤎ {rotbat} </b>\n"
                if zilzal == True:
                    caption += f"<b>{ZEDM}الحساب  ⤎  بـريميـوم 🌟</b>\n"
                if user_id in Zed_Dev or (gvarstatus("ZThon_Vip") and user_id == int(gvarstatus("ZThon_Vip"))):
                    if zilzal == True or user_id in zelzal:
                        caption += f"<b>{ZEDM}الاشتراك  ⤎  𝕍𝕀ℙ</b>\n"
                caption += f"<b>{ZEDM}الصـور    ⤎</b>  {replied_user_profile_photos_count}\n"
                caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz}  💌\n"
                caption += f"<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n" 
                if user_id != (await event.client.get_me()).id: 
                    caption += f"<b>{ZEDM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
                caption += f"<b>{ZEDM}الإنشـاء  ⤎</b>  {zzzsinc}  🗓\n" 
                caption += f"<b>{ZEDM}البايـو     ⤎  {user_bio}</b>\n"
                caption += f"ٴ<b>{ZEDF}</b>"
        else:
            caption = f"<b> {ZED_TEXT} </b>\n"
            caption += f"ٴ<b>{ZEDF}</b>\n"
            caption += f"<b>{ZEDM}الاســم    ⤎ </b> "
            caption += f'<a href="tg://user?id={user_id}">{full_name}</a>'
            caption += f"\n<b>{ZEDM}اليـوزر    ⤎  {username}</b>"
            caption += f"\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
            caption += f"<b>{ZEDM}الرتبــه    ⤎ {rotbat} </b>\n"
            if zilzal == True:
                caption += f"<b>{ZEDM}الحساب  ⤎  بـريميـوم 🌟</b>\n"
            if user_id in Zed_Dev or (gvarstatus("ZThon_Vip") and user_id == int(gvarstatus("ZThon_Vip"))):
                if zilzal == True or user_id in zelzal:
                    caption += f"<b>{ZEDM}الاشتراك  ⤎  𝕍𝕀ℙ</b>\n"
            caption += f"<b>{ZEDM}الصـور    ⤎</b>  {replied_user_profile_photos_count}\n"
            caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz}  💌\n"
            caption += f"<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n" 
            if user_id != (await event.client.get_me()).id: 
                caption += f"<b>{ZEDM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
            caption += f"<b>{ZEDM}الإنشـاء  ⤎</b>  {zzzsinc}  🗓\n" 
            caption += f"<b>{ZEDM}البايـو     ⤎  {user_bio}</b>\n"
            caption += f"ٴ<b>{ZEDF}</b>"
    else:
        zzz_caption = gvarstatus("ZID_TEMPLATE")
        caption = zzz_caption.format(
            znam=full_name,
            zusr=username,
            zidd=user_id,
            zrtb=rotbat,
            zpre=zpre,
            zvip=zvip,
            zpic=replied_user_profile_photos_count,
            zmsg=zzz,
            ztmg=zelzzz,
            zcom=common_chat,
            zsnc=zzzsinc,
            zbio=user_bio,
        )
    return photo, caption

@l313l.ar_cmd(
    pattern="ا(?: |$)(.*)",
    command=("ا", plugin_category),
    info={
        "header": "امـر مختصـر لـ عـرض معلومـات الشخـص",
        "الاستـخـدام": " {tr}ا بالـرد او {tr}ا + معـرف/ايـدي الشخص",
    },
)
async def who(event):
    "Gets info of an user"
    #if gvarstatus("ZThon_Vip") is not None or Zel_Uid in Zed_Dev:
        #input_str = event.pattern_match.group(1)
        #reply = event.reply_to_msg_id
        #if not input_str and not reply:
            #return
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in Zed_Dev):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر 🚫\n- فـي مجموعـة استفسـارات زدثــون ؟!**")
    zed = await edit_or_reply(event, "⇆")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    replied_user = await get_user_from_event(event)
    try:
        photo, caption = await fetch_info(replied_user, event)
    except (AttributeError, TypeError):
        return await edit_or_reply(zed, "**- لـم استطـع العثــور ع الشخــص ؟!**")
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if gvarstatus("ZID_TEMPLATE") is None:
        try:
            await event.client.send_file(
                event.chat_id,
                photo,
                caption=caption,
                link_preview=False,
                force_document=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("html"),
            )
            if not photo.startswith("http"):
                os.remove(photo)
            await zed.delete()
        except (TypeError, ChatSendMediaForbiddenError):
            await zed.edit(caption, parse_mode=CustomParseMode("html"))
    else:
        try:
            await event.client.send_file(
                event.chat_id,
                photo,
                caption=caption,
                link_preview=False,
                force_document=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("markdown"),
            )
            if not photo.startswith("http"):
                os.remove(photo)
            await zed.delete()
        except (TypeError, ChatSendMediaForbiddenError):
            await zed.edit(caption, parse_mode=CustomParseMode("markdown"))



@l313l.ar_cmd(pattern="الانشاء2(?: |$)(.*)")
async def zelzalll(event):
    zed = await edit_or_reply(event, "**- جـارِ جلب المعلومـات . . .**")
    zthon_user = await get_user_from_event(event)
    try:
        ZThon = await zzz_info(zthon_user, event)
    except (AttributeError, TypeError):
        return await edit_or_reply(zed, "**- لـم استطـع العثــور ع الشخــص ؟!**")
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    #zedub.parse_mode = CustomParseMode('html')  # TODO: Choose parsemode
    try:
        await event.client.send_message(
            event.chat_id,
            ZThon,
            link_preview=False,
            reply_to=message_id_to_reply,
            parse_mode="html",
        )
        await zed.delete()
    except:
        await zed.edit("**- غيـر معلـوم او هنـاك خطـأ ؟!**", parse_mode="html")


@l313l.ar_cmd(
    pattern="ايدي_ايموجي$",
    command=("ايدي_ايموجي", plugin_category),
    info={
        "header": "جلب ايدي الإيموجي البريميوم للمستخدم",
        "الاستخدام": "{tr}ايدي_ايموجي بالرد على المستخدم",
    },
)
async def get_emoji_id(event):
    replied_user = await event.get_reply_message()
    if not replied_user:
        return await edit_delete(event, "**⚠️ يرجى الرد على المستخدم**", time=10)
    
    try:
        user = await event.client.get_entity(replied_user.sender_id)
        if user.premium and user.emoji_status:
            emoji_id = user.emoji_status.document_id
            await edit_or_reply(
                event,
                f"**🎟 ايدي الإيموجي البريميوم لـ [{user.first_name}](tg://user?id={user.id}):**\n"
                f"`{emoji_id}`\n"
                f"**للاستخدام:** `<emoji document_id='{emoji_id}'>🌟</emoji>`"
            )
        else:
            await edit_or_reply(event, "**❌ هذا المستخدم ليس لديه إيموجي بريميوم**")
    except Exception as e:
        await edit_or_reply(event, f"**⚠️ خطأ:** {str(e)}")


