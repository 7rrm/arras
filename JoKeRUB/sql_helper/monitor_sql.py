from sqlalchemy import Column, String
from ..sql_helper import SESSION, BASE

class MonitoredUser(BASE):
    __tablename__ = "monitored_users"
    user_id = Column(String(64), primary_key=True)

    def __init__(self, user_id):
        self.user_id = user_id

MonitoredUser.__table__.create(checkfirst=True)

def add_monitored_user(user_id):
    try:
        if SESSION.query(MonitoredUser).filter(MonitoredUser.user_id == user_id).first():
            return False
        SESSION.add(MonitoredUser(user_id))
        SESSION.commit()
        return True
    except:
        SESSION.rollback()
        return False
    finally:
        SESSION.close()

def remove_monitored_user(user_id):
    try:
        if user := SESSION.query(MonitoredUser).filter(MonitoredUser.user_id == user_id).first():
            SESSION.delete(user)
            SESSION.commit()
            return True
        return False
    except:
        SESSION.rollback()
        return False
    finally:
        SESSION.close()

def get_all_monitored_users():
    try:
        return [user.user_id for user in SESSION.query(MonitoredUser).all()]
    except:
        return []
    finally:
        SESSION.close()
