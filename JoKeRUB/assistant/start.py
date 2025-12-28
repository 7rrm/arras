import re
import random
from collections import defaultdict
from datetime import datetime
from typing import Optional, Union

from telethon import Button, events
from telethon.errors import UserIsBlockedError
from telethon.events import CallbackQuery, StopPropagation
from telethon.utils import get_display_name

from . import Config, l313l

from ..core import check_owner, pool
from ..core.logger import logging
from ..core.session import tgbot
from ..helpers import reply_id
from ..helpers.utils import _format
from ..sql_helper.bot_blacklists import check_is_black_list
from ..sql_helper.bot_pms_sql import (
    add_user_to_db,
    get_user_id,
    get_user_logging,
    get_user_reply,
)
from ..sql_helper.bot_starters import add_starter_to_db, get_starter_details
from ..sql_helper.globals import delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID
from .botmanagers import ban_user_from_bot

LOGS = logging.getLogger(__name__)

plugin_category = "utils"
botusername = Config.TG_BOT_USERNAME
Zel_Uid = l313l.uid
dd = []
kk = []
tt = []

class FloodConfig:
    BANNED_USERS = set()
    USERS = defaultdict(list)
    MESSAGES = 3
    SECONDS = 6
    ALERT = defaultdict(dict)
    AUTOBAN = 10

async def check_bot_started_users(user, event):
    if user.id == Config.OWNER_ID:
        return
    check = get_starter_details(user.id)
    usernaam = f"@{user.username}" if user.username else "لايوجـد"
    if check is None:
        start_date = str(datetime.now().strftime("%B %d, %Y"))
        notification = f"**- مرحبـاً سيـدي 🧑🏻‍💻**\
                \n**- شخـص قام بالدخـول لـ البـوت المسـاعـد 💡**\
                \n\n**- الاسـم : **{get_display_name(user)}\
                \n**- الايـدي : **`{user.id}`\
                \n**- اليـوزر :** {usernaam}"
    else:
        start_date = check.date
        notification = f"**- مرحبـاً سيـدي 🧑🏻‍💻**\
                \n**- شخـص قام بالدخـول لـ البـوت المسـاعـد 💡**\
                \n\n**- الاسـم : **{get_display_name(user)}\
                \n**- الايـدي : **`{user.id}`\
                \n**- اليـوزر :** {usernaam}"
    try:
        add_starter_to_db(user.id, get_display_name(user), start_date, user.username)
    except Exception as e:
        LOGS.error(str(e))
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, notification)



@l313l.bot_cmd(
    pattern=f"^/start({botusername})?([\\s]+)?$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def bot_start(event):
    chat = await event.get_chat()
    user = await l313l.get_me()
    if check_is_black_list(chat.id):
        return
    if int(chat.id) in kk:
        kk.remove(int(chat.id))

    if int(chat.id) in dd:
        dd.remove(int(chat.id))
    reply_to = await reply_id(event)
    mention = f"[{chat.first_name}](tg://user?id={chat.id})"
    my_mention = f"[{user.first_name}](tg://user?id={user.id})"
    first = chat.first_name
    last = chat.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{chat.username}" if chat.username else mention
    userid = chat.id
    my_first = user.first_name
    my_last = user.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{user.username}" if user.username else my_mention
    if gvarstatus("START_BUTUN") is not None:
        zz_txt = "⌔ قنـاتـي ⌔"
        zz_ch = gvarstatus("START_BUTUN")
    elif user.username:
        zz_txt = "⌔ لـ التواصـل خـاص ⌔"
        zz_ch = user.username
    else:
        zz_txt = "⌔ قنـاة المـطور ⌔"
        zz_ch = "aqhvv"
    zid = 5427469031
    if gvarstatus("ZThon_Vip") is None:
        zid = 5427469031
    else:
        zid = int(gvarstatus("ZThon_Vip"))
    custompic = gvarstatus("BOT_START_PIC") or None
    if chat.id != Config.OWNER_ID:
        customstrmsg = gvarstatus("START_TEXT") or None
        if customstrmsg is not None:
            start_msg = customstrmsg.format(
                zz_mention=mention,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_zname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
            )
        else:
            start_msg = f"**⌔ مـرحباً بـك عزيـزي  {mention} **\
                        \n\n**⌔ انـا البـوت الخـاص بـ** {my_fullname}\
                        \n**⌔ يمكنك التواصـل مـع مـالكـي مـن هنـا 💌.**\
                        \n**⌔ فقـط ارسـل رسـالتك وانتظـر الـرد 📨.**\
                        \n**⌔ إننـي ايضـاً بـوت زخرفـة 🎨 & حـذف حسابات ⚠️.**\
                        \n**⌔ لـ الزخرفـة او الحـذف استخـدم الازرار بالاسفـل**"
        # ... (الكود السابق يبقى كما هو حتى جزء الأزرار)

        buttons = [
            [
                Button.inline("اضغـط لـ التواصـل 🗳", data="ttk_bot-1")
            ],
            [
                Button.inline("زخـارف تمبلـر 🎡", data="decor_main_menu")
            ],
            [
                Button.inline("لـ حـذف حسـابك ⚠️", data="zzk_bot-5")
            ],
            [
                Button.inline("الأوامـر المدفوعـة 💎", data="paid_commands_menu")
            ],
            [
                Button.url(zz_txt, f"https://t.me/{zz_ch}")
            ]
        ]

# ... (الكود الأوسط يبقى كما هو)
    elif chat.id == Config.OWNER_ID and chat.id == zid:
        customstrmsg = gvarstatus("START_TEXT") or None
        if customstrmsg is not None:
            start_msg = customstrmsg.format(
                zz_mention=mention,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_zname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
            )
        else:
            start_msg = f"**⌔ مـرحباً بـك عزيـزي  {mention} **\
                        \n\n**⌔ انـا البـوت الخـاص بـ** {my_fullname}\
                        \n**⌔ يمكنك التواصـل مـع مـالكـي مـن هنـا 💌.**\
                        \n**⌔ فقـط ارسـل رسـالتك وانتظـر الـرد 📨.**\
                        \n**⌔ إننـي ايضـاً بـوت زخرفـة 🎨 & حـذف حسابات ⚠️.**\
                        \n**⌔ لـ الزخرفـة او الحـذف استخـدم الازرار بالاسفـل**"
        buttons = [
            [
             Button.inline("زخـارف تمبلـر 🎡", data="decor_main_menu")
            ],
            [
                Button.inline("لـ حـذف حسـابك ⚠️", data="zzk_bot-5")
            ],
            [
                Button.inline("الأوامـر المدفوعـة 💎", data="paid_commands_menu")
            ],
            [
                Button.url(zz_txt, f"https://t.me/{zz_ch}")
            ]
        ]
    else:
        start_msg = "**⌔ مـرحبـاً عـزيـزي المـالك 🧑🏻‍💻..**\n**⌔ انا البـوت المسـاعـد الخـاص بـك (تواصـل📨 + زخرفـه🎨) 🤖🦾**\n**⌔ يستطيـع اي شخص التواصل بك من خـلالي 💌**\n\n**⌔ لـ زخرفـة اسـم اضغـط الـزر بالاسفـل**\n**⌔ لرؤيـة اوامـري الخاصـه بـك اضغـط :  /help **"
        buttons = [
            [
                Button.inline("زخـارف تمبلـر 🎡", data="decor_main_menu")
            ],
            [
                Button.inline("حـذف حسـابك ⚠️", data="zzk_bot-5")
            ],
            [
                Button.inline("الأوامـر المدفوعـة 💎", data="paid_commands_menu")
            ]
        ]
    try:
        if custompic:
            await event.client.send_file(
                chat.id,
                file=custompic,
                caption=start_msg,
                link_preview=False,
                buttons=buttons,
                reply_to=reply_to,
            )
        else:
            await event.client.send_message(
                chat.id,
                start_msg,
                link_preview=False,
                buttons=buttons,
                reply_to=reply_to,
            )
    except Exception as e:
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"** - سيـدي المطـور 🧑🏻‍💻**\n**- حـدث خطـأ عنـد اشتـراك احـد الاشخـاص فـي البـوت المسـاعـد ؟!**.\\\x1f                \n`{e}`",
            )

    else:
        await check_bot_started_users(chat, event)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"paid_commands_menu$")))
async def paid_commands_menu_handler(event):
    await event.edit(
        """**• مـرحبـاً بـك عـزيـزي 💎**
        
• **فـي قسـم الأوامـر المدفوعـة**
• هـذه الأوامـر تـم تطويرها خصيصـاً
﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎
• **استخـدم الأزرار بالأسفـل**""",
        buttons=[
            [
                Button.inline("هـاك تيرمكـس ⚓", data="termux_hack")
            ],
            [
                Button.inline("تـعديل وانشاء الصـور 🖼", data="edit_photo")
            ],
            [
                Button.inline("رجــوع ↩️", data="styleback")
            ],
        ],
        link_preview=False
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"termux_hack$")))
async def termux_hack_handler(event):
    user_id = event.query.user_id
    
    # للمالك فقط يمكنه استخدام الخدمة
    if user_id == Config.OWNER_ID:
        await event.edit(
            "**- مرحـبا بك عزيزي المـالك **\n"
            "**- في قسم اختراق تيرمكس **\n"
            "**- لرؤية أوامـر الإختراق أرسل** /hack",
            buttons=[
                [Button.inline("رجوع", data="paid_commands_menu")]
            ]
        )
    else:
        # للمستخدمين الآخرين: رسالة الخدمة المدفوعة
        await event.edit(
            "• عـذراً .. عـزيـزي 🙇🏻‍♀\n"
            "• هـذا القسم خاص بمالك البوت فقط 🚧\n"
            "• لـ تنصيب بـوت مماثـل\n"
            "• تواصـل مع المـطور **آراس**\n"
            "• @Lx5x5",
            buttons=[
                [Button.inline("رجوع", data="paid_commands_menu")]
            ]
        )

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"edit_photo$")))
async def edit_photo_handler(event):
    user_id = event.query.user_id
    
    # للمالك فقط يمكنه استخدام الخدمة
    if user_id == Config.OWNER_ID:
        await event.edit(
            "**- مرحـبا بك عزيزي المـالك **\n"
            "**- في قسم تعديل وإنشاء الصور **\n"
            "**- لرؤية أوامـر التعديل إرسل** /edit",
            buttons=[
                [Button.inline("رجوع", data="paid_commands_menu")]
            ]
        )
    else:
        # للمستخدمين الآخرين: رسالة الخدمة المدفوعة
        await event.edit(
            "• عـذراً .. عـزيـزي 🙇🏻‍♀\n"
            "• هـذا القسم خاص بمالك البوت فقط 🚧\n"
            "• لـ تنصيب بـوت مماثـل\n"
            "• تواصـل مع المـطور **آراس**\n"
            "• @Lx5x5",
            buttons=[
                [Button.inline("رجوع", data="paid_commands_menu")]
            ]
        )

