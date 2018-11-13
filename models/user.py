from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email_id = db.Column(db.String(80))
    password = db.Column(db.String(80))
    otp = db.Column(db.String(6))

    def __init__(self, username, password, email_id, otp):
        self.username = username
        self.email_id = email_id
        self.password = password
        self.otp = otp

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, email_id):
        return cls.query.filter_by(email_id=email_id).first()