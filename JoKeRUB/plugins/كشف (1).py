import os
import html
import contextlib
import requests
from datetime import datetime
from requests import get

from telethon.errors.rpcerrorlist import YouBlockedUserError, ChatSendMediaForbiddenError
from telethon.tl.types import MessageEntityMentionName, EmojiStatusEmpty
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.utils import get_input_location

from ..sql_helper.globals import gvarstatus
from JoKeRUB import l313l
from JoKeRUB.core.logger import logging
from ..utils import Zed_Vip, Zed_Dev
from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers import get_user_from_event, reply_id
from . import spamwatch

JEP_EM = Config.ID_EM or " ✦ "
ID_EDIT = gvarstatus("ID_ET") or "ايدي"

plugin_category = "utils"
LOGS = logging.getLogger(__name__)

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

async def fetch_zelzal(user_id):
    headers = {
        'Host': 'restore-access.indream.app',
        'Connection': 'keep-alive',
        'x-api-key': 'e758fb28-79be-4d1c-af6b-066633ded128',
        'Accept': '*/*',
        'Accept-Language': 'ar',
        'Content-Length': '25',
        'User-Agent': 'Nicegram/101 CFNetwork/1404.0.5 Darwin/22.3.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = '{"telegramId":' + str(user_id) + '}'
    response = requests.post('https://restore-access.indream.app/regdate', headers=headers, data=data).json()
    zelzal_date = response['data']['date']
    return zelzal_date

zed_dev = (5427469031, 1895219306, 925972505, 5280339206, 5426390871, 6269975462, 1985225531)
zel_dev = (5427469031, 5426390871, 6269975462, 1985225531)
zelzal = (5427469031, 1895219306, 5280339206)
ZIDA = gvarstatus("Z_ZZID") or "zvhhhclc"
Zel_Uid = l313l.uid

ZED_BLACKLIST = [
    -1002171868084,
]
async def fetch_info(replied_user, event):
    """Get details from the User object."""
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
    zelzal_sinc = await fetch_zelzal(user_id)
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
                caption = f"<b>✦ مـعلومـات المسـتخـدم سـورس زدثــون </b>"
                caption += f'<a href="emoji/5812307593032372545">❤️</a>\n'
                caption += f"ٴ<b>⋆┄─┄─┄─┄─</b>"
                caption += f'<a href="emoji/5809662223890518926">❤️</a>'
                caption += f"<b>─┄─┄─┄─┄⋆</b>\n"
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
                caption += f"ٴ<b>⋆┄─┄─┄─┄─</b>"
                caption += f'<a href="emoji/5809662223890518926">❤️</a>'
                caption += f"<b>─┄─┄─┄─┄⋆</b>\n"
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
    pattern="ايدي(?: |$)(.*)",
    command=("ايدي", plugin_category),
    info={
        "header": "لـ عـرض معلومـات الشخـص",
        "الاستـخـدام": " {tr}ايدي بالـرد او {tr}ايدي + معـرف/ايـدي الشخص",
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
    #except (AttributeError, TypeError):
        #return await edit_or_reply(zed, "**- لـم استطـع العثــور ع الشخــص ؟!**")
    except AttributeError as e:
        return await edit_or_reply(zed, str(e))
    except TypeError as e:
        return await edit_or_reply(zed, str(e))
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if gvarstatus("ZID_TEMPLATE") is None:
        #event.client.parse_mode = CustomParseMode('html')  # TODO: Choose parsemode
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
        #event.client.parse_mode = CustomParseMode('markdown')  # TODO: Choose parsemode
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


@l313l.ar_cmd(
    pattern="كشف(?:\s|$)([\s\S]*)",
    command=("كشف", plugin_category),
    info={
        "header": "Gets information of an user such as restrictions ban by spamwatch or cas.",
        "description": "That is like whether he banned is spamwatch or cas and small info like groups in common, dc ..etc.",
        "usage": "{tr}userinfo <username/userid/reply>",
    },
)
async def _(event):
    "Gets information of an user such as restrictions ban by spamwatch or cas"
    replied_user = await get_user_from_event(event)
    if not replied_user:
        return
    catevent = await edit_or_reply(event, "᯽︙ جار إحضار معلومات المستخدم اننظر قليلا ⚒️")
    replied_user = await event.client(GetFullUserRequest(replied_user.id))
    user_id = replied_user.users[0].id
    first_name = html.escape(replied_user.users[0].first_name)
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their
        # names
        first_name = first_name.replace("\u2060", "")
    # inspired by https://telegram.dog/afsaI181
    common_chats = 1
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception:
        dc_id = "Couldn't fetch DC ID!"
    if spamwatch:
        ban = spamwatch.get_ban(user_id)
        if ban:
            sw = f"**Spamwatch Banned :** `True` \n       **-**🤷‍♂️**Reason : **`{ban.reason}`"
        else:
            sw = f"**Spamwatch Banned :** `False`"
    else:
        sw = "**Spamwatch Banned :**`Not Connected`"
    try:
        casurl = "https://api.cas.chat/check?user_id={}".format(user_id)
        data = get(casurl).json()
    except Exception as e:
        LOGS.info(e)
        data = None
    if data:
        if data["ok"]:
            cas = "**Antispam(CAS) Banned :** `True`"
        else:
            cas = "**Antispam(CAS) Banned :** `False`"
    else:
        cas = "**Antispam(CAS) Banned :** `Couldn't Fetch`"
    caption = """**معلومات المسـتخدم [{}](tg://user?id={}):
   ⌔︙⚕️ الايدي: **`{}`
   ⌔︙👥**المجموعات المشتركه : **`{}`
   ⌔︙🌏**رقم قاعده البيانات : **`{}`
   ⌔︙🔏**هل هو حساب موثق  : **`{}`
""".format(
        first_name,
        user_id,
        user_id,
        common_chats,
        dc_id,
        replied_user.users[0].restricted,
        sw,
        cas,
    )
    await edit_or_reply(catevent, caption)

@l313l.ar_cmd(pattern="حساب(?: |$)(.*)")
async def openacc(event):
    acc = event.pattern_match.group(1)
    if not acc:
        return await edit_or_reply(event, "**- ارسـل الامـر والايـدي فقـط**")
    zzz = await edit_or_reply(event, "**⎉╎جـارِ صنـع رابـط دخـول لـ الحسـاب ▬▭ ...**")
    caption=f"**- رابـط صاحب الايدي ( {acc} )** :\n**- الرابـط ينفتـح عبـر تطبيـق تيليكرام بلاس فقـط**\n\n[اضـغـط هـنـا](tg://openmessage?user_id={acc})"
    await edit_or_reply(event, caption)
    

@l313l.ar_cmd(
    pattern="(الايدي|id)(?:\s|$)([\s\S]*)",
    command=("الايدي", plugin_category),
    info={
        "header": "To get id of the group or user.",
        "description": "if given input then shows id of that given chat/channel/user else if you reply to user then shows id of the replied user \
    along with current chat id and if not replied to user or given input then just show id of the chat where you used the command",
        "usage": "{tr}id <reply/username>",
    },
)
async def _(event):
    "To get id of the group or user."
    input_str = event.pattern_match.group(2)
    if input_str:
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{str(e)}`", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"᯽︙ ايدي المستخدم : `{input_str}` هو `{p.id}`"
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"᯽︙ ايدي الدردشة/القناة `{p.title}` هو `{p.id}`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "᯽︙ يـجب كـتابة مـعرف الشـخص او الـرد عـليه")
    elif event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                f"᯽︙ ايدي الدردشه: `{str(event.chat_id)}` \n᯽︙ ايدي المستخدم: `{str(r_msg.sender_id)}` \n᯽︙ ايدي الميديا: `{bot_api_file_id}`",
            )
        else:
            await edit_or_reply(
                event,
               f"᯽︙ ايدي الدردشه : `{str(event.chat_id)}` \n᯽︙ ايدي المستخدم: `{str(r_msg.sender_id)}` ",
            )
    else:
        await edit_or_reply(event, f"᯽︙ الـدردشـة الـحالية : `{str(event.chat_id)}`")
#by Reda For aljoker 🤡
@l313l.ar_cmd(
    pattern=r"كشف_ايدي(?: (\d+))?$",
    command=("كشف_ايدي", "utils"),
)
async def get_user_info(event):
    chat_id = event.chat_id
    user_input = event.pattern_match.group(1)
    
    if user_input:
        user_id = int(user_input)
        
        try:
            user = await l313l.get_entity(user_id)
            profile_link = f"[المُهان هنا](tg://user?id={user.id})"
            message = f"**معلومات العينتين** :\n**اسمه** : {user.first_name}\n**المعرف مالته** : `{user.username}`\n**حسابة الشخصي** : {profile_link}"
            await edit_or_reply(event, message)
        
        except Exception as e:
            await edit_or_reply(event, "**᯽︙ غير موجود ** ")
    
    else:
        await edit_or_reply(event, "**᯽︙ ضع ايدي الشخص عزيزي **")
