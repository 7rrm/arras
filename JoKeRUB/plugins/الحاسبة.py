import re
from telethon import Button
from telethon.events import CallbackQuery, InlineQuery
from JoKeRUB import CMD_HELP, l313l
from ..core.decorators import check_owner

CALC = {}
plugin_category = "utils"

# تعريف الأزرار بألوان مختلفة
m = [
    "AC", "C", "⌫", "%", "7", "8", "9", "+", "4", "5", "6", "-", "1", "2", "3", "x", "00", "0", ".", "÷"
]

def get_button_style(btn):
    if btn in ["AC", "C", "⌫"]:
        return "danger"  # أحمر للأزرار التحكم
    elif btn in ["+", "-", "x", "÷", "%"]:
        return "success"  # أخضر للعمليات الحسابية
    elif btn in ["="]:
        return "primary"  # أزرق للنتيجة
    else:
        return "primary"  # أزرق للأرقام

tultd = [Button.inline(f"{x}", data=f"calc{x}", style=get_button_style(x)) for x in m]
lst = list(zip(tultd[::4], tultd[1::4], tultd[2::4], tultd[3::4]))
lst.append([Button.inline("=", data="calc=", style="primary")])

@l313l.on(admin_cmd(pattern="حاسبة(?:\s|$)([\s\S]*)"))
async def icalc(e):
    if hasattr(e.client, 'bot_token') and e.client.bot_token:
        return await e.reply("**الحَـاسبة العـلمية لسـورس آراس\n @Lx5x5**", buttons=lst)
    
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
    current_text = "**الحَـاسبة العـلمية لسـورس آراس\n @Lx5x5**"
    
    if x == "AC":
        if CALC.get(user):
            CALC.pop(user)
        # إعادة فتح الحاسبة بأزرار ملونة
        m = [
            "AC", "C", "⌫", "%", "7", "8", "9", "+", "4", "5", "6", "-", "1", "2", "3", "x", "00", "0", ".", "÷"
        ]
        tultd = [Button.inline(f"{x}", data=f"calc{x}", style=get_button_style(x)) for x in m]
        lst_new = list(zip(tultd[::4], tultd[1::4], tultd[2::4], tultd[3::4]))
        lst_new.append([Button.inline("=", data="calc=", style="primary")])
        await e.edit(current_text, buttons=lst_new)
    
    elif x == "C":
        if CALC.get(user):
            CALC.pop(user)
        # ✅ إظهار رسالة "تم الحذف" فوق الأزرار
        await e.edit(f"**🗑 تم الحذف**\n\n{current_text}", buttons=lst)
    
    elif x == "⌫":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get[:-1]})
            await e.edit(f"**{get[:-1]}**\n\n{current_text}", buttons=lst)
        else:
            await e.answer("⚠️ لا توجد أرقام للحذف", alert=True)
    
    elif x == "%":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "/100"})
            await e.edit(f"**{get + '/100'}**\n\n{current_text}", buttons=lst)
        else:
            CALC.update({user: "0/100"})
            await e.edit(f"**0/100**\n\n{current_text}", buttons=lst)
    
    elif x == "÷":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "/"
