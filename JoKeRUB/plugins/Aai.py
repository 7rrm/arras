import glob
import random
import asyncio
import base64
import io
import urllib.parse
import os
import glob
import random
from pathlib import Path

# تحديث أداة التحميل تلقائياً لضمان تخطي حماية يوتيوب
os.system("pip install -U yt-dlp")

from ShazamAPI import Shazam
from telethon import types
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv, name_dl, song_dl, video_dl, yt_search
from ..helpers.tools import media_type
from ..helpers.utils import _catutils, reply_id
from . import l313l

plugin_category = "utils"
LOGS = logging.getLogger(__name__)

# --- دالة الحصول على ملف كوكيز عشوائي ---
def get_cookies_file():
    folder_path = f"{os.getcwd()}/karar"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    return cookie_txt_file

# --- دالة تحضير خيارات الكوكيز ---
def get_cookies_options():
    try:
        cookie_file = get_cookies_file()
        return f" --cookies {cookie_file} --no-check-certificate --no-warnings --ignore-errors --add-header 'Referer:https://www.google.com/' "
    except FileNotFoundError:
        return " --no-check-certificate --no-warnings --ignore-errors --add-header 'Referer:https://www.google.com/' "

@l313l.ar_cmd(pattern="بحث(320)?(?:\s|$)([\s\S]*)")
async def _(event):
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    query = event.pattern_match.group(2) or (reply.message if reply else None)
    if not query:
        return await edit_or_reply(event, "**⌔∮ يرجى كتابة اسم الأغنية أو الرد على نص**")
    
    catevent = await edit_or_reply(event, "**⌔∮ جاري البحث والتحميل.. انتظر قليلاً**")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit("**⌔∮ عذراً، لم يتم العثور على نتائج**")
    
    quality = "320k" if event.pattern_match.group(1) == "320" else "128k"
    
    # استخدام دالة get_cookies_options() بدلاً من C_PATH
    cookies_cmd = get_cookies_options()
    song_cmd = f"{song_dl.format(QUALITY=quality, video_link=video_link)}{cookies_cmd}"
    name_cmd = f"{name_dl.format(video_link=video_link)}{cookies_cmd}"
    
    try:
        await _catutils.runcmd(song_cmd)
        catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
        catname = os.path.splitext(catname)[0]
        song_file = Path(f"{catname}.mp3")
        
        if not os.path.exists(song_file):
            return await catevent.edit(f"**⌔∮ فشل التحميل من يوتيوب:**\n`{stderr}`")
            
        await event.client.send_file(
            event.chat_id, 
            song_file, 
            caption=f"**⌔∮ العنوان:** `{urllib.parse.unquote(catname).replace('./temp/', '')}`", 
            supports_streaming=True, 
            reply_to=reply_to_id
        )
        await catevent.delete()
        if os.path.exists(song_file): os.remove(song_file)
    except Exception as e:
        await catevent.edit(f"**⌔∮ حدث خطأ:** `{str(e)}` ")

@l313l.ar_cmd(pattern="فيديو(?:\s|$)([\s\S]*)")
async def _(event):
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    query = event.pattern_match.group(1) or (reply.message if reply else None)
    if not query:
        return await edit_or_reply(event, "**⌔∮ يرجى كتابة اسم الفيديو**")
    
    catevent = await edit_or_reply(event, "**⌔∮ جاري معالجة طلب الفيديو..**")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit("**⌔∮ لم أجد نتائج لهذا الفيديو**")
    
    # استخدام دالة get_cookies_options() بدلاً من C_PATH
    cookies_cmd = get_cookies_options()
    video_cmd = f"{video_dl.format(video_link=video_link)}{cookies_cmd}"
    name_cmd = f"{name_dl.format(video_link=video_link)}{cookies_cmd}"
    
    try:
        await _catutils.runcmd(video_cmd)
        catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
        catname = os.path.splitext(catname)[0]
        
        vsong_file = next(Path('.').glob(f"{catname}.*"), None)
        if not vsong_file: vsong_file = Path(f"{catname}.mp4")

        await event.client.send_file(
            event.chat_id, 
            vsong_file, 
            caption=f"**⌔∮ العنوان:** `{urllib.parse.unquote(catname).replace('./temp/', '')}`", 
            supports_streaming=True, 
            reply_to=reply_to_id
        )
        await catevent.delete()
        if os.path.exists(vsong_file): os.remove(vsong_file)
    except Exception as e:
        await catevent.edit(f"**⌔∮ خطأ أثناء تحميل الفيديو:** `{str(e)}` ")

@l313l.ar_cmd(pattern="اسم الاغنية$")
async def shazamcmd(event):
    reply = await event.get_reply_message()
    if not reply or media_type(reply) not in ["Voice", "Audio"]:
        return await edit_delete(event, "**⌔∮ يرجى الرد على بصمة أو ملف صوتي**")
    
    catevent = await edit_or_reply(event, "**⌔∮ جاري التعرف على الصوت...**")
    try:
        name = "shazam.mp3"
        await event.client.download_media(reply, name)
        track = next(Shazam(open(name, "rb").read()).recognizeSong())[1]["track"]
        await event.client.send_file(
            event.chat_id, 
            track["images"]["background"], 
            caption=f"**⌔∮ تم العثور على الأغنية:**\n\n`{track['share']['subject']}`", 
            reply_to=reply
        )
        await catevent.delete()
        os.remove(name)
    except Exception as e:
        await edit_delete(catevent, f"**⌔∮ لم أستطع التعرف على الصوت:** `{e}`")
