import json
import requests
from ...Config import Config
from ...core.logger import logging

LOGS = logging.getLogger("JoKeRUB")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "content-type": "application/json",
}


async def s_paste(message, extension="txt"):
    """
    To Paste the given message/text/code to spaceb.in (الخدمة 2)
    """
    siteurl = "https://spaceb.in/api/v1/documents/"
    try:
        response = requests.post(
            siteurl, data={"content": message, "extension": extension}
        )
    except Exception as e:
        return {"error": str(e)}
    
    if response.ok:
        response = response.json()
        if response["error"] != "" and response["status"] < 400:
            return {"error": response["error"]}
        return {
            "url": f"https://spaceb.in/{response['payload']['id']}",
            "raw": f"{siteurl}{response['payload']['id']}/raw",
            "bin": "Spacebin",
        }
    return {"error": "Unable to reach spacebin."}


async def n_paste(message, extension=None):
    """
    To Paste the given message/text/code to nekobin (الخدمة 3)
    """
    siteurl = "https://nekobin.com/api/documents"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    
    if response.ok:
        response = response.json()
        purl = (
            f"nekobin.com/{response['result']['key']}.{extension}"
            if extension
            else f"nekobin.com/{response['result']['key']}"
        )
        return {
            "url": purl,
            "raw": f"nekobin.com/raw/{response['result']['key']}",
            "bin": "Neko",
        }
    return {"error": "Unable to reach nekobin."}


async def pastetext(text_to_print, pastetype=None, extension=None):
    """
    الدالة الرئيسية المعدلة للخدمات الشغالة فقط
    """
    response = {"error": "something went wrong"}
    
    # محاولة الخدمة المحددة أولاً
    if pastetype is not None:
        if pastetype == "s" and extension:
            response = await s_paste(text_to_print, extension)
        elif pastetype == "s":
            response = await s_paste(text_to_print)
        elif pastetype == "n":
            response = await n_paste(text_to_print, extension)
    
    # إذا لم يتم تحديد نوع أو فشلت الخدمة المحددة
    if "error" in response or pastetype is None:
        # محاولة Nekobin أولاً
        response = await n_paste(text_to_print, extension)
        
        # إذا فشل Nekobin، جرب Spacebin
        if "error" in response:
            if extension:
                response = await s_paste(text_to_print, extension)
            else:
                response = await s_paste(text_to_print)
    
    return response
