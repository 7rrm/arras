import json
import math
import asyncio
import os
import random
import re
import time
from pathlib import Path
from uuid import uuid4
from datetime import datetime

from telethon import Button, types
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery
from telethon.tl.functions.users import GetUsersRequest
from telethon.utils import get_display_name

from . import l313l
from ..Config import Config
from ..helpers import reply_id
from ..sql_helper.globals import gvarstatus
from ..core.logger import logging
from ..helpers.utils import _format
from . import mention

LOGS = logging.getLogger(__name__)
tr = Config.COMMAND_HAND_LER

scc = "secret"
hmm = "همسـة"
ymm = "يستطيـع"
fmm = "• فتـح الهمسـه •"
dss = "⌔╎هو فقط من يستطيع ࢪؤيتهـا"
hss = f'''\
<tg-emoji emoji-id="5210763312597326700">📨</tg-emoji> <b>𝗮𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽 - همسـة سـريـه</b> <tg-emoji emoji-id="5210740682414644888">✅</tg-emoji>
<b>⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆</b>
<b>⌔╎الهمسـة لـ</b>'''
nmm = f'''<tg-emoji emoji-id="5210763312597326700">📨</tg-emoji> همسـه سـريـه <tg-emoji emoji-id="5210740682414644888">✅</tg-emoji>'''
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص)."
bmm = "اضغـط للـرد"
ttt = f'''\
<tg-emoji emoji-id="5210763312597326700">📨</tg-emoji> <b>𝗮𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽 - همسـة سـريـه</b> <tg-emoji emoji-id="5210740682414644888">✅</tg-emoji>
<b>⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆</b>
<b>⌔╎لـ أࢪسـال همسـه سـريـه الى</b>'''
ddd = f'''<tg-emoji emoji-id="5291726645658944556">💌</tg-emoji>'''
bbb = None

