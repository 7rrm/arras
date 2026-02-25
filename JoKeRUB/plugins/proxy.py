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
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    proxies = []
    for message in soup.find_all('a', href=True):
        if 'proxy' in message['href']:
            full_url = message['href']
            # التأكد من أن الرابط يبدأ بـ https://t.me/proxy?
            if full_url.startswith('https://t.me/proxy?') or full_url.startswith('tg://proxy?'):
                proxies.append(full_url)
    
    # إزالة التكرارات إن وجدت
    proxies = list(set(proxies))
    return proxies

def get_ping(proxy_url):
    try:
        # استخراج عنوان IP من رابط البروكسي
        # مثال: https://t.me/proxy?server=185.126.255.33&port=80&secret=...
        match = re.search(r'server=([^&]+)', proxy_url)
        if not match:
            return None
        
        proxy_server = match.group(1)
        
        # تنفيذ أمر ping (عدد 1 فقط)
        start_time = time.time()
        response = os.system(f"ping -c 1 {proxy_server} > /dev/null 2>&1")
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
            # اختيار بروكسي عشوائي من القائمة
            import random
            proxy = random.choice(proxies)
            
            # حساب البنك
            ping = get_ping(proxy)
            
            # إنشاء الرابط القابل للضغط
            proxy_link = f"[أضغـط هـنا]({proxy})"
            
            if ping is not None:
                await event.respond(
                    f"**✎┊‌ تم الحصول على بروكسي:** {proxy_link}\n"
                    f"**- البنك:** `{ping} ms`"
                )
            else:
                await event.respond(
                    f"**✎┊‌ تم الحصول على بروكسي:** {proxy_link}\n"
                    f"**- البنك:** `غير متوفر`"
                )
        else:
            await event.respond("**✎┊‌ عذرًا، لم يتم العثور على بروكسيات في الوقت الحالي.**")
            
    except Exception as e:
        await event.respond(f"**✎┊‌ حدث خطأ أثناء جلب البروكسي:**\n`{e}`")
