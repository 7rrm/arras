
import json
import requests
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.types import MessageEntityMentionName

from . import l313l
from ..Config import Config
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        if isinstance(user, int) or user.startswith("@"):
            user_obj = await event.client.get_entity(user)
            return user_obj
        try:
            user_object = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_object

async def zzz_info(zthon_user, event):
    FullUser = (await event.client(GetFullUserRequest(zthon_user.id))).full_user
    first_name = zthon_user.first_name
    full_name = FullUser.private_forward_name
    user_id = zthon_user.id
    username = zthon_user.username
    first_name = first_name.replace("\u2060", "") if first_name else None
    full_name = full_name or first_name
    username = "@{}".format(username) if username else "None"
    return user_id, full_name, username

@l313l.ar_cmd(pattern="اهمس(?: |$)(.*)")
async def repozedub(event):
    user = event.pattern_match.group(1)
    if not user and not event.reply_to_msg_id:
        return

    zthon_user = await get_user_from_event(event)
    try:
        user_id, full_name, username = await zzz_info(zthon_user, event)
    except (AttributeError, TypeError):
        return

    # حفظ بيانات المستلم
    delgvar("hmsa_id")
    delgvar("hmsa_name")
    delgvar("hmsa_user")
    addgvar("hmsa_id", user_id)
    addgvar("hmsa_name", full_name)
    addgvar("hmsa_user", username)

    # ✅ حسابك يرسل رسالة "جاري التحميل..."
    await event.edit("⏱️ جاري تجهيز الهمسة...")

    # 📝 نص الرسالة - بدون إيموجي بريميوم
    text = f"""
📨 <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<b>⌔╎لـ إرسال همسة سريّة إلى</b> {username or full_name} 💌
"""

    # 🎨 الأزرار الملونة - بدون إيموجي بريميوم داخل الزر
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "✍️ اضغط لكتابة الهمسة 📨",
                    "switch_inline_query_current_chat": f"secret {user_id} \n",
                    "style": "primary"  # 🔵 أزرق فقط - بدون icon_custom_emoji_id
                }
            ],
            [
                {
                    "text": "🔥 همسة سريعة",
                    "switch_inline_query_current_chat": f"secret {user_id} \nمرحبا",
                    "style": "success"  # 🟢 أخضر فقط - بدون icon_custom_emoji_id
                }
            ]
        ]
    }

    # ✅ إرسال الرسالة عبر Bot API - تظهر كأن حسابك أرسلها!
    send_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/sendMessage"
    send_data = {
        "chat_id": event.chat_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(keyboard),
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(send_url, json=send_data)
        if response.status_code == 200:
            await event.delete()  # حذف رسالة "جاري التحميل..."
            LOGS.info(f"✅ تم إرسال همسة إلى {username or full_name}")
        else:
            await event.edit("❌ حدث خطأ في الإرسال")
            LOGS.error(f"❌ خطأ: {response.text}")
    except Exception as e:
        await event.edit("❌ حدث خطأ، حاول مرة أخرى")
        LOGS.error(f"❌ خطأ: {e}")
