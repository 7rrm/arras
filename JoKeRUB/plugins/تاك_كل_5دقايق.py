# By Reda for JoKeRUB
# Tel: @rd0r0
from JoKeRUB import l313l
import asyncio
import time
import random
from ..core.managers import edit_or_reply
from telethon import events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

spam_chats = []
mention_in_progress = False

# رابط القناة التي تحتوي على الكليشات (يجب أن تكون عامة أو البوت عضو فيها)
CLIPS_CHANNEL = "https://t.me/dev_karar"  # قم بتغيير الرابط إلى رابط قناتك

async def get_clips():
    """
    جلب الكليشات من القناة المحددة.
    """
    clips = []
    try:
        async for message in l313l.iter_messages(CLIPS_CHANNEL):
            if message.text:  # التأكد من أن الرسالة تحتوي على نص
                clips.append(message.text)
        print(f"تم جلب الكليشات: {clips}")  # طباعة الكليشات
    except Exception as e:
        print(f"حدث خطأ أثناء جلب الكليشات: {e}")
    return clips

@l313l.ar_cmd(pattern="منشن_كل_5دقايق(?:\s|$)([\s\S]*)")
async def menall(event):
    print("تم استدعاء أمر المنشن!")  # طباعة رسالة تصحيح
    chat_id = event.chat_id
    if event.is_private:
        print("الحدث في محادثة خاصة!")  # طباعة رسالة تصحيح
        return await edit_or_reply(event, "** ᯽︙ هذا الامر يستعمل للقنوات والمجموعات فقط !**")
    msg = event.pattern_match.group(1)
    if not msg:
        print("لم يتم تقديم رسالة!")  # طباعة رسالة تصحيح
        return await edit_or_reply(event, "** ᯽︙ ضع رسالة للمنشن اولاً**")
    is_admin = False
    try:
        partici_ = await l313l(GetParticipantRequest(
          event.chat_id,
          event.sender_id
        ))
    except UserNotParticipantError:
        is_admin = False
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ''
    clips = await get_clips()  # جلب الكليشات من القناة
    if not clips:
        return await edit_or_reply(event, "** ᯽︙ لم يتم العثور على كليشات في القناة المحددة!**")
    async for usr in l313l.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        # اختيار كليشة عشوائية من القائمة
        clip = random.choice(clips)
        usrtxt = f"{clip} [{usr.first_name}](tg://user?id={usr.id})"
        await l313l.send_message(chat_id, usrtxt)
        await asyncio.sleep(60)  # انتظار 5 دقائق
    try:
        spam_chats.remove(chat_id)
    except:
        pass

@l313l.ar_cmd(pattern="الغاء_منشن_كل_5دقايق")
async def ca_sp(event):
  if not event.chat_id in spam_chats:
    return await edit_or_reply(event, "** ᯽︙ 🤷🏻 لا يوجد منشن لألغائه**")
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await edit_or_reply(event, "** ᯽︙ تم الغاء المنشن بنجاح ✓**")
