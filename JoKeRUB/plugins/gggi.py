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

zed_dev = (5280339206, 5427469031)
zel_dev = (5176749470, 5427469031)
zelzal = (5427469031, 5280339206)
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

async def fetch_zelzal(user_id): #Write Code By Zelzal T.me/zzzzl1l
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

from telethon.tl.functions.payments import GetSavedStarGiftsRequest
from telethon.tl.types import PeerUser
from telethon.utils import get_input_user

async def get_gifts_count(client, user_id: int) -> dict:
    """
    يحصل على عدد هدايا المستخدم
    """
    try:
        user_entity = await client.get_input_entity(PeerUser(user_id=user_id))
        
        request = GetSavedStarGiftsRequest(
            peer=get_input_user(user_entity),
            offset='',
            limit=100
        )
        
        response = await client(request)
        
        return {
            'total_count': response.count,
            'can_show_all': response.count <= 100,
        }
    except Exception:
        return {
            'total_count': 0,
            'can_show_all': False,
            'error': "لا يمكن الوصول إلى الهدايا"
        }

async def get_user_rating(client, user_id):
    try:
        full_user = await client(GetFullUserRequest(user_id))
        stars_rating = getattr(full_user.full_user, 'stars_rating', None)
        
        if stars_rating:
            level = stars_rating.level
            
            # ⚡ أقصى سرعة - شروط مباشرة
            if level == 1:
                level_display = '<a href="emoji/5217498259404130179">🎖</a>'
            elif level == 2:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 3:
                level_display = '<a href="emoji/5217707355591969547">⭐</a>'
            elif level == 4:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 5:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 6:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 7:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 8:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 9:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 10:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 11:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 12:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 13:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 14:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 15:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 16:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 17:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 18:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 19:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 20:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 21:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 22:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 23:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 24:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 25:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 26:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 27:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 28:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 29:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 30:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 31:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 32:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 33:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 34:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 35:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 36:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 37:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 38:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 39:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 40:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 41:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 42:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 43:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 44:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 45:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 46:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 47:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 48:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 49:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 50:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 51:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 52:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 53:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 54:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 55:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 56:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 57:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 58:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 59:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 60:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 61:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 62:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 63:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 64:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 65:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 66:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 67:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 68:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 69:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 70:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 71:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 72:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 73:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 74:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 75:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 76:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 77:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 78:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 79:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 80:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 81:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 82:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 83:
                level_display = '<a href="emoji/5217843832472764060">⭐</a>'
            elif level == 84:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 85:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 86:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 87:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 88:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 89:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 90:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 91:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 92:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 93:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 94:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 95:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 96:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 97:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 98:
                level_display = '<a href="emoji/5217757976076518557">⭐</a>'
            elif level == 99:
                level_display = '<a href="emoji/5217498259404130179">🎖</a>'
            else:
                level_display = str(level)
            
            return {'success': True, 'has_rating': True, 'level': level, 'level_display': level_display}
        else:
            return {'success': True, 'has_rating': False, 'level_display': "لا يوجد"}
            
    except Exception:
        return {'success': False, 'level_display': "خطأ"}
        
async def zzz_info(zthon_user, event):
    FullUser = (await event.client(GetFullUserRequest(zthon_user.id))).full_user
    first_name = zthon_user.first_name
    full_name = FullUser.private_forward_name
    user_id = zthon_user.id
    zelzal_sinc = await fetch_zelzal(user_id)
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
    zzzsinc = zelzal_sinc if zelzal_sinc else ("غيـر معلـوم")
    
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
    zelzal_sinc = await fetch_zelzal(user_id)
    first_name = replied_user.first_name
    last_name = replied_user.last_name
    full_name = f"{first_name} {last_name}" if last_name else first_name
    rating_info = await get_user_rating(event.client, user_id)

# ✅ سطر واحد فقط - استخدم level_display مباشرة
    level_message = rating_info['level_display']
    
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
    gifts_info = await get_gifts_count(event.client, user_id)
    gifts_count = gifts_info['total_count']
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
        zelzzz = "نار وشرار  🏆"
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
                caption += f'ٴ<a href="emoji/6323136954380585694">❤️</a>'
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
                caption += f"<b>{ZEDM}الهدايا    ⤎</b>  {gifts_count} "
                caption += f'<a href="emoji/5407064810040864883">❤️</a> \n'
                caption += f"<b>{ZEDM}المستــوى   ⤎ {level_message}</b>\n"
                caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz} "
                caption += f'<a href="emoji/5253742260054409879">❤️</a>\n'
                caption += f"<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n" 
                if user_id != (await event.client.get_me()).id: 
                    caption += f"<b>{ZEDM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
                caption += f"<b>{ZEDM}الإنشـاء  ⤎</b>  {zzzsinc}  🗓\n" 
                caption += f"<b>{ZEDM}البايـو     ⤎</b>  {user_bio}\n"
                caption += f'ٴ<a href="emoji/6323136954380585694">❤️</a>'
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
                caption += f"<b>{ZEDM}الهدايا    ⤎</b>  {gifts_count}  🎁\n"
                caption += f"<b>{ZEDM}المستــوى   ⤎ {level_message}</b>\n"
                caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz}  💌\n"
                caption += f"<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n" 
                if user_id != (await event.client.get_me()).id: 
                    caption += f"<b>{ZEDM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
                caption += f"<b>{ZEDM}الإنشـاء  ⤎</b>  {zzzsinc}  🗓\n" 
                caption += f"<b>{ZEDM}البايـو     ⤎</b>  {user_bio}\n"
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
            caption += f"<b>{ZEDM}الهدايا    ⤎</b>  {gifts_count}  🎁\n"
            caption += f"<b>{ZEDM}المستــوى   ⤎ {level_message}</b>\n"
            caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz}  💌\n"
            caption += f"<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n" 
            if user_id != (await event.client.get_me()).id: 
                caption += f"<b>{ZEDM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
            caption += f"<b>{ZEDM}الإنشـاء  ⤎</b>  {zzzsinc}  🗓\n" 
            caption += f"<b>{ZEDM}البايـو     ⤎</b>  {user_bio}\n"
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
            zgft=gifts_count,
            zlvl=level_message,
            zmsg=zzz,
            ztmg=zelzzz,
            zcom=common_chat,
            zsnc=zzzsinc,
            zbio=user_bio,
        )
    return photo, caption

