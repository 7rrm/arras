
from .. import l313l
from ..core.managers import edit_or_reply
from telethon import events
import aiohttp
import re
from bs4 import BeautifulSoup


TIKTOK_API = "https://www.tikwm.com/api/"

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
        title = result.get("title") or "TikTok Video"

        caption_text = f"تم التحميـل ⥂ ({title})"

        if result.get("play"):
            await event.client.send_file(
                event.chat_id,
                result["play"],
                caption=caption_text
            )

        if result.get("images"):
            for img in result["images"]:
                await event.client.send_file(
                    event.chat_id,
                    img,
                    caption="📸 صورة من تيك توك"
                )

        await zed.delete()
    except Exception as e:
        await zed.edit(f"❌ خطأ: {str(e)}")
        



@l313l.ar_cmd(pattern=r"انستا(?:\s+|$)(.*)")
async def insta_download(event):
    reply = await event.get_reply_message()
    link = event.pattern_match.group(1).strip() or (reply.text.strip() if reply else "")

    if not link or not re.search(r"(instagram\.com|instagr\.am)", link):
        return await edit_or_reply(event, "📌 أرسل رابط إنستقرام بعد الأمر أو بالرد على الرابط.")

    zed = await edit_or_reply(event, "⏳ جاري التحميل من إنستقرام...")

    try:
        api_url = "https://insta.savetube.me/downloadPostVideo"
        payload = {"url": link}

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload) as resp:
                if resp.status != 200:
                    return await zed.edit("⚠️ لم أستطع جلب الوسائط، جرّب رابط آخر.")
                data = await resp.json()

            video_url = data.get("post_video_url")
            thumb_url = data.get("post_video_thumbnail")

            if not video_url:
                return await zed.edit("⚠️ لم أجد أي وسائط في الرابط.")

            # جلب عنوان الفيديو من صفحة الإنستقرام
            async with session.get(link) as resp_html:
                if resp_html.status == 200:
                    html = await resp_html.text()
                    soup = BeautifulSoup(html, "html.parser")
                    og_title = soup.find("meta", property="og:title")
                    title = og_title["content"] if og_title else "Instagram Video"
                else:
                    title = "Instagram Video"

        caption_text = f"**تم التحميـل ⥂** (`{title}`)"

        await event.client.send_file(
            event.chat_id,
            video_url,
            caption=caption_text,
            thumb=thumb_url if thumb_url else None
        )

        await zed.delete()

    except Exception as e:
        await zed.edit(f"❌ خطأ: {str(e)}")
        
