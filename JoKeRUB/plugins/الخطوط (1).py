from telethon import events
from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete
from telethon import functions
from telethon.errors.rpcerrorlist import MessageIdInvalidError

# جميع أوامر التفعيل/الإيقاف تبقى كما هي
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
    
    # التحقق مما إذا كان النص يحتوي على إيموجي بريميوم
    has_premium_emoji = any(
        getattr(entity, 'premium', False)
        for entity in (event.message.entities or [])
    )
    
    if has_premium_emoji:
        return  # لا تطبق أي تنسيق إذا كان هناك إيموجي بريميوم
    
    # تطبيق التنسيقات إذا لم يكن هناك إيموجي بريميوم
    if gvarstatus("bold"):
        if not text.startswith('.') and '.' not in text[:-1]:
            text = f"**{text}**"
            modified = True
            
    if gvarstatus("tshwesh") and not modified:
        text = f"~~{text}~~"
        modified = True
        
    if gvarstatus("ramz") and not modified:
        text = f"`{text}`"
        modified = True
        
    if gvarstatus("joker") and not modified:
        text = f"```{text}```"
        modified = True
        
    if modified:
        try:
            await event.edit(text)
        except MessageIdInvalidError:
            pass
        except Exception as e:
            print(f"Error editing message: {e}")
