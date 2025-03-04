from telethon import events
from telethon.errors import MessageIdInvalidError
from JoKeRUB import l313l
from ..helpers.utils import gvarstatus, addgvar, delgvar
from ..helpers.functions import CustomParseMode

# تفعيل خط التشويش
@l313l.on(events.NewMessage(outgoing=True, pattern=r"^\.(تفعيل تشويش|تفعيل التشويش)$"))
async def enable_chaos(event):
    is_cllear = gvarstatus("cllear")
    if not is_cllear:
        addgvar("cllear", "on")
        await event.edit("**⎉╎تم تفعيـل خـط التشـويش .. بنجـاح ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل تشويش) **")
    else:
        await event.edit("**⎉╎خـط التشـويش مفعـل .. مسبقـاً ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل تشويش) **")

# تعطيل خط التشويش
@l313l.on(events.NewMessage(outgoing=True, pattern=r"^\.(تعطيل تشويش|تعطيل التشويش)$"))
async def disable_chaos(event):
    is_cllear = gvarstatus("cllear")
    if is_cllear:
        delgvar("cllear")
        await event.edit("**⎉╎تم تعطيـل خـط التشـويش .. بنجـاح ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل تشويش) **")
    else:
        await event.edit("**⎉╎خـط التشـويش معطـل .. مسبقـاً ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل تشويش) **")

# تحويل الرسائل إلى تشويش
@l313l.on(events.NewMessage(outgoing=True))
async def chaos_text(event):
    if event.message.text and not event.message.media and "." not in event.message.text:
        is_cllear = gvarstatus("cllear")
        if is_cllear:
            try:
                # إضافة العلامات ‹ و › وجعل النص غامقًا
                chaos_message = f"‹ **{event.message.text}** ›"
                # إرسال الرسالة بتنسيق Markdown
                await event.edit(f"[{chaos_message}](spoiler)", parse_mode=CustomParseMode("markdown"))
            except MessageIdInvalidError:
                pass
