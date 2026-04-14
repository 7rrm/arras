import re
from telethon import Button
from telethon.events import CallbackQuery, InlineQuery
from JoKeRUB import CMD_HELP, l313l
from ..core.decorators import check_owner

CALC = {}
plugin_category = "utils"

m = [
    "AC", "C", "⌫", "%", "7", "8", "9", "+", "4", "5", "6", "-", "1", "2", "3", "x", "00", "0", ".", "÷"
]
tultd = [Button.inline(f"{x}", data=f"calc{x}") for x in m]
lst = list(zip(tultd[::4], tultd[1::4], tultd[2::4], tultd[3::4]))
lst.append([Button.inline("=", data="calc=")])

@l313l.on(admin_cmd(pattern="حاسبة(?:\s|$)([\s\S]*)"))
async def icalc(e):
    # التحقق مما إذا كان العميل يعمل كبوت
    if hasattr(e.client, 'bot_token') and e.client.bot_token:
        return await e.reply("**الحَـاسبة العـملية للـمطور\n @Lx5x5**", buttons=lst)
    
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
        calc = event.builder.article("Calc", text="****الحَـاسبة العـملية للـمطور\n @Lx5x5**", buttons=lst)
        await event.answer([calc])

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"calc(.*)")))
@check_owner
async def _(e):
    x = (e.data_match.group(1)).decode()
    user = e.query.user_id
    get = None
    if x == "AC":
        if CALC.get(user):
            CALC.pop(user)
        await e.edit("***الحَـاسبة العـملية للـمطور\n @Lx5x5**", buttons=[Button.inline("افتح مره اخرى", data="recalc")])
    elif x == "C":
        if CALC.get(user):
            CALC.pop(user)
        await e.answer("تم الحذف")
    elif x == "⌫":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get[:-1]})
            await e.answer(str(get[:-1]))
    elif x == "%":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "/100"})
            await e.answer(str(get + "/100"))
    elif x == "÷":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "/"})
            await e.answer(str(get + "/"))
    elif x == "x":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "*"})
            await e.answer(str(get + "*"))
    elif x == "=":
        if CALC.get(user):
            get = CALC[user]
        if get:
            if get.endswith(("*", ".", "/", "-", "+")):
                get = get[:-1]
            try:
                out = eval(get)
                num = float(out)
                await e.answer(f"▾∮ الجـواب : {num}", cache_time=0, alert=True)
            except Exception as ex:
                CALC.pop(user)
                await e.answer(f"خـطأ: {str(ex)}", cache_time=0, alert=True)
        else:
            await e.answer("غير معروف")
    else:
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + x})
            await e.answer(str(get + x))
        else:
            CALC.update({user: x})
            await e.answer(str(x))

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"recalc")))
@check_owner
async def _(e):
    m = [
        "AC", "C", "⌫", "%", "7", "8", "9", "+", "4", "5", "6", "-", "1", "2", "3", "x", "00", "0", ".", "÷"
    ]
    tultd = [Button.inline(f"{x}", data=f"calc{x}") for x in m]
    lst = list(zip(tultd[::4], tultd[1::4], tultd[2::4], tultd[3::4]))
    lst.append([Button.inline("=", data="calc=")])
    await e.edit("**الحـاسبة العـلمية لسـورس آراس\n @Lx5x5**", buttons=lst)

CMD_HELP.update({
    "الحسابة": ".حاسبة" "\n فقط اكتب الامر لعرض حاسبة علميه تحتاج الى تفعيل وضع الانلاين اولا\n\n"
})
