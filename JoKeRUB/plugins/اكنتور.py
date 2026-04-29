import os
import re

try:
    import akinator
except ModuleNotFoundError:
    os.system("pip3 install akinator.py")
    import akinator

from telethon import Button
from telethon.errors import BotMethodInvalidError
from telethon.events import CallbackQuery, InlineQuery

from . import l313l

from ..Config import Config
from ..core.decorators import check_owner

games = {}
aki_photo = "https://graph.org/file/b0ff07069e8637783fdae.jpg"


@l313l.ar_cmd(pattern="اكينوتر(?:\s|$)([\s\S]*)")
async def rozdo(e):
    sta = akinator.Akinator()
    games.update({e.chat_id: {e.id: sta}})
    try:
        m = await e.client.inline_query(
            Config.TG_BOT_USERNAME, f"aki_{e.chat_id}_{e.id}"
        )
        await m[0].click(e.chat_id)
    except BotMethodInvalidError:
        return await e.send_file(
            e.chat_id, aki_photo, caption="** ᥀︙حاول مجدداً مرة اخرى*"
        )
    if e.out:
        await e.delete()


@l313l.tgbot.on(CallbackQuery(data=re.compile(b"aki_?(.*)")))
@check_owner
async def daj(e):
    adt = e.pattern_match.group(1).strip().decode("utf-8")
    dt = adt.split("_")
    ch = int(dt[0])
    mid = int(dt[1])
    await e.edit("** ᥀︙جار التحقق انتظر قليلاً**")
    try:
        aki = games[ch][mid]
        aki.child_mode = True  # تفعيل الوضع الآمن بهذه الطريقة
        qu = aki.start_game()
    except KeyError:
        return await e.answer("تم إنهاء اللعبة", alert=True)
    except Exception as ex:
        return await e.answer(f"خطأ: {str(ex)[:50]}", alert=True)
    
    bts = [Button.inline(o, f"aka_{adt}_{o}") for o in ["نعم", "لا", "لا أعلم"]]
    cts = [Button.inline(o, f"aka_{adt}_{o}") for o in ["من المحتمل", "على الاغلب لا"]]
    bts = [bts, cts]
    await e.edit(f"Q. {qu}", buttons=bts)


@l313l.tgbot.on(CallbackQuery(data=re.compile(b"aka_?(.*)")))
@check_owner
async def rooks(e):
    mk = e.pattern_match.group(1).decode("utf-8").split("_")
    ch = int(mk[0])
    mid = int(mk[1])
    ans = mk[2]
    try:
        gm = games[ch][mid]
    except KeyError:
        await e.answer("انتهت الجلسة! ابدأ لعبة جديدة", alert=True)
        return
    
    try:
        # تحويل الإجابة إلى اللغة التي تفهمها المكتبة
        answer_map = {
            "نعم": "yes",
            "لا": "no",
            "لا أعلم": "idk",
            "من المحتمل": "probably",
            "على الاغلب لا": "probably_not"
        }
        text = gm.answer(answer_map.get(ans, "idk"))
        
        if gm.progression >= 80:
            gm.win()
            gs = gm.first_guess
            result = f"🎉 **التخمين:** {gs['name']}\n📝 **الوصف:** {gs['description']}"
            if gs.get('absolute_picture_path'):
                await e.edit(result, file=gs['absolute_picture_path'])
            else:
                await e.edit(result)
            return
        
        bts = [Button.inline(o, f"aka_{ch}_{mid}_{o}") for o in ["نعم", "لا", "لا أعلم"]]
        cts = [Button.inline(o, f"aka_{ch}_{mid}_{o}") for o in ["من المحتمل", "على الاغلب لا"]]
        bts = [bts, cts]
        await e.edit(text, buttons=bts)
        
    except Exception as ex:
        await e.answer(f"خطأ: {str(ex)[:50]}", alert=True)

@l313l.tgbot.on(InlineQuery)
async def rozak(e):
    query_user_id = e.query.user_id
    query = e.text
    string = query.lower()
    if (
        query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS
    ) and string.startswith("aki"):
        ans = [
            await e.builder.photo(
                aki_photo,
                text=query,
                buttons=[Button.inline("‹ بدء اللعب ›", data=e.text)],
            )
        ]
        await e.answer(ans)
