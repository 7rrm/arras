import asyncio
import math
import os
import re
import heroku3
import requests
import urllib3
import random
import string
from datetime import datetime
from PIL import Image
from telegraph import Telegraph, exceptions, upload_file
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urlextract import URLExtract

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.errors.rpcerrorlist import ChatSendMediaForbiddenError
from telethon import Button, functions
from telethon.events import CallbackQuery
from telethon.utils import get_display_name

from . import l313l
from ..core.logger import logging
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format, get_user_from_event, reply_id
from ..sql_helper import global_collectionjson as sql
from ..sql_helper import global_list as sqllist
from ..sql_helper import pmpermit_sql
from ..sql_helper.mute_sql import is_muted, mute, unmute
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..utils import Zed_Dev
from . import BOTLOG, BOTLOG_CHATID, mention, edit_delete

plugin_category = "البوت"
LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER
PC_BLOCK = gvarstatus("PC_BLOCK")

extractor = URLExtract()
telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

class PMPERMIT:
    def __init__(self):
        self.TEMPAPPROVED = []

PMPERMIT_ = PMPERMIT()

async def do_pm_permit_action(event, chat):  # sourcery no-metrics
    # sourcery skip: low-code-quality
    reply_to_id = await reply_id(event)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    me = await event.client.get_me()
    mention = f"[{chat.first_name}](tg://user?id={chat.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = chat.first_name
    last = chat.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{chat.username}" if chat.username else mention
    userid = chat.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    if str(chat.id) not in PM_WARNS:
        PM_WARNS[str(chat.id)] = 0
    MAX_FLOOD_IN_PMS = 6
    try:
        ZT_WARNS = gvarstatus("MAX_FLOOD_IN_PMS")
        MAX_FLOOD_IN_PMS = int(ZT_WARNS) if gvarstatus("MAX_FLOOD_IN_PMS") else Config.MAX_FLOOD_IN_PMS
    except (ValueError, TypeError):
        MAX_FLOOD_IN_PMS = 6
    except Exception:
        MAX_FLOOD_IN_PMS = 6
    totalwarns = MAX_FLOOD_IN_PMS + 1
    warns = PM_WARNS[str(chat.id)] + 1
    remwarns = totalwarns - warns
    if PM_WARNS[str(chat.id)] >= MAX_FLOOD_IN_PMS:
        try:
            if str(chat.id) in PMMESSAGE_CACHE:
                await event.client.delete_messages(
                    chat.id, PMMESSAGE_CACHE[str(chat.id)]
                )
                del PMMESSAGE_CACHE[str(chat.id)]
        except Exception as e:
            LOGS.info(str(e))
        controlmute = gvarstatus("pmute") or None
        custompmblock = gvarstatus("pmblock") or None
        if custompmblock is not None:
            USER_BOT_WARN_ZERO = custompmblock.format(
                mention=mention,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
                totalwarns=totalwarns,
                warns=warns,
                remwarns=remwarns,
            )
        else:
            if controlmute is not None:
                USER_BOT_WARN_ZERO = f"**⤶ لقـد حذرتـڪ مـسـبـقـاً مـن الـتـڪـرار 📵** \n**⤶ تـم ڪتمـك تلقـائيـاً .. الان لا يـمـڪـنـڪ ازعـاجـي🔕**\n\n**⤶ تحيـاتـي** {my_mention}  🫡"
            else:
                USER_BOT_WARN_ZERO = f"**⤶ لقـد حذرتـڪ مـسـبـقـاً مـن الـتـڪـرار 📵** \n**⤶ تـم حـظـرڪ تلقـائيـاً .. الان لا يـمـڪـنـڪ ازعـاجـي🔕**\n\n**⤶ تحيـاتـي** {my_mention}  🫡"
        if controlmute is not None:
            msg = await event.reply(USER_BOT_WARN_ZERO)
            try:
                mute(event.chat_id, event.chat_id)
            except Exception as e:
                await event.reply(f"**- خطـأ **\n`{e}`")
            the_message = f"#حمـايـة_الخـاص\
                                \n** ⎉╎المستخـدم** [{get_display_name(chat)}](tg://user?id={chat.id}) .\
                                \n** ⎉╎تم كتمـه .. تلقائيـاً**\
                                \n** ⎉╎عـدد رسـائله :** {PM_WARNS[str(chat.id)]}"
            del PM_WARNS[str(chat.id)]
            sql.del_collection("pmwarns")
            sql.del_collection("pmmessagecache")
            sql.add_collection("pmwarns", PM_WARNS, {})
            sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
            try:
                return await event.client.send_message(
                    BOTLOG_CHATID,
                    the_message,
                )
            except BaseException:
                return
        else:
            msg = await event.reply(USER_BOT_WARN_ZERO)
            await event.client(functions.contacts.BlockRequest(chat.id))
            the_message = f"#حمـايـة_الخـاص\
                                \n** ⎉╎المستخـدم** [{get_display_name(chat)}](tg://user?id={chat.id}) .\
                                \n** ⎉╎تم حظـره .. تلقائيـاً**\
                                \n** ⎉╎عـدد رسـائله :** {PM_WARNS[str(chat.id)]}"
            del PM_WARNS[str(chat.id)]
            sql.del_collection("pmwarns")
            sql.del_collection("pmmessagecache")
            sql.add_collection("pmwarns", PM_WARNS, {})
            sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
            try:
                return await event.client.send_message(
                    BOTLOG_CHATID,
                    the_message,
                )
            except BaseException:
                return

    custompmpermit = gvarstatus("pmpermit_txt") or None
    if custompmpermit is not None:
        USER_BOT_NO_WARN = custompmpermit.format(
            mention=mention,
            first=first,
            last=last,
            fullname=fullname,
            username=username,
            userid=userid,
            my_first=my_first,
            my_last=my_last,
            my_fullname=my_fullname,
            my_username=my_username,
            my_mention=my_mention,
            totalwarns=totalwarns,
            warns=warns,
            remwarns=remwarns,
        )
    elif gvarstatus("pmute") is not None:
        USER_BOT_NO_WARN = f"""ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗮𝗥𝗮𝘀 **- الـرد التلقـائي 〽️**
**•─────────────────•**

❞ **مرحبـاً**  {mention} ❝

**⤶ قد اكـون مشغـول او غيـر موجـود حـاليـاً ؟!**
**⤶ ❨ لديـك** {warns} **مـن** {totalwarns} **تحذيـرات ⚠️❩**
**⤶ لا تقـم بـ إزعاجـي والا سـوف يتم ڪتمـك تلقـائياً . . .**

**⤶ فقط قل سبب مجيئك وانتظـر الـرد ⏳**"""
    elif gvarstatus("pmmenu") is None:
        USER_BOT_NO_WARN = f"""ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗮𝗥𝗮𝘀 **- الـرد التلقـائي 〽️**
**•─────────────────•**

❞ **مرحبـاً**  {mention} ❝

**⤶ قد اكـون مشغـول او غيـر موجـود حـاليـاً ؟!**
**⤶ ❨ لديـك** {warns} **مـن** {totalwarns} **تحذيـرات ⚠️❩**
**⤶ لا تقـم بـ إزعاجـي والا سـوف يتم حظـرك تلقـائياً . . .**

**⤶ فقط قل سبب مجيئك وانتظـر الـرد ⏳**"""
    else:
        USER_BOT_NO_WARN = f"""ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗮𝗥𝗮𝘀 **- الـرد التلقـائي 〽️**
**•─────────────────•**

❞ **مرحبـاً**  {mention} ❝

**⤶ قد اكـون مشغـول او غيـر موجـود حـاليـاً ؟!**
**⤶ ❨ لديـك** {warns} **مـن** {totalwarns} **تحذيـرات ⚠️❩**
**⤶ لا تقـم بـ إزعاجـي والا سـوف يتم حظـرك تلقـائياً . . .**

**⤶ فقط قل سبب مجيئك وانتظـر الـرد ⏳**"""
    addgvar("pmpermit_text", USER_BOT_NO_WARN)
    PM_WARNS[str(chat.id)] += 1
    try:
        if gvarstatus("pmmenu") is None:
            results = await event.client.inline_query(
                Config.TG_BOT_USERNAME, "pmpermit"
            )
            msg = await results[0].click(chat.id, reply_to=reply_to_id, hide_via=True)
        else:
            PM_PIC = gvarstatus("pmpermit_pic")
            if PM_PIC:
                CAT = [x for x in PM_PIC.split()]
                PIC = list(CAT)
                CAT_IMG = random.choice(PIC)
            else:
                CAT_IMG = None
            if CAT_IMG is not None:
                msg = await event.client.send_file(
                    chat.id,
                    CAT_IMG,
                    caption=USER_BOT_NO_WARN,
                    reply_to=reply_to_id,
                    force_document=False,
                )
            else:
                msg = await event.client.send_message(
                    chat.id, USER_BOT_NO_WARN, reply_to=reply_to_id
                )
    except Exception as e:
        LOGS.error(e)
        msg = await event.reply(USER_BOT_NO_WARN)
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    PMMESSAGE_CACHE[str(chat.id)] = msg.id
    sql.del_collection("pmwarns")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmwarns", PM_WARNS, {})
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})


