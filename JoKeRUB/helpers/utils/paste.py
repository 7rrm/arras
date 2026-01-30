import json
import requests
from ...Config import Config
from ...core.logger import logging

LOGS = logging.getLogger("JoKeRUB")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


async def s_paste(message, extension="txt"):
    """
    Primary Service: Paste to spaceb.in (Most Reliable)
    """
    siteurl = "https://spaceb.in/api/v1/documents/"
    try:
        response = requests.post(
            siteurl, 
            data={"content": message, "extension": extension},
            headers=headers,
            timeout=15,
            verify=True
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        LOGS.error(f"Spacebin request error: {e}")
        return {"error": f"Spacebin request failed: {str(e)}"}
    except Exception as e:
        LOGS.error(f"Spacebin unexpected error: {e}")
        return {"error": str(e)}
    
    try:
        response_data = response.json()
        if response_data.get("error", "") != "":
            error_msg = response_data.get("error", "Unknown error")
            LOGS.error(f"Spacebin API error: {error_msg}")
            return {"error": f"Spacebin API: {error_msg}"}
        
        paste_id = response_data['payload']['id']
        LOGS.info(f"Spacebin paste created successfully: {paste_id}")
        return {
            "url": f"https://spaceb.in/{paste_id}",
            "raw": f"https://spaceb.in/api/v1/documents/{paste_id}/raw",
            "bin": "Spacebin",
            "id": paste_id
        }
    except json.JSONDecodeError as e:
        LOGS.error(f"Spacebin JSON decode error: {e}")
        return {"error": "Invalid JSON response from Spacebin"}
    except KeyError as e:
        LOGS.error(f"Spacebin response missing key {e}: {response.text[:200]}")
        return {"error": "Unexpected response format from Spacebin"}


async def n_paste(message, extension=None):
    """
    Backup Service: Paste to nekobin.com
    """
    siteurl = "https://nekobin.com/api/documents"
    data = {"content": message}
    
    try:
        response = requests.post(
            url=siteurl, 
            data=json.dumps(data), 
            headers=headers, 
            timeout=15,
            verify=True
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        LOGS.error(f"Nekobin request error: {e}")
        return {"error": f"Nekobin request failed: {str(e)}"}
    except Exception as e:
        LOGS.error(f"Nekobin unexpected error: {e}")
        return {"error": str(e)}
    
    try:
        response_data = response.json()
        key = response_data['result']['key']
        purl = f"https://nekobin.com/{key}"
        if extension:
            purl += f".{extension}"
        
        LOGS.info(f"Nekobin paste created successfully: {key}")
        return {
            "url": purl,
            "raw": f"https://nekobin.com/raw/{key}",
            "bin": "Nekobin",
            "key": key
        }
    except json.JSONDecodeError as e:
        LOGS.error(f"Nekobin JSON decode error: {e}")
        return {"error": "Invalid JSON response from Nekobin"}
    except KeyError as e:
        LOGS.error(f"Nekobin response missing key {e}: {response.text[:200]}")
        return {"error": "Unexpected response format from Nekobin"}


async def h_paste(message, extension=None):
    """
    Alternative Service: Paste to hastebin.com (Fast & Reliable)
    """
    siteurl = "https://hastebin.com/documents"
    
    haste_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "text/plain",
    }
    
    try:
        response = requests.post(
            url=siteurl, 
            data=message.encode('utf-8'), 
            headers=haste_headers, 
            timeout=15,
            verify=True
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        LOGS.error(f"Hastebin request error: {e}")
        return {"error": f"Hastebin request failed: {str(e)}"}
    except Exception as e:
        LOGS.error(f"Hastebin unexpected error: {e}")
        return {"error": str(e)}
    
    try:
        response_data = response.json()
        key = response_data['key']
        purl = f"https://hastebin.com/{key}"
        if extension and extension != "txt":
            purl += f".{extension}"
        
        LOGS.info(f"Hastebin paste created successfully: {key}")
        return {
            "url": purl,
            "raw": f"https://hastebin.com/raw/{key}",
            "bin": "Hastebin",
            "key": key
        }
    except json.JSONDecodeError as e:
        LOGS.error(f"Hastebin JSON decode error: {e}")
        return {"error": "Invalid JSON response from Hastebin"}
    except KeyError as e:
        LOGS.error(f"Hastebin response missing key {e}: {response.text[:200]}")
        return {"error": "Unexpected response format from Hastebin"}


async def r_paste(message, extension="txt"):
    """
    Secondary Alternative: Paste to rentry.co (Simple & Clean)
    """
    siteurl = "https://rentry.co/api/new"
    data = {
        "text": message,
        "edit_code": "123456"  # كود تحرير افتراضي
    }
    
    rentry_headers = headers.copy()
    rentry_headers.update({
        "Referer": "https://rentry.co/",
    })
    
    try:
        response = requests.post(
            url=siteurl, 
            data=json.dumps(data), 
            headers=rentry_headers, 
            timeout=15,
            verify=True
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        LOGS.error(f"Rentry request error: {e}")
        return {"error": f"Rentry request failed: {str(e)}"}
    except Exception as e:
        LOGS.error(f"Rentry unexpected error: {e}")
        return {"error": str(e)}
    
    try:
        response_data = response.json()
        if "url" in response_data:
            url = response_data['url']
            LOGS.info(f"Rentry paste created successfully: {url}")
            return {
                "url": url,
                "raw": f"{url}/raw",
                "bin": "Rentry",
                "edit_code": data["edit_code"]
            }
        else:
            LOGS.error(f"Rentry no URL in response: {response_data}")
            return {"error": "No URL received from Rentry"}
    except json.JSONDecodeError as e:
        LOGS.error(f"Rentry JSON decode error: {e}")
        return {"error": "Invalid JSON response from Rentry"}


async def pastetext(text_to_print, pastetype=None, extension=None):
    """
    Main function to paste text with multiple reliable services
    Order: Spacebin → Nekobin → Hastebin → Rentry
    """
    
    # إذا طلب خدمة معينة
    if pastetype is not None:
        if pastetype == "s":  # Spacebin
            LOGS.info(f"User requested Spacebin paste")
            if extension:
                return await s_paste(text_to_print, extension)
            return await s_paste(text_to_print)
        
        elif pastetype == "n":  # Nekobin
            LOGS.info(f"User requested Nekobin paste")
            return await n_paste(text_to_print, extension)
        
        elif pastetype == "h":  # Hastebin
            LOGS.info(f"User requested Hastebin paste")
            return await h_paste(text_to_print, extension)
        
        elif pastetype == "r":  # Rentry
            LOGS.info(f"User requested Rentry paste")
            return await r_paste(text_to_print, extension or "txt")
    
    # AUTO MODE: Try services in order of reliability
    ext = extension or "txt"
    
    # 1. Try Spacebin first (most reliable for code)
    LOGS.info("Auto-paste: Trying Spacebin (1st choice)...")
    response = await s_paste(text_to_print, ext)
    if "error" not in response:
        LOGS.info(f"✓ Success with Spacebin: {response.get('id', 'N/A')}")
        return response
    
    # 2. Try Nekobin second
    LOGS.info("Auto-paste: Spacebin failed, trying Nekobin (2nd choice)...")
    response = await n_paste(text_to_print, extension)
    if "error" not in response:
        LOGS.info(f"✓ Success with Nekobin: {response.get('key', 'N/A')}")
        return response
    
    # 3. Try Hastebin third (fast and simple)
    LOGS.info("Auto-paste: Nekobin failed, trying Hastebin (3rd choice)...")
    response = await h_paste(text_to_print, extension)
    if "error" not in response:
        LOGS.info(f"✓ Success with Hastebin: {response.get('key', 'N/A')}")
        return response
    
    # 4. Try Rentry as last resort
    LOGS.info("Auto-paste: Hastebin failed, trying Rentry (4th choice)...")
    response = await r_paste(text_to_print, ext)
    if "error" not in response:
        LOGS.info(f"✓ Success with Rentry: {response.get('url', 'N/A')}")
        return response
    
    # All services failed
    LOGS.error("✗ All paste services failed!")
    error_summary = "All paste services are currently unavailable. Please try:\n"
    error_summary += "1. Check your internet connection\n"
    error_summary += "2. Try again in a few minutes\n"
    error_summary += "3. The paste services might be temporarily down"
    
    return {"error": error_summary}


async def paste_message(text, pastetype=None, extension=None):
    """
    Wrapper function for backward compatibility
    """
    try:
        result = await pastetext(text, pastetype, extension)
        
        if "error" in result:
            LOGS.error(f"Paste failed: {result['error']}")
            return f"Error: {result['error']}"
        
        bin_name = result.get("bin", "Paste")
        url = result.get("url", "")
        raw_url = result.get("raw", "")
        
        # Format the response message
        message = f"**{bin_name} Link:** {url}\n"
        message += f"**Raw Link:** {raw_url}"
        
        # Add extra info if available
        if "id" in result:
            message += f"\n**Paste ID:** `{result['id']}`"
        elif "key" in result:
            message += f"\n**Paste Key:** `{result['key']}`"
        
        return message
        
    except Exception as e:
        LOGS.error(f"Unexpected error in paste_message: {e}")
        return f"Unexpected error: {str(e)}"
