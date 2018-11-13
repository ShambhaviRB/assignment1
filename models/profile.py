from db import db


class ProfileModel(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), db.ForeignKey('users.username'))
    date_of_birth = db.Column(db.Integer)
    city = db.Column(db.String(80))
    phone_number = db.Column(db.Integer)

    def __init__(self, full_name, date_of_birth, city, phone_number):
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.city = city
        self.phone_number = phone_number

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, full_name):
        return cls.query.filter_by(full_name=full_name).first()

    def json(self):
        return {'full_name': self.full_name, 'date_of_birth': self.date_of_birth, 'city': self.city, 'phone_number': self.phone_number}