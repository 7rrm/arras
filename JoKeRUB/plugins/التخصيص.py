from urlextract import URLExtract
import re
import requests
from JoKeRUB import l313l
from JoKeRUB.core.logger import logging
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG_CHATID
from telegraph import Telegraph


LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER

extractor = URLExtract()

oldvars = {
    "PM_PIC": "pmpermit_pic",
    "PM_TEXT": "pmpermit_txt",
    "PM_BLOCK": "pmblock",
}

@l313l.ar_cmd(pattern="جلب (.*)")
async def getvar(event):
    input = event.pattern_match.group(1)
    if input is None:
        await edit_or_reply(event, "`ضع فار لجلب قيمته`")

        return
    if gvarstatus(input) is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
    await edit_or_reply(event, gvarstatus(input))


@l313l.ar_cmd(pattern="اضف (.*)")
async def custom_HuRe(event):
    reply = await event.get_reply_message()
    text = None
    var = None
    if reply:
        text = reply.text
    if text is None:
        return await edit_delete(
            event, "**⌔∮ يجب عليك الرد على النص او الرابط حسب الفار الذي تضيفه **"
        )
    input_str = event.pattern_match.group(1)
    if (
        input_str == "كليشة الحماية"
        or input_str == "كليشة الحمايه"
        or input_str == "كليشه الحماية"
        or input_str == "كليشه الحمايه"
    ):
        addgvar("pmpermit_txt", text)
        var = "pmpermit_txt"
    if input_str == "اشتراك الخاص" or input_str == "اشتراك خاص":
        addgvar("pchan", text)
        var = "pchan"
    if input_str == "اشتراك كروب" or input_str == "اشتراك الكروب":
        addgvar("gchan", text)
        var = "gchan"
    if input_str == "امر النشر" or input_str == "امر نشر":
        addgvar("MUKRR_ET", text)
        var = "MUKRR_ET"
        '''
    if input_str == "زخرفة الارقام" or input_str == "زخرفه الارقام":
        addgvar("JP_FN", text)
        var = "JP_FN"
    if input_str == "البايو" or input_str == "بايو":
        addgvar("DEFAULT_BIO", text)
        var = "DEFAULT_BIO"
        '''
    if input_str == "رمز الاسم" or input_str == "علامة الاسم":
        addgvar("TIME_JEP", text)
        var = "TIME_JEP"
    if input_str == "كليشة الفحص" or input_str == "كليشه الفحص" or input_str == "كليشه فحص" or input_str == "كليشه فحص":
        addgvar("ALIVE_TEMPLATE", text)
        var = "ALIVE_TEMPLATE"
    if input_str == "كليشة الحظر" or input_str == "كليشه الحظر":
        addgvar("pmblock", text)
        var = "pmblock"
    if input_str == "كليشة البوت" or input_str == "كليشه البوت":
        addgvar("START_TEXT", text)
        var = "START_TEXT"
    if input_str == "ايموجي الفحص":
        addgvar("ALIVE_EMOJI", text)
        var = "ALIVE_EMOJI"
    if input_str == "نص الفحص":
        addgvar("ALIVE_TEXT", text)
        var = "ALIVE_TEXT"
    if input_str == "عدد التحذيرات":
        addgvar("MAX_FLOOD_IN_PMS", text)
        var = "MAX_FLOOD_IN_PMS"
        '''
    if (
        input_str == "لون الوقتي"
        or input_str == "لون وقتي"
        or input_str == "لون صوره وقتيه"
        or input_str == "لون الصوره الوقتيه"
        or input_str == "لون"
    ):
       addgvar("digitalpiccolor", text)
       var = "digitalpiccolor"
       '''
    if input_str == "التخزين" or input_str == "تخزين":
        addgvar("PM_LOGGER_GROUP_ID", text)
        var = "PM_LOGGER_GROUP_ID"
    if input_str == "كليشة الخاص" or input_str == "كليشه الخاص":
        addgvar("aljoker_message", text)
        var = "aljoker_message"
    if input_str == "اشعارات" or input_str == "الاشعارات":
        addgvar("PRIVATE_GROUP_BOT_API_ID", text)
        var = "PRIVATE_GROUP_BOT_API_ID"
    await edit_or_reply(event, f"**₰ تم بنجاح تحديث فار {input_str} 𓆰،**")
    delgvar(var)
    addgvar(var, text)
    if BOTLOG_CHATID:
            await event.client.send_message(
            BOTLOG_CHATID,
            f"#اضف_فار\
                    \n**{input_str}** تم تحديثه بنجاح في قاعده البيانات كـ:",
        )


