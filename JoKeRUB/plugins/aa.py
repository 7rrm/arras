import asyncio
import contextlib
import re
import html
import shutil
from io import BytesIO
import os
import base64
import requests
from requests import get
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import MessageEntityMentionName, EmojiStatusEmpty, InputWallPaper
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import pack_bot_file_id
from telethon.errors.rpcerrorlist import YouBlockedUserError, ChatSendMediaForbiddenError
from telethon import events, types
from telethon.extensions import markdown, html
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

# بقية الكود هنا...

@l313l.on(events.NewMessage(incoming=True))
async def set_wallpaper(event):
    # تحميل الصورة من الرابط
    response = requests.get("https://graph.org/file/eff529df26a96f563829a-f6422391f7f002cd3a.jpg")
    image = BytesIO(response.content)
    
    # رفع الصورة إلى Telegram
    uploaded = await event.client.upload_file(image, file_name="wallpaper.jpg")
    
    # تعيين الخلفية مع تأثير ضبابي
    wallpaper = InputWallPaper(id=1, 
                                file=InputFile(id=uploaded.id, 
                                               access_hash=uploaded.access_hash, 
                                               file_reference=uploaded.file_reference), 
                                title="My Wallpaper", 
                                caption="Background with Blur", 
                                color=None)
    
    # تعيين الخلفية للمحادثة
    await event.client(SetChatWallPaperRequest(event.chat_id, wallpaper, 0))  # 0 تعني عدم استخدام تأثيرات إضافية
