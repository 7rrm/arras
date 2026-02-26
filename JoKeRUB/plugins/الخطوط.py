from telethon import events, types
from JoKeRUB import l313l
from ..sql_helper.globals import gvarstatus, addgvar, delgvar
from ..core.managers import edit_delete

# ========== تخزين مؤقت للسرعة ==========
_FORMAT_CACHE = {}

# ========== أوامر التحكم السريعة ==========
@l313l.on(admin_cmd(pattern="(خط الغامق|خط غامق)"))
async def bold_toggle(event):
    key = "bold"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الغامق بنجاح ✓**", 1)
    else:
        delgvar(key)
        await edit_delete(event, "**᯽︙ تم إيقاف خط الغامق ✓**", 1)

@l313l.on(admin_cmd(pattern="(خط المشطوب|خط مشطوب)"))
async def strikethrough_toggle(event):
    key = "tshwesh"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط المشطوب ✓**", 1)
    else:
        delgvar(key)
        await edit_delete(event, "**᯽︙ تم إيقاف خط المشطوب ✓**", 1)

@l313l.on(admin_cmd(pattern="(خط رمز|خط الرمز)"))
async def monospace_toggle(event):
    key = "ramz"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الرمز ✓**", 1)
    else:
        delgvar(key)
        await edit_delete(event, "**᯽︙ تم إيقاف خط الرمز ✓**", 1)

@l313l.on(admin_cmd(pattern="(خط الجوكر|خط جوكر)"))
async def joker_toggle(event):
    key = "joker"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الجوكر ✓**", 1)
    else:
        delgvar(key)
        await edit_delete(event, "**᯽︙ تم إيقاف خط الجوكر ✓**", 1)

@l313l.on(admin_cmd(pattern="(خط مزخرف|تفعيل خط مزخرف)"))
async def enable_decorative(event):
    key = "decorative_line"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**⎉╎تم تفعيل خط المزخرف مع التشويش ✓**", 1)
    else:
        await edit_delete(event, "**⎉╎خط المزخرف مفعل مسبقاً ✓**", 1)

@l313l.on(admin_cmd(pattern="(تعطيل خط مزخرف|إيقاف خط مزخرف)"))
async def disable_decorative(event):
    key = "decorative_line"
    if gvarstatus(key):
        delgvar(key)
        await edit_delete(event, "**⎉╎تم تعطيل خط المزخرف ✓**", 1)
    else:
        await edit_delete(event, "**⎉╎خط المزخرف معطل مسبقاً ✓**", 1)

# ========== المعالج السريع الموحد ==========
@l313l.on(events.NewMessage(outgoing=True))
async def fast_text_formatting(event):
    if not event.message.text or event.message.media or event.message.text.startswith('.'):
        return
    
    text = event.message.text
    modified = False
    
    # التحقق السريع من الخطوط العادية (بنفس الترتيب)
    if gvarstatus("bold"):
        text = f"**{text}**"
        modified = True
    elif gvarstatus("tshwesh"):
        text = f"~~{text}~~"
        modified = True
    elif gvarstatus("ramz"):
        text = f"`{text}`"
        modified = True
    elif gvarstatus("joker"):
        text = f"```{text}```"
        modified = True
    elif gvarstatus("decorative_line"):
        # خط مزخرف سريع بدون كلاسات
        decorated = f'<a href="emoji/5447181973544008180">✨</a> <a href="spoiler">{text}</a> <a href="emoji/5447389832781264371">✨</a>'
        text, entities = html.parse(decorated)
        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith('emoji/'):
                    entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, int(e.url.split('/')[1]))
        await event.edit(text, parse_mode=None, formatting_entities=entities)
        return
    
    if modified:
        try:
            await event.edit(text)
        except:
            pass
