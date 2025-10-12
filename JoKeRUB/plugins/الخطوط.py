from telethon import events
from telethon.tl.types import (
    MessageEntityBold, 
    MessageEntityStrike, 
    MessageEntityCode, 
    MessageEntityPre,
    MessageEntityCustomEmoji
)
from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete

# أوامر التفعيل (نفسها كما في الكود السابق)
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
    if not event.message.text or event.message.media or event.message.text.startswith('.'):
        return
    
    format_type = None
    if gvarstatus("bold"):
        format_type = MessageEntityBold
    elif gvarstatus("tshwesh"):
        format_type = MessageEntityStrike
    elif gvarstatus("ramz"):
        format_type = MessageEntityCode
    elif gvarstatus("joker"):
        format_type = lambda: MessageEntityPre(offset=0, length=len(event.message.text), language="")
    
    if not format_type:
        return
    
    entities = list(event.message.entities) if event.message.entities else []
    
    # إنشاء entity التنسيق
    if format_type == MessageEntityPre:
        format_entity = format_type()
    else:
        format_entity = format_type(offset=0, length=len(event.message.text))
    
    entities.insert(0, format_entity)
    
    try:
        await event.message.edit(event.message.text, formatting_entities=entities, parse_mode=None)
    except:
        pass
