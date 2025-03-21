from asyncio import sleep
from JoKeRUB import l313l
from JoKeRUB.core.logger import logging
from telethon import events

plugin_category = "tools"
LOGS = logging.getLogger(__name__)

# متغير لتخزين الوقت المحدد لحذف الرسائل
delete_delay = None

# ----------------------------------------
# الأمر: مؤقت (لحذف رسالة واحدة بعد وقت محدد)
# ----------------------------------------
@l313l.ar_cmd(
    pattern="مؤقت (\d*) ([\s\S]*)",
    command=("مؤقت", plugin_category),
    info={
        "شـرح": "لأرسـال رسـالة موقوتة وحـذفها بعـد وقت معيـن انت تضعـه",
        "⌔︙أسـتخدام": "{tr}مؤقت [الوقت] [النص]",
        "᯽︙ امثـلة": "{tr}مؤقت 10 ههلا",
    },
)
async def selfdestruct(destroy):
    "لأرسـال رسـالة مـوقوتة"
    cat = ("".join(destroy.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = cat[1]
    ttl = int(cat[0])
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, message)
    await sleep(ttl)
    await smsg.delete()

# ----------------------------------------
# الأمر: ضبط_المؤقت (لحذف جميع الرسائل بعد وقت محدد)
# ----------------------------------------
@l313l.ar_cmd(
    pattern="ضبط_المؤقت (\d+)",
    command=("ضبط_المؤقت", plugin_category),
    info={
        "شـرح": "لضبط الوقت الذي ستُحذف بعده جميع الرسائل تلقائيًا",
        "⌔︙أسـتخدام": "{tr}ضبط_المؤقت [الوقت بالثواني]",
        "᯽︙ امثـلة": "{tr}ضبط_المؤقت 10",
    },
)
async def set_auto_delete_timer(event):
    "لضبط الوقت الذي ستُحذف بعده جميع الرسائل تلقائيًا"
    global delete_delay
    try:
        delete_delay = int(event.pattern_match.group(1))
        await event.edit(f"**⌔︙ تم ضبط المؤقت لـ {delete_delay} ثانية. سيتم حذف جميع الرسائل بعد هذا الوقت.**")
    except ValueError:
        await event.edit("**⌔︙ يرجى إدخال رقم صحيح للوقت.**")

# ----------------------------------------
# الأمر: تعطيل_المؤقت (لإيقاف حذف الرسائل التلقائي)
# ----------------------------------------
@l313l.ar_cmd(
    pattern="تعطيل_المؤقت",
    command=("تعطيل_المؤقت", plugin_category),
    info={
        "شـرح": "لتعطيل المؤقت وحذف الرسائل التلقائي",
        "⌔︙أسـتخدام": "{tr}تعطيل_المؤقت",
    },
)
async def disable_auto_delete(event):
    "لتعطيل المؤقت وحذف الرسائل التلقائي"
    global delete_delay
    delete_delay = None
    await event.edit("**⌔︙ تم تعطيل المؤقت. لن يتم حذف الرسائل تلقائيًا.**")

# ----------------------------------------
# الوظيفة التلقائية لحذف الرسائل
# ----------------------------------------
@l313l.on(events.NewMessage(outgoing=True))
async def auto_delete_messages(event):
    "لحذف الرسائل تلقائيًا بعد الوقت المحدد"
    global delete_delay
    if delete_delay is not None:
        await sleep(delete_delay)
        try:
            await event.delete()
        except Exception as e:
            LOGS.error(f"حدث خطأ أثناء حذف الرسالة: {e}")
            
