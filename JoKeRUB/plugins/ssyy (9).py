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
import shutil
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

from telethon import events
from telethon.tl import types
from telethon.utils import get_attributes
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError, ChatSendMediaForbiddenError
from telethon.tl.functions.contacts import UnblockRequest as unblock

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


@l313l.ar_cmd(pattern="بنترست(?: |$)(.*)")
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
            caption=f"<b>✧╎المقطع : </b><code>{vid_data.get('title', os.path.basename(pathlib.Path(_fpath)))}</code>",
            supports_streaming=True,
            reply_to=reply_to_id,
            parse_mode="html",
        )
        for _path in [_fpath, thumb_pic]:
            os.remove(_path)
    await zedevent.delete()


# ================================================================================================ #
# =========================================ساوند كلاود================================================= #
# ================================================================================================ #

def remove_if_exists(path): #Code by T.me/zzzzl1l
    if os.path.exists(path):
        os.remove(path)

from ..sql_helper.globals import addgvar, delgvar, gvarstatus
import os
import requests
import yt_dlp
from youtube_search import YoutubeSearch
from telethon import events
import random
import glob
import time

# دالة الحصول على ملف الكوكيز
def get_cookies_file():
    folder_path = f"{os.getcwd()}/karar"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the cookies folder.")
    return random.choice(txt_files)

# إعدادات التحكم
search_settings = {
    'admin_id': l313l.uid    # أي دي المطور
}

# مسار الصورة المصغرة الثابتة
DEFAULT_THUMB = "l313l/razan/resources/start/ssyy.JPEG"

def is_search_enabled(chat_id=None):
    if chat_id:
        return gvarstatus(f"search_enabled_{chat_id}") == "True"
    return gvarstatus("search_enabled_private") == "True"

@l313l.on(events.NewMessage(pattern=r'^\.تفعيل بحث$'))
async def enable_search(event):
    if event.sender_id != search_settings['admin_id']:
        return await event.delete()
    
    if event.is_private:
        addgvar("search_enabled_private", "True")
        await event.reply("✓ تم تفعيل البحث في جميع الدردشات الخاصة")
    else:
        addgvar(f"search_enabled_{event.chat_id}", "True")
        await event.reply(f"✓ تم تفعيل البحث في هذه المجموعة")

@l313l.on(events.NewMessage(pattern=r'^\.تعطيل بحث$'))
async def disable_search(event):
    if event.sender_id != search_settings['admin_id']:
        return await event.delete()
    
    if event.is_private:
        delgvar("search_enabled_private")
        await event.reply("✗ تم تعطيل البحث في الدردشات الخاصة")
    else:
        delgvar(f"search_enabled_{event.chat_id}")
        await event.reply(f"✗ تم تعطيل البحث في هذه المجموعة")

