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
    zid = gvarstatus("ZThon_Vip")
    if zid is None and Zel_Uid not in Zed_Dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    
    if zid is not None:
        zid = int(zid)
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

@l313l.on(events.NewMessage(func=lambda e: e.is_private and (e.audio or e.voice) and e.media_unread)
async def sddm(event):
    global vocself
    if not vocself:  # إذا كانت ميزة الحفظ معطلة
        return
    
    # تحقق من صلاحية VIP
    zid = gvarstatus("ZThon_Vip")
    if zid is None and Zel_Uid not in Zed_Dev:
        return
    
    if zid is not None:
        if Zel_Uid != int(zid):
            return
    
    # تجنب حفظ الرسائل المرسلة من نفس المستخدم
    if event.sender_id == l313l.uid:
        return
    
    try:
        sender = await event.get_sender()
        username = f"@{sender.username}" if sender.username else "لا يوجد"
        
        # تحميل الملف الصوتي
        voc = await event.download_media()
        
        # إرسال الملف مع المعلومات
        await l313l.send_file(
            "me",
            voc,
            caption=(
                f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حفـظ البصمه الذاتيه 🎙](t.me/ZThon)\n"
                f"⋆─┄─┄─┄─┄─┄─┄─⋆\n"
                f"**⌔ مࢪحبـاً .. عـزيـزي 🫂\n"
                f"⌔ تـم حفظ البصمه الذاتية .. تلقائياً ☑️** ❝\n"
                f"**⌔ معلومـات المـرسـل :-**\n"
                f"**• الاسم :** {sender.first_name}\n"
                f"**• اليوزر :** {username}\n"
                f"**• الايدي :** `{sender.id}`"
            )
        )
    except Exception as e:
        print(f"حدث خطأ أثناء حفظ البصمة: {e}")
