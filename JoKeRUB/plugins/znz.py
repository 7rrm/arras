import json
import os
import re
import time
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

# تعريف النصوص الثابتة
scc = "secret"
hmm = "همسـة"
ymm = "يستطيـع"
fmm = "فتـح الهمسـه 🗳"
dss = "⌔╎هو فقط من يستطيع ࢪؤيتهـا"
hss = "ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - **همسـة سـريـه** 📠\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎الهمسـة لـ**"
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص)."
bmm = "اضغـط للـرد"
ttt = "ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔╎أضغـط الـزر بالأسفـل ⚓\n⌔╎لـ أࢪسـال همسـه سـريـه الى"
ddd = "💌"
bbb = None

@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    builder = event.builder
    result = None
    query = event.text
    string = query.lower()
    
    # معالجة معلومات المستخدم
    query_user_id = event.query.user_id
    user_id = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
    full_name = gvarstatus("hmsa_name") if gvarstatus("hmsa_name") else None
    username = gvarstatus("hmsa_user") if gvarstatus("hmsa_user") else None
    
    # تحديد هوية المرسل
    zelzal = None
    if gvarstatus("hmsa_user"):
        zelzal = gvarstatus("hmsa_user") if username.startswith("@") else f"[{full_name}](tg://user?id={user_id})"
    
    # تحديد صلاحيات المستخدم
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        malathid = Config.OWNER_ID
    elif query_user_id == user_id:
        malathid = user_id
    else:
        malathid = None
        
    # معالجة الهمسات
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS or query_user_id == user_id:
        # نمط الهمسة: secret <user> <message>
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, query)
        
        if match2:
            user_list = []
            zilzal = ""
            query = query[7:]  # إزالة كلمة secret
            
            # معالجة متعددة للمستلمين (باستخدام |)
            if "|" in query:
                iris, query = query.replace(" |", "|").replace("| ", "|").split("|")
                users = iris.split(" ")
            else:
                user, query = query.split(" ", 1)
                users = [user]
                
            # جمع معلومات المستلمين
            for user in users:
                usr = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else int(user)
                try:
                    u = await l313l.get_entity(usr)
                except ValueError:
                    u = await l313l(GetUsersRequest(usr))
                    
                zilzal += f"@{u.username}" if u.username else f"[{u.first_name}](tg://user?id={u.id})"
                zilzal += " "
                user_list.append(u.id)
                
            zilzal = zilzal[:-1]  # إزالة المسافة الأخيرة
            
            # حفظ الهمسة في ملف
            old_msg = os.path.join("./JoKeRUB", f"{user_id}.txt")
            try:
                with open(old_msg, "r") as f:
                    jsondata = json.load(f)
            except:
                jsondata = {}
                
            timestamp = int(time.time() * 2)
            new_msg = {
                str(timestamp): {
                    "userid": user_list,
                    "text": query,
                    "read": False  # حالة القراءة الافتراضية
                }
            }
            
            # إنشاء أزرار الهمسة
            buttons = [
                [Button.inline(fmm, data=f"{scc}_{timestamp}")],
                [Button.switch_inline(bmm, query=f"secret {malathid} \nهلو", same_peer=True)]
            ]
            
            # بناء نتيجة الإنلاين
            result = builder.article(
                title=f"{hmm} {zilzal}",
                description=f"{dss}",
                text=f"{hss} {zilzal} \n**{dss}**",
                buttons=buttons,
                link_preview=False,
            )
            
            await event.answer([result] if result else None)
            
            # تحديث ملف الهمسات
            jsondata.update(new_msg)
            with open(old_msg, "w") as f:
                json.dump(jsondata, f, indent=4)
                
        # حالة البحث عن zelzal
        elif string == "zelzal":
            if not gvarstatus("hmsa_id"):
                return
                
            bbb = [[Button.switch_inline("اضغـط هنـا", query=f"secret {gvarstatus('hmsa_id')} \nهلو", same_peer=True)]]
            
            results = [builder.article(
                title=nmm,
                description=mnn,
                text=f"**{ttt}** {zelzal} **{ddd}**",
                buttons=bbb,
                link_preview=False,
            )]
            
            await event.answer(results)
