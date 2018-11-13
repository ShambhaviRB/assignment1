from flask_restful import Resource, reqparse
from models.profile import ProfileModel
from flask import jsonify
from flask_jwt import jwt_required


class ProfileRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date_of_birth',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('city',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('phone_number',
                        type=str,
                        required=False,
                        )

    #@jwt_required()
    def get(self, name):
        profile = ProfileModel.find_by_name(name)
        if profile:
            return profile.json()
        return {'message': 'profile not found'}, 404

    def post(self, name):
        data = ProfileRegister.parser.parse_args()
        profile = ProfileModel.find_by_name(name)
        if profile is None:
            profile = ProfileModel(name, **data)
            profile.save_to_db()
            return {"message": "Profile created successfully."}, 201
        return jsonify({"message": "Profile with this name already exists"})

    #@jwt_required()
    def delete(self, name):
        profile = ProfileModel.find_by_name(name)
        if profile:
            profile.delete_from_db()
        return {'message': 'Item deleted'}, 200

    #@jwt_required()
    def put(self, name):
        data = ProfileRegister.parser.parse_args()

        profile = ProfileModel.find_by_name(name)

        if profile is None:
            profile = ProfileModel(name, **data)
        if data['date_of_birth']:
            profile.date_of_birth = data['date_of_birth']
        if data['city']:
            profile.city = data['city']
        if data['phone_number']:
            profile.phone_number = data['phone_number']

        profile.save_to_db()
        return profile.json()