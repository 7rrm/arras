from JoKeRUB import l313l
from telethon import events
from ..Config import Config
from ..sql_helper.globals import gvarstatus, addgvar, delgvar
from ..utils import Zed_Dev

Zel_Uid = l313l.uid
vocself = True

@l313l.ar_cmd(pattern="(تفعيل البصمه الذاتيه|تفعيل البصمه الذاتية|تفعيل البصمة الذاتيه|تفعيل البصمة الذاتية)")
async def start_datea(event):
    global vocself
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in Zed_Dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    zid = int(gvarstatus("ZThon_Vip"))
    if Zel_Uid != zid:
        return
    if vocself:
        return await edit_or_reply(event, "**⎉╎حفظ البصمه الذاتية التلقائي 🎙**\n**⎉╎مفعلـه .. مسبقـاً ✅**")
    vocself = True
    await edit_or_reply(event, "**⎉╎تم تفعيل حفظ البصمه الذاتية 🎙**\n**⎉╎تلقائياً .. بنجاح ✅**")

@l313l.ar_cmd(pattern="(تعطيل البصمه الذاتيه|تعطيل البصمه الذاتية|تعطيل البصمة الذاتيه|تعطيل البصمة الذاتية)")
async def stop_datea(event):
    global vocself
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in Zed_Dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @Lx5x5 .**")
    zid = int(gvarstatus("ZThon_Vip"))
    if Zel_Uid != zid:
        return
    if vocself:
        vocself = False
        return await edit_or_reply(event, "**⎉╎تم تعطيل حفظ البصمه الذاتية 🎙**\n**⎉╎الان صارت مو شغالة .. ✅**")
    await edit_or_reply(event, "**⎉╎حفظ البصمه الذاتية التلقائي 🎙**\n**⎉╎معطلـه .. مسبقـاً ✅**")

@l313l.on(events.NewMessage(func=lambda e: e.is_private and (e.audio or e.voice) and e.media_unread))
async def sddm(event):
    global vocself
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in Zed_Dev:
        return
    zelzal = event.sender_id
    malath = l313l.uid
    if zelzal == malath:
        return
    zid = int(gvarstatus("ZThon_Vip")) if gvarstatus("ZThon_Vip") else 0
    if Zel_Uid != zid:
        return
    if vocself:
        sender = await event.get_sender()
        username = f"@{sender.username}" if sender.username else "لا يوجد"
        chat = await event.get_chat()
        voc = await event.download_media()
        await l313l.send_file("me", voc, caption=f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حفـظ البصمه الذاتيه 🎙](t.me/lx5x5)\n⋆─┄─┄─┄─┄─┄─┄─⋆\n**⌔ مࢪحبـاً .. عـزيـزي 🫂\n⌔ تـم حفظ البصمه الذاتية .. تلقائياً ☑️** ❝\n**⌔ معلومـات المـرسـل :-**\n**• الاسم :** {_format.mentionuser(sender.first_name , sender.id)}\n**• اليوزر :** {username}\n**• الايدي :** `{sender.id}`")
