from JoKeRUB import l313l, bot
import time
from telethon.tl import types
from JoKeRUB import BOTLOG_CHATID
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
import asyncio
from ..Config import Config
import requests
from telethon import Button, events
from telethon.tl.functions.messages import ExportChatInviteRequest
from ..core.managers import edit_delete, edit_or_reply
#ياعلي
#اخ اخ اخ اخ اخ اخ اخممممممط ياطويل العمر اخمطط 😂
#Reda
REH = "**᯽︙ لأستخدام بوت اختراق الحساب عن طريق كود التيرمكس أضغط على الزر**"
JOKER_PIC = "https://graph.org/file/a467d3702fbc9ae391fe0-e6322ec96a2fd4c1f4.jpg"
Bot_Username = Config.TG_BOT_USERNAME
if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        joker = Bot_Username.replace("@", "")
        query = event.text
        await bot.get_me()
        if query.startswith("هاك") and event.query.user_id == bot.uid:
            buttons = Button.url("• اضغط هنا عزيزي •", f"https://t.me/{joker}")
            if JOKER_PIC and JOKER_PIC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(
                    JOKER_PIC, text=REH, buttons=buttons, link_preview=False
                )
            elif JOKER_PIC:
                result = builder.document(
                    JOKER_PIC,
                    title="Aljoker 🤡",
                    text=REH,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    title="Aljoker 🤡",
                    text=REH,
                    buttons=buttons,
                    link_preview=False,
                )
        await event.answer([result] if result else None)

@bot.on(admin_cmd(outgoing=True, pattern="هاك"))
async def repo(event):
    if event.fwd_from:
        return
    lMl10l = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    await bot.send_message(lMl10l, "/hack")
    response = await bot.inline_query(lMl10l, "هاك")
    await response[0].click(event.chat_id)
    await event.delete()

########################################
#################الاشـتـراك###################
#######################################

import os
import re
import time
import asyncio
from asyncio import sleep
import telethon
from telethon.events import CallbackQuery, InlineQuery
from telethon import Button, events, functions
from telethon.tl import functions, types
from telethon.extensions import html
from telethon.errors import FloodWaitError
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import EditBannedRequest, GetFullChannelRequest, GetParticipantRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights

from . import l313l
from ..sql_helper.fsub_sql import *
from ..sql_helper import no_log_pms_sql, pmpermit_sql
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete, edit_or_reply
from ..core.logger import logging
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event

# كلاس التحليل المخصص للإيموجي البريميوم
class CustomParseMode:
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'html':
            text, entities = html.parse(text)
            # معالجة إيموجيات البريميوم
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

zilzal = l313l.uid
zed_dev = (5427469031,)
LOGS = logging.getLogger(__name__)
zelzaal = gvarstatus("zelzaal_fsub") == "true"
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
ANTI_DDDD_ZEDTHON_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_messages=True, send_media=True, send_stickers=True, send_gifs=True
)

async def is_admin(event, user):
    try:
        sed = await event.client.get_permissions(event.chat_id, user)
        if sed.is_admin:
            is_mod = True
        else:
            is_mod = False
    except:
        is_mod = False
    return is_mod


async def check_him(channel, user):
    try:
        result = await bot(
            functions.channels.GetParticipantRequest(channel, user)
        )
        return True
    except telethon.errors.rpcerrorlist.UserNotParticipantError:
        return False


