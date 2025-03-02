"""
JoKeRUB team ©
By Reda
sub Hussein
"""
import os
from datetime import datetime
from gtts import gTTS
from JoKeRUB import l313l
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "utils"

@l313l.ar_cmd(pattern="تكلم(?:\s|$)([\s\S]*)",
               command=("تكلم", plugin_category),
              )
async def _(event):
    "تحويل النص إلى كلام بصوت رجل."

    start = datetime.now()
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    
    if not input_str and not reply:
        return await edit_delete(event, "**᯽︙ يجب عليك إدخال نص أو الرد على رسالة تحتوي على نص.**")
    
    if reply:
        input_str = reply.text
    
    if not input_str:
        return await edit_delete(event, "**�︙ لا يوجد نص لتحويله إلى كلام.**")
    
    jepevent = await edit_or_reply(event, "**᯽︙ يجري تحويل النص إلى كلام...**")
    
    try:
        tts = gTTS(text=input_str, lang='ar', slow=False)
        tts.save("output.mp3")
    except Exception as e:
        return await edit_delete(event, f"**᯽︙ حدث خطأ أثناء تحويل النص إلى كلام:**\n{e}")
    
    end = datetime.now()
    ms = (end - start).seconds
    
    await event.client.send_file(event.chat_id, "output.mp3", voice_note=True)
    await jepevent.edit(f"**᯽︙ تم تحويل النص إلى كلام بنجاح في {ms} ثانية.**")
    
    os.remove("output.mp3")
