import json
import re
import os
import time
from telethon import Button, events
from telethon.tl.functions.users import GetUsersRequest

from . import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus

# النصوص الثابتة
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

@l313l.tgbot.on(events.InlineQuery)
async def inline_handler(event):
    try:
        builder = event.builder
        query_user_id = event.query.user_id
        
        # الحصول على بيانات المستخدم الهدف
        user_id = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
        full_name = gvarstatus("hmsa_name") if gvarstatus("hmsa_name") else "المستخدم"
        
        # إنشاء رابط المنشن
        zelzal = f"[{full_name}](tg://user?id={user_id})" if user_id else "المستخدم"
        
        # التحقق من صلاحيات المستخدم
        if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
            malathid = Config.OWNER_ID
        elif query_user_id == user_id:
            malathid = user_id
        else:
            return await event.answer([])

        # معالجة الأمر secret
        if event.text and event.text.startswith("secret "):
            try:
                query = event.text[7:]
                info_type = [hmm, ymm, fmm]
                
                # فصل المستخدمين عن النص
                if "|" in query:
                    iris, query = query.split("|", 1)
                    users = iris.strip().split()
                else:
                    users = [query.split()[0]]
                    query = " ".join(query.split()[1:]) if len(query.split()) > 1 else ""
                
                # بناء قائمة المستخدمين
                user_list = []
                zilzal = ""
                
                for user in users:
                    try:
                        usr = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else (int(user) if user.isdigit() else user)
                        try:
                            u = await l313l.get_entity(usr)
                        except ValueError:
                            u = await l313l(GetUsersRequest(usr))
                        
                        # إضافة منشن للمستخدم
                        zilzal += f"[{u.first_name}](tg://user?id={u.id}) "
                        user_list.append(u.id)
                    except Exception as e:
                        print(f"Error processing user {user}: {e}")
                        continue
                
                if not user_list:
                    return await event.answer([])
                
                zilzal = zilzal.strip()
                
                # حفظ الرسالة
                timestamp = int(time.time() * 2)
                new_msg = {str(timestamp): {"userid": user_list, "text": query}}
                os.makedirs("./JoKeRUB", exist_ok=True)
                old_msg = os.path.join("./JoKeRUB", f"{user_id}.txt")
                
                try:
                    if os.path.exists(old_msg):
                        with open(old_msg, "r") as f:
                            jsondata = json.load(f)
                        jsondata.update(new_msg)
                    else:
                        jsondata = new_msg
                    
                    with open(old_msg, "w") as f:
                        json.dump(jsondata, f)
                except Exception as e:
                    print(f"Error saving message: {e}")
                
                # إنشاء زر الرد
                buttons = [
                    [Button.inline(info_type[2], data=f"{scc}_{timestamp}")],
                    [Button.switch_inline(bmm, query=f"secret {malathid} \nهلو", same_peer=True)]
                ]
                
                result = builder.article(
                    title=f"{hmm} {zilzal}",
                    description=f"{dss}",
                    text=f"{hss} {zilzal} \n**{dss}**",
                    buttons=buttons,
                    link_preview=False,
                )
                await event.answer([result])
            
            except Exception as e:
                print(f"Error in secret handler: {e}")
                await event.answer([])
        
        # معالجة الأمر zelzal
        elif event.text and event.text.lower() == "zelzal":
            try:
                if user_id:
                    bbb = [Button.switch_inline(
                        "اضغـط هنـا", 
                        query=f"secret {user_id} \nهلو", 
                        same_peer=True
                    )]
                    
                    results = [builder.article(
                        title=nmm,
                        description=mnn,
                        text=f"**{ttt}** {zelzal} **{ddd}**",
                        buttons=bbb,
                        link_preview=False,
                    )]
                    
                    await event.answer(results)
                else:
                    await event.answer([])
            except Exception as e:
                print(f"Error in zelzal handler: {e}")
                await event.answer([])
    
    except Exception as e:
        print(f"Global error in inline handler: {e}")
        await event.answer([])
