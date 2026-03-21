
import asyncio
from telethon import events
from JoKeRUB import l313l

plugin_category = "misc"
  
@l313l.ar_cmd(
    pattern="حفظ كامل(?: |$)(.*)",
    command=("حفظ كامل", plugin_category),
    info={
        "header": "نقل الرسائل من رسالة محددة إلى الأحدث في القناة.",
        "description": "يحفظ الرسائل بدءًا من الرابط المحدد وحتى الأحدث، مع تجنب الرسائل الأقدم.",
        "usage": "{tr}حفظ_كامل <رابط الرسالة>",
    },
)
async def transfer_channel(event):
    input_str = event.pattern_match.group(1).strip()
    if not input_str:
        return await event.edit("**✎┊ يرجى تحديد رابط الرسالة!**")

    await event.edit("**✎┊ جاري التحقق من الرسالة، يرجى الانتظار...**")

    try:
        # الحصول على كائن الرسالة من الرابط
        if "t.me/" in input_str:
            parts = input_str.split("/")
            msg_id = int(parts[-1]) if parts[-1].isdigit() else None
            if not msg_id:
                return await event.edit("**✎┊ الرابط غير صالح! تأكد من وجود ID الرسالة في الرابط.**")

            chat_entity = "/".join(parts[:-1])
            chat = await l313l.get_entity(chat_entity)
            start_msg = await l313l.get_messages(chat, ids=msg_id)
            
            if not start_msg:
                return await event.edit("**✎┊ لا يمكن العثور على الرسالة!**")
        else:
            return await event.edit("**✎┊ الرابط غير صالح! استخدم رابطًا مثل `https://t.me/القناة/123`**")

        target_chat = event.chat_id  # الدردشة الهدف
        transferred_messages = set()  # لتجنب تكرار الرسائل
        success = 0

        # جلب الرسائل الأحدث (التي بعد الرسالة المحددة)
        async for msg in l313l.iter_messages(chat, min_id=start_msg.id - 1, reverse=True):
            if msg.id in transferred_messages:
                continue

            await asyncio.sleep(5)  # تقليل خطر الحظر

            try:
                # 1. معالجة الألبومات (الوسائط المجمعة)
                if hasattr(msg, "grouped_id") and msg.grouped_id:
                    media_files = []
                    caption = msg.text if msg.text else ""
                    
                    # جمع كل الوسائط في الألبوم
                    async for m in l313l.iter_messages(chat, min_id=msg.id - 5, max_id=msg.id + 5):
                        if hasattr(m, "grouped_id") and m.grouped_id == msg.grouped_id and m.media:
                            media_path = await l313l.download_media(m.media)
                            media_files.append(media_path)
                            transferred_messages.add(m.id)

                    # إرسال الألبوم كرسالة واحدة
                    if media_files:
                        await l313l.send_file(
                            target_chat,
                            media_files,
                            caption=caption,
                        )
                        success += 1

                # 2. معالجة الرسائل العادية (صورة واحدة/نص)
                else:
                    if msg.text and not msg.media:
                        await l313l.send_message(target_chat, msg.text)
                        success += 1
                    elif msg.media:
                        caption = msg.text if msg.text else ""
                        media_path = await l313l.download_media(msg.media)
                        await l313l.send_file(
                            target_chat,
                            media_path,
                            caption=caption,
                        )
                        success += 1
                    transferred_messages.add(msg.id)

            except Exception as e:
                await event.reply(f"**✎┊ خطأ في حفظ الرسالة {msg.id}: {str(e)}**")

        await event.edit(f"**✎┊ تم نقل {success} رسالة بنجاح بدءًا من الرسالة المحددة! ✅**")
    except Exception as e:
        await event.edit(f"**✎┊ حدث خطأ: {str(e)}**")


import asyncio
from telethon import events
from JoKeRUB import l313l

plugin_category = "misc"

