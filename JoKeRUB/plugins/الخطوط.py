from telethon import events
from telethon.tl.types import (
    MessageEntityBold, 
    MessageEntityStrike, 
    MessageEntityCode, 
    MessageEntityPre,
    MessageEntityCustomEmoji
)
from telethon.tl.functions.messages import EditMessageRequest
from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete

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
    if not event.message.text:
        return
    
    if event.message.media:
        return
        
    text = event.message.text
    
    if text.startswith('.'):
        return
    
    # تحديد نوع التنسيق المطلوب
    format_type = None
    
    if gvarstatus("bold"):
        format_type = "bold"
    elif gvarstatus("tshwesh"):
        format_type = "strike"
    elif gvarstatus("ramz"):
        format_type = "code"
    elif gvarstatus("joker"):
        format_type = "pre"
    
    if not format_type:
        return
    
    # جمع جميع الـ entities الأصلية
    entities = []
    if event.message.entities:
        entities = list(event.message.entities)
    
    # إضافة entity التنسيق في البداية
    if format_type == "bold":
        entities.insert(0, MessageEntityBold(offset=0, length=len(text)))
    elif format_type == "strike":
        entities.insert(0, MessageEntityStrike(offset=0, length=len(text)))
    elif format_type == "code":
        entities.insert(0, MessageEntityCode(offset=0, length=len(text)))
    elif format_type == "pre":
        entities.insert(0, MessageEntityPre(offset=0, length=len(text), language=""))
    
    try:
        # استخدام EditMessageRequest مباشرة
        await event.client(EditMessageRequest(
            peer=event.chat_id,
            id=event.message.id,
            message=text,
            entities=entities,
            no_webpage=True
        ))
    except Exception as e:
        # إذا فشل، جرب الطريقة البديلة
        try:
            await event.client.edit_message(
                event.chat_id,
                event.message.id,
                text,
                formatting_entities=entities,
                link_preview=False
            )
        except:
            pass