@l313l.on(events.NewMessage(pattern=r'^\.بحث(?: |$)(.*)'))
async def search_song(event):
    # التحقق من الصلاحيات
    if event.sender_id == search_settings['admin_id']:
        pass  # المطور مسموح له دائماً
    elif event.is_private:
        if not is_search_enabled():
            return
    else:
        if not is_search_enabled(event.chat_id):
            return
    
    query = event.pattern_match.group(1).strip()
    if not query:
        if event.is_private:  # فقط في الدردشات الخاصة
            return await event.reply("╮ ❐ يرجى تحديد اسم الأغنية للبحث ...𓅫╰")
        return
    
    msg = await event.reply("**╮ جـارِ البحث عـن الإغـنيةة ... 🎧♥️ ╰**")
    
    try:
        # الحصول على ملف الكوكيز
        cookies_file = get_cookies_file()
        
        # إنشاء مجلد التحميل إذا لم يكن موجوداً
        os.makedirs("downloads", exist_ok=True)
        
        # إعدادات yt-dlp مع الكوكيز
        ydl_opts = {
            "format": "bestaudio[ext=m4a]",
            "socket_timeout": 5,
            "http_chunk_size": 5242880,
            "noplaylist": True,
            "extract_flat": True,
            "fragment_retries": 2,
            "retries": 2,
            "quiet": True,
            "no_warnings": True,
            "geo_bypass": True,
            "cookiefile": cookies_file,
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "postprocessors": [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }
        
        # البحث في اليوتيوب
        results = YoutubeSearch(query, max_results=1).to_dict()
        
        if not results:
            return await msg.edit("╮ ❐ لم يتم العثور على نتائج !!╰**")
        
        video_url = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        duration = results[0]["duration"]
        
        await msg.edit("**╮ ❐ جـارِ التحميل ▬▭ . . . ╰**")
        
        # عملية التحميل
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            # تغيير الامتداد إلى .m4a
            filename = os.path.splitext(filename)[0] + ".m4a"
            
            # التحقق من وجود الملف
            if not os.path.exists(filename):
                raise FileNotFoundError("Failed to download the file.")
        
        # عملية الرفع مع الصورة المصغرة الثابتة
        await msg.edit("╮ ❐ جـارِ الرفـع ▬▬ . . 🎧♥️╰")
        await event.client.send_file(
            event.chat_id,
            filename,
            caption=f"**S𝑜𝑛𝑔N𝑎𝑚𝑒 ⥂** `{title}`\n**D𝑢𝑟𝑎𝑡𝑖𝑜𝑛:-** `ٔ{duration}`",
            thumb=DEFAULT_THUMB if os.path.exists(DEFAULT_THUMB) else None,
            reply_to=event.id,
            attributes=[types.DocumentAttributeAudio(
                duration=int(duration.split(':')[0])*60 + int(duration.split(':')[1]),
                title=title,
                performer="YouTube"
            )]
        )
            
    except Exception as e:
        await msg.edit(f"**❌ حدث خطأ:**\n`{str(e)}`")
    finally:
        try:
            if 'filename' in locals() and os.path.exists(filename):
                os.remove(filename)
        except:
            pass
        await msg.delete()
    



@l313l.ar_cmd(pattern="فيديو(?: |$)(.*)")
async def _(event): #Code by T.me/zzzzl1l
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "**✧╎قم باضافـة إسـم للامـر ..**\n**✧╎فيديو + اسـم الفيديـو**")
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
        caption=f"**✧╎البحث :** `{title}`",
        thumb=preview,
        supports_streaming=True,
    )
    try:
        remove_if_exists(file_name)
        await zedevent.delete()
    except Exception as e:
        print(e)



async def get_ytthumb(video_id):
    thumb_path = os.path.join(Config.TEMP_DIR, f"{video_id}.jpg")
    for quality in ['maxresdefault', 'hqdefault', 'mqdefault', 'sddefault']:
        thumb_url = f"https://i.ytimg.com/vi/{video_id}/{quality}.jpg"
        try:
            await download_file(thumb_url, thumb_path)
            if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 0:
                return thumb_path
        except:
            continue
    return None

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
    
    audio_opts = {
        'format': 'bestaudio/best',
        'addmetadata': True,
        'writethumbnail': True,
        'prefer_ffmpeg': True,
        'geo_bypass': True,
        'nocheckcertificate': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': os.path.join(Config.TEMP_DIR, '%(id)s.%(ext)s'),
        'quiet': True,
        'logtostderr': False,
        'no_warnings': True,
        'cookiefile': get_cookies_file(),
        'ignoreerrors': True,
        'retries': 3,
    }
    
    for url in urls:
        try:
            # إنشاء مجلد مؤقت لكل عملية تحميل
            download_folder = os.path.join(Config.TEMP_DIR, str(time()))
            os.makedirs(download_folder, exist_ok=True)
            
            # تعديل مسار الإخراج ليكون في المجلد المؤقت
            audio_opts['outtmpl'] = os.path.join(download_folder, '%(id)s.%(ext)s')
            
            with YoutubeDL(audio_opts) as ydl:
                vid_data = ydl.extract_info(url, download=True)
                video_id = vid_data.get('id', url.split('=')[-1])
                
                # البحث عن الملف المحمل
                audio_file = None
                thumb_file = None
                for f in os.listdir(download_folder):
                    if f.endswith('.mp3'):
                        audio_file = os.path.join(download_folder, f)
                    elif f.endswith(('.jpg', '.webp')):
                        thumb_file = os.path.join(download_folder, f)
                
                if not audio_file:
                    return await edit_delete(zedevent, "**حدث خطأ أثناء تحويل الصوت**")
                
                await zedevent.edit(f"**╮ ❐ جـارِ التحضيـر للـرفع انتظـر ...𓅫╰**:\n**{vid_data.get('title', url)}**")
                
                # الحصول على صورة المصغرة (مع معالجة الأخطاء)
                if not thumb_file:
                    thumb_file = await get_ytthumb(video_id)
                
                # رفع الملف
                attributes, mime_type = get_attributes(audio_file)
                ul = io.open(audio_file, 'rb')
                
                uploaded = await event.client.fast_upload_file(
                    file=ul,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(
                            d, t, zedevent, time(),
                            "trying to upload",
                            file_name=os.path.basename(audio_file),
                        )
                    ),
                )
                ul.close()
                
                # رفع الصورة المصغرة إذا وجدت
                uploaded_thumb = None
                if thumb_file and os.path.exists(thumb_file):
                    try:
                        uploaded_thumb = await event.client.upload_file(thumb_file)
                    except:
                        pass
                
                media = types.InputMediaUploadedDocument(
                    file=uploaded,
                    mime_type=mime_type,
                    attributes=attributes,
                    force_file=False,
                    thumb=uploaded_thumb,
                )
                
                await event.client.send_file(
                    event.chat_id,
                    file=media,
                    caption=f"<b>File Name : </b><code>{vid_data.get('title', os.path.basename(audio_file))}</code>",
                    supports_streaming=True,
                    reply_to=reply_to_id,
                    parse_mode="html",
                )
                
                # تنظيف الملفات المؤقتة
                shutil.rmtree(download_folder, ignore_errors=True)
                
        except Exception as e:
            await zedevent.edit(f"**حدث خطأ أثناء التحميل:**\n`{str(e)}`")
            shutil.rmtree(download_folder, ignore_errors=True)
            continue
    
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

