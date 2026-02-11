import asyncio
import glob
import contextlib
import io
import os
import re
import pathlib
from time import time
import requests
import random
from pathlib import Path

import aiohttp
import aiofiles
import wget
import yt_dlp
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
from ShazamAPI import Shazam
from validators.url import url

from urlextract import URLExtract
from wget import download
from yt_dlp import YoutubeDL
from yt_dlp.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from telethon import functions
from telethon.tl.types import InputMessagesFilterEmpty
from telethon import events
from telethon.tl import types
from telethon.utils import get_attributes
from telethon.errors.rpcerrorlist import YouBlockedUserError, ChatSendMediaForbiddenError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.types import DocumentAttributeAudio

from ..Config import Config
from ..core import pool
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import progress, reply_id
from ..helpers.functions import delete_conv, name_dl, song_dl, video_dl, yt_search
from ..helpers.functions.utube import _mp3Dl, get_yt_video_id, get_ytthumb, ytsearch
from ..helpers.tools import media_type
from ..helpers.utils import _format, reply_id, _catutils
from . import BOTLOG, BOTLOG_CHATID, l313l

BASE_YT_URL = "https://www.youtube.com/watch?v="
extractor = URLExtract()
LOGS = logging.getLogger(__name__)

plugin_category = "البحث"

# =========================================================== #
#                                                             𝙕𝙏𝙝𝙤𝙣
# =========================================================== #
SONG_SEARCH_STRING = "<b>╮ جـارِ البحث ؏ـن المقطـٓع الصٓوتـي... 🎧♥️╰</b>"
SONG_NOT_FOUND = "<b>⎉╎لـم استطـع ايجـاد المطلـوب .. جرب البحث باستخـدام الامـر (.اغنيه)</b>"
SONG_SENDING_STRING = "<b>╮ جـارِ تحميـل المقطـٓع الصٓوتـي... 🎧♥️╰</b>"
# =========================================================== #
#                                                             𝙕𝙏𝙝𝙤𝙣
# =========================================================== #


def get_cookies_file():
    folder_path = f"{os.getcwd()}/karar"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    return cookie_txt_file


video_opts = {
    "format": "best",
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "writethumbnail": True,
    "prefer_ffmpeg": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "postprocessors": [
        {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
        {"key": "FFmpegMetadata"},
    ],
    "outtmpl": "zed_ytv.mp4",
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "cookiefile" : get_cookies_file(),
}


async def ytdl_down(event, opts, url):
    ytdl_data = None
    try:
        await event.edit("**╮ ❐ يتـم جلـب البيانـات انتظـر قليلاً ...𓅫╰▬▭ **")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await event.edit(f"`{DE}`")
    except ContentTooShortError:
        await event.edit("**- عذرا هذا المحتوى قصير جدا لتنزيله ⚠️**")
    except GeoRestrictedError:
        await event.edit(
            "**- الفيديو غير متاح من موقعك الجغرافي بسبب القيود الجغرافية التي يفرضها موقع الويب ❕**"
        )
    except MaxDownloadsReached:
        await event.edit("**- تم الوصول إلى الحد الأقصى لعدد التنزيلات ❕**")
    except PostProcessingError:
        await event.edit("**كان هناك خطأ أثناء المعالجة**")
    except UnavailableVideoError:
        await event.edit("**⌔∮عـذراً .. الوسائط غير متوفـره بالتنسيق المطلـوب**")
    except XAttrMetadataError as XAME:
        await event.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        await event.edit("**حدث خطأ أثناء استخراج المعلومات يرجى وضعها بشكل صحيح ⚠️**")
    except Exception as e:
        await event.edit(f"**- خطـأ : **\n__{e}__")
    return ytdl_data


async def fix_attributes(
    path, info_dict: dict, supports_streaming: bool = False, round_message: bool = False
) -> list:
    """Avoid multiple instances of an attribute."""
    new_attributes = []
    video = False
    audio = False

    uploader = info_dict.get("uploader", "Unknown artist")
    duration = int(info_dict.get("duration", 0))
    suffix = path.suffix[1:]
    if supports_streaming and suffix != "mp4":
        supports_streaming = True

    attributes, mime_type = get_attributes(path)
    if suffix == "mp3":
        title = str(info_dict.get("title", info_dict.get("id", "Unknown title")))
        audio = types.DocumentAttributeAudio(
            duration=duration, voice=None, title=title, performer=uploader
        )
    elif suffix == "mp4":
        width = int(info_dict.get("width", 0))
        height = int(info_dict.get("height", 0))
        for attr in attributes:
            if isinstance(attr, types.DocumentAttributeVideo):
                duration = duration or attr.duration
                width = width or attr.w
                height = height or attr.h
                break
        video = types.DocumentAttributeVideo(
            duration=duration,
            w=width,
            h=height,
            round_message=round_message,
            supports_streaming=supports_streaming,
        )

    if audio and isinstance(audio, types.DocumentAttributeAudio):
        new_attributes.append(audio)
    if video and isinstance(video, types.DocumentAttributeVideo):
        new_attributes.append(video)

    new_attributes.extend(
        attr
        for attr in attributes
        if (
            isinstance(attr, types.DocumentAttributeAudio)
            and not audio
            or not isinstance(attr, types.DocumentAttributeAudio)
            and not video
            or not isinstance(attr, types.DocumentAttributeAudio)
            and not isinstance(attr, types.DocumentAttributeVideo)
        )
    )
    return new_attributes, mime_type


@l313l.ar_cmd(pattern="سناب(?: |$)(.*)")
async def download_video(event):
    msg = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not msg and rmsg:
        msg = rmsg.text
    urls = extractor.find_urls(msg)
    if not urls:
        return await edit_or_reply(event, "**- قـم بادخــال رابـط مع الامـر او بالــرد ع رابـط ليتـم التحميـل**")
    zedevent = await edit_or_reply(event, "**⎉╎جـارِ التحميل انتظر قليلا ▬▭ ...**")
    reply_to_id = await reply_id(event)
    for url in urls:
        ytdl_data = await ytdl_down(zedevent, video_opts, url)
        if ytdl_down is None:
            return
        try:
            f = pathlib.Path("zed_ytv.mp4")
            print(f)
            catthumb = pathlib.Path("zed_ytv.jpg")
            if not os.path.exists(catthumb):
                catthumb = pathlib.Path("zed_ytv.webp")
            if not os.path.exists(catthumb):
                catthumb = None
            await zedevent.edit(
                f"**╮ ❐ جـارِ التحضيـر للـرفع انتظـر ...𓅫╰**:\
                \n**{ytdl_data['title']}**"
            )
            ul = io.open(f, "rb")
            c_time = time()
            attributes, mime_type = await fix_attributes(
                f, ytdl_data, supports_streaming=True
            )
            uploaded = await event.client.fast_upload_file(
                file=ul,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d, t, zedevent, c_time, "Upload :", file_name=ytdl_data["title"]
                    )
                ),
            )
            ul.close()
            media = types.InputMediaUploadedDocument(
                file=uploaded,
                mime_type=mime_type,
                attributes=attributes,
            )
            await event.client.send_file(
                event.chat_id,
                file=media,
                reply_to=reply_to_id,
                caption=f'**⎉╎المقطــع :** `{ytdl_data["title"]}`\n**⎉╎الرابـط : {msg}**\n**⎉╎تم  التحميـل .. بنجـاح ✅**"',
                thumb=catthumb,
            )
            os.remove(f)
            if catthumb:
                os.remove(catthumb)
        except TypeError:
            await asyncio.sleep(2)
    await event.delete()


