import asyncio
import contextlib
import re
import random
import time
import os
import requests
from datetime import datetime

from telethon import Button, events
from telethon.events import CallbackQuery
from telethon.tl.types import MessageEntityMentionName
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest, GetUsersRequest

from . import StartTime, l313l, mention
from ..core import check_owner
from ..Config import Config
from ..utils import Zed_Dev
from ..helpers import reply_id
from ..helpers.utils import _format
from ..core.logger import logging
from ..core.managers import edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.like_sql import (
    add_like,
    get_likes,
    remove_all_likes,
    remove_like,
)
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "العروض"
LOGS = logging.getLogger(__name__)

zed_dev = Zed_Dev
zelzal = (5427469031, 5280339206)
Zel_Uid = l313l.uid

ZED_BLACKLIST = [-1001935599871]

# متغير لتخزين الصفحات
template_pages = {}

# =========================================================== #
# الحصول على معلومات الحساب تلقائياً
# =========================================================== #

async def get_my_account_info():
    """استخراج معلومات الحساب الحالي تلقائياً"""
    me = await l313l.get_me()
    my_username = me.username if me.username else None
    my_name = me.first_name
    my_id = me.id
    return my_username, my_name, my_id

# =========================================================== #
# كليشات الايدي (ID Templates)
# =========================================================== #
# =========================================================== #
# كليشات الايدي (ID Templates) - زخارف عربية وإنجليزية
# =========================================================== #

