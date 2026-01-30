import json
import requests
from ...Config import Config
from ...core.logger import logging

LOGS = logging.getLogger("JoKeRUB")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "content-type": "application/json",
}


async def test_pasty(message, extension=None):
    """
    Test pasty.lus.pm service
    """
    LOGS.info("🧪 Testing Service 1: pasty.lus.pm")
    siteurl = "https://pasty.lus.pm/api/v1/pastes"
    data = {"content": message}
    
    try:
        LOGS.info(f"🌐 Sending request to: {siteurl}")
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers, timeout=10)
        LOGS.info(f"📊 Response Status: {response.status_code}")
        
        if response.ok:
            response_json = response.json()
            LOGS.info(f"✅ pasty.lus.pm SUCCESS! Key: {response_json.get('id', 'N/A')}")
            purl = (
                f"https://pasty.lus.pm/{response_json['id']}.{extension}"
                if extension
                else f"https://pasty.lus.pm/{response_json['id']}.txt"
            )
            return {
                "url": purl,
                "raw": f"https://pasty.lus.pm/{response_json['id']}/raw",
                "bin": "Pasty",
                "service": "pasty.lus.pm"
            }
        else:
            LOGS.error(f"❌ pasty.lus.pm FAILED: Status {response.status_code}")
            return {"error": f"HTTP {response.status_code}", "service": "pasty.lus.pm"}
            
    except json.JSONDecodeError as e:
        LOGS.error(f"❌ pasty.lus.pm JSON ERROR: {str(e)}")
        LOGS.error(f"Response text: {response.text[:200] if 'response' in locals() else 'No response'}")
        return {"error": f"JSON Error: {str(e)}", "service": "pasty.lus.pm"}
    except Exception as e:
        LOGS.error(f"❌ pasty.lus.pm CONNECTION ERROR: {str(e)}")
        return {"error": str(e), "service": "pasty.lus.pm"}


async def test_spacebin(message, extension="txt"):
    """
    Test spaceb.in service
    """
    LOGS.info("🧪 Testing Service 2: spaceb.in")
    siteurl = "https://spaceb.in/api/v1/documents/"
    
    try:
        LOGS.info(f"🌐 Sending request to: {siteurl}")
        response = requests.post(
            siteurl, 
            data={"content": message, "extension": extension},
            timeout=10
        )
        LOGS.info(f"📊 Response Status: {response.status_code}")
        
        if response.ok:
            response_json = response.json()
            LOGS.info(f"✅ spaceb.in SUCCESS! ID: {response_json.get('payload', {}).get('id', 'N/A')}")
            return {
                "url": f"https://spaceb.in/{response_json['payload']['id']}",
                "raw": f"{siteurl}{response_json['payload']['id']}/raw",
                "bin": "Spacebin",
                "service": "spaceb.in"
            }
        else:
            LOGS.error(f"❌ spaceb.in FAILED: Status {response.status_code}")
            return {"error": f"HTTP {response.status_code}", "service": "spaceb.in"}
            
    except json.JSONDecodeError as e:
        LOGS.error(f"❌ spaceb.in JSON ERROR: {str(e)}")
        LOGS.error(f"Response text: {response.text[:200] if 'response' in locals() else 'No response'}")
        return {"error": f"JSON Error: {str(e)}", "service": "spaceb.in"}
    except Exception as e:
        LOGS.error(f"❌ spaceb.in CONNECTION ERROR: {str(e)}")
        return {"error": str(e), "service": "spaceb.in"}


async def test_nekobin(message, extension=None):
    """
    Test nekobin.com service
    """
    LOGS.info("🧪 Testing Service 3: nekobin.com")
    siteurl = "https://nekobin.com/api/documents"
    data = {"content": message}
    
    try:
        LOGS.info(f"🌐 Sending request to: {siteurl}")
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers, timeout=10)
        LOGS.info(f"📊 Response Status: {response.status_code}")
        
        if response.ok:
            response_json = response.json()
            LOGS.info(f"✅ nekobin.com SUCCESS! Key: {response_json.get('result', {}).get('key', 'N/A')}")
            purl = (
                f"nekobin.com/{response_json['result']['key']}.{extension}"
                if extension
                else f"nekobin.com/{response_json['result']['key']}"
            )
            return {
                "url": purl,
                "raw": f"nekobin.com/raw/{response_json['result']['key']}",
                "bin": "Neko",
                "service": "nekobin.com"
            }
        else:
            LOGS.error(f"❌ nekobin.com FAILED: Status {response.status_code}")
            return {"error": f"HTTP {response.status_code}", "service": "nekobin.com"}
            
    except json.JSONDecodeError as e:
        LOGS.error(f"❌ nekobin.com JSON ERROR: {str(e)}")
        LOGS.error(f"Response text: {response.text[:200] if 'response' in locals() else 'No response'}")
        return {"error": f"JSON Error: {str(e)}", "service": "nekobin.com"}
    except Exception as e:
        LOGS.error(f"❌ nekobin.com CONNECTION ERROR: {str(e)}")
        return {"error": str(e), "service": "nekobin.com"}