@l313l.ar_cmd(pattern="فيس(?: |$)(.*)")
async def download_video(event):
    msg = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not msg and rmsg:
        msg = rmsg.text
    urls = extractor.find_urls(msg)
    if not urls:
        return await edit_or_reply(event, "**- قـم بادخــال رابـط مع الامـر او بالــرد ع رابـط ليتـم التحميـل**")
    zedevent = await edit_or_reply(event, "**⎉╎جـارِ التحميل انتظر قليلا ▬▭ ...**")
    reply_to_id = await reply_id(event)
    for url in urls:
        ytdl_data = await ytdl_down(zedevent, video_opts, url)
        if ytdl_down is None:
            return
        try:
            f = pathlib.Path("zed_ytv.mp4")
            print(f)
            catthumb = pathlib.Path("zed_ytv.jpg")
            if not os.path.exists(catthumb):
                catthumb = pathlib.Path("zed_ytv.webp")
            if not os.path.exists(catthumb):
                catthumb = None
            await zedevent.edit(
                f"**╮ ❐ جـارِ التحضيـر للـرفع انتظـر ...𓅫╰**:\
                \n**{ytdl_data['title']}**"
            )
            ul = io.open(f, "rb")
            c_time = time()
            attributes, mime_type = await fix_attributes(
                f, ytdl_data, supports_streaming=True
            )
            uploaded = await event.client.fast_upload_file(
                file=ul,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d, t, zedevent, c_time, "Upload :", file_name=ytdl_data["title"]
                    )
                ),
            )
            ul.close()
            media = types.InputMediaUploadedDocument(
                file=uploaded,
                mime_type=mime_type,
                attributes=attributes,
            )
            await event.client.send_file(
                event.chat_id,
                file=media,
                reply_to=reply_to_id,
                caption=f'**⎉╎المقطــع :** `{ytdl_data["title"]}`\n**⎉╎الرابـط : {msg}**\n**⎉╎تم  التحميـل .. بنجـاح ✅**"',
                thumb=catthumb,
            )
            os.remove(f)
            if catthumb:
                os.remove(catthumb)
        except TypeError:
            await asyncio.sleep(2)
    await event.delete()

@l313l.ar_cmd(pattern="بنترست(?: |$)([\s\S]*)")
async def Ahmed_pin(event):
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply:
        link = reply.text
    if not link:
        return await edit_delete(event, "**- ارسـل (.بنترست) + رابـط او بالـرد ع رابـط**", 10)
    if "pin" not in link:
        return await edit_delete(
            event, "**- احتـاج الـى رابــط من بنتـرسـت .. للتحميــل ؟!**", 10
        )
    
    dra = await edit_or_reply(event, "**↯︙جـارِ التحميل من بنتـرسـت انتظر قليلا**")
    chat = "@TIKTOKDOWNLOADROBOT"
    
    try:
        async with borg.conversation(chat) as conv:
            try:
                # إرسال الرابط والحفاظ على الرسالة الأولى لحذفها لاحقاً
                purgeflag = await conv.send_message(link)
            except YouBlockedUserError:
                await dra.edit("**- يرجى إلغاء حظر @TIKTOKDOWNLOADROBOT وحاول مرة أخرى**")
                return
            
            # تجاهل الرد الأول (⏳)
            await conv.get_response()
            
            # الحصول على الرد الثاني (الوسائط)
            dragoiq = await conv.get_response()
            
            await dra.delete()
            await borg.send_file(
                event.chat_id,
                dragoiq,
                caption=f"<b>↯︙تم التحميـل من بنتـرسـت بنجاح</b>",
                parse_mode="html",
            )
            
            # حذف المحادثة مع البوت باستخدام الدالة الموجودة
            await delete_conv(event, chat, purgeflag)
                
    except asyncio.TimeoutError:
        await dra.edit("**↯︙• عذراً، فشل التحميل حاول لاحقاً .**")
    except Exception as e:
        await dra.edit(f"**↯︙حدث خطأ غير متوقع:**\n`{str(e)}`")