ID_TEMPLATES = {
    # =========================================================== #
    # زخارف إنجليزية
    # =========================================================== #
    
    # زخرفة إنجليزية 1 - Script
    "eng_script": {
        "name": "𝓢𝓬𝓻𝓲𝓹𝓽 (EN)",
        "template": (
            "╭━━━━━━━━━━━━━━━╮\n"
            "┃ ✦ <b>𝓝𝓪𝓶𝓮</b> : {znam}\n"
            "┃ ✦ <b>𝓤𝓼𝓮𝓻</b> : {zusr}\n"
            "┃ ✦ <b>𝓘𝓓</b> : <code>{zidd}</code>\n"
            "┃ ✦ <b>𝓡𝓪𝓷𝓴</b> : {zrtb}\n"
            "┃ ✦ <b>𝓐𝓬𝓬𝓸𝓾𝓷𝓽</b> : {zpre}\n"
            "┃ ✦ <b>𝓥𝓘𝓟</b> : {zvip}\n"
            "┃ ✦ <b>𝓟𝓲𝓬𝓼</b> : {zpic}\n"
            "┃ ✦ <b>𝓜𝓼𝓰𝓼</b> : {zmsg} 💌\n"
            "┃ ✦ <b>𝓘𝓷𝓽𝓮𝓻𝓪𝓬𝓽</b> : {ztmg}\n"
            "┃ ✦ <b>𝓒𝓻𝓮𝓪𝓽𝓮𝓭</b> : {zsnc} 🗓\n"
            "┃ ✦ <b>𝓑𝓲𝓸</b> : {zbio}\n"
            "╰━━━━━━━━━━━━━━━╯"
        )
    },
    
    # زخرفة إنجليزية 2 - Double Struck
    "eng_double": {
        "name": "𝔻𝕠𝕦𝕓𝕝𝕖 (EN)",
        "template": (
            "╭━━━━━━━━━━━━━━━╮\n"
            "┃ ✦ <b>ℕ𝕒𝕞𝕖</b> : {znam}\n"
            "┃ ✦ <b>𝕌𝕤𝕖𝕣</b> : {zusr}\n"
            "┃ ✦ <b>𝕀𝔻</b> : <code>{zidd}</code>\n"
            "┃ ✦ <b>ℝ𝕒𝕟𝕜</b> : {zrtb}\n"
            "┃ ✦ <b>𝔸𝕔𝕔𝕠𝕦𝕟𝕥</b> : {zpre}\n"
            "┃ ✦ <b>𝕍𝕀ℙ</b> : {zvip}\n"
            "┃ ✦ <b>ℙ𝕚𝕔𝕤</b> : {zpic}\n"
            "┃ ✦ <b>𝕄𝕤𝕘𝕤</b> : {zmsg} 💌\n"
            "┃ ✦ <b>𝕀𝕟𝕥𝕖𝕣𝕒𝕔𝕥</b> : {ztmg}\n"
            "┃ ✦ <b>ℂ𝕣𝕖𝕒𝕥𝕖𝕕</b> : {zsnc} 🗓\n"
            "┃ ✦ <b>𝔹𝕚𝕠</b> : {zbio}\n"
            "╰━━━━━━━━━━━━━━━╯"
        )
    },
    
    # زخرفة إنجليزية 3 - Small Caps
    "eng_smallcaps": {
        "name": "Sᴍᴀʟʟ Cᴀᴘs (EN)",
        "template": (
            "╭━━━━━━━━━━━━━━━╮\n"
            "┃ ✦ <b>Nᴀᴍᴇ</b> : {znam}\n"
            "┃ ✦ <b>Usᴇʀ</b> : {zusr}\n"
            "┃ ✦ <b>ID</b> : <code>{zidd}</code>\n"
            "┃ ✦ <b>Rᴀɴᴋ</b> : {zrtb}\n"
            "┃ ✦ <b>Aᴄᴄᴏᴜɴᴛ</b> : {zpre}\n"
            "┃ ✦ <b>VIP</b> : {zvip}\n"
            "┃ ✦ <b>Pɪᴄs</b> : {zpic}\n"
            "┃ ✦ <b>Msɢs</b> : {zmsg} 💌\n"
            "┃ ✦ <b>Iɴᴛᴇʀᴀᴄᴛ</b> : {ztmg}\n"
            "┃ ✦ <b>Cʀᴇᴀᴛᴇᴅ</b> : {zsnc} 🗓\n"
            "┃ ✦ <b>Bɪᴏ</b> : {zbio}\n"
            "╰━━━━━━━━━━━━━━━╯"
        )
    },
    
    # زخرفة إنجليزية 4 - Circled
    "eng_circled": {
        "name": "🅒🅘🅡🅒🅛🅔 (EN)",
        "template": (
            "╭━━━━━━━━━━━━━━━╮\n"
            "┃ ✦ <b>🅝🅐🅜🅔</b> : {znam}\n"
            "┃ ✦ <b>🅤🅢🅔🅡</b> : {zusr}\n"
            "┃ ✦ <b>🅘🅓</b> : <code>{zidd}</code>\n"
            "┃ ✦ <b>🅡🅐🅝🅚</b> : {zrtb}\n"
            "┃ ✦ <b>🅐🅒🅒🅞🅤🅝🅣</b> : {zpre}\n"
            "┃ ✦ <b>🅥🅘🅟</b> : {zvip}\n"
            "┃ ✦ <b>🅟🅘🅒🅢</b> : {zpic}\n"
            "┃ ✦ <b>🅜🅢🅖🅢</b> : {zmsg} 💌\n"
            "┃ ✦ <b>🅘🅝🅣🅔🅡🅐🅒🅣</b> : {ztmg}\n"
            "┃ ✦ <b>🅒🅡🅔🅐🅣🅔🅓</b> : {zsnc} 🗓\n"
            "┃ ✦ <b>🅑🅘🅞</b> : {zbio}\n"
            "╰━━━━━━━━━━━━━━━╯"
        )
    },
    
    # زخرفة إنجليزية 5 - Bold
    "eng_bold": {
        "name": "𝐁𝐨𝐥𝐝 (EN)",
        "template": (
            "╭━━━━━━━━━━━━━━━╮\n"
            "┃ ✦ <b>𝐍𝐚𝐦𝐞</b> : {znam}\n"
            "┃ ✦ <b>𝐔𝐬𝐞𝐫</b> : {zusr}\n"
            "┃ ✦ <b>𝐈𝐃</b> : <code>{zidd}</code>\n"
            "┃ ✦ <b>𝐑𝐚𝐧𝐤</b> : {zrtb}\n"
            "┃ ✦ <b>𝐀𝐜𝐜𝐨𝐮𝐧𝐭</b> : {zpre}\n"
            "┃ ✦ <b>𝐕𝐈𝐏</b> : {zvip}\n"
            "┃ ✦ <b>𝐏𝐢𝐜𝐬</b> : {zpic}\n"
            "┃ ✦ <b>𝐌𝐬𝐠𝐬</b> : {zmsg} 💌\n"
            "┃ ✦ <b>𝐈𝐧𝐭𝐞𝐫𝐚𝐜𝐭</b> : {ztmg}\n"
            "┃ ✦ <b>𝐂𝐫𝐞𝐚𝐭𝐞𝐝</b> : {zsnc} 🗓\n"
            "┃ ✦ <b>𝐁𝐢𝐨</b> : {zbio}\n"
            "╰━━━━━━━━━━━━━━━╯"
        )
    },
    
    # زخرفة إنجليزية 6 - Italic
    "eng_italic": {
        "name": "𝐼𝓉𝒶𝓁𝒾𝒸 (EN)",
        "template": (
            "╭━━━━━━━━━━━━━━━╮\n"
            "┃ ✦ <b>𝐼𝓃𝒶𝓂𝑒</b> : {znam}\n"
            "┃ ✦ <b>𝒰𝓈𝑒𝓇</b> : {zusr}\n"
            "┃ ✦ <b>𝐼𝒟</b> : <code>{zidd}</code>\n"
            "┃ ✦ <b>𝑅𝒶𝓃𝓀</b> : {zrtb}\n"
            "┃ ✦ <b>𝒜𝒸𝒸ℴ𝓊𝓃𝓉</b> : {zpre}\n"
            "┃ ✦ <b>𝒱ℐ𝒫</b> : {zvip}\n"
            "┃ ✦ <b>𝒫𝒾𝒸𝓈</b> : {zpic}\n"
            "┃ ✦ <b>𝑀𝓈ℊ𝓈</b> : {zmsg} 💌\n"
            "┃ ✦ <b>𝐼𝓃𝓉ℯ𝓇𝒶𝒸𝓉</b> : {ztmg}\n"
            "┃ ✦ <b>𝒞𝓇ℯ𝒶𝓉ℯ𝒹</b> : {zsnc} 🗓\n"
            "┃ ✦ <b>𝐵𝒾ℴ</b> : {zbio}\n"
            "╰━━━━━━━━━━━━━━━╯"
        )
    },
    
    # زخرفة إنجليزية 7 - Mono
    "eng_mono": {
        "name": "𝙼𝚘𝚗𝚘 (EN)",
        "template": (
            "╭━━━━━━━━━━━━━━━╮\n"
            "┃ ✦ <b>𝙽𝚊𝚖𝚎</b> : {znam}\n"
            "┃ ✦ <b>𝚄𝚜𝚎𝚛</b> : {zusr}\n"
            "┃ ✦ <b>𝙸𝙳</b> : <code>{zidd}</code>\n"
            "┃ ✦ <b>𝚁𝚊𝚗𝚔</b> : {zrtb}\n"
            "┃ ✦ <b>𝙰𝚌𝚌𝚘𝚞𝚗𝚝</b> : {zpre}\n"
            "┃ ✦ <b>𝚅𝙸𝙿</b> : {zvip}\n"
            "┃ ✦ <b>𝙿𝚒𝚌𝚜</b> : {zpic}\n"
            "┃ ✦ <b>𝙼𝚜𝚐𝚜</b> : {zmsg} 💌\n"
            "┃ ✦ <b>𝙸𝚗𝚝𝚎𝚛𝚊𝚌𝚝</b> : {ztmg}\n"
            "┃ ✦ <b>𝙲𝚛𝚎𝚊𝚝𝚎𝚍</b> : {zsnc} 🗓\n"
            "┃ ✦ <b>𝙱𝚒𝚘</b> : {zbio}\n"
            "╰━━━━━━━━━━━━━━━╯"
        )
    },
    
    # زخرفة إنجليزية 8 - Bubble
    "eng_bubble": {
        "name": "Ⓑⓤⓑⓑⓛⓔ (EN)",
        "template": (
            "╭━━━━━━━━━━━━━━━╮\n"
            "┃ ✦ <b>Ⓝⓐⓜⓔ</b> : {znam}\n"
            "┃ ✦ <b>Ⓤⓢⓔⓡ</b> : {zusr}\n"
            "┃ ✦ <b>ⒾⒹ</b> : <code>{zidd}</code>\n"
            "┃ ✦ <b>Ⓡⓐⓝⓚ</b> : {zrtb}\n"
            "┃ ✦ <b>Ⓐⓒⓒⓞⓤⓝⓣ</b> : {zpre}\n"
            "┃ ✦ <b>ⓋⒾⓅ</b> : {zvip}\n"
            "┃ ✦ <b>Ⓟⓘⓒⓢ</b> : {zpic}\n"
            "┃ ✦ <b>Ⓜⓢⓖⓢ</b> : {zmsg} 💌\n"
            "┃ ✦ <b>Ⓘⓝⓣⓔⓡⓐⓒⓣ</b> : {ztmg}\n"
            "┃ ✦ <b>Ⓒⓡⓔⓐⓣⓔⓓ</b> : {zsnc} 🗓\n"
            "┃ ✦ <b>Ⓑⓘⓞ</b> : {zbio}\n"
            "╰━━━━━━━━━━━━━━━╯"
        )
    },
    
    # زخرفة إنجليزية 9 - Fraktur
    "eng_fraktur": {
        "name": "𝔉𝔯𝔞𝔨𝔱𝔲𝔯 (EN)",
        "template": (
            "╭━━━━━━━━━━━━━━━╮\n"
            "┃ ✦ <b>𝔑𝔞𝔪𝔢</b> : {znam}\n"
            "┃ ✦ <b>𝔘𝔰𝔢𝔯</b> : {zusr}\n"
            "┃ ✦ <b>ℑ𝔇</b> : <code>{zidd}</code>\n"
            "┃ ✦ <b>ℜ𝔞𝔫𝔨</b> : {zrtb}\n"
            "┃ ✦ <b>𝔄𝔠𝔠𝔬𝔲𝔫𝔱</b> : {zpre}\n"
            "┃ ✦ <b>𝔙ℑ𝔓</b> : {zvip}\n"
            "┃ ✦ <b>𝔓𝔦𝔠𝔰</b> : {zpic}\n"
            "┃ ✦ <b>𝔐𝔰𝔤𝔰</b> : {zmsg} 💌\n"
            "┃ ✦ <b>ℑ𝔫𝔱𝔢𝔯𝔞𝔠𝔱</b> : {ztmg}\n"
            "┃ ✦ <b>ℭ𝔯𝔢𝔞𝔱𝔢𝔡</b> : {zsnc} 🗓\n"
            "┃ ✦ <b>𝔅𝔦𝔬</b> : {zbio}\n"
            "╰━━━━━━━━━━━━━━━╯"
        )
    },
    
    # =========================================================== #
    # زخارف عربية
    # =========================================================== #
    
    # زخرفة عربية 1 - أنيق
    "arb_elegant": {
        "name": "أنيق (عربي)",
        "template": (
            "╭━━━━━━━━━━━━━━━╮\n"
            "┃ ✦ <b>الاســم</b> : {znam}\n"
            "┃ ✦ <b>اليـوزر</b> : {zusr}\n"
            "┃ ✦ <b>الايـدي</b> : <code>{zidd}</code>\n"
            "┃ ✦ <b>الرتبــه</b> : {zrtb}\n"
            "┃ ✦ <b>الحساب</b> : {zpre}\n"
            "┃ ✦ <b>الاشتراك</b> : {zvip}\n"
            "┃ ✦ <b>الصـور</b> : {zpic}\n"
            "┃ ✦ <b>الرسائل</b> : {zmsg} 💌\n"
            "┃ ✦ <b>التفاعل</b> : {ztmg}\n"
            "┃ ✦ <b>الإنشـاء</b> : {zsnc} 🗓\n"
            "┃ ✦ <b>البايـو</b> : {zbio}\n"
            "╰━━━━━━━━━━━━━━━╯"
        )
    },
    
    # زخرفة عربية 2 - قلوب
    "arb_heart": {
        "name": "قلوب (عربي)",
        "template": (
            "♥️━━━━━━━━━━━━━━━♥️\n"
            "♥️ <b>الاســم</b> : {znam}\n"
            "♥️ <b>اليـوزر</b> : {zusr}\n"
            "♥️ <b>الايـدي</b> : <code>{zidd}</code>\n"
            "♥️ <b>الرتبــه</b> : {zrtb}\n"
            "♥️ <b>الحساب</b> : {zpre}\n"
            "♥️ <b>الاشتراك</b> : {zvip}\n"
            "♥️ <b>الصـور</b> : {zpic}\n"
            "♥️ <b>الرسائل</b> : {zmsg} 💌\n"
            "♥️ <b>التفاعل</b> : {ztmg}\n"
            "♥️ <b>الإنشـاء</b> : {zsnc} 🗓\n"
            "♥️ <b>البايـو</b> : {zbio}\n"
            "♥️━━━━━━━━━━━━━━━♥️"
        )
    },
    
    # زخرفة عربية 3 - نجوم
    "arb_star": {
        "name": "نجوم (عربي)",
        "template": (
            "★━━━━━━━━━━━━━━━━━━★\n"
            "✧ <b>الاســم</b> : {znam}\n"
            "✧ <b>اليـوزر</b> : {zusr}\n"
            "✧ <b>الايـدي</b> : <code>{zidd}</code>\n"
            "✧ <b>الرتبــه</b> : {zrtb}\n"
            "✧ <b>الحساب</b> : {zpre}\n"
            "✧ <b>الاشتراك</b> : {zvip}\n"
            "✧ <b>الصـور</b> : {zpic}\n"
            "✧ <b>الرسائل</b> : {zmsg} 💌\n"
            "✧ <b>التفاعل</b> : {ztmg}\n"
            "✧ <b>الإنشـاء</b> : {zsnc} 🗓\n"
            "✧ <b>البايـو</b> : {zbio}\n"
            "★━━━━━━━━━━━━━━━━━━★"
        )
    },
    
    # زخرفة عربية 4 - صندوق
    "arb_box": {
        "name": "صندوق (عربي)",
        "template": (
            "┌─────────────────┐\n"
            "│ ✦ <b>الاســم</b> : {znam}\n"
            "│ ✦ <b>اليـوزر</b> : {zusr}\n"
            "│ ✦ <b>الايـدي</b> : <code>{zidd}</code>\n"
            "│ ✦ <b>الرتبــه</b> : {zrtb}\n"
            "│ ✦ <b>الحساب</b> : {zpre}\n"
            "│ ✦ <b>الاشتراك</b> : {zvip}\n"
            "│ ✦ <b>الصـور</b> : {zpic}\n"
            "│ ✦ <b>الرسائل</b> : {zmsg} 💌\n"
            "│ ✦ <b>التفاعل</b> : {ztmg}\n"
            "│ ✦ <b>الإنشـاء</b> : {zsnc} 🗓\n"
            "│ ✦ <b>البايـو</b> : {zbio}\n"
            "└─────────────────┘"
        )
    },
    
    # زخرفة عربية 5 - سهام
    "arb_arrow": {
        "name": "سهام (عربي)",
        "template": (
            "➜━━━━━━━━━━━━━━━➜\n"
            "➜ <b>الاســم</b> : {znam}\n"
            "➜ <b>اليـوزر</b> : {zusr}\n"
            "➜ <b>الايـدي</b> : <code>{zidd}</code>\n"
            "➜ <b>الرتبــه</b> : {zrtb}\n"
            "➜ <b>الحساب</b> : {zpre}\n"
            "➜ <b>الاشتراك</b> : {zvip}\n"
            "➜ <b>الصـور</b> : {zpic}\n"
            "➜ <b>الرسائل</b> : {zmsg} 💌\n"
            "➜ <b>التفاعل</b> : {ztmg}\n"
            "➜ <b>الإنشـاء</b> : {zsnc} 🗓\n"
            "➜ <b>البايـو</b> : {zbio}\n"
            "➜━━━━━━━━━━━━━━━➜"
        )
    },
    
    # زخرفة عربية 6 - تاج
    "arb_crown": {
        "name": "تاج (عربي)",
        "template": (
            "👑━━━━━━━━━━━━━━━👑\n"
            "┃ ✦ <b>الاســم</b> : {znam}\n"
            "┃ ✦ <b>اليـوزر</b> : {zusr}\n"
            "┃ ✦ <b>الايـدي</b> : <code>{zidd}</code>\n"
            "┃ ✦ <b>الرتبــه</b> : {zrtb}\n"
            "┃ ✦ <b>الحساب</b> : {zpre}\n"
            "┃ ✦ <b>الاشتراك</b> : {zvip}\n"
            "┃ ✦ <b>الصـور</b> : {zpic}\n"
            "┃ ✦ <b>الرسائل</b> : {zmsg} 💌\n"
            "┃ ✦ <b>التفاعل</b> : {ztmg}\n"
            "┃ ✦ <b>الإنشـاء</b> : {zsnc} 🗓\n"
            "┃ ✦ <b>البايـو</b> : {zbio}\n"
            "👑━━━━━━━━━━━━━━━👑"
        )
    },
    
    # زخرفة عربية 7 - ألماس
    "arb_diamond": {
        "name": "ألماس (عربي)",
        "template": (
            "💎━━━━━━━━━━━━━━━💎\n"
            "◇ <b>الاســم</b> : {znam}\n"
            "◇ <b>اليـوزر</b> : {zusr}\n"
            "◇ <b>الايـدي</b> : <code>{zidd}</code>\n"
            "◇ <b>الرتبــه</b> : {zrtb}\n"
            "◇ <b>الحساب</b> : {zpre}\n"
            "◇ <b>الاشتراك</b> : {zvip}\n"
            "◇ <b>الصـور</b> : {zpic}\n"
            "◇ <b>الرسائل</b> : {zmsg} 💌\n"
            "◇ <b>التفاعل</b> : {ztmg}\n"
            "◇ <b>الإنشـاء</b> : {zsnc} 🗓\n"
            "◇ <b>البايـو</b> : {zbio}\n"
            "💎━━━━━━━━━━━━━━━💎"
        )
    },
    
    # زخرفة عربية 8 - زهور
    "arb_flower": {
        "name": "زهور (عربي)",
        "template": (
            "❀━━━━━━━━━━━━━━━❀\n"
            "✿ <b>الاســم</b> : {znam}\n"
            "✿ <b>اليـوزر</b> : {zusr}\n"
            "✿ <b>الايـدي</b> : <code>{zidd}</code>\n"
            "✿ <b>الرتبــه</b> : {zrtb}\n"
            "✿ <b>الحساب</b> : {zpre}\n"
            "✿ <b>الاشتراك</b> : {zvip}\n"
            "✿ <b>الصـور</b> : {zpic}\n"
            "✿ <b>الرسائل</b> : {zmsg} 💌\n"
            "✿ <b>التفاعل</b> : {ztmg}\n"
            "✿ <b>الإنشـاء</b> : {zsnc} 🗓\n"
            "✿ <b>البايـو</b> : {zbio}\n"
            "❀━━━━━━━━━━━━━━━❀"
        )
    },
    
    # زخرفة عربية 9 - بسيط
    "arb_simple": {
        "name": "بسيط (عربي)",
        "template": (
            "👤 <b>الاســم</b> : {znam}\n"
            "🆔 <b>الايـدي</b> : <code>{zidd}</code>\n"
            "📝 <b>اليـوزر</b> : {zusr}\n"
            "⭐ <b>الحساب</b> : {zpre}\n"
            "💬 <b>الرسائل</b> : {zmsg} 💌\n"
            "📅 <b>الإنشـاء</b> : {zsnc} 🗓\n"
            "📝 <b>البايـو</b> : {zbio}\n"
        )
    },
    
    # زخرفة عربية 10 - خطوط
    "arb_lines": {
        "name": "خطوط (عربي)",
        "template": (
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            "⎯ <b>الاســم</b> : {znam}\n"
            "⎯ <b>اليـوزر</b> : {zusr}\n"
            "⎯ <b>الايـدي</b> : <code>{zidd}</code>\n"
            "⎯ <b>الرتبــه</b> : {zrtb}\n"
            "⎯ <b>الحساب</b> : {zpre}\n"
            "⎯ <b>الرسائل</b> : {zmsg} 💌\n"
            "⎯ <b>التفاعل</b> : {ztmg}\n"
            "⎯ <b>الإنشـاء</b> : {zsnc} 🗓\n"
            "⎯ <b>البايـو</b> : {zbio}\n"
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
        )
    },
    
    # =========================================================== #
    # كليشات سريعة
    # =========================================================== #
    
    # سريعة 1
    "quick_one": {
        "name": "سريع ❶",
        "template": (
            "<b>{znam}</b> | <code>{zidd}</code> | {zusr}\n"
            "{zrtb} | {zpre} | {zmsg} 💌"
        )
    },
    
    # سريعة 2
    "quick_two": {
        "name": "سريع ❷",
        "template": (
            "<b>{znam}</b>\n"
            "<code>{zidd}</code>\n"
            "{zusr}\n"
            "{zrtb}"
        )
    },
    
    # =========================================================== #
    # الكليشة الافتراضية
    # =========================================================== #
    
    "default": {
        "name": "الافتراضي",
        "template": DEFAULT_TEMPLATE
    }
}


