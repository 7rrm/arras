import json
import requests
from ...Config import Config
from ...core.logger import logging

LOGS = logging.getLogger("JoKeRUB")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "content-type": "application/json",
}

async def p_paste(message, extension=None):
    """
    لصق النص/الكود على pasty.lus.pm
    """
    siteurl = "https://pasty.lus.pm/api/v1/pastes"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    
    if response.ok:
        response = response.json()
        purl = (
            f"https://pasty.lus.pm/{response['id']}.{extension}"
            if extension
            else f"https://pasty.lus.pm/{response['id']}.txt"
        )
        
        # إرسال إشعار للبوت لوج (اختياري)
        try:
            from ...core.session import l313l
            await l313l.send_message(
                Config.BOTLOG_CHATID,
                f"**تم إنشاء رابط مشاركة نص.**\n"
                f"🔗 الرابط: [اضغط هنا]({purl})\n"
                f"🗑️ رمز الحذف: `{response['deletionToken']}`"
            )
        except Exception as e:
            LOGS.info(str(e))
        
        return {
            "url": purl,
            "raw": f"https://pasty.lus.pm/{response['id']}/raw",
            "bin": "Pasty",
        }
    
    return {"error": "تعذر الوصول إلى pasty.lus.pm"}

# الدالة الرئيسية المعدلة
async def pastetext(text_to_print, extension=None):
    """
    لصق النص على Pasty فقط
    """
    return await p_paste(text_to_print, extension)
