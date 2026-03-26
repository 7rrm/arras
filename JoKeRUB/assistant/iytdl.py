""" Download Youtube Video / Audio in a User friendly interface """
# --------------------------- #
#   Modded ytdl by code-rgb   #
# --------------------------- #

import asyncio
import glob
import io
import os
import re
from pathlib import Path
from time import time

import ujson
from telethon import Button, types
from telethon.errors import BotResponseTimeoutError
from telethon.events import CallbackQuery
from telethon.utils import get_attributes
from wget import download

from JoKeRUB import l313l

from ..Config import Config
from ..core import check_owner, pool
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import post_to_telegraph, progress, reply_id
from ..helpers.functions.utube import (
    _mp3Dl,
    _tubeDl,
    download_button,
    get_choice_by_id,
    get_ytthumb,
    yt_search_btns,
)
from ..plugins import BOTLOG_CHATID

LOGS = logging.getLogger(__name__)
BASE_YT_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = re.compile(
    r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})"
)
PATH = "./JoKeRUB/cache/ytsearch.json"
plugin_category = "البوت"


@l313l.ar_cmd(
    pattern="بحث(?:\s|$)([\s\S]*)",
    command=("بحث", plugin_category),
    info={
        "header": "ytdl with inline buttons.",
        "description": "To search and download youtube videos by inline buttons.",
        "usage": "{tr}iytdl [URL / Text] or [Reply to URL / Text]",
    },
)
async def iytdl_inline(event):
    "ytdl with inline buttons."
    print("[DEBUG] ========== بدء البحث ==========")
    print(f"[DEBUG] Config.TG_BOT_USERNAME = {Config.TG_BOT_USERNAME}")
    
    reply = await event.get_reply_message()
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    input_url = None
    if input_str:
        input_url = (input_str).strip()
    elif reply and reply.text:
        input_url = (reply.text).strip()
    
    print(f"[DEBUG] input_url = {input_url}")
    
    if not input_url:
        print("[DEBUG] لا يوجد رابط او نص")
        return await edit_delete(event, "**- بالـرد ع رابـط او كتـابة نص مـع الامـر**")
    
    zedevent = await edit_or_reply(event, f"**⌔╎جـارِ البحث في اليوتيوب عـن:** `'{input_url}'`")
    flag = True
    cout = 0
    results = None
    
    while flag:
        try:
            print(f"[DEBUG] محاولة البحث #{cout+1} عن: ytdl {input_url}")
            results = await event.client.inline_query(
                Config.TG_BOT_USERNAME, f"ytdl {input_url}"
            )
            print(f"[DEBUG] results = {results}")
            print(f"[DEBUG] عدد النتائج = {len(results) if results else 0}")
            flag = False
        except BotResponseTimeoutError as e:
            print(f"[DEBUG] BotResponseTimeoutError: {e}")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"[DEBUG] خطأ غير متوقع: {e}")
            print(f"[DEBUG] نوع الخطأ: {type(e)}")
            flag = False
        cout += 1
        if cout > 5:
            print("[DEBUG] تم الوصول للحد الأقصى 5 محاولات")
            flag = False
    
    if results:
        print("[DEBUG] تم العثور على نتائج، جاري العرض...")
        await zedevent.delete()
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    else:
        print("[DEBUG] لم يتم العثور على نتائج")
        await zedevent.edit("**⌔╎عـذراً .. لم اجد اي نتائـج**")


