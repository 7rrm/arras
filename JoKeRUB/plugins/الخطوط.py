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
from telethon.extensions import html, markdown

# ========== كلاس التحليل المخصص ==========
class CustomParseMode:
    def __init__(self, parse_mode):
        self.parse_mode = parse_mode
    
    def parse(self, text):
        text, entities = html.parse(text)  # ⚡ مباشرة HTML
        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith('emoji/'):
                    entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, int(e.url.split('/')[1]))
        return text, entities

# ========== أوامر التحكم ==========
@l313l.on(admin_cmd(pattern="(خط مزخرف|تفعيل خط مزخرف)"))
async def enable_decorative_line(event):
    if not gvarstatus("decorative_line"):
        addgvar("decorative_line", "on")
        await edit_delete(event, "**⎉╎تم تفعيل خط المزخرف مع التشويش ✓**")
    else:
        await edit_delete(event, "**⎉╎خط المزخرف مفعل مسبقاً ✓**")

@l313l.on(admin_cmd(pattern="(تعطيل خط مزخرف|إيقاف خط مزخرف)"))
async def disable_decorative_line(event):
    if gvarstatus("decorative_line"):
        delgvar("decorative_line")
        await edit_delete(event, "**⎉╎تم تعطيل خط المزخرف ✓**")
    else:
        await edit_delete(event, "**⎉╎خط المزخرف معطل مسبقاً ✓**")

# ========== المعالج الرئيسي ==========
@l313l.on(events.NewMessage(outgoing=True))
async def handle_decorative_spoiler(event):
    if not event.message.text or event.message.media or event.message.text.startswith('.'):
        return
    
    if not gvarstatus("decorative_line"):
        return
    
    text = event.message.text
    
    # إيموجيات مباشرة في الكود بدون متغيرات
    decorated_text = (
        f'<a href="emoji/5447181973544008180">✨</a> '  # إيموجي قبل
        f'<a href="spoiler">{text}</a> '                # نص مشوش
        f'<a href="emoji/5447389832781264371">✨</a>'   # إيموجي بعد
    )
    
    parser = CustomParseMode("html")
    parsed_text, entities = parser.parse(decorated_text)
    
    await event.edit(
        parsed_text,
        parse_mode=None,
        formatting_entities=entities
    )
