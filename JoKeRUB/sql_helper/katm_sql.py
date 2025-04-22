from sqlalchemy import Column, Numeric, String, UnicodeText, Integer

from . import BASE, SESSION


class Katm(BASE):
    __tablename__ = "zedkatms"
    chat_id = Column(String(14), primary_key=True)
    ktm_id = Column(String(14), primary_key=True, nullable=False)
    f_name = Column(UnicodeText)
    f_reason = Column(UnicodeText)
    is_temporary = Column(Integer, default=0)  # 0 for permanent, 1 for temporary
    mute_time = Column(String(20), default="")  # Store mute duration for temporary mutes

    def __init__(self, chat_id, ktm_id, f_name, f_reason, is_temporary=0, mute_time=""):
        self.chat_id = str(chat_id)
        self.ktm_id = str(ktm_id)
        self.f_name = f_name
        self.f_reason = f_reason
        self.is_temporary = is_temporary
        self.mute_time = mute_time

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


def get_katms(chat_id, is_temporary=None):
    try:
        if is_temporary is None:
            return SESSION.query(Katm).filter(Katm.chat_id == str(chat_id)).all()
        else:
            return SESSION.query(Katm).filter(
                Katm.chat_id == str(chat_id),
                Katm.is_temporary == is_temporary
            ).all()
    finally:
        SESSION.close()


def add_katm(chat_id, ktm_id, f_name, f_reason, is_temporary=0, mute_time=""):
    to_check = get_katm(chat_id, ktm_id)
    if not to_check:
        adder = Katm(str(chat_id), str(ktm_id), f_name, f_reason, is_temporary, mute_time)
        SESSION.add(adder)
        SESSION.commit()
        return True
    rem = SESSION.query(Katm).get((str(chat_id), str(ktm_id)))
    SESSION.delete(rem)
    SESSION.commit()
    adder = Katm(str(chat_id), str(ktm_id), f_name, f_reason, is_temporary, mute_time)
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


def remove_all_katms(chat_id, is_temporary=None):
    if is_temporary is None:
        saved_katm = SESSION.query(Katm).filter(Katm.chat_id == str(chat_id))
    else:
        saved_katm = SESSION.query(Katm).filter(
            Katm.chat_id == str(chat_id),
            Katm.is_temporary == is_temporary
        )
    if saved_katm:
        saved_katm.delete()
        SESSION.commit()
        return True
    return False
