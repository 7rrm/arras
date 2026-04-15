
import asyncio
import time
import io
import os
import shutil
import random
import logging
import glob

from datetime import datetime
from math import sqrt
from asyncio import sleep
from asyncio.exceptions import TimeoutError

from telethon import functions, types
from telethon.sync import errors
from telethon import events
from telethon.tl import functions
from telethon.errors import UserNotParticipantError

from telethon.tl.types import ChannelParticipantsAdmins

from . import l313l

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id
from ..helpers.utils import _format, get_user_from_event, reply_id 
from . import BOTLOG, BOTLOG_CHATID, mention, progress

LOGS = logging.getLogger(__name__)
plugin_category = "الادمن"


moment_worker = []
@l313l.ar_cmd(pattern="all?(.*)")
async def tagall(event):
  global moment_worker
  if event.is_private:
    return await edit_or_reply(event, "**- عـذراً ... هـذه ليـست مجمـوعـة ؟!**")
  if event.pattern_match.group(1):
    mode = "by_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "by_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await edit_or_reply(event, "**- عـذراً ... الرسـالة غيـر ظـاهـرة للأعضـاء الجـدد ؟!**")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await edit_or_reply(event, "**- اضـف نـص لـ الامـر . . .**\n\n**- مثـال :** `.all وينكـم`")
  else:
    return await edit_or_reply(event, "**- بالـرد عـلى رسـالـه . . او باضـافة نـص مـع الامـر**")
  if mode == "by_cmd":
    moment_worker.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in l313l.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"- [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await edit_or_reply(event, "**⎉╎تم إيقـاف التـاك .. بنجـاح ✓**")
        return
      if usrnum == 5:
        await l313l.send_message(event.chat_id, f"{usrtxt}\n\n- {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
  if mode == "by_reply":
    moment_worker.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in l313l.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"- [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await edit_or_reply(event, "**⎉╎تم إيقـاف التـاك .. بنجـاح ✓**")
        return
      if usrnum == 5:
        await l313l.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""



@l313l.ar_cmd(pattern="ايقاف التاك?(.*)")
async def stop_tagall(event):
  if not event.chat_id in moment_worker:
    return await edit_or_reply(event, '**- عـذراً .. لا يوجـد هنـاك تـاك لـ إيقـافـه ؟!**')
  else:
    try:
      moment_worker.remove(event.chat_id)
    except:
      pass
    return await edit_or_reply(event, '**⎉╎تم إيقـاف التـاك .. بنجـاح ✓**')


@l313l.ar_cmd(pattern="تاك(?:\s|$)([\s\S]*)")
async def tagall(event):
  global moment_worker
  if event.is_private:
    return await edit_or_reply(event, "**- عـذراً ... هـذه ليـست مجمـوعـة ؟!**")
  if event.pattern_match.group(1):
    mode = "by_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "by_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await edit_or_reply(event, "**- عـذراً ... الرسـالة غيـر ظـاهـرة للأعضـاء الجـدد ؟!**")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await edit_or_reply(event, "**- اضـف نـص لـ الامـر . . .**\n\n**- مثـال :** `.all وينكـم`")
  else:
    return await edit_or_reply(event, "**- بالـرد عـلى رسـالـه . . او باضـافة نـص مـع الامـر**")
  if mode == "by_cmd":
    moment_worker.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in l313l.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"- [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await edit_or_reply(event, "**⎉╎تم إيقـاف التـاك .. بنجـاح ✓**")
        return
      if usrnum == 5:
        await l313l.send_message(event.chat_id, f"{usrtxt}\n\n- {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
  if mode == "by_reply":
    moment_worker.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in l313l.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"- [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await edit_or_reply(event, "**⎉╎تم إيقـاف التـاك .. بنجـاح ✓**")
        return
      if usrnum == 5:
        await l313l.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""



@l313l.ar_cmd(
    pattern="اذكر(?:\s|$)([\s\S]*)",
    command=("اذكر", plugin_category),
    info={
        "header": "لـ جـلب اسـم الشخـص بشكـل ماركـدون ⦇.منشن بالـرد او + معـرف/ايـدي الشخص⦈ ",
        "الاسـتخـدام": "{tr}منشن <username/userid/reply>",
    },
)
async def permalink(event):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(event)
    if not user:
        return
    if custom:
        return await edit_or_reply(event, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(event, f"[{tag}](tg://user?id={user.id})")




spam_chats = []

@l313l.ar_cmd(pattern="منشن(?:\s|$)([\s\S]*)")
async def menall(event):
    chat_id = event.chat_id
    if event.is_private:
        return await edit_or_reply(event, "** ᯽︙ هذا الامر يستعمل للقنوات والمجموعات فقط !**")
    msg = event.pattern_match.group(1)
    if not msg:
        return await edit_or_reply(event, "** ᯽︙ ضع رسالة للمنشن اولاً**")
    is_admin = False
    try:
        partici_ = await l313l(GetParticipantRequest(
          event.chat_id,
          event.sender_id
        ))
    except UserNotParticipantError:
        is_admin = False
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ''
    async for usr in l313l.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        usrtxt = f"{msg}\n[{usr.first_name}](tg://user?id={usr.id}) "
        await l313l.send_message(chat_id, usrtxt)
        await asyncio.sleep(2)
        await event.delete()
    try:
        spam_chats.remove(chat_id)
    except:
        pass
@l313l.ar_cmd(pattern="الغاء منشن")
async def ca_sp(event):
  if not event.chat_id in spam_chats:
    return await edit_or_reply(event, "** ᯽︙ 🤷🏻 لا يوجد منشن لألغائه**")
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await edit_or_reply(event, "** ᯽︙ تم الغاء المنشن بنجاح ✓**")

