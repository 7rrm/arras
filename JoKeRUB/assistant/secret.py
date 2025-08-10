import json
import os
import re
from datetime import datetime
from telethon import events, Button
from telethon.tl.functions.users import GetUsersRequest

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    uzerid = gvarstatus("hmsa_id")
    ussr = int(uzerid) if uzerid.isdigit() else uzerid
    myid = Config.OWNER_ID
    
    try:
        zzz = await l313l.get_entity(ussr)
    except ValueError:
        zzz = await l313l(GetUsersRequest(ussr))
    
    user_id = int(uzerid)
    file_name = f"./JoKeRUB/{user_id}.txt"
    
    if not os.path.exists(file_name):
        return await event.answer("❌ عذراً، هذه الهمسة لم تعد موجودة", alert=True)
    
    try:
        with open(file_name, "r") as f:
            jsondata = json.load(f)
        message = jsondata.get(str(timestamp), {})
        
        if not message:
            return await event.answer("❌ عذراً، هذه الهمسة منتهية الصلاحية", alert=True)
            
        allowed_users = [message["userid"], myid, zzz.id]
        
        if event.query.user_id not in allowed_users:
            return await event.answer("🔒 هذه الهمسة ليست لك!", alert=True)
            
        # عرض الهمسة للمستخدم
        await event.answer(f"📩 الهمسة: {message['text']}", alert=True)
        
        # تحديث الواجهة لإظهار أنها قُرئت
        await event.edit(
            text=f"# همسة سرية - aRRaS Whisper\n\n---\n\nالهمسة لـ {zzz.first_name}\n\n✅ تم قراءة الهمسة\n\nص {datetime.now().strftime('%H:%M')}",
            buttons=None
        )
        
        # حذف الهمسة بعد قراءتها (اختياري)
        del jsondata[str(timestamp)]
        with open(file_name, "w") as f:
            json.dump(jsondata, f)
            
    except Exception as e:
        LOGS.error(f"Error in secret callback: {str(e)}")
        await event.answer("❌ حدث خطأ أثناء محاولة عرض الهمسة", alert=True)
