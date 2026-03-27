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
    
    # تحديد الدردشة المستهدفة
    if event.is_private:
        target_chat = event.sender_id
    else:
        target_chat = event.chat_id
    
    zedevent = await edit_or_reply(event, f"**⌔╎جـارِ البحث في اليوتيوب عـن:** `'{input_url}'`")
    
    # البحث المباشر وعرض النتائج بدون Inline
    try:
        from ..helpers.functions.utube import ytsearch_data, result_formatter, get_ytthumb
        from youtubesearchpython import VideosSearch
        
        # البحث في اليوتيوب
        search = VideosSearch(input_url, limit=10)
        resp = (search.result()).get("result")
        
        if not resp:
            return await zedevent.edit("**⌔╎عـذراً .. لم اجد اي نتائـج**")
        
        outdata = await result_formatter(resp)
        key_ = rand_key()
        ytsearch_data.store_(key_, outdata)
        
        buttons = [
            [
                Button.inline(
                    f"1 / {len(outdata)}",
                    data=f"ytdl_next_{key_}_1_{target_chat}_{reply_to_id}",
                ),
                Button.inline(
                    "القائمـة 📜",
                    data=f"ytdl_listall_{key_}_1_{target_chat}_{reply_to_id}",
                ),
                Button.inline(
                    "⬇️  تحميـل",
                    data=f'ytdl_download_{outdata[1]["video_id"]}_0_{target_chat}_{reply_to_id}',
                ),
            ]
        ]
        
        caption = outdata[1]["message"]
        photo = await get_ytthumb(outdata[1]["video_id"])
        
        # إرسال النتيجة مباشرة
        await zedevent.delete()
        await event.client.send_file(
            target_chat,
            photo,
            caption=caption,
            buttons=buttons,
            parse_mode="html",
            reply_to=reply_to_id
        )
        
    except Exception as e:
        LOGS.error(f"Search error: {e}")
        await zedevent.edit(f"**⌔╎عـذراً .. حدث خطأ:** `{e}`")

@l313l.tgbot.on(
    CallbackQuery(data=re.compile(b"^ytdl_download_(.*)_0$"))
)
@check_owner
async def ytdl_download_callback(c_q: CallbackQuery):
    yt_code = c_q.pattern_match.group(1).decode("UTF-8")
    yt_url = BASE_YT_URL + yt_code

    # الحصول على chat_id من الرسالة
    if hasattr(c_q, 'message') and hasattr(c_q.message, 'chat_id'):
        chat_id = c_q.message.chat_id
    else:
        chat_id = c_q.chat_id or c_q.sender_id

    # التأكد من أن chat_id ليس معرف الحساب العادي
    if chat_id == l313l.uid:
        chat_id = c_q.sender_id
        LOGS.info(f"Changed chat_id from saved messages to user: {chat_id}")

    LOGS.info(f"Download requested - Final chat_id: {chat_id}")

    await c_q.answer("🔄 جـارِ التحميل...", alert=False)

    try:
        await c_q.edit("**🔄 جـارِ طلب التحميل من البوت الخارجي...**")
    except:
        pass

    try:
        # استخدام l313l للتواصل مع البوت الخارجي
        async with l313l.conversation("@W60yBot", timeout=60) as conv:
            await conv.send_message(f"يوت {yt_url}")
            try:
                await asyncio.wait_for(conv.get_response(), timeout=1)
            except:
                pass
            
            audio_response = await conv.get_response()
            
            if audio_response and audio_response.media:
                caption = (
                    f"<blockquote>\n"
                    f"<b>D𝑜𝑤𝑛𝑙𝑜𝑎𝑑 D𝑜𝑛𝑒 .</b>"
                    f'<a href="emoji/5890831539507302154">🎵</a>\n'
                    f"</blockquote>"
                    f"<b>↯︰By: @Lx5x5 .</b>"
                    f'<a href="emoji/5368338253868968009">🦅</a>\n'
                )
                
                # إرسال الملف
                await l313l.send_file(
                    chat_id,
                    audio_response.media,
                    caption=caption,
                    parse_mode="html"
                )
                
                try:
                    await c_q.edit("✅ **تم التحميل بنجاح**", buttons=[])
                except:
                    pass
            else:
                await l313l.send_message(chat_id, "❌ **فشل التحميل**\nلم يتم استلام ملف")
                
    except asyncio.TimeoutError:
        await l313l.send_message(chat_id, "❌ **انتهت المهلة**\nالبوت لم يستجب")
    except Exception as e:
        LOGS.error(f"Download error: {e}")
        await l313l.send_message(chat_id, f"❌ **خطأ:** `{str(e)[:100]}`")

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


