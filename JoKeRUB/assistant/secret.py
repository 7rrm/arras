import json
import os
import re
from datetime import datetime

from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.functions.messages import EditMessageRequest
from telethon import Button
from telethon.utils import get_display_name

from JoKeRUB import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus

# في دالة on_callback_query
@l313l.tgbot.on(CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_secret_open(event):
    secret_id = event.pattern_match.group(1).decode("UTF-8")
    user_id = event.query.user_id

    # البحث عن الهمسة في جميع ملفات JSON (أو يمكن تحديد ملف المستلم)
    # هنا سنفترض أن الهمسة محفوظة في ملف باسم whispers_XXXX.json
    # لكن الأسهل: نبحث في مجلد JoKeRUB عن أي ملف ونفتحه
    whispers_dir = "./JoKeRUB"
    found = False
    secret_text = ""
    sender_id = None
    user_list = []

    for filename in os.listdir(whispers_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(whispers_dir, filename)
            try:
                with open(file_path, "r") as f:
                    db = json.load(f)
                if secret_id in db:
                    data = db[secret_id]
                    user_list = data.get("userid", [])
                    sender_id = data.get("sender_id")
                    secret_text = data.get("text", "")
                    found = True
                    break
            except:
                continue

    if not found:
        await event.answer("الهمسة غير موجودة أو انتهت صلاحيتها.", alert=True)
        return

    # التحقق من الصلاحية
    allowed_ids = user_list + [sender_id, Config.OWNER_ID]
    if user_id not in allowed_ids:
        await event.answer("عذراً، هذه الهمسة ليست لك.", alert=True)
        return

    # عرض الهمسة
    await event.answer(secret_text, alert=True)

    # إذا كان الفاتح هو أحد المستلمين، نسجل القراءة
    if user_id in user_list:
        # تسجيل وقت القراءة
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M").lstrip("0")
        data["read"] = True
        data["read_time"] = current_time
        data["read_by"] = user_id
        with open(file_path, "w") as f:
            json.dump(db, f, indent=4)

        # تحديث الرسالة الأصلية (إذا كان البوت هو من أرسلها)
        try:
            # يمكنك إضافة كود لتعديل الرسالة وعرض من قرأها
            pass
        except:
            pass