@l313l.ar_cmd(pattern="انستا(?: |$)([\s\S]*)")
async def instagram_downloader(event):
    # نفس كود البنترست بلضبط مع تغيير الرسائل فقط
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply:
        link = reply.text
    if not link:
        return await edit_delete(event, "**- ارسـل (.انستا) + رابـط او بالـرد ع رابـط**", 10)
    
    # فقط غيرنا pin إلى instagram
    if "instagram.com" not in link:
        return await edit_delete(
            event, "**- احتـاج الـى رابــط من انستقرام .. للتحميــل ؟!**", 10
        )
    
    # نفس المتغيرات بلضبط
    dra = await edit_or_reply(event, "**↯︙جـارِ التحميل من انستقرام انتظر قليلا**")
    chat = "@TIKTOKDOWNLOADROBOT"  # نفس البوت بلضبط
    
    try:
        # نفس المحادثة بلضبط
        async with borg.conversation(chat) as conv:
            try:
                # نفس الإرسال بلضبط
                purgeflag = await conv.send_message(link)
            except YouBlockedUserError:
                await dra.edit("**- يرجى إلغاء حظر @TIKTOKDOWNLOADROBOT وحاول مرة أخرى**")
                return
            
            # نفس تجاهل الرد الأول بلضبط
            await conv.get_response()
            
            # نفس الحصول على الرد الثاني بلضبط
            dragoiq = await conv.get_response()
            
            # نفس الحذف بلضبط
            await dra.delete()
            
            # نفس الإرسال بلضبط
            await borg.send_file(
                event.chat_id,
                dragoiq,
                caption=f"<b>↯︙تم التحميـل من انستقرام بنجاح</b>",
                parse_mode="html",
            )
            
            # نفس حذف المحادثة بلضبط
            await delete_conv(event, chat, purgeflag)
                
    except asyncio.TimeoutError:
        await dra.edit("**↯︙• عذراً، فشل التحميل حاول لاحقاً .**")
    except Exception as e:
        await dra.edit(f"**↯︙حدث خطأ غير متوقع:**\n`{str(e)}`")

@l313l.ar_cmd(
    pattern="ساوند(?: |$)(.*)",
    command=("ساوند", plugin_category),
    info={
        "header": "تحميـل الاغـاني مـن سـاونـد كـلاود الـخ عـبر الرابـط",
        "مثــال": ["{tr}ساوند بالــرد ع رابــط", "{tr}ساوند + رابــط"],
    },
)
async def download_audio(event):
    """To download audio from YouTube and many other sites."""
    msg = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not msg and rmsg:
        msg = rmsg.text
    urls = extractor.find_urls(msg)
    if not urls:
        return await edit_or_reply(event, "**- قـم بادخــال رابـط مع الامـر او بالــرد ع رابـط ليتـم التحميـل**")
    zedevent = await edit_or_reply(event, "**⎉╎جـارِ التحميل انتظر قليلا ▬▭ ...**")
    reply_to_id = await reply_id(event)
    for url in urls:
        try:
            vid_data = YoutubeDL({"no-playlist": True, "cookiefile": get_cookies_file()}).extract_info(
                url, download=False
            )
        except ExtractorError:
            vid_data = {"title": url, "uploader": "Catuserbot", "formats": []}
        startTime = time()
        retcode = await _mp3Dl(url=url, starttime=startTime, uid="320")
        if retcode != 0:
            return await event.edit(str(retcode))
        _fpath = ""
        thumb_pic = None
        for _path in glob.glob(os.path.join(Config.TEMP_DIR, str(startTime), "*")):
            if _path.lower().endswith((".jpg", ".png", ".webp")):
                thumb_pic = _path
            else:
                _fpath = _path
        if not _fpath:
            return await edit_delete(zedevent, "__Unable to upload file__")
        await zedevent.edit(
            f"**╮ ❐ جـارِ التحضيـر للـرفع انتظـر ...𓅫╰**:\
            \n**{vid_data['title']}***"
        )
        attributes, mime_type = get_attributes(str(_fpath))
        ul = io.open(pathlib.Path(_fpath), "rb")
        if thumb_pic is None:
            thumb_pic = str(
                await pool.run_in_thread(download)(
                    await get_ytthumb(get_yt_video_id(url))
                )
            )
        uploaded = await event.client.fast_upload_file(
            file=ul,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d,
                    t,
                    zedevent,
                    startTime,
                    "trying to upload",
                    file_name=os.path.basename(pathlib.Path(_fpath)),
                )
            ),
        )
        ul.close()
        media = types.InputMediaUploadedDocument(
            file=uploaded,
            mime_type=mime_type,
            attributes=attributes,
            force_file=False,
            thumb=await event.client.upload_file(thumb_pic) if thumb_pic else None,
        )
        await event.client.send_file(
            event.chat_id,
            file=media,
            caption=f"<b>⎉╎المقطع : </b><code>{vid_data.get('title', os.path.basename(pathlib.Path(_fpath)))}</code>",
            supports_streaming=True,
            reply_to=reply_to_id,
            parse_mode="html",
        )
        for _path in [_fpath, thumb_pic]:
            os.remove(_path)
    await zedevent.delete()