@l313l.bot_cmd(incoming=True, func=lambda e: e.is_private)
async def bot_pms(event):  # sourcery no-metrics
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    if check_is_black_list(chat.id):
        return
    if event.contact or int(chat.id) in kk:
        return
    if chat.id != Config.OWNER_ID:
        if event.text.startswith("/cancle"):
            if int(chat.id) in dd:
                dd.remove(int(chat.id))
            if int(chat.id) in kk:
                kk.remove(int(chat.id))
            zzc = "**- تم الالغـاء .. بنجـاح**"
            return await event.client.send_message(
                chat.id,
                zzc,
                link_preview=False,
                reply_to=reply_to,
            )
        if chat.id in dd:
            text = event.text
            iitems = ['࿐', '𖣳', '𓃠', '𖡟', '𖠜', '‌♡⁩', '‌༗', '‌𖢖', '❥', '‌ঌ', '𝆹𝅥𝅮', '𖠜', '𖠲', '𖤍', '𖠛', ' 𝅘𝅥𝅮', '‌༒', '‌ㇱ', '߷', 'メ', '〠', '𓃬', '𖠄']
            smiile1 = random.choice(iitems)
            smiile2 = random.choice(iitems)
            smiile3 = random.choice(iitems)
            smiile4 = random.choice(iitems)
            smiile5 = random.choice(iitems)
            smiile6 = random.choice(iitems)
            smiile7 = random.choice(iitems)
            smiile8 = random.choice(iitems)
            smiile9 = random.choice(iitems)
            smiile10 = random.choice(iitems)
            smiile11 = random.choice(iitems)
            smiile12 = random.choice(iitems)
            smiile13 = random.choice(iitems)
            smiile14 = random.choice(iitems)
            smiile15 = random.choice(iitems)
            smiile16 = random.choice(iitems)
            smiile17 = random.choice(iitems)
            smiile18 = random.choice(iitems)
            smiile19 = random.choice(iitems)
            smiile20 = random.choice(iitems)
            smiile21 = random.choice(iitems)
            smiile22 = random.choice(iitems)
            smiile23 = random.choice(iitems)
            smiile24 = random.choice(iitems)
            smiile25 = random.choice(iitems)
            smiile26 = random.choice(iitems)
            smiile27 = random.choice(iitems)
            smiile28 = random.choice(iitems)
            smiile29 = random.choice(iitems)
            smiile30 = random.choice(iitems)
            smiile31 = random.choice(iitems)
            smiile32 = random.choice(iitems)
            smiile33 = random.choice(iitems)
            smiile34 = random.choice(iitems)
            smiile35 = random.choice(iitems)
            smiile36 = random.choice(iitems)
            smiile37 = random.choice(iitems)

            WA1 = text.replace('a', 'ᵃ').replace('A', 'ᴬ').replace('b', 'ᵇ').replace('B', 'ᴮ').replace('c', 'ᶜ').replace('C', 'ᶜ').replace('d', 'ᵈ').replace('D', 'ᴰ').replace('e', 'ᵉ').replace('E', 'ᴱ').replace('f', 'ᶠ').replace('F', 'ᶠ').replace('g', 'ᵍ').replace('G', 'ᴳ').replace('h', 'ʰ').replace('H', 'ᴴ').replace('i', 'ⁱ').replace('I', 'ᴵ').replace('j', 'ʲ').replace('J', 'ᴶ').replace('k', 'ᵏ').replace('K', 'ᴷ').replace('l', 'ˡ').replace('L', 'ᴸ').replace('m', 'ᵐ').replace('M', 'ᴹ').replace('n', 'ⁿ').replace('N', 'ᴺ').replace('o', 'ᵒ').replace('O', 'ᴼ').replace('p', 'ᵖ').replace('P', 'ᴾ').replace('q', '۩').replace('Q', 'Q').replace('r', 'ʳ').replace('R', 'ᴿ').replace('s', 'ˢ').replace('S', 'ˢ').replace('t', 'ᵗ').replace('T', 'ᵀ').replace('u', 'ᵘ').replace('U', 'ᵁ').replace('v', 'ⱽ').replace('V', 'ⱽ').replace('w', 'ʷ').replace('W', 'ᵂ').replace('x', 'ˣ').replace('X', 'ˣ').replace('y', 'ʸ').replace('Y', 'ʸ').replace('z', 'ᶻ').replace('Z', 'ᶻ')
            WA2 = text.replace('a', 'ᴀ').replace('b', 'ʙ').replace('c', 'ᴄ').replace('d', 'ᴅ').replace('e', 'ᴇ').replace('f', 'ғ').replace('g', 'ɢ').replace('h', 'ʜ').replace('i', 'ɪ').replace('j', 'ᴊ').replace('k', 'ᴋ').replace('l', 'ʟ').replace('m', 'ᴍ').replace('n', 'ɴ').replace('o', 'ᴏ').replace('p', 'ᴘ').replace('q', 'ǫ').replace('r', 'ʀ').replace('s', 's').replace('t', 'ᴛ').replace('u', 'ᴜ').replace('v', 'ᴠ').replace('w', 'ᴡ').replace('x', 'x').replace('y', 'ʏ').replace('z', 'ᴢ').replace('A', 'ᴀ').replace('B', 'ʙ').replace('C', 'ᴄ').replace('D', 'ᴅ').replace('E', 'ᴇ').replace('F', 'ғ').replace('G', 'ɢ').replace('H', 'ʜ').replace('I', 'ɪ').replace('J', 'ᴊ').replace('K', 'ᴋ').replace('L', 'ʟ').replace('M', 'ᴍ').replace('N', 'ɴ').replace('O', 'ᴏ').replace('P', 'ᴘ').replace('Q', 'ǫ').replace('R', 'ʀ').replace('S', 'S').replace('T', 'ᴛ').replace('U', 'ᴜ').replace('V', 'ᴠ').replace('W', 'ᴡ').replace('X', 'X').replace('Y', 'ʏ').replace('Z', 'ᴢ')
            WA3 = text.replace('a','α').replace("b","в").replace("c","c").replace("d","∂").replace("e","ε").replace("E","ғ").replace("g","g").replace("h","н").replace("i","ι").replace("j","נ").replace("k","к").replace("l","ℓ").replace("m","м").replace("n","η").replace("o","σ").replace("p","ρ").replace("q","q").replace("r","я").replace("s","s").replace("t","т").replace("u","υ").replace("v","v").replace("w","ω").replace("x","x").replace("y","ү").replace("z","z").replace("A","α").replace("B","в").replace("C","c").replace("D","∂").replace("E","ε").replace("E","ғ").replace("G","g").replace("H","н").replace("I","ι").replace("J","נ").replace("K","к").replace("L","ℓ").replace("M","м").replace("N","η").replace("O","σ").replace("P","ρ").replace("Q","q").replace("R","я").replace("S","s").replace("T","т").replace("U","υ").replace("V","v").replace("W","ω").replace("X","X").replace("Y","ү").replace("Z","z")
            WA4 = text.replace('a','𝙰') .replace('b','𝙱') .replace('c','𝙲') .replace('d','𝙳') .replace('e','𝙴') .replace('f','𝙵') .replace('g','𝙶') .replace('h','𝙷') .replace('i','𝙸') .replace('j','𝚓') .replace('k','𝙺') .replace('l','𝙻') .replace('m','𝙼') .replace('n','𝙽') .replace('o','𝙾') .replace('p','𝙿') .replace('q','𝚀') .replace('r','𝚁') .replace('s','𝚂') .replace('t','𝚃') .replace('u','𝚄') .replace('v','??') .replace('w','𝚆') .replace('x','𝚇') .replace('y','𝚈') .replace('z','𝚉').replace('A','𝙰') .replace('B','𝙱') .replace('C','𝙲') .replace('D','𝙳') .replace('E','𝙴') .replace('F','𝙵') .replace('G','𝙶') .replace('H','𝙷') .replace('I','𝙸') .replace('J','𝚓') .replace('K','𝙺') .replace('L','𝙻') .replace('M','𝙼') .replace('N','𝙽') .replace('O','𝙾') .replace('P','𝙿') .replace('Q','𝚀') .replace('R','𝚁') .replace('S','𝚂') .replace('T','𝚃') .replace('U','𝚄') .replace('V','𝚅') .replace('W','𝚆') .replace('X','𝚇') .replace('Y','𝚈') .replace('Z','𝚉')
            WA5 = text.replace('a','🇦 ').replace("b","🇧 ").replace("c","🇨 ").replace("d","🇩 ").replace("e","🇪 ").replace("f","🇫 ").replace("g","🇬 ").replace("h","🇭 ").replace("i","🇮 ").replace("j","🇯 ").replace("k","🇰 ").replace("l","🇱 ").replace("m","🇲 ").replace("n","🇳 ").replace("o","🇴 ").replace("p","🇵 ").replace("q","🇶 ").replace("r","🇷 ").replace("s","🇸 ").replace("t","🇹 ").replace("u","🇻 ").replace("v","🇺 ").replace("w","🇼 ").replace("x","🇽 ").replace("y","🇾 ").replace("z","🇿 ").replace("A","🇦 ").replace("B","🇧 ").replace("C","🇨 ").replace("D","🇩 ").replace("E","🇪 ").replace("F","🇫 ").replace("G","🇬 ").replace("H","🇭 ").replace("I","🇮 ").replace("J","🇯 ").replace("K","🇰 ").replace("L","🇱 ").replace("M","🇲 ").replace("N","🇳 ").replace("O","🇴 ").replace("P","🇵 ").replace("Q","🇶 ").replace("R","🇷 ").replace("S","🇸 ").replace("T","🇹 ").replace("U","🇻 ").replace("V","🇺 ").replace("W","🇼 ").replace("X","🇽 ").replace("Y","🇾 ").replace("Z","🇿 ")
            WA6 = text.replace('a','ⓐ').replace("b","ⓑ").replace("c","ⓒ").replace("d","ⓓ").replace("e","ⓔ").replace("f","ⓕ").replace("g","ⓖ").replace("h","ⓗ").replace("i","ⓘ").replace("j","ⓙ").replace("k","ⓚ").replace("l","ⓛ").replace("m","ⓜ").replace("n","ⓝ").replace("o","ⓞ").replace("p","ⓟ").replace("q","ⓠ").replace("r","ⓡ").replace("s","ⓢ").replace("t","ⓣ").replace("u","ⓤ").replace("v","ⓥ").replace("w","ⓦ").replace("x","ⓧ").replace("y","ⓨ").replace("z","ⓩ").replace("A","Ⓐ").replace("B","Ⓑ").replace("C","Ⓒ").replace("D","Ⓓ").replace("E","Ⓔ").replace("F","Ⓕ").replace("G","Ⓖ").replace("H","Ⓗ").replace("I","Ⓘ").replace("J","Ⓙ").replace("K","Ⓚ").replace("L","Ⓛ").replace("M","🄼").replace("N","Ⓝ").replace("O","Ⓞ").replace("P","Ⓟ").replace("Q","Ⓠ").replace("R","Ⓡ").replace("S","Ⓢ").replace("T","Ⓣ").replace("U","Ⓤ").replace("V","Ⓥ").replace("W","Ⓦ").replace("X","Ⓧ").replace("Y","Ⓨ").replace("Z","Ⓩ")
            WA7 = text.replace('a','🅐').replace("b","🅑").replace("c","🅒").replace("d","🅓").replace("e","🅔").replace("f","🅕").replace("g","🅖").replace("h","🅗").replace("i","🅘").replace("j","🅙").replace("k","🅚").replace("l","🅛").replace("m","🅜").replace("n","🅝").replace("o","🅞").replace("p","🅟").replace("q","🅠").replace("r","🅡").replace("s","🅢").replace("t","🅣").replace("u","🅤").replace("v","🅥").replace("w","🅦").replace("x","🅧").replace("y","🅨").replace("z","🅩").replace("A","🅐").replace("B","🅑").replace("C","🅒").replace("D","🅓").replace("E","🅔").replace("F","🅕").replace("G","🅖").replace("H","🅗").replace("I","🅘").replace("J","🅙").replace("K","🅚").replace("L","🅛").replace("M","🅜").replace("N","🅝").replace("O","🅞").replace("P","🅟").replace("Q","🅠").replace("R","🅡").replace("S","🅢").replace("T","🅣").replace("U","🅤").replace("V","🅥").replace("W","🅦").replace("X","🅧").replace("Y","🅨").replace("Z","🅩")
            WA8 = text.replace('a','🄰').replace("b","🄱").replace("c","🄲").replace("d","🄳").replace("e","🄴").replace("f","🄵").replace("g","🄶").replace("h","🄷").replace("i","🄸").replace("j","🄹").replace("k","🄺").replace("l","🄻").replace("m","🄼").replace("n","🄽").replace("o","🄾").replace("p","🄿").replace("q","🅀").replace("r","🅁").replace("s","🅂").replace("t","🅃").replace("u","🅄").replace("v","🅅").replace("w","🅆").replace("x","🅇").replace("y","🅈").replace("z","🅉").replace("A","🄰").replace("B","🄱").replace("C","🄲").replace("D","🄳").replace("E","🄴").replace("F","🄵").replace("G","🄶").replace("H","🄷").replace("I","🄸").replace("J","🄹").replace("K","🄺").replace("L","🄻").replace("M","🄼").replace("N","🄽").replace("O","🄾").replace("P","🄿").replace("Q","🅀").replace("R","🅁").replace("S","🅂").replace("T","🅃").replace("U","🅄").replace("V","🅅").replace("W","🅆").replace("X","🅇").replace("Y","🅈").replace("Z","🅉")
            WA9 = text.replace('a','🅐').replace("b","🅑").replace("c","🅲").replace("d","🅳").replace("e","🅴").replace("f","🅵").replace("g","🅶").replace("h","🅷").replace("i","🅸").replace("j","🅹").replace("k","🅺").replace("l","🅻").replace("m","🅼").replace("n","🅽").replace("o","🅞").replace("p","🅟").replace("q","🆀").replace("r","🆁").replace("s","🆂").replace("t","🆃").replace("u","🆄").replace("v","🆅").replace("w","🆆").replace("x","🆇").replace("y","🆈").replace("z","🆉").replace("A","🅐").replace("B","🅑").replace("C","🅲").replace("D","🅳").replace("E","🅴").replace("F","🅵").replace("G","🅶").replace("H","🅷").replace("I","🅸").replace("J","🅹").replace("K","🅺").replace("L","🅻").replace("M","🅼").replace("N","🅽").replace("O","🅞").replace("P","🅟").replace("Q","🆀").replace("R","🆁").replace("S","🆂").replace("T","🆃").replace("U","🆄").replace("V","🆅").replace("W","🆆").replace("X","🆇").replace("Y","🆈").replace("Z","🆉")
            WA10 = text.replace('a','𝘢') .replace('b','𝘣') .replace('c','𝘤') .replace('d','𝘥') .replace('e','𝘦') .replace('f','𝘧') .replace('g','𝘨') .replace('h','𝘩') .replace('i','𝘪') .replace('j','𝘫') .replace('k','𝘬') .replace('l','𝘭') .replace('m','𝘮') .replace('n','𝘯') .replace('o','𝘰') .replace('p','𝘱') .replace('q','𝘲') .replace('r','𝘳') .replace('s','𝘴') .replace('t','𝘵') .replace('u','𝘶') .replace('v','𝘷') .replace('w','𝘸') .replace('x','𝘹') .replace('y','𝘺') .replace('z','𝘻').replace('A','𝘢') .replace('B','𝘣') .replace('C','𝘤') .replace('D','𝘥') .replace('E','𝘦') .replace('F','𝘧') .replace('G','𝘨') .replace('H','𝘩') .replace('I','𝘪') .replace('J','𝘫') .replace('K','𝘬') .replace('L','𝘭') .replace('M','𝘮') .replace('N','𝘯') .replace('O','𝘰') .replace('P','𝘱') .replace('Q','𝘲') .replace('R','𝘳') .replace('S','𝘴') .replace('T','𝘵') .replace('U','𝘶') .replace('V','𝘷') .replace('W','𝘸') .replace('X','𝘹') .replace('Y','𝘺') .replace('Z','𝘻')
            WA11 = text.replace('a','𝘈').replace("b","𝘉").replace("c","𝘊").replace("d","𝘋").replace("e","𝘌").replace("f","𝘍").replace("g","𝘎").replace("h","𝘏").replace("i","𝘐").replace("j","𝘑").replace("k","𝘒").replace("l","𝘓").replace("m","𝘔").replace("n","𝘕").replace("o","𝘖").replace("p","𝘗").replace("q","𝘘").replace("r","𝘙").replace("s","𝘚").replace("t","𝘛").replace("u","𝘜").replace("v","𝘝").replace("w","𝘞").replace("x","𝘟").replace("y","𝘠").replace("z","𝘡").replace("A","𝘈").replace("B","𝘉").replace("C","𝘊").replace("D","𝘋").replace("E","𝘌").replace("F","𝘍").replace("G","𝘎").replace("H","𝘏").replace("I","𝘐").replace("J","𝘑").replace("K","𝘒").replace("L","𝘓").replace("M","𝘔").replace("N","𝘕").replace("O","𝘖").replace("P","𝘗").replace("Q","𝘘").replace("R","𝘙").replace("S","𝘚").replace("T","𝘛").replace("U","𝘜").replace("V","𝘝").replace("W","𝘞").replace("X","𝘟").replace("Y","𝘠").replace("Z","𝘡")
            WA12 = text.replace('a','Ａ').replace('b','Ｂ').replace('c','Ｃ').replace('d','Ｄ').replace('e','Ｅ').replace('f','Ｆ').replace('g','Ｇ').replace('h','Ｈ').replace('i','Ｉ').replace('j','Ｊ').replace('k','Ｋ').replace('l','Ｌ').replace('m','Ｍ').replace('n','Ｎ').replace('o','Ｏ').replace('p','Ｐ').replace('q','Ｑ').replace('r','Ｒ').replace('s','Ｓ').replace('t','Ｔ').replace('u','Ｕ').replace('v','Ｖ').replace('w','Ｗ').replace('x','Ｘ').replace('y','Ｙ').replace('z','Ｚ')
            WA13 = text.replace('a','ًٍَُِّA').replace("b","ًٍَُِّB").replace("c","ًٍَُِّC").replace("d","ًٍَُِّD").replace("e","ًٍَُِّE").replace("f","ًٍَُِّF").replace("g","ًٍَُِّG").replace("h","ًٍَُِّH").replace("i","ًٍَُِّI").replace("j","ًٍَُِّJ").replace("k","ًٍَُِّK").replace("l","ًٍَُِّL").replace("m","ًٍَُِّM").replace("n","ًٍَُِّN").replace("o","ًٍَُِّO").replace("p","ًٍَُِّP").replace("q","ًٍَُِّQ").replace("r","ًٍَُِّR").replace("s","ًٍَُِّS").replace("t","ًٍَُِّT").replace("u","ًٍَُِّU").replace("v","ًٍَُِّV").replace("w","ًٍَُِّW").replace("x","ًٍَُِّX").replace("y","ًٍَُِّY").replace("z","ًٍَُِّZ")
            WA14 = text.replace('a','ᥲ').replace('b','ᗷ').replace('c','ᑕ').replace('d','ᗞ').replace('e','ᗴ').replace('f','ᖴ').replace('g','Ꮐ').replace('h','ᕼ').replace('i','Ꭵ').replace('j','ᒍ').replace('k','Ꮶ').replace('l','ᥣ').replace('m','ᗰ').replace('n','ᑎ').replace('o','ᝪ').replace('p','ᑭ').replace('q','ᑫ').replace('r','ᖇ').replace('s','ᔑ').replace('t','Ꭲ').replace('u','ᑌ').replace('v','ᐯ').replace('w','ᗯ').replace('x','᙭').replace('y','Ꭹ').replace('z','𝖹')
            WA15 = text.replace('a','ᗩ').replace('b','ᗷ').replace('c','ᑕ').replace('d','ᗪ').replace('e','ᗴ').replace('f','ᖴ').replace('g','Ǥ').replace('h','ᕼ').replace('i','Ꮖ').replace('j','ᒎ').replace('k','ᛕ').replace('l','し').replace('m','ᗰ').replace('n','ᑎ').replace('o','ᗝ').replace('p','ᑭ').replace('q','Ɋ').replace('r','ᖇ').replace('s','Տ').replace('t','丅').replace('u','ᑌ').replace('v','ᐯ').replace('w','ᗯ').replace('x','᙭').replace('y','Ƴ').replace('z','乙').replace('A','ᗩ').replace('B','ᗷ').replace('C','ᑕ').replace('D','ᗪ').replace('E','ᗴ').replace('F','ᖴ').replace('G','Ǥ').replace('H','ᕼ').replace('I','Ꮖ').replace('J','ᒎ').replace('L','ᛕ').replace('L','し').replace('M','ᗰ').replace('N','ᑎ').replace('O','ᗝ').replace('P','ᑭ').replace('Q','Ɋ').replace('R','ᖇ').replace('S','Տ').replace('T','丅').replace('U','ᑌ').replace('V','ᐯ').replace('W','ᗯ').replace('X','᙭').replace('Y','Ƴ').replace('Z','乙')
            WA16 = text.replace('a','A̶').replace('b','B̶').replace('c','C̶').replace('d','D̶').replace('e','E̶').replace('f','F̶').replace('g','G̶').replace('h','H̶').replace('i','I̶').replace('j','J̶').replace('k','K̶').replace('l','L̶').replace('m','M̶').replace('n','N̶').replace('o','O̶').replace('p','P̶').replace('q','Q̶').replace('r','R̶').replace('s','S̶').replace('t','T̶').replace('u','U̶').replace('v','V̶').replace('w','W̶').replace('x','X̶').replace('y','Y̶').replace('z','Z̶').replace('A','A̶').replace('B','B̶').replace('C','C̶').replace('D','D̶').replace('E','E̶').replace('F','F̶').replace('G','G̶').replace('H','H̶').replace('I','I̶').replace('J','J̶').replace('K','K̶').replace('L','L̶').replace('M','M̶').replace('N','N̶').replace('O','O̶').replace('P','P̶').replace('Q','Q̶').replace('R','R̶').replace('S','S̶').replace('T','T̶').replace('U','U̶').replace('V','V̶').replace('W','W̶').replace('X','X̶').replace('Y','Y̶').replace('Z','Z̶')
            WA17 = text.replace('a','𝖆') .replace('b','𝖉') .replace('c','𝖈') .replace('d','𝖉') .replace('e','𝖊') .replace('f','𝖋') .replace('g','𝖌') .replace('h','𝖍') .replace('i','𝖎') .replace('j','𝖏') .replace('k','𝖐') .replace('l','𝖑') .replace('m','𝖒') .replace('n','𝖓') .replace('o','𝖔') .replace('p','𝖕') .replace('q','𝖖') .replace('r','𝖗') .replace('s','𝖘') .replace('t','𝖙') .replace('u','𝖚') .replace('v','𝒗') .replace('w','𝒘') .replace('x','𝖝') .replace('y','𝒚') .replace('z','𝒛').replace('A','𝖆') .replace('B','𝖉') .replace('C','𝖈') .replace('D','𝖉') .replace('E','𝖊') .replace('F','𝖋') .replace('G','𝖌') .replace('H','𝖍') .replace('I','𝖎') .replace('J','𝖏') .replace('K','𝖐') .replace('L','𝖑') .replace('M','𝖒') .replace('N','𝖓') .replace('O','𝖔') .replace('P','𝖕') .replace('Q','𝖖') .replace('R','𝖗') .replace('S','𝖘') .replace('T','𝖙') .replace('U','𝖚') .replace('V','𝒗') .replace('W','𝒘') .replace('X','𝖝') .replace('Y','𝒚') .replace('Z','𝒛')
            WA18 = text.replace('a','𝒂') .replace('b','𝒃') .replace('c','𝒄') .replace('d','𝒅') .replace('e','𝒆') .replace('f','𝒇') .replace('g','𝒈') .replace('h','𝒉') .replace('i','𝒊') .replace('j','𝒋') .replace('k','𝒌') .replace('l','𝒍') .replace('m','𝒎') .replace('n','𝒏') .replace('o','𝒐') .replace('p','𝒑') .replace('q','𝒒') .replace('r','𝒓') .replace('s','𝒔') .replace('t','𝒕') .replace('u','𝒖') .replace('v','𝒗') .replace('w','𝒘') .replace('x','𝒙') .replace('y','𝒚') .replace('z','𝒛')
            WA19 = text.replace('a','𝑎') .replace('b','𝑏') .replace('c','𝑐') .replace('d','𝑑') .replace('e','𝑒') .replace('f','𝑓') .replace('g','𝑔') .replace('h','ℎ') .replace('i','𝑖') .replace('j','𝑗') .replace('k','𝑘') .replace('l','𝑙') .replace('m','𝑚') .replace('n','𝑛') .replace('o','𝑜') .replace('p','𝑝') .replace('q','𝑞') .replace('r','𝑟') .replace('s','𝑠') .replace('t','𝑡') .replace('u','𝑢') .replace('v','𝑣') .replace('w','𝑤') .replace('x','𝑥') .replace('y','𝑦') .replace('z','𝑧')
            WA20 = text.replace('a','ꪖ') .replace('b','᥇') .replace('c','ᥴ') .replace('d','ᦔ') .replace('e','ꫀ') .replace('f','ᠻ') .replace('g','ᧁ') .replace('h','ꫝ') .replace('i','𝓲') .replace('j','𝓳') .replace('k','𝘬') .replace('l','ꪶ') .replace('m','ꪑ') .replace('n','ꪀ') .replace('o','ꪮ') .replace('p','ρ') .replace('q','𝘲') .replace('r','𝘳') .replace('s','𝘴') .replace('t','𝓽') .replace('u','ꪊ') .replace('v','ꪜ') .replace('w','᭙') .replace('x','᥊') .replace('y','ꪗ') .replace('z','ɀ').replace('A','ꪖ') .replace('B','᥇') .replace('C','ᥴ') .replace('D','ᦔ') .replace('E','ꫀ') .replace('F','ᠻ') .replace('G','ᧁ') .replace('H','ꫝ') .replace('I','𝓲') .replace('J','𝓳') .replace('K','𝘬') .replace('L','ꪶ') .replace('M','ꪑ') .replace('N','ꪀ') .replace('O','ꪮ') .replace('P','ρ') .replace('Q','𝘲') .replace('R','𝘳') .replace('S','𝘴') .replace('T','𝓽') .replace('U','ꪊ') .replace('V','ꪜ') .replace('W','᭙') .replace('X','᥊') .replace('Y','ꪗ') .replace('Z','ɀ')
            WA21 = text.replace('a','ą').replace('b','ც').replace('c','ƈ').replace('d','ɖ').replace('e','ɛ').replace('f','ʄ').replace('g','ɠ').replace('h','ɧ').replace('i','ı').replace('j','ʝ').replace('k','ƙ').replace('l','Ɩ').replace('m','ɱ').replace('n','ŋ').replace('o','ơ').replace('p','℘').replace('q','զ').replace('r','r').replace('s','ʂ').replace('t','ɬ').replace('u','ų').replace('v','v').replace('w','ῳ').replace('x','ҳ').replace('y','ყ').replace('z','ʑ')
            WA22 = text.replace('a','Δ').replace("b","β").replace("c","૮").replace("d","ᴅ").replace("e","૯").replace("f","ƒ").replace("g","ɢ").replace("h","み").replace("i","เ").replace("j","ʝ").replace("k","ҡ").replace("l","ɭ").replace("m","ണ").replace("n","ท").replace("o","๏").replace("p","ρ").replace("q","ǫ").replace("r","ʀ").replace("s","ઽ").replace("t","τ").replace("u","υ").replace("v","ѵ").replace("w","ω").replace("x","ﾒ").replace("y","ყ").replace("z","ʑ")
            WA23 = text.replace('a','ᕱ').replace("b","β").replace("c","૮").replace("d","Ɗ").replace("e","ξ").replace("f","ƒ").replace("g","Ǥ").replace("h","ƕ").replace("i","Ĩ").replace("j","ʝ").replace("k","Ƙ").replace("l","Ꮭ").replace("m","ണ").replace("n","ท").replace("o","♡").replace("p","Ƥ").replace("q","𝑄").replace("r","Ꮢ").replace("s","Ƨ").replace("t","Ƭ").replace("u","Ꮜ").replace("v","ѵ").replace("w","ẁ́̀́").replace("x","ﾒ").replace("y","ɣ").replace("z","ʑ")
            WA24 = text.replace('a','A꯭').replace("b","B꯭").replace("c","C꯭").replace("d","D꯭").replace("e","E꯭").replace("f","F꯭").replace("g","G꯭").replace("h","H꯭").replace("i","I꯭").replace("j","J꯭").replace("k","K꯭").replace("l","L꯭").replace("m","M꯭").replace("n","N꯭").replace("o","O꯭").replace("p","P꯭").replace("q","Q꯭").replace("r","R꯭").replace("s","S꯭").replace("t","T꯭").replace("u","U꯭").replace("v","V꯭").replace("w","W꯭").replace("x","X꯭").replace("y","Y꯭").replace("z","Z꯭").replace('A','A꯭').replace("B","B꯭").replace("C","C꯭").replace("D","D꯭").replace("E","E꯭").replace("F","F꯭").replace("G","G꯭").replace("H","H꯭").replace("I","I꯭").replace("J","J꯭").replace("K","K꯭").replace("L","L꯭").replace("M","M꯭").replace("N","N꯭").replace("O","O꯭").replace("P","P꯭").replace("Q","Q꯭").replace("R","R꯭").replace("S","S꯭").replace("T","T꯭").replace("U","U꯭").replace("V","V꯭").replace("W","W꯭").replace("X","X꯭").replace("Y","Y꯭").replace("Z","Z꯭")
            WA25 = text.replace('a', '[̲̅a̲̅]').replace('b', '[̲̅b̲̅]').replace('c', '[̲̅c̲̅]').replace('d', '[̲̅d̲̅]').replace('e', '[̲̅e̲̅]').replace('f', '[̲̅f̲̅]').replace('g', '[̲̅g̲̅]').replace('h', '[̲̅h̲̅]').replace('i', '[̲̅i̲̅]').replace('j', '[̲̅j̲̅]').replace('k', '[̲̅k̲̅]').replace('l', '[̲̅l̲̅]').replace('m', '[̲̅m̲̅]').replace('n', '[̲̅n̲̅]').replace('o', '[̲̅o̲̅]').replace('p', '[̲̅p̲̅]').replace('q', '[̲̅q̲̅]').replace('r', '[̲̅r̲̅]').replace('s', '[̲̅s̲̅]').replace('t', '[̲̅t̲̅]').replace('u', '[̲̅u̲̅]').replace('v', '[̲̅v̲̅]').replace('w', '[̲̅w̲̅]').replace('x', '[̲̅x̲̅]').replace('y', '[̲̅y̲̅]').replace('z', '[̲̅z̲̅]').replace('A', '[̲̅A̲̅]').replace('B', '[̲̅B̲̅]').replace('C', '[̲̅C̲̅]').replace('D', '[̲̅D̲̅]').replace('E', '[̲̅E̲̅]').replace('F', '[̲̅F̲̅]').replace('G', '[̲̅G̲̅]').replace('H', '[̲̅H̲̅]').replace('I', '[̲̅I̲̅]').replace('J', '[̲̅J̲̅]').replace('K', '[̲̅K̲̅]').replace('L', '[̲̅L̲̅]').replace('M', '[̲̅M̲̅]').replace('N', '[̲̅N̲̅]').replace('O', '[̲̅O̲̅]').replace('P', '[̲̅P̲̅]').replace('Q', '[̲̅Q̲̅]').replace('R', '[̲̅R̲̅]').replace('S', '[̲̅S̲̅]').replace('T', '[̲̅T̲̅]').replace('U', '[̲̅U̲̅]').replace('V', '[̲̅V̲̅]').replace('W', '[̲̅W̲̅]').replace('X', '[̲̅X̲̅]').replace('Y', '[̲̅Y̲̅]').replace('Z', '[̲̅Z̲̅]')
            WA26 = text.replace('a','𝔄').replace("b","𝔅").replace("c","ℭ").replace("d","𝔇").replace("e","𝔈").replace("f","𝔉").replace("g","𝔊").replace("h","ℌ").replace("i","ℑ").replace("j","𝔍").replace("k","𝔎").replace("l","𝔏").replace("m","𝔐").replace("n","𝔑").replace("o","𝔒").replace("p","𝔓").replace("q","𝔔").replace("r","ℜ").replace("s","𝔖").replace("t","𝔗").replace("u","𝔘").replace("v","𝔙").replace("w","𝔚").replace("x","𝔛").replace("y","𝔜").replace("z","ℨ").replace("A","𝔄").replace("B","𝔅").replace("C","ℭ").replace("D","𝔇").replace("E","𝔈").replace("F","𝔉").replace("G","𝔊").replace("H","ℌ").replace("I","ℑ").replace("J","𝔍").replace("K","??").replace("L","𝔏").replace("M","𝔐").replace("N","𝔑").replace("O","𝔒").replace("P","𝔓").replace("Q","𝔔").replace("R","ℜ").replace("S","𝔖").replace("T","𝔗").replace("U","𝔘").replace("V","𝔙").replace("W","𝔚").replace("X","𝔛").replace("Y","𝔜").replace("Z","ℨ")
            WA27 = text.replace('a','𝕬').replace("b","𝕭").replace("c","𝕮").replace("d","𝕯").replace("e","𝕰").replace("f","𝕱").replace("g","𝕲").replace("h","𝕳").replace("i","𝕴").replace("j","𝕵").replace("k","𝕶").replace("l","𝕷").replace("m","𝕸").replace("n","𝕹").replace("o","𝕺").replace("p","𝕻").replace("q","𝕼").replace("r","𝕽").replace("s","𝕾").replace("t","𝕿").replace("u","𝖀").replace("v","𝖁").replace("w","𝖂").replace("x","𝖃").replace("y","𝖄").replace("z","𝖅").replace("A","𝕬").replace("B","𝕭").replace("C","𝕮").replace("D","𝕯").replace("E","𝕰").replace("F","𝕱").replace("G","𝕲").replace("H","𝕳").replace("I","𝕴").replace("J","𝕵").replace("K","𝕶").replace("L","𝕷").replace("M","𝕸").replace("N","𝕹").replace("O","𝕺").replace("P","𝕻").replace("Q","𝕼").replace("R","𝕽").replace("S","𝕾").replace("T","𝕿").replace("U","𝖀").replace("V","𝖁").replace("W","𝖂").replace("X","𝖃").replace("Y","𝖄").replace("Z","𝖅")
            WA28 = text.replace('a','𝔸').replace("b","𝔹").replace("c","ℂ").replace("d","𝔻").replace("e","𝔼").replace("f","𝔽").replace("g","𝔾").replace("h","ℍ").replace("i","𝕀").replace("j","𝕁").replace("k","𝕂").replace("l","𝕃").replace("m","𝕄").replace("n","ℕ").replace("o","𝕆").replace("p","ℙ").replace("q","ℚ").replace("r","ℝ").replace("s","𝕊").replace("t","𝕋").replace("u","𝕌").replace("v","𝕍").replace("w","𝕎").replace("x","𝕏").replace("y","𝕐").replace("z","ℤ").replace("A","𝔸").replace("B","𝔹").replace("C","ℂ").replace("D","𝔻").replace("E","𝔼").replace("F","𝔽").replace("G","𝔾").replace("H","ℍ").replace("I","𝕀").replace("J","𝕁").replace("K","𝕂").replace("L","𝕃").replace("M","𝕄").replace("N","ℕ").replace("O","𝕆").replace("P","ℙ").replace("Q","ℚ").replace("R","ℝ").replace("S","𝕊").replace("T","𝕋").replace("U","𝕌").replace("V","𝕍").replace("W","𝕎").replace("X","𝕏").replace("Y","𝕐").replace("Z","ℤ")
            WA29 = text.replace('a','░a░').replace("b","░b░").replace("c","░c░").replace("d","░d░").replace("e","░e░").replace("f","░f░").replace("g","░g░").replace("h","░h░").replace("i","░i░").replace("j","░j░").replace("k","░k░").replace("l","░l░").replace("m","░m░").replace("n","░n░").replace("o","░o░").replace("p","░p░").replace("q","░q░").replace("r","░r░").replace("s","░s░").replace("t","░t░").replace("u","░u░").replace("v","░v░").replace("w","░w░").replace("x","░x░").replace("y","░y░").replace("z","░z░").replace("A","░A░").replace("B","░B░").replace("C","░C░").replace("D","░D░").replace("E","░E░").replace("F","░F░").replace("G","░G░").replace("H","░H░").replace("I","░I░").replace("J","░J░").replace("K","░K░").replace("L","░L░").replace("M","░M░").replace("N","░N░").replace("O","░O░").replace("P","░P░").replace("Q","░Q░").replace("R","░R░").replace("S","░S░").replace("T","░T░").replace("U","░U░").replace("V","░V░").replace("W","░W░").replace("X","░X░").replace("Y","░Y░").replace("Z","░Z░")
            WA30 = text.replace('a','𝐚').replace("b","𝐛").replace("c","𝐜").replace("d","𝐝").replace("e","𝐞").replace("f","𝐟").replace("g","𝐠").replace("h","𝐡").replace("i","𝐢").replace("j","𝐣").replace("k","𝐤").replace("l","𝐥").replace("m","𝐦").replace("n","𝐧").replace("o","𝐨").replace("p","𝐩").replace("q","𝐪").replace("r","𝐫").replace("s","𝐬").replace("t","𝐭").replace("u","𝐮").replace("v","𝐯").replace("w","𝐰").replace("x","𝐱").replace("y","𝐲").replace("z","𝐳").replace("A","𝐚").replace("B","𝐛").replace("C","𝐜").replace("D","𝐝").replace("E","𝐞").replace("F","𝐟").replace("G","𝐠").replace("H","𝐡").replace("I","𝐢").replace("J","𝐣").replace("K","𝐤").replace("L","𝐥").replace("M","𝐦").replace("N","𝐧").replace("O","𝐨").replace("P","𝐩").replace("Q","𝐪").replace("R","𝐫").replace("S","𝐬").replace("T","𝐭").replace("U","𝐮").replace("V","𝐯").replace("W","𝐰").replace("X","𝐱").replace("Y","𝐲").replace("Z","𝐳")
            WA31 = text.replace('a','𝒂').replace("b","𝒃").replace("c","𝒄").replace("d","𝒅").replace("e","𝒆").replace("f","𝒇").replace("g","𝒈").replace("h","𝒉").replace("i","𝒊").replace("j","𝒋").replace("k","𝒌").replace("l","𝒍").replace("m","𝒎").replace("n","𝒏").replace("o","𝒐").replace("p","𝒑").replace("q","𝒒").replace("r","𝒓").replace("s","𝒔").replace("t","𝒕").replace("u","𝒖").replace("v","𝒗").replace("w","𝒘").replace("x","𝒙").replace("y","𝒚").replace("z","𝒛").replace("A","𝒂").replace("B","𝒃").replace("C","𝒄").replace("D","𝒅").replace("E","𝒆").replace("F","𝒇").replace("G","𝒈").replace("H","𝒉").replace("I","𝒊").replace("J","𝒋").replace("K","𝒌").replace("L","𝒍").replace("M","𝒎").replace("N","𝒏").replace("O","𝒐").replace("P","𝒑").replace("Q","𝒒").replace("R","𝒓").replace("S","𝒔").replace("T","𝒕").replace("U","𝒖").replace("V","𝒗").replace("W","𝒘").replace("X","𝒙").replace("Y","𝒚").replace("Z","𝒛")
            WA32 = text.replace('a','𝗮').replace("b","𝗯").replace("c","𝗰").replace("d","𝗱").replace("e","𝗲").replace("f","𝗳").replace("g","𝗴").replace("h","𝗵").replace("i","𝗶").replace("j","𝗷").replace("k","𝗸").replace("l","𝗹").replace("m","𝗺").replace("n","𝗻").replace("o","𝗼").replace("p","𝗽").replace("q","𝗾").replace("r","𝗿").replace("s","𝘀").replace("t","𝘁").replace("u","𝘂").replace("v","𝘃").replace("w","𝘄").replace("x","𝘅").replace("y","𝘆").replace("z","𝘇").replace("A","𝗔").replace("B","𝗕").replace("C","𝗖").replace("D","𝗗").replace("E","𝗘").replace("F","𝗙").replace("G","𝗚").replace("H","𝗛").replace("I","𝗜").replace("J","𝗝").replace("K","𝗞").replace("L","𝗟").replace("M","𝗠").replace("N","𝗡").replace("O","𝗢").replace("P","𝗣").replace("Q","𝗤").replace("R","𝗥").replace("S","𝗦").replace("T","𝗧").replace("U","𝗨").replace("V","𝗩").replace("W","𝗪").replace("X","𝗫").replace("Y","𝗬").replace("Z","𝗭")
            WA33 = text.replace('a','𝙖').replace("b","𝙗").replace("c","𝙘").replace("d","𝙙").replace("e","𝙚").replace("f","𝙛").replace("g","𝙜").replace("h","𝙝").replace("i","𝙞").replace("j","𝙟").replace("k","𝙠").replace("l","𝙡").replace("m","𝙢").replace("n","𝙣").replace("o","𝙤").replace("p","𝙥").replace("q","𝙦").replace("r","𝙧").replace("s","𝙨").replace("t","𝙩").replace("u","𝙪").replace("v","𝙫").replace("w","𝙬").replace("x","𝙭").replace("y","𝙮").replace("z","𝙯").replace("A","𝙖").replace("B","𝙗").replace("C","𝙘").replace("D","𝙙").replace("E","𝙚").replace("F","𝙛").replace("G","𝙜").replace("H","𝙝").replace("I","𝙞").replace("J","𝙟").replace("K","𝙠").replace("L","𝙡").replace("M","𝙢").replace("N","𝙣").replace("O","𝙤").replace("P","𝙥").replace("Q","𝙦").replace("R","𝙧").replace("S","𝙨").replace("T","𝙩").replace("U","𝙪").replace("V","𝙫").replace("W","𝙬").replace("X","𝙭").replace("Y","𝙮").replace("Z","𝙯")
            WA34 = text.replace('a','𝐀').replace("b","𝐁").replace("c","𝐂").replace("d","𝐃").replace("e","𝐄").replace("f","𝐅").replace("g","𝐆").replace("h","𝐇").replace("i","𝐈").replace("j","𝐉").replace("k","𝐊").replace("l","𝐋").replace("m","𝐌").replace("n","𝐍").replace("o","𝐎").replace("p","𝐏").replace("q","𝐐").replace("r","𝐑").replace("s","𝐒").replace("t","𝐓").replace("u","𝐔").replace("v","𝐕").replace("w","𝐖").replace("x","𝐗").replace("y","𝐘").replace("z","𝐙").replace("A","𝐀").replace("B","𝐁").replace("C","𝐂").replace("D","𝐃").replace("E","𝐄").replace("F","𝐅").replace("G","𝐆").replace("H","𝐇").replace("I","𝐈").replace("J","𝐉").replace("K","𝐊").replace("L","𝐋").replace("M","𝐌").replace("N","𝐍").replace("O","𝐎").replace("P","𝐏").replace("Q","𝐐").replace("R","𝐑").replace("S","𝐒").replace("T","𝐓").replace("U","𝐔").replace("V","𝐕").replace("W","𝐖").replace("X","𝐗").replace("Y","𝐘").replace("Z","𝐙")
            WA35 = text.replace('a','𝑨').replace("b","𝑩").replace("c","𝑪").replace("d","𝑫").replace("e","𝑬").replace("f","𝑭").replace("g","𝑮").replace("h","𝑯").replace("i","??").replace("j","𝑱").replace("k","𝑲").replace("l","𝑳").replace("m","𝑴").replace("n","𝑵").replace("o","𝑶").replace("p","𝑷").replace("q","𝑸").replace("r","𝑹").replace("s","𝑺").replace("t","𝑻").replace("u","𝑼").replace("v","𝑽").replace("w","𝑾").replace("x","𝑿").replace("y","𝒀").replace("z","𝒁").replace("A","𝑨").replace("B","𝑩").replace("C","𝑪").replace("D","𝑫").replace("E","𝑬").replace("F","𝑭").replace("G","𝑮").replace("H","𝑯").replace("I","𝑰").replace("J","𝑱").replace("K","𝑲").replace("L","𝑳").replace("M","𝑴").replace("N","𝑵").replace("O","𝑶").replace("P","𝑷").replace("Q","𝑸").replace("R","𝑹").replace("S","𝑺").replace("T","𝑻").replace("U","𝑼").replace("V","𝑽").replace("W","𝑾").replace("X","𝑿").replace("Y","𝒀").replace("Z","𝒁")
            WA36 = text.replace('a','𝘼').replace("b","𝘽").replace("c","𝘾").replace("d","𝘿").replace("e","𝙀").replace("f","𝙁").replace("g","𝙂").replace("h","𝙃").replace("i","𝙄").replace("j","𝙅").replace("k","𝙆").replace("l","𝙇").replace("m","𝙈").replace("n","𝙉").replace("o","𝙊").replace("p","𝙋").replace("q","𝙌").replace("r","𝙍").replace("s","𝙎").replace("t","𝙏").replace("u","𝙐").replace("v","𝙑").replace("w","𝙒").replace("x","𝙓").replace("y","𝙔").replace("z","𝙕").replace("A","𝘼").replace("B","𝘽").replace("C","𝘾").replace("D","𝘿").replace("E","𝙀").replace("F","𝙁").replace("G","𝙂").replace("H","𝙃").replace("I","𝙄").replace("J","𝙅").replace("K","𝙆").replace("L","𝙇").replace("M","𝙈").replace("N","𝙉").replace("O","𝙊").replace("P","𝙋").replace("Q","𝙌").replace("R","𝙍").replace("S","𝙎").replace("T","𝙏").replace("U","𝙐").replace("V","𝙑").replace("W","𝙒").replace("X","𝙓").replace("Y","𝙔").replace("Z","𝙕")
            WA37 = text.replace('a','𝗔').replace("b","𝗕").replace("c","𝗖").replace("d","𝗗").replace("e","𝗘").replace("f","𝗙").replace("g","𝗚").replace("h","𝗛").replace("i","𝗜").replace("j","𝗝").replace("k","𝗞").replace("l","𝗟").replace("m","𝗠").replace("n","𝗡").replace("o","𝗢").replace("p","𝗣").replace("q","𝗤").replace("r","𝗥").replace("s","𝗦").replace("t","𝗧").replace("u","𝗨").replace("v","𝗩").replace("w","𝗪").replace("x","𝗫").replace("y","𝗬").replace("z","𝗭").replace("A","𝗔").replace("B","𝗕").replace("C","𝗖").replace("D","𝗗").replace("E","𝗘").replace("F","𝗙").replace("G","𝗚").replace("H","𝗛").replace("I","𝗜").replace("J","𝗝").replace("K","𝗞").replace("L","𝗟").replace("M","𝗠").replace("N","𝗡").replace("O","𝗢").replace("P","𝗣").replace("Q","𝗤").replace("R","𝗥").replace("S","𝗦").replace("T","𝗧").replace("U","𝗨").replace("V","𝗩").replace("W","𝗪").replace("X","𝗫").replace("Y","𝗬").replace("Z","𝗭")
            dd.remove(int(chat.id))
            return await event.client.send_message(chat.id, f"**ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗦𝘁𝘆𝗹𝗲 - زخـرفـه تمبلـر**\n**⋆┄─┄─┄─┄┄─┄─┄─┄─┄⋆**\n{WA1} {smiile1}\n{WA2} {smiile2}\n{WA3} {smiile3}\n{WA4} {smiile4}\n{WA5} {smiile5}\n{WA6} {smiile6}\n{WA7} {smiile7}\n{WA8} {smiile8}\n{WA9} {smiile9}\n{WA10} {smiile10}\n{WA11} {smiile11}\n{WA12} {smiile12}\n{WA13} {smiile13}\n{WA14} {smiile14}\n{WA15} {smiile15}\n{WA16} {smiile16}\n{WA17} {smiile17}\n{WA18} {smiile18}\n{WA19} {smiile19}\n{WA20} {smiile20}\n{WA21} {smiile21}\n{WA22} {smiile22}\n{WA23} {smiile23}\n{WA24} {smiile24}\n{WA25} {smiile25}\n{WA26} {smiile26}\n{WA27} {smiile27}\n{WA28} {smiile28}\n{WA29} {smiile29}\n{WA30} {smiile30}\n{WA31} {smiile31}\n{WA32} {smiile32}\n{WA33} {smiile33}\n{WA34} {smiile34}\n{WA35} {smiile35}\n{WA36} {smiile36}\n{WA37} {smiile37}")
        if int(chat.id) in tt:
            msg = await event.forward_to(Config.OWNER_ID)
            chat = await event.get_chat()
            user = await l313l.get_me()
            reply_to = await reply_id(event)
            mention = f"[{chat.first_name}](tg://user?id={chat.id})"
            my_mention = f"[{user.first_name}](tg://user?id={user.id})"
            first = chat.first_name
            last = chat.last_name
            fullname = f"{first} {last}" if last else first
            username = f"@{chat.username}" if chat.username else mention
            userid = chat.id
            my_first = user.first_name
            my_last = user.last_name
            my_fullname = f"{my_first} {my_last}" if my_last else my_first
            my_username = f"@{user.username}" if user.username else my_mention
            if gvarstatus("START_BUTUN") is not None:
                zz_txt = "⌔ قنـاتـي ⌔"
                zz_ch = gvarstatus("START_BUTUN")
            elif user.username:
                zz_txt = "⌔ لـ التواصـل خـاص ⌔"
                zz_ch = user.username
            else:
                zz_txt = "⌔ قنـاة المـطور ⌔"
                zz_ch = "aqhvv"
            customtasmsg = gvarstatus("TAS_TEXT") or None
            if customtasmsg is not None:
                tas_msg = customtasmsg.format(
                    zz_mention=mention,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    my_first=my_first,
                    my_last=my_last,
                    my_zname=my_fullname,
                    my_username=my_username,
                    my_mention=my_mention,
                )
            else:
                tas_msg = f"**⌔ عـزيـزي  {mention} **\
                            \n**⌔ تم ارسـال رسالتـك لـ** {my_fullname} 💌\
                            \n**⌔ تحلى بالصبـر وانتظـر الـرد 📨.**"
            buttons = [
                [
                    Button.inline("تعطيـل التواصـل", data="ttk_bot-off")
                ]
            ]
            await event.client.send_message(
                chat.id,
                tas_msg,
                link_preview=False,
                buttons=buttons,
                reply_to=reply_to,
            )
            try:
                add_user_to_db(msg.id, get_display_name(chat), chat.id, event.id, 0, 0)
            except Exception as e:
                LOGS.error(str(e))
    else:
        if event.text.startswith("/style"):
            dd.append(int(chat.id))
            zzs = "**- مرحبـا عزيـزي المـالك 🧑🏻‍💻**\n**- ارسـل الان الاسـم الذي تريـد زخرفتـه بالانكـلـش ✓**\n\n**- لـ الالغـاء ارسـل /cancle**"
            return await event.client.send_message(
                chat.id,
                zzs,
                reply_to=reply_to,
            )
        if event.text.startswith("/cancle"):
            if int(chat.id) in dd:
                dd.remove(int(chat.id))
            zzc = "**- تم الالغـاء .. بنجـاح**"
            return await event.client.send_message(
                chat.id,
                zzc,
                reply_to=reply_to,
            )
        if event.text.startswith("/"):
            return
        if chat.id in dd:
            text = event.text
            iitems = ['࿐', '𖣳', '𓃠', '𖡟', '𖠜', '‌♡⁩', '‌༗', '‌𖢖', '❥', '‌ঌ', '𝆹𝅥𝅮', '𖠜', '𖠲', '𖤍', '𖠛', ' 𝅘𝅥𝅮', '‌༒', '‌ㇱ', '߷', 'メ', '〠', '𓃬', '𖠄']
            smiile1 = random.choice(iitems)
            smiile2 = random.choice(iitems)
            smiile3 = random.choice(iitems)
            smiile4 = random.choice(iitems)
            smiile5 = random.choice(iitems)
            smiile6 = random.choice(iitems)
            smiile7 = random.choice(iitems)
            smiile8 = random.choice(iitems)
            smiile9 = random.choice(iitems)
            smiile10 = random.choice(iitems)
            smiile11 = random.choice(iitems)
            smiile12 = random.choice(iitems)
            smiile13 = random.choice(iitems)
            smiile14 = random.choice(iitems)
            smiile15 = random.choice(iitems)
            smiile16 = random.choice(iitems)
            smiile17 = random.choice(iitems)
            smiile18 = random.choice(iitems)
            smiile19 = random.choice(iitems)
            smiile20 = random.choice(iitems)
            smiile21 = random.choice(iitems)
            smiile22 = random.choice(iitems)
            smiile23 = random.choice(iitems)
            smiile24 = random.choice(iitems)
            smiile25 = random.choice(iitems)
            smiile26 = random.choice(iitems)
            smiile27 = random.choice(iitems)
            smiile28 = random.choice(iitems)
            smiile29 = random.choice(iitems)
            smiile30 = random.choice(iitems)
            smiile31 = random.choice(iitems)
            smiile32 = random.choice(iitems)
            smiile33 = random.choice(iitems)
            smiile34 = random.choice(iitems)
            smiile35 = random.choice(iitems)
            smiile36 = random.choice(iitems)
            smiile37 = random.choice(iitems)

            WA1 = text.replace('a', 'ᵃ').replace('A', 'ᴬ').replace('b', 'ᵇ').replace('B', 'ᴮ').replace('c', 'ᶜ').replace('C', 'ᶜ').replace('d', 'ᵈ').replace('D', 'ᴰ').replace('e', 'ᵉ').replace('E', 'ᴱ').replace('f', 'ᶠ').replace('F', 'ᶠ').replace('g', 'ᵍ').replace('G', 'ᴳ').replace('h', 'ʰ').replace('H', 'ᴴ').replace('i', 'ⁱ').replace('I', 'ᴵ').replace('j', 'ʲ').replace('J', 'ᴶ').replace('k', 'ᵏ').replace('K', 'ᴷ').replace('l', 'ˡ').replace('L', 'ᴸ').replace('m', 'ᵐ').replace('M', 'ᴹ').replace('n', 'ⁿ').replace('N', 'ᴺ').replace('o', 'ᵒ').replace('O', 'ᴼ').replace('p', 'ᵖ').replace('P', 'ᴾ').replace('q', '۩').replace('Q', 'Q').replace('r', 'ʳ').replace('R', 'ᴿ').replace('s', 'ˢ').replace('S', 'ˢ').replace('t', 'ᵗ').replace('T', 'ᵀ').replace('u', 'ᵘ').replace('U', 'ᵁ').replace('v', 'ⱽ').replace('V', 'ⱽ').replace('w', 'ʷ').replace('W', 'ᵂ').replace('x', 'ˣ').replace('X', 'ˣ').replace('y', 'ʸ').replace('Y', 'ʸ').replace('z', 'ᶻ').replace('Z', 'ᶻ')
            WA2 = text.replace('a', 'ᴀ').replace('b', 'ʙ').replace('c', 'ᴄ').replace('d', 'ᴅ').replace('e', 'ᴇ').replace('f', 'ғ').replace('g', 'ɢ').replace('h', 'ʜ').replace('i', 'ɪ').replace('j', 'ᴊ').replace('k', 'ᴋ').replace('l', 'ʟ').replace('m', 'ᴍ').replace('n', 'ɴ').replace('o', 'ᴏ').replace('p', 'ᴘ').replace('q', 'ǫ').replace('r', 'ʀ').replace('s', 's').replace('t', 'ᴛ').replace('u', 'ᴜ').replace('v', 'ᴠ').replace('w', 'ᴡ').replace('x', 'x').replace('y', 'ʏ').replace('z', 'ᴢ').replace('A', 'ᴀ').replace('B', 'ʙ').replace('C', 'ᴄ').replace('D', 'ᴅ').replace('E', 'ᴇ').replace('F', 'ғ').replace('G', 'ɢ').replace('H', 'ʜ').replace('I', 'ɪ').replace('J', 'ᴊ').replace('K', 'ᴋ').replace('L', 'ʟ').replace('M', 'ᴍ').replace('N', 'ɴ').replace('O', 'ᴏ').replace('P', 'ᴘ').replace('Q', 'ǫ').replace('R', 'ʀ').replace('S', 'S').replace('T', 'ᴛ').replace('U', 'ᴜ').replace('V', 'ᴠ').replace('W', 'ᴡ').replace('X', 'X').replace('Y', 'ʏ').replace('Z', 'ᴢ')
            WA3 = text.replace('a','α').replace("b","в").replace("c","c").replace("d","∂").replace("e","ε").replace("E","ғ").replace("g","g").replace("h","н").replace("i","ι").replace("j","נ").replace("k","к").replace("l","ℓ").replace("m","м").replace("n","η").replace("o","σ").replace("p","ρ").replace("q","q").replace("r","я").replace("s","s").replace("t","т").replace("u","υ").replace("v","v").replace("w","ω").replace("x","x").replace("y","ү").replace("z","z").replace("A","α").replace("B","в").replace("C","c").replace("D","∂").replace("E","ε").replace("E","ғ").replace("G","g").replace("H","н").replace("I","ι").replace("J","נ").replace("K","к").replace("L","ℓ").replace("M","м").replace("N","η").replace("O","σ").replace("P","ρ").replace("Q","q").replace("R","я").replace("S","s").replace("T","т").replace("U","υ").replace("V","v").replace("W","ω").replace("X","X").replace("Y","ү").replace("Z","z")
            WA4 = text.replace('a','𝙰') .replace('b','𝙱') .replace('c','𝙲') .replace('d','𝙳') .replace('e','𝙴') .replace('f','𝙵') .replace('g','𝙶') .replace('h','𝙷') .replace('i','𝙸') .replace('j','𝚓') .replace('k','𝙺') .replace('l','𝙻') .replace('m','𝙼') .replace('n','𝙽') .replace('o','𝙾') .replace('p','𝙿') .replace('q','𝚀') .replace('r','𝚁') .replace('s','𝚂') .replace('t','𝚃') .replace('u','𝚄') .replace('v','??') .replace('w','𝚆') .replace('x','𝚇') .replace('y','𝚈') .replace('z','𝚉').replace('A','𝙰') .replace('B','𝙱') .replace('C','𝙲') .replace('D','𝙳') .replace('E','𝙴') .replace('F','𝙵') .replace('G','𝙶') .replace('H','𝙷') .replace('I','𝙸') .replace('J','𝚓') .replace('K','𝙺') .replace('L','𝙻') .replace('M','𝙼') .replace('N','𝙽') .replace('O','𝙾') .replace('P','𝙿') .replace('Q','𝚀') .replace('R','𝚁') .replace('S','𝚂') .replace('T','𝚃') .replace('U','𝚄') .replace('V','𝚅') .replace('W','𝚆') .replace('X','𝚇') .replace('Y','𝚈') .replace('Z','𝚉')
            WA5 = text.replace('a','🇦 ').replace("b","🇧 ").replace("c","🇨 ").replace("d","🇩 ").replace("e","🇪 ").replace("f","🇫 ").replace("g","🇬 ").replace("h","🇭 ").replace("i","🇮 ").replace("j","🇯 ").replace("k","🇰 ").replace("l","🇱 ").replace("m","🇲 ").replace("n","🇳 ").replace("o","🇴 ").replace("p","🇵 ").replace("q","🇶 ").replace("r","🇷 ").replace("s","🇸 ").replace("t","🇹 ").replace("u","🇻 ").replace("v","🇺 ").replace("w","🇼 ").replace("x","🇽 ").replace("y","🇾 ").replace("z","🇿 ").replace("A","🇦 ").replace("B","🇧 ").replace("C","🇨 ").replace("D","🇩 ").replace("E","🇪 ").replace("F","🇫 ").replace("G","🇬 ").replace("H","🇭 ").replace("I","🇮 ").replace("J","🇯 ").replace("K","🇰 ").replace("L","🇱 ").replace("M","🇲 ").replace("N","🇳 ").replace("O","🇴 ").replace("P","🇵 ").replace("Q","🇶 ").replace("R","🇷 ").replace("S","🇸 ").replace("T","🇹 ").replace("U","🇻 ").replace("V","🇺 ").replace("W","🇼 ").replace("X","🇽 ").replace("Y","🇾 ").replace("Z","🇿 ")
            WA6 = text.replace('a','ⓐ').replace("b","ⓑ").replace("c","ⓒ").replace("d","ⓓ").replace("e","ⓔ").replace("f","ⓕ").replace("g","ⓖ").replace("h","ⓗ").replace("i","ⓘ").replace("j","ⓙ").replace("k","ⓚ").replace("l","ⓛ").replace("m","ⓜ").replace("n","ⓝ").replace("o","ⓞ").replace("p","ⓟ").replace("q","ⓠ").replace("r","ⓡ").replace("s","ⓢ").replace("t","ⓣ").replace("u","ⓤ").replace("v","ⓥ").replace("w","ⓦ").replace("x","ⓧ").replace("y","ⓨ").replace("z","ⓩ").replace("A","Ⓐ").replace("B","Ⓑ").replace("C","Ⓒ").replace("D","Ⓓ").replace("E","Ⓔ").replace("F","Ⓕ").replace("G","Ⓖ").replace("H","Ⓗ").replace("I","Ⓘ").replace("J","Ⓙ").replace("K","Ⓚ").replace("L","Ⓛ").replace("M","🄼").replace("N","Ⓝ").replace("O","Ⓞ").replace("P","Ⓟ").replace("Q","Ⓠ").replace("R","Ⓡ").replace("S","Ⓢ").replace("T","Ⓣ").replace("U","Ⓤ").replace("V","Ⓥ").replace("W","Ⓦ").replace("X","Ⓧ").replace("Y","Ⓨ").replace("Z","Ⓩ")
            WA7 = text.replace('a','🅐').replace("b","🅑").replace("c","🅒").replace("d","🅓").replace("e","🅔").replace("f","🅕").replace("g","🅖").replace("h","🅗").replace("i","🅘").replace("j","🅙").replace("k","🅚").replace("l","🅛").replace("m","🅜").replace("n","🅝").replace("o","🅞").replace("p","🅟").replace("q","🅠").replace("r","🅡").replace("s","🅢").replace("t","🅣").replace("u","🅤").replace("v","🅥").replace("w","🅦").replace("x","🅧").replace("y","🅨").replace("z","🅩").replace("A","🅐").replace("B","🅑").replace("C","🅒").replace("D","🅓").replace("E","🅔").replace("F","🅕").replace("G","🅖").replace("H","🅗").replace("I","🅘").replace("J","🅙").replace("K","🅚").replace("L","🅛").replace("M","🅜").replace("N","🅝").replace("O","🅞").replace("P","🅟").replace("Q","🅠").replace("R","🅡").replace("S","🅢").replace("T","🅣").replace("U","🅤").replace("V","🅥").replace("W","🅦").replace("X","🅧").replace("Y","🅨").replace("Z","🅩")
            WA8 = text.replace('a','🄰').replace("b","🄱").replace("c","🄲").replace("d","🄳").replace("e","🄴").replace("f","🄵").replace("g","🄶").replace("h","🄷").replace("i","🄸").replace("j","🄹").replace("k","🄺").replace("l","🄻").replace("m","🄼").replace("n","🄽").replace("o","🄾").replace("p","🄿").replace("q","🅀").replace("r","🅁").replace("s","🅂").replace("t","🅃").replace("u","🅄").replace("v","🅅").replace("w","🅆").replace("x","🅇").replace("y","🅈").replace("z","🅉").replace("A","🄰").replace("B","🄱").replace("C","🄲").replace("D","🄳").replace("E","🄴").replace("F","🄵").replace("G","🄶").replace("H","🄷").replace("I","🄸").replace("J","🄹").replace("K","🄺").replace("L","🄻").replace("M","🄼").replace("N","🄽").replace("O","🄾").replace("P","🄿").replace("Q","🅀").replace("R","🅁").replace("S","🅂").replace("T","🅃").replace("U","🅄").replace("V","🅅").replace("W","🅆").replace("X","🅇").replace("Y","🅈").replace("Z","🅉")
            WA9 = text.replace('a','🅐').replace("b","🅑").replace("c","🅲").replace("d","🅳").replace("e","🅴").replace("f","🅵").replace("g","🅶").replace("h","🅷").replace("i","🅸").replace("j","🅹").replace("k","🅺").replace("l","🅻").replace("m","🅼").replace("n","🅽").replace("o","🅞").replace("p","🅟").replace("q","🆀").replace("r","🆁").replace("s","🆂").replace("t","🆃").replace("u","🆄").replace("v","🆅").replace("w","🆆").replace("x","🆇").replace("y","🆈").replace("z","🆉").replace("A","🅐").replace("B","🅑").replace("C","🅲").replace("D","🅳").replace("E","🅴").replace("F","🅵").replace("G","🅶").replace("H","🅷").replace("I","🅸").replace("J","🅹").replace("K","🅺").replace("L","🅻").replace("M","🅼").replace("N","🅽").replace("O","🅞").replace("P","🅟").replace("Q","🆀").replace("R","🆁").replace("S","🆂").replace("T","🆃").replace("U","🆄").replace("V","🆅").replace("W","🆆").replace("X","🆇").replace("Y","🆈").replace("Z","🆉")
            WA10 = text.replace('a','𝘢') .replace('b','𝘣') .replace('c','𝘤') .replace('d','𝘥') .replace('e','𝘦') .replace('f','𝘧') .replace('g','𝘨') .replace('h','𝘩') .replace('i','𝘪') .replace('j','𝘫') .replace('k','𝘬') .replace('l','𝘭') .replace('m','𝘮') .replace('n','𝘯') .replace('o','𝘰') .replace('p','𝘱') .replace('q','𝘲') .replace('r','𝘳') .replace('s','𝘴') .replace('t','𝘵') .replace('u','𝘶') .replace('v','𝘷') .replace('w','𝘸') .replace('x','𝘹') .replace('y','𝘺') .replace('z','𝘻').replace('A','𝘢') .replace('B','𝘣') .replace('C','𝘤') .replace('D','𝘥') .replace('E','𝘦') .replace('F','𝘧') .replace('G','𝘨') .replace('H','𝘩') .replace('I','𝘪') .replace('J','𝘫') .replace('K','𝘬') .replace('L','𝘭') .replace('M','𝘮') .replace('N','𝘯') .replace('O','𝘰') .replace('P','𝘱') .replace('Q','𝘲') .replace('R','𝘳') .replace('S','𝘴') .replace('T','𝘵') .replace('U','𝘶') .replace('V','𝘷') .replace('W','𝘸') .replace('X','𝘹') .replace('Y','𝘺') .replace('Z','𝘻')
            WA11 = text.replace('a','𝘈').replace("b","𝘉").replace("c","𝘊").replace("d","𝘋").replace("e","𝘌").replace("f","𝘍").replace("g","𝘎").replace("h","𝘏").replace("i","𝘐").replace("j","𝘑").replace("k","𝘒").replace("l","𝘓").replace("m","𝘔").replace("n","𝘕").replace("o","𝘖").replace("p","𝘗").replace("q","𝘘").replace("r","𝘙").replace("s","𝘚").replace("t","𝘛").replace("u","𝘜").replace("v","𝘝").replace("w","𝘞").replace("x","𝘟").replace("y","𝘠").replace("z","𝘡").replace("A","𝘈").replace("B","𝘉").replace("C","𝘊").replace("D","𝘋").replace("E","𝘌").replace("F","𝘍").replace("G","𝘎").replace("H","𝘏").replace("I","𝘐").replace("J","𝘑").replace("K","𝘒").replace("L","𝘓").replace("M","𝘔").replace("N","𝘕").replace("O","𝘖").replace("P","𝘗").replace("Q","𝘘").replace("R","𝘙").replace("S","𝘚").replace("T","𝘛").replace("U","𝘜").replace("V","𝘝").replace("W","𝘞").replace("X","𝘟").replace("Y","𝘠").replace("Z","𝘡")
            WA12 = text.replace('a','Ａ').replace('b','Ｂ').replace('c','Ｃ').replace('d','Ｄ').replace('e','Ｅ').replace('f','Ｆ').replace('g','Ｇ').replace('h','Ｈ').replace('i','Ｉ').replace('j','Ｊ').replace('k','Ｋ').replace('l','Ｌ').replace('m','Ｍ').replace('n','Ｎ').replace('o','Ｏ').replace('p','Ｐ').replace('q','Ｑ').replace('r','Ｒ').replace('s','Ｓ').replace('t','Ｔ').replace('u','Ｕ').replace('v','Ｖ').replace('w','Ｗ').replace('x','Ｘ').replace('y','Ｙ').replace('z','Ｚ')
            WA13 = text.replace('a','ًٍَُِّA').replace("b","ًٍَُِّB").replace("c","ًٍَُِّC").replace("d","ًٍَُِّD").replace("e","ًٍَُِّE").replace("f","ًٍَُِّF").replace("g","ًٍَُِّG").replace("h","ًٍَُِّH").replace("i","ًٍَُِّI").replace("j","ًٍَُِّJ").replace("k","ًٍَُِّK").replace("l","ًٍَُِّL").replace("m","ًٍَُِّM").replace("n","ًٍَُِّN").replace("o","ًٍَُِّO").replace("p","ًٍَُِّP").replace("q","ًٍَُِّQ").replace("r","ًٍَُِّR").replace("s","ًٍَُِّS").replace("t","ًٍَُِّT").replace("u","ًٍَُِّU").replace("v","ًٍَُِّV").replace("w","ًٍَُِّW").replace("x","ًٍَُِّX").replace("y","ًٍَُِّY").replace("z","ًٍَُِّZ")
            WA14 = text.replace('a','ᥲ').replace('b','ᗷ').replace('c','ᑕ').replace('d','ᗞ').replace('e','ᗴ').replace('f','ᖴ').replace('g','Ꮐ').replace('h','ᕼ').replace('i','Ꭵ').replace('j','ᒍ').replace('k','Ꮶ').replace('l','ᥣ').replace('m','ᗰ').replace('n','ᑎ').replace('o','ᝪ').replace('p','ᑭ').replace('q','ᑫ').replace('r','ᖇ').replace('s','ᔑ').replace('t','Ꭲ').replace('u','ᑌ').replace('v','ᐯ').replace('w','ᗯ').replace('x','᙭').replace('y','Ꭹ').replace('z','𝖹')
            WA15 = text.replace('a','ᗩ').replace('b','ᗷ').replace('c','ᑕ').replace('d','ᗪ').replace('e','ᗴ').replace('f','ᖴ').replace('g','Ǥ').replace('h','ᕼ').replace('i','Ꮖ').replace('j','ᒎ').replace('k','ᛕ').replace('l','し').replace('m','ᗰ').replace('n','ᑎ').replace('o','ᗝ').replace('p','ᑭ').replace('q','Ɋ').replace('r','ᖇ').replace('s','Տ').replace('t','丅').replace('u','ᑌ').replace('v','ᐯ').replace('w','ᗯ').replace('x','᙭').replace('y','Ƴ').replace('z','乙').replace('A','ᗩ').replace('B','ᗷ').replace('C','ᑕ').replace('D','ᗪ').replace('E','ᗴ').replace('F','ᖴ').replace('G','Ǥ').replace('H','ᕼ').replace('I','Ꮖ').replace('J','ᒎ').replace('L','ᛕ').replace('L','し').replace('M','ᗰ').replace('N','ᑎ').replace('O','ᗝ').replace('P','ᑭ').replace('Q','Ɋ').replace('R','ᖇ').replace('S','Տ').replace('T','丅').replace('U','ᑌ').replace('V','ᐯ').replace('W','ᗯ').replace('X','᙭').replace('Y','Ƴ').replace('Z','乙')
            WA16 = text.replace('a','A̶').replace('b','B̶').replace('c','C̶').replace('d','D̶').replace('e','E̶').replace('f','F̶').replace('g','G̶').replace('h','H̶').replace('i','I̶').replace('j','J̶').replace('k','K̶').replace('l','L̶').replace('m','M̶').replace('n','N̶').replace('o','O̶').replace('p','P̶').replace('q','Q̶').replace('r','R̶').replace('s','S̶').replace('t','T̶').replace('u','U̶').replace('v','V̶').replace('w','W̶').replace('x','X̶').replace('y','Y̶').replace('z','Z̶').replace('A','A̶').replace('B','B̶').replace('C','C̶').replace('D','D̶').replace('E','E̶').replace('F','F̶').replace('G','G̶').replace('H','H̶').replace('I','I̶').replace('J','J̶').replace('K','K̶').replace('L','L̶').replace('M','M̶').replace('N','N̶').replace('O','O̶').replace('P','P̶').replace('Q','Q̶').replace('R','R̶').replace('S','S̶').replace('T','T̶').replace('U','U̶').replace('V','V̶').replace('W','W̶').replace('X','X̶').replace('Y','Y̶').replace('Z','Z̶')
            WA17 = text.replace('a','𝖆') .replace('b','𝖉') .replace('c','𝖈') .replace('d','𝖉') .replace('e','𝖊') .replace('f','𝖋') .replace('g','𝖌') .replace('h','𝖍') .replace('i','𝖎') .replace('j','𝖏') .replace('k','𝖐') .replace('l','𝖑') .replace('m','𝖒') .replace('n','𝖓') .replace('o','𝖔') .replace('p','𝖕') .replace('q','𝖖') .replace('r','𝖗') .replace('s','𝖘') .replace('t','𝖙') .replace('u','𝖚') .replace('v','𝒗') .replace('w','𝒘') .replace('x','𝖝') .replace('y','𝒚') .replace('z','𝒛').replace('A','𝖆') .replace('B','𝖉') .replace('C','𝖈') .replace('D','𝖉') .replace('E','𝖊') .replace('F','𝖋') .replace('G','𝖌') .replace('H','𝖍') .replace('I','𝖎') .replace('J','𝖏') .replace('K','𝖐') .replace('L','𝖑') .replace('M','𝖒') .replace('N','𝖓') .replace('O','𝖔') .replace('P','𝖕') .replace('Q','𝖖') .replace('R','𝖗') .replace('S','𝖘') .replace('T','𝖙') .replace('U','𝖚') .replace('V','𝒗') .replace('W','𝒘') .replace('X','𝖝') .replace('Y','𝒚') .replace('Z','𝒛')
            WA18 = text.replace('a','𝒂') .replace('b','𝒃') .replace('c','𝒄') .replace('d','𝒅') .replace('e','𝒆') .replace('f','𝒇') .replace('g','𝒈') .replace('h','𝒉') .replace('i','𝒊') .replace('j','𝒋') .replace('k','𝒌') .replace('l','𝒍') .replace('m','𝒎') .replace('n','𝒏') .replace('o','𝒐') .replace('p','𝒑') .replace('q','𝒒') .replace('r','𝒓') .replace('s','𝒔') .replace('t','𝒕') .replace('u','𝒖') .replace('v','𝒗') .replace('w','𝒘') .replace('x','𝒙') .replace('y','𝒚') .replace('z','𝒛')
            WA19 = text.replace('a','𝑎') .replace('b','𝑏') .replace('c','𝑐') .replace('d','𝑑') .replace('e','𝑒') .replace('f','𝑓') .replace('g','𝑔') .replace('h','ℎ') .replace('i','𝑖') .replace('j','𝑗') .replace('k','𝑘') .replace('l','𝑙') .replace('m','𝑚') .replace('n','𝑛') .replace('o','𝑜') .replace('p','𝑝') .replace('q','𝑞') .replace('r','𝑟') .replace('s','𝑠') .replace('t','𝑡') .replace('u','𝑢') .replace('v','𝑣') .replace('w','𝑤') .replace('x','𝑥') .replace('y','𝑦') .replace('z','𝑧')
            WA20 = text.replace('a','ꪖ') .replace('b','᥇') .replace('c','ᥴ') .replace('d','ᦔ') .replace('e','ꫀ') .replace('f','ᠻ') .replace('g','ᧁ') .replace('h','ꫝ') .replace('i','𝓲') .replace('j','𝓳') .replace('k','𝘬') .replace('l','ꪶ') .replace('m','ꪑ') .replace('n','ꪀ') .replace('o','ꪮ') .replace('p','ρ') .replace('q','𝘲') .replace('r','𝘳') .replace('s','𝘴') .replace('t','𝓽') .replace('u','ꪊ') .replace('v','ꪜ') .replace('w','᭙') .replace('x','᥊') .replace('y','ꪗ') .replace('z','ɀ').replace('A','ꪖ') .replace('B','᥇') .replace('C','ᥴ') .replace('D','ᦔ') .replace('E','ꫀ') .replace('F','ᠻ') .replace('G','ᧁ') .replace('H','ꫝ') .replace('I','𝓲') .replace('J','𝓳') .replace('K','𝘬') .replace('L','ꪶ') .replace('M','ꪑ') .replace('N','ꪀ') .replace('O','ꪮ') .replace('P','ρ') .replace('Q','𝘲') .replace('R','𝘳') .replace('S','𝘴') .replace('T','𝓽') .replace('U','ꪊ') .replace('V','ꪜ') .replace('W','᭙') .replace('X','᥊') .replace('Y','ꪗ') .replace('Z','ɀ')
            WA21 = text.replace('a','ą').replace('b','ც').replace('c','ƈ').replace('d','ɖ').replace('e','ɛ').replace('f','ʄ').replace('g','ɠ').replace('h','ɧ').replace('i','ı').replace('j','ʝ').replace('k','ƙ').replace('l','Ɩ').replace('m','ɱ').replace('n','ŋ').replace('o','ơ').replace('p','℘').replace('q','զ').replace('r','r').replace('s','ʂ').replace('t','ɬ').replace('u','ų').replace('v','v').replace('w','ῳ').replace('x','ҳ').replace('y','ყ').replace('z','ʑ')
            WA22 = text.replace('a','Δ').replace("b","β").replace("c","૮").replace("d","ᴅ").replace("e","૯").replace("f","ƒ").replace("g","ɢ").replace("h","み").replace("i","เ").replace("j","ʝ").replace("k","ҡ").replace("l","ɭ").replace("m","ണ").replace("n","ท").replace("o","๏").replace("p","ρ").replace("q","ǫ").replace("r","ʀ").replace("s","ઽ").replace("t","τ").replace("u","υ").replace("v","ѵ").replace("w","ω").replace("x","ﾒ").replace("y","ყ").replace("z","ʑ")
            WA23 = text.replace('a','ᕱ').replace("b","β").replace("c","૮").replace("d","Ɗ").replace("e","ξ").replace("f","ƒ").replace("g","Ǥ").replace("h","ƕ").replace("i","Ĩ").replace("j","ʝ").replace("k","Ƙ").replace("l","Ꮭ").replace("m","ണ").replace("n","ท").replace("o","♡").replace("p","Ƥ").replace("q","𝑄").replace("r","Ꮢ").replace("s","Ƨ").replace("t","Ƭ").replace("u","Ꮜ").replace("v","ѵ").replace("w","ẁ́̀́").replace("x","ﾒ").replace("y","ɣ").replace("z","ʑ")
            WA24 = text.replace('a','A꯭').replace("b","B꯭").replace("c","C꯭").replace("d","D꯭").replace("e","E꯭").replace("f","F꯭").replace("g","G꯭").replace("h","H꯭").replace("i","I꯭").replace("j","J꯭").replace("k","K꯭").replace("l","L꯭").replace("m","M꯭").replace("n","N꯭").replace("o","O꯭").replace("p","P꯭").replace("q","Q꯭").replace("r","R꯭").replace("s","S꯭").replace("t","T꯭").replace("u","U꯭").replace("v","V꯭").replace("w","W꯭").replace("x","X꯭").replace("y","Y꯭").replace("z","Z꯭").replace('A','A꯭').replace("B","B꯭").replace("C","C꯭").replace("D","D꯭").replace("E","E꯭").replace("F","F꯭").replace("G","G꯭").replace("H","H꯭").replace("I","I꯭").replace("J","J꯭").replace("K","K꯭").replace("L","L꯭").replace("M","M꯭").replace("N","N꯭").replace("O","O꯭").replace("P","P꯭").replace("Q","Q꯭").replace("R","R꯭").replace("S","S꯭").replace("T","T꯭").replace("U","U꯭").replace("V","V꯭").replace("W","W꯭").replace("X","X꯭").replace("Y","Y꯭").replace("Z","Z꯭")
            WA25 = text.replace('a', '[̲̅a̲̅]').replace('b', '[̲̅b̲̅]').replace('c', '[̲̅c̲̅]').replace('d', '[̲̅d̲̅]').replace('e', '[̲̅e̲̅]').replace('f', '[̲̅f̲̅]').replace('g', '[̲̅g̲̅]').replace('h', '[̲̅h̲̅]').replace('i', '[̲̅i̲̅]').replace('j', '[̲̅j̲̅]').replace('k', '[̲̅k̲̅]').replace('l', '[̲̅l̲̅]').replace('m', '[̲̅m̲̅]').replace('n', '[̲̅n̲̅]').replace('o', '[̲̅o̲̅]').replace('p', '[̲̅p̲̅]').replace('q', '[̲̅q̲̅]').replace('r', '[̲̅r̲̅]').replace('s', '[̲̅s̲̅]').replace('t', '[̲̅t̲̅]').replace('u', '[̲̅u̲̅]').replace('v', '[̲̅v̲̅]').replace('w', '[̲̅w̲̅]').replace('x', '[̲̅x̲̅]').replace('y', '[̲̅y̲̅]').replace('z', '[̲̅z̲̅]').replace('A', '[̲̅A̲̅]').replace('B', '[̲̅B̲̅]').replace('C', '[̲̅C̲̅]').replace('D', '[̲̅D̲̅]').replace('E', '[̲̅E̲̅]').replace('F', '[̲̅F̲̅]').replace('G', '[̲̅G̲̅]').replace('H', '[̲̅H̲̅]').replace('I', '[̲̅I̲̅]').replace('J', '[̲̅J̲̅]').replace('K', '[̲̅K̲̅]').replace('L', '[̲̅L̲̅]').replace('M', '[̲̅M̲̅]').replace('N', '[̲̅N̲̅]').replace('O', '[̲̅O̲̅]').replace('P', '[̲̅P̲̅]').replace('Q', '[̲̅Q̲̅]').replace('R', '[̲̅R̲̅]').replace('S', '[̲̅S̲̅]').replace('T', '[̲̅T̲̅]').replace('U', '[̲̅U̲̅]').replace('V', '[̲̅V̲̅]').replace('W', '[̲̅W̲̅]').replace('X', '[̲̅X̲̅]').replace('Y', '[̲̅Y̲̅]').replace('Z', '[̲̅Z̲̅]')
            WA26 = text.replace('a','𝔄').replace("b","𝔅").replace("c","ℭ").replace("d","𝔇").replace("e","𝔈").replace("f","𝔉").replace("g","𝔊").replace("h","ℌ").replace("i","ℑ").replace("j","𝔍").replace("k","𝔎").replace("l","𝔏").replace("m","𝔐").replace("n","𝔑").replace("o","𝔒").replace("p","𝔓").replace("q","𝔔").replace("r","ℜ").replace("s","𝔖").replace("t","𝔗").replace("u","𝔘").replace("v","𝔙").replace("w","𝔚").replace("x","𝔛").replace("y","𝔜").replace("z","ℨ").replace("A","𝔄").replace("B","𝔅").replace("C","ℭ").replace("D","𝔇").replace("E","𝔈").replace("F","𝔉").replace("G","𝔊").replace("H","ℌ").replace("I","ℑ").replace("J","𝔍").replace("K","𝔎").replace("L","𝔏").replace("M","𝔐").replace("N","𝔑").replace("O","𝔒").replace("P","𝔓").replace("Q","𝔔").replace("R","ℜ").replace("S","𝔖").replace("T","𝔗").replace("U","𝔘").replace("V","𝔙").replace("W","𝔚").replace("X","𝔛").replace("Y","𝔜").replace("Z","ℨ")
            WA27 = text.replace('a','𝕬').replace("b","𝕭").replace("c","𝕮").replace("d","𝕯").replace("e","𝕰").replace("f","𝕱").replace("g","𝕲").replace("h","𝕳").replace("i","𝕴").replace("j","𝕵").replace("k","𝕶").replace("l","𝕷").replace("m","𝕸").replace("n","𝕹").replace("o","𝕺").replace("p","𝕻").replace("q","𝕼").replace("r","𝕽").replace("s","𝕾").replace("t","𝕿").replace("u","𝖀").replace("v","𝖁").replace("w","𝖂").replace("x","𝖃").replace("y","𝖄").replace("z","𝖅").replace("A","𝕬").replace("B","𝕭").replace("C","𝕮").replace("D","𝕯").replace("E","𝕰").replace("F","𝕱").replace("G","𝕲").replace("H","𝕳").replace("I","𝕴").replace("J","𝕵").replace("K","𝕶").replace("L","𝕷").replace("M","𝕸").replace("N","𝕹").replace("O","𝕺").replace("P","𝕻").replace("Q","𝕼").replace("R","𝕽").replace("S","𝕾").replace("T","𝕿").replace("U","𝖀").replace("V","𝖁").replace("W","𝖂").replace("X","𝖃").replace("Y","𝖄").replace("Z","𝖅")
            WA28 = text.replace('a','𝔸').replace("b","𝔹").replace("c","ℂ").replace("d","𝔻").replace("e","𝔼").replace("f","𝔽").replace("g","𝔾").replace("h","ℍ").replace("i","𝕀").replace("j","𝕁").replace("k","𝕂").replace("l","𝕃").replace("m","𝕄").replace("n","ℕ").replace("o","𝕆").replace("p","ℙ").replace("q","ℚ").replace("r","ℝ").replace("s","𝕊").replace("t","𝕋").replace("u","𝕌").replace("v","𝕍").replace("w","𝕎").replace("x","𝕏").replace("y","𝕐").replace("z","ℤ").replace("A","𝔸").replace("B","𝔹").replace("C","ℂ").replace("D","𝔻").replace("E","𝔼").replace("F","𝔽").replace("G","𝔾").replace("H","ℍ").replace("I","𝕀").replace("J","𝕁").replace("K","𝕂").replace("L","𝕃").replace("M","𝕄").replace("N","ℕ").replace("O","𝕆").replace("P","ℙ").replace("Q","ℚ").replace("R","ℝ").replace("S","𝕊").replace("T","𝕋").replace("U","𝕌").replace("V","𝕍").replace("W","𝕎").replace("X","𝕏").replace("Y","𝕐").replace("Z","ℤ")
            WA29 = text.replace('a','░a░').replace("b","░b░").replace("c","░c░").replace("d","░d░").replace("e","░e░").replace("f","░f░").replace("g","░g░").replace("h","░h░").replace("i","░i░").replace("j","░j░").replace("k","░k░").replace("l","░l░").replace("m","░m░").replace("n","░n░").replace("o","░o░").replace("p","░p░").replace("q","░q░").replace("r","░r░").replace("s","░s░").replace("t","░t░").replace("u","░u░").replace("v","░v░").replace("w","░w░").replace("x","░x░").replace("y","░y░").replace("z","░z░").replace("A","░A░").replace("B","░B░").replace("C","░C░").replace("D","░D░").replace("E","░E░").replace("F","░F░").replace("G","░G░").replace("H","░H░").replace("I","░I░").replace("J","░J░").replace("K","░K░").replace("L","░L░").replace("M","░M░").replace("N","░N░").replace("O","░O░").replace("P","░P░").replace("Q","░Q░").replace("R","░R░").replace("S","░S░").replace("T","░T░").replace("U","░U░").replace("V","░V░").replace("W","░W░").replace("X","░X░").replace("Y","░Y░").replace("Z","░Z░")
            WA30 = text.replace('a','𝐚').replace("b","𝐛").replace("c","𝐜").replace("d","𝐝").replace("e","𝐞").replace("f","𝐟").replace("g","𝐠").replace("h","𝐡").replace("i","𝐢").replace("j","𝐣").replace("k","𝐤").replace("l","𝐥").replace("m","𝐦").replace("n","𝐧").replace("o","𝐨").replace("p","𝐩").replace("q","𝐪").replace("r","𝐫").replace("s","𝐬").replace("t","𝐭").replace("u","𝐮").replace("v","𝐯").replace("w","𝐰").replace("x","𝐱").replace("y","𝐲").replace("z","𝐳").replace("A","𝐚").replace("B","𝐛").replace("C","𝐜").replace("D","𝐝").replace("E","𝐞").replace("F","𝐟").replace("G","𝐠").replace("H","𝐡").replace("I","𝐢").replace("J","𝐣").replace("K","𝐤").replace("L","𝐥").replace("M","𝐦").replace("N","𝐧").replace("O","𝐨").replace("P","𝐩").replace("Q","𝐪").replace("R","𝐫").replace("S","𝐬").replace("T","𝐭").replace("U","𝐮").replace("V","𝐯").replace("W","𝐰").replace("X","𝐱").replace("Y","𝐲").replace("Z","𝐳")
            WA31 = text.replace('a','𝒂').replace("b","𝒃").replace("c","𝒄").replace("d","𝒅").replace("e","𝒆").replace("f","𝒇").replace("g","𝒈").replace("h","𝒉").replace("i","𝒊").replace("j","𝒋").replace("k","𝒌").replace("l","𝒍").replace("m","𝒎").replace("n","𝒏").replace("o","𝒐").replace("p","𝒑").replace("q","𝒒").replace("r","𝒓").replace("s","𝒔").replace("t","𝒕").replace("u","𝒖").replace("v","𝒗").replace("w","𝒘").replace("x","𝒙").replace("y","𝒚").replace("z","𝒛").replace("A","𝒂").replace("B","𝒃").replace("C","𝒄").replace("D","??").replace("E","𝒆").replace("F","𝒇").replace("G","𝒈").replace("H","𝒉").replace("I","𝒊").replace("J","𝒋").replace("K","𝒌").replace("L","𝒍").replace("M","𝒎").replace("N","𝒏").replace("O","𝒐").replace("P","𝒑").replace("Q","𝒒").replace("R","𝒓").replace("S","𝒔").replace("T","𝒕").replace("U","𝒖").replace("V","𝒗").replace("W","𝒘").replace("X","𝒙").replace("Y","𝒚").replace("Z","𝒛")
            WA32 = text.replace('a','𝗮').replace("b","𝗯").replace("c","𝗰").replace("d","𝗱").replace("e","𝗲").replace("f","𝗳").replace("g","𝗴").replace("h","𝗵").replace("i","𝗶").replace("j","𝗷").replace("k","𝗸").replace("l","𝗹").replace("m","𝗺").replace("n","𝗻").replace("o","𝗼").replace("p","𝗽").replace("q","𝗾").replace("r","𝗿").replace("s","𝘀").replace("t","𝘁").replace("u","𝘂").replace("v","𝘃").replace("w","𝘄").replace("x","𝘅").replace("y","𝘆").replace("z","𝘇").replace("A","𝗔").replace("B","𝗕").replace("C","𝗖").replace("D","𝗗").replace("E","𝗘").replace("F","𝗙").replace("G","𝗚").replace("H","𝗛").replace("I","𝗜").replace("J","𝗝").replace("K","𝗞").replace("L","𝗟").replace("M","𝗠").replace("N","𝗡").replace("O","𝗢").replace("P","𝗣").replace("Q","𝗤").replace("R","𝗥").replace("S","𝗦").replace("T","𝗧").replace("U","𝗨").replace("V","𝗩").replace("W","𝗪").replace("X","𝗫").replace("Y","𝗬").replace("Z","𝗭")
            WA33 = text.replace('a','𝙖').replace("b","𝙗").replace("c","𝙘").replace("d","𝙙").replace("e","𝙚").replace("f","𝙛").replace("g","𝙜").replace("h","𝙝").replace("i","𝙞").replace("j","𝙟").replace("k","𝙠").replace("l","𝙡").replace("m","𝙢").replace("n","𝙣").replace("o","𝙤").replace("p","𝙥").replace("q","𝙦").replace("r","𝙧").replace("s","𝙨").replace("t","𝙩").replace("u","𝙪").replace("v","𝙫").replace("w","𝙬").replace("x","𝙭").replace("y","𝙮").replace("z","𝙯").replace("A","𝙖").replace("B","𝙗").replace("C","𝙘").replace("D","𝙙").replace("E","𝙚").replace("F","𝙛").replace("G","𝙜").replace("H","𝙝").replace("I","𝙞").replace("J","𝙟").replace("K","𝙠").replace("L","𝙡").replace("M","𝙢").replace("N","𝙣").replace("O","𝙤").replace("P","𝙥").replace("Q","𝙦").replace("R","𝙧").replace("S","𝙨").replace("T","𝙩").replace("U","𝙪").replace("V","𝙫").replace("W","𝙬").replace("X","𝙭").replace("Y","𝙮").replace("Z","𝙯")
            WA34 = text.replace('a','𝐀').replace("b","𝐁").replace("c","𝐂").replace("d","𝐃").replace("e","𝐄").replace("f","??").replace("g","𝐆").replace("h","𝐇").replace("i","𝐈").replace("j","𝐉").replace("k","𝐊").replace("l","𝐋").replace("m","𝐌").replace("n","𝐍").replace("o","𝐎").replace("p","𝐏").replace("q","𝐐").replace("r","𝐑").replace("s","𝐒").replace("t","𝐓").replace("u","𝐔").replace("v","𝐕").replace("w","𝐖").replace("x","𝐗").replace("y","𝐘").replace("z","𝐙").replace("A","𝐀").replace("B","𝐁").replace("C","𝐂").replace("D","𝐃").replace("E","𝐄").replace("F","𝐅").replace("G","𝐆").replace("H","𝐇").replace("I","𝐈").replace("J","𝐉").replace("K","𝐊").replace("L","𝐋").replace("M","𝐌").replace("N","𝐍").replace("O","𝐎").replace("P","𝐏").replace("Q","𝐐").replace("R","𝐑").replace("S","𝐒").replace("T","𝐓").replace("U","𝐔").replace("V","𝐕").replace("W","𝐖").replace("X","𝐗").replace("Y","𝐘").replace("Z","𝐙")
            WA35 = text.replace('a','𝑨').replace("b","𝑩").replace("c","𝑪").replace("d","𝑫").replace("e","𝑬").replace("f","𝑭").replace("g","𝑮").replace("h","𝑯").replace("i","𝑰").replace("j","𝑱").replace("k","𝑲").replace("l","𝑳").replace("m","𝑴").replace("n","𝑵").replace("o","𝑶").replace("p","𝑷").replace("q","𝑸").replace("r","𝑹").replace("s","𝑺").replace("t","𝑻").replace("u","𝑼").replace("v","𝑽").replace("w","𝑾").replace("x","𝑿").replace("y","𝒀").replace("z","𝒁").replace("A","𝑨").replace("B","𝑩").replace("C","𝑪").replace("D","𝑫").replace("E","𝑬").replace("F","𝑭").replace("G","𝑮").replace("H","𝑯").replace("I","𝑰").replace("J","𝑱").replace("K","𝑲").replace("L","𝑳").replace("M","𝑴").replace("N","𝑵").replace("O","𝑶").replace("P","𝑷").replace("Q","𝑸").replace("R","𝑹").replace("S","𝑺").replace("T","𝑻").replace("U","𝑼").replace("V","𝑽").replace("W","𝑾").replace("X","𝑿").replace("Y","𝒀").replace("Z","𝒁")
            WA36 = text.replace('a','𝘼').replace("b","𝘽").replace("c","𝘾").replace("d","𝘿").replace("e","𝙀").replace("f","𝙁").replace("g","𝙂").replace("h","𝙃").replace("i","𝙄").replace("j","𝙅").replace("k","𝙆").replace("l","𝙇").replace("m","𝙈").replace("n","𝙉").replace("o","𝙊").replace("p","𝙋").replace("q","𝙌").replace("r","𝙍").replace("s","𝙎").replace("t","𝙏").replace("u","𝙐").replace("v","𝙑").replace("w","𝙒").replace("x","𝙓").replace("y","𝙔").replace("z","𝙕").replace("A","𝘼").replace("B","𝘽").replace("C","𝘾").replace("D","𝘿").replace("E","𝙀").replace("F","𝙁").replace("G","𝙂").replace("H","𝙃").replace("I","𝙄").replace("J","𝙅").replace("K","𝙆").replace("L","𝙇").replace("M","𝙈").replace("N","𝙉").replace("O","𝙊").replace("P","𝙋").replace("Q","𝙌").replace("R","𝙍").replace("S","𝙎").replace("T","𝙏").replace("U","𝙐").replace("V","𝙑").replace("W","𝙒").replace("X","𝙓").replace("Y","𝙔").replace("Z","𝙕")
            WA37 = text.replace('a','𝗔').replace("b","𝗕").replace("c","𝗖").replace("d","𝗗").replace("e","𝗘").replace("f","𝗙").replace("g","𝗚").replace("h","𝗛").replace("i","𝗜").replace("j","𝗝").replace("k","𝗞").replace("l","𝗟").replace("m","𝗠").replace("n","𝗡").replace("o","𝗢").replace("p","𝗣").replace("q","𝗤").replace("r","𝗥").replace("s","𝗦").replace("t","𝗧").replace("u","𝗨").replace("v","𝗩").replace("w","𝗪").replace("x","𝗫").replace("y","𝗬").replace("z","𝗭").replace("A","𝗔").replace("B","𝗕").replace("C","𝗖").replace("D","𝗗").replace("E","𝗘").replace("F","𝗙").replace("G","𝗚").replace("H","𝗛").replace("I","𝗜").replace("J","𝗝").replace("K","𝗞").replace("L","𝗟").replace("M","𝗠").replace("N","𝗡").replace("O","𝗢").replace("P","𝗣").replace("Q","𝗤").replace("R","𝗥").replace("S","𝗦").replace("T","𝗧").replace("U","𝗨").replace("V","𝗩").replace("W","𝗪").replace("X","𝗫").replace("Y","𝗬").replace("Z","𝗭")
            dd.remove(int(chat.id))
            return await event.client.send_message(chat.id, f"**ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗦𝘁𝘆𝗹𝗲 - زخـرفـه تمبلـر**\n**⋆┄─┄─┄─┄┄─┄─┄─┄─┄⋆**\n{WA1} {smiile1}\n{WA2} {smiile2}\n{WA3} {smiile3}\n{WA4} {smiile4}\n{WA5} {smiile5}\n{WA6} {smiile6}\n{WA7} {smiile7}\n{WA8} {smiile8}\n{WA9} {smiile9}\n{WA10} {smiile10}\n{WA11} {smiile11}\n{WA12} {smiile12}\n{WA13} {smiile13}\n{WA14} {smiile14}\n{WA15} {smiile15}\n{WA16} {smiile16}\n{WA17} {smiile17}\n{WA18} {smiile18}\n{WA19} {smiile19}\n{WA20} {smiile20}\n{WA21} {smiile21}\n{WA22} {smiile22}\n{WA23} {smiile23}\n{WA24} {smiile24}\n{WA25} {smiile25}\n{WA26} {smiile26}\n{WA27} {smiile27}\n{WA28} {smiile28}\n{WA29} {smiile29}\n{WA30} {smiile30}\n{WA31} {smiile31}\n{WA32} {smiile32}\n{WA33} {smiile33}\n{WA34} {smiile34}\n{WA35} {smiile35}\n{WA36} {smiile36}\n{WA37} {smiile37}")
        reply_to = await reply_id(event)
        if reply_to is None:
            return
        users = get_user_id(reply_to)
        if users is None:
            return
        for usr in users:
            user_id = int(usr.chat_id)
            reply_msg = usr.reply_id
            user_name = usr.first_name
            break
        if user_id is not None:
            try:
                if event.media:
                    msg = await event.client.send_file(
                        user_id, event.media, caption=event.text, reply_to=reply_msg
                    )
                else:
                    msg = await event.client.send_message(
                        user_id, event.text, reply_to=reply_msg, link_preview=False
                    )
            except UserIsBlockedError:
                return await event.reply("𝗧𝗵𝗶𝘀 𝗯𝗼𝘁 𝘄𝗮𝘀 𝗯𝗹𝗼𝗰𝗸𝗲𝗱 𝗯𝘆 𝘁𝗵𝗲 𝘂𝘀𝗲𝗿. ❌")
            except Exception as e:
                return await event.reply(f"**- خطـأ:**\n`{e}`")
            try:
                add_user_to_db(
                    reply_to, user_name, user_id, reply_msg, event.id, msg.id
                )
            except Exception as e:
                LOGS.error(str(e))


