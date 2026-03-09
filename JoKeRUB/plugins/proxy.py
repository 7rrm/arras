import requests
from bs4 import BeautifulSoup
import time
import os
import re
from JoKeRUB import l313l

plugin_category = "الادوات"

# ---- البحث عن بروكسيات ----
def fetch_proxies():
    url = 'https://t.me/s/ProxyMTProto'
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        proxies = []
        for message in soup.find_all('a', href=True):
            href = message['href']
            # استخراج روابط البروكسيات الحقيقية فقط
            if href.startswith(('https://t.me/proxy', 'tg://proxy')):
                proxies.append(href)
        
        return proxies
    except Exception as e:
        print(f"Error fetching proxies: {e}")
        return []

def extract_server_from_proxy(proxy_url):
    """استخراج عنوان السيرفر من رابط البروكسي"""
    try:
        # البحث عن parameter server في الرابط
        if 'server=' in proxy_url:
            server_match = re.search(r'server=([^&]+)', proxy_url)
            if server_match:
                return server_match.group(1)
        return None
    except:
        return None

def get_ping(proxy_url):
    """قياس سرعة الاتصال بالبروكسي"""
    try:
        # استخراج عنوان السيرفر
        server = extract_server_from_proxy(proxy_url)
        if not server:
            return None
        
        # تنفيذ أمر ping
        startupinfo = None
        if os.name == 'nt':  # ويندوز
            response = os.system(f"ping -n 1 -w 2000 {server} > nul 2>&1")
            if response == 0:
                # قياس الوقت في ويندوز
                result = os.popen(f"ping -n 1 {server}").read()
                match = re.search(r'time[=<](\d+)ms', result, re.IGNORECASE)
                if match:
                    return int(match.group(1))
        else:  # لينكس
            response = os.system(f"ping -c 1 -W 2 {server} > /dev/null 2>&1")
            if response == 0:
                # قياس الوقت في لينكس
                result = os.popen(f"ping -c 1 {server}").read()
                match = re.search(r'time[=<](\d+(?:\.\d+)?)\s*ms', result, re.IGNORECASE)
                if match:
                    return int(float(match.group(1)))
        
        return None
    except Exception as e:
        print(f"Error in ping: {e}")
        return None

# ---- أمر تيليجرام لجلب البروكسي ----
@l313l.ar_cmd(
    pattern="بروكسي",
    command=("بروكسي", plugin_category),
    info={
        "header": "لـ جلب بروكسي سريع",
        "الاستخدام": "{tr}بروكسي",
    },
)
async def fetch_random_proxy(event):
    try:
        await event.edit("**✎┊‌جارٍ جلب بروكسي عشوائي ...**")
        proxies = fetch_proxies()
        
        if proxies:
            # تجربة عدة بروكسيات حتى نجد واحد يعمل
            working_proxy = None
            ping_value = None
            
            for proxy in proxies[:5]:  # نجرب أول 5 بروكسيات
                ping = get_ping(proxy)
                if ping is not None:
                    working_proxy = proxy
                    ping_value = ping
                    break
            
            if working_proxy:
                # إنشاء الرابط القابل للضغط فقط
                proxy_link = f"[أضغـط هـنـا]({working_proxy})"
                
                await event.edit(
                    f"**✎┊‌ تم الحصول على بروكسي:** {proxy_link}\n"
                    f"**✎┊‌ البنك:** `{ping_value} ms`"
                )
            else:
                # إذا لم نجد بروكسي بشبكة، نعرض أول بروكسي بدون بنك
                proxy_link = f"[أضغـط هـنـا]({proxies[0]})"
                await event.edit(
                    f"**✎┊‌ تم الحصول على بروكسي:** {proxy_link}\n"
                    f"**✎┊‌ البنك:** `غير متوفر`"
                )
        else:
            await event.edit("**✎┊‌ عذرًا، لم يتم العثور على بروكسيات في الوقت الحالي.**")
            
    except Exception as e:
        await event.edit(f"**✎┊‌ حدث خطأ أثناء جلب البروكسي:**\n`{str(e)}`")
