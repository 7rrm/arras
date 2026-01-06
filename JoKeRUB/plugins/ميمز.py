
import asyncio
import random
import re
import json
import base64
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from asyncio.exceptions import TimeoutError
from telethon import events
from ..sql_helper.memes_sql import get_link, add_link, delete_link, BASE, SESSION, AljokerLink
from telethon.errors.rpcerrorlist import YouBlockedUserError
#ياقائم آل محمد
from JoKeRUB import l313l
from ..helpers.utils import reply_id
plugin_category = "tools"
# الي يخمط ويكول من كتابتي الا امه انيجه وقد اعذر من انذر
    
@l313l.on(admin_cmd(pattern="حالتي ?(.*)"))
async def _(event):
    await event.edit("**- يتم التاكد من حالتك اذا كنت محظور او لا**")
    async with bot.conversation("@SpamBot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=178220800)
            )
            await conv.send_message("/start")
            response = await response
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit("** اولا الغي حظر @SpamBot وحاول مجددا**")
            return
        await event.edit(f"- {response.message.message} .")

@l313l.on(admin_cmd(pattern="الاغنية ?(.*)"))
async def _(event):
    "To reverse search music by bot."
    if not event.reply_to_msg_id:
        return await event.edit("**▾∮ يجب الرد على الاغنيه اولا**")
    reply_message = await event.get_reply_message()
    chat = "@auddbot"
    try:
        async with event.client.conversation(chat) as conv:
            try:
                await event.edit("**▾∮ يتم التعرف على الاغنية انتظر**")
                start_msg = await conv.send_message("/start")
                response = await conv.get_response()
                send_audio = await conv.send_message(reply_message)
                check = await conv.get_response()
                if not check.text.startswith("Audio received"):
                    return await event.edit(
                        "**▾∮ يجب ان يكون حجم الاغنيه من 5 الى 10 ثواني **."
                    )
                await event.edit("- انتظر قليلا")
                result = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("```Mohon buka blokir (@auddbot) dan coba lagi```")
                return
            namem = f"**الأغنية : **{result.text.splitlines()[0]}\
        \n\n**التفاصيـل : **{result.text.splitlines()[2]}"
            await event.edit(namem)
            await event.client.delete_messages(
                conv.chat_id,
                [start_msg.id, send_audio.id, check.id, result.id, response.id],
            )
    except TimeoutError:
        return await event.edit("***حدث خطا ما حاول مجددا**")
        
import random
from telethon import events

# متغير لتخزين حالة التفعيل
song_enabled = False

# معرف المستخدم الخاص بك
my_id = 5427469031  # استبدل YOUR_USER_ID بمعرفك الفعلي

# أمر تفعيل غنيلي
@l313l.on(events.NewMessage(pattern="^\.تفعيل غنيلي$"))
async def enable_song(event):
    global song_enabled
    
    # التحقق من أن المرسل هو أنت
    if event.sender_id == my_id:
        song_enabled = True
        await event.reply("تم تفعيل غنيلي بنجاح! الآن البوت سيرد على أي شخص يكتب `.غنيلي`.")
    # إذا كان المرسل شخصًا آخر، لا يتم الرد بأي شيء
    else:
        return

# أمر إلغاء تفعيل غنيلي
@l313l.on(events.NewMessage(pattern="^\.ايقاف غنيلي$"))
async def disable_song(event):
    global song_enabled
    
    # التحقق من أن المرسل هو أنت
    if event.sender_id == my_id:
        song_enabled = False
        await event.reply("تم إلغاء تفعيل غنيلي بنجاح! الآن البوت لن يرد على الآخرين عند كتابة `.غنيلي`.")
    # إذا كان المرسل شخصًا آخر، لا يتم الرد بأي شيء
    else:
        return

