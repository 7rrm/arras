from sqlalchemy import Column, Numeric, String, UnicodeText, DateTime
from datetime import datetime

from . import BASE, SESSION


class Katm(BASE):
    __tablename__ = "zedkatms"
    chat_id = Column(String(14), primary_key=True)
    ktm_id = Column(String(14), primary_key=True, nullable=False)
    f_name = Column(UnicodeText)
    f_reason = Column(UnicodeText)
    is_temporary = Column(String(1), default="0")
    mute_time = Column(String(20))
    end_time = Column(DateTime)

    def __init__(self, chat_id, ktm_id, f_name, f_reason, is_temporary="0", mute_time=None, end_time=None):
        self.chat_id = str(chat_id)
        self.ktm_id = str(ktm_id)
        self.f_name = f_name
        self.f_reason = f_reason
        self.is_temporary = is_temporary
        self.mute_time = mute_time
        self.end_time = end_time

    def __eq__(self, other):
        return bool(
            isinstance(other, Katm)
            and self.chat_id == other.chat_id
            and self.ktm_id == other.ktm_id
        )


Katm.__table__.create(bind=SESSION.get_bind(), checkfirst=True)


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


def get_temporary_katms(chat_id):
    try:
        return SESSION.query(Katm).filter(
            Katm.chat_id == str(chat_id),
            Katm.is_temporary == "1"
        ).all()
    finally:
        SESSION.close()


def get_permanent_katms(chat_id):
    try:
        return SESSION.query(Katm).filter(
            Katm.chat_id == str(chat_id),
            Katm.is_temporary == "0"
        ).all()
    finally:
        SESSION.close()


def add_katm(chat_id, ktm_id, f_name, f_reason, is_temporary="0", mute_time=None, end_time=None):
    to_check = get_katm(chat_id, ktm_id)
    if not to_check:
        adder = Katm(str(chat_id), str(ktm_id), f_name, f_reason, is_temporary, mute_time, end_time)
        SESSION.add(adder)
        SESSION.commit()
        return True
    rem = SESSION.query(Katm).get((str(chat_id), str(ktm_id)))
    SESSION.delete(rem)
    SESSION.commit()
    adder = Katm(str(chat_id), str(ktm_id), f_name, f_reason, is_temporary, mute_time, end_time)
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
