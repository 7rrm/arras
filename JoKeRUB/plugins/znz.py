import json
import re
import os
import time
from telethon import Button
from telethon.tl.functions.users import GetUsersRequest

from . import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

# المتغيرات الأصلية كما هي
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

@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    builder = event.builder
    query_user_id = event.query.user_id
    user_id = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
    full_name = gvarstatus("hmsa_name") if gvarstatus("hmsa_name") else None
    username = gvarstatus("hmsa_user") if gvarstatus("hmsa_user") else None
    
    # إنشاء منشن من المتغيرات الموجودة
    zelzal = f"[{full_name}](tg://user?id={user_id})" if user_id else None

    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        malathid = Config.OWNER_ID
    elif query_user_id == user_id:
        malathid = user_id
    else:
        malathid = None

    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS or query_user_id == user_id:
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, event.text)
        if match2:
            user_list = []
            zilzal = ""
            query = event.text[7:]
            
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
                    # استخدام المنشن بدلاً من اليوزر
                    zilzal += f"[{u.first_name}](tg://user?id={u.id}) "
                    user_list.append(u.id)
                except Exception as e:
                    LOGS.error(f"Error getting user entity: {e}")
                    continue

            zilzal = zilzal.strip()
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
                    "read": False,
                    "sender_id": event.query.user_id
                }
            }

            # استخدام المتغيرات الأصلية مع تعديل بسيط
            text_message = (
                f"{ttt} {zilzal} {ddd}"
            )

            buttons = [
                [Button.inline(fmm, data=f"{scc}_{timestamp}")],
                [Button.switch_inline(bmm, query=f"secret {malathid} \nهلو", same_peer=True)]
            ]

            result = builder.article(
                title=f"{hmm} {zilzal}",
                description=f"{dss}",
                text=text_message,
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)

            if jsondata:
                jsondata.update(new_msg)
                json.dump(jsondata, open(old_msg, "w"))
            else:
                json.dump(new_msg, open(old_msg, "w"))

        elif event.text.lower() == "zelzal":
            if zelzal:
                bbb = [[Button.switch_inline("اضغـط هنـا", query=f"secret {user_id} \nهلو", same_peer=True)]]
                
                results = []
                results.append(
                    builder.article(
                        title=f"{nmm}",
                        description=f"{mnn}",
                        text=f"**{ttt}** {zelzal} **{ddd}**",
                        buttons=bbb,
                        link_preview=False,
                    ),
                )
                await event.answer(results)
