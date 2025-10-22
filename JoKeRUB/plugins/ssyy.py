import os
import requests
import yt_dlp
from youtube_search import YoutubeSearch
from telethon import events
from telethon.tl.types import DocumentAttributeAudio

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id
from . import l313l


def get_cookies_file():
    folder_path = f"{os.getcwd()}/karar"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    return cookie_txt_file
    
# إعدادات yt-dlp السريعة
ydl_opts = {
    "format": "bestaudio[ext=m4a]/bestaudio/best",
    "outtmpl": "%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
    "geo_bypass": True,
    "cookiefile": get_cookies_file,  # يمكن إضافة كوكيز إذا احتجت
}

@l313l.ar_cmd(pattern="(بحث|تحميل|تنزيل|يوت|yt)(?:\s|$)([\s\S]*)")
async def song_download(event):
    "تحميل الأغاني من اليوتيوب بسرعة"
    query = event.pattern_match.group(2)
    reply = await event.get_reply_message()
    
    if not query and reply:
        query = reply.text
    if not query:
        return await edit_or_reply(event, "**⎉╎قم بإدخال اسم الأغنية للبحث ...**")
    
    zedevent = await edit_or_reply(event, "**╮ جـارِ البحث ؏ـن المقطـٓع الصٓوتـي... 🎧♥️╰**")
    
    try:
        # البحث السريع
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            return await zedevent.edit("**⎉╎لم يتم العثور على نتائج ... حاول مرة أخرى**")
        
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        duration = results[0]["duration"]
        
        # تحميل الصورة المصغرة
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        
    except Exception as e:
        return await zedevent.edit(f"**⎉╎خطأ في البحث:** `{str(e)}`")
    
    await zedevent.edit("**╮ ❐ جـارِ التحميل ▬▭ . . . ╰**")
    
    try:
        # التحميل السريع
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        
        # تحويل المدة إلى ثواني
        duration_seconds = 0
        if ':' in duration:
            parts = duration.split(':')
            if len(parts) == 2:
                duration_seconds = int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:
                duration_seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        
        await zedevent.edit("**╮ ❐ جـارِ الرفـع ▬▬ . . 🎧♥️╰**")
        
        # إرسال الملف
        await event.client.send_file(
            event.chat_id,
            audio_file,
            caption=f"**🎵 الأغنية:** `{title}`\n**⏱ المدة:** `{duration}`\n**👤 بواسطة:** {event.sender.mention}",
            thumb=thumb_name,
            attributes=[
                DocumentAttributeAudio(
                    duration=duration_seconds,
                    performer="@mmmsc",
                    title=title
                )
            ],
            reply_to=event.reply_to_msg_id
        )
        
        await zedevent.delete()
        
    except Exception as e:
        await zedevent.edit(f"**⎉╎خطأ في التحميل:** `{str(e)}`")
    
    finally:
        # تنظيف الملفات المؤقتة
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
            if os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as e:
            print(f"Error cleaning files: {e}")

# إصدار محسن بإعدادات أسرع
@l313l.ar_cmd(pattern="اغنيه(?:\s|$)([\s\S]*)")
async def fast_song_download(event):
    "تحميل الأغاني بسرعة فائقة"
    query = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    
    if not query and reply:
        query = reply.text
    if not query:
        return await edit_or_reply(event, "**⎉╎قم بإدخال اسم الأغنية ...**")
    
    zedevent = await edit_or_reply(event, "**🎧╎جاري البحث عن الأغنية...**")
    
    # إعدادات أسرع
    fast_ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "outtmpl": "temp_audio.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "geo_bypass": True,
        "http_chunk_size": 10485760,  # 10MB chunks للسرعة
    }
    
    try:
        # البحث
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            return await zedevent.edit("**❌╎لم أعثر على أي نتائج**")
        
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]
        duration = results[0]["duration"]
        
        await zedevent.edit("**⬇️╎جاري التحميل...**")
        
        # التحميل
        with yt_dlp.YoutubeDL(fast_ydl_opts) as ydl:
            ydl.download([link])
        
        # البحث عن الملف المحمل
        audio_file = None
        for file in os.listdir():
            if file.startswith("temp_audio") and file.endswith(".m4a"):
                audio_file = file
                break
        
        if not audio_file:
            return await zedevent.edit("**❌╎فشل في تحميل الملف**")
        
        # تحويل المدة
        duration_seconds = 0
        if ':' in duration:
            parts = duration.split(':')
            if len(parts) == 2:
                duration_seconds = int(parts[0]) * 60 + int(parts[1])
        
        await zedevent.edit("**⬆️╎جاري الرفع...**")
        
        # إرسال الملف
        await event.client.send_file(
            event.chat_id,
            audio_file,
            caption=f"**🎵 {title}**\n**⏱ {duration}**\n**👤 {event.sender.mention}**",
            attributes=[
                DocumentAttributeAudio(
                    duration=duration_seconds,
                    performer="ZThon Music",
                    title=title[:30]
                )
            ],
            reply_to=event.reply_to_msg_id
        )
        
        await zedevent.delete()
        
    except Exception as e:
        await zedevent.edit(f"**❌╎خطأ:** `{str(e)}`")
    
    finally:
        # تنظيف
        try:
            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)
        except:
            pass

__mod_name__ = "اليوتيوب"
__help__ = """
**أوامر تحميل الأغاني:**

◍ `.بحث` + اسم الأغنية
◍ `.تحميل` + اسم الأغنية  
◍ `.اغنيه` + اسم الأغنية (الأسرع)
◍ `.يوت` + اسم الأغنية

**مثال:**
◍ `.بحث اغنية الحب`
◍ `.اغنيه Fair Trade Drake`
"""