@l313l.tgbot.on(
    CallbackQuery(
        data=re.compile(b"^ytdl_download_(.*)_([\d]+|mkv|mp4|mp3)(?:_(a|v))?")
    )
)
@check_owner
async def ytdl_download_callback(c_q: CallbackQuery):  # sourcery no-metrics
    print("[DEBUG] ========== بدء التحميل ==========")
    yt_code = (
        str(c_q.pattern_match.group(1).decode("UTF-8"))
        if c_q.pattern_match.group(1) is not None
        else None
    )
    choice_id = (
        str(c_q.pattern_match.group(2).decode("UTF-8"))
        if c_q.pattern_match.group(2) is not None
        else None
    )
    downtype = (
        str(c_q.pattern_match.group(3).decode("UTF-8"))
        if c_q.pattern_match.group(3) is not None
        else None
    )
    print(f"[DEBUG] yt_code = {yt_code}")
    print(f"[DEBUG] choice_id = {choice_id}")
    print(f"[DEBUG] downtype = {downtype}")
    
    if str(choice_id).isdigit():
        choice_id = int(choice_id)
        if choice_id == 0:
            print("[DEBUG] عرض أزرار التحميل")
            await c_q.answer("🔄  جـارِ ...", alert=False)
            await c_q.edit(buttons=(await download_button(yt_code)))
            return
    startTime = time()
    choice_str, disp_str = get_choice_by_id(choice_id, downtype)
    print(f"[DEBUG] choice_str = {choice_str}")
    print(f"[DEBUG] disp_str = {disp_str}")
    
    media_type = "فيديو" if downtype == "v" else "مقطع صوتي"
    callback_continue = f"جار تحميل {media_type} يرجى الانتظار"
    callback_continue += f"\n\nصيغـة الملـف : {disp_str}"
    await c_q.answer(callback_continue, alert=True)
    upload_msg = await c_q.client.send_message(
        BOTLOG_CHATID, "**⌔╎جـارِ الـرفـع ...**"
    )
    yt_url = BASE_YT_URL + yt_code
    await c_q.edit(
        f"<b>⌔╎جـارِ تحميـل 🎧 {media_type} ...</b>\n\n  <a href={yt_url}>  <b>⌔╎الـرابـط 📎</b></a>\n🎚 <b>⌔╎الصيغـه </b> : {disp_str}",
        parse_mode="html",
    )
    
    print(f"[DEBUG] بدء التحميل من: {yt_url}")
    if downtype == "v":
        retcode = await _tubeDl(url=yt_url, starttime=startTime, uid=choice_str)
    else:
        retcode = await _mp3Dl(url=yt_url, starttime=startTime, uid=choice_str)
    
    print(f"[DEBUG] retcode = {retcode}")
    
    if retcode != 0:
        print(f"[DEBUG] فشل التحميل، retcode = {retcode}")
        return await upload_msg.edit(str(retcode))
    
    _fpath = ""
    thumb_pic = None
    print(f"[DEBUG] البحث في المسار: {os.path.join(Config.TEMP_DIR, str(startTime), '*')}")
    for _path in glob.glob(os.path.join(Config.TEMP_DIR, str(startTime), "*")):
        print(f"[DEBUG] ملف موجود: {_path}")
        if _path.lower().endswith((".jpg", ".png", ".webp")):
            thumb_pic = _path
            print(f"[DEBUG] صورة مصغرة: {thumb_pic}")
        else:
            _fpath = _path
            print(f"[DEBUG] ملف الفيديو/الصوت: {_fpath}")
    
    if not _fpath:
        print("[DEBUG] لم يتم العثور على الملف!")
        await edit_delete(upload_msg, "**⌔╎اووبـس .. لم يتـم إيجـاد المطلـوب ؟!**")
        return
    
    if not thumb_pic:
        print(f"[DEBUG] جلب صورة مصغرة للفيديو: {yt_code}")
        thumb_pic = str(await pool.run_in_thread(download)(await get_ytthumb(yt_code)))
    
    print("[DEBUG] بدء رفع الملف...")
    attributes, mime_type = get_attributes(str(_fpath))
    ul = io.open(Path(_fpath), "rb")
    uploaded = await c_q.client.fast_upload_file(
        file=ul,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(
                d,
                t,
                c_q,
                startTime,
                "trying to upload",
                file_name=os.path.basename(Path(_fpath)),
            )
        ),
    )
    ul.close()
    media = types.InputMediaUploadedDocument(
        file=uploaded,
        mime_type=mime_type,
        attributes=attributes,
        force_file=False,
        thumb=await c_q.client.upload_file(thumb_pic) if thumb_pic else None,
    )
    uploaded_media = await c_q.client.send_file(
        BOTLOG_CHATID,
        file=media,
        caption=f"<b>⌔╎الاسـم : </b><code>{os.path.basename(Path(_fpath))}</code>",
        parse_mode="html",
    )
    await upload_msg.delete()
    await c_q.edit(
        text=f"<b>⌔╎الـرابـط 📎: </b> <a href={yt_url}><b>{os.path.basename(Path(_fpath))}</b></a>",
        file=uploaded_media.media,
        parse_mode="html",
    )
    print("[DEBUG] ========== انتهى التحميل بنجاح ==========")


