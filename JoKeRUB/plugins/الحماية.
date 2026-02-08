import random
import re
from datetime import datetime

from telethon import Button, functions
from telethon.events import CallbackQuery
from telethon.utils import get_display_name

from JoKeRUB import l313l
from JoKeRUB.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format, get_user_from_event, reply_id
from ..sql_helper import global_collectionjson as sql
from ..sql_helper import global_list as sqllist
from ..sql_helper import pmpermit_sql
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import mention

LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER
# ترجمه وكتابة فريق الجوكر


async def do_pm_permit_action(event, chat):  # sourcery no-metrics
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
    try:
        MAX_FLOOD_IN_PMS = int(gvarstatus("MAX_FLOOD_IN_PMS") or 6)
    except (ValueError, TypeError):
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
        
        # التحقق من نوع العقوبة (كتم أم حظر)
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
            )  # ترجمه وكتابة فريق الجوكر
        else:
            if controlmute is not None:
                USER_BOT_WARN_ZERO = f"**⤶ لقـد حذرتـڪ مـسـبـقـاً مـن الـتـڪـرار 📵** \n**⤶ تـم ڪتمـك تلقـائيـاً .. الان لا يـمـڪـنـڪ ازعـاجـي🔕**\n\n**⤶ تحيـاتـي** {my_mention}  🫡"
            else:
                USER_BOT_WARN_ZERO = f"**⤶ لقـد حذرتـڪ مـسـبـقـاً مـن الـتـڪـرار 📵** \n**⤶ تـم حـظـرڪ تلقـائيـاً .. الان لا يـمـڪـنـڪ ازعـاجـي🔕**\n\n**⤶ تحيـاتـي** {my_mention}  🫡"
        
        if controlmute is not None:
            msg = await event.reply(USER_BOT_WARN_ZERO)
            # هنا يمكن إضافة دالة الكتم إذا كانت موجودة في SQL
            the_message = f"#حمـايـة_الخـاص\
                            \n** ⎉╎المستخـدم** [{get_display_name(chat)}](tg://user?id={chat.id}) .\
                            \n** ⎉╎تم كتمـه .. تلقائيـاً**\
                            \n** ⎉╎عـدد رسـائله :** {PM_WARNS[str(chat.id)]}"
        else:
            msg = await event.reply(USER_BOT_WARN_ZERO)
            await event.client(functions.contacts.BlockRequest(chat.id))
            the_message = f"#حمـايـة_الخـاص\
                            \n** ⎉╎المستخـدم** [{get_display_name(chat)}](tg://user?id={chat.id}) .\
                            \n** ⎉╎تم حظـره .. تلقائيـاً**\
                            \n** ⎉╎عـدد رسـائله :** {PM_WARNS[str(chat.id)]}"
        
        del PM_WARNS[str(chat.id)]
