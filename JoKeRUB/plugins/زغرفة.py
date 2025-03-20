import asyncio
import requests
import json
from asyncio import sleep
from telethon import events, types
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import l313l

@l313l.ar_cmd(pattern="زخرفه(?: |$)(.*)")
async def zelzal_gif(event):
    namz = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not namz and reply:
        return await edit_delete(event, "**- ارسـل (.زخرفه) + اسمـك بالانكلـش**", 10)
    if not namz:
        return await edit_delete(event, "**- ارسـل (.زخرفه) + اسمـك بالانكلـش**", 10)
    data = {
        'text': namz,
        '_csrf': '',
        'pages[]': [
            'New',
            'Unique',
            'CoolText',
        ],
    }
    response = requests.post('https://www.fancytextpro.com/generate', headers=headers, data=data)
    data = json.loads(response.content)
    #s1 = data['MusicalMap']
    s2 = data['neonCharMap']
    s3 = data['boldCharMap']
    s4 = data['EmojiMap']
    s4 = data['italicCharMap']
    s5 = data['AncientMap']
    s6 = data['Ladyleo']
    if "💋" in s6:
        s6 = s6.replace("💋 ", "").replace(" 💋", "")
    s7 = data['boldItalicCharMap']
    s8 = data['SinoTibetan']
    s9 = data['monospaceCharMap']
    s10 = data['weirdChar']
    s11 = data['BoldFloara']
    if "🌸" in s11:
        s11 = s11.replace("🌸ꗥ～ꗥ🌸 ", "ꗥ～").replace(" 🌸ꗥ～ꗥ🌸", "～ꗥ")
    s12 = data['upperAnglesCharMap']
    s13 = data['BuzzChar']
    s14 = data['greekCharMap']
    s15 = data['SunnyDay']
    s16 = data['invertedSquaresCharMap']
    if "🅰" in s16:
        s16 = s16.replace("🅰", "🅐")
    if "🅱" in s16:
        s16 = s16.replace("🅱", "🅑")
    if "🅿" in s16:
        s16 = s16.replace("🅿", "🅟")
    if "🅾" in s16:
        s16 = s16.replace("🅾", "🅞")
    s17 = data['TextDecorated']
    s18 = data['doubleStruckCharMap']
    s19 = data['Dessert']
    s20 = data['oldEnglishCharMap']
    s21 = data['taiVietCharMap']
    s22 = data["oldEnglishCharBoldMap"]
    s23 = data['oldItalicText']
    s24 = data['cursiveLetters']
    s25 = data['cursiveLettersBold']
    s26 = data['BoldJavaneseText']
    s27 = data['wideTextCharMap']
    s28 = data['subscriptCharMap']
    s29 = data['GunText']
    s30 = data['superscriptCharMap']
    s31 = data['ak47GunText']
    zz = "زخرفـه انكلـش\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆"
    aa = f"`{s2}`\n`{s3}`\n`{s4}`\n`{s5}`\n`{s6}`\n`{s7}`\n`{s8}`\n`{s9}`\n`{s10}`\n`{s11}`\n`{s12}`\n`{s13}`\n`{s14}`\n`{s15}`\n`{s16}`\n`{s17}`\n`{s18}`\n`{s19}`\n`{s20}`\n`{s21}`\n`{s22}`\n`{s23}`\n`{s24}`\n`{s25}`\n`{s26}`\n`{s27}`\n`{s28}`\n`{s29}`\n`{s30}`\n`{s31}`"
    dd = "࿐  𖣳  𓃠  𖡟  𖠜  ‌♡⁩  ‌༗  ‌𖢖  ❥  ‌ঌ  𝆹𝅥𝅮  𖠜\n𖠲  𖤍  𖠛  𝅘𝅥𝅮  ‌༒  ‌ㇱ  ߷  メ 〠  𓃬  𖠄\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\nl⌭l♥️🧸 زخرفـة انكلـش 30 نـوع تمبلـر -\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆"
    await edit_or_reply(event, f"**{zz}**\n{aa}\n\n**{dd}**")
    