@l313l.tgbot.on(
    CallbackQuery(data=re.compile(b"^ytdl_(listall|back|next|detail)_([a-z0-9]+)_(.*)"))
)
@check_owner
async def ytdl_callback(c_q: CallbackQuery):
    print("[DEBUG] ========== معاينة ==========")
    choosen_btn = (
        str(c_q.pattern_match.group(1).decode("UTF-8"))
        if c_q.pattern_match.group(1) is not None
        else None
    )
    data_key = (
        str(c_q.pattern_match.group(2).decode("UTF-8"))
        if c_q.pattern_match.group(2) is not None
        else None
    )
    page = (
        str(c_q.pattern_match.group(3).decode("UTF-8"))
        if c_q.pattern_match.group(3) is not None
        else None
    )
    print(f"[DEBUG] choosen_btn = {choosen_btn}")
    print(f"[DEBUG] data_key = {data_key}")
    print(f"[DEBUG] page = {page}")
    
    if not os.path.exists(PATH):
        print(f"[DEBUG] الملف غير موجود: {PATH}")
        return await c_q.answer(
            "عملية البحث غير دقيقة يرجى اختيار عنوان صحيح وحاول مجددا",
            alert=True,
        )
    
    with open(PATH) as f:
        view_data = ujson.load(f)
    search_data = view_data.get(data_key)
    total = len(search_data) if search_data is not None else 0
    print(f"[DEBUG] total = {total}")
    
    if total == 0:
        print("[DEBUG] لا توجد بيانات بحث")
        return await c_q.answer(
            "يرجى البحث مرة اخرى لم يتم العثور على نتائج دقيقة", alert=True
        )
    
    if choosen_btn == "back":
        index = int(page) - 1
        del_back = index == 1
        await c_q.answer()
        back_vid = search_data.get(str(index))
        await c_q.edit(
            text=back_vid.get("message"),
            file=await get_ytthumb(back_vid.get("video_id")),
            buttons=yt_search_btns(
                del_back=del_back,
                data_key=data_key,
                page=index,
                vid=back_vid.get("video_id"),
                total=total,
            ),
            parse_mode="html",
        )
    elif choosen_btn == "next":
        index = int(page) + 1
        if index > total:
            return await c_q.answer("هذا كل ما يمكنني عرضه", alert=True)
        await c_q.answer()
        front_vid = search_data.get(str(index))
        await c_q.edit(
            text=front_vid.get("message"),
            file=await get_ytthumb(front_vid.get("video_id")),
            buttons=yt_search_btns(
                data_key=data_key,
                page=index,
                vid=front_vid.get("video_id"),
                total=total,
            ),
            parse_mode="html",
        )
    elif choosen_btn == "listall":
        await c_q.answer("العرض تغير الى :  📜  اللستة", alert=False)
        list_res = "".join(
            search_data.get(vid_s).get("list_view") for vid_s in search_data
        )

        telegraph = await post_to_telegraph(
            f"يتم عرض {total} من الفيديوهات على اليوتيوب حسب طلبك ...",
            list_res,
        )
        await c_q.edit(
            file=await get_ytthumb(search_data.get("1").get("video_id")),
            buttons=[
                (
                    Button.url(
                        "↗️  اضغط للتحميل",
                        url=telegraph,
                    )
                ),
                (
                    Button.inline(
                        "📰  عرض التفاصيل",
                        data=f"ytdl_detail_{data_key}_{page}",
                    )
                ),
            ],
        )
    else:  # Detailed
        index = 1
        await c_q.answer("تم تغيير العرض الى:  📰  التفاصيل", alert=False)
        first = search_data.get(str(index))
        await c_q.edit(
            text=first.get("message"),
            file=await get_ytthumb(first.get("video_id")),
            buttons=yt_search_btns(
                del_back=True,
                data_key=data_key,
                page=index,
                vid=first.get("video_id"),
                total=total,
            ),
            parse_mode="html",
        )
