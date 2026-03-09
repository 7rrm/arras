import requests
from bs4 import BeautifulSoup
import time
import os
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

def get_ping(proxy_url):
    try:
        proxy_info = proxy_url.split("://")[1]
        proxy_ip = proxy_info.split(":")[0]
        start_time = time.time()
        response = os.system(f"ping -c 1 {proxy_ip}")
        end_time = time.time()
        if response == 0:
            ping = int((end_time - start_time) * 1000)
            return ping
        else:
            return None
    except Exception as e:
        print(f"Error fetching ping: {e}")
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
            # جلب أول بروكسي في القائمة
            proxy = proxies[0]
            
            # إنشاء الرابط القابل للضغط
            proxy_link = f"[أضغـط هـنـا]({proxy})"
            
            # قياس سرعة الاتصال (بنفس الطريقة الأصلية)
            ping = get_ping(proxy)
            
            if ping is not None:
                await event.edit(
                    f"**- تم الحصول على بروكسي:** {proxy_link}\n"
                    f"**- البنك:** `{ping} ms`"
                )
            else:
                await event.edit(
                    f"**- تم الحصول على بروكسي:** {proxy_link}\n"
                    f"**- البنك:** `غير متوفر`"
                )
        else:
            await event.edit("**✎┊‌ عذرًا، لم يتم العثور على بروكسيات في الوقت الحالي.**")
            
    except Exception as e:
        await event.edit(f"**✎┊‌ حدث خطأ أثناء جلب البروكسي:**\n{e}")
