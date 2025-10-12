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
    # التحقق من وجود نص في الرسالة
    if not event.message.text:
        return
    
    # تجاهل الرسائل التي تحتوي على وسائط (صور/فيديو/إلخ)
    if event.message.media:
        return
        
    text = event.message.text
    
    # تجاهل الأوامر التي تبدأ بنقطة
    if text.startswith('.'):
        return
    
    # التحقق من وجود نمط تنسيق مفعل
    format_entity = None
    
    if gvarstatus("bold"):
        format_entity = MessageEntityBold(offset=0, length=len(text))
    elif gvarstatus("tshwesh"):
        format_entity = MessageEntityStrike(offset=0, length=len(text))
    elif gvarstatus("ramz"):
        format_entity = MessageEntityCode(offset=0, length=len(text))
    elif gvarstatus("joker"):
        format_entity = MessageEntityPre(offset=0, length=len(text), language="")
    
    # إذا لم يكن هناك تنسيق مفعل، لا تفعل شيء
    if not format_entity:
        return
    
    # الحصول على جميع الـ entities الأصلية (بما في ذلك الإيموجيات المخصصة)
    original_entities = []
    if event.message.entities:
        original_entities = list(event.message.entities)
    
    # دمج entity التنسيق مع الـ entities الأصلية
    # نضع entity التنسيق أولاً لأنه يغطي كامل النص
    all_entities = [format_entity] + original_entities
    
    try:
        # تحديث الرسالة مع الحفاظ على جميع الـ entities
        await event.edit(text, formatting_entities=all_entities)
    except Exception as e:
        # في حالة حدوث خطأ، يمكنك طباعة الخطأ للتشخيص
        # أو تجاهله بصمت
        pass
