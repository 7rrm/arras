from telethon import events
from telethon.tl.types import MessageEntityBold, MessageEntityStrike, MessageEntityCode, MessageEntityPre
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
    if not event.message.text or event.message.media:
        return
        
    text = event.message.text
    
    # تجاهل الأوامر
    if text.startswith('.') or '.' in text[:-1]:
        return
    
    # الحصول على الـ entities الأصلية (تشمل الإيموجيات المخصصة)
    original_entities = list(event.message.entities or [])
    
    # إنشاء entity جديد للتنسيق
    new_entity = None
    
    if gvarstatus("bold"):
        new_entity = MessageEntityBold(offset=0, length=len(text))
    elif gvarstatus("tshwesh"):
        new_entity = MessageEntityStrike(offset=0, length=len(text))
    elif gvarstatus("ramz"):
        new_entity = MessageEntityCode(offset=0, length=len(text))
    elif gvarstatus("joker"):
        new_entity = MessageEntityPre(offset=0, length=len(text), language="")
    
    if new_entity:
        # دمج الـ entities الجديدة مع القديمة
        all_entities = [new_entity] + original_entities
        
        try:
            await event.edit(text, formatting_entities=all_entities)
        except:
            pass