@l313l.ar_cmd(pattern="انستا(?: |$)(.*)")
async def zelzal_insta(event):
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply:
        link = reply.text
    if not link:
        return await edit_delete(event, "**- ارسـل (.انستا) + رابـط او بالـرد ع رابـط**", 10)
    if "instagram.com" not in link:
        return await edit_delete(event, "**- احتـاج الـى رابــط من الانستـا .. للتحميــل ؟!**", 10)
    if link.startswith("https://instagram"):
        link = link.replace("https://instagram", "https://www.instagram")
    if link.startswith("http://instagram"):
        link = link.replace("http://instagram", "http://www.instagram")
    if "/reel/" in link:
        cap_zzz = f"<b>✧╎تم تحميـل مقطـع انستـا (ريلـز) .. بنجـاح ☑️\n ⌔╎الرابـط 🖇: <code>{link}</code>\n ✧╎تم التحميـل بواسطـة سورس آراس </b>"
    elif "/tv/" in link:
        cap_zzz = f"<b>✧╎تم تحميـل بث انستـا (Tv) .. بنجـاح ☑️\n ⌔╎الرابـط 🖇: <code>{link}</code>\n ✧╎تم التحميـل بواسطـة سورس آراس </b>"
    elif "/stories/" in link:
        cap_zzz = f"<b>✧╎تم تحميـل ستـوري انستـا .. بنجـاح ☑️\n ⌔╎الرابـط 🖇: <code>{link}</code>\n ✧╎تم التحميـل بواسطـة سورس آراس </b>"
    else:
        cap_zzz = f"<b>✧╎تم تحميـل مقطـع انستـا .. بنجـاح ☑️\n ⌔╎الرابـط 🖇: <code>{link}</code>\n ✧╎تم التحميـل بواسطـة آراس </b>"
    chat = "@story_repost_bot"
    zed = await edit_or_reply(event, "** ⌔╎جـارِ التحميل من الانستـا .. انتظر قليلا ▬▭**")
    async with borg.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link)
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(2036153627, max_id=0, just_clear=True))
        except YouBlockedUserError:
            await l313l(unblock("story_repost_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link)
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(2036153627, max_id=0, just_clear=True))
            

@l313l.ar_cmd(pattern="تيك(?: |$)(.*)")
async def zelzal_insta(event):
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply:
        link = reply.text
    if not link:
        return await edit_delete(event, "**- ارسـل (.تيك) + رابـط او بالـرد ع رابـط**", 10)
    if "tiktok.com" not in link:
        return await edit_delete(event, "**- احتـاج الـى رابــط من تيـك تـوك .. للتحميــل ؟!**", 10)
    cap_zzz = f"<b>✧╎تم تحميـل مـن تيـك تـوك .. بنجـاح ☑️\n ⌔╎الرابـط 🖇: <code>{link}</code>\n✧╎تم التحميـل بواسطـة سورس آراس </b>"
    chat = "@downloader_tiktok_bot"
    zed = await edit_or_reply(event, "**✧╎جـارِ التحميل من تيـك تـوك .. انتظر قليلا ▬▭**")
    async with borg.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link)
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(1332941342, max_id=0, just_clear=True))
        except YouBlockedUserError:
            await l313l(unblock("downloader_tiktok_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link)
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(1332941342, max_id=0, just_clear=True))
