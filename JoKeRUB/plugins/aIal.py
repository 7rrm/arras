import random
import requests
import time
import asyncio
from asyncio import sleep
import telethon
from telethon.sync import functions
from telethon.errors import FloodWaitError
from user_agent import generate_user_agent

from . import l313l
from ..core.managers import edit_delete, edit_or_reply

trys = [0]
crys = [0]
arys = [0]
brys = [0]
itsclim = ["off"]
iscuto = ["off"]
istuto = ["off"]
isbuto = ["off"]

async def gen_meaningful_username():
    # اختيار كلمة عشوائية من القائمة
    word = random.choice(meaningful_words)
    # إرجاع الكلمة بدون إضافة أرقام
    return word

async def check_user(username):
    url = "https://t.me/" + str(username)
    headers = {
        "User-Agent": generate_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    response = requests.get(url, headers=headers)
    if (
        response.text.find(
            'If you have <strong>Telegram</strong>, you can contact <a class="tgme_username_link"'
        )
        >= 0
    ):
        return True
    else:
        return False

async def checker_user(username):
    url = "https://t.me/" + str(username)
    headers = {
        "User-Agent": generate_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    response = requests.get(url, headers=headers)
    if (
        response.text.find(
            'If you have <strong>Telegram</strong>, you can contact <a class="tgme_username_link"'
        )
        >= 0
    ):
        return True
    else:
        return False

@l313l.ar_cmd(pattern="نقل_قناة")
async def transfer_to_channel(event):
    # الحصول على اليوزر الحالي للحساب
    current_username = f"@{l313l.me.username}" if l313l.me.username else None
    if not current_username:
        return await edit_or_reply(event, "**⎉╎حسـابك لا يمتلك يـوزر حاليـاً ❌**")

    try:
        # إزالة اليوزر من الحساب أولًا
        await l313l(functions.account.UpdateUsernameRequest(username=""))

        # إنشاء قناة جديدة
        ch = await l313l(
            functions.channels.CreateChannelRequest(
                title="القنـاة الجديـدة",
                about=f"تم نقـل اليـوزر بواسطـة - @aqhvv | @Lx5x5",
            )
        )
        ch = ch.chats[0].id  # الحصول على معرف القناة مباشرة

        # تعيين اليوزر للقناة الجديدة
        await l313l(
            functions.channels.UpdateUsernameRequest(
                channel=ch, username=current_username.replace("@", "")
            )
        )

        await edit_or_reply(event, f"**⎉╎تم نقـل اليـوزر {current_username} إلى القنـاة الجديـدة .. بنجـاح ☑️**")
    except Exception as e:
        await edit_or_reply(event, f"**⎉╎حدث خطأ أثناء نقـل اليـوزر:**\n`{str(e)}`")

@l313l.ar_cmd(pattern="نقل_حساب (.*)")
async def transfer_to_account(event):
    username = event.pattern_match.group(1)
    if not username.startswith('@'):
        return await edit_or_reply(event, "**⎉╎عـذراً عـزيـزي المدخـل خطـأ ❌**\n**⎉╎استخـدم الامـر كالتالـي**\n**⎉╎ارسـل (**`.نقل_حساب`** + اليـوزر)**")

    # الحصول على اليوزر الحالي للحساب
    current_username = f"@{l313l.me.username}" if l313l.me.username else None

    try:
        # إذا كان الحساب يمتلك يوزر، قم بحذفه أولًا
        if current_username:
            await l313l(functions.account.UpdateUsernameRequest(username=""))
            await edit_or_reply(event, f"**⎉╎تم إزالـة اليـوزر الحالي ({current_username}) .. بنجـاح ☑️**")

        # تعيين اليوزر الجديد لحسابك
        await l313l(functions.account.UpdateUsernameRequest(username=username.replace("@", "")))

        await edit_or_reply(event, f"**⎉╎تم تعييـن اليـوزر {username} لحسـابك .. بنجـاح ☑️**")
    except Exception as e:
        await edit_or_reply(event, f"**⎉╎حدث خطأ أثناء نقـل اليـوزر:**\n`{str(e)}`")

@l313l.ar_cmd(pattern="نقل_بوت_القناة (.*)")
async def transfer_bot_to_channel(event):
    username = event.pattern_match.group(1)
    if not username.startswith('@'):
        return await edit_or_reply(event, "**⎉╎عـذراً عـزيـزي المدخـل خطـأ ❌**\n**⎉╎استخـدم الامـر كالتالـي**\n**⎉╎ارسـل (**`.نقل_بوت_القناة`** + اليـوزر)**")
    
    try:
        # إزالة اليوزر من القناة
        await l313l(
            functions.channels.UpdateUsernameRequest(
                channel=event.chat_id, username=""
            )
        )
        
        # إنشاء بوت جديد باستخدام اليوزر
        bot_name = "البوت الجديد"  # يمكنك تغيير الاسم حسب الرغبة
        
        await event.client.send_message("@BotFather", "/newbot")
        await event.client.send_message("@BotFather", bot_name)
        await event.client.send_message("@BotFather", username.replace("@", ""))
        
        await edit_or_reply(event, f"**⎉╎تم نقـل اليـوزر {username} إلى بوت فـاذر (@BotFather) .. بنجـاح ☑️**\n**⎉╎تم إنشـاء بـوت جديد باستخـدام اليـوزر.**")
    except Exception as e:
        await edit_or_reply(event, f"**⎉╎حدث خطأ أثناء نقـل اليـوزر:**\n`{str(e)}`")

@l313l.ar_cmd(pattern="نقل_بوت_الحساب (.*)")
async def transfer_bot_to_account(event):
    username = event.pattern_match.group(1)
    if not username.startswith('@'):
        return await edit_or_reply(event, "**⎉╎عـذراً عـزيـزي المدخـل خطـأ ❌**\n**⎉╎استخـدم الامـر كالتالـي**\n**⎉╎ارسـل (**`.نقل_بوت_الحساب`** + اليـوزر)**")
    
    try:
        # إزالة اليوزر من الحساب
        await l313l(functions.account.UpdateUsernameRequest(username=""))
        
        # إنشاء بوت جديد باستخدام اليوزر
        bot_name = "البوت الجديد"  # يمكنك تغيير الاسم حسب الرغبة
        
        await event.client.send_message("@BotFather", "/newbot")
        await event.client.send_message("@BotFather", bot_name)
        await event.client.send_message("@BotFather", username.replace("@", ""))
        
        await edit_or_reply(event, f"**⎉╎تم نقـل اليـوزر {username} إلى بوت فـاذر (@BotFather) .. بنجـاح ☑️**\n**⎉╎تم إنشـاء بـوت جديد باستخـدام اليـوزر.**")
    except Exception as e:
        await edit_or_reply(event, f"**⎉╎حدث خطأ أثناء نقـل اليـوزر:**\n`{str(e)}`")

@l313l.ar_cmd(pattern="نقل_ملكية (.*)")
async def transfer_ownership(event):
    target_user = event.pattern_match.group(1)
    if not target_user.startswith('@'):
        return await edit_or_reply(event, "**⎉╎عـذراً عـزيـزي المدخـل خطـأ ❌**\n**⎉╎استخـدم الامـر كالتالـي**\n**⎉╎ارسـل (**`.نقل_ملكية`** + معرف الشخص)**")
    
    # طلب كلمة المرور من المستخدم
    password_msg = await event.respond("**⎉╎رجـاءً أدخـل كلمـة مـرور حسـابك:**")
    
    try:
        # انتظار إدخال كلمة المرور
        def check_password(m):
            return m.sender_id == event.sender_id and m.chat_id == event.chat_id
        
        password_event = await event.client.wait_for('message', timeout=60, check=check_password)
        password = password_event.text
        
        # تعديل الرسالة لاستبدال كلمة المرور بعلامات ****
        await password_event.edit("******")
        
        # الحصول على كيان المستخدم الهدف
        target_entity = await event.client.get_entity(target_user)
        
        # نقل ملكية القناة
        await event.client(
            functions.channels.EditCreatorRequest(
                channel=event.chat_id,
                user_id=target_entity.id,
                password=password  # استخدام كلمة المرور التي أدخلها المستخدم
            )
        )
        
        await edit_or_reply(event, f"**⎉╎تم نقـل ملكيـة القنـاة إلى {target_user} .. بنجـاح ☑️**")
    except asyncio.TimeoutError:
        await edit_or_reply(event, "**⎉╎انتهـى الوقـت المحدد لإدخـال كلمـة المـرور.**")
    except Exception as e:
        await edit_or_reply(event, f"**⎉╎حدث خطأ أثناء نقـل الملكيـة:**\n`{str(e)}`")

async def gen_user(choice):
    a = "qwertyuiopasdfghjklzxcvbnm"
    b = "1234567890"
    e = "qwertyuiopasdfghjklzxcvbnm1234567890"
    z = "sdfghjklzwerty1234567890uioxcvbqpanm"
    o = "0987654321"
    q = "5432109876"
    k = "mnbvcxzlkjhgfdsapoiuytrewq"
    if choice == "سداسي_حرفين1": #ARAAAR
        c = d = random.choices(a)
        d = random.choices(e)
        f = [c[0], d[0], c[0], c[0], c[0], d[0]]
        random.shuffle(f)
        username = "".join(f)

    elif choice == "سداسي_رقمين1": #A8AAA8
        c = d = random.choices(a)
        d = random.choices(o)
        f = [c[0], d[0], c[0], c[0], c[0], d[0]]
        random.shuffle(f)
        username = "".join(f)

    elif choice == "سداسي_شرطه": #AAAA_R ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], c[0], c[0], c[0], "_", d[0]]
        username = "".join(f)

    elif choice == "سداسي_حرفين2": #AAAARR ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], c[0], c[0], c[0], d[0], d[0]]
        username = "".join(f)

    elif choice == "سداسي_رقمين2": #AAAA88 ~ 
        c = random.choices(a)
        d = random.choices(o)
        f = [c[0], c[0], c[0], c[0], d[0], d[0]]
        username = "".join(f)

    elif choice == "سداسي_حرفين3": #AAARRA ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], c[0], c[0], d[0], d[0], c[0]]
        username = "".join(f)

    elif choice == "سداسي_رقمين3": #AAA88A ~ 
        c = random.choices(a)
        d = random.choices(o)
        f = [c[0], c[0], c[0], d[0], d[0], c[0]]
        username = "".join(f)

    elif choice == "سداسي_حرفين4": #AARRAA ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], c[0], d[0], d[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سداسي_رقمين4": #AA88AA ~ 
        c = random.choices(a)
        d = random.choices(o)
        f = [c[0], c[0], d[0], d[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سداسي_حرفين5": #ARRAAA ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], d[0], d[0], c[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سداسي_حرفين6": #AARRRR ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], c[0], d[0], d[0], d[0], d[0]]
        username = "".join(f)

    elif choice == "ثلاثي1": #A_R_D
        c = random.choices(a)
        d = random.choices(e)
        s = random.choices(z)
        f = [c[0], "_", d[0], "_", s[0]]
        username = "".join(f)

    elif choice == "ثلاثي2": #A_7_R ~ 
        c = random.choices(a)
        d = random.choices(o)
        s = random.choices(z)
        f = [c[0], "_", d[0], "_", s[0]]
        username = "".join(f)

    elif choice == "ثلاثي3": #A_7_0 ~ 
        c = random.choices(a)
        d = random.choices(b)
        s = random.choices(o)
        f = [c[0], "_", d[0], "_", s[0]]
        username = "".join(f)

    elif choice == "شبه رباعي1": #A_A_A_R ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], "_", c[0], "_", c[0], "_", d[0]]
        username = "".join(f)

    elif choice == "شبه رباعي2": #A_R_R_R ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], "_", d[0], "_", d[0], "_", d[0]]
        username = "".join(f)

    elif choice == "شبه رباعي3": #A_RR_A ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], "_", d[0], d[0], "_", c[0]]
        username = "".join(f)

    elif choice == "شبه رباعيa": #A_RR_A ~ 
        d = random.choices(z)
        f = ["a", "_", d[0], d[0], "_", "a"]
        username = "".join(f)

    elif choice == "شبه رباعيz": #Z_RR_Z ~ 
        d = random.choices(z)
        f = ["z", "_", d[0], d[0], "_", "z"]
        username = "".join(f)

    elif choice == "شبه رباعيr": #R_AA_R ~ 
        d = random.choices(z)
        f = ["r", "_", d[0], d[0], "_", "r"]
        username = "".join(f)

    elif choice == "شبه رباعيo": #O_RR_O ~ 
        d = random.choices(z)
        f = ["o", "_", d[0], d[0], "_", "o"]
        username = "".join(f)

    elif choice == "شبه رباعيi": #i_RR_i ~ 
        d = random.choices(z)
        f = ["i", "_", d[0], d[0], "_", "i"]
        username = "".join(f)

    elif choice == "شبه رباعيl": #l_RR_l ~ 
        d = random.choices(z)
        f = ["l", "_", d[0], d[0], "_", "l"]
        username = "".join(f)

    elif choice == "شبه رباعي4": #A_RR_R ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], "_", d[0], d[0], "_", d[0]]
        username = "".join(f)

    elif choice == "شبه رباعي5": #A_RR_R ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], d[0], d[0], "_", d[0]]
        username = "".join(f)

    elif choice == "شبه_رباعيi": # lk_kl | ik_ki ~ 
        g = "li"
        h = "sdfghjklzwerty1234567890uioxcvbqpanm"
        c = random.choices(g)
        d = random.choices(h)
        f = [c[0], d[0], "_", d[0], c[0]]
        username = "".join(f)

    elif choice == "شبه_رباعيu": # lu_ul ~ 
        c = random.choices(a)
        f = [c[0], "u", "_", "u", c[0]]
        username = "".join(f)

    elif choice == "شبه_رباعيn": # ln_nl ~ 
        c = random.choices(a)
        f = [c[0], "n", "_", "n", c[0]]
        username = "".join(f)

    elif choice == "شبه_رباعيe": # le_el ~ 
        c = random.choices(a)
        f = [c[0], "e", "_", "e", c[0]]
        username = "".join(f)

    elif choice == "شبه_رباعيo": # lo_ol ~ 
        c = random.choices(a)
        f = [c[0], "o", "_", "o", c[0]]
        username = "".join(f)

    elif choice == "شبه_رباعيv": # lv_vl ~ 
        c = random.choices(a)
        f = [c[0], "v", "_", "v", c[0]]
        username = "".join(f)

    elif choice == "رباعيات حرف": #AA_AR ~ 
        c = random.choices(a)
        d = random.choices(k)
        f = [c[0], c[0], "_", c[0], d[0]]
        username = "".join(f)

    elif choice == "رباعيات رقم": #AA_AR ~ 
        c = random.choices(a)
        d = random.choices(o)
        f = [c[0], c[0], "_", c[0], d[0]]
        username = "".join(f)

    elif choice == "رباعي1": #AAA_R ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], c[0], c[0], "_", d[0]]
        username = "".join(f)

    elif choice == "رباعيa": #AAA_R ~ 
        c = random.choices(e)
        f = ["a", "a", "a", "_", c[0]]
        username = "".join(f)

    elif choice == "رباعيz": #ZZZ_R ~ 
        c = random.choices(e)
        f = ["z", "z", "z", "_", c[0]]
        username = "".join(f)

    elif choice == "رباعيr": #RRR_D ~ 
        c = random.choices(e)
        f = ["r", "r", "r", "_", c[0]]
        username = "".join(f)

    elif choice == "رباعي رقم1": #AAA_7 ~ 
        c = random.choices(a)
        d = random.choices(o)
        f = [c[0], c[0], c[0], "_", d[0]]
        username = "".join(f)

    elif choice == "رباعي2": #A_RRR ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], "_", d[0], d[0], d[0]]
        username = "".join(f)

    elif choice == "رباعي رقم2": #A_777 ~ 
        c = random.choices(a)
        d = random.choices(o)
        f = [c[0], "_", d[0], d[0], d[0]]
        username = "".join(f)

    elif choice == "رباعي3": #AA_RR ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], c[0], "_", d[0], d[0]]
        username = "".join(f)

    elif choice == "رباعي4": #AA_AR ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], c[0], "_", c[0], d[0]]
        username = "".join(f)

    elif choice == "رباعي5": #AA_RA ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], c[0], "_", d[0], c[0]]
        username = "".join(f)

    elif choice == "رباعي6": #AR_RA ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], d[0], "_", d[0], c[0]]
        username = "".join(f)

    elif choice == "رباعي رقم6": #A7_7A ~ 
        c = random.choices(a)
        d = random.choices(o)
        f = [c[0], d[0], "_", d[0], c[0]]
        username = "".join(f)

    elif choice == "رباعي7": #AR_AR ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], d[0], "_", c[0], d[0]]
        username = "".join(f)

    elif choice == "رباعي رقم7": #A7_A7 ~ 
        c = random.choices(a)
        d = random.choices(o)
        f = [c[0], d[0], "_", c[0], d[0]]
        username = "".join(f)

    elif choice == "رباعي8": #AR_RR ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], d[0], "_", d[0], d[0]]
        username = "".join(f)

    elif choice == "رباعي رقم8": #A7_77 ~ 
        c = random.choices(a)
        d = random.choices(o)
        f = [c[0], d[0], "_", d[0], d[0]]
        username = "".join(f)

    elif choice == "سداسيات1": #AAAAAR
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], c[0], c[0], c[0], c[0], d[0]]
        username = "".join(f)

    elif choice == "سداسيات2": #AAAARA ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], c[0], c[0], c[0], d[0], c[0]]
        username = "".join(f)

    elif choice == "سداسيات3": #AAARAA ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], c[0], c[0], d[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سداسيات4": #AARAAA ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], c[0], d[0], c[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سداسيات5": #ARAAAA ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], d[0], c[0], c[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سداسيات6": #ARRRRR ~ 
        c = random.choices(a)
        d = random.choices(e)
        f = [c[0], d[0], d[0], d[0], d[0], d[0]]
        username = "".join(f)

    elif choice == "سداسيvip": #VIP537 ~ 
        c = random.choices(b)
        d = random.choices(o)
        s = random.choices(q)
        f = ["v", "i", "p", c[0], d[0], s[0]]
        username = "".join(f)

    elif choice == "سداسي_vip": #VIP537 ~ 
        c = random.choices(b)
        d = random.choices(o)
        f = ["v", "i", "p", "_", c[0], d[0]]
        username = "".join(f)

    elif choice == "بوتات1": #AR_Bot ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], d[0], "_", "b", "o", "t"]
        username = "".join(f)

    elif choice == "بوتات2": #A_RBot ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], "_", d[0], "b", "o", "t"]
        username = "".join(f)

    elif choice == "بوتات3": #AR7Bot ~ 
        c = random.choices(a)
        d = random.choices(k)
        s = random.choices(b)
        f = [c[0], d[0], s[0], "b", "o", "t"]
        username = "".join(f)

    elif choice == "بوتات4": #A7RBot ~ 
        c = random.choices(a)
        d = random.choices(b)
        s = random.choices(k)
        f = [c[0], d[0], s[0], "b", "o", "t"]
        username = "".join(f)

    elif choice == "بوتات5": #A77Bot ~ 
        c = random.choices(a)
        d = random.choices(b)
        s = random.choices(o)
        f = [c[0], d[0], s[0], "b", "o", "t"]
        username = "".join(f)

    elif choice == "بوتات6": #ADRBot
        c = random.choices(a)
        d = random.choices(e)
        s = random.choices(z)
        f = [c[0], d[0], s[0], "b", "o", "t"]
        username = "".join(f)

    elif choice == "بوتات7": #(AARBot - AA8bot) ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], c[0], d[0], "b", "o", "t"]
        username = "".join(f)

    elif choice == "بوتات8": #AARBot ~ 
        c = random.choices(a)
        d = random.choices(k)
        f = [c[0], c[0], d[0], "b", "o", "t"]
        username = "".join(f)

    elif choice == "بوتات9": #AA8Bot ~ 
        c = random.choices(a)
        d = random.choices(o)
        f = [c[0], c[0], d[0], "b", "o", "t"]
        username = "".join(f)

    elif choice == "خماسي حرفين1": #AAARD ~ 
        c = random.choices(a)
        d = random.choices(z)
        s = random.choices(e)
        f = [c[0], c[0], c[0], s[0], d[0]]
        username = "".join(f)

    elif choice == "خماسي ارقام": #AR888 ~ 
        c = random.choices(a)
        d = random.choices(e)
        s = random.choices(b)
        f = [c[0], d[0], s[0], s[0], s[0]]
        username = "".join(f)

    elif choice == "خماسي رقمين1": #AAARD ~ 
        c = random.choices(a)
        d = random.choices(o)
        s = random.choices(b)
        f = [c[0], c[0], c[0], d[0], s[0]]
        username = "".join(f)

    elif choice == "خماسي حرفين2": #A7RRR ~ 
        c = random.choices(a)
        d = random.choices(b)
        s = random.choices(z)
        f = [c[0], d[0], s[0], s[0], s[0]]
        username = "".join(f)

    elif choice == "خماسي k": #A800k ~ 
        c = random.choices(a)
        d = random.choices(o)
        f = [c[0], d[0], "0", "0", "k"]
        username = "".join(f)

    elif choice == "خماسي حرفينa": #AAARD ~ 
        c = random.choices(z)
        d = random.choices(e)
        f = ["a", "a", "a", c[0], d[0]]
        username = "".join(f)

    elif choice == "خماسي حرفينr": #RRRAD ~ 
        c = random.choices(z)
        d = random.choices(e)
        f = ["r", "r", "r", c[0], d[0]]
        username = "".join(f)

    elif choice == "خماسي رقمينm": #MMM87 ~ 
        c = random.choices(b)
        d = random.choices(o)
        f = ["m", "m", "m", c[0], d[0]]
        username = "".join(f)

    elif choice == "خماسي حرفينn": #NNNAR ~ 
        c = random.choices(e)
        d = random.choices(z)
        f = ["n", "n", "n", c[0], d[0]]
        username = "".join(f)

    elif choice == "خماسي حرفينz": #ZZZAR ~ 
        c = random.choices(z)
        d = random.choices(e)
        f = ["z", "z", "z", c[0], d[0]]
        username = "".join(f)

    elif choice == "خماسي حرفين3": #ARRRD ~ 
        c = random.choices(a)
        d = random.choices(z)
        s = random.choices(e)
        f = [c[0], d[0], d[0], d[0], s[0]]
        username = "".join(f)

    elif choice == "خماسي حرفين33": #AAARR ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], c[0], c[0], d[0], d[0]]
        username = "".join(f)

    elif choice == "خماسي حرفين44": #ARRRA ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], d[0], d[0], d[0], c[0]]
        username = "".join(f)

    elif choice == "خماسي حرفين55": #AARRR ~ 
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], c[0], d[0], d[0], d[0]]
        username = "".join(f)

    elif choice == "خماسي حرفين66": #ARAAR
        c = random.choices(a)
        d = random.choices(z)
        f = [c[0], d[0], c[0], c[0], d[0]]
        username = "".join(f)

    elif choice == "سباعيات1": #AAAAAAR ~ 
        c = d = random.choices(a)
        d = random.choices(z)
        f = [c[0], c[0], c[0], c[0], c[0], c[0], d[0]]
        username = "".join(f)

    elif choice == "سباعيات2": #AAAAARA ~ 
        c = d = random.choices(a)
        d = random.choices(z)
        f = [c[0], c[0], c[0], c[0], c[0], d[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات3": #AAAARAA
        c = d = random.choices(a)
        d = random.choices(z)
        f = [c[0], c[0], c[0], c[0], d[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات4": #AAARAAA ~ 
        c = d = random.choices(a)
        d = random.choices(z)
        f = [c[0], c[0], c[0], d[0], c[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات5": #AARAAAA ~ 
        c = d = random.choices(a)
        d = random.choices(z)
        f = [c[0], c[0], d[0], c[0], c[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات6": #ARAAAAA ~ 
        c = d = random.choices(a)
        d = random.choices(z)
        f = [c[0], d[0], c[0], c[0], c[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات7": #ARRRRRR ~ 
        c = d = random.choices(a)
        d = random.choices(z)
        f = [c[0], d[0], d[0], d[0], d[0], d[0], d[0]]
        username = "".join(f)

    elif choice == "سباعيات حرف1": #AAAAAAR ~ 
        c = d = random.choices(a)
        d = random.choices(k)
        f = [c[0], c[0], c[0], c[0], c[0], c[0], d[0]]
        username = "".join(f)

    elif choice == "سباعيات رقم1": #AAAAAA8 ~ 
        c = d = random.choices(a)
        d = random.choices(o)
        f = [c[0], c[0], c[0], c[0], c[0], c[0], d[0]]
        username = "".join(f)

    elif choice == "سباعيات حرف2": #AAAAARA ~ 
        c = d = random.choices(a)
        d = random.choices(k)
        f = [c[0], c[0], c[0], c[0], c[0], d[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات رقم2": #AAAAA8A ~ 
        c = d = random.choices(a)
        d = random.choices(o)
        f = [c[0], c[0], c[0], c[0], c[0], d[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات حرف3": #AAAARAA
        c = d = random.choices(a)
        d = random.choices(k)
        f = [c[0], c[0], c[0], c[0], d[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات رقم3": #AAAA8AA
        c = d = random.choices(a)
        d = random.choices(o)
        f = [c[0], c[0], c[0], c[0], d[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات حرف4": #AAARAAA ~ 
        c = d = random.choices(a)
        d = random.choices(k)
        f = [c[0], c[0], c[0], d[0], c[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات رقم4": #AAA8AAA ~ 
        c = d = random.choices(a)
        d = random.choices(o)
        f = [c[0], c[0], c[0], d[0], c[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات حرف5": #AARAAAA ~ 
        c = d = random.choices(a)
        d = random.choices(k)
        f = [c[0], c[0], d[0], c[0], c[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات رقم5": #AA8AAAA ~ 
        c = d = random.choices(a)
        d = random.choices(o)
        f = [c[0], c[0], d[0], c[0], c[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات حرف6": #ARAAAAA ~ 
        c = d = random.choices(a)
        d = random.choices(k)
        f = [c[0], d[0], c[0], c[0], c[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات رقم6": #A8AAAAA ~ 
        c = d = random.choices(a)
        d = random.choices(o)
        f = [c[0], d[0], c[0], c[0], c[0], c[0], c[0]]
        username = "".join(f)

    elif choice == "سباعيات حرف7": #ARRRRRR ~ 
        c = d = random.choices(a)
        d = random.choices(k)
        f = [c[0], d[0], d[0], d[0], d[0], d[0], d[0]]
        username = "".join(f)

    elif choice == "سباعيات رقم7": #A888888 ~ 
        c = d = random.choices(a)
        d = random.choices(o)
        f = [c[0], d[0], d[0], d[0], d[0], d[0], d[0]]
        username = "".join(f)

    elif choice == "ايقاف": #
        return "stop"
    else:
        return "error"
    return username

meaningful_words = [
    word for word in [
    "angel", "anger", "arrow", "badge", "beast", "blade", "blaze", "brave", "brick", "bride",
    "candy", "charm", "clash", "crown", "dance", "demon", "doubt", "dragon", "dream", "eagle",
    "earth", "enemy", "faith", "flame", "fleet", "frost", "ghost", "glory", "grace", "guard",
    "heart", "honor", "honey", "horse", "hound", "hunter", "iron", "jewel", "knight", "light",
    "lover", "magic", "mercy", "metal", "might", "mirth", "monk", "moon", "mystic", "night",
    "noble", "ocean", "panda", "peace", "pearl", "phantom", "pride", "queen", "raven", "rider",
    "river", "rogue", "royal", "saber", "saint", "scout", "serpent", "shadow", "shark", "shield",
    "silver", "siren", "slayer", "sniper", "solar", "soul", "spark", "spirit", "star", "steel",
    "storm", "strife", "sun", "sword", "thief", "thunder", "tiger", "titan", "tower", "trick",
    "valor", "vapor", "viper", "vortex", "wander", "warrior", "water", "whisper", "wind", "wolf",
    "wonder", "wrath", "zeal", "zephyr", "abyss", "amber", "anvil", "apollo", "archer", "atlas",
    "aurora", "avalon", "banshee", "basilisk", "behemoth", "blitz", "boulder", "breeze", "cactus",
    "carnage", "cascade", "cinder", "comet", "corsair", "crimson", "cyclone", "dagger", "dawn",
    "demon", "desert", "diamond", "dusk", "eclipse", "ember", "eternity", "falcon", "flame",
    "flint", "forge", "frost", "galaxy", "gale", "glacier", "glimmer", "goliath", "gossamer",
    "hail", "harbinger", "haze", "horizon", "hurricane", "inferno", "ivory", "jade", "jester",
    "jupiter", "kraken", "labyrinth", "lagoon", "lava", "legend", "leviathan", "lily", "lunar",
    "magnet", "marble", "mars", "meadow", "mercury", "midnight", "mirage", "mist", "monsoon",
    "moonlight", "nebula", "neptune", "nimbus", "nova", "obsidian", "onyx", "opal", "orbit",
    "pandora", "phoenix", "platinum", "pluto", "pulse", "quartz", "quasar", "radiant", "rain",
    "relic", "rhapsody", "rune", "sable", "sapphire", "saturn", "scorpio", "seraph", "shadow",
    "shard", "sierra", "silhouette", "siren", "solaris", "solstice", "specter", "spiral", "spire",
    "stardust", "storm", "stratus", "summit", "sunset", "supernova", "tempest", "titanium", "torrent",
    "tranquility", "twilight", "typhoon", "umbra", "valkyrie", "vanguard", "venom", "vertex", "vortex",
    "warlock", "whirlwind", "wisp", "wyvern", "xenon", "zodiac", "abyss", "acumen", "aegis", "aether",
    "alchemy", "alpine", "ambrosia", "anarchy", "anthem", "arcadia", "archon", "ares", "argus", "artemis",
    "asgard", "astral", "athena", "atlas", "aurora", "avalon", "azrael", "banshee", "basilisk", "behemoth",
    "blitz", "boulder", "breeze", "cactus", "carnage", "cascade", "cinder", "comet", "corsair", "crimson",
    "cyclone", "dagger", "dawn", "demon", "desert", "diamond", "dusk", "eclipse", "ember", "eternity",
    "falcon", "flame", "flint", "forge", "frost", "galaxy", "gale", "glacier", "glimmer", "goliath",
    "gossamer", "hail", "harbinger", "haze", "horizon", "hurricane", "inferno", "ivory", "jade", "jester",
    "jupiter", "kraken", "labyrinth", "lagoon", "lava", "legend", "leviathan", "lily", "lunar", "magnet",
    "marble", "mars", "meadow", "mercury", "midnight", "mirage", "mist", "monsoon", "moonlight", "nebula",
    "neptune", "nimbus", "nova", "obsidian", "onyx", "opal", "orbit", "pandora", "phoenix", "platinum",
    "pluto", "pulse", "quartz", "quasar", "radiant", "rain", "relic", "rhapsody", "rune", "sable", "sapphire",
    "saturn", "scorpio", "seraph", "shadow", "shard", "sierra", "silhouette", "siren", "solaris", "solstice",
    "specter", "spiral", "spire", "stardust", "storm", "stratus", "summit", "sunset", "supernova", "tempest",
    "titanium", "torrent", "tranquility", "twilight", "typhoon", "umbra", "valkyrie", "vanguard", "venom",
    "vertex", "vortex", "warlock", "whirlwind", "wisp", "wyvern", "xenon", "zodiac", "karlos", "matrix",
    "neo", "trinity", "morpheus", "orion", "thor", "loki", "zeus", "hermes", "athena", "apollo", "hercules",
    "perseus", "medusa", "poseidon", "hades", "ares", "artemis", "dionysus", "chronos", "gaia", "selene",
    "helios", "eros", "hypnos", "nike", "nemesis", "iris", "hecate", "pan", "janus", "vulcan", "bacchus",
    "cerberus", "sphinx", "minotaur", "pegasus", "centaur", "phoenix", "griffin", "chimera", "hydra", "siren",
    "unicorn", "drake", "wyrm", "basilisk", "kraken", "leviathan", "behemoth", "gargoyle", "banshee", "valkyrie",
    "fenrir", "jormungandr", "yggdrasil", "midgard", "asgard", "valhalla", "niflheim", "muspelheim", "alfheim",
    "svartalfheim", "vanaheim", "jotunheim", "helheim", "nidavellir", "utgard", "bifrost", "ginnungagap", "ragnarok"
    ] if len(word) == 5  # تصفية الكلمات التي تحتوي على 5 أحرف فقط
]

@l313l.ar_cmd(pattern="صيد معاني")
async def hunt_meaningful_usernames(event):
    await edit_or_reply(event, "**⎉╎تم بـدء صيد أسماء ذات معنى .. بنجـاح ☑️**\n**⎉╎لمعرفـة حالة عمليـة الصيـد (** `.حالة الصيد` **)**\n**⎉╎لـ ايقـاف عمليـة الصيـد (** `.صيد ايقاف` **)**")
    
    # إنشاء قناة تلقائيًا إذا لم يتم توفير قناة
    try:
        zuz = f"@{l313l.me.username}" if l313l.me.username else ""
        ch = await l313l(
            functions.channels.CreateChannelRequest(
                title="الصيد الخاص بـ Lx5x5",
                about=f"تم إنشاء هذه القناة لصيد أسماء مستخدمين ذات معنى بواسطة - @aqhvv | {zuz}",
            )
        )
        try:
            ch = ch.updates[1].channel_id
        except Exception:
            ch = ch.chats[0].id
    except Exception as e:
        await l313l.send_message(event.chat_id, f"**- حدث خطأ أثناء إنشاء القناة:**\n`{str(e)}`")
        return

    itsclim.clear()
    itsclim.append("on")
    vedmod = True
    while vedmod:
        username = await gen_meaningful_username()
        isav = await check_user(username)
        if isav == True:
            try:
                await l313l(
                    functions.channels.UpdateUsernameRequest(
                        channel=ch, username=username
                    )
                )
                await event.client.send_message(
                    event.chat_id,
                    f"- Done : @{username} ✅\n- By : @Lx5x5\n- Hunting Log {trys[0]}",
                )
                await event.client.send_message(
                    "@Lx5x5", f"- Done : @{username} ✅\n- By : @Lx5x5\n- Hunting Log {trys[0]}",
                )
                vedmod = False
                break
            except FloodWaitError as zed:
                wait_time = zed.seconds
                await sleep(wait_time + 10)
                pass
            except telethon.errors.rpcerrorlist.UsernameInvalidError:
                pass
            except telethon.errors.FloodError as e:
                flood_error = e.seconds
                await sleep(flood_error + 10)
                pass
            except Exception as e:
                if "too many public channels" in str(e):
                    await l313l.send_message(
                        event.chat_id,
                        f"""- خطأ بصيـد اليـوزر @{username} ,\n- الخطأ :\nانت تمتلك العديد من القنوات العامة قم بحذف معرف او اكثر من قنواتك لكي تستطيع صيد هذا اليوزر""",
                    )
                    break
                else:
                    pass
        else:
            pass
        trys[0] += 1
        await asyncio.sleep(1)

    itsclim.clear()
    itsclim.append("off")
    trys[0] = 0
    return await event.client.send_message(event.chat_id, "**- تم الانتهاء من الصيد .. بنجـاح ✅**")

ZelzalChecler_cmd = (
    "𓆩 [اوامـر الصيـد والتثبيت](t.me/Lx5x5) 𓆪\n\n"
    "**✾╎اولاً قـائمـة اوامـر تشيكـر صيـد معـرفات تيليجـرام :** \n\n"
    "`.النوع`\n"
    "**⪼ لـ عـرض الانـوع التي يمكـن صيدهـا مع الامثـله**\n"
    "`.صيد` + النـوع\n"
    "**⪼ لـ صيـد يـوزرات عشوائيـه على حسب النـوع**\n"
    "`.حالة الصيد`\n"
    "**⪼ لـ معرفـة حالـة تقـدم عمليـة الصيـد**\n"
    "`.صيد ايقاف`\n"
    "**⪼ لـ إيقـاف عمليـة الصيـد الجاريـه**\n\n\n"
    "**✾╎ثانياً قـائمـة اوامـر تشيكـر تثبيت معـرفات تيليجـرام :** \n\n"
    "`.تثبيت_قناة` + اليوزر\n"
    "**⪼ لـ تثبيت اليـوزر بقنـاة معينـه اذا اصبح متاحـاً يتم اخـذه**\n"
    "`.تثبيت_حساب` + اليوزر\n"
    "**⪼ لـ تثبيت اليـوزر بحسـابك مباشـرة اذا اصبح متاحـاً يتم اخـذه**\n"
    "`.تثبيت_بوت` + اليوزر\n"
    "**⪼ لـ تثبيت اليـوزر في بـوت فـاذر اذا اصبح متاحـاً يتم اخـذه**\n\n"
    "`.حالة تثبيت_القناة`\n"
    "**⪼ لـ معرفـة حالـة تقـدم التثبيت التلقـائـي على القنـاة**\n"
    "`.حالة تثبيت_الحساب`\n"
    "**⪼ لـ معرفـة حالـة تقـدم التثبيت التلقـائـي على حسابـك**\n"
    "`.حالة تثبيت_البوت`\n"
    "**⪼ لـ معرفـة حالـة تقـدم التثبيت التلقـائـي على بـوت فـاذر**\n\n"
    "`.ايقاف تثبيت_القناة`\n"
    "**⪼ لـ إيقـاف عمليـة تثبيت_القناة التلقـائـي**\n"
    "`.ايقاف تثبيت_الحساب`\n"
    "**⪼ لـ إيقـاف عمليـة تثبيت_الحساب التلقـائـي**\n"
    "`.ايقاف تثبيت_البوت`\n"
    "**⪼ لـ إيقـاف عمليـة تثبيت_البوت التلقـائـي**\n\n\n"
    "**- ملاحظـات مهمـه قبـل استخـدام اوامـر الصيـد والتثبيت :**\n"
    "**⪼** تأكد من ان حسابك يوجد فيه مساحه لانشاء قناة عامة (قناة بمعرف)\n"
    "**⪼** اذا كان لا يوجد مساحه لانشاء قناة عامة قم بارسال يوزر اي قناة من قنوات حسابك وبالرد ع يوزرها ارسل احد اوامر الصيد\n"
    "**⪼** لا تقم بـ ايقاف الصيد حتى ولو استمر الصيد ايام\n"
    "**⪼** تحلى بالصبر وكرر محاولات الصيد حتى تصيد يوزر\n"
    "**⪼** كل نوع من اليوزرات يختلف عن الاخر من حيث نسبة الصيد\n"
    "**⪼ التثبيت هو تثبيت يوزر محدد حتى ماينسرق منك عندما يصير متاح**\n\n"
    
)

ZelzalType_cmd = (
"𓆩 [أنـواع اليـوزرات](t.me/lx5x5) 𓆪\n\n"
"**✾╎قـائمـة أنـواع اليـوزرات التي يمكـن صيدهـا مـع الامثـلة :** \n\n"
"⪼  `.صيد ثلاثي1`  **مثـال ~** A_D_R\n"
"⪼  `.صيد ثلاثي2`  **مثـال ~** A_7_R\n"
"⪼  `.صيد ثلاثي3`  **مثـال ~** A_7_0\n\n"
"⪼  `.صيد رباعي1`  **مثـال ~** AAA_R\n"
"⪼  `.صيد رباعي2`  **مثـال ~** A_RRR\n"
"⪼  `.صيد رباعي3`  **مثـال ~** AA_RR\n"
"⪼  `.صيد رباعي4`  **مثـال ~** AA_AR\n"
"⪼  `.صيد رباعي5`  **مثـال ~** AA_RA\n"
"⪼  `.صيد رباعي6`  **مثـال ~** AR_RA\n"
"⪼  `.صيد رباعي7`  **مثـال ~** AR_AR\n"
"⪼  `.صيد رباعي8`  **مثـال ~** AR_RR\n\n"
"⪼  `.صيد شبه رباعي1`  **مثـال ~** A_A_A_R\n"
"⪼  `.صيد شبه رباعي2`  **مثـال ~** A_R_R_R\n"
"⪼  `.صيد شبه رباعي3`  **مثـال ~** A_RR_A\n"
"⪼  `.صيد شبه رباعي4`  **مثـال ~** A_RR_R\n\n"
"⪼  `.صيد خماسي حرفين1`  **مثـال ~** AAARD\n"
"⪼  `.صيد خماسي حرفين2`  **مثـال ~** A7RRR\n"
"⪼  `.صيد خماسي ارقام`  **مثـال ~** AR777\n\n"
"⪼  `.صيد خماسي حرفين3`  **مثـال ~** ARRRD\n"
"⪼  `.صيد سداسي_حرفين1`  **مثـال ~** ARAAAR\n"
"⪼  `.صيد سداسي_حرفين2`  **مثـال ~** AAAARR\n"
"⪼  `.صيد سداسي_حرفين3`  **مثـال ~** AAARRA\n"
"⪼  `.صيد سداسي_حرفين4`  **مثـال ~** AARRAA\n"
"⪼  `.صيد سداسي_حرفين5`  **مثـال ~** ARRAAA\n"
"⪼  `.صيد سداسي_حرفين6`  **مثـال ~** AARRRR\n"
"⪼  `.صيد سداسي_شرطه`  **مثـال ~** AAAA_R\n\n"
"⪼  `.صيد سباعيات1`  **مثـال ~** AAAAAAR\n"
"⪼  `.صيد سباعيات2`  **مثـال ~** AAAAARA\n"
"⪼  `.صيد سباعيات3`  **مثـال ~** AAAARAA\n"
"⪼  `.صيد سباعيات4`  **مثـال ~** AAARAAA\n"
"⪼  `.صيد سباعيات5`  **مثـال ~** AARAAAA\n"
"⪼  `.صيد سباعيات6`  **مثـال ~** ARAAAAA\n"
"⪼  `.صيد سباعيات7`  **مثـال ~** ARRRRRR\n\n"
"⪼  `.صيد بوتات1`  **مثـال ~** AR_Bot\n"
"⪼  `.صيد بوتات2`  **مثـال ~** A_RBot\n"
"⪼  `.صيد بوتات3`  **مثـال ~** AR7Bot\n"
"⪼  `.صيد بوتات4`  **مثـال ~** A7RBot\n"
"⪼  `.صيد بوتات5`  **مثـال ~** A77Bot\n"
"⪼  `.صيد بوتات6`  **مثـال ~** ADRBot\n"
"⪼  `.صيد بوتات7`  **مثـال ~** AARBot - AA8Bot\n"
"⪼  `.صيد بوتات8`  **مثـال ~** AARBot\n"
"⪼  `.صيد بوتات9`  **مثـال ~** AA8Bot\n\n"
"**- لـ عـرض اوامـر الصيـد والتثبيت الاساسيـة ارسـل الامـر التالـي :**\n"
"**⪼**  `.الصيد`  **او**  `.التثبيت`"
)

ZelzalVip_cmd = (
"𓆩 [أنـواع اليـوزرات](t.me/lx5x5) 𓆪\n\n"
"**✾╎قـائمـة أنـواع اليـوزرات التي يمكـن صيدهـا مـع الامثـلة :** \n\n"
"⪼  `.صيد شبه رباعيa`  **مثـال ~** A_RR_A\n"
"⪼  `.صيد شبه رباعيz`  **مثـال ~** Z_RR_Z\n"
"⪼  `.صيد شبه رباعيr`  **مثـال ~** R_AA_R\n"
"⪼  `.صيد شبه رباعيo`  **مثـال ~** O_RR_O\n"
"⪼  `.صيد شبه رباعيi`  **مثـال ~** i_RR_i\n"
"⪼  `.صيد شبه رباعيl`  **مثـال ~** l_RR_l\n\n"
"⪼  `.صيد شبه_رباعيi`  **مثـال ~**  lk_kl | ik_ki\n"
"⪼  `.صيد شبه_رباعيu`  **مثـال ~** lu_ul\n"
"⪼  `.صيد شبه_رباعيn`  **مثـال ~** ln_nl\n"
"⪼  `.صيد شبه_رباعيo`  **مثـال ~** lo_ol\n"
"⪼  `.صيد شبه_رباعيv`  **مثـال ~** lv_vl\n"
"⪼  `.صيد شبه_رباعيe`  **مثـال ~** le_el\n\n"
"⪼  `.صيد خماسي حرفينa`  **مثـال ~** AAARD\n"
"⪼  `.صيد خماسي حرفينr`  **مثـال ~** RRRAD\n"
"⪼  `.صيد خماسي حرفينz`  **مثـال ~** ZZZAR\n"
"⪼  `.صيد خماسي حرفينn`  **مثـال ~** NNNAR\n"
"⪼  `.صيد خماسي رقمينm`  **مثـال ~** MMM87\n\n"
"⪼  `.صيد سباعيات حرف1`  **مثـال ~** AAAAAAR\n"
"⪼  `.صيد سباعيات حرف2`  **مثـال ~** AAAAARA\n"
"⪼  `.صيد سباعيات حرف3`  **مثـال ~** AAAARAA\n"
"⪼  `.صيد سباعيات حرف4`  **مثـال ~** AAARAAA\n"
"⪼  `.صيد سباعيات حرف5`  **مثـال ~** AARAAAA\n"
"⪼  `.صيد سباعيات حرف6`  **مثـال ~** ARAAAAA\n"
"⪼  `.صيد سباعيات رقم1`  **مثـال ~** AAAAAAR\n"
"⪼  `.صيد سباعيات رقم2`  **مثـال ~** AAAAARA\n"
"⪼  `.صيد سباعيات رقم3`  **مثـال ~** AAAARAA\n"
"⪼  `.صيد سباعيات رقم4`  **مثـال ~** AAARAAA\n"
"⪼  `.صيد سباعيات رقم5`  **مثـال ~** AARAAAA\n"
"⪼  `.صيد سباعيات رقم6`  **مثـال ~** ARAAAAA"
)

@l313l.ar_cmd(pattern="(الصيد|التثبيت)")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalChecler_cmd)

@l313l.ar_cmd(pattern="(النوع|الانواع)")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalType_cmd)

@l313l.ar_cmd(pattern="الانووااع")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalVip_cmd)

@l313l.ar_cmd(pattern="صيد (.*)")
async def hunterusername(event):
    choice = str(event.pattern_match.group(1))
    replly = await event.get_reply_message()
    if not choice:
        return await edit_or_reply(event, "**⎉╎امـر خاطـئ .. تصفح اوامـر الصيـد**\n**⎉╎لـ الاوامـر العامـه .. ارسـل** ( `.الصيد` )\n**⎉╎لـ انـواع اليـوزرات .. ارسـل** ( `.الانواع` )")
    try:
        if replly and replly.text.startswith('@'):
            ch = replly.text
            await edit_or_reply(event, f"**⎉╎تم بـدء الصيـد .. بنجـاح ☑️**\n**⎉╎النـوع** {choice} \n**⎉╎على القنـاة** {ch} \n**⎉╎لمعرفـة حالة عمليـة الصيـد (** `.حالة الصيد` **)**\n**⎉╎لـ ايقـاف عمليـة الصيـد (** `.صيد ايقاف` **)**")
        elif choice == "ايقاف":
            await edit_or_reply(event, "..")
        else:
            zuz = f"@{l313l.me.username}" if l313l.me.username else ""
            ch = await l313l(
                functions.channels.CreateChannelRequest(
                    title="الـصيد الخـاص ب Lx5x5",
                    about=f"This channel to hunt username by - @aqhvv | {zuz}",
                )
            )
            try:
                ch = ch.updates[1].channel_id
            except Exception:
                ch = ch.chats[0].id
            await edit_or_reply(event, f"**⎉╎تم بـدء الصيـد .. بنجـاح ☑️**\n**⎉╎علـى النـوع** {choice} \n**⎉╎لمعرفـة حالة عمليـة الصيـد (** `.حالة الصيد` **)**\n**⎉╎لـ ايقـاف عمليـة الصيـد (** `.صيد ايقاف` **)**")
    except Exception as e:
        await l313l.send_message(event.chat_id, f"**- اووبـس .. خطـأ فـي إنشـاء القنـاة ؟!**\n**- تفاصيـل الخطـأ :**\n`{str(e)}`")
        vedmod = False

    itsclim.clear()
    itsclim.append("on")
    vedmod = True
    while vedmod:
        username = await gen_user(choice)
        if username == "stop":
            itsclim.clear()
            itsclim.append("off")
            trys[0] = 0
            break
            return await edit_or_reply(event, "**- تم إيقـاف عمليـة الصيـد .. بنجـاح ✓**")
        if username == "error":
            await edit_or_reply(event, f"**- عـذراً عـزيـزي\n- لايوجـد نوع** {choice} \n**- لـ عرض الانواع ارسـل (**`.الانواع`**)**")
            break
        isav = await check_user(username)
        if isav == True:
            try:
                await l313l(
                    functions.channels.UpdateUsernameRequest(
                        channel=ch, username=username
                    )
                )
                await event.client.send_message(
                    event.chat_id,
                    f"- Done : @{username} ✅\n- By : @Lx5x5\n- Hunting Log {trys[0]}",
                )
                await event.client.send_message(
                    "@Lx5x5", f"- Done : @{username} ✅\n- By : @Lx5x5\n- Hunting Log {trys[0]}",
                )
                vedmod = False
                break
            except FloodWaitError as zed:
                wait_time = zed.seconds
                await sleep(wait_time + 10)
                pass
            except telethon.errors.rpcerrorlist.UsernameInvalidError:
                pass
            except telethon.errors.FloodError as e:
                flood_error = e.seconds
                await sleep(flood_error + 10)
                pass
            except Exception as e:
                if "too many public channels" in str(e):
                    await l313l.send_message(
                        event.chat_id,
                        f"""- خطأ بصيـد اليـوزر @{username} ,\n- الخطأ :\nانت تمتلك العديد من القنوات العامة قم بحذف معرف او اكثر من قنواتك لكي تستطيع صيد هذا اليوزر""",
                    )
                    break
                else:
                    pass
        else:
            pass
        trys[0] += 1
        await asyncio.sleep(1)

    itsclim.clear()
    itsclim.append("off")
    trys[0] = 0
    return await event.client.send_message(event.chat_id, "**- تم الانتهاء من الصيد .. بنجـاح ✅**")

@l313l.ar_cmd(pattern="تثبيت (.*)")
async def _(event):
    zelzal = str(event.pattern_match.group(1))
    if zelzal.startswith('@'):
        return await edit_or_reply(event, "**⎉╎امـر خاطـئ .. تصفح اوامـر التثبيت**\n**⎉╎لـ الاوامـر العامـه للتثبيت .. ارسـل** ( `.التثبيت` )")

@l313l.ar_cmd(pattern="تثبيت_قناة (.*)")
async def _(event):
    zelzal = str(event.pattern_match.group(1))
    if not zelzal.startswith('@'):
        return await edit_or_reply(event, "**⎉╎عـذراً عـزيـزي المدخـل خطـأ ❌**\n**⎉╎استخـدم الامـر كالتالـي**\n**⎉╎ارسـل (**`.تثبيت_قناة`** + اليـوزر)**")
    try:
        zuz = f"@{l313l.me.username}" if Il313l.me.username else ""
        ch = await l313l(
            functions.channels.CreateChannelRequest(
                title="التـثبيت الخاص ب Lx5x5",
                about=f"تم تثبيت اليـوزر - @aqhvv | {zuz} ",
            )
        )
        try:
            ch = ch.updates[1].channel_id
        except Exception:
            ch = ch.chats[0].id
        await edit_or_reply(event, f"**⎉╎تم بـدء التثبيت .. بنجـاح ☑️**\n**⎉╎اليـوزر المثبت ( {zelzal} )**\n**⎉╎لمعرفـة تقـدم عمليـة التثبيت (**`.حالة تثبيت_القناة`**)**\n**⎉╎لـ ايقـاف عمليـة التثبيت (**`.ايقاف تثبيت_القناة`**)**")
    except Exception as e:
        await l313l.send_message(
            event.chat_id, f"**- اووبـس .. خطـأ فـي إنشـاء القنـاة ؟!**\n**- تفاصيـل الخطـأ :**\n`{str(e)}`"
        )
        cmodels = False

    iscuto.clear()
    iscuto.append("on")
    username = zelzal.replace("@", "") 
    cmodels = True
    while cmodels:
        isch = await checker_user(username)
        if isch == True:
            try:
                await l313l(
                    functions.channels.UpdateUsernameRequest(
                        channel=ch, username=username
                    )
                )
                await event.client.send_message(
                    event.chat_id,
                    f"- Done : @{username} ✅\n- Save: ❲ Channel ❳\n- By : @Lx5x5 \n- Hunting Log {crys[0]}",
                )
                break
            except FloodWaitError as zed: #Code by t.me/zzzzl1l
                wait_time = zed.seconds
                await sleep(wait_time + 10)
                pass
            except telethon.errors.rpcerrorlist.UsernameInvalidError:
                pass
            except telethon.errors.FloodError as e:
                flood_error = e.seconds
                await sleep(flood_error + 10)
                pass
            except Exception as eee:
                if "USERNAME_PURCHASE_AVAILABLE" in str(eee):
                    pass
                if "username is already taken" in str(eee):
                    pass
                else:
                    await l313l.send_message(
                        event.chat_id,
                        f"""- خطأ مع @{username} , الخطأ :{str(eee)}""",
                    )
                    break
        else:
            pass
        crys[0] += 1

        await asyncio.sleep(5)
    iscuto.clear()
    iscuto.append("off")
    crys[0] = 0
    return await l313l.send_message(event.chat_id, "**- تم الانتهاء من التثبيت .. بنجـاح ✅**")


@l313l.ar_cmd(pattern="تثبيت_حساب (.*)")
async def _(event):
    zelzal = str(event.pattern_match.group(1))
    if not zelzal.startswith('@'):
        return await edit_or_reply(event, "**⎉╎عـذراً عـزيـزي المدخـل خطـأ ❌**\n**⎉╎استخـدم الامـر كالتالـي**\n**⎉╎ارسـل (**`.تثبيت_حساب`** + اليـوزر)**")
    await edit_or_reply(event, f"**⎉╎تم بـدء التثبيت .. بنجـاح ☑️**\n**⎉╎اليـوزر المثبت ( {zelzal} )**\n**⎉╎لمعرفـة تقـدم عمليـة التثبيت (**`.حالة تثبيت_الحساب`**)**\n**⎉╎لـ ايقـاف عمليـة التثبيت (**`.ايقاف تثبيت_الحساب`**)**")
    istuto.clear()
    istuto.append("on")
    username = zelzal.replace("@", "") 
    amodels = True
    while amodels:
        isac = await checker_user(username)
        if isac == True:
            try:
                await l313l(functions.account.UpdateUsernameRequest(username=username))
                await event.client.send_message(
                    event.chat_id,
                    f"- Done : @{username} ✅\n- Save: ❲ Account ❳\n- By : @Lx5x5 \n- Hunting Log {arys[0]}",
                )
                break
            except FloodWaitError as zed: #Code by t.me/zzzzl1l
                wait_time = zed.seconds
                await sleep(wait_time + 10)
                pass
            except telethon.errors.rpcerrorlist.UsernameInvalidError:
                pass
            except telethon.errors.FloodError as e:
                flood_error = e.seconds
                await sleep(flood_error + 10)
                pass
            except Exception as eee:
                if "USERNAME_PURCHASE_AVAILABLE" in str(eee):
                    pass
                if "username is already taken" in str(eee):
                    pass
                else:
                    await l313l.send_message(
                        event.chat_id,
                        f"""- خطأ مع @{username} , الخطأ :{str(eee)}""",
                    )
                    break
        else:
            pass
        arys[0] += 1

        await asyncio.sleep(5)
    istuto.clear()
    istuto.append("off")
    arys[0] = 0
    return await l313l.send_message(event.chat_id, "**- تم الإنتهـاء من تثبيت اليـوزر ع حسـابك .. بنجـاح ✅**")


@l313l.ar_cmd(pattern="تثبيت_بوت (.*)")
async def _(event):
    zelzal = str(event.pattern_match.group(1))
    if not zelzal.startswith('@'):
        return await edit_or_reply(event, "**⎉╎عـذراً عـزيـزي المدخـل خطـأ ❌**\n**⎉╎استخـدم الامـر كالتالـي**\n**⎉╎ارسـل (**`.تثبيت_بوت`** + اليـوزر)**")
    await edit_or_reply(event, f"**⎉╎تم بـدء التثبيت .. بنجـاح ☑️**\n**⎉╎اليـوزر المثبت ( {zelzal} )**\n**⎉╎لمعرفـة تقـدم عمليـة التثبيت (**`.حالة تثبيت_البوت`**)**\n**⎉╎لـ ايقـاف عمليـة التثبيت (**`.ايقاف تثبيت_البوت`**)**")
    isbuto.clear()
    isbuto.append("on")
    username = zelzal.replace("@", "") 
    bmodels = True
    zzznm = "⎉ تثبيت زدثون 𝗭𝗧𝗵𝗼𝗻 ⎉"
    zzzby = "تم تثبيت اليـوزر بواسطـة سـورس زدثـــون - @ZThon "
    while bmodels:
        isbt = await checker_user(username)
        if isbt == True:
            try:
                await bot.send_message("@BotFather", "/newbot")
                await asyncio.sleep(1)
                await bot.send_message("@BotFather", zzznm)
                await asyncio.sleep(1)
                await bot.send_message("@BotFather", zelzal)
                await asyncio.sleep(3)
                await bot.send_message("@BotFather", "/setabouttext")
                await asyncio.sleep(1)
                await bot.send_message("@BotFather", zelzal)
                await asyncio.sleep(1)
                await bot.send_message("@BotFather", zzzby)
                await asyncio.sleep(3)
                await bot.send_message("@BotFather", "/setdescription")
                await asyncio.sleep(1)
                await bot.send_message("@BotFather", zelzal)
                await asyncio.sleep(1)
                await bot.send_message("@BotFather", zzzby)
                await event.client.send_message(
                    event.chat_id,
                    f"- Done : @{username} ✅\n- Save: ❲ Bot ❳\n- By : @ZThon \n- Hunting Log {brys[0]}",
                )
                break
            except FloodWaitError as zed: #Code by t.me/zzzzl1l
                wait_time = zed.seconds
                await sleep(wait_time + 10)
                pass
            except telethon.errors.rpcerrorlist.UsernameInvalidError:
                pass
            except telethon.errors.FloodError as e:
                flood_error = e.seconds
                await sleep(flood_error + 10)
                pass
            except Exception as eee:
                if "USERNAME_PURCHASE_AVAILABLE" in str(eee):
                    pass
                if "username is already taken" in str(eee):
                    pass
                else:
                    await l313l.send_message(
                        event.chat_id,
                        f"""- خطأ مع @{username} , الخطأ :{str(eee)}""",
                    )
                    break
        else:
            pass
        brys[0] += 1

        await asyncio.sleep(5)
    isbuto.clear()
    isbuto.append("off")
    brys[0] = 0
    return await l313l.send_message(event.chat_id, "**- تم الإنتهـاء من تثبيت البـوت .. بنجـاح ✅**\n**- لـ التأكـد قـم بالذهـاب الـى @BotFather**")


@l313l.ar_cmd(pattern="حالة الصيد")
async def _(event):
    if "on" in itsclim:
        await edit_or_reply(event, f"**- الصيد وصل لـ({trys[0]}) من المحـاولات**")
    elif "off" in itsclim:
        await edit_or_reply(event, "**- لا توجد عمليـة صيد جاريـه حاليـاً ؟!**")
    else:
        await edit_or_reply(event, "**- لقد حدث خطأ ما وتوقف الامر لديك**")

@l313l.ar_cmd(pattern="حالة تثبيت_القناة")
async def _(event):
    if "on" in iscuto:
        await edit_or_reply(event, f"**- التثبيت وصل لـ({crys[0]}) من المحاولات**")
    elif "off" in iscuto:
        await edit_or_reply(event, "**- لا توجد عمليـة تثبيث جاريـه حاليـاً ؟!**")
    else:
        await edit_or_reply(event, "-لقد حدث خطأ ما وتوقف الامر لديك")

@l313l.ar_cmd(pattern="حالة تثبيت_الحساب")
async def _(event):
    if "on" in istuto:
        await edit_or_reply(event, f"**- التثبيت وصل لـ({arys[0]}) من المحاولات**")
    elif "off" in istuto:
        await edit_or_reply(event, "**- لا توجد عمليـة تثبيث جاريـه حاليـاً ؟!**")
    else:
        await edit_or_reply(event, "-لقد حدث خطأ ما وتوقف الامر لديك")

@l313l.ar_cmd(pattern="حالة تثبيت_البوت")
async def _(event):
    if "on" in isbuto:
        await edit_or_reply(event, f"**- التثبيت وصل لـ({brys[0]}) من المحاولات**")
    elif "off" in isbuto:
        await edit_or_reply(event, "**- لا توجد عمليـة تثبيث جاريـه حاليـاً ؟!**")
    else:
        await edit_or_reply(event, "-لقد حدث خطأ ما وتوقف الامر لديك")


@l313l.ar_cmd(pattern="ايقاف تثبيت_القناة")
async def _(event):
    if "on" in iscuto:
        iscuto.clear()
        iscuto.append("off")
        crys[0] = 0
        return await edit_or_reply(event, "**- تم إيقـاف عمليـة التثبيت .. بنجـاح ✓**")
    elif "off" in iscuto:
        return await edit_or_reply(event, "**- لا توجد عمليـة تثبيث جاريـه حاليـاً ؟!**")
    else:
        return await edit_or_reply(event, "**-لقد حدث خطأ ما وتوقف الامر لديك**")

@l313l.ar_cmd(pattern="ايقاف تثبيت_الحساب")
async def _(event):
    if "on" in istuto:
        istuto.clear()
        istuto.append("off")
        arys[0] = 0
        return await edit_or_reply(event, "**- تم إيقـاف عمليـة التثبيت .. بنجـاح ✓**")
    elif "off" in istuto:
        return await edit_or_reply(event, "**- لا توجد عمليـة تثبيث جاريـه حاليـاً ؟!**")
    else:
        return await edit_or_reply(event, "**-لقد حدث خطأ ما وتوقف الامر لديك**")

@l313l.ar_cmd(pattern="ايقاف تثبيت_البوت")
async def _(event):
    if "on" in isbuto:
        isbuto.clear()
        isbuto.append("off")
        brys[0] = 0
        return await edit_or_reply(event, "**- تم إيقـاف عمليـة التثبيت .. بنجـاح ✓**")
    elif "off" in isbuto:
        return await edit_or_reply(event, "**- لا توجد عمليـة تثبيث جاريـه حاليـاً ؟!**")
    else:
        return await edit_or_reply(event, "**-لقد حدث خطأ ما وتوقف الامر لديك**")

