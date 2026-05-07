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
from telethon.tl.types import DocumentAttributeAudio

LOGS = logging.getLogger(__name__)
BASE_YT_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = re.compile(
    r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})"
)
PATH = "./JoKeRUB/cache/ytsearch.json"
plugin_category = "البوت"



@l313l.ar_cmd(
    pattern="بحث(?:\s|$)([\s\S]*)",
    command=("يوت", plugin_category),
    info={
        "header": "ytdl with inline buttons.",
        "description": "To search and download youtube videos by inline buttons.",
        "usage": "{tr}iytdl [URL / Text] or [Reply to URL / Text]",
    },
)
async def iytdl_inline(event):
    "ytdl with inline buttons."
    reply = await event.get_reply_message()
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    input_url = None
    if input_str:
        input_url = (input_str).strip()
    elif reply and reply.text:
        input_url = (reply.text).strip()
    if not input_url:
        return await edit_delete(event, "**- بالـرد ع رابـط او كتـابة نص مـع الامـر**")
    zedevent = await edit_or_reply(event, f"**⌔╎جـارِ البحث في اليوتيوب عـن:** `'{input_url}'`")
    flag = True
    cout = 0
    results = None
    while flag:
        try:
            results = await event.client.inline_query(
                Config.TG_BOT_USERNAME, f"ytdl {input_url}"
            )
            flag = False
        except BotResponseTimeoutError:
            await asyncio.sleep(2)
        cout += 1
        if cout > 5:
            flag = False
    if results:
        await zedevent.delete()
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    else:
        await zedevent.edit("**⌔╎عـذراً .. لم اجد اي نتائـج**")


@l313l.tgbot.on(
    CallbackQuery(data=re.compile(b"^ytdl_download_(.*)_audio$"))
)
@check_owner
async def ytdl_download_audio(c_q: CallbackQuery):
    """تحميل الصوت"""
    yt_code = c_q.pattern_match.group(1).decode("UTF-8")
    
    await c_q.answer("🔄 جـارِ التحميل...", alert=False)
    
    try:
        await c_q.edit("**╮ جـارِ التجهيز ... 🎧 ╰**")
    except:
        pass
    
    try:
        import requests
        
        API_KEY = "60177503-3647-4d6c-be9c-cd0b47a80a6b"
        api_url = f"https://muntazer.online/yt/m4a={API_KEY}=https://youtu.be/{yt_code}"
        
        def fetch_api():
            resp = requests.get(api_url, timeout=60)
            if resp.status_code == 200:
                return resp.json()
            return None
        
        result = await asyncio.get_event_loop().run_in_executor(None, fetch_api)
        
        if result and result.get("status") == "ok":
            link = result.get("link")
            
            if link:
                parts = link.strip('/').split('/')
                channel_username = parts[-2]
                message_id = int(parts[-1])
                
                await c_q.edit("**📥 جـارِ استلام الملف...**")
                
                s_msg = await c_q.client.get_messages(channel_username, ids=message_id)
                
                if s_msg and s_msg.media:
                    caption = (
                        f"<blockquote>"
                        f"<b>D𝑜𝑤𝑛𝑙𝑜𝑎𝑑 D𝑜𝑛𝑒 .</b>"
                        f'<tg-emoji emoji-id="5890831539507302154">🎵</tg-emoji>'
                        f"</blockquote>"
                    )
                    
                    buttons = [
                        [Button.url("‹ : المـطـور : ›", "https://t.me/lx5x5", style="primary")],
                    ]
                    
                    uploaded_media = await c_q.client.send_file(
                        BOTLOG_CHATID,
                        s_msg.media,
                        caption=f"<b>🎵 {yt_code}</b>",
                        parse_mode="html"
                    )
                    
                    await c_q.edit(
                        text=caption,
                        file=uploaded_media.media,
                        parse_mode="html",
                        buttons=buttons
                    )
                    
                else:
                    await c_q.edit("❌ **فشل التحميل**\nلم يتم العثور على الملف")
            else:
                await c_q.edit("❌ **فشل التحميل**\nلا يوجد رابط")
        else:
            await c_q.edit("❌ **فشل التحميل**\nAPI لم يستجب")
            
    except Exception as e:
        LOGS.error(f"Download error: {e}")
        await c_q.edit(f"❌ **خطأ:** `{str(e)[:100]}`")

