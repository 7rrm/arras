from sqlalchemy import Column, Numeric, String, UnicodeText, Integer
from sqlalchemy.exc import OperationalError

from . import BASE, SESSION


class Katm(BASE):
    __tablename__ = "zedkatms"
    chat_id = Column(String(14), primary_key=True)
    ktm_id = Column(String(14), primary_key=True, nullable=False)
    f_name = Column(UnicodeText)
    f_reason = Column(UnicodeText)
    is_temporary = Column(Integer, default=0)
    mute_time = Column(String(20), default="")

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


def create_table_safe():
    try:
        # إنشاء الجدول الأساسي
        Katm.__table__.create(bind=SESSION.get_bind(), checkfirst=True)
        
        # محاولة إضافة الأعمدة الجديدة إذا لم تكن موجودة
        try:
            SESSION.execute("ALTER TABLE zedkatms ADD COLUMN IF NOT EXISTS is_temporary INTEGER DEFAULT 0")
            SESSION.execute("ALTER TABLE zedkatms ADD COLUMN IF NOT EXISTS mute_time VARCHAR(20) DEFAULT ''")
            SESSION.commit()
        except OperationalError:
            SESSION.rollback()
    except Exception as e:
        print(f"حدث خطأ أثناء إنشاء الجدول: {e}")
    finally:
        SESSION.close()


create_table_safe()


def get_katm(chat_id, ktm_id):
    try:
        return SESSION.query(Katm).get((str(chat_id), str(ktm_id)))
    finally:
        SESSION.close()


def get_katms(chat_id, is_temporary=None):
    try:
        query = SESSION.query(Katm).filter(Katm.chat_id == str(chat_id))
        if is_temporary is not None:
            query = query.filter(Katm.is_temporary == is_temporary)
        return query.all()
    except OperationalError:
        # إذا كانت الأعمدة غير موجودة، استخدم الاستعلام الأساسي
        return SESSION.query(Katm).filter(Katm.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()


def add_katm(chat_id, ktm_id, f_name, f_reason, is_temporary=0, mute_time=""):
    try:
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
    except Exception as e:
        SESSION.rollback()
        print(f"Error in add_katm: {e}")
        return False


def remove_katm(chat_id, ktm_id):
    try:
        to_check = get_katm(chat_id, ktm_id)
        if not to_check:
            return False
        
        rem = SESSION.query(Katm).get((str(chat_id), str(ktm_id)))
        SESSION.delete(rem)
        SESSION.commit()
        return True
    except Exception as e:
        SESSION.rollback()
        print(f"Error in remove_katm: {e}")
        return False


def remove_all_katms(chat_id, is_temporary=None):
    try:
        query = SESSION.query(Katm).filter(Katm.chat_id == str(chat_id))
        if is_temporary is not None:
            query = query.filter(Katm.is_temporary == is_temporary)
        
        deleted_count = query.delete()
        SESSION.commit()
        return deleted_count > 0
    except OperationalError:
        # إذا كانت الأعمدة غير موجودة، استخدم الاستعلام الأساسي
        deleted_count = SESSION.query(Katm).filter(Katm.chat_id == str(chat_id)).delete()
        SESSION.commit()
        return deleted_count > 0
    except Exception as e:
        SESSION.rollback()
        print(f"Error in remove_all_katms: {e}")
        return False
