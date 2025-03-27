from telethon import events
from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete
from telethon import functions
from telethon.errors.rpcerrorlist import MessageIdInvalidError

class CustomParseMode:
    """
    Example using Markdown:

    - client.send_message('me', 'hello this is a [Text](spoiler), with custom emoji [❤️](emoji/10002345) !')

    Example using HTML:

    - client.send_message('me', 'hello this is a <a href="spoiler">Text</a>, with custom emoji <a href="emoji/10002345">❤️</a> !')

    `Sending spoilers and custom emoji <https://github.com/LonamiWebs/Telethon/wiki/Sending-more-than-just-messages#sending-spoilers-and-custom-emoji>`_
    :param parse_mode: The format to use for parsing text.
                       Can be either 'markdown' for Markdown formatting
                       or 'html' for HTML formatting.
    """
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'markdown':
            text, entities = markdown.parse(text)
        elif self.parse_mode == 'html':
            text, entities = html.parse(text)
        else:
            raise InvalidFormatException("Invalid parse mode. Choose either Markdown or HTML.")

        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith('emoji/'):
                    entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, int(e.url.split('/')[1]))
        return text, entities

    @staticmethod
    def unparse(text, entities):
        for i, e in enumerate(entities or []):
            if isinstance(e, types.MessageEntityCustomEmoji):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, f'emoji/{e.document_id}')
            if isinstance(e, types.MessageEntitySpoiler):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, 'spoiler')
        return html.unparse(text, entities)

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

@l313l.on(admin_cmd(pattern="(خط التشويش|خط تشويش|تفعيل تشويش|تفعيل التشويش)"))
async def _(event):
    is_cllear = gvarstatus("cllear")
    if not is_cllear:
        addgvar ("cllear", "on")
        await edit_delete(event, "**⎉╎تم تفعيـل خـط التشـويش .. بنجـاح ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل تشويش) **")
        return
    if is_cllear:
        await edit_delete(event, "**⎉╎خـط التشـويش مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل تشويش) **")
        return

@l313l.on(admin_cmd(pattern="(تعطيل تشويش|تعطيل التشويش)"))
async def _(event):
    is_cllear = gvarstatus("cllear")
    if is_cllear:
        delgvar("cllear")
        await edit_delete(event, "**⎉╎تم تعطيـل خـط التشـويش .. بنجـاح ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل تشويش) **")
        return
    if not is_cllear:
        await edit_delete(event, "**⎉╎خـط التشـويش مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل تشويش) **")
        return


@l313l.on(events.NewMessage(outgoing=True))
async def comming(event):
    if event.message.text and not event.message.media and "." not in event.message.text:
        is_cllear = gvarstatus("cllear")
        if is_cllear:
            try:
                await event.edit(f"[{event.message.text}](spoiler)", parse_mode=CustomParseMode("markdown"))
            except MessageIdInvalidError:
                pass
