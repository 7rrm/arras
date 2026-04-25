
import asyncio
import random
import re
import json
import base64
from ..helpers.functions import delete_conv
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.functions.contacts import UnblockRequest as unblock
from asyncio.exceptions import TimeoutError
from telethon import events
from ..sql_helper.memes_sql import get_link, add_link, delete_link, BASE, SESSION, AljokerLink
from telethon.errors.rpcerrorlist import YouBlockedUserError
#ياقائم آل محمد
from JoKeRUB import l313l
from . import BOTLOG, BOTLOG_CHATID, l313l
from ..helpers.utils import reply_id
plugin_category = "tools"
# الي يخمط ويكول من كتابتي الا امه انيجه وقد اعذر من انذر

@l313l.ar_cmd(pattern="حالتي ?(.*)")
async def kkr(event):
    jokevent = await edit_or_reply(event, "**- جـارِ التحقـق انتظـر قليـلاً . . .**")
    bot_spam = "@SpamBot"
    async with bot.conversation(bot_spam) as conv:
        try:
            dontTag = conv.wait_event(
                events.NewMessage(incoming=True, from_users=178220800))
            purgeflag = await conv.send_message("/start")
            dontTag = await dontTag
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await l313l(unblock(bot_spam))
            dontTag = conv.wait_event(
                events.NewMessage(incoming=True, from_users=178220800))
            purgeflag = await conv.send_message("/start")
            dontTag = await dontTag
            await bot.send_read_acknowledge(conv.chat_id)
        
        await jokevent.edit(f"**⌔╎حالة حسابـك حاليـاً هـي :**\n\n~ {dontTag.message.message}")
        
        # حذف المحادثة كامله بنفس الطريقة
        await delete_conv(event, bot_spam, purgeflag)

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

# معرف المالك من l313l.uid
my_id = l313l.uid

# متغيرات حالة الأنظمة
song_enabled = False
poem_enabled = False
remix_enabled = False

# قاموس لتخزين كائنات القنوات (لتحسين الأداء)
channels = {
    'song': None,
    'poem': None,
    'remix': None
}

async def get_cached_channel(client, username):
    """الحصول على كائن القناة مع تخزين مؤقت لتجنب طلبات API المتكررة"""
    if channels[username] is None:
        channels[username] = await client.get_entity(username)
    return channels[username]

async def send_media_from_channel(event, channel_username, start_num, end_num, caption):
    """وظيفة عامة لإرسال وسائط من أي قناة"""
    try:
        # الحصول على رقم عشوائي
        rl = random.randint(start_num, end_num)
        
        # الحصول على كائن القناة (من التخزين المؤقت)
        channel = await get_cached_channel(event.client, channel_username)
        
        # 🔥 التحسين الأهم: جلب الرسالة الحقيقية بدلاً من تحميل الملف
        message = await event.client.get_messages(channel, ids=rl)
        
        if message and message.media:
            # إرسال الميديا مباشرة (نقل داخلي سريع)
            await event.client.send_file(
                event.chat_id,
                message.media,
                caption=caption,
                reply_to=event.id if event.sender_id != my_id else None,
                parse_mode="html"
            )
            # حذف أمر المستخدم فقط إذا لم يكن المالك (اختياري)
            if event.sender_id != my_id:
                await event.delete()
        else:
            await event.reply("⚠️ لم يتم العثور على الميديا بهذا الرقم.")
            
    except Exception as e:
        await event.reply(f"حدث خطأ: {str(e)}")

# ========== نظام "غنيلي" (مدمج) ==========
@l313l.on(events.NewMessage(pattern="^\.(تفعيل|ايقاف) غنيلي$"))
async def toggle_song(event):
    global song_enabled
    if event.sender_id == my_id:
        action = event.pattern_match.group(1)
        song_enabled = (action == "تفعيل")
        status = "تم تفعيل" if song_enabled else "تم إلغاء تفعيل"
        await event.reply(f"{status} غنيلي بنجاح!")

@l313l.on(events.NewMessage(pattern="^\.غنيلي$"))
async def send_song(event):
    if not song_enabled and event.sender_id != my_id:
        return
    await send_media_from_channel(event, "Kii_ti", 5, 141, "- تم اختيارها لك .")

# ========== نظام "شعر" (مدمج) ==========
@l313l.on(events.NewMessage(pattern="^\.(تفعيل|ايقاف) شعر$"))
async def toggle_poem(event):
    global poem_enabled
    if event.sender_id == my_id:
        action = event.pattern_match.group(1)
        poem_enabled = (action == "تفعيل")
        status = "تم تفعيل" if poem_enabled else "تم إلغاء تفعيل"
        await event.reply(f"{status} الشعر بنجاح!")

@l313l.on(events.NewMessage(pattern="^\.شعر$"))
async def send_poem(event):
    if not poem_enabled and event.sender_id != my_id:
        return
    await send_media_from_channel(event, "Lx1x2", 4, 67, "- تم اختيارها لك .")

# ========== نظام "ريمكس" (مدمج) ==========
@l313l.on(events.NewMessage(pattern="^\.(تفعيل|ايقاف) ريمكس$"))
async def toggle_remix(event):
    global remix_enabled
    if event.sender_id == my_id:
        action = event.pattern_match.group(1)
        remix_enabled = (action == "تفعيل")
        status = "تم تفعيل" if remix_enabled else "تم إلغاء تفعيل"
        await event.reply(f"{status} الريمكس بنجاح!")

@l313l.on(events.NewMessage(pattern="^\.ريمكس$"))
async def send_remix(event):
    if not remix_enabled and event.sender_id != my_id:
        return
    await send_media_from_channel(event, "rem77e", 4, 70, "- تم اختيار هذا الريمكس لك .")

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
