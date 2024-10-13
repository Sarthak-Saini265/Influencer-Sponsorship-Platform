from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login
from flask import request, session, url_for, redirect


resource_fields = {
    "username": fields.String,
    "password": fields.String,
}


class login_user(Resource):
    @marshal_with(resource_fields)
    def get(self):
        username = request.args.get("username")
        user = login.query.filter_by(username=username).first()
        print(user)
        if user:
            if request.args.get("password") == user.password:
                return user
            else:
                abort(401, error="Unauthorized access")
        else:
            abort(404, error="OOPS! User not found")


    def post(self):
        signup_type = request.args.get("signup_type")
        data = request.json
        if data['username'] in [i[0] for i in login.query.with_entities(login.username).all()]:
            abort(409, error="Username already exists")

        else:
            user = login(username = data['username'], password = data['password'], acc_type = signup_type)
            db.session.add(user)
            db.session.commit()

        return "User created"