@l313l.ar_cmd(pattern="تلي (.*)")
async def _(event): # Code by t.me/zzzzl1l
    search = event.pattern_match.group(1)
    l = 'qwertyuiopasdfghjklxcvbnmz'
    result = await l313l(functions.contacts.SearchRequest(
        q=search,
        limit=20
    ))
    json = result.to_dict()
    i = str(''.join(random.choice(l) for i in range(3))) + '.txt'
    counter = 0
    for item in json['chats']:
        channel_id = item["username"]
        links = f'https://t.me/{channel_id}'
        counter += 1
        open(i, 'a').write(f"{counter}• {links}\n")
    link = open(i, 'r').read()
    if not link:
        await event.edit("**- لا توجد نتائج في البحث**")
    else:
        await event.edit(f'''
ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 - **بـحـث تيليـجـࢪام**
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
l {search} l  **🔎 نتائـج البحث عـن -**
l قنوات + مجموعات l **يشمـل -**

{link}
        ''')

import random
import os
from telethon.tl.types import InputMessagesFilterEmpty
from datetime import datetime

@l313l.ar_cmd(pattern="كلمه (.*)")
async def _(event): # Code by t.me/zzzzl1l
    search_word = event.pattern_match.group(1)
    chat = await event.get_chat()
    chat_name = chat.title or "دردشة خاصة"
    
    # إنشاء اسم ملف فريد
    file_name = f"بحث_{search_word}_{random.randint(1000, 9999)}.txt"
    
    # تحديث الرسالة لإعلام المستخدم
    await event.edit(f"**⏳ جاري البحث عن `{search_word}` في {chat_name}...**")
    
    counter = 0
    
    try:
        # فتح الملف للكتابة
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"🔍 نتائج البحث عن: {search_word}\n")
            f.write(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"📍 في: {chat_name}\n")
            f.write("="*50 + "\n\n")
        
        # البحث في الرسائل
        messages = await l313l.get_messages(chat, filter=InputMessagesFilterEmpty(), limit=250)
        
        for message in messages:
            if message.message and search_word in message.message:
                links = f'https://t.me/c/{chat.id}/{message.id}'
                counter += 1
                
                # كتابة النتيجة في الملف
                with open(file_name, 'a', encoding='utf-8') as f:
                    f.write(f"{counter}• {links}\n")
        
        # تحديث رأس الملف بعد معرفة العدد النهائي
        with open(file_name, 'r+', encoding='utf-8') as f:
            content = f.read()
            f.seek(0)
            f.write(f"🔍 نتائج البحث عن: {search_word}\n")
            f.write(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"📍 في: {chat_name}\n")
            f.write(f"✅ عدد النتائج: {counter} نتيجة\n")
            f.write("="*50 + "\n\n")
            # الحفاظ على المحتوى الأصلي (بدون الرأس القديم)
            lines = content.split('\n')
            if len(lines) > 4:
                f.write('\n'.join(lines[4:]))
        
        # حذف رسالة "جاري البحث"
        await event.delete()
        
        # إرسال الملف إذا كان هناك نتائج
        if counter > 0:
            await l313l.send_file(
                event.chat_id,
                file_name,
                caption=f'''
ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 - **بـحـث تيليـجـࢪام**
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
l {search_word} l  **نتائـج البحث عـن -**
l {chat_name} l  **فـي المجموعـة -**
l {counter} نتيجة l  **العدد -**

*تم حفظ النتائج في الملف المرفق*
                ''',
                reply_to=event.message.id
            )
        else:
            await event.respond(f"**❌ لا توجد نتائج لـ `{search_word}` في {chat_name}**")
            
    except Exception as e:
        await event.edit(f"**⚠️ حدث خطأ:** `{str(e)}`")
    
    finally:
        # تنظيف الملف المؤقت
        if os.path.exists(file_name):
            os.remove(file_name)