async def test_deldog(message, extension=None):
    """
    Test del.dog service (the problematic one)
    """
    LOGS.info("🧪 Testing Service 4: del.dog")
    siteurl = "https://del.dog/documents"
    data = {"content": message}
    
    try:
        LOGS.info(f"🌐 Sending request to: {siteurl}")
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers, timeout=10)
        LOGS.info(f"📊 Response Status: {response.status_code}")
        
        if response.ok:
            response_json = response.json()
            LOGS.info(f"✅ del.dog SUCCESS! Key: {response_json.get('key', 'N/A')}")
            purl = (
                f"https://del.dog/{response_json['key']}.{extension}"
                if extension
                else f"https://del.dog/{response_json['key']}"
            )
            return {
                "url": purl,
                "raw": f"https://del.dog/raw/{response_json['key']}",
                "bin": "Dog",
                "service": "del.dog"
            }
        else:
            LOGS.error(f"❌ del.dog FAILED: Status {response.status_code}")
            LOGS.error(f"Response text: {response.text[:200]}")
            return {"error": f"HTTP {response.status_code}", "service": "del.dog"}
            
    except json.JSONDecodeError as e:
        LOGS.error(f"❌ del.dog JSON ERROR: {str(e)}")
        LOGS.error(f"Response text: {response.text[:500] if 'response' in locals() else 'No response'}")
        return {"error": f"JSON Error: {str(e)}", "service": "del.dog"}
    except Exception as e:
        LOGS.error(f"❌ del.dog CONNECTION ERROR: {str(e)}")
        return {"error": str(e), "service": "del.dog"}


async def p_paste(message, extension=None):
    """Alias for backward compatibility"""
    return await test_pasty(message, extension)


async def s_paste(message, extension="txt"):
    """Alias for backward compatibility"""
    return await test_spacebin(message, extension)


async def n_paste(message, extension=None):
    """Alias for backward compatibility"""
    return await test_nekobin(message, extension)


async def d_paste(message, extension=None):
    """Alias for backward compatibility"""
    return await test_deldog(message, extension)


async def pastetext(text_to_print, pastetype=None, extension=None):
    """
    📌 MAIN FUNCTION - Tests all services one by one
    This is the function that gets called from other parts of the code
    """
    LOGS.info("=" * 60)
    LOGS.info("🚀 STARTING PASTE SERVICE TEST")
    LOGS.info(f"📏 Content length: {len(text_to_print)} chars")
    LOGS.info(f"📁 Extension: {extension}")
    LOGS.info(f"🎯 Requested service type: {pastetype}")
    LOGS.info("=" * 60)
    
    # إذا طلب خدمة معينة، نجربها فقط
    if pastetype == "s":
        LOGS.info("🎯 User requested spaceb.in specifically")
        result = await test_spacebin(text_to_print, extension or "txt")
        
        if "error" not in result:
            LOGS.info(f"✅ SUCCESS with requested service: {result['service']}")
            return result
        else:
            LOGS.warning(f"⚠️ Requested service failed, trying others...")
    
    # نجرب الخدمات واحدة تلو الأخرى
    services_to_test = [
        ("pasty.lus.pm", test_pasty),
        ("spaceb.in", test_spacebin),
        ("nekobin.com", test_nekobin),
        ("del.dog", test_deldog),
    ]
    
    for service_name, service_func in services_to_test:
        LOGS.info(f"\n🔄 Testing {service_name}...")
        result = await service_func(text_to_print, extension)
        
        if "error" not in result:
            LOGS.info(f"🎉 SUCCESS! Using {service_name}")
            LOGS.info(f"🔗 URL: {result.get('url', 'N/A')}")
            return result
        else:
            LOGS.warning(f"⚠️ {service_name} failed: {result.get('error', 'Unknown error')}")
            continue
    
    # إذا فشلت جميع الخدمات
    LOGS.error("💥 ALL SERVICES FAILED!")
    return {
        "error": "جميع خدمات الرفع غير متاحة. جرب:\n1. pastebin.com\n2. controlc.com\n3. يدويًا في المحادثة",
        "url": "",
        "raw": "",
        "bin": "None",
        "service": "None"
        }
