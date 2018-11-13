from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, jwt_required
import datetime

from security import authenticate, identity

from models.profile import ProfileModel
from models.user import UserModel

from resources.user import UserRegister
from resources.profile import ProfileRegister
from otp_handler import gen_send_otp, otp_check

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(UserRegister, '/signup')
api.add_resource(ProfileRegister, '/profile/<string:name>')


@app.route('/confirm', methods=['POST'])
def confirm():
    data = UserRegister.parser.parse_args()
    user = UserModel.find_by_username(data["username"])

    if otp_check(data["otp"], user):
        user.save_to_db()
        return jsonify({"message": "OTP matched"})
    return jsonify({"message": "OTP not matched"})


@app.route('/forgot', methods=["POST"])
def forgot_password():
    data = UserRegister.parser.parse_args()
    user = UserModel.find_by_username(data['username'])
    if user is None:
        return "user of this name doesn't exist"
    confirm = False
    user.otp = gen_send_otp(user, confirm)
    print(user.otp)
    user.otp_sent = datetime.datetime.utcnow()
    user.save_to_db()
    return jsonify({"message": "OTP has been sent to your mail"})


@app.route('/reset', methods=["POST"])
def reset():
    data = UserRegister.parser.parse_args()
    user = UserModel.find_by_username(data['username'])
    if user.otp == data["otp"]:
        user.password = data["password"]
        user.save_to_db()
        return jsonify({"message": "your password has been reset. Login again"})
    return jsonify({"message": "otp doesnt match!! try /forgot again"})


@app.route('/resend', methods= ["POST"])
def call_forgot():
    forgot_password()
    return jsonify({"message":"OTP has been sent to your mail"})


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5001, debug=True)