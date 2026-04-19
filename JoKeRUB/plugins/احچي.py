"""
JoKeRUB team ©
By Reda
sub Hussein
"""
import os
from datetime import datetime
import speech_recognition as sr
from pydub import AudioSegment

from JoKeRUB import l313l
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.utils import reply_id
import ocrspace

plugin_category = "utils"

#لتخمط الملف اذا انته ابن گحبة انسخ وألصق لسورسك وصيح اني مطور الملف متعوب عليه وشغل ايد

@l313l.ar_cmd(pattern="احجي(?:\s|$)([\s\S]*)",
               command=("احجي", plugin_category),
              )
async def _(event):
    "تحويل الكلام الى نص."
    
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    lan = input_str
    if not lan:
         return await edit_delete(event, "يجب ان تضع اختصار اللغة المطلوبة")
    
    #ted = await edit_or_reply(event, str(lan))
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    mediatype = media_type(reply)
    if not reply or (mediatype and mediatype not in ["Voice", "Audio"]):
        return await edit_delete(
            event,
            "`قم بالرد على رسالة او مقطع صوتي لتحويله الى نص.`",
        )
    jepevent = await edit_or_reply(event, "`يجري تنزيل الملف...`")
    oggfi = await event.client.download_media(reply, Config.TEMP_DIR)
    await jepevent.edit("`يجري تحويل الكلام الى نص....`")
    r = sr.Recognizer()
    #audio_data = open(required_file_name, "rb").read()
    ogg = oggfi.removesuffix('.ogg')
   
    AudioSegment.from_file(oggfi).export(f"{ogg}.wav", format="wav")
    user_audio_file = sr.AudioFile(f"{ogg}.wav")
    with user_audio_file as source:
         audio = r.record(source)

    
    try:
         text = r.recognize_google(audio, language=str(lan))
    except ValueError:
         return await edit_delete(event, "**لا يوجد كلام في المقطع الصوتي**")
    except BaseException as err:
         return await edit_delete(event, f"**!لا يوجد كلام في هذا المقطع الصوتي\n{err}**")
    end = datetime.now()
    ms = (end - start).seconds
    
    string_to_show = "**يگول : **`{}`".format(
            text
        )
    await jepevent.edit(string_to_show)
    # now, remove the temporary file
    os.remove(oggfi)
    os.remove(f"{ogg}.wav")

import os
import ocrspace
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply

plugin_category = "الادوات"

# ========== جميع اللغات المدعومة ==========
langs = {
    'عربي': 'ara',
    'بلغاري': 'bul',
    'صيني مبسط': 'chs',
    'صيني تقليدي': 'cht',
    'كرواتي': 'hrv',
    'تشيكي': 'cze',
    'دنماركي': 'dan',
    'هولندي': 'dut',
    'انجليزي': 'eng',
    'استوني': 'est',
    'فنلندي': 'fin',
    'فرنسي': 'fre',
    'الماني': 'ger',
    'يوناني': 'gre',
    'هنغاري': 'hun',
    'كوري': 'kor',
    'ايطالي': 'ita',
    'ياباني': 'jpn',
    'لاتفي': 'lav',
    'ليتواني': 'lit',
    'نرويجي': 'nor',
    'بولندي': 'pol',
    'برتغالي': 'por',
    'روماني': 'ron',
    'روسي': 'rus',
    'سلوفاكي': 'slk',
    'سلوفيني': 'slv',
    'اسباني': 'spa',
    'سويدي': 'swe',
    'تركي': 'tur',
    'اوكراني': 'ukr',
    'فيتنامي': 'vie',
}

# ========== أمر عرض جميع اللغات ==========
@l313l.ar_cmd(pattern="اللغات")
async def get_langs(event):
    """⌔ عرض جميع اللغات المدعومة"""
    txt = "**⌔ اللغات المدعومة لاستخراج النص:**\n\n"
    for name, code in langs.items():
        txt += f"• **{name}** : `{code}`\n"
    txt += "\n**⌔ استخدم:** `.استخرج <اسم اللغة>`"
    await edit_or_reply(event, txt)

# ========== أمر استخراج النص ==========
@l313l.ar_cmd(pattern="استخرج(?:\s|$)([\s\S]*)")
async def extract(event):
    """⌔ استخراج النص من الصورة"""
    reply = await event.get_reply_message()
    lan = event.pattern_match.group(1).strip()

    if not reply:
        return await edit_delete(event, "**⌔ قم بالرد على صورة لاستخراج النص منها**")

    if not reply.photo and not reply.document:
        return await edit_delete(event, "**⌔ هذا ليس بصورة**")

    tmp = Config.TMP_DOWNLOAD_DIRECTORY or "./temp/"
    if not os.path.exists(tmp):
        os.makedirs(tmp)

    pic = await reply.download_media(tmp)
    if not pic:
        return await edit_delete(event, "**⌔ فشل تحميل الصورة**")

    status = await edit_or_reply(event, "**⌔ جاري استخراج النص...**")

    # ========== تحديد اللغة ==========
    try:
        if not lan:
            api = ocrspace.API()
            lang_used = "الانجليزي (الافتراضية)"
        elif lan in langs.values():
            api = ocrspace.API(language=lan)
            lang_used = lan
        elif lan in langs:
            api = ocrspace.API(language=langs[lan])
            lang_used = lan
        else:
            # البحث عن لغة مطابقة
            found = None
            for name, code in langs.items():
                if lan.lower() in name.lower() or name.lower() in lan.lower():
                    found = name
                    api = ocrspace.API(language=code)
                    lang_used = name
                    break
            if not found:
                return await status.edit(f"**⌔ لا توجد لغة باسم `{lan}`**\n**⌔ استخدم `.اللغات` لعرض اللغات المدعومة**")
    except Exception as e:
        return await status.edit(f"**⌔ خطأ في اللغة:**\n`{e}`")

    await status.edit(f"**⌔ يجري الاستخراج...**\n**⌔ اللغة:** `{lang_used}`")

    # ========== استخراج النص ==========
    try:
        with open(pic, 'rb') as f:
            result = api.ocr_file(f)
    except Exception as e:
        return await status.edit(f"**⌔ فشل الاستخراج:**\n`{e}`")
    finally:
        if os.path.exists(pic):
            os.remove(pic)

    if not result or result.strip() == "":
        return await status.edit("**⌔ لم يتم العثور على نص في الصورة**\n**⌔ تأكد أن النص واضح**")

    await status.edit(f"**⌔ النص المستخرج:**\n\n`{result}`")
