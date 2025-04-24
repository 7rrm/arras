import asyncio
import aiohttp
import os
import shutil
import time
from bs4 import BeautifulSoup
from datetime import datetime
from telethon.utils import guess_extension
from urllib.parse import urlencode

from . import l313l
from ..Config import Config

ZELZAL_APP_ID = "6e65179ed1d879f3d905e28ef8803625"


@l313l.ar_cmd(pattern="صور (.*)")
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("**╮ ❐ جـاري البحث عن الصـور  ...𓅫╰**")
    query = event.pattern_match.group(1)
    download_dir = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, query)
    
    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)
    
    input_url = "https://bots.shrimadhavuk.me/search/"
    headers = {"USER-AGENT": "UseTGBot"}
    image_paths = []
    
    try:
        async with aiohttp.ClientSession() as session:
            data = {
                "q": query,
                "app_id": ZELZAL_APP_ID,
                "p": "GoogleImages"
            }
            response = await session.get(input_url, params=data, headers=headers)
            result = await response.json()
            
            for item in result.get("results", [])[:10]:  # الحد الأقصى 10 صور
                image_url = item.get("url")
                if not image_url:
                    continue
                
                try:
                    async with session.get(image_url) as img_response:
                        # معالجة نوع المحتوى بشكل آمن
                        content_type = img_response.headers.get("Content-Type", "image/jpeg")
                        ext = guess_extension(content_type) or ".jpg"
                        filename = f"{int(time.time())}{ext}"
                        filepath = os.path.join(download_dir, filename)
                        
                        with open(filepath, "wb") as f:
                            f.write(await img_response.read())
                        image_paths.append(filepath)
                except Exception as e:
                    print(f"Failed to download image: {e}")
                    continue
    
        if not image_paths:
            await event.edit(f"**- لم أتمكن من إيجاد صور لـ {query}**")
            return
            
        await event.reply(file=image_paths, parse_mode="html", force_document=True)
        
    except Exception as e:
        await event.edit(f"**حدث خطأ: {str(e)}**")
        return
    finally:
        # تنظيف الملفات المؤقتة
        for file in image_paths:
            try:
                os.remove(file)
            except:
                pass
        shutil.rmtree(download_dir, ignore_errors=True)
        
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(f"**- اكتمل البحث عن {query} في {ms} ثانية ✓**", link_preview=False)
        await asyncio.sleep(5)
        await event.delete()


@l313l.ar_cmd(pattern="خلفيات (.*)")
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("**╮ ❐ جـاري البحث عن خلفيـات  ...𓅫╰**")
    query = event.pattern_match.group(1)
    download_dir = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, query)
    
    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)
    
    input_url = "https://bots.shrimadhavuk.me/search/"
    headers = {"USER-AGENT": "UseTGBot"}
    image_paths = []
    
    try:
        async with aiohttp.ClientSession() as session:
            data = {
                "q": query + " خلفيات HD",  # إضافة HD للبحث عن خلفيات عالية الجودة
                "app_id": ZELZAL_APP_ID,
                "p": "GoogleImages"
            }
            response = await session.get(input_url, params=data, headers=headers)
            result = await response.json()
            
            for item in result.get("results", [])[:10]:  # الحد الأقصى 10 صور
                image_url = item.get("url")
                if not image_url:
                    continue
                
                try:
                    async with session.get(image_url) as img_response:
                        # معالجة نوع المحتوى بشكل آمن
                        content_type = img_response.headers.get("Content-Type", "image/jpeg")
                        ext = guess_extension(content_type) or ".jpg"
                        filename = f"{int(time.time())}{ext}"
                        filepath = os.path.join(download_dir, filename)
                        
                        with open(filepath, "wb") as f:
                            f.write(await img_response.read())
                        image_paths.append(filepath)
                except Exception as e:
                    print(f"Failed to download image: {e}")
                    continue
    
        if not image_paths:
            await event.edit(f"**- لم أتمكن من إيجاد خلفيات لـ {query}**")
            return
            
        await event.reply(file=image_paths, parse_mode="html", force_document=True)
        
    except Exception as e:
        await event.edit(f"**حدث خطأ: {str(e)}**")
        return
    finally:
        # تنظيف الملفات المؤقتة
        for file in image_paths:
            try:
                os.remove(file)
            except:
                pass
        shutil.rmtree(download_dir, ignore_errors=True)
        
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(f"**- اكتمل البحث عن خلفيات {query} في {ms} ثانية ✓**", link_preview=False)
        await asyncio.sleep(5)
        await event.delete()
