import json
import os
import re
from telethon import Button
from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.functions.messages import UpdateInlineBotMessageRequest
from JoKeRUB import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_plug_in_callback_query_handler(event):
    try:
        # البيانات الأساسية
        timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
        uzerid = gvarstatus("hmsa_id")
        ussr = int(uzerid) if uzerid.isdigit() else uzerid
        myid = Config.OWNER_ID
        
        # الحصول على معلومات المستخدم
        try:
            zzz = await l313l.get_entity(ussr)
        except ValueError:
            zzz = await l313l(GetUsersRequest(ussr))
        
        # التحقق من ملف الهمسة
        user_id = int(uzerid)
        file_name = f"./JoKeRUB/{user_id}.txt"
        if not os.path.exists(file_name):
            return await event.answer("- عـذراً .. هذه الرسـالة لم تعد موجـوده.", alert=True)
        
        # قراءة محتوى الهمسة
        with open(file_name, 'r') as f:
            jsondata = json.load(f)
        
        if str(timestamp) not in jsondata:
            return await event.answer("- عـذراً .. الهمسة ليست موجهة لك !!", alert=True)
        
        message = jsondata[str(timestamp)]
        userid = message["userid"]
        ids = [userid, myid, zzz.id]
        
        # التحقق من صلاحيات المستخدم
        if event.query.user_id not in ids:
            return await event.answer("مطـي الهمسـه مـو الك 🧑🏻‍🦯🦓", alert=True)
        
        encrypted_tcxt = message["text"]
        
        # إذا كان المستخدم هو المستقبل (وليست المالك أو المساعد)
        if event.query.user_id == userid:
            # تحديث الرسالة الأصلية
            new_text = (
                f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه 📠\n"
                f"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
                f"⌔╎الهمسـة لـ {zzz.first_name}\n"
                f"⌔╎تمت قراءة الهمسة ✅"
            )
            
            new_buttons = [
                [Button.switch_inline("اضغـط للـرد", query=f"secret {myid} \nهلو", same_peer=True)]
            ]
            
            try:
                await event.client(
                    UpdateInlineBotMessageRequest(
                        peer=await event.get_input_chat(),
                        id=event.query.msg_id,
                        text=new_text,
                        buttons=new_buttons
                    )
                )
            except:
                pass
        
        # عرض محتوى الهمسة للمستخدم
        await event.answer(encrypted_tcxt, alert=True)
    
    except Exception as e:
        await event.answer("❌ حدث خطأ أثناء محاولة فتح الهمسة!", alert=True)