from telethon.tl.types import MessageEntityBlockquote
from telethon.tl.types import InputMediaPhoto
from telethon.tl.types import InputMediaUploadedPhoto

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
    
    # إضافة الاقتباس مع الحفاظ على الإيموجي
    quoted_caption = f"<blockquote>{caption}</blockquote>"
    
    if gvarstatus("ZID_TEMPLATE") is None:
        try:
            # رفع الصورة مع التشويش
            uploaded_file = await event.client.upload_file(photo)
            spoiler_media = InputMediaUploadedPhoto(
                file=uploaded_file,
                spoiler=True  # ✅ التشويش مفعل
            )
            
            # إرسال رسالة واحدة مع الصورة المشوشة والمعلومات
            await event.client.send_message(
                event.chat_id,
                message=quoted_caption,
                file=spoiler_media,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("html")
            )
            
            os.remove(photo)
            await zed.delete()
            
        except (TypeError, ChatSendMediaForbiddenError):
            await zed.edit(quoted_caption, parse_mode=CustomParseMode("html"))
    else:
        try:
            # نفس المنطق للقالب المخصص
            uploaded_file = await event.client.upload_file(photo)
            spoiler_media = InputMediaUploadedPhoto(
                file=uploaded_file,
                spoiler=True  # ✅ التشويش مفعل
            )
            
            await event.client.send_message(
                event.chat_id,
                message=quoted_caption,
                file=spoiler_media,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("html")
            )
            
            os.remove(photo)
            await zed.delete()
            
        except (TypeError, ChatSendMediaForbiddenError):
            await zed.edit(quoted_caption, parse_mode=CustomParseMode("html"))

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


from telethon.tl.types import MessageEntityCustomEmoji

@l313l.ar_cmd(
    pattern="ايموجي$",
    command=("جلب_ايموجي", plugin_category),
    info={
        "header": "جلب معرف الإيموجي",
        "الاستخدام": "{tr}جلب_ايموجي بالرد على الإيموجي",
    },
)
async def get_emoji_id(event):
    replied_message = await event.get_reply_message()
    
    # الرسالة لعدم الرد على الإيموجي
    if not replied_message:
        replied_emoji_message = "لم تقم بالرد على إيموجي"
    else:
        replied_emoji_message = None  # سيتم تعيينه لاحقًا إذا كان هناك إيموجي
    
    try:
        # التحقق مما إذا كانت الرسالة تحتوي على إيموجي مخصص
        if replied_message and replied_message.entities:
            emoji_entity = replied_message.entities[0]  # الحصول على الكيان الأول
            if isinstance(emoji_entity, MessageEntityCustomEmoji):
                emoji_id = emoji_entity.document_id  # معرف الإيموجي المدخل
                replied_emoji_message = f"`{emoji_id}`"  # تعيين معرف الإيموجي
                
        # جلب معرف الإيموجي الموجود في حساب المستخدم
        user = await event.client.get_me()
        if user.emoji_status:
            user_emoji_id = user.emoji_status.document_id
            user_emoji_message = f"`{user_emoji_id}`"
        else:
            user_emoji_message = "لا يوجد إيموجي في حسابك"

        # إرسال النتائج
        await edit_or_reply(
            event,
            f"🎟 ايدي الإيموجي:\n{replied_emoji_message}\n\n"
            f"🎟 ايدي الموجود في حسابك:\n{user_emoji_message}\n\n"
            f"للاستخدام: `<emoji document_id='{emoji_id if replied_emoji_message != 'لم تقم بالرد على إيموجي' else ''}'>🌟</emoji>`"
        )
    except Exception as e:
        await edit_or_reply(event, f"**⚠️ خطأ:** {str(e)}")
        
@l313l.ar_cmd(pattern="اسمي$")
async def permalink(event):
    user = await event.client.get_me()
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(event, f"[{tag}](tg://user?id={user.id})")


