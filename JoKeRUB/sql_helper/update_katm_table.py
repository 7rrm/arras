from sqlalchemy import Integer, String
from sqlalchemy.sql import text

from . import BASE, SESSION


def update_katm_table():
    try:
        # إضافة الأعمدة الجديدة إذا لم تكن موجودة
        SESSION.execute(text("""
            ALTER TABLE zedkatms 
            ADD COLUMN IF NOT EXISTS is_temporary INTEGER DEFAULT 0
        """))
        
        SESSION.execute(text("""
            ALTER TABLE zedkatms 
            ADD COLUMN IF NOT EXISTS mute_time VARCHAR(20) DEFAULT ''
        """))
        
        SESSION.commit()
        print("تم تحديث جدول zedkatms بنجاح!")
    except Exception as e:
        SESSION.rollback()
        print(f"حدث خطأ أثناء تحديث الجدول: {e}")
    finally:
        SESSION.close()


if __name__ == "__main__":
    update_katm_table()