@l313l.ar_cmd(
    pattern="احفظ(?: |$)(.*)",
    command=("احفظ", plugin_category),
    info={
        "header": "جلب رسالة من قناة مقيدة وحفظها في الدردشة الحالية",
        "description": "يحفظ الرسالة من القنوات المقيدة عن طريق التحميل وإعادة الإرسال",
        "usage": "{tr}جلب <رابط الرسالة>",
    },
)
async def bypass_restriction(event):
    input_str = event.pattern_match.group(1).strip()
    if not input_str:
        return await event.edit("**✪╎يُرجى تحديد رابـط الرسـالة!**")

    await event.edit("**✪╎جـاري جلـب الرسـالة من القنـاة المقيدة...**")

    try:
        # الحصول على كائن الرسالة من الرابط
        if "t.me/" in input_str:
            parts = input_str.split("/")
            msg_id = int(parts[-1]) if parts[-1].isdigit() else None
            if not msg_id:
                return await event.edit("**✪╎الرابـط غيـر صالـح! تأكـد من وجـود ID الرسـالة في الرابـط.**")

            chat_entity = "/".join(parts[:-1])
            chat = await l313l.get_entity(chat_entity)
            msg = await l313l.get_messages(chat, ids=msg_id)
            
            if not msg:
                return await event.edit("**✪╎لا يمكـن العثـور على الرسـالة!**")
        else:
            return await event.edit("**✪╎الرابـط غيـر صالـح! استخـدم رابـطًا مثـل `https://t.me/القنـاة/123`**")

        target_chat = event.chat_id  # الدردشة الحالية

        try:
            # إذا كانت الرسالة نصية فقط
            if msg.text and not msg.media:
                await l313l.send_message(target_chat, msg.text)
                await event.edit("**✪╎تم جلـب النـص بنجـاح ✅**")
                return

            # إذا كانت الرسالة تحتوي على ميديا
            if msg.media:
                # تحميل الميديا
                media_path = await l313l.download_media(msg.media)
                caption = msg.text if msg.text else ""
                
                # تحديد نوع الميديا
                if hasattr(msg.media, "photo"):
                    await l313l.send_file(target_chat, media_path, caption=caption)
                elif hasattr(msg.media, "document"):
                    await l313l.send_file(target_chat, media_path, caption=caption)
                elif hasattr(msg.media, "webpage"):
                    await l313l.send_message(target_chat, msg.text)
                else:
                    await l313l.send_file(target_chat, media_path, caption=caption)
                
                await event.edit("**✪╎تم جلـب المحتـوى بنجـاح ✅**")
                return

        except Exception as e:
            await event.edit(f"**✪╎خطـأ في جلـب الرسـالة: {str(e)}**")
            return

    except Exception as e:
        await event.edit(f"**✪╎حـدث خطـأ: {str(e)}**")


"""
`Credits` @amnd33p
from ..helpers.utils import _format
Modified by @Zed-Thon
"""

import io
import traceback
from datetime import datetime

import requests
from selenium import webdriver
from validators.url import url

from . import l313l

from ..Config import Config
from ..core.managers import edit_or_reply
from . import reply_id

plugin_category = "العروض"


