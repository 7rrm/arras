from telethon import events
from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete
from telethon import functions
from telethon.errors.rpcerrorlist import MessageIdInvalidError

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
    
    # التحقق من جميع أنواع الخطوط
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
        except:
            pass
            
#########################
from telethon import events, types
from JoKeRUB import l313l
from ..sql_helper.globals import gvarstatus, addgvar, delgvar
from ..core.managers import edit_delete
from telethon.extensions import html

DECORATIVE_EMOJI_ID = "5447181973544008180"  # إيموجي قبل النص
DECORATIVE_EMOJII_ID = "5447389832781264371"  # إيموجي بعد النص

# ========== الأمر الرئيسي ==========
@l313l.on(admin_cmd(pattern="تشويش مزخرف"))
async def toggle_spoiler_decor(event):
    if not gvarstatus("spoiler_decor"):
        addgvar("spoiler_decor", "on")
        await edit_delete(event, "**✓ تم تفعيل التشويش المزخرف**")
    else:
        delgvar("spoiler_decor")
        await edit_delete(event, "**✗ تم تعطيل التشويش المزخرف**")

# ========== المعالج السريع ==========
@l313l.on(events.NewMessage(outgoing=True))
async def fast_decor_spoiler(event):
    if not event.message.text or event.message.media or event.message.text.startswith('.'):
        return
    
    if gvarstatus("spoiler_decor"):
        text = event.message.text
        formatted = f'<a href="emoji/{DECORATIVE_EMOJI_ID}">✨</a><tg-spoiler>{text}</tg-spoiler><a href="emoji/{DECORATIVE_EMOJII_ID}">✨</a>\nهذا يأتي بعد النص'
        
        try:
            await event.edit(formatted, parse_mode="html")
        except:
            try:
                simple = f"✨ [{text}](spoiler) ✨\nهذا يأتي بعد النص"
                await event.edit(simple, parse_mode="markdown")
            except:
                pass