# =========================================================== #
# دوال مساعدة
# =========================================================== #

async def fetch_zelzal(user_id):
    headers = {
        'Host': 'restore-access.indream.app',
        'Connection': 'keep-alive',
        'x-api-key': 'e758fb28-79be-4d1c-af6b-066633ded128',
        'Accept': '*/*',
        'Accept-Language': 'ar',
        'User-Agent': 'Nicegram/101 CFNetwork/1404.0.5 Darwin/22.3.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = '{"telegramId":' + str(user_id) + '}'
    try:
        response = requests.post('https://restore-access.indream.app/regdate', headers=headers, data=data).json()
        return response['data']['date']
    except Exception:
        return "غير معلوم"

async def fetch_info(event, user_id=None):
    """Get details from the User object."""
    if user_id is None:
        replied_user = await l313l.get_me()
        user_id = replied_user.id
    else:
        replied_user = await l313l.get_entity(user_id)
    
    FullUser = (await l313l(GetFullUserRequest(replied_user.id))).full_user
    replied_user_profile_photos = await l313l(
        GetUserPhotosRequest(user_id=replied_user.id, offset=42, max_id=0, limit=80)
    )
    replied_user_profile_photos_count = replied_user_profile_photos.count if replied_user_profile_photos else "لا يوجد"
    
    zelzal_sinc = await fetch_zelzal(user_id)
    first_name = replied_user.first_name
    full_name = FullUser.private_forward_name or first_name
    common_chat = FullUser.common_chats_count
    username = f"@{replied_user.username}" if replied_user.username else "لا يوجد"
    user_bio = FullUser.about or "لا يوجد"
    
    zilzal = (await l313l.get_entity(user_id)).premium
    zpre = "ℙℝ𝔼𝕄𝕀𝕌𝕄 🌟" if zilzal or user_id in zelzal else "𝕍𝕀ℝ𝕋𝕌𝔸𝕃 ✨"
    
    photo_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, str(user_id) + ".jpg")
    await l313l.download_profile_photo(user_id, photo_path, download_big=True)
    
    first_name = first_name.replace("\u2060", "") if first_name else "مستخدم"
    zzzsinc = zelzal_sinc if zelzal_sinc else "غير معلوم"
    
    # حساب عدد الرسائل
    try:
        zmsg = await l313l.get_messages(event.chat_id, 0, from_user=user_id)
        zzz = zmsg.total if zmsg else 0
    except Exception:
        zzz = 0
    
    if zzz < 100:
        zelzzz = "غير متفاعل 🗿"
    elif zzz < 500:
        zelzzz = "ضعيف 🗿"
    elif zzz < 700:
        zelzzz = "شد حيلك 🏇"
    elif zzz < 1000:
        zelzzz = "ماشي الحال 🏄🏻‍♂"
    elif zzz < 2000:
        zelzzz = "ملك التفاعل 🎖"
    elif zzz < 3000:
        zelzzz = "امبراطور التفاعل 🥇"
    elif zzz < 4000:
        zelzzz = "غنبله 💣"
    else:
        zelzzz = "نار وشرر 🏆"
    
    # تحديد الرتبة
    if user_id in zelzal:
        rotbat = "مطـور السـورس 𓄂" 
    elif user_id in zed_dev:
        rotbat = "مـطـور 𐏕" 
    elif user_id == (await l313l.get_me()).id:
        rotbat = "مـالك الحساب 𓀫" 
    else:
        rotbat = "العضـو 𓅫"
    
    # الكليشة المختارة (إذا لم تكن مختارة، استخدم الأساسية)
    selected_template = gvarstatus("SELECTED_ID_TEMPLATE")
    if selected_template and selected_template in ID_TEMPLATES:
        template_data = ID_TEMPLATES[selected_template]
        template = template_data["template"]
    else:
        template = DEFAULT_TEMPLATE
    
    zvip = "𝕍𝕀ℙ 💎" if user_id in Zed_Dev else "ℕ𝕆ℕ𝔼"
    
    caption = template.format(
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
    
    return photo_path, caption

# =========================================================== #
# دالة تحديث رسالة الكليشات
# =========================================================== #

async def update_template_message(event, user_id):
    """تحديث رسالة الكليشات الحالية"""
    template_keys = list(ID_TEMPLATES.keys())
    total_pages = len(template_keys)
    
    current_page = template_pages.get(user_id, 0)
    if current_page >= total_pages:
        current_page = 0
    current_key = template_keys[current_page]
    current_template = ID_TEMPLATES[current_key]
    
    text = f"**🎨 الكليشة {current_page + 1}/{total_pages}**\n\n"
    text += f"```\n{current_template['template'][:500]}\n```\n"
    text += f"• **الاسم:** {current_template['name']}"
    
    buttons = []
    nav_buttons = []
    if current_page > 0:
        nav_buttons.append(Button.inline("◀️ رجوع", data="template_prev", style="primary"))
    if current_page < total_pages - 1:
        nav_buttons.append(Button.inline("التالي ▶️", data="template_next", style="primary"))
    
    if nav_buttons:
        buttons.append(nav_buttons)
    
    buttons.append([
        Button.inline("💾 حفظ الكليشة", data=f"template_save_{current_key}", style="success"),
        Button.inline("❌ إغلاق", data="close_panel", style="danger")
    ])
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# الاستعلامات المضمنة
# =========================================================== #

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler_like(event):
        builder = event.builder
        query = event.text
        await l313l.get_me()
        
        # ✅ استعلام idid - بطاقة المعلومات
        if query.startswith("idid") and event.query.user_id == l313l.uid:
            try:
                photo_path, caption = await fetch_info(event)
            except Exception as e:
                return
            
            like_button_mode = gvarstatus("LIKE_BUTTON_MODE") or "likes"
            my_username, my_name, my_id = await get_my_account_info()
            my_link = f"https://t.me/{my_username}" if my_username else f"tg://user?id={my_id}"
            
            # زر واحد فقط حسب النمط المختار
            if like_button_mode == "likes":
                Like_id = int(gvarstatus("Like_Id")) if gvarstatus("Like_Id") else 0
                buttons = [[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes", style="primary")]]
            else:
                buttons = [[Button.url(f"👤 {my_name}", my_link, style="primary")]]
            
            try:
                if photo_path and os.path.exists(photo_path):
                    uploaded_file = await event.client.upload_file(file=photo_path)
                    result = builder.photo(
                        uploaded_file,
                        text=caption,
                        buttons=buttons,
                        link_preview=False,
                        parse_mode="html",
                    )
                    os.remove(photo_path)
                else:
                    result = builder.article(
                        title="l313l",
                        text=caption,
                        buttons=buttons,
                        link_preview=False,
                        parse_mode="html",
                    )
            except Exception:
                result = builder.article(
                    title="l313l",
                    text=caption,
                    buttons=buttons,
                    link_preview=False,
                    parse_mode="html",
                )
            
            await event.answer([result] if result else None)
        
        # ✅ استعلام كليشات الايدي
        elif query.startswith("id_templates") and event.query.user_id == l313l.uid:
            user_id = event.query.user_id
            template_keys = list(ID_TEMPLATES.keys())
            total_pages = len(template_keys)
            
            # إعادة تعيين الصفحة إلى 0 عند الفتح الجديد
            template_pages[user_id] = 0
            current_key = template_keys[0]
            current_template = ID_TEMPLATES[current_key]
            
            text = f"**🎨 الكليشة 1/{total_pages}**\n\n"
            text += f"```\n{current_template['template'][:500]}\n```\n"
            text += f"• **الاسم:** {current_template['name']}"
            
            buttons = []
            nav_buttons = []
            if total_pages > 1:
                nav_buttons.append(Button.inline("التالي ▶️", data="template_next", style="primary"))
            
            if nav_buttons:
                buttons.append(nav_buttons)
            
            buttons.append([
                Button.inline("💾 حفظ الكليشة", data=f"template_save_{current_key}", style="success"),
                Button.inline("❌ إغلاق", data="close_panel", style="danger")
            ])
            
            result = builder.article(
                title="🎨 كليشات الايدي",
                description=f"الكليشة 1/{total_pages}: {current_template['name']}",
                text=text,
                buttons=buttons,
                link_preview=False,
                parse_mode="Markdown",
            )
            await event.answer([result], cache_time=0)
        
        # ✅ استعلام نمط اللايك
        elif query.startswith("like_mode") and event.query.user_id == l313l.uid:
            current_mode = gvarstatus("LIKE_BUTTON_MODE") or "likes"
            my_username, my_name, my_id = await get_my_account_info()
            
            text = f"**⚙️ إعدادات زر اللايك**\n\n"
            text += f"• النمط الحالي: **{'❤️ نمط القلوب' if current_mode == 'likes' else '👤 نمط الحساب'}**\n\n"
            text += f"• شكل الزر:\n"
            
            if current_mode == "likes":
                text += f"`ʟɪᴋᴇ ♥️ ⤑ (العدد)`\n"
                text += f"• زر الإعجاب فقط"
            else:
                text += f"`👤 {my_name}`\n"
                text += f"• رابط حسابك فقط"
            
            text += f"\n\n• استخدم الأمر `.نمط اللايك` مرة أخرى للتبديل"
            
            buttons = [
                [Button.inline("🔄 تبديل النمط", data="toggle_like_mode", style="primary")],
                [Button.inline("❌ إغلاق", data="close_panel", style="danger")]
            ]
            
            result = builder.article(
                title="⚙️ إعدادات اللايك",
                description=f"النمط الحالي: {'قلوب' if current_mode == 'likes' else 'حساب'}",
                text=text,
                buttons=buttons,
                link_preview=False,
                parse_mode="Markdown",
            )
            await event.answer([result], cache_time=0)

# =========================================================== #
# أوامر المستخدم
# =========================================================== #

@l313l.ar_cmd(pattern="لايك(?: |$)(.*)")
async def who(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵**")
    
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in zed_dev):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷**")
    
    zed = await edit_or_reply(event, "⇆")
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "idid")
    await response[0].click(event.chat_id)
    await zed.delete()

@l313l.ar_cmd(pattern="كليشات الايدي$")
async def id_templates_cmd(event):
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "id_templates")
    await response[0].click(event.chat_id)
    await event.delete()

@l313l.ar_cmd(pattern="نمط اللايك$")
async def like_mode_cmd(event):
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "like_mode")
    await response[0].click(event.chat_id)
    await event.delete()