@l313l.ar_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def on_new_private_message(event):
    if gvarstatus("pmpermit") is None:
        return
    chat = await event.get_chat()
    zel_dev = (5427469031, 5426390871)
    if chat.bot or chat.verified:
        return
    if pmpermit_sql.is_approved(chat.id):
        return
    if event.chat_id in zel_dev:
        reason = "**انـه احـد المطـورين المساعديـن 🥳♥️**"
        try:
            PM_WARNS = sql.get_collection("pmwarns").json
        except AttributeError:
            PM_WARNS = {}
        if not pmpermit_sql.is_approved(chat.id):
            if str(chat.id) in PM_WARNS:
                del PM_WARNS[str(chat.id)]
            start_date = str(datetime.now().strftime("%B %d, %Y"))
            pmpermit_sql.approve(
                chat.id, get_display_name(chat), start_date, chat.username, reason
            )
        return await event.client.send_message(chat, "**احد المطورين هنـا اننـي محظـوظ لقدومـك الـي 🙈♥️**")
    if chat.id in PMPERMIT_.TEMPAPPROVED:
        return
    if is_muted(event.chat_id, event.chat_id):
        return
    await do_pm_permit_action(event, chat)


@l313l.ar_cmd(outgoing=True, func=lambda e: e.is_private, edited=False, forword=None)
async def you_dm_other(event):
    if gvarstatus("pmpermit") is None:
        return
    chat = await event.get_chat()
    if chat.bot or chat.verified:
        return
    if event.text and event.text.startswith(
        (
            f"{cmdhd}بلوك",
            f"{cmdhd}رفض",
            f"{cmdhd}قبول",
            f"{cmdhd}da",
            f"{cmdhd}سماح",
            f"{cmdhd}tempapprove",
            f"{cmdhd}tempa",
            f"{cmdhd}tapprove",
            f"{cmdhd}ta",
        )
    ):
        return
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    start_date = str(datetime.now().strftime("%B %d, %Y"))
    if not pmpermit_sql.is_approved(chat.id) and str(chat.id) not in PM_WARNS:
        pmpermit_sql.approve(
            chat.id, get_display_name(chat), start_date, chat.username, "اووبس . . لـم يتـم رفضـه"
        )
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(chat.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(
                    chat.id, PMMESSAGE_CACHE[str(chat.id)]
                )
            except Exception as e:
                LOGS.info(str(e))
            del PMMESSAGE_CACHE[str(chat.id)]
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})


