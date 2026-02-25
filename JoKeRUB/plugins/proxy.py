import requests
from bs4 import BeautifulSoup
import random
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
        await event.edit("**- جارٍ جلب بروكسي عشوائي ...**")
        proxies = fetch_proxies()
        
        if proxies:
            # اختيار بروكسي عشوائي من القائمة
            proxy = random.choice(proxies)
            
            # إنشاء الرابط القابل للضغط
            proxy_link = f"[أضغـط هـنـا]({proxy})"
            
            await event.edit(
                f"**✎┊‌ تم الحصول على بروكسي:** {proxy_link}"
            )
        else:
            await event.edit("**✎┊‌ عذرًا، لم يتم العثور على بروكسيات في الوقت الحالي.**")
            
    except Exception as e:
        await event.edit(f"**✎┊‌ حدث خطأ أثناء جلب البروكسي:**\n`{e}`")