@l313l.ar_cmd(pattern="كلمة (.*)")
async def search_all(event):
    search_word = event.pattern_match.group(1)
    
    # إنشاء اسم ملف فريد
    import random
    l = 'qwertyuiopasdfghjklxcvbnmz'
    file_name = str(''.join(random.choice(l) for i in range(3))) + '.txt'
    
    # رسالة بداية واحدة فقط
    await event.edit(f"**⏳ جاري البحث عن `{search_word}` في جميع المحادثات...**")
    
    counter = 0
    
    try:
        # الحصول على جميع الدردشات
        dialogs = await l313l.get_dialogs(limit=None)
        
        results_per_chat = {}
        
        # البحث في كل دردشة
        for dialog in dialogs:
            try:
                chat = dialog.entity
                chat_id = chat.id
                chat_name = dialog.name or "بدون اسم"
                
                # البحث في الدردشة
                chat_results = []
                async for message in l313l.iter_messages(
                    chat_id, 
                    search=search_word,
                    limit=20
                ):
                    if message.message and search_word in message.message:
                        link = f'https://t.me/c/{chat_id}/{message.id}'
                        chat_results.append(link)
                
                if chat_results:
                    results_per_chat[chat_name] = chat_results
                    counter += len(chat_results)
                    
            except Exception:
                continue
        
        # إنشاء ملف النتائج (دائماً)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"نتائج البحث عن: {search_word}\n")
            f.write(f"العدد الإجمالي: {counter} نتيجة\n")
            f.write("="*50 + "\n\n")
            
            for chat_name, links in results_per_chat.items():
                f.write(f"📌 **{chat_name}** ({len(links)} نتيجة):\n")
                for link_idx, link in enumerate(links[:5], 1):
                    f.write(f"  {link_idx}. {link}\n")
                if len(links) > 5:
                    f.write(f"  ... و {len(links) - 5} نتيجة أخرى\n")
                f.write("\n")
        
        # حذف رسالة "جاري البحث"
        await event.delete()
        
        # إرسال الملف دائماً (حتى لو كانت النتائج قصيرة)
        await l313l.send_file(
            event.chat_id,
            file_name,
            caption=f"**نتائج البحث عن: `{search_word}`**\n**العدد الإجمالي: {counter} نتيجة**\n\n*تم حفظ النتائج في الملف المرفق*",
            reply_to=event.message.id
        )
        
    except Exception as e:
        await event.edit(f"**⚠️ حدث خطأ:** `{str(e)}`")
    
    finally:
        # تنظيف الملف المؤقت
        import os
        if os.path.exists(file_name):
            os.remove(file_name)


# ================================================================================================ #
# =========================================ساوند كلاود================================================= #
# ================================================================================================ #
'''
import os
import yt_dlp
from youtube_search import YoutubeSearch
from telethon.errors import ChatSendMediaForbiddenError
from telethon.tl.types import DocumentAttributeAudio

# مسار الصورة المصغرة الثابتة
DEFAULT_THUMBNAIL = "l313l/razan/resources/start/ssyy.JPEG"
DEFAULT_ARTIST = "𓏺 ᥲRRᥲS . @Lx5x5 "

def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)

def parse_duration(duration_str):
    """تحويل المدة من mm:ss إلى ثواني وتنسيق للعرض"""
    try:
        parts = list(map(int, duration_str.split(':')))
        if len(parts) == 2:
            seconds = parts[0] * 60 + parts[1]
            # تنسيق المدة إلى دقائق وثواني
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            return seconds, f"{minutes:02d}:{remaining_seconds:02d}"
        return 0, "00:00"
    except:
        return 0, "00:00"

@l313l.ar_cmd(pattern="بحث(?: |$)(.*)")
async def yt_audio_search(event):
    # الحصول على الاستعلام من الرسالة
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "**✧╎قم باضافـة إسـم للامـر ..**\n**⎉╎بحث + اسـم المقطـع الصـوتي**")
    
    zedevent = await edit_or_reply(event, "**╮ جـارِ البحث عـن الإغـنيةة ... 🎧♥️ ╰**")
    
    ydl_ops = {
            "format":"worstaudio[ext=m4a]",
            "socket_timeout": 5,
            "http_chunk_size": 5242880,
            "noplaylist": True,
            "extract_flat": True,
            "fragment_retries": 2,
            "retries": 2,
            "quiet": True,
            "no_warnings": True,
            "geo_bypass": True,
            "cookiefile": get_cookies_file(),
            "outtmpl": "%(id)s.%(ext)s"
    }
    
    try:
        # البحث باستخدام YoutubeSearch
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            raise Exception("لم يتم العثور على نتائج")
            
        video_id = results[0]['id']
        link = f"https://youtu.be/{video_id}"
        title = results[0]["title"]
        duration_str = results[0]["duration"]
        duration_seconds, formatted_duration = parse_duration(duration_str)
        
    except Exception as e:
        await zedevent.edit(f"**- فشـل في البحث** \n**- الخطأ:** `{str(e)}`")
        return
    
    await zedevent.edit("**╮ ❐ جـارِ التحميل ▬▭ . . . ╰**")
    
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            audio_file = ydl.prepare_filename(info_dict)
            
        await zedevent.edit("**╮ ❐ جـارِ الرفـع ▬▬ . . 🎧♥️╰**")
        await event.client.send_file(
            event.chat_id,
            audio_file,
            force_document=False,
            caption=f"**S𝑜𝑛𝑔N𝑎𝑚𝑒 ⥂** `{title}`\n**D𝑢𝑟𝑎𝑡𝑖𝑜𝑛 :-** `{formatted_duration}`",
            thumb=DEFAULT_THUMBNAIL,
            reply_to=event.reply_to_msg_id or event.id,
            attributes=[
                DocumentAttributeAudio(
                    duration=duration_seconds,
                    performer=DEFAULT_ARTIST,
                    title=title
                )
            ]
        )
        
        await zedevent.delete()
        
    except ChatSendMediaForbiddenError:
        await zedevent.edit("**- عـذراً .. الوسـائـط مغلقـه هنـا**")
    except Exception as e:
        await zedevent.edit(f"**- فشـل التحميـل** \n**- الخطأ:** `{str(e)}`")
    finally:
        remove_if_exists(audio_file)

@l313l.ar_cmd(pattern="فيديو(?: |$)(.*)")
async def _(event): #Code by T.me/zzzzl1l
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "**⎉╎قم باضافـة إسـم للامـر ..**\n**⎉╎فيديو + اسـم الفيديـو**")
    zedevent = await edit_or_reply(event, "**╮ جـارِ البحث ؏ـن الفيديـو... 🎧♥️╰**")
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
        "no_warnings": True,
        "cookiefile" : get_cookies_file(),
    }
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
    except Exception as e:
        await zedevent.edit(f"**- فشـل التحميـل** \n**- الخطأ :** `{str(e)}`")
        #return
    try:
        msg = await zedevent.edit("**╮ جـارِ التحميل ▬▭ . . .🎧♥️╰**")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await zedevent.edit(f"**- فشـل التحميـل** \n**- الخطأ :** `{str(e)}`")
    preview = wget.download(thumbnail)
    await zedevent.edit("**╮ جـارِ الرفـع ▬▬ . . .🎧♥️╰**")
    await event.client.send_file(
        event.chat_id,
        file_name,
        caption=f"**⎉╎البحث :** `{title}`",
        thumb=preview,
        supports_streaming=True,
    )
    try:
        remove_if_exists(file_name)
        await zedevent.delete()
    except Exception as e:
        print(e)
        
'''
# ================================================================================================ #
# =========================================ردود الخاص================================================= #
# ================================================================================================ #