@l313l.ar_cmd(pattern="حذف (.*)")
async def custom_HuRe(event):
    input_str = event.pattern_match.group(1)
    if (
        input_str == "كليشة الحماية"
        or input_str == "كليشة الحمايه"
        or input_str == "كليشه الحماية"
        or input_str == "كليشه الحمايه"
    ):
        if gvarstatus("pmpermit_txt") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("pmpermit_txt")
    if input_str == "كليشة الفحص" or input_str == "كليشه الفحص" or input_str == "كليشه فحص" or input_str == "كليشه فحص":
        if gvarstatus("ALIVE_TEMPLATE") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("ALIVE_TEMPLATE")
    if input_str == "كليشة الحظر" or input_str == "كليشه الحظر":
        if gvarstatus("pmblock") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("pmblock")
    if (
        input_str == "صورة الحماية"
        or input_str == "صورة الحمايه"
        or input_str == "صوره الحماية"
        or input_str == "صوره الحمايه"
    ):
        if gvarstatus("pmpermit_pic") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("pmpermit_pic")
        '''  
    if (
        input_str == "لون الوقتي"
        or input_str == "لون وقتي"
        or input_str == "لون صوره وقتيه"
        or input_str == "لون الصوره الوقتيه"
    ):
        if gvarstatus("digitalpiccolor") is None:
            return await edit_delete(
                event, "**لم تضيف الفار اصلاً**"
            )
        delgvar("digitalpiccolor")
        '''
    if input_str == "صورة الفحص" or input_str == "صوره الفحص":
        if gvarstatus("ALIVE_PIC") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("ALIVE_PIC")
    if input_str == "كليشة البوت" or input_str == "كليشه البوت":
        if gvarstatus("START_TEXT") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("START_TEXT")
    if input_str == "ايموجي الفحص":
        if gvarstatus("ALIVE_EMOJI") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("ALIVE_EMOJI")
    if input_str == "التخزين" or input_str == "تخزين":
    	if gvatstatus("PM_LOGGER_GROUP_ID") is None:
    	    return await edit_delete(event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**")
    	delgvar("PM_LOGGER_GROUP_ID")
    if input_str == "اشعارات" or input_str == "الاشعارات":
    	if gvatstatus("PRIVATE_GROUP_BOT_API_ID") is None:
    	    return await edit_delete(event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**")
    	delgvar("PRIVATE_GROUP_BOT_API_ID")
    if input_str == "نص الفحص":
        if gvarstatus("ALIVE_TEXT") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
            '''
        delgvar("ALIVE_TEXT")
    if input_str == "زخرفة الارقام" or input_str == "زخرفه الارقام":
        if gvarstatus("JP_FN") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("JP_FN")
    if input_str == "بايو" or input_str == "البايو":
        if gvarstatus("DEFAULT_BIO") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("DEFAULT_BIO")
        '''
    if input_str == "رمز الاسم":
        if gvarstatus("TIME_JEP") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("TIME_JEP")
    if input_str == "عدد التحذيرات":
        if gvarstatus("MAX_FLOOD_IN_PMS") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("MAX_FLOOD_IN_PMS")
    if input_str == "صورة البنك" or input_str == "صوره البنك":
        if gvarstatus("PING_PIC") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("PING_PIC")
    await edit_or_reply(
        event, f"₰ هذا الفار تم حذفه بنجاح وارجاع قيمته الى القيمه الاصلية ✅"
    )
    if BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#حذف_فار\
                    \n**فار {input_str}** تم حذفه من قاعده البيانات",
        )
telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]

