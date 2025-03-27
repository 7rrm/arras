from telethon import events, types
from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete
from telethon.errors.rpcerrorlist import MessageIdInvalidError

# استيراد محولات التنسيق من telethon
from telethon.extensions import markdown, html

class CustomParseMode:
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'markdown':
            text, entities = markdown.parse(text)
        elif self.parse_mode == 'html':
            text, entities = html.parse(text)
        else:
            raise ValueError("Invalid parse mode")

        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
        return text, entities

    @staticmethod
    def unparse(text, entities):
        return html.unparse(text, entities)

# أوامر الخطوط الأساسية
@l313l.on(admin_cmd(pattern="(خط الغامق|خط غامق)"))
async def bold_toggle(event):
    if not gvarstatus("bold"):
        addgvar("bold", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الغامق بنجاح ✓**")
    else:
        delgvar("bold")
        await edit_delete(event, "**᯽︙ تم إيقاف خط الغامق ✓**")

# ... (بقية أوامر الخطوط بنفس النمط)

@l313l.on(admin_cmd(pattern="(خط التشويش|خط تشويش|تفعيل تشويش|تفعيل التشويش)"))
async def spoiler_toggle(event):
    if not gvarstatus("cllear"):
        addgvar("cllear", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط التشويش بنجاح ✓**")
    else:
        await edit_delete(event, "**᯽︙ خط التشويش مفعل بالفعل ✓**")

@l313l.on(admin_cmd(pattern="(تعطيل تشويش|تعطيل التشويش)"))
async def spoiler_disable(event):
    if gvarstatus("cllear"):
        delgvar("cllear")
        await edit_delete(event, "**᯽︙ تم تعطيل خط التشويش بنجاح ✓**")
    else:
        await edit_delete(event, "**᯽︙ خط التشويش معطل بالفعل ✓**")

@l313l.on(events.NewMessage(outgoing=True))
async def handle_all_messages(event):
    if not event.message.text or event.message.media:
        return
        
    text = event.message.text
    modified = False
    
    # تجنب تنفيذ الأوامر التي تبدأ بنقطة
    if text.startswith('.'):
        return
    
    # تطبيق كافة التنسيقات
    if gvarstatus("bold"):
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
        
    if gvarstatus("cllear") and not modified:
        try:
            await event.delete()
            await event.respond(
                f"`‹` {text} `›`",
                parse_mode="markdown",
                spoiler=True
            )
            return
        except Exception as e:
            print(f"Error: {e}")
            return
        
    if modified:
        try:
            await event.edit(text)
        except MessageIdInvalidError:
            pass
