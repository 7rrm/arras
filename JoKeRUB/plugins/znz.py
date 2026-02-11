import json
import os
import re
import time
from telethon import Button, types
from telethon.events import InlineQuery
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.types import InputBotInlineResult, InputBotInlineMessageText, InputWebDocument

from . import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus

# 🎯 إيموجيات بريميوم - نفس IDs ملف sii.py
MAIL_EMOJI_ID = "5210763312597326700"      # 📨
CHECK_EMOJI_ID = "5210740682414644888"     # ✅
CHECK_GREEN_ID = "5843826335088120045"     # ✅ أخضر
CLOCK_EMOJI_ID = "5839380464116175529"     # 🕖
FIRE_EMOJI_ID = "5368324170671202286"      # 🔥
LOCK_EMOJI_ID = "5341741293349680948"      # 🔒
UNLOCK_EMOJI_ID = "5341741293789691996"    # 🔓
HEART_EMOJI_ID = "5316347681116269519"     # ❤️
STAR_EMOJI_ID = "5316347681116269521"      # ⭐
CROWN_EMOJI_ID = "5316347681116269523"     # 👑
GEM_EMOJI_ID = "5316347681116269524"       # 💎
SPEECH_EMOJI_ID = "5210763312597326701"    # 💬
ROBOT_EMOJI_ID = "5210763312597326702"     # 🤖

scc = "secret"
hmm = "همسـة"
ymm = "يستطيـع"
fmm = "• فتـح الهمسـه •"
dss = "⌔╎هو فقط من يستطيع ࢪؤيتهـا"
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص)."

@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    query = event.text
    string = query.lower()
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
    
    # ✅ السماح للمالك والسودو والمستخدم المحدد
    is_allowed = (
        query_user_id == Config.OWNER_ID or 
        query_user_id in Config.SUDO_USERS or 
        query_user_id == user_id
    )
    
    if not is_allowed:
        return
    
    # ============== زر zelzal الرئيسي ==============
    if string == "zelzal":
        if not gvarstatus("hmsa_id"):
            return
        
        # ✅ ✅ ✅ نفس تنسيق ملف sii.py بالضبط ✅ ✅ ✅
        message_text = f'''\
<tg-emoji emoji-id="{MAIL_EMOJI_ID}">📨</tg-emoji> <b>آراس ويسبر - همسة سريـة</b> <tg-emoji emoji-id="{LOCK_EMOJI_ID}">🔒</tg-emoji>

<tg-emoji emoji-id="{FIRE_EMOJI_ID}">🔥</tg-emoji> <b>الهمسة موجهة إلى:</b> {zelzal}

<tg-emoji emoji-id="{CHECK_EMOJI_ID}">✅</tg-emoji> <b>اضغط الزر بالأسفل لإرسال همسة</b>

<tg-emoji emoji-id="{CROWN_EMOJI_ID}">👑</tg-emoji> <i>همسة خاصة - لا يراها إلا المستقبل</i>'''
        
        # ✅ زر switch_inline عادي
        buttons = [[
            Button.switch_inline(
                "🔥 همسة سريـة",
                query=f"secret {gvarstatus('hmsa_id')} \nهلو",
                same_peer=True
            )
        ]]
        
        # ✅ ✅ ✅ الطريقة الصحيحة لـ Inline Mode ✅ ✅ ✅
        result = await event.builder._build_article(
            title=nmm,
            description=mnn,
            text=message_text,
            buttons=buttons,
            link_preview=False,
            parse_mode="html"
        )
        
        await event.answer([result])
    
    # ============== إرسال همسة جديدة ==============
    elif query.startswith("secret "):
        query = query[7:]
        user_list = []
        zilzal = ""
        
        if "|" in query:
            iris, msg_text = query.replace(" |", "|").replace("| ", "|").split("|")
            users = iris.split(" ")
        else:
            user, msg_text = query.split(" ", 1)
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
        
        # حفظ الهمسة
        old_msg = os.path.join("./JoKeRUB", f"{user_id}.txt")
        try:
            jsondata = json.load(open(old_msg))
        except Exception:
            jsondata = False
        
        timestamp = int(time.time() * 2)
        new_msg = {str(timestamp): {"userid": user_list, "text": msg_text}}
        
        # ✅ ✅ ✅ نص الهمسة مع إيموجي بريميوم - زي sii.py ✅ ✅ ✅
        hmsa_text = f'''\
<tg-emoji emoji-id="{MAIL_EMOJI_ID}">📨</tg-emoji> <b>الهمسة السريـة</b> <tg-emoji emoji-id="{LOCK_EMOJI_ID}">🔒</tg-emoji>

<tg-emoji emoji-id="{FIRE_EMOJI_ID}">🔥</tg-emoji> <b>إلى:</b> {zilzal}

<tg-emoji emoji-id="{SPEECH_EMOJI_ID}">💬</tg-emoji> <b>الرسالة:</b>
<i>"{msg_text}"</i>

<tg-emoji emoji-id="{CHECK_EMOJI_ID}">✅</tg-emoji> <b>فقط المستقبل يمكنه فتحها</b>'''
        
        buttons = [[
            Button.inline("• فتـح الهمسـه •", data=f"{scc}_{timestamp}")
        ]]
        
        # ✅ ✅ ✅ استخدام نفس الطريقة ✅ ✅ ✅
        result = await event.builder._build_article(
            title=f"{hmm} {zilzal}",
            description=dss,
            text=hmsa_text,
            buttons=buttons,
            link_preview=False,
            parse_mode="html"
        )
        
        await event.answer([result] if result else None)
        
        if jsondata:
            jsondata.update(new_msg)
            json.dump(jsondata, open(old_msg, "w"))
        else:
            json.dump(new_msg, open(old_msg, "w"))