# تعريف الحدث للرد على أي شخص يكتب .غنيلي
@l313l.on(events.NewMessage(pattern="^\.غنيلي$"))
async def send_song(event):
    global song_enabled
    
    # إذا كان المرسل هو البوت نفسه (أنت)، يرد دائمًا
    if event.sender_id == my_id:
        pass  # يستمر في تنفيذ الكود
    # إذا كان المرسل شخصًا آخر، يرد فقط إذا كان غنيلي مفعلًا
    elif not song_enabled:
        return
    
    try:
        # رقم عشوائي بين 1 و 385
        rl = random.randint(5, 141)
        
        # رابط الملف العشوائي من القناة
        url = f"https://t.me/Kii_ti/{rl}"
        
        # إرسال الملف مع تعليق
        await event.client.send_file(
            event.chat_id,
            url,
            caption="- تم اختيارها لك .",
            parse_mode="html"
        )
        
        # حذف الأمر الأصلي (اختياري)
        await event.delete()
    
    except Exception as e:
        # في حالة حدوث خطأ، إرسال رسالة تفيد بذلك
        await event.reply(f"حدث خطأ أثناء إرسال الغناء: {str(e)}")

import random
from telethon import events

# متغير لتخزين حالة التفعيل
poem_enabled = False

# معرف المستخدم الخاص بك
my_id = 5427469031  # استبدل YOUR_USER_ID بمعرفك الفعلي

# أمر تفعيل الشعر
@l313l.on(events.NewMessage(pattern="^\.تفعيل شعر$"))
async def enable_poem(event):
    global poem_enabled
    
    # التحقق من أن المرسل هو أنت
    if event.sender_id == my_id:
        poem_enabled = True
        await event.reply("تم تفعيل الشعر بنجاح! الآن البوت سيرد على أي شخص يكتب `.شعر`.")
    # إذا كان المرسل شخصًا آخر، لا يتم الرد بأي شيء
    else:
        return

# أمر إلغاء تفعيل الشعر
@l313l.on(events.NewMessage(pattern="^\.ايقاف شعر$"))
async def disable_poem(event):
    global poem_enabled
    
    # التحقق من أن المرسل هو أنت
    if event.sender_id == my_id:
        poem_enabled = False
        await event.reply("تم إلغاء تفعيل الشعر بنجاح! الآن البوت لن يرد على الآخرين عند كتابة `.شعر`.")
    # إذا كان المرسل شخصًا آخر، لا يتم الرد بأي شيء
    else:
        return

# تعريف الحدث للرد على أي شخص يكتب .شعر
@l313l.on(events.NewMessage(pattern="^\.شعر$"))
async def send_poem(event):
    global poem_enabled
    
    # إذا كان المرسل هو البوت نفسه (أنت)، يرد دائمًا
    if event.sender_id == my_id:
        pass  # يستمر في تنفيذ الكود
    # إذا كان المرسل شخصًا آخر، يرد فقط إذا كان الشعر مفعلًا
    elif not poem_enabled:
        return
    
    try:
        # رقم عشوائي بين 4 و67
        rl = random.randint(4, 67)
        
        # رابط الملف العشوائي من القناة
        url = f"https://t.me/Lx1x2/{rl}"
        
        # إرسال الملف كرد على رسالة المستخدم
        await event.client.send_file(
            event.chat_id,
            url,
            caption="- تم اختيارها لك .",
            reply_to=event.id,  # الرد على رسالة المستخدم
            parse_mode="html"
        )
        
        # حذف الأمر الأصلي (اختياري)

    
    except Exception as e:
        # في حالة حدوث خطأ، إرسال رسالة تفيد بذلك
        await event.reply(f"حدث خطأ أثناء إرسال الشعر: {str(e)}")

import random
from telethon import events

# متغير لتخزين حالة التفعيل
remix_enabled = False

# معرف المستخدم الخاص بك
my_id = 5427469031  # استبدل YOUR_USER_ID بمعرفك الفعلي

# أمر تفعيل الريمكس
@l313l.on(events.NewMessage(pattern="^\.تفعيل ريمكس$"))
async def enable_remix(event):
    global remix_enabled
    
    # التحقق من أن المرسل هو أنت
    if event.sender_id == my_id:
        remix_enabled = True
        await event.reply("تم تفعيل الريمكس بنجاح! الآن البوت سيرد على أي شخص يكتب `.ريمكس`.")
    # إذا كان المرسل شخصًا آخر، لا يتم الرد بأي شيء
    else:
        return