async def rights(event):
    result = await bot(
        functions.channels.GetParticipantRequest(
            channel=event.chat_id,
            user_id=zilzal,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )


@l313l.ar_cmd(pattern="(ضع اشتراك الخاص|وضع اشتراك الخاص)(?: |$)(.*)")
async def _(event):
    if input_str := event.pattern_match.group(2):
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{e}`", 5)
        try:
            if p.first_name:
                await asyncio.sleep(1.5)
                delgvar("Custom_Pm_Channel")
                addgvar("Custom_Pm_Channel", f"-100{p.id}")
                return await edit_or_reply(
                    event, f"**⎉╎تم إضافة قناة الاشتراك الاجباري للخاص .. بنجـاح ☑️**\n\n**⎉╎يوزر القناة : ↶** `{input_str}`\n**⎉╎ايدي القناة : ↶** `{p.id}`\n\n**⎉╎ارسـل الان** `.تفعيل الاشتراك خاص`"
                )
        except Exception:
            try:
                if p.title:
                    await asyncio.sleep(1.5)
                    delgvar("Custom_Pm_Channel")
                    addgvar("Custom_Pm_Channel", f"-100{p.id}")
                    return await edit_or_reply(
                        event, f"**⎉╎تم إضافة قناة الاشتراك الاجباري للخاص .. بنجـاح ☑️**\n\n**⎉╎اسم القناة : ↶** `{p.title}`\n**⎉╎ايدي القناة : ↶** `{p.id}`\n\n**⎉╎ارسـل الان** `.تفعيل الاشتراك خاص`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "⪼ **أدخل معـرف القناة او قم باستخدام الامر داخل القناة**")
    elif event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            await asyncio.sleep(1.5)
            delgvar("Custom_Pm_Channel")
            addgvar("Custom_Pm_Channel", event.chat_id)
            await edit_or_reply(
                event,
                f"**⎉╎تم إضافة قناة الاشتراك الاجباري للخاص .. بنجـاح ☑️**\n\n**⎉╎ايدي القناة : ↶** `{event.chat_id}`\n\n**⎉╎ارسـل الان** `.تفعيل الاشتراك خاص`",
            )

        else:
            await asyncio.sleep(1.5)
            delgvar("Custom_Pm_Channel")
            addgvar("Custom_Pm_Channel", event.chat_id)
            await edit_or_reply(
                event,
                f"**⎉╎تم إضافة قناة الاشتراك الاجباري للخاص .. بنجـاح ☑️**\n\n**⎉╎ايدي القناة : ↶** `{event.chat_id}`\n\n**⎉╎ارسـل الان** `.تفعيل الاشتراك خاص`",
            )

    else:
        await asyncio.sleep(1.5)
        delgvar("Custom_Pm_Channel")
        addgvar("Custom_Pm_Channel", event.chat_id)
        await edit_or_reply(event, f"**⎉╎تم إضافة قناة الاشتراك الاجباري للخاص .. بنجـاح ☑️**\n\n**⎉╎ايدي القناة : ↶** `{event.chat_id}`\n\n**⎉╎ارسـل الان** `.تفعيل الاشتراك خاص`")


@l313l.ar_cmd(pattern="(تفعيل اشتراك الخاص|تفعيل الاشتراك خاص)")
async def start_datea(event):
    if gvarstatus("zelzaal_fsub") == "true":
        return await edit_or_reply(event, "**⎉╎الاشتراك الاجبـاري لـ الخـاص .. مفعـل مسبقـاً ☑️**")
    addgvar("zelzaal_fsub", "true")
    await edit_or_reply(event, "**⎉╎تم تفعيـل الاشتـراك الاجبـاري خـاص .. بنجـاح ☑️**")

@l313l.ar_cmd(pattern="(تعطيل اشتراك الخاص|تعطيل الاشتراك الخاص)")
async def stop_datea(event):
    if gvarstatus("zelzaal_fsub") == "true":
        delgvar("zelzaal_fsub")
        return await edit_or_reply(event, "**⎉╎تم تعطيـل الاشتـراك الاجبـاري خـاص .. بنجـاح ☑️**")
    await edit_or_reply(event, "**⎉╎الاشتراك الاجبـاري لـ الخـاص .. معطـل مسبقـاً ☑️**")

@l313l.ar_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def fp(event):
    if gvarstatus("zelzaal_fsub") != "true":
        return
    
    chat = await event.get_chat()
    sender = await event.get_sender()
    if chat.bot or sender.bot or chat.id == 777000:
        return
    
    ch = gvarstatus("Custom_Pm_Channel")
    if not ch:
        return
        
    ch = int(ch)
    rip = await check_him(ch, event.sender_id)
    
    if rip is False and not pmpermit_sql.is_approved(event.sender_id):
        user = await event.client.get_entity(event.sender_id)
        username = user.first_name or "عزيزي"
        
        c = await l313l.get_entity(ch)
        chn = c.username if c.username else (await l313l(ExportChatInviteRequest(ch))).link
        
        message = (
            f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗦𝘂𝗯 - الاشتراك الإجباري\n"
            f"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n"
            f"⌔╎مࢪحبـاً عـزيـزي {username} "
            f"<a href='emoji/5994531982975964413'>❤️</a>\n"
            f"⌔╎لـ الغـاء كتمـك "
            f"<a href='emoji/5841359499146825803'>❤️</a>\n"
            f"⌔╎يُرجـى الإشتـراك بالقنـاة {f'@{chn}' if chn.startswith('@') or not chn.startswith('http') else chn} "
            f"<a href='emoji/5994576637750941503'>❤️</a>"
        )
        
        await event.respond(message, parse_mode=CustomParseMode("html"), link_preview=False)
        await event.delete()

@l313l.ar_cmd(pattern="(ضع اشتراك الكروب|وضع اشتراك الكروب) ?(.*)")
async def fs(event):
    permissions = await bot.get_permissions(event.chat_id, event.sender_id)
    if not permissions.is_admin:
        return await event.reply(
            "**⌔╎عـذراً .. عـزيـزي\n**⌔╎لا املك صلاحيات المشـرف هنـا**"
        )
    if not await is_admin(event, zilzal):
        return await event.reply("**⌔╎عـذراً .. عـزيـزي\n**⌔╎لا املك صلاحيات المشـرف هنـا**")
    if event.is_private:
        await edit_or_reply(event, "**✾╎عـذراً .. هـذا الامـر خـاص بالمجمـوعـات فقـط**")
        return
    ahmed = event.pattern_match.group(1)
    if not ahmed:
        return await edit_delete(event, "**✾╎استخـدم الامـر هكـذا**\n**✾╎.اشتراك الكروب + معـرف القنـاة**")
    args = event.pattern_match.group(2)
    channel = args.replace("@", "")
    if args == "تفعيل" or args == "تشغيل":
        return await event.reply("**⌔╎عـذراً .. يرجى التحقق من معـرف القنـاة**")
    if args in ("off", "تعطيل", "ايقاف"):
        rm_fsub(event.chat_id)
        await event.reply("**✾╎تـم إيقـاف الاشتـراك الاجبـاري هنـا .. بنجـاح ✓**")
    else:
        try:
            ch_full = await bot(GetFullChannelRequest(channel=channel))
        except Exception as e:
            await event.reply(f"{e}")
            return await event.reply("**⌔╎عـذراً .. معـرف القنـاة غيـر موجـود**")
        rip = await check_him(channel, zilzal)
        if rip is False:
            return await event.reply(
                f"**⌔╎عـذراً .. عـزيـزي**\n**⌔╎لـ تمكين الاشتـراك الاجبـاري**\n**⌔╎يجب ان تكون مشرفًا في** [القنـاة](https://t.me/{args}).",
                link_preview=False,
            )
        add_fsub(event.chat_id, str(channel))
        await event.reply(f"**✾╎تم تفعيل الاشتراك الاجباري .. بنجاح ☑️**\n**✾╎قناة الاشتراك ~** @{channel}.")


@l313l.ar_cmd(incoming=True, func=lambda e: e.is_group, edited=False, forword=None)
async def fg(event):
    chat_db = is_fsub(event.chat_id)
    if not chat_db:
        return
    chat_id = event.chat_id
    zed_dev = (5427469031,)
    zelzal = event.sender_id
    try:
        sender = await event.get_sender()
        sender_entity = await event.client.get_entity(sender)
        if sender_entity.bot:
            return
    except FloodWaitError as e:
        wait_time = e.seconds
        await sleep(wait_time + 3)
    if zelzal in zed_dev:
        return
    if not await is_admin(event, zilzal):
        return
    if chat_db:
        try:
            channel = chat_db.channel
            chat_id = event.chat_id
            chat_db = is_fsub(event.chat_id)
            channel = chat_db.channel
            sender = await event.get_sender()
            grp = f"t.me/{channel}"
            rip = await check_him(channel, event.sender_id)
            if rip is False:
                message = (
                    f"<b>ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗦𝘂𝗕 - الاشتراك الإجباري</b>\n"
                    f"<b>⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆</b>\n\n"
                    f"<b>⌔╎مࢪحبـاً عـزيـزي</b> [{sender.first_name}](tg://user?id={sender.id}) "
                    f"<a href='emoji/5994531982975964413'>❤️</a>\n"
                    f"<b>⌔╎لـ الغـاء كتمـك </b>"
                    f"<a href='emoji/5841359499146825803'>❤️</a>\n"
                    f"<b>⌔╎يُࢪجـى الإشتـࢪاك بالقنـاة @{channel}</b> <a href='emoji/5994576637750941503'>❤️</a>"
                )
                await bot.send_message(
                    event.chat_id, 
                    message,
                    parse_mode=CustomParseMode("html"),
                    link_preview=False
                )
                await event.delete()
        except:
            if not await rights(event):
                await bot.send_message(
                    event.chat_id,
                    "<b>⌔╎عـذراً .. عـزيـزي\n⌔╎لا املك صلاحيات المشـرف هنـا</b>",
                    parse_mode=CustomParseMode("html")
                )

@l313l.ar_cmd(pattern="تعطيل اشتراك الكروب$")
async def removef(event):
    if is_fsub(event.chat_id):
        rm_fsub(event.chat_id)
        await edit_or_reply(event, "**✾╎تـم إيقـاف الاشتـراك الاجبـاري هنـا .. بنجـاح ✓**")
    else:
        return await edit_delete(event, "**✾╎عـذراً .. الاشتـراك الاجبـاري غيـر مفعـل هنـا**")

