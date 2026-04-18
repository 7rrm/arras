import json
import requests
import os

from ...Config import Config
from ...core.logger import logging

LOGS = logging.getLogger("JoKeRUB")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "content-type": "application/json",
}


async def d_paste(message, extension=None):
    """
    To Paste the given message/text/code to dogbin
    """
    siteurl = "https://del.dog/documents"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        purl = (
            f"https://del.dog/{response['key']}.{extension}"
            if extension
            else f"https://del.dog/{response['key']}"
        )
        return {
            "url": purl,
            "raw": f"https://del.dog/raw/{response['key']}",
            "bin": "Dog",
        }
    return {"error": "Unable to reach dogbin."}


async def pastetext(text_to_print, extension=None):
    """
    محاولة النشر على Dogbin فقط، في حال الفشل يستخدم الملف المحلي
    """
    # محاولة Dogbin أولاً
    response = await d_paste(text_to_print, extension)
    
    if "error" not in response:
        return response
    
    # إذا فشل Dogbin، نستخدم طريقة الملف المحلي
    timestamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paste_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text_to_print)
        
        return {
            "url": filename,
            "raw": filename,
            "bin": "LocalFile",
            "is_file": True
        }
    except Exception as e:
        return {"error": f"File save failed: {str(e)}"}