@l313l.ar_cmd(
    pattern="(سكرين|ss) ([\s\S]*)",
    command=("سكرين", plugin_category),
    info={
        "header": "لـ اخذ لقطـة شاشـه لـ المواقـع",
        "الاستخـدام": "{tr}سكرين + رابـط",
        "مثــال": "{tr}سكرين https://github.com",
    },
)
async def _(event):
    "لـ اخذ لقطـة شاشـه لـ المواقـع"
    if Config.CHROME_BIN is None:
        return await edit_or_reply(
            event, "Need to install Google Chrome. Module Stopping."
        )
    zzevent = await edit_or_reply(event, "**- جـارِ اخـذ لقطـة شاشـه للصفحـه...**")
    start = datetime.now()
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--headless")
        # https://stackoverflow.com/a/53073789/4723940
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = Config.CHROME_BIN
        await event.edit("**- جـارِ الاتصـال بجـوجل كـروم ...**")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        cmd = event.pattern_match.group(1)
        input_str = event.pattern_match.group(2)
        inputstr = input_str
        rmsg = await event.get_reply_message()
        if not inputstr and rmsg:
            inputstr = rmsg.text
        if not inputstr and not rmsg:
            return await zzevent.edit("**- قـم بادخــال رابـط مع الامـر او بالــرد ع رابـط ...**")
        if cmd == "سكرين":
            caturl = url(inputstr)
            if not inputstr:
                return await zzevent.edit("**- قـم بادخــال رابـط مع الامـر او بالــرد ع رابـط ...**")
            if not caturl:
                inputstr = f"http://{input_str}"
                caturl = url(inputstr)
            if not caturl:
                return await zzevent.edit("**- عـذراً .. الرابـط المدخـل ليس رابـط مدعـوم ؟!**")
        if cmd == "ss":
            inputstr = f"https://www.google.com/search?q={input_str}"
        driver.get(inputstr)
        await zzevent.edit("**- جـارِ رفـع لقطـة شاشـه للصفحـه...**")
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
        )
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
        )
        driver.set_window_size(width + 100, height + 100)
        # Add some pixels on top of the calculated dimensions
        # for good measure to make the scroll bars disappear
        im_png = driver.get_screenshot_as_png()
        # saves screenshot of entire page
        await zzevent.edit("**- تم إغـلاق جوجـل كـروم ✓**")
        driver.close()
        message_id = await reply_id(event)
        end = datetime.now()
        ms = (end - start).seconds
        hmm = f"**⎉╎المـوقع : **{input_str} \n**⎉╎ الوقت المستغـرق : {ms} ثانيـه**\n**⎉╎تم اخـذ لقطـة شاشـه .. بنجـاح ✓**"
        await zzevent.delete()
        with io.BytesIO(im_png) as out_file:
            out_file.name = f"{input_str}.PNG"
            await event.client.send_file(
                event.chat_id,
                out_file,
                caption=hmm,
                force_document=True,
                reply_to=message_id,
                allow_cache=False,
                silent=True,
            )
    except Exception:
        await zzevent.edit(f"`{traceback.format_exc()}`")


@l313l.ar_cmd(
    pattern="لقطه ([\s\S]*)",
    command=("لقطه", plugin_category),
    info={
        "header": "لـ اخذ لقطـة شاشـه لـ المواقـع",
        "الوصـف": "For functioning of this command you need to set SCREEN_SHOT_LAYER_ACCESS_KEY var",
        "الاستخـدام": "{tr}لقطه + رابـط",
        "مثــال": "{tr}لقطه https://github.com",
    },
)
async def _(event):
    "لـ اخذ لقطـة شاشـه لـ المواقـع"
    start = datetime.now()
    message_id = await reply_id(event)
    if Config.SCREEN_SHOT_LAYER_ACCESS_KEY is None:
        return await edit_or_reply(
            event,
            "`Need to get an API key from https://screenshotlayer.com/product and need to set it SCREEN_SHOT_LAYER_ACCESS_KEY !`",
        )
    zzevent = await edit_or_reply(event, "**- جـارِ اخـذ لقطـة شاشـه للصفحـه...**")
    sample_url = "https://api.screenshotlayer.com/api/capture?access_key={}&url={}&fullpage={}&viewport={}&format={}&force={}"
    input_str = event.pattern_match.group(1)
    inputstr = input_str
    caturl = url(inputstr)
    if not caturl:
        inputstr = f"http://{input_str}"
        caturl = url(inputstr)
    if not caturl:
        return await zzevent.edit("**- عـذراً .. الرابـط المدخـل ليس رابـط مدعـوم ؟!**")
    response_api = requests.get(
        sample_url.format(
            Config.SCREEN_SHOT_LAYER_ACCESS_KEY, inputstr, "1", "2560x1440", "PNG", "1"
        )
    )
    # https://stackoverflow.com/a/23718458/4723940
    contentType = response_api.headers["content-type"]
    end = datetime.now()
    ms = (end - start).seconds
    hmm = f"**⎉╎المـوقع : **{input_str} \n**⎉╎ الوقت المستغـرق : {ms} ثانيـه**\n**⎉╎تم اخـذ لقطـة شاشـه .. بنجـاح ✓**"
    if "image" in contentType:
        with io.BytesIO(response_api.content) as screenshot_image:
            screenshot_image.name = "screencapture.png"
            try:
                await event.client.send_file(
                    event.chat_id,
                    screenshot_image,
                    caption=hmm,
                    force_document=True,
                    reply_to=message_id,
                )
                await zzevent.delete()
            except Exception as e:
                await zzevent.edit(str(e))
    else:
        await zzevent.edit(f"`{response_api.text}`")
