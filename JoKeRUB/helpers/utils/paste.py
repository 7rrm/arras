import json
import requests
import os
from datetime import datetime

from ...Config import Config
from ...core.logger import logging

LOGS = logging.getLogger("JoKeRUB")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
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


async def save_to_local_file(message, extension=None):
    """
    حفظ النص كملف محلي (احتياطي عند فشل الخدمات)
    """
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"Source_aRaS_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(message)
        
        return {
            "url": filename,
            "raw": filename,
            "bin": "LocalFile",
            "is_file": True,
            "filename": filename
        }
    except Exception as e:
        return {"error": f"File save failed: {str(e)}"}


async def pastetext(text_to_print, pastetype=None, extension=None):
    """
    النشر على Dogbin أولاً، في حال الفشل يحفظ كملف محلي
    - pastetype: يتم تجاهله (نستخدم Dogbin فقط)
    - extension: امتداد الملف مثل txt, py, json
    """
    # محاولة Dogbin أولاً
    response = await d_paste(text_to_print, extension)
    
    if "error" not in response:
        return response
    
    # إذا فشل Dogbin → حفظ كملف محلي
    LOGS.info(f"Dogbin failed: {response['error']}, switching to local file")
    return await save_to_local_file(text_to_print, extension)
