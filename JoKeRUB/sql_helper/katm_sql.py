from sqlalchemy import Column, Numeric, String, UnicodeText, Integer
from datetime import datetime, timedelta
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
        self.end_time = (datetime.now() + self.parse_time(mute_time)).timestamp()

    def parse_time(self, time_str):
        time_letter = time_str[-1].lower()
        time_number = int(time_str[:-1])
        time_dict = {
            's': timedelta(seconds=time_number),
            'm': timedelta(minutes=time_number),
            'h': timedelta(hours=time_number),
            'd': timedelta(days=time_number)
        }
        return time_dict.get(time_letter, timedelta(seconds=0))

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
    adder = Katm(str(chat_id), str(ktm_id), f_name, f_reason)
    SESSION.add(adder)
    SESSION.commit()

def remove_katm(chat_id, ktm_id):
    to_check = get_katm(chat_id, ktm_id)
    if not to_check:
        return False
    rem = SESSION.query(Katm).get((str(chat_id), str(ktm_id)))
    SESSION.delete(rem)
    SESSION.commit()
    return True

def remove_all_katms(chat_id):
    saved_katm = SESSION.query(Katm).filter(Katm.chat_id == str(chat_id))
    if saved_katm:
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
    adder = TempKatm(str(chat_id), str(ktm_id), f_name, f_reason, mute_time)
    SESSION.add(adder)
    SESSION.commit()

def remove_tempkatm(chat_id, ktm_id):
    to_check = get_tempkatm(chat_id, ktm_id)
    if not to_check:
        return False
    rem = SESSION.query(TempKatm).get((str(chat_id), str(ktm_id)))
    SESSION.delete(rem)
    SESSION.commit()
    return True

def remove_all_tempkatms(chat_id):
    saved_katm = SESSION.query(TempKatm).filter(TempKatm.chat_id == str(chat_id))
    if saved_katm:
        saved_katm.delete()
        SESSION.commit()

def check_expired_tempkatms(chat_id=None):
    current_time = datetime.now().timestamp()
    query = SESSION.query(TempKatm).filter(TempKatm.end_time <= current_time)
    if chat_id:
        query = query.filter(TempKatm.chat_id == str(chat_id))
    expired = query.all()
    for mute in expired:
        SESSION.delete(mute)
    SESSION.commit()
    return expired