@l313l.bot_cmd(edited=True)
async def bot_pms_edit(event):  # sourcery no-metrics
    chat = await event.get_chat()
    if not event.is_private:
        return
    if check_is_black_list(chat.id):
        return
    if chat.id != Config.OWNER_ID and int(chat.id) in tt:
        users = get_user_reply(event.id)
        if users is None:
            return
        if reply_msg := next(
            (user.message_id for user in users if user.chat_id == str(chat.id)),
            None,
        ):
            await event.client.send_message(
                Config.OWNER_ID,
                f"⬆️ **هـذه الرسـاله تم تعديلهـا بواسطـة المستخـدم ** {_format.mentionuser(get_display_name(chat) , chat.id)} كـ :",
                reply_to=reply_msg,
            )
            msg = await event.forward_to(Config.OWNER_ID)
            try:
                add_user_to_db(msg.id, get_display_name(chat), chat.id, event.id, 0, 0)
            except Exception as e:
                LOGS.error(str(e))
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"**- سيـدي المطـور  🧑🏻‍💻**\n**- حدث خطـأ أثنـاء اشتـراك احـد المستخدميـن في البـوت المسـاعـد الخاص بك.**\n`{str(e)}`",
                    )

    else:
        reply_to = await reply_id(event)
        if reply_to is not None:
            users = get_user_id(reply_to)
            result_id = 0
            if users is None:
                return
            for usr in users:
                if event.id == usr.logger_id:
                    user_id = int(usr.chat_id)
                    reply_msg = usr.reply_id
                    result_id = usr.result_id
                    break
            if result_id != 0:
                try:
                    await event.client.edit_message(
                        user_id, result_id, event.text, file=event.media
                    )
                except Exception as e:
                    LOGS.error(str(e))