# Copyright (C) 2023 Zilzalll . All Rights Reserved
@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    builder = event.builder
    result = None
    query = event.text
    string = query.lower()
    query_user_id = event.query.user_id
    user_id = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
    full_name = gvarstatus("hmsa_name") if gvarstatus("hmsa_name") else None
    username = gvarstatus("hmsa_user") if gvarstatus("hmsa_user") else None
    
    # إنشاء اسم المستلم بشكل مرتبط
    zelzal = None
    if gvarstatus("hmsa_user"):
        if username and username.startswith("@"):
            try:
                receiver = await l313l.get_entity(username)
                receiver_name = f'<a href="tg://user?id={receiver.id}">{get_display_name(receiver)}</a>'
                zelzal = receiver_name
            except:
                zelzal = username
        elif full_name:
            zelzal = f'<a href="tg://user?id={user_id}">{full_name}</a>'
        else:
            zelzal = f'<a href="tg://user?id={user_id}">المستخدم</a>'
    
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        malathid = Config.OWNER_ID
    elif query_user_id == user_id:
        malathid = user_id
    else:
        malathid = None
    
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, query)
        if match2:
            user_list = []
            zilzal = ""
            query = query[7:]
            
            if "|" in query:
                iris, query = query.replace(" |", "|").replace("| ", "|").split("|")
                users = iris.split(" ")
            else:
                user, query = query.split(" ", 1)
                users = [user]
            
            # إنشاء نص المستلمين مع روابط
            receiver_links = []
            for user in users:
                usr = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else int(user)
                try:
                    u = await l313l.get_entity(usr)
                except ValueError:
                    u = await l313l(GetUsersRequest(usr))
                
                if u.username:
                    receiver_links.append(f'<a href="tg://user?id={u.id}">{get_display_name(u)}</a>')
                else:
                    receiver_links.append(f'<a href="tg://user?id={u.id}">{get_display_name(u)}</a>')
                user_list.append(u.id)
            
            zilzal = " و ".join(receiver_links)
            
            old_msg = os.path.join("./JoKeRUB", f"{user_id}.txt")
            try:
                jsondata = json.load(open(old_msg))
            except Exception:
                jsondata = False
            
            timestamp = int(time.time() * 2)
            new_msg = {
                str(timestamp): {
                    "userid": user_list, 
                    "text": query,
                    "sender_id": query_user_id,
                    "timestamp": timestamp
                }
            }
            
            # زر الفتح بإيموجي بريميوم
            buttons = [[
                Button.inline(
                    f'''<tg-emoji emoji-id="5210740682414644888">✅</tg-emoji> {fmm}''', 
                    data=f"{scc}_{timestamp}"
                )
            ]]
            
            # نص الهمسة مع إيموجي بريميوم
            secret_text = f'''\
<tg-emoji emoji-id="5210763312597326700">📨</tg-emoji> <b>𝗮𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽 - همسـة سـريـه</b> <tg-emoji emoji-id="5210740682414644888">✅</tg-emoji>
<b>⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆</b>
<b>⌔╎الهمسـة لـ</b> {zilzal}
<b>⌔╎{dss}</b>'''
            
            result = builder.article(
                title=f"📨 همسـة سـريـه لـ {len(user_list)} أشخاص",
                description="همسـة سـريـه للمستلمين المحددين",
                text=secret_text,
                buttons=buttons,
                link_preview=False,
                parse_mode='html'
            )
            await event.answer([result] if result else None)
            
            if jsondata:
                jsondata.update(new_msg)
                json.dump(jsondata, open(old_msg, "w"))
            else:
                json.dump(new_msg, open(old_msg, "w"))
        
        elif string == "zelzal":
            if not zelzal:
                return
            
            # زر الإنلاين مع إيموجي بريميوم
            bbb = [[
                Button.switch_inline(
                    f'''<tg-emoji emoji-id="5210740682414644888">✅</tg-emoji> {bmm}''', 
                    query=f"secret {user_id} \nاهـلـوࢪلـو",
                    same_peer=True
                )
            ]]
            
            # نص الرسالة مع إيموجي بريميوم (مشابه لملف القراءة)
            message_text = f'''\
<tg-emoji emoji-id="5210763312597326700">📨</tg-emoji> <b>𝗮𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽 - همسـة سـريـه</b> <tg-emoji emoji-id="5210740682414644888">✅</tg-emoji>
<b>⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆</b>
<b>⌔╎اضغـط الـزر بالاسفـل</b> <tg-emoji emoji-id="5258215850745275216">⚓</tg-emoji>
<b>⌔╎لـ اࢪسـال همسـه سـࢪيـه الى</b> {zelzal}
<b>{ddd}</b>'''
            
            results = []
            results.append(
                builder.article(
                    title=f"📨 همسـة سـريـه",
                    description=f"لإرسال همسة سرية إلى {full_name or username}",
                    text=message_text,
                    buttons=bbb,
                    link_preview=False,
                    parse_mode='html'
                ),
            )
            await event.answer(results)
    
    elif query_user_id == user_id:
        # ... (نفس الكود السابق للمستخدم العادي مع التعديلات المشابهة)
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, query)
        if match2:
            user_list = []
            zilzal = ""
            query = query[7:]
            
            if "|" in query:
                iris, query = query.replace(" |", "|").replace("| ", "|").split("|")
                users = iris.split(" ")
            else:
                user, query = query.split(" ", 1)
                users = [user]
            
            receiver_links = []
            for user in users:
                usr = int(user) if user.isdigit() else user
                try:
                    u = await l313l.get_entity(usr)
                except ValueError:
                    u = await l313l(GetUsersRequest(usr))
                
                if u.username:
                    receiver_links.append(f'<a href="tg://user?id={u.id}">{get_display_name(u)}</a>')
                else:
                    receiver_links.append(f'<a href="tg://user?id={u.id}">{get_display_name(u)}</a>')
                user_list.append(u.id)
            
            zilzal = " و ".join(receiver_links)
            
            old_msg = os.path.join("./JoKeRUB", f"{user_id}.txt")
            try:
                jsondata = json.load(open(old_msg))
            except Exception:
                jsondata = False
            
            timestamp = int(time.time() * 2)
            new_msg = {
                str(timestamp): {
                    "userid": user_list, 
                    "text": query,
                    "sender_id": query_user_id,
                    "timestamp": timestamp
                }
            }
            
            buttons = [[
                Button.inline(
                    f'''<tg-emoji emoji-id="5210740682414644888">✅</tg-emoji> {fmm}''', 
                    data=f"{scc}_{timestamp}"
                )
            ]]
            
            secret_text = f'''\
<tg-emoji emoji-id="5210763312597326700">📨</tg-emoji> <b>𝗮𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽 - همسـة سـريـه</b> <tg-emoji emoji-id="5210740682414644888">✅</tg-emoji>
<b>⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆</b>
<b>⌔╎الهمسـة لـ</b> {zilzal}
<b>⌔╎{dss}</b>'''
            
            result = builder.article(
                title=f"📨 همسـة سـريـه لـ {len(user_list)} أشخاص",
                description="همسـة سـريـه للمستلمين المحددين",
                text=secret_text,
                buttons=buttons,
                link_preview=False,
                parse_mode='html'
            )
            await event.answer([result] if result else None)
            
            if jsondata:
                jsondata.update(new_msg)
                json.dump(jsondata, open(old_msg, "w"))
            else:
                json.dump(new_msg, open(old_msg, "w"))
        
        elif string == "zelzal":
            if not zelzal:
                return
            
            bbb = [[
                Button.switch_inline(
                    f'''<tg-emoji emoji-id="5210740682414644888">✅</tg-emoji> {bmm}''', 
                    query=f"secret {user_id} \nاهـلـوࢪلـو",
                    same_peer=True
                )
            ]]
            
            message_text = f'''\
<tg-emoji emoji-id="5210763312597326700">📨</tg-emoji> <b>𝗮𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽 - همسـة سـريـه</b> <tg-emoji emoji-id="5210740682414644888">✅</tg-emoji>
<b>⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆</b>
<b>⌔╎اضغـط الـزر بالاسفـل</b> <tg-emoji emoji-id="5258215850745275216">⚓</tg-emoji>
<b>⌔╎لـ اࢪسـال همسـه سـࢪيـه الى</b> {zelzal}
<b>{ddd}</b>'''
            
            results = []
            results.append(
                builder.article(
                    title=f"📨 همسـة سـريـه",
                    description=f"لإرسال همسة سرية إلى {full_name or username}",
                    text=message_text,
                    buttons=bbb,
                    link_preview=False,
                    parse_mode='html'
                ),
            )
            await event.answer(results)
    else:
        return
