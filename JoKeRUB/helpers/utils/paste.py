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
    Test pasty.lus.pm service - HTTP ONLY VERSION
    """
    LOGS.info("🧪 Testing pasty.lus.pm (HTTP)")
    
    # استخدم HTTP فقط - لأن HTTPS معطل
    siteurl = "http://pasty.lus.pm/api/v1/pastes"
    data = {"content": message}
    
    try:
        LOGS.info(f"🌐 Sending HTTP request to: {siteurl}")
        response = requests.post(
            url=siteurl, 
            data=json.dumps(data), 
            headers=headers, 
            timeout=10
        )
        LOGS.info(f"📊 Response Status: {response.status_code}")
        
        if response.ok:
            try:
                response_json = response.json()
                LOGS.info(f"✅ pasty.lus.pm SUCCESS! Key: {response_json.get('id', 'N/A')}")
                
                # استخدم HTTP في الروابط أيضاً
                purl = (
                    f"http://pasty.lus.pm/{response_json['id']}.{extension}"
                    if extension
                    else f"http://pasty.lus.pm/{response_json['id']}.txt"
                )
                LOGS.info(f"🔗 Paste URL: {purl}")
                
                return {
                    "url": purl,
                    "raw": f"http://pasty.lus.pm/{response_json['id']}/raw",
                    "bin": "Pasty",
                    "service": "pasty.lus.pm"
                }
            except json.JSONDecodeError as e:
                LOGS.error(f"❌ JSON Error: {str(e)}")
                LOGS.error(f"Response: {response.text[:500]}")
                return {"error": f"JSON Error: {str(e)}", "service": "pasty.lus.pm"}
        else:
            LOGS.error(f"❌ HTTP {response.status_code}: {response.text[:200]}")
            return {"error": f"HTTP {response.status_code}", "service": "pasty.lus.pm"}
            
    except Exception as e:
        LOGS.error(f"❌ Connection Error: {str(e)}")
        return {"error": str(e), "service": "pasty.lus.pm"}


async def test_hastebin(message, extension=None):
    """
    Test hastebin.com - يعمل دائمًا تقريبًا
    """
    LOGS.info("🧪 Testing hastebin.com")
    siteurl = "https://hastebin.com/documents"
    
    try:
        response = requests.post(
            siteurl,
            data=message.encode('utf-8'),
            headers={"Content-Type": "text/plain"},
            timeout=10
        )
        
        if response.ok:
            try:
                response_json = response.json()
                key = response_json.get('key')
                if key:
                    haste_url = f"https://hastebin.com/{key}"
                    LOGS.info(f"✅ hastebin.com SUCCESS: {haste_url}")
                    return {
                        "url": haste_url,
                        "raw": f"https://hastebin.com/raw/{key}",
                        "bin": "Hastebin",
                        "service": "hastebin.com"
                    }
            except:
                LOGS.error("❌ hastebin.com: Invalid JSON response")
    
    except Exception as e:
        LOGS.error(f"❌ hastebin.com ERROR: {str(e)}")
    
    return {"error": "hastebin.com failed", "service": "hastebin.com"}


async def test_ixio(message, extension=None):
    """
    Test ix.io - خدمة بسيطة جدًا
    """
    LOGS.info("🧪 Testing ix.io")
    
    try:
        response = requests.post(
            "http://ix.io",
            data={"f:1": message},
            timeout=10
        )
        
        if response.ok:
            paste_url = response.text.strip()
            LOGS.info(f"✅ ix.io SUCCESS: {paste_url}")
            return {
                "url": paste_url,
                "raw": paste_url,
                "bin": "ix.io",
                "service": "ix.io"
            }
    
    except Exception as e:
        LOGS.error(f"❌ ix.io ERROR: {str(e)}")
    
    return {"error": "ix.io failed", "service": "ix.io"}


async def test_cl1p(message, extension=None):
    """
    Test cl1p.net - خدمة أخرى بسيطة
    """
    LOGS.info("🧪 Testing cl1p.net")
    
    try:
        # cl1p.net يحتاج معرف فريد لكل لصق
        import uuid
        clip_id = str(uuid.uuid4())[:8]
        
        response = requests.post(
            f"https://cl1p.net/{clip_id}",
            data={"content": message},
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            clip_url = f"https://cl1p.net/{clip_id}"
            LOGS.info(f"✅ cl1p.net SUCCESS: {clip_url}")
            return {
                "url": clip_url,
                "raw": clip_url,
                "bin": "cl1p.net",
                "service": "cl1p.net"
            }
    
    except Exception as e:
        LOGS.error(f"❌ cl1p.net ERROR: {str(e)}")
    
    return {"error": "cl1p.net failed", "service": "cl1p.net"}


async def test_teknik(message, extension=None):
    """
    Test teknik.io - خدمة حديثة
    """
    LOGS.info("🧪 Testing teknik.io")
    siteurl = "https://api.teknik.io/v1/Paste"
    
    try:
        response = requests.post(
            siteurl,
            json={
                "code": message,
                "title": "Paste",
                "language": "text",
                "expire": 1440  # 24 ساعة
            },
            headers=headers,
            timeout=10
        )
        
        if response.ok:
            try:
                response_json = response.json()
                if response_json.get('success'):
                    paste_url = f"https://paste.teknik.io/{response_json['result']['id']}"
                    LOGS.info(f"✅ teknik.io SUCCESS: {paste_url}")
                    return {
                        "url": paste_url,
                        "raw": f"https://paste.teknik.io/{response_json['result']['id']}/raw",
                        "bin": "Teknik",
                        "service": "teknik.io"
                    }
            except:
                LOGS.error("❌ teknik.io: Invalid response")
    
    except Exception as e:
        LOGS.error(f"❌ teknik.io ERROR: {str(e)}")
    
    return {"error": "teknik.io failed", "service": "teknik.io"}


async def test_rentry(message, extension=None):
    """
    Test rentry.co - يعمل بشكل ممتاز
    """
    LOGS.info("🧪 Testing rentry.co")
    
    try:
        import secrets
        import string
        
        # إنشاء معرف عشوائي
        alphabet = string.ascii_lowercase + string.digits
        url_id = ''.join(secrets.choice(alphabet) for _ in range(5))
        
        response = requests.post(
            "https://rentry.co/api/new",
            json={
                "text": message,
                "edit_code": "0000",  # كود تحرير بسيط
                "url": url_id
            },
            timeout=10
        )
        
        if response.ok:
            try:
                response_json = response.json()
                if response_json.get('url'):
                    paste_url = response_json['url']
                    LOGS.info(f"✅ rentry.co SUCCESS: {paste_url}")
                    return {
                        "url": paste_url,
                        "raw": paste_url + "/raw",
                        "bin": "Rentry",
                        "service": "rentry.co"
                    }
            except:
                LOGS.error("❌ rentry.co: Invalid response")
    
    except Exception as e:
        LOGS.error(f"❌ rentry.co ERROR: {str(e)}")
    
    return {"error": "rentry.co failed", "service": "rentry.co"}


# الدوال القديمة للحفاظ على التوافق
async def p_paste(message, extension=None):
    return await test_pasty(message, extension)

async def s_paste(message, extension="txt"):
    LOGS.warning("⚠️ spaceb.in disabled due to 415 error")
    return {"error": "spaceb.in disabled", "service": "spaceb.in"}

async def n_paste(message, extension=None):
    LOGS.warning("⚠️ nekobin.com disabled due to 400 error")
    return {"error": "nekobin.com disabled", "service": "nekobin.com"}

async def d_paste(message, extension=None):
    LOGS.warning("⚠️ del.dog disabled due to JSON error")
    return {"error": "del.dog disabled", "service": "del.dog"}


async def pastetext(text_to_print, pastetype=None, extension=None):
    """
    🎯 MAIN FUNCTION - مع خدمات موثوقة تعمل فعلاً
    """
    LOGS.info("=" * 60)
    LOGS.info("🚀 STARTING PASTE WITH WORKING SERVICES")
    LOGS.info(f"📏 Content length: {len(text_to_print)} chars")
    LOGS.info("=" * 60)
    
    # إذا طلب pasty.lus.pm تحديداً
    if pastetype == "p":
        LOGS.info("🎯 User requested pasty.lus.pm")
        result = await test_pasty(text_to_print, extension)
        if "error" not in result:
            return result
    
    # ترتيب الخدمات - الأكثر موثوقية أولاً
    services_to_test = [
        ("rentry.co", test_rentry),          # 👍 الأفضل - يعمل دائمًا
        ("hastebin.com", test_hastebin),     # 👍 جيد جدًا
        ("pasty.lus.pm (HTTP)", test_pasty), # 👎 HTTP فقط
        ("ix.io", test_ixio),               # 👍 بسيط ويعمل
        ("teknik.io", test_teknik),         # 👍 حديث
        ("cl1p.net", test_cl1p),            # 👍 احتياطي
    ]
    
    success_count = 0
    for service_name, service_func in services_to_test:
        LOGS.info(f"\n🔧 [{success_count + 1}] Testing: {service_name}")
        result = await service_func(text_to_print, extension)
        
        if "error" not in result:
            LOGS.info(f"✅ [{success_count + 1}] SUCCESS! Using {service_name}")
            LOGS.info(f"🔗 URL: {result.get('url', 'N/A')}")
            return result
        else:
            LOGS.warning(f"❌ [{success_count + 1}] {service_name} failed")
            success_count += 1
    
    # إذا فشلت جميع الخدمات
    LOGS.error("💥 ALL SERVICES FAILED!")
    return {
        "error": (
            "⚠️ جميع خدمات الرفع غير متاحة حاليًا.\n\n"
            "✅ الحلول:\n"
            "1. استخدم خدمة خارجية:\n"
            "   • https://pastebin.com\n"
            "   • https://controlc.com\n"
            "   • https://rentry.co\n"
            "2. قسم النص إلى أجزاء\n"
            "3. أرسل كملف txt"
        ),
        "url": "",
        "raw": "",
        "bin": "None",
        "service": "None"
    }
