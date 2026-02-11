
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

        caption_text = f"**تم التحميـل ⥂** {title}"

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


@l313l.ar_cmd(pattern="انستقرام(?: |$)([\s\S]*)")
async def Ahmed_insta(event):
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply:
        link = reply.text
    if not link:
        return await edit_delete(event, "**↯︙ارسـل (.انستقرام) + رابـط او بالـرد ع رابـط**", 10)
    
    # تحقق من أن الرابط لإنستقرام
    if "instagram.com" not in link and "instagr.am" not in link:
        return await edit_delete(
            event, 
            "**↯︙احتـاج الـى رابــط من إنستقرام للتحميــل !**\n"
            "**↯︙مثـل:** `https://www.instagram.com/p/CvHk6zNtG5L/`", 
            10
        )
    
    dra = await edit_or_reply(event, "**↯︙جـارِ التحميل من إنستقرام انتظر قليلاً...**")
    chat = "@TIKTOKDOWNLOADROBOT"  # نفس بوت البنترست
    
    try:
        async with borg.conversation(chat) as conv:
            try:
                # إرسال الرابط والحفاظ على الرسالة الأولى لحذفها لاحقاً
                purgeflag = await conv.send_message(link)
            except YouBlockedUserError:
                await dra.edit("**↯︙يرجى إلغاء حظر @TIKTOKDOWNLOADROBOT وحاول مرة أخرى**")
                return
            
            try:
                # تجاهل الرد الأول (⏳ جاري التحميل)
                await conv.get_response(timeout=20)
            except asyncio.TimeoutError:
                # قد لا يرسل البوت رد أول في بعض الأحيان
                pass
            
            try:
                # الحصول على الرد الثاني (الوسائط) أو الانتظار أكثر
                dragoiq = await conv.get_response(timeout=40)
                
                await dra.delete()
                
                # إرسال الملف إلى المحادثة
                await borg.send_file(
                    event.chat_id,
                    dragoiq.media if dragoiq.media else dragoiq,
                    caption=(
                        f"<b>↯︙تم التحميـل من إنستقرام بنجاح ☑️</b>\n"
                        f"<b>🔗 الرابــط:</b> <code>{link}</code>"
                    ),
                    parse_mode="html",
                    reply_to=reply.id if reply else None
                )
                
                # حذف المحادثة مع البوت
                await delete_conv(event, chat, purgeflag)
                    
            except asyncio.TimeoutError:
                await dra.edit("**↯︙البوت لم يرد بالوسائط، حاول رابط آخر أو جرب لاحقاً**")
                await delete_conv(event, chat, purgeflag)
                
    except asyncio.TimeoutError:
        await dra.edit("**↯︙عذراً، فشل التحميل حاول لاحقاً**")
    except Exception as e:
        await dra.edit(f"**↯︙حدث خطأ غير متوقع:**\n`{str(e)}`")