@l313l.ar_cmd(pattern="المعجبين$")
async def on_like_list(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵**")
    
    likers = get_likes(l313l.uid)
    if likers:
        OUT_STR = "𓆩 𝗮𝗥𝗥𝗮𝗦 𝗟𝗶𝗸𝗲 - **قائمـة المعجبيــن** ❤️𓆪\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
        for mogab in likers:
            OUT_STR += f"\n• **الاسم:** [{mogab.f_name}](tg://user?id={mogab.lik_id})\n• **الايـدي:** `{mogab.lik_id}`\n• **اليـوزر:** {mogab.f_user}\n"
        OUT_STR += f"\n• **إجمالي عـدد المعجبيـن {len(likers)}**"
        await edit_or_reply(event, OUT_STR)
    else:
        await edit_or_reply(event, "**- مسكيـن ع باب الله 🧑🏻‍🦯**\n**- ماعنـدك معجبيـن حالياً ❤️‍🩹**")

@l313l.ar_cmd(pattern="مسح المعجبين$")
async def on_all_liked_delete(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵**")
    
    likers = get_likes(l313l.uid)
    if likers:
        zed = await edit_or_reply(event, "⪼ جـارِ مسـح المعجبيـن .. انتظـر ⏳")
        remove_all_likes(l313l.uid)
        delgvar("Like_Id")
        await zed.edit("⪼ تم حـذف جميـع المعجبيـن .. بنجـاح ✅")
    else:
        await edit_or_reply(event, "**- مسكيـن ع باب الله 🧑🏻‍🦯**\n**- ماعنـدك معجبيـن حالياً ❤️‍🩹**")

@l313l.ar_cmd(pattern="مسح الاعدادات$")
async def reset_settings(event):
    delgvar("SELECTED_ID_TEMPLATE")
    delgvar("LIKE_BUTTON_MODE")
    delgvar("Like_Id")
    remove_all_likes(l313l.uid)
    await edit_or_reply(event, "✅ تم مسح جميع الإعدادات والتغييرات بنجاح!\n\n• عادت الكليشة إلى الأساسية\n• عاد نمط اللايك إلى القلوب\n• تم مسح جميع المعجبين")

# =========================================================== #
# أزرار التفاعل (CallbackQuery)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"likes")))
async def like_callback(event):
    user_id = event.sender_id
    
    if user_id == l313l.uid:
        return await event.answer("❌ لا يمكنك الإعجاب بنفسك!", alert=True)
    
    try:
        user = await l313l.get_entity(user_id)
        user_name = f"{user.first_name}{' ' + user.last_name if user.last_name else ''}"
        user_username = f"@{user.username}" if user.username else "لا يوجد"
    except Exception:
        user_name = "مستخدم محذوف"
        user_username = "لا يوجد"
    
    Like_id = int(gvarstatus("Like_Id")) if gvarstatus("Like_Id") else 0
    like_button_mode = gvarstatus("LIKE_BUTTON_MODE") or "likes"
    
    if add_like(str(l313l.uid), str(user_id), user_name, user_username) is True:
        Like_id += 1
        addgvar("Like_Id", Like_id)
    else:
        return await event.answer("❤️ انت معجب من قبل بهذا الشخص!", cache_time=0, alert=True)
    
    # إرسال إشعار للمطور
    try:
        await l313l.send_message(
            BOTLOG_CHATID,
            f"#لايك_جديد 💝\n\n"
            f"**- المستخدم :** [{user_name}](tg://user?id={user_id})\n"
            f"**- الايدي :** `{user_id}`\n"
            f"**- اليوزر :** {user_username}\n"
            f"**- أصبح عدد المعجبين :** {Like_id}",
        )
    except Exception:
        pass
    
    # تحديث الزر حسب النمط
    if like_button_mode == "likes":
        button_text = f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}"
        button_data = "likes"
        buttons = [[Button.inline(button_text, data=button_data, style="primary")]]
    else:
        my_username, my_name, my_id = await get_my_account_info()
        my_link = f"https://t.me/{my_username}" if my_username else f"tg://user?id={my_id}"
        buttons = [[Button.url(f"👤 {my_name}", my_link, style="primary")]]
    
    try:
        await event.edit(buttons=buttons)
        await event.answer(f"✅ تم إضافة إعجابك لـ {user_name}!", alert=True)
    except Exception:
        await event.answer(f"✅ تم إضافة إعجابك لـ {user_name}!", alert=True)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"template_prev")))