@l313l.tgbot.on(
    CallbackQuery(data=re.compile(b"^ytdl_download_(.*)_video$"))
)
@check_owner
async def ytdl_download_video(c_q: CallbackQuery):
    """تحميل الفيديو"""
    yt_code = c_q.pattern_match.group(1).decode("UTF-8")
    
    await c_q.answer("🔄 جـارِ التحميل...", alert=False)
    
    try:
        await c_q.edit("**╮ جـارِ التجهيز ... 🎬 ╰**")
    except:
        pass
    
    try:
        import requests
        
        API_KEY = "60177503-3647-4d6c-be9c-cd0b47a80a6b"
        api_url = f"https://muntazer.online/tuob/mp4={API_KEY}=https://youtu.be/{yt_code}"
        
        def fetch_api():
            resp = requests.get(api_url, timeout=60)
            if resp.status_code == 200:
                return resp.json()
            return None
        
        result = await asyncio.get_event_loop().run_in_executor(None, fetch_api)
        
        if result and result.get("status") == "ok":
            link = result.get("link")
            
            if link:
                parts = link.strip('/').split('/')
                channel_username = parts[-2]
                message_id = int(parts[-1])
                
                await c_q.edit("**📥 جـارِ استلام الملف...**")
                
                s_msg = await c_q.client.get_messages(channel_username, ids=message_id)
                
                if s_msg and s_msg.media:
                    caption = (
                        f"<blockquote>"
                        f"<b>D𝑜𝑤𝑛𝑙𝑜𝑎𝑑 D𝑜𝑛𝑒 .</b>"
                        f'<tg-emoji emoji-id="5886584791809134461">🎬</tg-emoji>'
                        f"</blockquote>"
                    )
                    
                    buttons = [
                        [Button.url("‹ : المـطـور : ›", "https://t.me/lx5x5", style="primary")],
                    ]
                    
                    uploaded_media = await c_q.client.send_file(
                        BOTLOG_CHATID,
                        s_msg.media,
                        caption=f"<b>🎬 {yt_code}</b>",
                        parse_mode="html"
                    )
                    
                    await c_q.edit(
                        text=caption,
                        file=uploaded_media.media,
                        parse_mode="html",
                        buttons=buttons
                    )
                    
                else:
                    await c_q.edit("❌ **فشل التحميل**\nلم يتم العثور على الملف")
            else:
                await c_q.edit("❌ **فشل التحميل**\nلا يوجد رابط")
        else:
            await c_q.edit("❌ **فشل التحميل**\nAPI لم يستجب")
            
    except Exception as e:
        LOGS.error(f"Download error: {e}")
        await c_q.edit(f"❌ **خطأ:** `{str(e)[:100]}`")

@l313l.tgbot.on(
    CallbackQuery(data=re.compile(b"^ytdl_(listall|back|next|detail)_([a-z0-9]+)_(.*)"))
)
@check_owner
async def ytdl_callback(c_q: CallbackQuery):
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
    if not os.path.exists(PATH):
        return await c_q.answer(
            "عملية البحث غير دقيقة يرجى اختيار عنوان صحيح وحاول مجددا",
            alert=True,
        )
    with open(PATH) as f:
        view_data = ujson.load(f)
    search_data = view_data.get(data_key)
    total = len(search_data) if search_data is not None else 0
    if total == 0:
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
                    Button.inline(
                        "‹ : رجــوع : ›",
                        data=f"ytdl_detail_{data_key}_{page}",
                        style="danger"
                    )
                ),
                (
                    Button.url(
                        "‹ : النتائـج : ›",
                        url=telegraph,
                        style="danger"
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

              