@l313l.ar_cmd(
    pattern="تحميل صوت(?: |$)(.*)",
    command=("تحميل صوت", plugin_category),
    info={
        "header": "تحميـل الاغـاني مـن يوتيوب .. فيسبوك .. انستا .. الـخ عـبر الرابـط",
        "مثــال": ["{tr}تحميل صوت بالــرد ع رابــط", "{tr}تحميل صوت + رابــط"],
    },
)
async def download_audio(event):
    msg = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not msg and rmsg:
        msg = rmsg.text
    urls = extractor.find_urls(msg)
    if not urls:
        return await edit_or_reply(event, "**- قـم بادخــال رابـط مع الامـر او بالــرد ع رابـط ليتـم التحميـل**")
    zedevent = await edit_or_reply(event, "**⌔╎جـارِ التحميل انتظر قليلا ▬▭ ...**")
    reply_to_id = await reply_id(event)
    for url in urls:
        try:
            vid_data = YoutubeDL({"no-playlist": True, "cookiefile": get_cookies_file()}).extract_info(
                url, download=False
            )
        except ExtractorError:
            vid_data = {"title": url, "uploader": "Catuserbot", "formats": []}
        startTime = time()
        retcode = await _mp3Dl(url=url, starttime=startTime, uid="320")
        if retcode != 0:
            return await event.edit(str(retcode))
        _fpath = ""
        thumb_pic = None
        for _path in glob.glob(os.path.join(Config.TEMP_DIR, str(startTime), "*")):
            if _path.lower().endswith((".jpg", ".png", ".webp")):
                thumb_pic = _path
            else:
                _fpath = _path
        if not _fpath:
            return await edit_delete(zedevent, "__Unable to upload file__")
        await zedevent.edit(
            f"**╮ ❐ جـارِ التحضيـر للـرفع انتظـر ...𓅫╰**:\
            \n**{vid_data['title']}***"
        )
        attributes, mime_type = get_attributes(str(_fpath))
        ul = io.open(pathlib.Path(_fpath), "rb")
        if thumb_pic is None:
            thumb_pic = str(
                await pool.run_in_thread(download)(
                    await get_ytthumb(get_yt_video_id(url))
                )
            )
        uploaded = await event.client.fast_upload_file(
            file=ul,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d,
                    t,
                    zedevent,
                    startTime,
                    "trying to upload",
                    file_name=os.path.basename(pathlib.Path(_fpath)),
                )
            ),
        )
        ul.close()
        media = types.InputMediaUploadedDocument(
            file=uploaded,
            mime_type=mime_type,
            attributes=attributes,
            force_file=False,
            thumb=await event.client.upload_file(thumb_pic) if thumb_pic else None,
        )
        await event.client.send_file(
            event.chat_id,
            file=media,
            caption=f"<b>File Name : </b><code>{vid_data.get('title', os.path.basename(pathlib.Path(_fpath)))}</code>",
            supports_streaming=True,
            reply_to=reply_to_id,
            parse_mode="html",
        )
        for _path in [_fpath, thumb_pic]:
            os.remove(_path)
    await zedevent.delete()

