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
    To Paste the given message/text/code to paste.pelkum.dev
    """
    siteurl = "https://pasty.lus.pm/api/v1/pastes"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    
    if response.ok:
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            LOGS.error(f"Pasty.lus.pm response is not JSON: {response.text[:200]}")
            return {"error": "Invalid response from pasty.lus.pm"}
        
        purl = (
            f"https://pasty.lus.pm/{response_json['id']}.{extension}"
            if extension
            else f"https://pasty.lus.pm/{response_json['id']}.txt"
        )
        try:
            from ...core.session import l313l

            await l313l.send_message(
                Config.BOTLOG_CHATID,
                f"**You have created a new paste in pasty bin.** Link to pasty is [here]({purl}). You can delete that paste by using this token `{response_json['deletionToken']}`",
            )
        except Exception as e:
            LOGS.info(str(e))
        return {
            "url": purl,
            "raw": f"https://pasty.lus.pm/{response_json['id']}/raw",
            "bin": "Pasty",
        }
    return {"error": f"Unable to reach pasty.lus.pm. Status: {response.status_code}"}


async def s_paste(message, extension="txt"):
    """
    To Paste the given message/text/code to spaceb.in
    """
    siteurl = "https://spaceb.in/api/v1/documents/"
    try:
        response = requests.post(
            siteurl, data={"content": message, "extension": extension}
        )
    except Exception as e:
        return {"error": str(e)}
    
    if response.ok:
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            LOGS.error(f"Spacebin response is not JSON: {response.text[:200]}")
            return {"error": "Invalid response from spaceb.in"}
        
        if response_json["error"] != "" and response_json["status"] < 400:
            return {"error": response_json["error"]}
        return {
            "url": f"https://spaceb.in/{response_json['payload']['id']}",
            "raw": f"{siteurl}{response_json['payload']['id']}/raw",
            "bin": "Spacebin",
        }
    return {"error": f"Unable to reach spacebin. Status: {response.status_code}"}


async def n_paste(message, extension=None):
    """
    To Paste the given message/text/code to nekobin
    """
    siteurl = "https://nekobin.com/api/documents"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    
    if response.ok:
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            LOGS.error(f"Nekobin response is not JSON: {response.text[:200]}")
            return {"error": "Invalid response from nekobin"}
        
        purl = (
            f"nekobin.com/{response_json['result']['key']}.{extension}"
            if extension
            else f"nekobin.com/{response_json['result']['key']}"
        )
        return {
            "url": purl,
            "raw": f"nekobin.com/raw/{response_json['result']['key']}",
            "bin": "Neko",
        }
    return {"error": f"Unable to reach nekobin. Status: {response.status_code}"}


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
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            # إذا فشل تحويل JSON، طباعة الاستجابة للتصحيح
            LOGS.error(f"Del.dog response is not JSON: {response.text[:200]}")
            return {"error": "Invalid response from del.dog"}
        
        purl = (
            f"https://del.dog/{response_json['key']}.{extension}"
            if extension
            else f"https://del.dog/{response_json['key']}"
        )
        return {
            "url": purl,
            "raw": f"https://del.dog/raw/{response_json['key']}",
            "bin": "Dog",
        }
    return {"error": f"Unable to reach dogbin. Status: {response.status_code}"}


async def pastetext(text_to_print, pastetype=None, extension=None):
    """
    Main paste function that tries multiple paste services
    """
    LOGS.debug(f"Attempting paste with type: {pastetype}, extension: {extension}")
    response = {"error": "something went wrong"}
    
    if pastetype is not None:
        if pastetype == "p":
            response = await p_paste(text_to_print, extension)
            LOGS.debug(f"Pasty.lus.pm result: {'Success' if 'error' not in response else 'Failed'}")
        elif pastetype == "s" and extension:
            response = await s_paste(text_to_print, extension)
            LOGS.debug(f"Spacebin result: {'Success' if 'error' not in response else 'Failed'}")
        elif pastetype == "s":
            response = await s_paste(text_to_print)
            LOGS.debug(f"Spacebin result: {'Success' if 'error' not in response else 'Failed'}")
        elif pastetype == "n":  # جعل Nekobin قبل Dogbin
            response = await n_paste(text_to_print, extension)
            LOGS.debug(f"Nekobin result: {'Success' if 'error' not in response else 'Failed'}")
        elif pastetype == "d":
            response = await d_paste(text_to_print, extension)
            LOGS.debug(f"Del.dog result: {'Success' if 'error' not in response else 'Failed'}")
    
    # سجل الاستجابة لمعرفة أي خدمة تعمل
    if "bin" in response:
        LOGS.debug(f"Paste successful with: {response['bin']}")
    else:
        LOGS.debug(f"Paste failed: {response.get('error', 'Unknown error')}")
    
    # المحاولة مع خدمات احتياطية إذا فشلت الخدمة المطلوبة
    if "error" in response:
        LOGS.debug("Trying backup services...")
        response = await p_paste(text_to_print, extension)
        LOGS.debug(f"Backup 1 (Pasty): {'Success' if 'error' not in response else 'Failed'}")
    
    if "error" in response:
        response = await n_paste(text_to_print, extension)  # Nekobin قبل Dogbin
        LOGS.debug(f"Backup 2 (Nekobin): {'Success' if 'error' not in response else 'Failed'}")
    
    if "error" in response:
        response = await d_paste(text_to_print, extension)  # Dogbin في النهاية
        LOGS.debug(f"Backup 3 (Del.dog): {'Success' if 'error' not in response else 'Failed'}")
    
    if "error" in response:
        if extension:
            response = await s_paste(text_to_print, extension)
        else:
            response = await s_paste(text_to_print)
        LOGS.debug(f"Backup 4 (Spacebin): {'Success' if 'error' not in response else 'Failed'}")
    
    # إذا فشلت جميع الخدمات
    if "error" in response:
        LOGS.error(f"All paste services failed. Last error: {response['error']}")
        return {
            "error": "All paste services are currently unavailable. Please try again later.",
            "url": "",
            "raw": "",
            "bin": "None"
        }
    
    return response
