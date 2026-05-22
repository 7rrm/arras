import json
import math
import asyncio
import os
import random
import re
import time
from pathlib import Path
from uuid import uuid4

from telethon import Button, types
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.types import InputWebDocument

from . import l313l
from ..Config import Config
from ..helpers import reply_id
from ..sql_helper.globals import gvarstatus, addgvar, delgvar
from ..core.logger import logging
from ..helpers.utils import _format
from . import mention

LOGS = logging.getLogger(__name__)
tr = Config.COMMAND_HAND_LER

scc = "secret"
hmm = "همسـة لـ"
ymm = "يستطيـع"
fmm = "• فتـح الهمسـه •"
dss = "⌔╎هو فقط من يستطيع ࢪؤيتهـا"
hss = "ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه 📨\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎الهمسـة لـ**"
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص)."
bmm = "اضغـط للـرد"
ttt = "ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه 📨\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎لـ أࢪسـال همسـه سـريـه الى**"
ddd = "💌"
bbb = None

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
    zelzal = None
    
    if gvarstatus("hmsa_user"):
        if username and username.startswith("@"):
            zelzal = gvarstatus("hmsa_user")
        elif full_name:
            zelzal = f"[{full_name}](tg://user?id={user_id})"
    
    # ========== وضع الهمسة للجميع ==========
    if string == "zelzal_all":
        hmsa_for_all = gvarstatus("hmsa_for_all")
        
        if not hmsa_for_all:
            result = builder.article(
                title="❌ الهمسة غير متاحة",
                description="تم أخذ هذه الهمسة بالفعل",
                text="**⌔╎عذراً .. هذه الهمسة تم أخذها من قبل شخص آخر**",
                buttons=[[Button.inline("✖️", data="close")]]
            )
            return await event.answer([result])
        
        # مسح كل شيء وتعيين المستخدم الجديد
        delgvar("hmsa_id")
        delgvar("hmsa_name")
        delgvar("hmsa_user")
        delgvar("hmsa_for_all")
        
        # تعيين المستخدم الحالي كالمستلم
        addgvar("hmsa_id", str(query_user_id))
        
        try:
            user_info = await l313l.get_entity(query_user_id)
            addgvar("hmsa_name", user_info.first_name)
            addgvar("hmsa_user", f"@{user_info.username}" if user_info.username else "None")
        except:
            addgvar("hmsa_name", "المستخدم")
            addgvar("hmsa_user", "None")
        
        # إنشاء الزر بنفس طريقة الكود الأصلي
        hmsa_id_value = gvarstatus("hmsa_id")
        if hmsa_id_value:
            query_text = f"secret {hmsa_id_value} \nهلو"
            bbb = [(Button.switch_inline("اضغـط هنـا", query=query_text, same_peer=True, style="primary"))]
            
            # جلب اسم المستخدم للعرض
            user_name = gvarstatus("hmsa_user") or gvarstatus("hmsa_name") or "الشخص"
            
            results = []
            results.append(
                builder.article(
                    title=f"📨 همسة للجميع",
                    description=f"أول شخص يفتحها",
                    text=f"**ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه 📨**\n"
                         f"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
                         f"**⌔╎الهمسـة لأول شخص يقوم بفتحها**",
                    buttons=bbb,
                    link_preview=False,
                ),
            )
            return await event.answer(results)
        else:
            return
    
    # ========== الكود الأصلي لـ zelzal ==========
    if string == "zelzal":
        if gvarstatus("hmsa_id"):
            hmsa_id_value = gvarstatus("hmsa_id")
            query_text = f"secret {hmsa_id_value} \nهلو"
            bbb = [(Button.switch_inline("اضغـط هنـا", query=query_text, same_peer=True, style="primary"))]
            results = []
            results.append(
                builder.article(
                    title=f"{nmm}",
                    description=f"{mnn}",
                    text=f"{ttt} {zelzal or 'الشخص'} **{ddd}**",
                    buttons=bbb,
                    link_preview=False,
                ),
            )
            return await event.answer(results)
        else:
            return
    
    # ========== معالجة secret ==========
    inf = re.compile(r"secret (\d+) (.*)")
    match = inf.match(query)
    if match:
        target_user_id = match.group(1)
        msg_text = match.group(2)
        
        if not msg_text or msg_text.strip() == "هلو":
            return
        
        user_list = [int(target_user_id)]
        zilzal = ""
        
        try:
            u = await l313l.get_entity(int(target_user_id))
            if u.username:
                zilzal = f"@{u.username}"
            else:
                zilzal = f"[{u.first_name}](tg://user?id={u.id})"
        except:
            zilzal = f"[المستخدم](tg://user?id={target_user_id})"
        
        old_msg = os.path.join("./JoKeRUB", f"{target_user_id}.txt")
        try:
            jsondata = json.load(open(old_msg))
        except Exception:
            jsondata = False
        
        timestamp = int(time.time() * 2)
        new_msg = {str(timestamp): {"userid": user_list, "text": msg_text, "sender_id": query_user_id}}
        
        buttons = [[Button.inline("• فتـح الهمسـه •", data=f"secret_{timestamp}", style="danger")]]
        thumb = InputWebDocument(
            url="https://graph.org/file/5c149c9217a0eba19983e-2fe63df9e99eed4541.jpg",
            size=0,
            mime_type="image/jpeg",
            attributes=[]
        )
        
        result = builder.article(
            title=f"همسـة لـ {zilzal}",
            description=f"{dss}",
            text=f"{hss} {zilzal} \n**{dss}**",
            buttons=buttons,
            link_preview=False,
            thumb=thumb,
        )
        
        await event.answer([result])
        
        if jsondata:
            jsondata.update(new_msg)
            json.dump(jsondata, open(old_msg, "w"))
        else:
            json.dump(new_msg, open(old_msg, "w"))
        return
    
    # ========== باقي الكود الأصلي للصلاحيات ==========
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, query)
        if match2:
            # ... الكود الأصلي ...
            pass
    elif query_user_id == user_id:
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, query)
        if match2:
            # ... الكود الأصلي ...
            pass
    else:
        return
