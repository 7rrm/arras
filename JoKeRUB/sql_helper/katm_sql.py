from sqlalchemy import Column, Numeric, String, UnicodeText, Integer
from datetime import datetime
from . import BASE, SESSION


class Katm(BASE):
    __tablename__ = "zedkatms"
    chat_id = Column(String(14), primary_key=True)
    ktm_id = Column(String(14), primary_key=True, nullable=False)
    f_name = Column(UnicodeText)
    f_reason = Column(UnicodeText)

    def __init__(self, chat_id, ktm_id, f_name, f_reason):
        self.chat_id = str(chat_id)
        self.ktm_id = str(ktm_id)
        self.f_name = f_name
        self.f_reason = f_reason

    def __eq__(self, other):
        return bool(
            isinstance(other, Katm)
            and self.chat_id == other.chat_id
            and self.ktm_id == other.ktm_id
        )


class TempKatm(BASE):
    __tablename__ = "zedtempkatms"
    chat_id = Column(String(14), primary_key=True)
    ktm_id = Column(String(14), primary_key=True, nullable=False)
    f_name = Column(UnicodeText)
    f_reason = Column(UnicodeText)
    mute_time = Column(String(20))
    end_time = Column(Numeric)

    def __init__(self, chat_id, ktm_id, f_name, f_reason, mute_time):
        self.chat_id = str(chat_id)
        self.ktm_id = str(ktm_id)
        self.f_name = f_name
        self.f_reason = f_reason
        self.mute_time = mute_time
        self.end_time = datetime.now().timestamp() + self.parse_time(mute_time)

    def parse_time(self, time_str):
        time_letter = time_str[-1]
        time_number = int(time_str[:-1])
        
        time_dict = {
            's': time_number,
            'm': time_number * 60,
            'h': time_number * 3600,
            'd': time_number * 86400
        }
        return time_dict.get(time_letter.lower(), 0)

    def __eq__(self, other):
        return bool(
            isinstance(other, TempKatm)
            and self.chat_id == other.chat_id
            and self.ktm_id == other.ktm_id
        )


# إنشاء الجداول
Katm.__table__.create(bind=SESSION.get_bind(), checkfirst=True)
TempKatm.__table__.create(bind=SESSION.get_bind(), checkfirst=True)

# دوال الكتم العام
def get_katm(chat_id, ktm_id):
    try:
        return SESSION.query(Katm).get((str(chat_id), str(ktm_id)))
    finally:
        SESSION.close()


def get_katms(chat_id):
    try:
        return SESSION.query(Katm).filter(Katm.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()


def add_katm(chat_id, ktm_id, f_name, f_reason):
    to_check = get_katm(chat_id, ktm_id)
    if not to_check:
        adder = Katm(str(chat_id), str(ktm_id), f_name, f_reason)
        SESSION.add(adder)
        SESSION.commit()
        return True
    rem = SESSION.query(Katm).get((str(chat_id), str(ktm_id)))
    SESSION.delete(rem)
    SESSION.commit()
    adder = Katm(str(chat_id), str(ktm_id), f_name, f_reason)
    SESSION.add(adder)
    SESSION.commit()
    return False


def remove_katm(chat_id, ktm_id):
    to_check = get_katm(chat_id, ktm_id)
    if not to_check:
        return False
    rem = SESSION.query(Katm).get((str(chat_id), str(ktm_id)))
    SESSION.delete(rem)
    SESSION.commit()
    return True


def remove_all_katms(chat_id):
    if saved_katm := SESSION.query(Katm).filter(Katm.chat_id == str(chat_id)):
        saved_katm.delete()
        SESSION.commit()

# دوال الكتم المؤقت
def get_tempkatm(chat_id, ktm_id):
    try:
        return SESSION.query(TempKatm).get((str(chat_id), str(ktm_id)))
    finally:
        SESSION.close()


def get_tempkatms(chat_id):
    try:
        return SESSION.query(TempKatm).filter(TempKatm.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()


def add_tempkatm(chat_id, ktm_id, f_name, f_reason, mute_time):
    to_check = get_tempkatm(chat_id, ktm_id)
    if not to_check:
        adder = TempKatm(str(chat_id), str(ktm_id), f_name, f_reason, mute_time)
        SESSION.add(adder)
        SESSION.commit()
        return True
    rem = SESSION.query(TempKatm).get((str(chat_id), str(ktm_id)))
    SESSION.delete(rem)
    SESSION.commit()
    adder = TempKatm(str(chat_id), str(ktm_id), f_name, f_reason, mute_time)
    SESSION.add(adder)
    SESSION.commit()
    return False


def remove_tempkatm(chat_id, ktm_id):
    to_check = get_tempkatm(chat_id, ktm_id)
    if not to_check:
        return False
    rem = SESSION.query(TempKatm).get((str(chat_id), str(ktm_id)))
    SESSION.delete(rem)
    SESSION.commit()
    return True


def remove_all_tempkatms(chat_id):
    if saved_katm := SESSION.query(TempKatm).filter(TempKatm.chat_id == str(chat_id)):
        saved_katm.delete()
        SESSION.commit()


def check_expired_tempkatms():
    current_time = datetime.now().timestamp()
    expired = SESSION.query(TempKatm).filter(TempKatm.end_time <= current_time).all()
    for mute in expired:
        remove_tempkatm(mute.chat_id, mute.ktm_id)
    SESSION.commit()
    return expired
