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
    To Paste the given message/text/code to nekobin
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


async def dpaste_io(message, extension=None):
    """
    Alternative paste service using dpaste.org
    """
    siteurl = "https://dpaste.org/api/"
    data = {"content": message, "syntax": "text"}
    try:
        response = requests.post(url=siteurl, data=data, timeout=10)
    except Exception as e:
        return {"error": str(e)}
    
    if response.ok:
        # dpaste.org returns plain text URL
        paste_url = response.text.strip()
        return {
            "url": paste_url,
            "raw": paste_url + ".txt",
            "bin": "dpaste",
        }
    return {"error": f"Unable to reach dpaste.org. Status: {response.status_code}"}


async def pastetext(text_to_print, pastetype=None, extension=None):
    response = {"error": "something went wrong"}
    
    # قائمة بالمواقع بالمحاولة
    paste_functions = [
        (p_paste, "p"),
        (n_paste, "n"),
        (s_paste, "s"),
        (dpaste_io, "dpaste"),  # أضف البديل الجديد
    ]
    
    if pastetype is not None:
        # محاولة الموقع المحدد أولاً
        if pastetype == "p":
            response = await p_paste(text_to_print, extension)
        elif pastetype == "s" and extension:
            response = await s_paste(text_to_print, extension)
        elif pastetype == "s":
            response = await s_paste(text_to_print)
        elif pastetype == "d":
            # تجربة dpaste كبديل لـ del.dog
            response = await dpaste_io(text_to_print, extension)
        elif pastetype == "n":
            response = await n_paste(text_to_print, extension)
    
    # إذا فشل الموقع المحدد، جرب الباقي
    if "error" in response:
        for paste_func, _ in paste_functions:
            try:
                if paste_func == s_paste and extension:
                    response = await paste_func(text_to_print, extension)
                else:
                    response = await paste_func(text_to_print)
                if "error" not in response:
                    break
            except:
                continue
    
    return response
