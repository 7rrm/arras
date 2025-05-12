from telethon import events
from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete
from telethon import functions
from telethon.errors.rpcerrorlist import MessageIdInvalidError
import re
# جميع أوامر الخطوط مع التعديل الجديد للخط الغامق
@l313l.on(admin_cmd(pattern="(خط الغامق|خط غامق)"))
async def bold_toggle(event):
    if not gvarstatus("bold"):
        addgvar("bold", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الغامق بنجاح ✓**")
    else:
        delgvar("bold")
        await edit_delete(event, "**᯽︙ تم إيقاف خط الغامق ✓**")

@l313l.on(admin_cmd(pattern="(خط المشطوب|خط مشطوب)"))
async def strikethrough_toggle(event):
    if not gvarstatus("tshwesh"):
        addgvar("tshwesh", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط المشطوب ✓**")
    else:
        delgvar("tshwesh")
        await edit_delete(event, "**᯽︙ تم إيقاف خط المشطوب ✓**")

@l313l.on(admin_cmd(pattern="(خط رمز|خط الرمز)"))
async def monospace_toggle(event):
    if not gvarstatus("ramz"):
        addgvar("ramz", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الرمز ✓**")
    else:
        delgvar("ramz")
        await edit_delete(event, "**᯽︙ تم إيقاف خط الرمز ✓**")

@l313l.on(admin_cmd(pattern="(خط الجوكر|خط جوكر)"))
async def joker_toggle(event):
    if not gvarstatus("joker"):
        addgvar("joker", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الجوكر ✓**")
    else:
        delgvar("joker")
        await edit_delete(event, "**᯽︙ تم إيقاف خط الجوكر ✓**")

@l313l.on(events.NewMessage(outgoing=True))
async def handle_text_formatting(event):
    if not event.message.text or event.message.media:
        return
        
    text = event.message.text
    modified = False
    
    # فصل اليوزرنيمات عن النص العادي
    parts = re.split(r'(\s+|@\w+)', text)  # يفصل النص واليوزرنيمات
    processed_parts = []
    
    for part in parts:
        if part.startswith('@') or part.isspace():
            processed_parts.append(part)  # يترك اليوزرنيمات والمسافات كما هي
        else:
            if gvarstatus("bold"):
                part = f"**{part}**"
                modified = True
            elif gvarstatus("tshwesh"):
                part = f"~~{part}~~"
                modified = True
            elif gvarstatus("ramz"):
                part = f"`{part}`"
                modified = True
            elif gvarstatus("joker"):
                part = f"```{part}```"
                modified = True
            processed_parts.append(part)
    
    if modified:
        new_text = ''.join(processed_parts)
        try:
            await event.edit(new_text)
        except:
            pass