@tgbot.on(events.MessageDeleted)
async def handler(event):
    if not event.is_private:
        return
    for msg_id in event.deleted_ids:
        users_1 = get_user_reply(msg_id)
        users_2 = get_user_logging(msg_id)
        if users_2 is not None:
            result_id = 0
            for usr in users_2:
                if msg_id == usr.logger_id:
                    user_id = int(usr.chat_id)
                    result_id = usr.result_id
                    break
            if result_id != 0:
                try:
                    await event.client.delete_messages(user_id, result_id)
                except Exception as e:
                    LOGS.error(str(e))
        if users_1 is not None:
            reply_msg = next(
                (
                    user.message_id
                    for user in users_1
                    if user.chat_id != Config.OWNER_ID
                ),
                None,
            )

            try:
                if reply_msg:
                    users = get_user_id(reply_msg)
                    for usr in users:
                        user_id = int(usr.chat_id)
                        user_name = usr.first_name
                        break
                    if check_is_black_list(user_id):
                        return
                    await event.client.send_message(
                        Config.OWNER_ID,
                        f"⬆️ **هـذه الرسـاله لقـد تـم حذفهـا بواسطـة المستخـدم ** {_format.mentionuser(user_name , user_id)}.",
                        reply_to=reply_msg,
                    )
            except Exception as e:
                LOGS.error(str(e))