@l313l.ar_cmd(
    pattern="اسمه(?:\\s|$)([\\s\\S]*)",
    command=("اسمه", plugin_category),
    info={
        "header": "لـ جـلب اسـم الشخـص بشكـل ماركـدون ⦇.اسمه بالـرد او + معـرف/ايـدي الشخص⦈ ",
        "الاسـتخـدام": "{tr}اسمه <username/userid/reply>",
    },
)
async def permalink(event):
    """Generates a link to the user's PM with a custom text."""
    user = await get_user_from_event(event)
    if not user:
        return
    
    # الحصول على النص المخصص إذا وجد (الجزء بعد الأمر)
    custom_text = event.pattern_match.group(1).strip() if event.pattern_match.group(1) else None
    
    if custom_text:
        text = f"[{custom_text}](tg://user?id={user.id})"
    else:
        tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
        text = f"[{tag}](tg://user?id={user.id})"
    
    await edit_or_reply(event, text)
    
@l313l.on(admin_cmd(pattern="(خط التشويش|خط تشويش|تفعيل تشويش|تفعيل التشويش)"))
async def _(event):
    is_cllear = gvarstatus("cllear")
    if not is_cllear:
        addgvar ("cllear", "on")
        await edit_delete(event, "**⎉╎تم تفعيـل خـط التشـويش .. بنجـاح ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل تشويش) **")
        return
    if is_cllear:
        await edit_delete(event, "**⎉╎خـط التشـويش مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل تشويش) **")
        return

@l313l.on(admin_cmd(pattern="(تعطيل تشويش|تعطيل التشويش)"))
async def _(event):
    is_cllear = gvarstatus("cllear")
    if is_cllear:
        delgvar("cllear")
        await edit_delete(event, "**⎉╎تم تعطيـل خـط التشـويش .. بنجـاح ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل تشويش) **")
        return
    if not is_cllear:
        await edit_delete(event, "**⎉╎خـط التشـويش مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل تشويش) **")
        return

@l313l.on(events.NewMessage(outgoing=True))
async def comming(event):
    if event.message.text and not event.message.media and "." not in event.message.text:
        is_cllear = gvarstatus("cllear")
        if is_cllear:
            try:
                await event.edit(f"‹  **[{event.message.text}](spoiler)**  ›", parse_mode=CustomParseMode("markdown"))
            except MessageIdInvalidError:
                pass


# ================================================================================================ #
# =========================================الهدايا================================================= #
# ================================================================================================ #
from telethon.tl.functions.payments import GetStarGiftsRequest
from telethon.tl.types import InputDocument

async def get_star_gifts_info(client):
    """جلب معلومات الهدايا النجمية"""
    try:
        result = await client(GetStarGiftsRequest(hash=0))
        gifts = []
        
        for gift in getattr(result, "gifts", []):
            if not getattr(gift, "sold_out", False):
                gift_info = {
                    "id": gift.id,
                    "access_hash": gift.access_hash,  # الحصول على access_hash
                    "title": getattr(gift, "title", "بدون اسم") or getattr(gift, "alt", f"ID: {gift.id}"),
                    "stars": getattr(gift, "stars", 0),
                    "limited": getattr(gift, "limited", False),
                    "remains": getattr(gift, "availability_remains", 0),
                    "sold_out": getattr(gift, "sold_out", False)
                }
                gifts.append(gift_info)
        
        return gifts
        
    except Exception as e:
        return None

@l313l.ar_cmd(
    pattern="الهدايا$",
    command=("الهدايا", plugin_category),
    info={
        "header": "لـ عـرض الهدايـا النجميـة المتاحـة في تيليجرام",
        "الاستـخـدام": "{tr}الهدايا",
    },
)
async def star_gifts(event):
    "عرض الهدايا النجمية المتاحة"
    zed = await edit_or_reply(event, "**🎁 جـارِ جلب الهدايـا النجميـة...**")
    
    try:
        gifts = await get_star_gifts_info(event.client)
        
        if not gifts:
            await zed.edit("**❌ لا توجد هدايا نجمية متاحة حالياً**")
            return
        
        # ترتيب الهدايا حسب النجوم
        gifts = sorted(gifts, key=lambda g: -g["stars"])
        
        # إنشاء رسالة الهدايا
        message = "**🎁 الهدايـا النجميـة المتاحـة:**\n\n"
        
        for i, gift in enumerate(gifts, 1):
            limited_icon = " ⭐" if gift["limited"] else ""
            sold_out_icon = " 🔴" if gift["sold_out"] else " 🟢"
            remains_text = f" - المتبقي: {gift['remains']}" if gift["limited"] and gift["remains"] > 0 else ""
            
            message += (
                f"**{i}. {gift['title']}**\n"
                f"   ⏣ **{gift['stars']} نجمـة**{limited_icon}{sold_out_icon}{remains_text}\n\n"
            )
            
            # إرسال الملصق
            sticker = InputDocument(
                id=gift["id"],
                access_hash=gift["access_hash"],
                file_reference=b''  # يمكنك تركه فارغًا
            )
            await event.client.send_file(event.chat_id, sticker)  # 