@l313l.ar_cmd(
    pattern="تحميل فيديو(?: |$)(.*)",
    command=("تحميل فيديو", plugin_category),
    info={
        "header": "تحميـل مقـاطـع الفيـديــو مـن يوتيوب .. فيسبوك .. انستا .. الـخ عـبر الرابـط",
        "مثــال": [
            "{tr}تحميل فيديو بالــرد ع رابــط",
            "{tr}تحميل فيديو + رابــط",
        ],
    },
)
async def download_video(event):
    msg = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not msg and rmsg:
        msg = rmsg.text
    urls = extractor.find_urls(msg)
    if not urls:
        return await edit_or_reply(event, "**- قـم بادخــال رابـط مع الامـر او بالــرد ع رابـط ليتـم التحميـل**")
    zedevent = await edit_or_reply(event, "**⌔╎جـارِ التحميل انتظر قليلا ▬▭ ...**")
    reply_to_id = await reply_id(event)
    for url in urls:
        ytdl_data = await ytdl_down(zedevent, video_opts, url)
        if ytdl_down is None:
            return
        try:
            f = pathlib.Path("zed_ytv.mp4")
            print(f)
            zedthumb = pathlib.Path("zed_ytv.jpg")
            if not os.path.exists(zedthumb):
                zedthumb = pathlib.Path("zed_ytv.webp")
            if not os.path.exists(zedthumb):
                zedthumb = None
            await zedevent.edit(
                f"**╮ ❐ جـارِ التحضيـر للـرفع انتظـر ...𓅫╰**:\
                \n**{ytdl_data['title']}**"
            )
            ul = io.open(f, "rb")
            c_time = time()
            attributes, mime_type = await fix_attributes(
                f, ytdl_data, supports_streaming=True
            )
            uploaded = await event.client.fast_upload_file(
                file=ul,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d, t, zedevent, c_time, "Upload :", file_name=ytdl_data["title"]
                    )
                ),
            )
            ul.close()
            media = types.InputMediaUploadedDocument(
                file=uploaded,
                mime_type=mime_type,
                attributes=attributes,
            )
            await event.client.send_file(
                event.chat_id,
                file=media,
                reply_to=reply_to_id,
                caption=f'**- المقطــع :** `{ytdl_data["title"]}`',
                thumb=zedthumb,
            )
            os.remove(f)
            if zedthumb:
                os.remove(zedthumb)
        except TypeError:
            await asyncio.sleep(2)
    await event.delete()

from telethon import types, events
from telethon.extensions import html, markdown
from telethon.tl.functions.channels import JoinChannelRequest
import asyncio
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

# كلاس التحليل المخصص لدعم الإيموجيات البريميوم
class CustomParseMode:
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'html':
            text, entities = html.parse(text)
            for i, e in enumerate(entities):
                if isinstance(e, types.MessageEntityTextUrl):
                    if e.url.startswith('emoji/'):
                        document_id = int(e.url.split('/')[1])
                        entities[i] = types.MessageEntityCustomEmoji(
                            offset=e.offset,
                            length=e.length,
                            document_id=document_id
                        )
            return text, entities
        elif self.parse_mode == 'markdown':
            return markdown.parse(text)
        raise ValueError("Unsupported parse mode")

    @staticmethod
    def unparse(text, entities):
        return html.unparse(text, entities)

# إعدادات التحكم
youtube_settings = {
    'bot_username1': '@W60yBot',
    'bot_username2': '@BaarxXxbot',
    'channels': ['@B_a_r']
}

video_settings = {
    'bot_username': '@J_NO0bot',
    'channels': ['@arras_id']
}

# دالة التحقق من التفعيل
def is_youtube_enabled(chat_id=None):
    if chat_id:
        return gvarstatus(f"youtube_enabled_{chat_id}") == "True"
    return gvarstatus("youtube_enabled_private") == "True"

def is_video_enabled(chat_id=None):
    if chat_id:
        return gvarstatus(f"video_enabled_{chat_id}") == "True"
    return gvarstatus("video_enabled_private") == "True"

# ============================================
# أوامر التفعيل والتعطيل - للمطور فقط (ar_cmd)
# ============================================

@l313l.ar_cmd(pattern="تفعيل يوت$")
async def enable_youtube(event):
    if event.is_private:
        addgvar("youtube_enabled_private", "True")
        await event.edit("✓ تم تفعيل تحميل اليوتيوب في جميع الدردشات الخاصة")
    else:
        addgvar(f"youtube_enabled_{event.chat_id}", "True")
        await event.edit(f"✓ تم تفعيل تحميل اليوتيوب في هذه المجموعة")

@l313l.ar_cmd(pattern="تعطيل يوت$")
async def disable_youtube(event):
    if event.is_private:
        delgvar("youtube_enabled_private")
        await event.edit("✗ تم تعطيل تحميل اليوتيوب في الدردشات الخاصة")
    else:
        delgvar(f"youtube_enabled_{event.chat_id}")
        await event.edit(f"✗ تم تعطيل تحميل اليوتيوب في هذه المجموعة")

@l313l.ar_cmd(pattern="تفعيل فيديو$")
async def enable_video(event):
    if event.is_private:
        addgvar("video_enabled_private", "True")
        await event.edit("✓ تم تفعيل تحميل الفيديو في جميع الدردشات الخاصة")
    else:
        addgvar(f"video_enabled_{event.chat_id}", "True")
        await event.edit(f"✓ تم تفعيل تحميل الفيديو في هذه المجموعة")

@l313l.ar_cmd(pattern="تعطيل فيديو$")
async def disable_video(event):
    if event.is_private:
        delgvar("video_enabled_private")
        await event.edit("✗ تم تعطيل تحميل الفيديو في الدردشات الخاصة")
    else:
        delgvar(f"video_enabled_{event.chat_id}")
        await event.edit(f"✗ تم تعطيل تحميل الفيديو في هذه المجموعة")

# ============================================
# الأمر الرئيسي لتحميل اليوتيوب
# ============================================