@l313l.bot_cmd(pattern="^/info$", from_users=Config.OWNER_ID)
async def bot_start(event):
    reply_to = await reply_id(event)
    if not reply_to:
        return await event.reply("**- بالـرد على رسـالة الشخـص للحصول على المعلومات . . .**")
    info_msg = await event.client.send_message(
        event.chat_id,
        "**🔎 جـارِ البحث عن هـذا المستخـدم في قاعدة البيـانات الخاصـة بك ...**",
        reply_to=reply_to,
    )
    users = get_user_id(reply_to)
    if users is None:
        return await info_msg.edit(
            "**- هنـالك خطـأ:** \n`عـذراً! ، لا يمكن العثور على هذا المستخدم في قاعدة البيانات الخاصة بك :(`"
        )
    for usr in users:
        user_id = int(usr.chat_id)
        user_name = usr.first_name
        user_naam = f"@{usr.username}" if usr.username else "لايوجـد"
        break
    if user_id is None:
        return await info_msg.edit(
            "**- هنـالك خطـأ :** \n`عـذراً! ، لا يمكن العثور على هذا المستخدم في قاعدة البيانات الخاصة بك :(`"
        )
    uinfo = f"**- هـذه الرسالـة ارسلـت بواسـطة** 👤\
            \n\n**الاسـم:** {user_name}\
            \n**الايـدي:** `{user_id}`\
            \n**اليـوزر:** {user_naam}"
    await info_msg.edit(uinfo)


async def send_flood_alert(user_) -> None:
    # sourcery no-metrics
    buttons = [
        (
            Button.inline("🚫  حظـر", data=f"bot_pm_ban_{user_.id}"),
            Button.inline(
                "➖ تعطيـل مكـافح التكـرار",
                data="toggle_bot-antiflood_off",
            ),
        )
    ]
    found = False
    if FloodConfig.ALERT and (user_.id in FloodConfig.ALERT.keys()):
        found = True
        try:
            FloodConfig.ALERT[user_.id]["count"] += 1
        except KeyError:
            found = False
            FloodConfig.ALERT[user_.id]["count"] = 1
        except Exception as e:
            if BOTLOG:
                await l313l.tgbot.send_message(
                    BOTLOG_CHATID,
                    f"**- خطـأ :**\nعنـد تحديث عدد مرات التكرار\n`{e}`",
                )

        flood_count = FloodConfig.ALERT[user_.id]["count"]
    else:
        flood_count = FloodConfig.ALERT[user_.id]["count"] = 1

    flood_msg = (
        r"⚠️ **#تحذيـر_التكـرار**"
        "\n\n"
        f"  الايدي: `{user_.id}`\n"
        f"  الاسم: {get_display_name(user_)}\n"
        f"  👤 الحساب: {_format.mentionuser(get_display_name(user_), user_.id)}"
        f"\n\n**قام بالتكـرار بالبوت المساعد** ->  [ Flood rate ({flood_count}) ]\n"
        "__Quick Action__: Ignored from bot for a while."
    )

    if found:
        if flood_count >= FloodConfig.AUTOBAN:
            if user_.id in Config.SUDO_USERS:
                sudo_spam = (
                    f"**- المطـور المسـاعد :** {_format.mentionuser(user_.first_name , user_.id)}:\n**- ايدي المطـور:** {user_.id}\n\n"
                    "**- قـام بالتكـرار في بوتك المسـاعد,لتنزيلـه استخـدم الامـر** تنزيل مطور + الايدي"
                )
                if BOTLOG:
                    await l313l.tgbot.send_message(BOTLOG_CHATID, sudo_spam)
            else:
                await ban_user_from_bot(
                    user_,
                    f"**- الحظـر التلقـائي لمكافـح التكـرار في البـوت**  [exceeded flood rate of ({FloodConfig.AUTOBAN})]",
                )
                FloodConfig.USERS[user_.id].clear()
                FloodConfig.ALERT[user_.id].clear()
                FloodConfig.BANNED_USERS.remove(user_.id)
            return
        fa_id = FloodConfig.ALERT[user_.id].get("fa_id")
        if not fa_id:
            return
        try:
            msg_ = await l313l.tgbot.get_messages(BOTLOG_CHATID, fa_id)
            if msg_.text != flood_msg:
                await msg_.edit(flood_msg, buttons=buttons)
        except Exception as fa_id_err:
            LOGS.debug(fa_id_err)
            return
    else:
        if BOTLOG:
            fa_msg = await l313l.tgbot.send_message(
                BOTLOG_CHATID,
                flood_msg,
                buttons=buttons,
            )
        try:
            chat = await l313l.tgbot.get_entity(BOTLOG_CHATID)
            await l313l.tgbot.send_message(
                Config.OWNER_ID,
                f"⚠️  **[تحذيـر مكافـح التكـرار](https://t.me/c/{chat.id}/{fa_msg.id})**",
            )
        except UserIsBlockedError:
            if BOTLOG:
                await l313l.tgbot.send_message(BOTLOG_CHATID, "**- قم بالغـاء حظـر بوتك المسـاعـد ؟!**")
    if FloodConfig.ALERT[user_.id].get("fa_id") is None and fa_msg:
        FloodConfig.ALERT[user_.id]["fa_id"] = fa_msg.id


@l313l.tgbot.on(CallbackQuery(data=re.compile(b"bot_pm_ban_([0-9]+)")))
@check_owner
async def bot_pm_ban_cb(c_q: CallbackQuery):
    user_id = int(c_q.pattern_match.group(1))
    try:
        user = await l313l.get_entity(user_id)
    except Exception as e:
        await c_q.answer(f"- خطـأ :\n{e}")
    else:
        await c_q.answer(f"- جـارِ حظـر -> {user_id} ...", alert=False)
        await ban_user_from_bot(user, "Spamming Bot")
        await c_q.edit(f"**- الايـدي :** {user_id} \n**- تم الحظـر .. بنجـاح ✅**")


def time_now() -> Union[float, int]:
    return datetime.timestamp(datetime.now())


@pool.run_in_thread
def is_flood(uid: int) -> Optional[bool]:
    """Checks if a user is flooding"""
    FloodConfig.USERS[uid].append(time_now())
    if (
        len(
            list(
                filter(
                    lambda x: time_now() - int(x) < FloodConfig.SECONDS,
                    FloodConfig.USERS[uid],
                )
            )
        )
        > FloodConfig.MESSAGES
    ):
        FloodConfig.USERS[uid] = list(
            filter(
                lambda x: time_now() - int(x) < FloodConfig.SECONDS,
                FloodConfig.USERS[uid],
            )
        )
        return True


@l313l.tgbot.on(CallbackQuery(data=re.compile(b"toggle_bot-antiflood_off$")))
@check_owner
async def settings_toggle(c_q: CallbackQuery):
    if gvarstatus("bot_antif") is None:
        return await c_q.answer("**- مكافـح التكـرار التلقـائي بالبـوت .. معطـل مسبقـاً**", alert=False)
    delgvar("bot_antif")
    await c_q.answer("Bot Antiflood disabled.", alert=False)
    await c_q.edit("**- مكافـح التكـرار التلقـائي بالبـوت .. تم تعطيلـه بنجـاح✓**")