async def template_prev(event):
    user_id = event.query.user_id
    current_page = template_pages.get(user_id, 0)
    if current_page > 0:
        template_pages[user_id] = current_page - 1
        await update_template_message(event, user_id)
    else:
        await event.answer("⚠️ هذه هي الكليشة الأولى!", alert=True)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"template_next")))
async def template_next(event):
    user_id = event.query.user_id
    current_page = template_pages.get(user_id, 0)
    total_pages = len(ID_TEMPLATES)
    
    if current_page + 1 < total_pages:
        template_pages[user_id] = current_page + 1
        await update_template_message(event, user_id)
    else:
        await event.answer("⚠️ هذه هي الكليشة الأخيرة!", alert=True)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"template_save_(.+)")))
async def template_save(event):
    match = re.match(r"template_save_(.+)", event.data.decode())
    if not match:
        return
    
    template_key = match.group(1)
    if template_key in ID_TEMPLATES:
        addgvar("SELECTED_ID_TEMPLATE", template_key)
        await event.edit(f"✅ تم حفظ كليشة **{ID_TEMPLATES[template_key]['name']}** بنجاح!\n\n• ستظهر في جميع بطاقات الـ .لايك")
    else:
        await event.answer("❌ كليشة غير موجودة!", alert=True)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"toggle_like_mode")))
