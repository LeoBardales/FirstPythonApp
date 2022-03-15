from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, username,password,Activo,usertype,eid, fullname="") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.activo=Activo
        self.usertype=usertype
        self.eid=eid

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