@l313l.on(events.NewMessage(pattern=r'^(\.يوت|يوت)(?:\s|$)([\s\S]*)'))
async def yoot_auto_search(event):
    if not event.is_private and not event.pattern_match.group(1).startswith('.'):
        return
    
    if event.sender_id != l313l.uid:
        if event.is_private:
            if not is_youtube_enabled():
                return
        else:
            if not is_youtube_enabled(event.chat_id):
                return
    
    query = event.pattern_match.group(2).strip()
    if not query:
        return await event.reply("✧╎قم باضافـة إسـم للامـر ..\n⎉╎يوت + اسـم المقطـع الصـوتي")
    
    search_msg = await event.reply("**╮ جـارِ البحث عـن الإغـنيةة ... 🎧♥️ ╰**")
    
    try:
        for channel in youtube_settings['channels']:
            try:
                await event.client(JoinChannelRequest(channel))
                await asyncio.sleep(0.5)
            except:
                pass
        
        # محاولة مع البوت الأول
        try:
            async with event.client.conversation(youtube_settings['bot_username1'], timeout=30) as conv:
                await conv.send_message(f"يوت {query}")
                try:
                    first_response = await asyncio.wait_for(conv.get_response(), timeout=1)
                except asyncio.TimeoutError:
                    raise Exception("timeout")
                
                audio_response = await conv.get_response()
                
                if audio_response.media:
                    caption = (
                        f"<blockquote>\n"
                        f"<b>D𝑜𝑤𝑛𝑙𝑜𝑎𝑑 D𝑜𝑛𝑒 .</b>"
                        f'<a href="emoji/5890831539507302154">🎵</a>\n'
                        f"</blockquote>"
                        f"<b>↯︰By: @Lx5x5 .</b>"
                        f'<a href="emoji/5368338253868968009">🦅</a>\n'
                    )
                    
                    await event.client.send_file(
                        event.chat_id,
                        audio_response.media,
                        caption=caption,
                        parse_mode=CustomParseMode("html"),
                        reply_to=event.message.id
                    )
                    
                    await search_msg.delete()
                    return
                else:
                    raise Exception("no_media")
        
        except Exception as e:
            # محاولة مع البوت الثاني
            async with event.client.conversation(youtube_settings['bot_username2'], timeout=30) as conv:
                await conv.send_message(f"يوت {query}")
                first_response = await conv.get_response()
                audio_response = await conv.get_response()
                
                if audio_response.media:
                    caption = (
                        f"<blockquote>\n"
                        f"<b>D𝑜𝑤𝑛𝑙𝑜𝑎𝑑 D𝑜𝑛𝑒 .</b>"
                        f'<a href="emoji/5890831539507302154">🎵</a>\n'
                        f"</blockquote>"
                        f"<b>↯︰By: @Lx5x5 .</b>"
                        f'<a href="emoji/5368338253868968009">🦅</a>\n'
                    )
                    
                    await event.client.send_file(
                        event.chat_id,
                        audio_response.media,
                        caption=caption,
                        parse_mode=CustomParseMode("html"),
                        reply_to=event.message.id
                    )
                    
                    await search_msg.delete()
                else:
                    await search_msg.edit("**⎉╎لم يتم إيجاد نتيجة**")
        
    except asyncio.TimeoutError:
        await search_msg.edit("**• عذراً، فشل التحميل حاول لاحقاً،**")
    except Exception as e:
        await search_msg.edit(f"**⎉╎خطأ:** `{e}`")

# ============================================
# الأمر الرئيسي لتحميل الفيديو
# ============================================

@l313l.on(events.NewMessage(pattern=r'^(\.فيديو|فيديو)(?:\s|$)([\s\S]*)'))
async def video_auto_search(event):
    if not event.is_private and not event.pattern_match.group(1).startswith('.'):
        return
    
    if event.sender_id != l313l.uid:
        if event.is_private:
            if not is_video_enabled():
                return
        else:
            if not is_video_enabled(event.chat_id):
                return
    
    query = event.pattern_match.group(2).strip()
    if not query:
        return await event.reply("✧╎قم باضافـة إسـم للامـر ..\n⎉╎فيديو + اسـم المقطـع المرئي")
    
    search_msg = await event.client.send_message(
        event.chat_id,
        '<a href="emoji/5974332403890523746">️🎬</a>',
        parse_mode=CustomParseMode("html"),
        reply_to=event.message.id
    )
    
    try:
        for channel in video_settings['channels']:
            try:
                await event.client(JoinChannelRequest(channel))
                await asyncio.sleep(1)
            except:
                pass
        
        async with event.client.conversation(video_settings['bot_username'], timeout=30) as conv:
            await conv.send_message(f"تحميل {query}")
            first_response = await conv.get_response()
            video_response = await conv.get_response()
            
            if video_response.media:
                caption = (
                    f"<blockquote>\n"
                    f"<b>D𝑜𝑤𝑛𝑙𝑜𝑎𝑑 D𝑜𝑛𝑒 .</b>"
                    f'<a href="emoji/5886584791809134461">🎬</a>\n'
                    f"</blockquote>"
                    f"<b>↯︰By: @Lx5x5 .</b>"
                    f'<a href="emoji/5368338253868968009">🦅</a>\n'
                )
                
                await event.client.send_file(
                    event.chat_id,
                    video_response.media,
                    caption=caption,
                    parse_mode=CustomParseMode("html"),
                    reply_to=event.message.id
                )
                
                await search_msg.delete()
            else:
                await search_msg.edit("**⎉╎لم يتم إيجاد نتيجة**")
        
    except asyncio.TimeoutError:
        await search_msg.edit("**⎉╎انتهت المهلة في انتظار الرد**")
    except Exception as e:
        await search_msg.edit(f"**⎉╎خطأ:** `{e}`")
