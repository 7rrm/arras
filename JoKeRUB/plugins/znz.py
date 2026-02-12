import json
import math
import asyncio
import os
import random
import re
import time
import requests  # ✅ إضافة import requests
from pathlib import Path
from uuid import uuid4

from telethon import Button, types
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery
from telethon.tl.functions.users import GetUsersRequest

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
hss = "ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه 📨\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎الهمسـة لـ**"
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص)."
bmm = "اضغـط للـرد"
ttt = "ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه 📨\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎لـ أࢪسـال همسـه سريـه الى**"
ddd = "💌"
bbb = None

# 🎨 ايموجي بريميوم للزر
FIRE_EMOJI = "5368324170671202286"  # 🔥 ايموجي نار بريميوم

@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    builder = event.builder
    result = None
    query = event.text
    string = query.lower()
    query.split(" ", 2)
    str_y = query.split(" ", 1)
    string.split()
    query_user_id = event.query.user_id
    user_id = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
    full_name = gvarstatus("hmsa_name") if gvarstatus("hmsa_name") else None
    username = gvarstatus("hmsa_user") if gvarstatus("hmsa_user") else None
    zelzal = None
    if gvarstatus("hmsa_user"):
        if username.startswith("@"):
            zelzal = gvarstatus("hmsa_user")
        else:
            zelzal = f"[{full_name}](tg://user?id={user_id})"
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
            info_type = [hmm, ymm, fmm]
            if "|" in query:
                iris, query = query.replace(" |", "|").replace("| ", "|").split("|")
                users = iris.split(" ")
            else:
                user, query = query.split(" ", 1)
                users = [user]
            for user in users:
                usr = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else int(user)
                try:
                    u = await l313l.get_entity(usr)
                except ValueError:
                    u = await l313l(GetUsersRequest(usr))
                if u.username:
                    zilzal += f"@{u.username}"
                else:
                    zilzal += f"[{u.first_name}](tg://user?id={u.id})"
                user_list.append(u.id)
                zilzal += " "
            zilzal = zilzal[:-1]
            old_msg = os.path.join("./JoKeRUB", f"{user_id}.txt")
            try:
                jsondata = json.load(open(old_msg))
            except Exception:
                jsondata = False
            timestamp = int(time.time() * 2)
            new_msg = {
                str(timestamp): {"userid": user_list, "text": query}
            }
            
            # ✅ زر أزرق مع ايموجي ناري - باستخدام REST API
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "🔥 اضغـط هنـا 🔥",
                            "callback_data": f"{scc}_{timestamp}",
                            "style": "primary",  # 🔵 لون أزرق
                            "icon_custom_emoji_id": FIRE_EMOJI
                        }
                    ]
                ]
            }
            
            inline_data = {
                "inline_query_id": event.id,
                "results": json.dumps([
                    {
                        "type": "article",
                        "id": str(timestamp),
                        "title": f"{hmm} {zilzal}",
                        "description": f"{dss}",
                        "input_message_content": {
                            "message_text": f"{hss} {zilzal} \n**{dss}**",
                            "parse_mode": "Markdown"
                        },
                        "reply_markup": keyboard
                    }
                ]),
                "cache_time": 0,
                "is_personal": True
            }
            
            try:
                requests.post(url, json=inline_data)
                print(f"✅ تم إرسال الهمسة مع الزر الأزرق للمستخدم {user_id}")
            except Exception as e:
                print(f"❌ خطأ في إرسال الزر: {e}")
                
            if jsondata:
                jsondata.update(new_msg)
                json.dump(jsondata, open(old_msg, "w"))
            else:
                json.dump(new_msg, open(old_msg, "w"))
            return  # ✅ مهم: نرجع بعد الإرسال
            
        elif string == "zelzal":
            if gvarstatus("hmsa_id"):
                # ✅ زر أزرق مع ايموجي ناري للهمسة الرئيسية
                url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
                
                keyboard = {
                    "inline_keyboard": [
                        [
                            {
                                "text": "🔥 اضغـط هنـا 🔥",
                                "switch_inline_query": f"secret {gvarstatus('hmsa_id')} \nهلو",
                                "style": "primary",  # 🔵 لون أزرق
                                "icon_custom_emoji_id": FIRE_EMOJI
                            }
                        ]
                    ]
                }
                
                inline_data = {
                    "inline_query_id": event.id,
                    "results": json.dumps([
                        {
                            "type": "article",
                            "id": "zelzal",
                            "title": f"{nmm}",
                            "description": f"{mnn}",
                            "input_message_content": {
                                "message_text": f"{ttt} {zelzal} **{ddd}**",
                                "parse_mode": "Markdown"
                            },
                            "reply_markup": keyboard
                        }
                    ]),
                    "cache_time": 0,
                    "is_personal": True
                }
                
                try:
                    requests.post(url, json=inline_data)
                    print(f"✅ تم إرسال زر الهمسة الأزرق للمستخدم {user_id}")
                except Exception as e:
                    print(f"❌ خطأ: {e}")
                return  # ✅ مهم: نرجع بعد الإرسال
            else:
                return
                
    elif query_user_id == user_id:
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, query)
        if match2:
            user_list = []
            zilzal = ""
            query = query[7:]
            info_type = [hmm, ymm, fmm]
            if "|" in query:
                iris, query = query.replace(" |", "|").replace("| ", "|").split("|")
                users = iris.split(" ")
            else:
                user, query = query.split(" ", 1)
                users = [user]
            for user in users:
                usr = int(user) if user.isdigit() else user
                try:
                    u = await l313l.get_entity(usr)
                except ValueError:
                    u = await l313l(GetUsersRequest(usr))
                if u.username:
                    zilzal += f"@{u.username}"
                else:
                    zilzal += f"[{u.first_name}](tg://user?id={u.id})"
                user_list.append(u.id)
                zilzal += " "
            zilzal = zilzal[:-1]
            old_msg = os.path.join("./JoKeRUB", f"{user_id}.txt")
            try:
                jsondata = json.load(open(old_msg))
            except Exception:
                jsondata = False
            timestamp = int(time.time() * 2)
            new_msg = {
                str(timestamp): {"userid": user_list, "text": query}
            }
            
            # ✅ زر أزرق مع ايموجي ناري
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "🔥 اضغـط هنـا 🔥",
                            "callback_data": f"{scc}_{timestamp}",
                            "style": "primary",  # 🔵 لون أزرق
                            "icon_custom_emoji_id": FIRE_EMOJI
                        }
                    ]
                ]
            }
            
            inline_data = {
                "inline_query_id": event.id,
                "results": json.dumps([
                    {
                        "type": "article",
                        "id": str(timestamp),
                        "title": f"{hmm} {zilzal}",
                        "description": f"{dss}",
                        "input_message_content": {
                            "message_text": f"{hss} {zilzal} \n{dss}",
                            "parse_mode": "Markdown"
                        },
                        "reply_markup": keyboard
                    }
                ]),
                "cache_time": 0,
                "is_personal": True
            }
            
            try:
                requests.post(url, json=inline_data)
                print(f"✅ تم إرسال الهمسة مع الزر الأزرق للمستخدم {user_id}")
            except Exception as e:
                print(f"❌ خطأ: {e}")
                
            if jsondata:
                jsondata.update(new_msg)
                json.dump(jsondata, open(old_msg, "w"))
            else:
                json.dump(new_msg, open(old_msg, "w"))
            return  # ✅ مهم: نرجع بعد الإرسال
                
        elif string == "zelzal":
            if gvarstatus("hmsa_id"):
                # ✅ زر أزرق مع ايموجي ناري للهمسة الرئيسية
                url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
                
                keyboard = {
                    "inline_keyboard": [
                        [
                            {
                                "text": "🔥 اضغـط هنـا 🔥",
                                "switch_inline_query": f"secret {gvarstatus('hmsa_id')} \nهلو",
                                "style": "primary",  # 🔵 لون أزرق
                                "icon_custom_emoji_id": FIRE_EMOJI
                            }
                        ]
                    ]
                }
                
                inline_data = {
                    "inline_query_id": event.id,
                    "results": json.dumps([
                        {
                            "type": "article",
                            "id": "zelzal",
                            "title": f"{nmm}",
                            "description": f"{mnn}",
                            "input_message_content": {
                                "message_text": f"**{ttt}** {zelzal} **{ddd}**",
                                "parse_mode": "Markdown"
                            },
                            "reply_markup": keyboard
                        }
                    ]),
                    "cache_time": 0,
                    "is_personal": True
                }
                
                try:
                    requests.post(url, json=inline_data)
                    print(f"✅ تم إرسال زر الهمسة الأزرق للمستخدم {user_id}")
                except Exception as e:
                    print(f"❌ خطأ: {e}")
                return  # ✅ مهم: نرجع بعد الإرسال
            else:
                return
    else:
        return