@l313l.tgbot.on(CallbackQuery(data=re.compile(b"ttk_bot-1$")))
async def settings_toggle(c_q: CallbackQuery):
    await c_q.edit(
        """**- مرحبـاً بك عـزيـزي ✍🏻**
**- عنـد تفعيـل وضـع التواصـل 📨**
**- سـوف يتم تحويـل البوت الى بوت تواصـل**
**- بمعنى اي رسالة سوف ترسلهـا هنـا 💌**
**- سوف يتلقاها مالك البـوت 📫**
﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎
**- لـ التفعيـل او لـ تعطيـل استخـدم الازرار بالاسفـل 🛃**
.""",

        buttons=[
            [
                Button.inline("تفعيـل التواصـل", data="ttk_bot-on")
            ],
            [
                Button.inline("تعطيـل التواصـل", data="ttk_bot-off")
            ],
            [
                Button.inline("رجــوع", data="styleback")
            ],
        ],
    link_preview=False)


@l313l.tgbot.on(CallbackQuery(data=re.compile(b"zzk_bot-on$")))
async def settings_toggle(c_q: CallbackQuery):
    dd.append(int(c_q.query.user_id))
    await c_q.edit(
        "**- ارسـل الان الاسـم الذي تريـد زخرفتـه بالانكـلـش ✓**\n\n"
        "**- لـ الالغـاء ارسـل /cancle**",
        buttons=[
            [Button.inline("رجوع ↩️", data="decor_main_menu")]
        ]
    )


@l313l.tgbot.on(CallbackQuery(data=re.compile(b"ttk_bot-on$")))
async def settings_toggle(c_q: CallbackQuery):
    if c_q.query.user_id in tt:
        return await c_q.answer("**- وضـع التواصـل .. مفعـل مسبقـاً**", alert=False)
    tt.append(int(c_q.query.user_id))
    await c_q.edit(
        """**- تم تفعيـل وضع التواصل ✓**
**- كل ماترسلـه الان سـوف يرسـل لـ مالك البـوت 📨**
﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎
.""",

        buttons=[
            [Button.inline("تعطيل وضع التواصل", data="ttk_bot-off")],
        ],
    link_preview=False)


@l313l.tgbot.on(CallbackQuery(data=re.compile(b"ttk_bot-off$")))
async def settings_toggle(c_q: CallbackQuery):
    if c_q.query.user_id not in tt:
        return await c_q.answer("**- وضـع التواصـل .. معطـل مسبقـاً**", alert=False)
    tt.remove(int(c_q.query.user_id))
    await c_q.edit("**- تم الخروج من وضع التواصل ✓**\n\n**- لـ البدء ارسـل /start**")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"decor_main_menu$")))
async def decor_main_menu_handler(event):
    await event.edit(
        """**• مرحبـاً بك عـزيـزي 🫂

• في قسـم بـوت الزخرفـه 📨
• هذا القسم يحتوي على عـدة أقسـام خدميه
❶ زخـرفة انجلـش تمبلـر 🎡
❷ رمـوز تمبلـر ممطروقـه 💠
❸ جميـع زخـارف الارقـام 🌀
﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎
• لـ البـدء إستخـدم الازرار بالاسفـل ⌨
.**""",
        buttons=[
            [
                Button.inline("زخرفـة انكـلـش ✍🏻", data="zzk_bot-on")
            ],
            [
                Button.inline("رمـوز تمبلـر 1 🎨", data="zzk_bot-1"),
                Button.inline("رمـوز تمبلـر 2 🎨", data="zzk_bot-2")
            ],
            [
                Button.inline("زغـارف أرقـام 🔢", data="zzk_bot-3")
            ],
            [
                Button.inline("رجــوع ↩️", data="styleback")
            ],
        ],
        link_preview=False
    )
    
@l313l.tgbot.on(CallbackQuery(data=re.compile(b"styleback$")))
async def settings_toggle(event):
    user = await l313l.get_me()
    my_mention = f"[{user.first_name}](tg://user?id={user.id})"
    my_first = user.first_name
    my_last = user.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{user.username}" if user.username else my_mention
    if gvarstatus("START_BUTUN") is not None:
        zz_txt = "⌔ قنـاتـي ⌔"
        zz_ch = gvarstatus("START_BUTUN")
    elif user.username:
        zz_txt = "⌔ لـ التواصـل خـاص ⌔"
        zz_ch = user.username
    else:
        zz_txt = "⌔ قنـاة المـطور ⌔"
        zz_ch = "aqhvv"
    zid = 5427469031
    if gvarstatus("ZThon_Vip") is None:
        zid = 5427469031
    else:
        zid = int(gvarstatus("ZThon_Vip"))
    if event.query.user_id != Config.OWNER_ID:
        start_msg = f"**⌔ مـرحباً بـك مجـدداً ⛹🏻‍♀**\
                    \n\n**⌔ انـا البـوت الخـاص بـ** {my_fullname}\
                    \n**⌔ يمكنك التواصـل مـع مـالكـي مـن هنـا 💌.**\
                    \n**⌔ فقـط ارسـل رسـالتك وانتظـر الـرد 📨.**\
                    \n**⌔ إننـي ايضـاً بـوت زخرفـة 🎨 & حـذف حسابات ⚠️.**\
                    \n**⌔ لـ الزخرفـة او الحـذف استخـدم الازرار بالاسفـل**"
        buttons = [
            [
                Button.inline("اضغـط لـ التواصـل 🗳", data="ttk_bot-1")
            ],
            [
                Button.inline("زخـارف تمبلـر 🎡", data="decor_main_menu")
            ],
            [
                Button.inline("حـذف حسـابك ⚠️", data="zzk_bot-5")
            ],
            [
                Button.inline("الأوامـر المدفوعـة 💎", data="paid_commands_menu")
            ],
            [
                Button.url(zz_txt, f"https://t.me/{zz_ch}")
            ]
        ]
    elif event.query.user_id == Config.OWNER_ID and event.query.user_id == zid:
        start_msg = "**⌔ مـرحبـاً عـزيـزي المـالك 🧑🏻‍💻..**\n**⌔ انا البـوت المسـاعـد الخـاص بـك (تواصـل📨 + زخرفـه🎨) 🤖🦾**\n**⌔ يستطيـع اي شخص التواصل بك من خـلالي 💌**\n\n**⌔ لـ زخرفـة اسـم اضغـط الـزر بالاسفـل**\n**⌔ لرؤيـة اوامـري الخاصـه بـك اضغـط :  /help **"
        buttons = [
            [
                Button.inline("زخـارف تمبلـر 🎡", data="decor_main_menu")
            ],
            [
                Button.inline("لـ حـذف حسـابك ⚠️", data="zzk_bot-5")
            ],
            [
                Button.inline("الأوامـر المدفوعـة 💎", data="paid_commands_menu")
            ],
            [
                Button.url(zz_txt, f"https://t.me/{zz_ch}")
            ]
        ]
    else:
        start_msg = "**⌔ مـرحبـاً عـزيـزي المـالك 🧑🏻‍💻..**\n**⌔ انا البـوت المسـاعـد الخـاص بـك (تواصـل📨 + زخرفـه🎨) 🤖🦾**\n**⌔ يستطيـع اي شخص التواصل بك من خـلالي 💌**\n\n**⌔ لـ زخرفـة اسـم اضغـط الـزر بالاسفـل**\n**⌔ لرؤيـة اوامـري الخاصـه بـك اضغـط :  /help **"
        buttons = [
            [
                Button.inline("زخـارف تمبلـر 🎡", data="decor_main_menu")
            ],
            [
                Button.inline("لـ حـذف حسـابك ⚠️", data="zzk_bot-5")
            ],
            [
                Button.inline("الأوامـر المدفوعـة 💎", data="paid_commands_menu")
            ],
            [
                Button.url(zz_txt, f"https://t.me/{zz_ch}")
            ]
        ]
    await event.edit(start_msg, buttons=buttons, link_preview=False)


@l313l.tgbot.on(CallbackQuery(data=re.compile(b"zzk_bot-1$")))
async def settings_toggle(c_q: CallbackQuery):
    try:
        await c_q.edit(
            """ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗗𝗲𝗰𝗼𝗿 - **رمـوز تمبلـر** 🎡
**⋆┄─┄─┄─┄─┄─┄─┄─┄⋆**
𓅄 𓅅 𓅆 𓅇 𓅈 𓅉 𓅊 𓅋 𓅌 𓅍 𓅎 𓅏 𓅐 𓅑 𓅒 𓅓 𓅔𓅕 𓅖 𓅗 𓅘 𓅙 𓅚 𓅛 𓅜 𓅝 𓅞 𓅟 𓅠 𓅡 𓅢 𓅣 𓅤 𓅥 𓅦 𓅧 𓅨 𓅩 𓅫 𓅬 𓅭 𓅮 𓅯 𓅰 𓅱 𓅲 𓅳 𓅴 
‏𓅵 𓅶 𓅷 𓅸 𓅹 𓅺 𓅻 
‏ ☤ 𓅾 𓅿 𓆀 𓆁 𓆂

‏𓀀 𓀁 𓀂 𓀃 𓀄 𓀅 𓀆 𓀇 𓀈 𓀉 𓀊 𓀋 𓀌 𓀍 𓀎 𓀏 𓀐 𓀑 𓀒 𓀓 𓀔 𓀕 𓀖 𓀗 𓀘 𓀙 𓀚 𓀛 𓀜 𓀝 𓀞 𓀟 𓀠 𓀡 𓀢 𓀣 𓀤 𓀥 𓀦 𓀧 𓀪 𓀫 𓀬 𓀭 𓀮 𓀯 𓀰 𓀱 𓀲 𓀳 𓀴 𓀵 𓀶 𓀷 𓀸 𓀹 𓀺 𓀻 𓀼 𓀽 𓀾 𓀿 𓁀 𓁁 𓁂 𓁃 𓁄 𓁅 𓁆 𓁇 𓁈 𓁉 𓁊 𓁋 𓁌 𓁍 𓁎 𓁏 𓁐 𓁑 𓁒 𓁓 𓁔 𓁕 𓁖 𓁗 𓁘 𓁙 𓁚 𓁛 𓁜 𓁝 𓁞 𓁟 𓁠 𓁡 𓁢 𓁣 𓁤 𓁥 𓁦 𓁧 𓁨 𓁩 𓁪 𓁫 𓁬 𓁭 𓁮 𓁯 𓁰 𓁱 𓁲 𓁳 𓁴 𓁵 𓁶 𓁷 𓁸 𓁹 𓁺 𓁻 𓁼 𓁽 𓁾 𓁿 𓂀𓂅 𓂆 𓂇 𓂈 𓂉 𓂊 𓂎 𓂏 𓂐 𓂑 𓃃 𓃅 𓃆 𓃇 𓃈
𓃒 𓃓 𓃔 𓃕 𓃖 𓃗 𓃘 𓃙 𓃚 𓃛 𓃜 𓃝 𓃞 𓃟 𓃠 𓃡 𓃢 𓃣 𓃤 𓃥 𓃦 𓃧 𓃨 𓃩 𓃪 𓃫 𓃬 𓃭 𓃮 𓃯 𓃰 𓃱 𓃲 𓃳 𓃴 𓃵 𓃶 𓃷 𓃸 𓃹 𓃺 𓃻 𓃼 𓃽 𓃾 𓃿 𓄀 𓄁 𓄂 𓄃 𓄄 𓄅 𓄆 𓄇 𓄈 𓄉 𓄊 𓄋 𓄌 𓄍 𓄎 𓄏 𓄐 𓄑 𓄒 𓄓 𓄔 𓄕 𓄖 𓄙 𓄚 𓄛 𓄜 𓄝 𓄞 𓄟 𓄠 𓄡 𓄢 𓄣 𓄤 𓄥 𓄦 𓄧 𓄨 𓄩 𓄪 𓄫 𓄬 𓄭 𓄮 𓄯 𓄰 𓄱 𓄲 𓄳 𓄴 𓄵 𓄶 𓄷 𓄸 𓄹 𓄺   𓄼 𓄽 𓄾 𓄿 𓅀 𓅁 𓅂 𓅃 𓅄 𓅅 𓅆 𓅇 𓅈 𓅉 𓅊 𓅋 𓅌 𓅍 𓅎 𓅏 𓅐 𓅑 𓅒 𓅓 𓅔 𓅕 𓅖 𓅗 𓅘 𓅙 𓅚 𓅛 𓅜 𓅝 𓅞 𓅟 𓅠 𓅡 𓅢 𓅣 𓅤 𓅥 𓅦 𓅧 𓅨 𓅩 𓅪 𓅫 𓅬 𓅭 𓅮 𓅯 𓅰 𓅱 𓅲 𓅳 𓅴 𓅵 𓅶 𓅷 𓅸 𓅹 𓅺 𓅻 𓅼 𓅽 𓅾 𓅿 𓆀 𓆁 𓆂 𓆃 𓆄 𓆅 𓆆 𓆇 𓆈 𓆉 𓆊 𓆋 𓆌 𓆍 𓆎 𓆐 𓆑 𓆒 𓆓 𓆔 𓆕 𓆖 𓆗 𓆘 𓆙 𓆚 𓆛 𓆜 𓆝 𓆞 𓆟 𓆠 𓆡 𓆢 𓆣 𓆤 𓆥 𓆦 𓆧 𓆨 𓆩𓆪 𓆫 𓆬 𓆭 𓆮 𓆯 𓆰 𓆱 𓆲 𓆳 𓆴 𓆵 𓆶 𓆷 𓆸 𓆹 𓆺 𓆻 𓆼 𓆽 𓆾 𓆿 𓇀 𓇁 𓇂 𓇃 𓇄 𓇅 𓇆 𓇇 𓇈 𓇉 𓇊 𓇋 𓇌 𓇍 𓇎 𓇏 𓇐 𓇑 𓇒 𓇓 𓇔 𓇕 𓇖 𓇗 𓇘 𓇙 𓇚 𓇛 𓇜 𓇝 𓇞 𓇟 𓇠 𓇡 𓇢 𓇣 𓇤 𓇥 𓇦 𓇧 𓇨 𓇩 𓇪 𓇫 𓇬 𓇭 𓇮 𓇯 𓇰 𓇱 𓇲 𓇳 𓇴 𓇵 𓇶 𓇷 𓇸 𓇹 𓇺 𓇻 𓇼 𓇾 𓇿 𓈀 𓈁 𓈂 𓈃 𓈄 𓈅 𓈆 𓈇 𓈈 𓈉 𓈊 𓈋 𓈌 𓈍 𓈎 𓈏 𓈐 𓈑 𓈒 𓈓 𓈔 𓈕 𓈖 𓈗 𓈘 𓊈 𓊉 𓊊 𓊋 𓊌 𓊍 𓊎 𓊏 𓊐 
𓊑 𓊒 𓊔 𓊕 𓊘 𓊙 𓊚 𓊛 𓊜 𓊝 𓊠 𓊡 𓊢 𓊣 𓊤 𓊥 𓊦 𓊧 𓊨 𓊩 𓊪 𓊫 𓊬 𓊭 𓊮 𓊯 𓊰 ?? ?? 𓊳 𓊴 𓊵 𓊶 𓊷 𓊸 𓊹 𓊺 𓊻 𓊼 𓊿 𓋀 𓋁 𓋂 𓋃 𓋄 𓋅 𓋆 𓋇 𓋈 𓋉 𓋊 𓋋 𓋌 𓋍 𓋎 𓋏 𓋐 𓋑 𓋒 𓋓 𓋔 𓋕 𓋖 𓋗 𓋘 𓋙 𓋚 𓋛 𓋜 𓋝 𓋞 𓋟 𓌰 𓌱 𓌲 𓌳 𓌴 𓌵 𓌶 𓌷 𓌸 𓌹 𓌺 𓌻 𓌼 𓌽 𓌾 𓌿 𓍀 𓍁 𓍂 𓍃 𓍄 𓍅 𓍆 𓍇 𓍈 𓍉 𓍊 𓍋 𓍌 𓍍 𓍎 𓍏 𓍐 𓍑 𓍒 𓍓 𓍔 𓍕 𓍖 𓍗 𓍘 𓍙 𓍚 𓍛 𓍜 𓍝 𓍞 𓍟 𓍠 𓍡 𓍢 𓍣 𓍤 𓍬 𓍭 𓍮 𓍯 𓍰 𓍱 𓍲 𓍳 𓍴 𓍵 𓍶 𓍷 𓍸 𓍹 𓍺 𓍻 𓍼 𓍽 𓍾 𓍿 𓎀 𓎁 𓎂 𓎃 𓎄 𓎅 𓎆 𓎓 𓎔 𓎕 𓎖 𓎗 𓎘 𓎙 𓎚 𓎛 𓎜 𓎝 𓎞 𓎟 𓎠 𓎡 𓏋 𓏌 𓏍 𓏎 𓏏 𓏐 𓏑 𓏒 𓏓 
‏ 𓏕 𓏖 𓏗 𓏘 𓏙 𓏚 𓏛 𓏜 𓏝 𓏞 𓏟 𓏠 𓏡 𓏢 𓏣 𓏤 𓏥 𓏦 𓏧 𓏨 𓏩 𓏪 𓏫 𓏬 𓏭 𓏮 𓏯 𓏰 𓏱 𓏲 𓏳 𓏴 𓏶 𓏷 𓏸 𓏹 𓏺 𓏻 𓏼 𓏽 𓏾 𓏿 𓐀 𓐁 𓐂 𓐃 𓐄 𓐅 𓐆

- 𖣨 ، ෴ ، 𖡺  ، 𖣐 ، ✜ ، ✘ ، 𖡻 ،
- ༄ ، ༺༻ ، ༽༼ ،  ╰☆╮،  
- ɵ‌᷄ˬɵ‌᷅ ، ‏⠉‌⃝ ، ࿇࿆ ، ꔚ، ま ، ☓ ،
{𓆉 . 𓃠 .𓅿 . 𓃠 . 𓃒 . 𓅰 . 𓃱 . 𓅓 . 𐂃  . ꕥ  . ⌘ . ♾ .    ꙰  .  . ᤑ .  ﾂ .
____
✦ ,✫ ,✯, ✮ ,✭ ,✰, ✬ ,✧, ✤, ❅ , 𒀭,✵ , ✶ , ✷ , ✸ , ✹ ,⧫, . 𐂂 }

-〘 𖢐 ، 𒍦 ، 𒍧 ، 𖢣 ، 𝁫 ، 𒍭 ، 𝁅 ، 𝁴 ، 𒍮 ، 𝁵 ، 𝀄 ، 𓏶 ، 𓏧 ، 𓏷 ، 𓏯 ، 𓏴 ، 𓏳 ، 𓏬 ، 𓏦 ، 𓏵 ، 𓏱 ، ᳱ ، ᯼ ، 𐃕 ، ᯥ ، ᯤ ، ᯾ ، ᳶ ، ᯌ ، ᢆ ،

ᥦ ، ᨙ ، ᨚ  ، ᨔ  ، ⏢ ، ⍨ ، ⍃ ، ⏃ ، ⍦ ، ⏕ ، ⏤ ، ⏁ ، ⏂ ، ⏆ ، ⌳ ، ࿅ ، ࿕ ، ࿇ ، ᚙ ، ࿊ ، ࿈ ، ྿ ،
࿂ ، ࿑ ،  ᛥ ، ࿄ ، 𐀁 ، 𐀪 ، 𐀔 ، 𐀴 ، 𐀤 ، 𐀦 ، 𐀂 ، 𐀣 ، 𐀢 ، 𐀶 ، 𐀷 ، 𐂭 ، 𐂦 ، 𐂐 ، 𐂅 ، 𐂡 ، 𐂢 ، 𐂠 ، 𐂓 ، 𐂑 ، 𐃸 ، 𐃶 ، 𐂴 ، 𐃭 ، 𐃳 ، 𐃣 ، 𐂰 ، 𐃟 ، 𐃐 ، 𐃙 ، 𐃀 ، 𐇮 ، 𐇹 ، 𐇲 ، 𐇩 ، 𐇪 ، 𐇶 ، 𐇻 ، 𐇡 ، 𐇸 ، 𐇣 ، 𐇤 ، 𐎅 ، 𐏍 ، 𐎃 ، 𐏒 ، 𐎄 ، 𐏕 〙.

╔ ╗. 𓌹  𓌺 .〝  〞. ‹ ›  .「  」. ‌‏𓂄‏ ‌‌‏𓂁
〖 〗. 《》 .  < > . « »  . ﹄﹃""",

            buttons=[
                [Button.inline("رجوع", data="decor_main_menu")],
            ],
        link_preview=False)
    except Exception:
        await c_q.client.send_message(
            c_q.query.user_id,
            """ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗗𝗲𝗰𝗼𝗿 - **رمـوز تمبلـر** 🎡
**⋆┄─┄─┄─┄─┄─┄─┄─┄⋆**
𓅄 𓅅 𓅆 𓅇 𓅈 𓅉 𓅊 𓅋 𓅌 𓅍 𓅎 𓅏 𓅐 𓅑 𓅒 𓅓 𓅔𓅕 𓅖 𓅗 𓅘 𓅙 𓅚 𓅛 𓅜 𓅝 𓅞 𓅟 𓅠 𓅡 𓅢 𓅣 𓅤 𓅥 𓅦 𓅧 𓅨 𓅩 𓅫 𓅬 𓅭 𓅮 𓅯 𓅰 𓅱 𓅲 𓅳 𓅴 
‏𓅵 𓅶 𓅷 𓅸 𓅹 𓅺 𓅻 
‏ ☤ 𓅾 𓅿 𓆀 𓆁 𓆂

‏𓀀 𓀁 𓀂 𓀃 𓀄 𓀅 𓀆 𓀇 𓀈 𓀉 𓀊 𓀋 𓀌 𓀍 𓀎 𓀏 𓀐 𓀑 𓀒 𓀓 𓀔 𓀕 𓀖 𓀗 𓀘 𓀙 𓀚 𓀛 𓀜 𓀝 𓀞 𓀟 𓀠 𓀡 𓀢 𓀣 𓀤 𓀥 𓀦 𓀧 𓀪 𓀫 𓀬 𓀭 𓀮 𓀯 𓀰 𓀱 𓀲 𓀳 𓀴 𓀵 𓀶 𓀷 𓀸 𓀹 𓀺 𓀻 𓀼 𓀽 𓀾 𓀿 𓁀 𓁁 𓁂 𓁃 𓁄 𓁅 𓁆 𓁇 𓁈 𓁉 𓁊 𓁋 𓁌 𓁍 𓁎 𓁏 𓁐 𓁑 𓁒 𓁓 𓁔 𓁕 𓁖 𓁗 𓁘 𓁙 𓁚 𓁛 𓁜 𓁝 𓁞 𓁟 𓁠 𓁡 𓁢 𓁣 𓁤 𓁥 𓁦 𓁧 𓁨 𓁩 𓁪 𓁫 𓁬 𓁭 𓁮 𓁯 𓁰 𓁱 𓁲 𓁳 𓁴 𓁵 𓁶 𓁷 𓁸 𓁹 𓁺 𓁻 𓁼 𓁽 𓁾 𓁿 𓂀𓂅 𓂆 𓂇 𓂈 𓂉 𓂊 𓂎 𓂏 𓂐 𓂑 𓃃 𓃅 𓃆 𓃇 𓃈
𓃒 𓃓 𓃔 𓃕 𓃖 𓃗 𓃘 𓃙 𓃚 𓃛 𓃜 𓃝 𓃞 𓃟 𓃠 𓃡 𓃢 𓃣 𓃤 𓃥 𓃦 𓃧 𓃨 𓃩 𓃪 𓃫 𓃬 𓃭 𓃮 𓃯 𓃰 𓃱 𓃲 𓃳 𓃴 𓃵 𓃶 𓃷 𓃸 𓃹 𓃺 𓃻 𓃼 𓃽 𓃾 𓃿 𓄀 𓄁 𓄂 𓄃 𓄄 𓄅 𓄆 𓄇 𓄈 𓄉 𓄊 𓄋 𓄌 𓄍 𓄎 𓄏 𓄐 𓄑 𓄒 𓄓 𓄔 𓄕 𓄖 𓄙 𓄚 𓄛 𓄜 𓄝 𓄞 𓄟 𓄠 𓄡 𓄢 𓄣 𓄤 𓄥 𓄦 𓄧 𓄨 𓄩 𓄪 𓄫 𓄬 𓄭 𓄮 𓄯 𓄰 𓄱 𓄲 𓄳 𓄴 𓄵 𓄶 𓄷 𓄸 𓄹 𓄺   𓄼 𓄽 𓄾 𓄿 𓅀 𓅁 𓅂 𓅃 𓅄 𓅅 𓅆 𓅇 𓅈 𓅉 𓅊 𓅋 𓅌 𓅍 𓅎 𓅏 𓅐 𓅑 𓅒 𓅓 𓅔 𓅕 𓅖 𓅗 𓅘 𓅙 𓅚 𓅛 𓅜 𓅝 𓅞 𓅟 𓅠 𓅡 𓅢 𓅣 𓅤 𓅥 𓅦 𓅧 𓅨 𓅩 𓅪 𓅫 𓅬 𓅭 𓅮 𓅯 𓅰 𓅱 𓅲 𓅳 𓅴 𓅵 𓅶 𓅷 𓅸 𓅹 𓅺 𓅻 𓅼 𓅽 𓅾 𓅿 𓆀 𓆁 𓆂 𓆃 𓆄 𓆅 𓆆 𓆇 𓆈 𓆉 𓆊 𓆋 𓆌 𓆍 𓆎 𓆐 𓆑 𓆒 𓆓 𓆔 𓆕 𓆖 𓆗 𓆘 𓆙 𓆚 𓆛 𓆜 𓆝 𓆞 𓆟 𓆠 𓆡 𓆢 𓆣 𓆤 𓆥 𓆦 𓆧 𓆨 𓆩𓆪 𓆫 𓆬 𓆭 𓆮 𓆯 𓆰 𓆱 𓆲 𓆳 𓆴 𓆵 𓆶 𓆷 𓆸 𓆹 𓆺 𓆻 𓆼 𓆽 𓆾 𓆿 𓇀 𓇁 𓇂 𓇃 𓇄 𓇅 𓇆 𓇇 𓇈 𓇉 𓇊 𓇋 𓇌 𓇍 𓇎 𓇏 𓇐 𓇑 𓇒 𓇓 𓇔 𓇕 𓇖 𓇗 𓇘 𓇙 𓇚 𓇛 𓇜 𓇝 𓇞 𓇟 𓇠 𓇡 𓇢 𓇣 𓇤 𓇥 𓇦 𓇧 𓇨 𓇩 𓇪 𓇫 𓇬 𓇭 𓇮 𓇯 𓇰 𓇱 𓇲 𓇳 𓇴 𓇵 𓇶 𓇷 𓇸 𓇹 𓇺 𓇻 𓇼 𓇾 𓇿 𓈀 𓈁 𓈂 𓈃 𓈄 𓈅 𓈆 𓈇 𓈈 𓈉 𓈊 𓈋 𓈌 𓈍 𓈎 𓈏 𓈐 𓈑 𓈒 𓈓 𓈔 𓈕 𓈖 𓈗 𓈘 𓊈 𓊉 𓊊 𓊋 𓊌 𓊍 𓊎 𓊏 𓊐 
𓊑 𓊒 𓊔 𓊕 𓊘 𓊙 𓊚 𓊛 𓊜 𓊝 𓊠 𓊡 𓊢 𓊣 𓊤 𓊥 𓊦 𓊧 𓊨 𓊩 𓊪 𓊫 𓊬 𓊭 𓊮 𓊯 𓊰 𓊱 𓊲 𓊳 𓊴 𓊵 𓊶 𓊷 𓊸 𓊹 𓊺 𓊻 𓊼 𓊿 𓋀 𓋁 𓋂 𓋃 𓋄 𓋅 𓋆 𓋇 𓋈 𓋉 𓋊 𓋋 𓋌 𓋍 𓋎 𓋏 𓋐 𓋑 𓋒 𓋓 𓋔 𓋕 𓋖 𓋗 𓋘 𓋙 𓋚 𓋛 𓋜 𓋝 𓋞 𓋟 𓌰 𓌱 𓌲 𓌳 𓌴 𓌵 𓌶 𓌷 𓌸 𓌹 𓌺 𓌻 𓌼 𓌽 𓌾 𓌿 𓍀 𓍁 𓍂 𓍃 𓍄 𓍅 𓍆 𓍇 𓍈 𓍉 𓍊 𓍋 𓍌 𓍍 𓍎 𓍏 𓍐 𓍑 𓍒 𓍓 𓍔 𓍕 𓍖 𓍗 𓍘 𓍙 𓍚 𓍛 𓍜 𓍝 𓍞 𓍟 𓍠 𓍡 𓍢 𓍣 𓍤 𓍬 𓍭 𓍮 𓍯 𓍰 𓍱 𓍲 𓍳 𓍴 𓍵 𓍶 𓍷 𓍸 𓍹 𓍺 𓍻 𓍼 𓍽 𓍾 𓍿 𓎀 𓎁 𓎂 𓎃 𓎄 𓎅 𓎆 𓎓 𓎔 𓎕 𓎖 𓎗 𓎘 𓎙 𓎚 𓎛 𓎜 𓎝 𓎞 𓎟 𓎠 𓎡 𓏋 𓏌 𓏍 𓏎 𓏏 𓏐 𓏑 𓏒 𓏓 
‏ 𓏕 𓏖 𓏗 𓏘 𓏙 𓏚 𓏛 𓏜 𓏝 𓏞 𓏟 𓏠 𓏡 𓏢 𓏣 𓏤 𓏥 𓏦 𓏧 𓏨 𓏩 𓏪 𓏫 𓏬 𓏭 𓏮 𓏯 𓏰 𓏱 𓏲 𓏳 𓏴 𓏶 𓏷 𓏸 𓏹 𓏺 𓏻 𓏼 𓏽 𓏾 𓏿 𓐀 𓐁 𓐂 𓐃 𓐄 𓐅 𓐆

- ?? ، ෴ ، 𖡺  ، 𖣐 ، ✜ ، ✘ ، 𖡻 ،
- ༄ ، ༺༻ ، ༽༼ ،  ╰☆╮،  
- ɵ‌᷄ˬɵ‌᷅ ، ‏⠉‌⃝ ، ࿇࿆ ، ꔚ، ま ، ☓ ،
{𓆉 . 𓃠 .𓅿 . 𓃠 . 𓃒 . 𓅰 . 𓃱 . 𓅓 . 𐂃  . ꕥ  . ⌘ . ♾ .    ꙰  .  . ᤑ .  ﾂ .
____
✦ ,✫ ,✯, ✮ ,✭ ,✰, ✬ ,✧, ✤, ❅ , 𒀭,✵ , ✶ , ✷ , ✸ , ✹ ,⧫, . 𐂂 }

-〘 𖢐 ، 𒍦 ، 𒍧 ، 𖢣 ، 𝁫 ، 𒍭 ، 𝁅 ، 𝁴 ، 𒍮 ، 𝁵 ، 𝀄 ، 𓏶 ، 𓏧 ، 𓏷 ، 𓏯 ، 𓏴 ، 𓏳 ، 𓏬 ، 𓏦 ، 𓏵 ، 𓏱 ، ᳱ ، ᯼ ، 𐃕 ، ᯥ ، ᯤ ، ᯾ ، ᳶ ، ᯌ ، ᢆ ،

ᥦ ، ᨙ ، ᨚ  ، ᨔ  ، ⏢ ، ⍨ ، ⍃ ، ⏃ ، ⍦ ، ⏕ ، ⏤ ، ⏁ ، ⏂ ، ⏆ ، ⌳ ، ࿅ ، ࿕ ، ࿇ ، ᚙ ، ࿊ ، ࿈ ، ྿ ،
࿂ ، ࿑ ،  ᛥ ، ࿄ ، 𐀁 ، 𐀪 ، 𐀔 ، 𐀴 ، 𐀤 ، 𐀦 ، 𐀂 ، 𐀣 ، 𐀢 ، 𐀶 ، 𐀷 ، 𐂭 ، 𐂦 ، 𐂐 ، 𐂅 ، 𐂡 ، 𐂢 ، 𐂠 ، 𐂓 ، 𐂑 ، 𐃸 ، 𐃶 ، 𐂴 ، 𐃭 ، 𐃳 ، 𐃣 ، 𐂰 ، 𐃟 ، 𐃐 ، 𐃙 ، 𐃀 ، 𐇮 ، 𐇹 ، 𐇲 ، 𐇩 ، 𐇪 ، 𐇶 ، 𐇻 ، 𐇡 ، 𐇸 ، 𐇣 ، 𐇤 ، 𐎅 ، 𐏍 ، 𐎃 ، 𐏒 ، 𐎄 ، 𐏕 〙.

╔ ╗. 𓌹  𓌺 .〝  〞. ‹ ›  .「  」. ‌‏𓂄‏ ‌‌‏𓂁
〖 〗. 《》 .  < > . « »  . ﹄﹃""",

            buttons=[
                [Button.inline("رجوع", data="decor_main_menu")],
            ],
        link_preview=False)