# أمر إلغاء تفعيل الريمكس
@l313l.on(events.NewMessage(pattern="^\.ايقاف ريمكس$"))
async def disable_remix(event):
    global remix_enabled
    
    # التحقق من أن المرسل هو أنت
    if event.sender_id == my_id:
        remix_enabled = False
        await event.reply("تم إلغاء تفعيل الريمكس بنجاح! الآن البوت لن يرد على الآخرين عند كتابة `.ريمكس`.")
    # إذا كان المرسل شخصًا آخر، لا يتم الرد بأي شيء
    else:
        return

# تعريف الحدث للرد على أي شخص يكتب .ريمكس
@l313l.on(events.NewMessage(pattern="^\.ريمكس$"))
async def send_remix(event):
    global remix_enabled
    
    # إذا كان المرسل هو البوت نفسه (أنت)، يرد دائمًا
    if event.sender_id == my_id:
        pass  # يستمر في تنفيذ الكود
    # إذا كان المرسل شخصًا آخر، يرد فقط إذا كان الريمكس مفعلًا
    elif not remix_enabled:
        return
    
    try:
        # رقم عشوائي بين 4 و70
        rl = random.randint(4, 70)
        
        # رابط الملف العشوائي من القناة
        url = f"https://t.me/rem77e/{rl}"
        
        # إرسال الملف الصوتي كرد على رسالة المستخدم
        await event.client.send_file(
            event.chat_id,
            url,
            caption="- تم اختيار هذا الريمكس لك .",
            reply_to=event.id,  # الرد على رسالة المستخدم
            parse_mode="html"
        )
        
        # حذف الأمر الأصلي (اختياري)
    except Exception as e:
        # في حالة حدوث خطأ، إرسال رسالة تفيد بذلك
        await event.reply(f"حدث خطأ أثناء إرسال الريمكس: {str(e)}")


@l313l.on(admin_cmd(outgoing=True, pattern=r"ميمز (\S+) (.+)"))
async def Hussein(event):
    url = event.pattern_match.group(1)
    lMl10l = event.pattern_match.group(2)
    add_link(lMl10l, url)
    await event.edit(f"**᯽︙ تم اضافة البصمة {lMl10l} بنجاح ✓ **")
    joker = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    joker = Get(joker)
    try:
        await event.client(joker)
    except BaseException:
        pass

@l313l.on(admin_cmd(outgoing=True, pattern="?(.*)"))
async def Hussein(event):
    lMl10l = event.pattern_match.group(1)
    Joker = await reply_id(event)
    url = get_link(lMl10l)
    if url:
        await event.client.send_file(event.chat_id, url, parse_mode="html", reply_to=Joker)
        await event.delete()
        joker = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
        joker = Get(joker)
        try:
            await event.client(joker)
        except BaseException:
            pass

@l313l.ar_cmd(pattern="ازالة(?:\s|$)([\s\S]*)")
async def delete_aljoker(event):
    lMl10l = event.pattern_match.group(1)
    delete_link(lMl10l)
    await event.edit(f"**᯽︙ تم حذف البصمة '{lMl10l}' بنجاح ✓**")
    joker = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    joker = Get(joker)
    try:
        await event.client(joker)
    except BaseException:
        pass

@l313l.on(admin_cmd(outgoing=True, pattern="قائمة الميمز"))
async def list_aljoker(event):
    links = SESSION.query(AljokerLink).all()
    if links:
        message = "**᯽︙ قائمة تخزين اوامر الميمز:**\n"
        for link in links:
            message += f"- البصمة : .`{link.key}`\n"
    else:
        message = "**᯽︙ لاتوجد بصمات ميمز مخزونة حتى الآن**"
    await event.edit(message)
    joker = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    joker = Get(joker)
    try:
        await event.client(joker)
    except BaseException:
        pass
@l313l.on(admin_cmd(outgoing=True, pattern="ازالة_البصمات"))
async def delete_all_aljoker(event):
    SESSION.query(AljokerLink).delete()
    await event.edit("**᯽︙ تم حذف جميع بصمات الميمز من القائمة **")
    joker = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    joker = Get(joker)
    try:
        await event.client(joker)
    except BaseException:
        pass