@l313l.ar_cmd(
    pattern="الحمايه (تفعيل|تعطيل)$",
    command=("الحمايه", plugin_category),
    info={
        "header": "لـ تفعيـل/تعطيـل حمـايـة الخـاص لـ حسـابـك",
        "الاسـتخـدام": "{tr}الحمايه تفعيل/تعطيل",
    },
)
async def pmpermit_on(event):
    "Turn on/off pmpermit."
    input_str = event.pattern_match.group(1)
    if input_str == "تفعيل":
        if gvarstatus("pmpermit") is None:
            addgvar("pmpermit", "true")
            await edit_delete(
                event, "**⎉╎تـم تفعيـل امـر حمايـه الخـاص .. بنجـاح 🔕☑️...**"
            )
        else:
            await edit_delete(event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُفعـل  🔐✅**")
    elif gvarstatus("pmpermit") is not None:
        delgvar("pmpermit")
        await edit_delete(
            event, "**⎉╎تـم تعطيـل أمـر حمايـة الخـاص .. بنجـاح 🔔☑️...**"
        )
    else:
        await edit_delete(event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُعطـل 🔓✅**")
    if input_str == "تعطيل":
        if gvarstatus("pmmenu") is None:
            addgvar("pmmenu", "false")
            await edit_delete(
                event,
                "**⎉╎تـم تعطيـل أمـر حمايـة الخـاص .. بنجـاح 🔔☑️...**",
            )
        else:
            await edit_delete(
                event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُعطـل 🔓✅**"
            )
    elif gvarstatus("pmmenu") is not None:
        delgvar("pmmenu")
        await edit_delete(
            event, "**⎉╎تـم تفعيـل امـر حمايـه الخـاص .. بنجـاح 🔕☑️...**"
        )
    else:
        await edit_delete(
            event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُفعـل  🔐✅**"
        )

@l313l.ar_cmd(
    pattern="الحماية (تفعيل|تعطيل)$",
    command=("الحماية", plugin_category),
    info={
        "header": "لـ تفعيـل/تعطيـل حمـايـة الخـاص لـ حسـابـك",
        "الاسـتخـدام": "{tr}الحماية تفعيل/تعطيل",
    },
)
async def pmpermit_on(event):
    "Turn on/off pmmenu."
    input_str = event.pattern_match.group(1)
    if input_str == "تفعيل":
        if gvarstatus("pmpermit") is None:
            addgvar("pmpermit", "true")
            await edit_delete(
                event, "**⎉╎تـم تفعيـل امـر حمايـه الخـاص .. بنجـاح 🔕☑️...**"
            )
        else:
            await edit_delete(event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُفعـل  🔐✅**")
    elif gvarstatus("pmpermit") is not None:
        delgvar("pmpermit")
        await edit_delete(
            event, "**⎉╎تـم تعطيـل أمـر حمايـة الخـاص .. بنجـاح 🔔☑️...**"
        )
    else:
        await edit_delete(event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُعطـل 🔓✅**")
    if input_str == "تعطيل":
        if gvarstatus("pmmenu") is None:
            addgvar("pmmenu", "false")
            await edit_delete(
                event,
                "**⎉╎تـم تعطيـل أمـر حمايـة الخـاص .. بنجـاح 🔔☑️...**",
            )
        else:
            await edit_delete(
                event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُعطـل 🔓✅**"
            )
    elif gvarstatus("pmmenu") is not None:
        delgvar("pmmenu")
        await edit_delete(
            event, "**⎉╎تـم تفعيـل امـر حمايـه الخـاص .. بنجـاح 🔕☑️...**"
        )
    else:
        await edit_delete(
            event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُفعـل  🔐✅**"
        )


@l313l.ar_cmd(
    pattern="(قبول|سماح)(?: |$)(.*)",
    command=("سماح", plugin_category),
    info={
        "header": "لـ السمـاح لـ شخـص بمـراسلتـك خـاص اثنـاء تفعيـل الحمـايـه",
        "الاسـتخـدام": [
            "{tr}قبول/سماح + المعـرف/بالـرد + السـبب فـي الكـروب",
            "{tr}قبول/سماح + السـبب فـي الخـاص",
        ],
    },
)
async def approve_p_m(event):  # sourcery no-metrics
    "To approve user to pm"
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"** ⎉╎لـيشتغل هذا الأمـر ...**\n** ⎉╎ يـجب تفعيـل امـر الحـمايـه اولاً **\n** ⎉╎بإرسـال** `{cmdhd}الحمايه تفعيل`",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(2)
        if is_muted(user.id, event.chat_id):
            try:
                unmute(user.id, event.chat_id)
            except Exception as e:
                await event.edit(f"**- خطــأ **\n`{e}`")
            await event.edit("**- تـم الغــاء كتــم الشخـص هنـا .. بنجــاح ✓**")
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الغــاء_كــتـم_حمـايـة_الخـاص\n"
                    f"**- الشخـص :** [{user.first_name}](tg://user?id={user.id})\n",
                )
    else:
        user, reason = await get_user_from_event(event, secondgroup=True)
        if not user:
            return
    if not reason:
        reason = "**⎉╎لـم يـذكـر 🤷🏻‍♂**"
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if not pmpermit_sql.is_approved(user.id):
        if str(user.id) in PM_WARNS:
            del PM_WARNS[str(user.id)]
        start_date = str(datetime.now().strftime("%B %d, %Y"))
        pmpermit_sql.approve(
            user.id, get_display_name(user), start_date, user.username, reason
        )
        chat = user
        await edit_delete(
            event,
            f"**⎉╎المستخـدم**  [{user.first_name}](tg://user?id={user.id})\n**⎉╎تـم السـمـاح لـه بـإرسـال الـرسـائـل 💬✓** \n **⎉╎ الـسـبـب ❔  :** {reason}",
        )
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(user.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(
                    user.id, PMMESSAGE_CACHE[str(user.id)]
                )
            except Exception as e:
                LOGS.info(str(e))
            del PMMESSAGE_CACHE[str(user.id)]
        sql.del_collection("pmwarns")
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmwarns", PM_WARNS, {})
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    else:
        await edit_delete(
            event,
            f"**⎉╎المستخـدم** [{user.first_name}](tg://user?id={user.id}) \n**⎉╎هـو بـالـفـعل فـي قـائـمـة الـسـمـاح ✅**",
        )


@l313l.ar_cmd(
    pattern="t(emp)?(a|approve)(?: |$)(.*)",
    command=("tapprove", plugin_category),
    info={
        "header": "To approve user to direct message you for temporarily.",
        "note": "Heroku restarts every 24 hours so with every restart it dissapproves every temp approved user",
        "الاسـتخـدام": [
            "{tr}ta/tapprove <username/reply reason> in group",
            "{tr}ta/tapprove <reason> in pm",
        ],
    },
)
async def tapprove_pm(event):  # sourcery no-metrics
    "Temporarily approve user to pm"
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"** ⎉╎لـيشتغل هذا الأمـر ...**\n** ⎉╎ يـجب تفعيـل امـر الحـمايـه اولاً **\n** ⎉╎بإرسـال** `{cmdhd}الحمايه تفعيل`",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(3)
    else:
        user, reason = await get_user_from_event(event, thirdgroup=True)
        if not user:
            return
    if not reason:
        reason = "**⎉╎لـم يـذكـر 🤷🏻‍♂**"
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
        
