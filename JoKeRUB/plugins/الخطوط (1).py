from telethon import events
from JoKeRUB import l313l
from ..sql_helper.globals import gvarstatus
from ..core.managers import edit_delete
from telethon.errors import MessageIdInvalidError
import re

async def apply_formatting(text, format_type):
    """تطبيق التنسيق على النص مع تجاهل الإيموجي المميز"""
    # فصل النص عن الإيموجي المميز (باستخدام تعبير منتظم)
    parts = re.split(r'(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])', text)
    
    formatted_text = ""
    for part in parts:
        if part.strip():  # إذا كان الجزء نصًا وليس فراغًا
            if format_type == "bold":
                formatted_text += f"**{part}**"
            elif format_type == "strikethrough":
                formatted_text += f"~~{part}~~"
            elif format_type == "monospace":
                formatted_text += f"`{part}`"
            elif format_type == "joker":
                formatted_text += f"```{part}```"
        else:
            formatted_text += part  # إذا كان إيموجي، نضيفه كما هو
    
    return formatted_text

@l313l.on(events.NewMessage(outgoing=True))
async def handle_text_formatting(event):
    if not event.message.text or event.message.media:
        return
        
    text = event.message.text
    modified = False
    formatted_text = text
    
    # التحقق من نوع التنسيق المطلوب
    if gvarstatus("bold"):
        formatted_text = await apply_formatting(text, "bold")
        modified = True
    elif gvarstatus("tshwesh"):
        formatted_text = await apply_formatting(text, "strikethrough")
        modified = True
    elif gvarstatus("ramz"):
        formatted_text = await apply_formatting(text, "monospace")
        modified = True
    elif gvarstatus("joker"):
        formatted_text = await apply_formatting(text, "joker")
        modified = True
        
    if modified:
        try:
            await event.edit(formatted_text)
        except MessageIdInvalidError:
            pass
        except Exception as e:
            print(f"Error: {e}")
