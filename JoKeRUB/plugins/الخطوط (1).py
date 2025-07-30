from telethon import events
from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete
import re

# --- أوامر تفعيل وإيقاف جميع الخطوط ---
@l313l.on(events.NewMessage(pattern=r"^(خط الغامق|خط غامق)$"))
async def bold_toggle(event):
    if not gvarstatus("bold"):
        addgvar("bold", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الغامق بنجاح ✓**")
    else:
        delgvar("bold")
        await edit_delete(event, "**᯽︙ تم إيقاف خط الغامق ✓**")

@l313l.on(events.NewMessage(pattern=r"^(خط المشطوب|خط مشطوب)$"))
async def strikethrough_toggle(event):
    if not gvarstatus("tshwesh"):
        addgvar("tshwesh", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط المشطوب ✓**")
    else:
        delgvar("tshwesh")
        await edit_delete(event, "**᯽︙ تم إيقاف خط المشطوب ✓**")

@l313l.on(events.NewMessage(pattern=r"^(خط الرمز|خط رمز)$"))
async def monospace_toggle(event):
    if not gvarstatus("ramz"):
        addgvar("ramz", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الرمز ✓**")
    else:
        delgvar("ramz")
        await edit_delete(event, "**᯽︙ تم إيقاف خط الرمز ✓**")

@l313l.on(events.NewMessage(pattern=r"^(خط الجوكر|خط جوكر)$"))
async def joker_toggle(event):
    if not gvarstatus("joker"):
        addgvar("joker", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الجوكر ✓**")
    else:
        delgvar("joker")
        await edit_delete(event, "**᯽︙ تم إيقاف خط الجوكر ✓**")

# --- معالج النصوص (يطبق التنسيق على النص فقط ويحافظ على الإيموجي) ---
@l313l.on(events.NewMessage(outgoing=True))
async def handle_text_formatting(event):
    if not event.message.text or event.message.media:
        return
        
    text = event.message.text
    modified = False
    
    # تطبيق خط الغامق (على النص فقط دون الإيموجي)
    if gvarstatus("bold"):
        parts = re.split(r'([\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251\U0001f926-\U0001f937\U0001F1E0-\U0001F1FF]+|\s+)', text)
        new_text = []
        for part in parts:
            if part and not re.match(r'^[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251\U0001f926-\U0001f937\U0001F1E0-\U0001F1FF\s]+$', part):
                new_text.append(f"**{part}**")
            else:
                new_text.append(part)
        text = ''.join(new_text)
        modified = True
    
    # تطبيق خط المشطوب (على النص كاملاً)
    elif gvarstatus("tshwesh"):
        text = f"~~{text}~~"
        modified = True
        
    # تطبيق خط الرمز (على النص كاملاً)
    elif gvarstatus("ramz"):
        text = f"`{text}`"
        modified = True
        
    # تطبيق خط الجوكر (على النص كاملاً)
    elif gvarstatus("joker"):
        text = f"```{text}```"
        modified = True
        
    if modified:
        try:
            await event.edit(text)
        except MessageIdInvalidError:
            pass
        except Exception as e:
            print(f"Error: {e}")
