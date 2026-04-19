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

langs = {
    'عربي': 'ara',
    'بلغاري': 'bul',
    'صيني مبسط': 'chs',
    'صيني تقليدي': 'cht',
    'كرواتي': 'hrv',
    'دنماركي': 'dan',
    'هولندي': 'dut',
    'انجليزي': 'eng',
    'فنلندي': 'fin',
    'فرنسي': 'fre',
    'الماني': 'ger',
    'يوناني': 'gre',
    'هنغاري': 'hun',
    'كوري': 'kor',
    'ايطالي': 'ita',
    'ياباني': 'jpn',
    'نرويجي': 'nor',
    'بولندي': 'pol',
    'برتغالي': 'por',
    'روسي': 'rus',
    'سلوفيني': 'slv',
    'اسباني': 'spa',
    'سويدي': 'swe',
    'تركي': 'tur',
}

# ========== أمر عرض اللغات المدعومة ==========
@l313l.ar_cmd(pattern="اللغات")
async def get_supported_languages(event):
    """⌔ عرض اللغات المدعومة لاستخراج النص"""
    languages_list = "**⌔ اللغات المدعومة لأمر استخراج النص:**\n\n"
    for lang_name, lang_code in langs.items():
        languages_list += f"• **{lang_name}** : `{lang_code}`\n"
    
    languages_list += "\n**⌔ استخدم الأمر:** `.استخرج <اسم اللغة>`"
    await edit_or_reply(event, languages_list)

# ========== دالة استخراج النص ==========
def to_text(pic, api):
    try:
        output = api.ocr_file(open(pic, 'rb'))
    except Exception as e:
        return f"**⌔ حدث الخطأ التالي:**\n`{e}`"
    else:
        if output:
            return f"**⌔ النص المستخرج:**\n\n`{output}`"
        else:
            return "**⌔ حدث خطأ في النظام , حاول مجدداً**"
    finally:
        if os.path.exists(pic):
            os.remove(pic)

# ========== أمر استخراج النص ==========
@l313l.ar_cmd(pattern="استخرج(?:\s|$)([\s\S]*)",
               command=("استخرج", plugin_category),
              )
async def extract_text(event):
    """⌔ استخراج النص من الصورة"""
    reply = await event.get_reply_message()
    lan = event.pattern_match.group(1).strip()
    
    if not reply:
        return await edit_delete(event, "**⌔ قم بالرد على الصورة المراد استخراج النص منها**")
    
    # التحقق من وجود صورة
    if not reply.photo and not reply.document:
        return await edit_delete(event, "**⌔ قم بالرد على صورة فقط**")
    
    pic_file = await l313l.download_media(reply, Config.TMP_DOWNLOAD_DIRECTORY)
    
    if not pic_file:
        return await edit_delete(event, "**⌔ فشل تحميل الصورة , حاول مجدداً**")
    
    # إعداد API مع اللغة المطلوبة
    if not lan:
        api = ocrspace.API()
        lang_used = "الانجليزي (الافتراضية)"
    else:
        try:
            # البحث عن اللغة حتى لو كان الاسم غير كامل
            matched_lang = None
            for lang_name in langs:
                if lan.lower() in lang_name.lower() or lang_name.lower() in lan.lower():
                    matched_lang = lang_name
                    break
            
            if matched_lang:
                lang = langs[matched_lang]
                api = ocrspace.API(language=lang)
                lang_used = matched_lang
            else:
                return await edit_delete(event, f"**⌔ لا توجد لغة باسم `{lan}`**\n**⌔ استخدم امر `.اللغات` لعرض اللغات المدعومة**")
        except Exception as er:
            return await edit_delete(event, f"**⌔ حدث خطأ في اللغة:**\n`{er}`")
    
    # استخراج النص
    status_msg = await edit_or_reply(event, f"**⌔ يجري استخراج النص...**\n**⌔ اللغة المستخدمة:** `{lang_used}`")
    
    result = to_text(pic_file, api)
    await status_msg.edit(result)