@l313l.tgbot.on(CallbackQuery(data=re.compile(b"zzk_bot-2$")))
async def settings_toggle(c_q: CallbackQuery):
    try:
        await c_q.edit(
            """ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗗𝗲𝗰𝗼𝗿 - **رمـوز تمبلـر** 🎡
**⋆┄─┄─┄─┄─┄─┄─┄─┄⋆**
‏ ‐ ‑ ‒ – — ― ‖ ‗ ‘ ’ ‚ ‛ “ ” „ ‟ † ‡ • ‣ ․ ‥ … ‧     
  ‰ ‱ ′ ″ ‴ ‵ ‶ ‷ ‸ ‹ › ※ ‼️ ‽ ‾ ‿ ⁀ ⁁ ⁂ ⁃ ⁄ ⁅ ⁆ ⁇ ⁈ ⁉️ ⁊ ⁋ ⁌ ⁍ ⁎ ⁏ ⁐ ⁑ ⁒ ⁓ ⁔ ⁕ ⁖ ⁗ ⁘ ⁙ ⁚ ⁛ ⁜ ⁝ ⁞   ⁠ ⁡ ⁢ ⁣ ⁤ ⁥ ‌ ‌ ⁨ ⁩ ⁪ ⁫ ⁬ ⁭ ⁮ ⁯ 
⁰ ⁱ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ⁿ ₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉ ₐ ₑ ₒ ₓ ₕ ₖ ₗ ₘ ₙ ₚ ₛ ₜ ₝ ₞ ₟ ₠ ₡ ₢ ₣ ₤ ₥ ₦ ₧ ₨ ₩ ₪ ₫ € ₭ ₮ ₯ ₰ ₱ ₲ ₳ ₴ ₵ ℀ ℁
ℂ ℃ ℄ ℅ ℆ ℇ ℈ ℉ ℊ ℋ ℌ ℍ ℎ ℏ ℐ ℑ ℒ ℓ ℔ ℕ №
℗ ℘ ℙ ℚ ℛ ℜ ℝ ℞ ℟ ℠ ℡ ™
℣ ℤ ℥ Ω ℧ ℨ ℩ K Å ℬ ℭ ℮ ℯ ℰ ℱ Ⅎ
ℳ ℴ ℵ ℶ ℷ ℸ ℹ️ ℺ ℻ ℼ ℽ ℾ ℿ ⅀ ⅁ ⅂ ⅃ ⅄ ⅅ ⅆ ⅇ ⅈ ⅉ
⅊ ⅋ ⅌ ⅍ ⅎ ⅏ ⅐ ⅑ ⅒ ⅓ ⅔ ⅕ ⅖ ⅗ ⅘ ⅙ ⅚ ⅛ ⅜ ⅝ ⅞
ↀ ↁ ↂ Ↄ ↉ ↊ ↋
∀ ∁ ∂ ∃ ∄ ∅ ∆ ∇ ∈ ∉ ∊ ∋ ∌ ∍
∎ ∏ ∐ ∑ − ∓ ∔ ∕ ∖ ∗ ∘ ∙ √ ∛ ∜ ∝ ∞ ∟ ∠ ∡ ∢
∣ ∤ ∥ ∦ ∧ ∨ ∩ ∪
∫ ∬ ∭ ∮ ∯ ∰ ∱ ∲ ∳ ∴ ∵ ∶ ∷ ∸ ∹ ∺ ∻ ∼ ∽ ∾ ∿ ≀ ≁ ≂ ≃ ≄ ≅ ≆ ≇ ≈ ≉ ≊ ≋ ≌ ≍ ≎ ≏ ≐ ≑ ≒ ≓ ≔ ≕ ≖ ≗ ≘ ≙ ≚ ≛ ≜ ≝ ≞ ≟ ≠ ≡ ≢ ≣ ≤ ≥ ≦ ≧ ≨ ≩ ≪ ≫ ≬ ≭ ≮ ≯ ≰ ≱ ≲ ≳ ≴ ≵ ≶ ≷ ≸ ≹ ≺ ≻ ≼ ≽ ≾ ≿ ⊀ ⊁ ⊂ ⊃ ⊄ ⊅ ⊆ ⊇ ⊈ ⊉ ⊊ ⊋ ⊌ ⊍ ⊎ ⊏ ⊐ ⊑ ⊒ ⊓ ⊔ ⊕ ⊖ ⊗ ⊘ ⊙ ⊚ ⊛ ⊜ ⊝ ⊞ ⊟ ⊠ ⊡ ⊢ ⊣ ⊤ ⊥ ⊦ ⊧ ⊨ ⊩ ⊪ ⊫ ⊬ ⊭ ⊮ ⊯ ⊰ ⊱ ⊲ ⊳ ⊴ ⊵ ⊶ ⊷ ⊸ ⊹ ⊺ ⊻ ⊼ ⊽ ⊾ ⊿ ⋀ ⋁ ⋂ ⋃ ⋄ ⋅ ⋆ ⋇ ⋈ ⋉ ⋊ ⋋ ⋌ ⋍ ⋎ ⋏ ⋐ ⋑ ⋒ ⋓ ⋔ ⋕ ⋖ ⋗ ⋘ ⋙ ⋚ ⋛ ⋜ ⋝ ⋞ ⋟ ⋠ ⋡ ⋢ ⋣ ⋤ ⋥ ⋦ ⋧ ⋨ ⋩ ⋪ ⋫ ⋬ ⋭ ⋮ ⋯ ⋰ ⋱ ⋲ ⋳ ⋴ ⋵ ⋶ ⋷ ⋸ ⋹ ⋺ ⋻ ⋼ ⋽ ⋾ ⋿ ⌀ ⌁ ⌂ ⌃ ⌄ ⌅ ⌆ ⌇ ⌈ ⌉ ⌊ ⌋ ⌌ ⌍ ⌎ ⌏ ⌐ ⌑ ⌒ ⌓ ⌔ ⌕ ⌖ ⌗ ⌘ ⌙ ⌚️ ⌛️ ⌜ ⌝ ⌞ ⌟ ⌠ ⌡ ⌢ ⌣ ⌤ ⌥ ⌦ ⌧ ⌨️ 〈 〉 ⌫ ⌬ ⌭ ⌮ ⌯ ⌰ ⌱ ⌲ ⌳ ⌴ ⌵ ⌶ ⌷ ⌸ ⌹ ⌺ ⌻ ⌼ ⌽ ⌾ ⌿ ⍀ ⍁ ⍂ ⍃ ⍄ ⍅ ⍆ ⍇ ⍈ ⍉ ⍊ ⍋ ⍌ ⍍ ⍎ ⍏ ⍐ ⍑ ⍒ ⍓ ⍔ ⍕ ⍖ ⍗ ⍘ ⍙ ⍚ ⍛ ⍜ ⍝ ⍞ ⍟ ⍠ ⍡ ⍢ ⍣ ⍤ ⍥ ⍦ ⍧ ⍨ ⍩ ⍪ ⍫ ⍬ ⍭ ⍮ ⍯ ⍰ ⍱ ⍲ ⍳ ⍴ ⍵ ⍶ ⍷ ⍸ ⍹ ⍺ ⍻ ⍼ ⍽ ⍾ ⍿ ⎀ ⎁ ⎂ ⎃ ⎄ ⎅ ⎆ ⎇ ⎈ ⎉ ⎊ ⎋ ⎌ ⎍ ⎎ ⎏ ⎐ ⎑ ⎒ ⎓ ⎔ ⎕ ⎖ ⎗ ⎘ ⎙ ⎚ ⎛ ⎜ ⎝ ⎞ ⎟ ⎠ ⎡ ⎢ ⎣ ⎤ ⎥ ⎦ ⎧ ⎨ ⎩ ⎪ ⎫ ⎬ ⎭ ⎮ ⎯ ⎰ ⎱ ⎲ ⎳ ⎴ ⎵ ⎶ ⎷ ⎸ ⎹ ⎺ ⎻ ⎼ ⎽ ⎾ ⎿ ⏀ ⏁ ⏂ ⏃ ⏄ ⏅ ⏆ ⏇ ⏈ ⏉ ⏋ ⏌ ⏍ ⏎ ⏏️ ⏐ ⏑ ⏒ ⏓ ⏔ ⏕ ⏖ ⏗ ⏘ ⏙ ⏚ ⏛ ⏜ ⏝ ⏞ ⏟ ⏠ ⏡ ⏢ ⏣ ⏤ ⏥ ⏦ ␋ ␢ ␣ ─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋ ┌ ┍ ┎ ┏ ┐ ┑ ┒ ┓ └ ┕ ┖ ┗ ┘ ┙ ┚ ┛ ├ ┝ ┞ ┟ ┠ ┡ ┢ ┣ ┤ ┥ ┦ ┧ ┨ ┩ ┪ ┫ ┬ ┭ ┮ ┯ ┰ ┱ ┲ ┳ ┴ ┵ ┶ ┷ ┸ ┹ ┺ ┻ ┼ ┽ ┾ ┿ ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋ ╌ ╍ ╎ ╏ ═ ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙ ╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬ ╬﹌ ╭ ╮ ╯ ╰ ╰☆╮ ╱ ╲ ╳ ╴ ╵ ╶ ╷ ╸ ╹ ╺ ╻ ╼ ╽ ╾ ╿ ▀ ▁ ▂ ▃ ▄ ▅ ▆ ▇ █ ▉ ▊ ▋ ▌ ▍ ▎ ▏ ▐ ░ ▒ ▓ ▔ ▕ ▖ ▗ ▘ ▙ ▚ ▛ ▜ ▝ ▞ ▟ ■ □ ▢ ▣ ▤ ▥ ▦ ▧ ▨ ▩ ▪️ ▫️ ▬ ▭ ▮ ▯ ▰ ▱ ▲ △ ▴ ▵ ▷ ▸ ▹ ► ▻ ▼ ▽ ▾ ▿  ◁ ◂ ◃ ◄ ◅ ◆ ◇ ◈ ◉ ◊ ○ ◌ ◍ ◎ ● ◐ ◑ ◒ ◓ ◔ ◔ʊ ◕ ◖ ◗ ◘ ◙ ◚ ◛ ◜ ◝ ◞ ◟ ◠ ◡ ◢ ◣ ◤ ◥ ◦ ◧ ◨ ◩ ◪ ◫ ◬ ◭ ◮ ◯ ◰ ◱ ◲ ◳ ◴ ◵ ◶ ◷ ◸ ◹ ◺  ☓☠️ ☡☰ ☱ ☲ ☳ ☴ ☵ ☶ ☷ ♔ ♕ ♖ ♗ ♘ ♙ ♚ ♛ ♜ ♝ ♞ ♟ ♠️ ♡ ♢  ♩ ♪ ♫ ♬ ♭ ♮ ♯ ♰ ♱ ♻️ ♼ ♽ ⚆ ⚇ ⚈ ⚉ ⚊ ⚋ ⚌ ⚍ ⚎ ⚏ ⚐ ⚑ ✐ ✑ ✒️ ✓ ✔️ ✕ ✖️ ✗ ✘ ✙ ✚ ✛ ✜  ✞ ✟ ✠ ✢ ✣ ✤ ✥ ✦ ✧ ✧♱ ✩ ✪ ✫ ✬ ✭ ✮ ✯ ✰ ✱ ✲  ✵ ✶ ✷ ✸ ✹ ✺ ✻ ✼ ✽ ✾ ✿ ❀ ❁ ❂ ❃ ❄️ ❅ ❆ ❈ ❉ ❊ ❋ ❍ ❏ ❐ ❑ ❒ ❖ ❗️ ❘ ❙ ❚ ❛ ❜ ❝ ❞ ❡ ❢ ❣️ ❤️ ❥ ❦ ❧ 
اسم مخفي (                          ‌ ‍ ‎)
———————×———————

❨ ❩ ❪ ❫ ❬ ❭ ❮ ❯ ❰ ❱ ❲ ❳ ❴ ❵ ⟦ ⟧ ⟨ ⟩ ⟪ ⟫ ⦀ ⦁ ⦂
⦃ ⦄ ⦅ ⦆ ⦇ ⦈ ⦉ ⦊ ⦋ ⦌ ⦍ ⦎ ⦏ ⦐ ⦑ ⦒ ⦓ ⦔ ⦕ ⦖ ⦗ ⦘ 

———————×———————

← ↑ → ↓ ↔️ ↕️ ↖️ ↗️ ↘️ ↙️ ↚ ↛ ↜ ↝
↞ ↟ ↠ ↡ ↢ ↣ ↤ ↥ ↦ ↧ ↨ ↩️ ↪️ ↫ ↬ ↭ ↮ ↯ ↰ ↱ ↲ ↳ ↴ ↵ ↶ ↷ ↸ ↹
↺ ↻ ↼ ↽ ↾ ↿ ⇀ ⇁ ⇂ ⇃ ⇄ ⇅ ⇆ ⇇ ⇈ ⇉ ⇊ ⇋ ⇌ ⇍ ⇎ ⇏
⇐ ⇑ ⇒ ⇓ ⇔ ⇕ ⇖ ⇗ ⇘ ⇙ ⇚ ⇛ ⇜ ⇝ ⇞ ⇟ ⇠ ⇡ ⇢ ⇣ ⇤ ⇥
⇦ ⇧ ⇨ ⇩ ⇪ ⇫ ⇬ ⇭ ⇮ ⇯ ⇰ ⇱ ⇲ ⇳ ⇴ ⇵ ⇶ ⇷ ⇸ ⇹ ⇺ ⇻ ⇼ ⇽ ⇾ ⇿

➔ ➘ ➙ ➚ ➛ ➜ ➝ ➞ ➟ ➠  ➢ ➣ ➤ ➥ ➦ ➧ ➨ ➩ ➪ ➫ ➬ ➭ ➮ ➯ ➱ ➲ ➳ ➴ ➵ ➶ ➷ ➸ ➹ ➺ ➻ ➼ ➽ ➾
⟰ ⟱ ⟲ ⟳ ⟴ ⟵ ⟶ ⟷ ⟸ ⟹ ⟺ ⟻ ⟼ ⟽ ⟾
⟿ ⤀ ⤁ ⤂ ⤃ ⤄ ⤅ ⤆ ⤇ ⤈ ⤉ ⤊ ⤋
⤌ ⤍ ⤎ ⤏ ⤐ ⤑ ⤒ ⤓ ⤔ ⤕ ⤖ ⤗ ⤘
⤙ ⤚ ⤛ ⤜ ⤝ ⤞ ⤟ ⤠ ⤡ ⤢ ⤣ ⤤ ⤥ ⤦
⤧ ⤨ ⤩ ⤪ ⤫ ⤬ ⤭ ⤮ ⤯ ⤰ ⤱ ⤲ ⤳ ⤶ ⤷ ⤸ ⤹
⤺ ⤻ ⤼ ⤽ ⤾ ⤿ ⥀ ⥁ ⥂ ⥃ ⥄ ⥅ ⥆
⥇ ⥈ ⥉ ⥊ ⥋ ⥌ ⥍ ⥎ ⥏ ⥐ ⥑ ⥒ ⥓ ⥔ ⥕
⥖ ⥗ ⥘ ⥙ ⥚ ⥛ ⥜ ⥝ ⥞ ⥟ ⥠ ⥡
⥢ ⥣ ⥤ ⥥ ⥦ ⥧ ⥨ ⥩ ⥪ ⥫ ⥬ ⥭
⥮ ⥯ ⥰ ⥱ ⥲ ⥳ ⥴ ⥵ ⥶ ⥷ ⥸ ⥹ ⥺ ⥻ ⥼ ⥽ ⥾ ⥿

———————×———————

⟀ ⟁ ⟂ ⟃ ⟄ ⟇ ⟈ ⟉ ⟊ ⟐ ⟑ ⟒ ⟓ ⟔ ⟕ ⟖
⟗ ⟘ ⟙ ⟚ ⟛ ⟜ ⟝ ⟞ ⟟ ⟠ ⟡ ⟢ ⟣ ⟤ ⟥ 
⦙ ⦚ ⦛ ⦜ ⦝ ⦞ ⦟ ⦠ ⦡ ⦢ ⦣ ⦤ ⦥ ⦦ ⦧ ⦨ ⦩ ⦪ ⦫ ⦬ ⦭ ⦮ ⦯
⦰ ⦱ ⦲ ⦳ ⦴ ⦵ ⦶ ⦷ ⦸ ⦹ ⦺ ⦻ ⦼ ⦽ ⦾ ⦿ ⧀ ⧁ ⧂ ⧃
⧄ ⧅ ⧆ ⧇ ⧈ ⧉ ⧊ ⧋ ⧌ ⧍ ⧎ ⧏ ⧐ ⧑ ⧒ ⧓ ⧔ ⧕ ⧖ ⧗
⧘ ⧙ ⧚ ⧛ ⧜ ⧝ ⧞ ⧟ ⧡ ⧢ ⧣ ⧤ ⧥ ⧦ ⧧
⧨ ⧩ ⧪ ⧫ ⧬ ⧭ ⧮ ⧯ ⧰ ⧱ ⧲ ⧳
 ⧴ ⧵ ⧶ ⧷ ⧸ ⧹ ⧺ɷ
﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎
.""",

            buttons=[
                [Button.inline("رجوع", data="decor_main_menu")],
            ],
        link_preview=False)
    except Exception:
        await c_q.client.send_message(
            c_q.query.user_id,
            """ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗗𝗲𝗰𝗼𝗿 - **رمـوز تمبلـر** 🎡
**⋆┄─┄─┄─┄─┄─┄─┄─┄⋆**
‏ ‐ ‑ ‒ – — ― ‖ ‗ ‘ ’ ‚ ‛ “ ” „ ‟ † ‡ • ‣ ․ ‥ … ‧     
  ‰ ‱ ′ ″ ‴ ‵ ‶ ‷ ‸ ‹ › ※ ‼️ ‽ ‾ ‿ ⁀ ⁁ ⁂ ⁃ ⁄ ⁅ ⁆ ⁇ ⁈ ⁉️ ⁊ ⁋ ⁌ ⁍ ⁎ ⁏ ⁐ ⁑ ⁒ ⁓ ⁔ ⁕ ⁖ ⁗ ⁘ ⁙ ⁚ ⁛ ⁜ ⁝ ⁞   ⁠ ⁡ ⁢ ⁣ ⁤ ⁥ ‌ ‌ ⁨ ⁩ ⁪ ⁫ ⁬ ⁭ ⁮ ⁯ 
⁰ ⁱ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ⁿ ₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉ ₐ ₑ ₒ ₓ ₕ ₖ ₗ ₘ ₙ ₚ ₛ ₜ ₝ ₞ ₟ ₠ ₡ ₢ ₣ ₤ ₥ ₦ ₧ ₨ ₩ ₪ ₫ € ₭ ₮ ₯ ₰ ₱ ₲ ₳ ₴ ₵ ℀ ℁
ℂ ℃ ℄ ℅ ℆ ℇ ℈ ℉ ℊ ℋ ℌ ℍ ℎ ℏ ℐ ℑ ℒ ℓ ℔ ℕ №
℗ ℘ ℙ ℚ ℛ ℜ ℝ ℞ ℟ ℠ ℡ ™
℣ ℤ ℥ Ω ℧ ℨ ℩ K Å ℬ ℭ ℮ ℯ ℰ ℱ Ⅎ
ℳ ℴ ℵ ℶ ℷ ℸ ℹ️ ℺ ℻ ℼ ℽ ℾ ℿ ⅀ ⅁ ⅂ ⅃ ⅄ ⅅ ⅆ ⅇ ⅈ ⅉ
⅊ ⅋ ⅌ ⅍ ⅎ ⅏ ⅐ ⅑ ⅒ ⅓ ⅔ ⅕ ⅖ ⅗ ⅘ ⅙ ⅚ ⅛ ⅜ ⅝ ⅞
ↀ ↁ ↂ Ↄ ↉ ↊ ↋
∀ ∁ ∂ ∃ ∄ ∅ ∆ ∇ ∈ ∉ ∊ ∋ ∌ ∍
∎ ∏ ∐ ∑ − ∓ ∔ ∕ ∖ ∗ ∘ ∙ √ ∛ ∜ ∝ ∞ ∟ ∠ ∡ ∢
∣ ∤ ∥ ∦ ∧ ∨ ∩ ∪
∫ ∬ ∭ ∮ ∯ ∰ ∱ ∲ ∳ ∴ ∵ ∶ ∷ ∸ ∹ ∺ ∻ ∼ ∽ ∾ ∿ ≀ ≁ ≂ ≃ ≄ ≅ ≆ ≇ ≈ ≉ ≊ ≋ ≌ ≍ ≎ ≏ ≐ ≑ ≒ ≓ ≔ ≕ ≖ ≗ ≘ ≙ ≚ ≛ ≜ ≝ ≞ ≟ ≠ ≡ ≢ ≣ ≤ ≥ ≦ ≧ ≨ ≩ ≪ ≫ ≬ ≭ ≮ ≯ ≰ ≱ ≲ ≳ ≴ ≵ ≶ ≷ ≸ ≹ ≺ ≻ ≼ ≽ ≾ ≿ ⊀ ⊁ ⊂ ⊃ ⊄ ⊅ ⊆ ⊇ ⊈ ⊉ ⊊ ⊋ ⊌ ⊍ ⊎ ⊏ ⊐ ⊑ ⊒ ⊓ ⊔ ⊕ ⊖ ⊗ ⊘ ⊙ ⊚ ⊛ ⊜ ⊝ ⊞ ⊟ ⊠ ⊡ ⊢ ⊣ ⊤ ⊥ ⊦ ⊧ ⊨ ⊩ ⊪ ⊫ ⊬ ⊭ ⊮ ⊯ ⊰ ⊱ ⊲ ⊳ ⊴ ⊵ ⊶ ⊷ ⊸ ⊹ ⊺ ⊻ ⊼ ⊽ ⊾ ⊿ ⋀ ⋁ ⋂ ⋃ ⋄ ⋅ ⋆ ⋇ ⋈ ⋉ ⋊ ⋋ ⋌ ⋍ ⋎ ⋏ ⋐ ⋑ ⋒ ⋓ ⋔ ⋕ ⋖ ⋗ ⋘ ⋙ ⋚ ⋛ ⋜ ⋝ ⋞ ⋟ ⋠ ⋡ ⋢ ⋣ ⋤ ⋥ ⋦ ⋧ ⋨ ⋩ ⋪ ⋫ ⋬ ⋭ ⋮ ⋯ ⋰ ⋱ ⋲ ⋳ ⋴ ⋵ ⋶ ⋷ ⋸ ⋹ ⋺ ⋻ ⋼ ⋽ ⋾ ⋿ ⌀ ⌁ ⌂ ⌃ ⌄ ⌅ ⌆ ⌇ ⌈ ⌉ ⌊ ⌋ ⌌ ⌍ ⌎ ⌏ ⌐ ⌑ ⌒ ⌓ ⌔ ⌕ ⌖ ⌗ ⌘ ⌙ ⌚️ ⌛️ ⌜ ⌝ ⌞ ⌟ ⌠ ⌡ ⌢ ⌣ ⌤ ⌥ ⌦ ⌧ ⌨️ 〈 〉 ⌫ ⌬ ⌭ ⌮ ⌯ ⌰ ⌱ ⌲ ⌳ ⌴ ⌵ ⌶ ⌷ ⌸ ⌹ ⌺ ⌻ ⌼ ⌽ ⌾ ⌿ ⍀ ⍁ ⍂ ⍃ ⍄ ⍅ ⍆ ⍇ ⍈ ⍉ ⍊ ⍋ ⍌ ⍍ ⍎ ⍏ ⍐ ⍑ ⍒ ⍓ ⍔ ⍕ ⍖ ⍗ ⍘ ⍙ ⍚ ⍛ ⍜ ⍝ ⍞ ⍟ ⍠ ⍡ ⍢ ⍣ ⍤ ⍥ ⍦ ⍧ ⍨ ⍩ ⍪ ⍫ ⍬ ⍭ ⍮ ⍯ ⍰ ⍱ ⍲ ⍳ ⍴ ⍵ ⍶ ⍷ ⍸ ⍹ ⍺ ⍻ ⍼ ⍽ ⍾ ⍿ ⎀ ⎁ ⎂ ⎃ ⎄ ⎅ ⎆ ⎇ ⎈ ⎉ ⎊ ⎋ ⎌ ⎍ ⎎ ⎏ ⎐ ⎑ ⎒ ⎓ ⎔ ⎕ ⎖ ⎗ ⎘ ⎙ ⎚ ⎛ ⎜ ⎝ ⎞ ⎟ ⎠ ⎡ ⎢ ⎣ ⎤ ⎥ ⎦ ⎧ ⎨ ⎩ ⎪ ⎫ ⎬ ⎭ ⎮ ⎯ ⎰ ⎱ ⎲ ⎳ ⎴ ⎵ ⎶ ⎷ ⎸ ⎹ ⎺ ⎻ ⎼ ⎽ ⎾ ⎿ ⏀ ⏁ ⏂ ⏃ ⏄ ⏅ ⏆ ⏇ ⏈ ⏉ ⏋ ⏌ ⏍ ⏎ ⏏️ ⏐ ⏑ ⏒ ⏓ ⏔ ⏕ ⏖ ⏗ ⏘ ⏙ ⏚ ⏛ ⏜ ⏝ ⏞ ⏟ ⏠ ⏡ ⏢ ⏣ ⏤ ⏥ ⏦ ␋ ␢ ␣ ─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋ ┌ ┍ ┎ ┏ ┐ ┑ ┒ ┓ └ ┕ ┖ ┗ ┘ ┙ ┚ ┛ ├ ┝ ┞ ┟ ┠ ┡ ┢ ┣ ┤ ┥ ┦ ┧ ┨ ┩ ┪ ┫ ┬ ┭ ┮ ┯ ┰ ┱ ┲ ┳ ┴ ┵ ┶ ┷ ┸ ┹ ┺ ┻ ┼ ┽ ┾ ┿ ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋ ╌ ╍ ╎ ╏ ═ ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙ ╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬ ╬﹌ ╭ ╮ ╯ ╰ ╰☆╮ ╱ ╲ ╳ ╴ ╵ ╶ ╷ ╸ ╹ ╺ ╻ ╼ ╽ ╾ ╿ ▀ ▁ ▂ ▃ ▄ ▅ ▆ ▇ █ ▉ ▊ ▋ ▌ ▍ ▎ ▏ ▐ ░ ▒ ▓ ▔ ▕ ▖ ▗ ▘ ▙ ▚ ▛ ▜ ▝ ▞ ▟ ■ □ ▢ ▣ ▤ ▥ ▦ ▧ ▨ ▩ ▪️ ▫️ ▬ ▭ ▮ ▯ ▰ ▱ ▲ △ ▴ ▵ ▷ ▸ ▹ ► ▻ ▼ ▽ ▾ ▿  ◁ ◂ ◃ ◄ ◅ ◆ ◇ ◈ ◉ ◊ ○ ◌ ◍ ◎ ● ◐ ◑ ◒ ◓ ◔ ◔ʊ ◕ ◖ ◗ ◘ ◙ ◚ ◛ ◜ ◝ ◞ ◟ ◠ ◡ ◢ ◣ ◤ ◥ ◦ ◧ ◨ ◩ ◪ ◫ ◬ ◭ ◮ ◯ ◰ ◱ ◲ ◳ ◴ ◵ ◶ ◷ ◸ ◹ ◺  ☓☠️ ☡☰ ☱ ☲ ☳ ☴ ☵ ☶ ☷ ♔ ♕ ♖ ♗ ♘ ♙ ♚ ♛ ♜ ♝ ♞ ♟ ♠️ ♡ ♢  ♩ ♪ ♫ ♬ ♭ ♮ ♯ ♰ ♱ ♻️ ♼ ♽ ⚆ ⚇ ⚈ ⚉ ⚊ ⚋ ⚌ ⚍ ⚎ ⚏ ⚐ ⚑ ✐ ✑ ✒️ ✓ ✔️ ✕ ✖️ ✗ ✘ ✙ ✚ ✛ ✜  ✞ ✟ ✠ ✢ ✣ ✤ ✥ ✦ ✧ ✧♱ ✩ ✪ ✫ ✬ ✭ ✮ ✯ ✰ ✱ ✲  ✵ ✶ ✷ ✸ ✹ ✺ ✻ ✼ ✽ ✾ ✿ ❀ ❁ ❂ ❃ ❄️ ❅ ❆ ❈ ❉ ❊ ❋ ❍ ❏ ❐ ❑ ❒ ❖ ❗️ ❘ ❙ ❚ ❛ ❜ ❝ ❞ ❡ ❢ ❣️ ❤️ ❥ ❦ ❧ 
اسم مخفي (                          ‌ ‍ ‎)
———————×———————

❨ ❩ ❪ ❫ ❬ ❭ ❮ ❯ ❰ ❱ ❲ ❳ ❴ ❵ ⟦ ⟧ ⟨ ⟩ ⟪ ⟫ ⦀ ⦁ ⦂
⦃ ⦄ ⦅ ⦆ ⦇ ⦈ ⦉ ⦊ ⦋ ⦌ ⦍ ⦎ ⦏ ⦐ ⦑ ⦒ ⦓ ⦔ ⦕ ⦖ ⦗ ⦘ 

———————×———————

← ↑ → ↓ ↔️ ↕️ ↖️ ↗️ ↘️ ↙️ ↚ ↛ ↜ ↝
↞ ↟ ↠ ↡ ↢ ↣ ↤ ↥ ↦ ↧ ↨ ↩️ ↪️ ↫ ↬ ↭ ↮ ↯ ↰ ↱ ↲ ↳ ↴ ↵ ↶ ↷ ↸ ↹
↺ ↻ ↼ ↽ ↾ ↿ ⇀ ⇁ ⇂ ⇃ ⇄ ⇅ ⇆ ⇇ ⇈ ⇉ ⇊ ⇋ ⇌ ⇍ ⇎ ⇏
⇐ ⇑ ⇒ ⇓ ⇔ ⇕ ⇖ ⇗ ⇘ ⇙ ⇚ ⇛ ⇜ ⇝ ⇞ ⇟ ⇠ ⇡ ⇢ ⇣ ⇤ ⇥
⇦ ⇧ ⇨ ⇩ ⇪ ⇫ ⇬ ⇭ ⇮ ⇯ ⇰ ⇱ ⇲ ⇳ ⇴ ⇵ ⇶ ⇷ ⇸ ⇹ ⇺ ⇻ ⇼ ⇽ ⇾ ⇿

➔ ➘ ➙ ➚ ➛ ➜ ➝ ➞ ➟ ➠  ➢ ➣ ➤ ➥ ➦ ➧ ➨ ➩ ➪ ➫ ➬ ➭ ➮ ➯ ➱ ➲ ➳ ➴ ➵ ➶ ➷ ➸ ➹ ➺ ➻ ➼ ➽ ➾
⟰ ⟱ ⟲ ⟳ ⟴ ⟵ ⟶ ⟷ ⟸ ⟹ ⟺ ⟻ ⟼ ⟽ ⟾
⟿ ⤀ ⤁ ⤂ ⤃ ⤄ ⤅ ⤆ ⤇ ⤈ ⤉ ⤊ ⤋
⤌ ⤍ ⤎ ⤏ ⤐ ⤑ ⤒ ⤓ ⤔ ⤕ ⤖ ⤗ ⤘
⤙ ⤚ ⤛ ⤜ ⤝ ⤞ ⤟ ⤠ ⤡ ⤢ ⤣ ⤤ ⤥ ⤦
⤧ ⤨ ⤩ ⤪ ⤫ ⤬ ⤭ ⤮ ⤯ ⤰ ⤱ ⤲ ⤳ ⤶ ⤷ ⤸ ⤹
⤺ ⤻ ⤼ ⤽ ⤾ ⤿ ⥀ ⥁ ⥂ ⥃ ⥄ ⥅ ⥆
⥇ ⥈ ⥉ ⥊ ⥋ ⥌ ⥍ ⥎ ⥏ ⥐ ⥑ ⥒ ⥓ ⥔ ⥕
⥖ ⥗ ⥘ ⥙ ⥚ ⥛ ⥜ ⥝ ⥞ ⥟ ⥠ ⥡
⥢ ⥣ ⥤ ⥥ ⥦ ⥧ ⥨ ⥩ ⥪ ⥫ ⥬ ⥭
⥮ ⥯ ⥰ ⥱ ⥲ ⥳ ⥴ ⥵ ⥶ ⥷ ⥸ ⥹ ⥺ ⥻ ⥼ ⥽ ⥾ ⥿

———————×———————

⟀ ⟁ ⟂ ⟃ ⟄ ⟇ ⟈ ⟉ ⟊ ⟐ ⟑ ⟒ ⟓ ⟔ ⟕ ⟖
⟗ ⟘ ⟙ ⟚ ⟛ ⟜ ⟝ ⟞ ⟟ ⟠ ⟡ ⟢ ⟣ ⟤ ⟥ 
⦙ ⦚ ⦛ ⦜ ⦝ ⦞ ⦟ ⦠ ⦡ ⦢ ⦣ ⦤ ⦥ ⦦ ⦧ ⦨ ⦩ ⦪ ⦫ ⦬ ⦭ ⦮ ⦯
⦰ ⦱ ⦲ ⦳ ⦴ ⦵ ⦶ ⦷ ⦸ ⦹ ⦺ ⦻ ⦼ ⦽ ⦾ ⦿ ⧀ ⧁ ⧂ ⧃
⧄ ⧅ ⧆ ⧇ ⧈ ⧉ ⧊ ⧋ ⧌ ⧍ ⧎ ⧏ ⧐ ⧑ ⧒ ⧓ ⧔ ⧕ ⧖ ⧗
⧘ ⧙ ⧚ ⧛ ⧜ ⧝ ⧞ ⧟ ⧡ ⧢ ⧣ ⧤ ⧥ ⧦ ⧧
⧨ ⧩ ⧪ ⧫ ⧬ ⧭ ⧮ ⧯ ⧰ ⧱ ⧲ ⧳
 ⧴ ⧵ ⧶ ⧷ ⧸ ⧹ ⧺ɷ
﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎
.""",

            buttons=[
                [Button.inline("رجوع", data="decor_main_menu")],
            ],
        link_preview=False)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"zzk_bot-3$")))
