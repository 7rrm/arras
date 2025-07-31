from telethon import events
from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete
from telethon import functions
from telethon.errors.rpcerrorlist import MessageIdInvalidError

# أوامر التفعيل/الإيقاف (تبقى كما هي بدون تغيير)
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
    formatting_applied = False
    
    # حفظ الإيموجي المميز قبل التنسيق
    original_entities = event.message.entities or event.message.raw_text_entities
    
    # تطبيق التنسيقات حسب الأولوية
    if gvarstatus("bold"):
        text = f"**{text}**"
        modified = True
        formatting_applied = True
        
    elif gvarstatus("tshwesh"):
        text = f"~~{text}~~"
        modified = True
        formatting_applied = True
        
    elif gvarstatus("ramz"):
        text = f"`{text}`"
        modified = True
        formatting_applied = True
        
    elif gvarstatus("joker"):
        text = f"```{text}```"
        modified = True
        formatting_applied = True
        
    if modified:
        try:
            # إذا كان هناك تنسيق ولكن النص يحتوي على كيانات (مثل إيموجي مميز)
            if original_entities and formatting_applied:
                # إرسال الرسالة بدون parse_mode للحفاظ على الكيانات الأصلية
                await event.edit(text, parse_mode=None)
            else:
                # إرسال الرسالة مع التنسيق العادي
                await event.edit(text)
        except MessageIdInvalidError:
            pass
        except Exception as e:
            print(f"خطأ في تعديل الرسالة: {e}")
