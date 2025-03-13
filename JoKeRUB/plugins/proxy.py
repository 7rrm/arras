import requests
from bs4 import BeautifulSoup
import time
import os
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
            proxies.append(message['href'])
    
    return proxies

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
            proxy = proxies[0]
            ping = get_ping(proxy)

            if ping is not None:
                await event.respond(f"**✎┊‌ تم الحصول على بروكسي:**\n{proxy}\n**البنك:** {ping} ms")
            else:
                await event.respond("**✎┊‌ عذرًا، لم أتمكن من حساب البنك للبروكسي.**")
        else:
            await event.respond("**✎┊‌ عذرًا، لم يتم العثور على بروكسيات في الوقت الحالي.**")
    except Exception as e:
        await event.respond(f"**✎┊‌ حدث خطأ أثناء جلب البروكسي:**\n{e}")
        
