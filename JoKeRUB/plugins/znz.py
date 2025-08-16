import json
import re
import os
import time
from telethon import Button
from telethon.tl.functions.users import GetUsersRequest

@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    builder = event.builder
    query_user_id = event.query.user_id
    user_id = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
    username = gvarstatus("hmsa_user") if gvarstatus("hmsa_user") else None
    
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS or query_user_id == user_id:
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, event.text)
        if match2:
            query = event.text[7:]
            if "|" in query:
                iris, query = query.replace(" |", "|").replace("| ", "|").split("|")
                users = iris.split(" ")
            else:
                user, query = query.split(" ", 1)
                users = [user]
            
            zilzal = ""
            user_list = []
            for user in users:
                usr = int(user) if user.isdigit() else user
                try:
                    u = await l313l.get_entity(usr)
                except ValueError:
                    u = await l313l(GetUsersRequest(usr))
                
                # التعديل الرئيسي هنا - استخدام المنشن المباشر فقط
                if u.username:
                    zilzal += f"@{u.username} "
                else:
                    zilzal += f"[{u.first_name}](tg://user?id={u.id}) "
                user_list.append(u.id)
            
            zilzal = zilzal.strip()
            timestamp = int(time.time() * 2)
            buttons = [
                [Button.inline("فتـح الهمسـه 🗳", data=f"secret_{timestamp}")],
                [Button.switch_inline("اضغـط للـرد", query=f"secret {query_user_id} \nهلو", same_peer=True)]
            ]
            
            result = builder.article(
                title=f"همسـة {zilzal}",
                description="⌔╎هو فقط من يستطيع ࢪؤيتهـا",
                text=f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - **همسـة سـريـه** 📠\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎الهمسـة لـ** {zilzal} \n**⌔╎هو فقط من يستطيع ࢪؤيتهـا**",
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result])