async def toggle_like_mode(event):
    current_mode = gvarstatus("LIKE_BUTTON_MODE") or "likes"
    new_mode = "profile" if current_mode == "likes" else "likes"
    addgvar("LIKE_BUTTON_MODE", new_mode)
    
    mode_name = "نمط الحساب" if new_mode == "profile" else "نمط القلوب"
    my_username, my_name, my_id = await get_my_account_info()
    
    text = f"**⚙️ إعدادات زر اللايك**\n\n"
    text += f"• النمط الحالي: **{'❤️ نمط القلوب' if new_mode == 'likes' else '👤 نمط الحساب'}**\n\n"
    text += f"• شكل الزر:\n"
    
    if new_mode == "likes":
        text += f"`ʟɪᴋᴇ ♥️ ⤑ (العدد)`\n"
        text += f"• زر الإعجاب فقط"
    else:
        text += f"`👤 {my_name}`\n"
        text += f"• رابط حسابك فقط"
    
    text += f"\n\n• استخدم الأمر `.نمط اللايك` مرة أخرى للتبديل"
    
    buttons = [
        [Button.inline("🔄 تبديل النمط", data="toggle_like_mode", style="primary")],
        [Button.inline("❌ إغلاق", data="close_panel", style="danger")]
    ]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")
    await event.answer(f"✅ تم التبديل إلى {mode_name}", alert=True)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"close_panel")))
async def close_panel(event):
    """إغلاق القائمة"""
    await event.edit("❌ تم إغلاق القائمة!", buttons=None, parse_mode="Markdown")
