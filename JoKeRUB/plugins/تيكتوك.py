
from .. import l313l
from ..core.managers import edit_or_reply
from telethon import events
import aiohttp
import re

TIKTOK_API = "https://www.tikwm.com/api/"
INSTAGRAM_API = "https://snapinsta.io/action.php"  # 𝑨𝑺𝑯𝑬𝑸 𝑨𝑳𝑺𝑨𝑴𝑻 𝒀𝑨𝑴𝑬𝑵𝑻𝑯𝑶𝑵

async def fetch_data(url, params=None, method="GET", data=None, return_json=True):
    async with aiohttp.ClientSession() as session:
        if method == "GET":
            async with session.get(url, params=params) as resp:
                return await (resp.json() if return_json else resp.text())
        else:
            async with session.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}) as resp:
                return await (resp.json() if return_json else resp.text())

@l313l.ar_cmd(pattern="تيك(?:\s+|$)(.*)")
async def tiktok_download(event):
    reply = await event.get_reply_message()
    link = event.pattern_match.group(1) or (reply.text if reply else "")

    if not link or "tiktok.com" not in link:
        return await edit_or_reply(event, "📌 أرسل رابط تيك توك بعد الأمر أو بالرد على الرابط.")

    zed = await edit_or_reply(event, "⏳ جاري التحميل من تيك توك...")
    try:
        data = await fetch_data(TIKTOK_API, method="POST", data={"url": link}, return_json=True)

        if data.get("code") != 0:
            return await zed.edit("⚠️ لم أستطع جلب الفيديو، تأكد من الرابط.")

        result = data["data"]

        if result.get("play"):
            await event.client.send_file(event.chat_id, result["play"], caption="**𝑶𝑲✅𝑻𝑰𝑲 𝑻𝑶𝑲**\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 𝙔𝘼𝙈𝙀𝙉𝙏𝙃𝙊𝙉](https://t.me/YamenThon)")

        if result.get("images"):
            for img in result["images"]:
                await event.client.send_file(event.chat_id, img, caption="📸 صورة من تيك توك")

        await zed.delete()
    except Exception as e:
        await zed.edit(f"❌ خطأ: {str(e)}")


import re
import aiohttp

@l313l.ar_cmd(pattern=r"اانستا(?:\s+|$)(.*)")
async def insta_download(event):
    reply = await event.get_reply_message()
    link = event.pattern_match.group(1).strip() or (reply.text.strip() if reply else "")

    if not link or not re.search(r"(instagram\.com|instagr\.am)", link):
        return await edit_or_reply(event, "📌 أرسل رابط إنستقرام بعد الأمر أو بالرد على الرابط.")

    zed = await edit_or_reply(event, "⏳ جاري التحميل من إنستقرام...")

    try:
        # أسرع API مباشر
        video_url = await fastest_instagram_api(link)
        
        if not video_url:
            return await zed.edit("⚠️ لم أستطع تحميل الفيديو.")

        # إرسال الفيديو
        await event.client.send_file(
            event.chat_id,
            video_url,
            caption="**𝑶𝑲📥𝑰𝑵𝑺𝑻𝑨𝑮𝑹𝑨𝑴**\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 𝙔𝘼𝙈𝙀𝙉𝙏𝙃𝙊𝙉](https://t.me/YamenThon)",
            supports_streaming=True
        )

        await zed.delete()

    except Exception as e:
        await zed.edit(f"❌ خطأ: {str(e)}")

async def fastest_instagram_api(link):
    """أسرع API لتحميل الإنستجرام"""
    try:
        # استخدم هذا API - الأسرع والأكثر استقراراً
        api_url = "https://api.savetube.be/api/instagram"
        params = {"url": link}
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(api_url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("url")
                    
    except Exception as e:
        print(f"API Error: {e}")
        
    return None