@l313l.ar_cmd(pattern="اضف صورة (الفحص|فحص) ?(.*)")
async def alive_aljoker(event):
    reply = await event.get_reply_message()
    if reply and reply.media:
        input_str = event.pattern_match.group(1)
        media = await reply.download_media()
        response = telegraph.upload_file(media)
        url = 'https://telegra.ph' + response[0]['src']
        addgvar("ALIVE_PIC", url)
        await event.edit(f"**᯽︙ تم بنجاح اضافة صورة  {input_str} ✓ **")
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#اضف_فار\n**{input_str}** تم تحديثه بنجاح في قاعدة البيانات كـ: {url}",
            )
        else:
            await event.edit("**حدث خطأ أثناء تحميل الصورة على Telegraph**")
    else:
        await event.edit("**᯽︙ يرجى الرد على الصورة لتحديث الفار**")
@l313l.ar_cmd(pattern="اضف صورة (البنك|بنك) ?(.*)")
async def add_ping_aljoker(event):
    reply = await event.get_reply_message()
    if reply and reply.media:
        input_str = event.pattern_match.group(1)
        media = await reply.download_media()
        response = telegraph.upload_file(media)
        url = 'https://telegra.ph' + response[0]['src']
        addgvar("PING_PIC", url)
        await event.edit(f"**᯽︙ تم بنجاح اضافة صورة  {input_str} ✓ **")
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#اضف_فار\n**{input_str}** تم تحديثه بنجاح في قاعدة البيانات كـ: {url}",
            )
        else:
            await event.edit("**حدث خطأ أثناء تحميل الصورة على Telegraph**")
    else:
        await event.edit("**᯽︙ يرجى الرد على الصورة لتحديث الفار**")
@l313l.ar_cmd(pattern="اضف صورة (الحماية|الحمايه|حماية|حمايه) ?(.*)")
async def security_aljoker(event):
    reply = await event.get_reply_message()
    if reply and reply.media:
        input_str = event.pattern_match.group(1)
        media = await reply.download_media()
        response = telegraph.upload_file(media)
        url = 'https://telegra.ph' + response[0]['src']
        addgvar("pmpermit_pic", url)
        await event.edit(f"**᯽︙ تم بنجاح اضافة صورة  {input_str} ✓ **")
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#اضف_فار\n**{input_str}** تم تحديثه بنجاح في قاعدة البيانات كـ: {url}",
            )
        else:
            await event.edit("**حدث خطأ أثناء تحميل الصورة على Telegraph**")
    else:
        await event.edit("** ᯽︙ يرجى الرد على الصورة او فيديو لتحديث الفار **")
@l313l.ar_cmd(pattern="اضف صورة (الخاص|خاص) ?(.*)")
async def al5a9_aljoker(event):
    reply = await event.get_reply_message()
    if reply and reply.media:
        input_str = event.pattern_match.group(1)
        media = await reply.download_media()
        response = telegraph.upload_file(media)
        url = 'https://telegra.ph' + response[0]['src']
        addgvar("aljoker_url", url)
        await event.edit(f"**᯽︙ تم بنجاح اضافة صورة  {input_str} ✓ **")
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#اضف_فار\n**{input_str}** تم تحديثه بنجاح في قاعدة البيانات كـ: {url}",
            )
        else:
            await event.edit("**حدث خطأ أثناء تحميل الصورة على Telegraph**")
    else:
        await event.edit("** ᯽︙ يرجى الرد على الصورة او فيديو لتحديث الفار **")
