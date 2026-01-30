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
    To Paste the given message/text/code to spaceb.in (PRIMARY SERVICE)
    """
    siteurl = "https://spaceb.in/api/v1/documents/"
    try:
        response = requests.post(
            siteurl, 
            data={"content": message, "extension": extension},
            timeout=10
        )
    except Exception as e:
        return {"error": str(e)}
    
    if response.ok:
        response = response.json()
        if response["error"] != "" and response["status"] < 400:
            return {"error": response["error"]}
        return {
            "url": f"https://spaceb.in/{response['payload']['id']}",
            "raw": f"https://spaceb.in/api/v1/documents/{response['payload']['id']}/raw",
            "bin": "Spacebin",
            "id": response['payload']['id']
        }
    return {"error": f"Unable to reach spacebin. Status: {response.status_code}"}


async def p_paste(message, extension=None):
    """
    To Paste the given message/text/code to paste.pelkum.dev
    """
    siteurl = "https://pasty.lus.pm/api/v1/pastes"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers, timeout=10)
    except Exception as e:
        return {"error": str(e)}
    
    if response.ok:
        response = response.json()
        purl = (
            f"https://pasty.lus.pm/{response['id']}.{extension}"
            if extension
            else f"https://pasty.lus.pm/{response['id']}.txt"
        )
        try:
            from ...core.session import l313l
            await l313l.send_message(
                Config.BOTLOG_CHATID,
                f"**You have created a new paste in pasty bin.** Link to pasty is [here]({purl}). You can delete that paste by using this token `{response['deletionToken']}`",
            )
        except Exception as e:
            LOGS.info(str(e))
        return {
            "url": purl,
            "raw": f"https://pasty.lus.pm/{response['id']}/raw",
            "bin": "Pasty",
        }
    return {"error": "Unable to reach pasty.lus.pm"}


async def n_paste(message, extension=None):
    """
    To Paste the given message/text/code to nekobin
    """
    siteurl = "https://nekobin.com/api/documents"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers, timeout=10)
    except Exception as e:
        return {"error": str(e)}
    
    if response.ok:
        response = response.json()
        purl = (
            f"https://nekobin.com/{response['result']['key']}.{extension}"
            if extension
            else f"https://nekobin.com/{response['result']['key']}"
        )
        return {
            "url": purl,
            "raw": f"https://nekobin.com/raw/{response['result']['key']}",
            "bin": "Neko",
        }
    return {"error": "Unable to reach nekobin."}


async def d_paste(message, extension=None):
    """
    To Paste the given message/text/code to dogbin
    """
    siteurl = "https://del.dog/documents"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers, timeout=10)
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


async def pastetext(text_to_print, pastetype=None, extension=None):
    """
    Main function to paste text with Spacebin as primary service
    """
    response = {"error": "something went wrong"}
    
    # إذا تم تحديد نوع معين، استخدمه
    if pastetype is not None:
        if pastetype == "s" and extension:
            response = await s_paste(text_to_print, extension)
        elif pastetype == "s":
            response = await s_paste(text_to_print)
        elif pastetype == "p":
            response = await p_paste(text_to_print, extension)
        elif pastetype == "d":
            response = await d_paste(text_to_print, extension)
        elif pastetype == "n":
            response = await n_paste(text_to_print, extension)
    
    # إذا لم يتم تحديد نوع أو فشل النوع المحدد، جرب بالترتيب:
    if "error" in response:
        # المحاولة الأولى: Spacebin (الخدمة الأساسية)
        if extension:
            response = await s_paste(text_to_print, extension)
        else:
            response = await s_paste(text_to_print)
    
    if "error" in response:
        # المحاولة الثانية: Nekobin
        response = await n_paste(text_to_print, extension)
    
    if "error" in response:
        # المحاولة الثالثة: Pasty
        response = await p_paste(text_to_print, extension)
    
    if "error" in response:
        # المحاولة الرابعة: Dogbin
        response = await d_paste(text_to_print, extension)
    
    return response
