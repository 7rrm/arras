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
        LOGS.error(f"Spacebin error: {e}")
        return {"error": str(e)}
    
    if response.ok:
        try:
            response_data = response.json()
            if response_data.get("error", "") != "" and response_data.get("status", 0) < 400:
                return {"error": response_data["error"]}
            return {
                "url": f"https://spaceb.in/{response_data['payload']['id']}",
                "raw": f"https://spaceb.in/api/v1/documents/{response_data['payload']['id']}/raw",
                "bin": "Spacebin",
                "id": response_data['payload']['id']
            }
        except json.JSONDecodeError as e:
            LOGS.error(f"Spacebin JSON decode error: {e}")
            return {"error": f"Invalid response from Spacebin: {response.status_code}"}
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
        LOGS.error(f"Pasty error: {e}")
        return {"error": str(e)}
    
    if response.ok:
        try:
            response_data = response.json()
            purl = (
                f"https://pasty.lus.pm/{response_data['id']}.{extension}"
                if extension
                else f"https://pasty.lus.pm/{response_data['id']}.txt"
            )
            try:
                from ...core.session import l313l
                await l313l.send_message(
                    Config.BOTLOG_CHATID,
                    f"**You have created a new paste in pasty bin.** Link to pasty is [here]({purl}). You can delete that paste by using this token `{response_data['deletionToken']}`",
                )
            except Exception as e:
                LOGS.info(f"Failed to send botlog: {e}")
            return {
                "url": purl,
                "raw": f"https://pasty.lus.pm/{response_data['id']}/raw",
                "bin": "Pasty",
            }
        except json.JSONDecodeError as e:
            LOGS.error(f"Pasty JSON decode error: {e}")
            return {"error": f"Invalid response from Pasty: {response.status_code}"}
    return {"error": f"Unable to reach pasty.lus.pm. Status: {response.status_code}"}


async def n_paste(message, extension=None):
    """
    To Paste the given message/text/code to nekobin
    """
    siteurl = "https://nekobin.com/api/documents"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers, timeout=10)
    except Exception as e:
        LOGS.error(f"Nekobin error: {e}")
        return {"error": str(e)}
    
    if response.ok:
        try:
            response_data = response.json()
            purl = (
                f"https://nekobin.com/{response_data['result']['key']}.{extension}"
                if extension
                else f"https://nekobin.com/{response_data['result']['key']}"
            )
            return {
                "url": purl,
                "raw": f"https://nekobin.com/raw/{response_data['result']['key']}",
                "bin": "Neko",
            }
        except json.JSONDecodeError as e:
            LOGS.error(f"Nekobin JSON decode error: {e}")
            return {"error": f"Invalid response from Nekobin: {response.status_code}"}
    return {"error": f"Unable to reach nekobin.com. Status: {response.status_code}"}


async def pastetext(text_to_print, pastetype=None, extension=None):
    """
    Main function to paste text with Spacebin as primary service
    (Dogbin service has been removed due to errors)
    """
    response = {"error": "not tried yet"}
    
    # إذا تم تحديد نوع معين، استخدمه
    if pastetype is not None:
        if pastetype == "s" and extension:
            response = await s_paste(text_to_print, extension)
        elif pastetype == "s":
            response = await s_paste(text_to_print)
        elif pastetype == "p":
            response = await p_paste(text_to_print, extension)
        elif pastetype == "n":
            response = await n_paste(text_to_print, extension)
        # تمت إزالة 'd' لأن Dogbin تم حذفه
    
    # إذا لم يتم تحديد نوع أو فشل النوع المحدد، جرب بالترتيب الجديد:
    if "error" in response:
        LOGS.info("Trying Spacebin (primary)...")
        if extension:
            response = await s_paste(text_to_print, extension)
        else:
            response = await s_paste(text_to_print)
    
    if "error" in response:
        LOGS.info("Spacebin failed, trying Nekobin...")
        response = await n_paste(text_to_print, extension)
    
    if "error" in response:
        LOGS.info("Nekobin failed, trying Pasty...")
        response = await p_paste(text_to_print, extension)
    
    # تمت إزالة Dogbin من الترتيب
    
    return response
