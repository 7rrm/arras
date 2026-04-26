import re
from telethon import Button
from telethon.events import CallbackQuery, InlineQuery
from JoKeRUB import CMD_HELP, l313l
from ..core.decorators import check_owner

CALC = {}
plugin_category = "utils"

# دالة تحديد لون الزر حسب النوع
def get_button_style(btn):
    if btn in ["AC", "C", "⌫"]:
        return "danger"  # 🔴 أحمر - أزرار التحكم
    elif btn in ["+", "-", "x", "÷", "%", "="]:
        return "success"  # 🟢 أخضر - العمليات الحسابية والنتيجة
    else:
        return "primary"  # 🔵 أزرق - الأرقام

# إنشاء الأزرار بألوان
m = [
    "AC", "C", "⌫", "%", "7", "8", "9", "+", "4", "5", "6", "-", "1", "2", "3", "x", "00", "0", ".", "÷"
]
tultd = [Button.inline(f"{x}", data=f"calc{x}", style=get_button_style(x)) for x in m]
lst = list(zip(tultd[::4], tultd[1::4], tultd[2::4], tultd[3::4]))
lst.append([Button.inline("=", data="calc=", style="success")])

@l313l.on(admin_cmd(pattern="حاسبة(?:\s|$)([\s\S]*)"))
async def icalc(e):
    # التحقق مما إذا كان العميل يعمل كبوت
    if hasattr(e.client, 'bot_token') and e.client.bot_token:
        return await e.reply("**الحَـاسبة العـلمية لسـورس آراس\n @Lx5x5**", buttons=lst)
    
    # إذا لم يكن بوت، قم بتنفيذ الاستعلام المضمن
    results = await e.client.inline_query(Config.TG_BOT_USERNAME, "calc")
    await results[0].click(e.chat_id, silent=True, hide_via=True)
    await e.delete()

@l313l.tgbot.on(InlineQuery)
async def inlinecalc(event):
    query_user_id = event.query.user_id
    query = event.text
    string = query.lower()
    if (query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS) and string == "calc":
        calc = event.builder.article("Calc", text="**الحَـاسبة العـلمية لسـورس آراس\n @Lx5x5**", buttons=lst)
        await event.answer([calc])

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"calc(.*)")))
@check_owner
async def calc_handler(e):
    x = (e.data_match.group(1)).decode()
    user = e.query.user_id
    get = None
    
    if x == "AC":
        if CALC.get(user):
            CALC.pop(user)
        # إعادة فتح الحاسبة بأزرار ملونة
        m = [
            "AC", "C", "⌫", "%", "7", "8", "9", "+", "4", "5", "6", "-", "1", "2", "3", "x", "00", "0", ".", "÷"
        ]
        tultd = [Button.inline(f"{x}", data=f"calc{x}", style=get_button_style(x)) for x in m]
        lst_new = list(zip(tultd[::4], tultd[1::4], tultd[2::4], tultd[3::4]))
        lst_new.append([Button.inline("=", data="calc=", style="success")])
        await e.edit("**الحَـاسبة العـلمية لسـورس آراس\n @Lx5x5**", buttons=lst_new)
    
    elif x == "C":
        if CALC.get(user):
            CALC.pop(user)
        await e.answer("🗑 تم الحذف", alert=True)
    
    elif x == "⌫":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get[:-1]})
            await e.answer(str(get[:-1]), alert=False)
        else:
            await e.answer("⚠️ لا توجد أرقام للحذف", alert=True)
    
    elif x == "%":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "/100"})
            await e.answer(str(get + "/100"), alert=False)
        else:
            CALC.update({user: "0/100"})
            await e.answer("0/100", alert=False)
    
    elif x == "÷":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "/"})
            await e.answer(str(get + "/"), alert=False)
        else:
            await e.answer("⚠️ اكتب رقماً أولاً", alert=True)
    
    elif x == "x":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "*"})
            await e.answer(str(get + "*"), alert=False)
        else:
            await e.answer("⚠️ اكتب رقماً أولاً", alert=True)
    
    elif x == "+":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "+"})
            await e.answer(str(get + "+"), alert=False)
        else:
            await e.answer("⚠️ اكتب رقماً أولاً", alert=True)
    
    elif x == "-":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "-"})
            await e.answer(str(get + "-"), alert=False)
        else:
            await e.answer("⚠️ اكتب رقماً أولاً", alert=True)
    
    elif x == ".":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "."})
            await e.answer(str(get + "."), alert=False)
        else:
            CALC.update({user: "0."})
            await e.answer("0.", alert=False)
    
    elif x == "00":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "00"})
            await e.answer(str(get + "00"), alert=False)
        else:
            CALC.update({user: "00"})
            await e.answer("00", alert=False)
    
    elif x == "=":
        if CALC.get(user):
            get = CALC[user]
        if get:
            if get.endswith(("*", ".", "/", "-", "+")):
                get = get[:-1]
            try:
                out = eval(get)
                if isinstance(out, float) and out.is_integer():
                    out = int(out)
                CALC.pop(user)
                await e.answer(f"📐 النتيجة: {out}", alert=True)
            except Exception as ex:
                CALC.pop(user)
                await e.answer(f"❌ خطأ: {str(ex)}", alert=True)
        else:
            await e.answer("⚠️ لا توجد معادلة", alert=True)
    
    else:
        # الأرقام (0-9)
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + x})
            await e.answer(str(get + x), alert=False)
        else:
            CALC.update({user: x})
            await e.answer(str(x), alert=False)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"recalc")))
@check_owner
async def recalc_handler(e):
    m = [
        "AC", "C", "⌫", "%", "7", "8", "9", "+", "4", "5", "6", "-", "1", "2", "3", "x", "00", "0", ".", "÷"
    ]
    tultd = [Button.inline(f"{x}", data=f"calc{x}", style=get_button_style(x)) for x in m]
    lst = list(zip(tultd[::4], tultd[1::4], tultd[2::4], tultd[3::4]))
    lst.append([Button.inline("=", data="calc=", style="success")])
    await e.edit("**الحَـاسبة العـلمية لسـورس آراس\n @Lx5x5**", buttons=lst)

CMD_HELP.update({
    "الحسابة": ".حاسبة\n فقط اكتب الامر لعرض حاسبة علميه تحتاج الى تفعيل وضع الانلاين اولا\n\n"
})
