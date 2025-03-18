#Fixed by Reda

import os

from telethon import events
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights
from JoKeRUB import l313l

#Joker
from ..core.managers import edit_or_reply

from . import *
plugin_category = "utils"

# أمر إضافة كروب جديد
@l313l.ar_cmd(
    pattern="\$\$اضافة_كروب ?(.*)$",  # الأمر الجديد مع $$
    command=("اضافة_كروب", plugin_category),
)
async def add_group(event):
    if not event.out and not is_fullsudo(event.sender_id):
        return await edit_or_reply(event, "هـذا الامـر مقـيد ")
    
    group_id = event.pattern_match.group(1)
    if not group_id:
        return await edit_or_reply(event, "** ᯽︙ يرجى إدخال ايدي الكروب**")
    
    # تحميل القائمة الحالية
    groups = load_groups()
    
    # إضافة الكروب الجديد إذا لم يكن موجودًا
    if group_id not in groups:
        groups.append(group_id)
        save_groups(groups)
        await edit_or_reply(event, f"** ᯽︙ تم إضافة الكروب `{group_id}` إلى القائمة بنجاح**")
    else:
        await edit_or_reply(event, f"** ᯽︙ الكروب `{group_id}` موجود بالفعل في القائمة**")

# أمر إرسال الرسالة إلى الكروبات المضافة
@l313l.ar_cmd(
    pattern="\$\$نشر_رسالة$",  # الأمر الجديد مع $$
    command=("نشر_رسالة", plugin_category),
)
async def send_to_specific_groups(event):
    if not event.out and not is_fullsudo(event.sender_id):
        return await edit_or_reply(event, "هـذا الامـر مقـيد ")
    
    # الرسالة المحددة التي تريد إرسالها
    message = "ش"  # يمكنك تغييرها إلى أي رسالة تريدها
    
    # تحميل قائمة الكروبات
    specific_groups = load_groups()
    if not specific_groups:
        return await edit_or_reply(event, "** ᯽︙ لم يتم إضافة أي كروبات بعد**")
    
    event = await edit_or_reply(event, "** ᯽︙ يتـم إرسـال الـرسـالـة إلـى الـكروبات الـمحددة انتـظر قليلا**")
    
    er = 0
    done = 0
    
    for group in specific_groups:
        try:
            await bot.send_message(int(group), message)  # إرسال الرسالة إلى الكروب
            done += 1
        except Exception as e:
            print(f"حدث خطأ في إرسال الرسالة إلى الكروب {group}: {e}")
            er += 1
    
    await event.edit(f"** ᯽︙ تـم إرسـال الـرسـالـة إلـى {done} كروب بنجاح، وحدث خطأ في {er} كروب**")

@l313l.ar_cmd(
    pattern="وجه ?(.*)$",
    command=("وجه", plugin_category),
)
async def gcast(event):
    if not event.out and not is_fullsudo(event.sender_id):
        return await edit_or_reply(event, "هـذا الامـر مقـيد ")
    xx = event.pattern_match.group(1)
    if not xx:
        return edit_or_reply(event, "** ᯽︙ يجـب وضـع نـص مع الـتوجيه**")
    tt = event.text
    msg = tt[5:]
    event = await edit_or_reply(event, "** ᯽︙ يتـم الـتوجيـة للـمجموعـات انتـظر قليلا**")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await event.edit(f"تـم بنـجـاح فـي {done} من الـدردشـات , خطـأ فـي {er} من الـدردشـات")


@l313l.ar_cmd(
    pattern="حول ?(.*)$",
    command=("حول", plugin_category),
)
async def gucast(event):
    if not event.out and not is_fullsudo(event.sender_id):
        return await edit_or_reply(event, "هـذا الامـر مقـيد للسـودو")
    xx = event.pattern_match.group(1)
    if not xx:
        return edit_or_reply(event, "** ᯽︙ يجـب وضـع نـص مع الامـر للتوجيـه**")
    tt = event.text
    msg = tt[6:]
    kk = await edit_or_reply(event, "** ᯽︙ يتـم الـتوجيـة للخـاص انتـظر قليلا**")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await event.edit(f"تـم بنـجـاح فـي {done} من الـدردشـات , خطـأ فـي {er} من الـدردشـات")
@l313l.ar_cmd(
    pattern="توجيه?(.*)$",
    command=("توجيه", plugin_category),
)
async def all_joker(event):
    if not event.out and not is_fullsudo(event.sender_id):
        return await edit_or_reply(event, "هـذا الامـر مقـيد ")
    xx = event.pattern_match.group(1)
    if not xx:
        return edit_or_reply(event, "** ᯽︙ يجـب وضـع نـص مع الـتوجيه**")
    tt = event.text
    msg = tt[5:]
    event = await edit_or_reply(event, "** ᯽︙ يتـم الـتوجيـة لجـميـع جهات الاتصـال انتـظر قليلا**")
    er = 0
    done = 0
    async for dialog in bot.iter_dialogs():
        try:
            done += 1
            await bot.send_message(dialog.id, msg)
        except BaseException:
            er += 1
    await event.edit(f"تـم بنـجـاح فـي إرسـال الـرسـالـة إلـى جميع المحادثات الخاصة والدردشات {done}  خطـأ فـي {er} ")