async def settings_toggle(c_q: CallbackQuery):
    await c_q.edit(
        """ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗗𝗲𝗰𝗼𝗿 - **ارقـام مزغـرفـة** 🎡
**⋆┄─┄─┄─┄─┄─┄─┄─┄⋆**
¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ⁰
₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉ ₀
———————×———————
① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⓪
⑩ ⑪ ⑫ ⑬ ⑭ ⑮ ⑯ ⑰ ⑱ ⑲ ⑳
➀ ➁ ➂ ➃ ➄ ➅ ➆ ➇ ➈ ➉
⓵ ⓶ ⓷ ⓸ ⓹ ⓺ ⓻ ⓼ ⓽ ⓾
❶ ❷ ❸ ❹ ❺ ❻ ❼ ❽ ❾ ⓿
❿ ⓫ ⓬ ⓭ ⓮ ⓯ ⓰ ⓱ ⓲ ⓳ ⓴
➊ ➋ ➌ ➍ ➎ ➏ ➐➑ ➒ ➓ 
———————×———————
𝟶 𝟷 𝟸 𝟹 𝟺 𝟻 𝟼 𝟽 𝟾  𝟿
𝟘 𝟙  𝟚  𝟛  𝟜  𝟝  𝟞  𝟟  𝟠 𝟡
𝟬 𝟭  𝟮  𝟯  𝟰  𝟱   𝟲  𝟳  𝟴  𝟵
𝟎  𝟏  𝟐  𝟑  𝟒   𝟓   𝟔  𝟕   𝟖   𝟗
０ １ ２ ３ ４ ５ ６ ７８９
⑴ ⑵ ⑶ ⑷ ⑸ ⑹ ⑺ ⑻ ⑼ ⑽
⑾ ⑿ ⒀ ⒁ ⒂ ⒃ ⒄ ⒅ ⒆ ⒇
⒈ ⒉ ⒊ ⒋ ⒌ ⒍ ⒎ ⒏ ⒐ ⒑
⒒ ⒓ ⒔ ⒕ ⒖ ⒗ ⒘ ⒙ ⒚ ⒛
﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎
.""",

        buttons=[
            [Button.inline("رجوع", data="decor_main_menu")],
        ],
    link_preview=False)


@l313l.tgbot.on(CallbackQuery(data=re.compile(b"zzk_bot-4$")))
async def settings_toggle(c_q: CallbackQuery):
    await c_q.edit(
        """ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗗𝗲𝗰𝗼𝗿 - **ارقـام مزغـرفـة** 🎡
**⋆┄─┄─┄─┄─┄─┄─┄─┄⋆**
¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ⁰
₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉ ₀
———————×———————
① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⓪
⑩ ⑪ ⑫ ⑬ ⑭ ⑮ ⑯ ⑰ ⑱ ⑲ ⑳
➀ ➁ ➂ ➃ ➄ ➅ ➆ ➇ ➈ ➉
⓵ ⓶ ⓷ ⓸ ⓹ ⓺ ⓻ ⓼ ⓽ ⓾
❶ ❷ ❸ ❹ ❺ ❻ ❼ ❽ ❾ ⓿
❿ ⓫ ⓬ ⓭ ⓮ ⓯ ⓰ ⓱ ⓲ ⓳ ⓴
➊ ➋ ➌ ➍ ➎ ➏ ➐➑ ➒ ➓ 
———————×———————
𝟶 𝟷 𝟸 𝟹 𝟺 𝟻 𝟼 𝟽 𝟾  𝟿
𝟘 𝟙  𝟚  𝟛  𝟜  𝟝  𝟞  𝟟  𝟠 𝟡
𝟬 𝟭  𝟮  𝟯  𝟰  𝟱   𝟲  𝟳  𝟴  𝟵
𝟎  𝟏  𝟐  𝟑  𝟒   𝟓   𝟔  𝟕   𝟖   𝟗
０ １ ２ ３ ４ ５ ６ ７８９
⑴ ⑵ ⑶ ⑷ ⑸ ⑹ ⑺ ⑻ ⑼ ⑽
⑾ ⑿ ⒀ ⒁ ⒂ ⒃ ⒄ ⒅ ⒆ ⒇
⒈ ⒉ ⒊ ⒋ ⒌ ⒍ ⒎ ⒏ ⒐ ⒑
⒒ ⒓ ⒔ ⒕ ⒖ ⒗ ⒘ ⒙ ⒚ ⒛
﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎
.""",

        buttons=[
            [Button.inline("رجوع", data="decor_main_menu")],
        ],
    link_preview=False)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"zzk_bot-5$")))
async def settings_toggle(c_q: CallbackQuery):
    await c_q.edit(
        """ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗗𝗲𝗹 - **حـذف الحسـاب** ⚠️
**⋆┄─┄─┄─┄─┄─┄─┄─┄⋆**
**- لـ حذف حسابك قم بارسـال الامـر التالي :**

`حذف حسابي`

**ثم اتبـع التعليمـات**
﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎
.""",

        buttons=[
            [Button.inline("رجوع", data="styleback")],
        ],
    link_preview=False)


@l313l.bot_cmd(incoming=True, func=lambda e: e.is_private)
@l313l.bot_cmd(edited=True, func=lambda e: e.is_private)
async def antif_on_msg(event):
    if gvarstatus("bot_antif") is None:
        return
    chat = await event.get_chat()
    if chat.id == Config.OWNER_ID:
        return
    user_id = chat.id
    if check_is_black_list(user_id):
        raise StopPropagation
    if await is_flood(user_id):
        await send_flood_alert(chat)
        FloodConfig.BANNED_USERS.add(user_id)
        raise StopPropagation
    if user_id in FloodConfig.BANNED_USERS:
        FloodConfig.BANNED_USERS.remove(user_id)
