from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login, influencer
from flask import request, session, url_for, redirect




class login_operations(Resource):
    def put(self):
        data = request.json
        username = request.args.get("username")
        
        if request.method == "PUT":
            user = login.query.filter_by(username=username).first()
            if data['current_password'] == user.password:
                user.password = data['new_password']
            else:
                abort(401, error="Unauthorized access. Wrong password")
            db.session.commit()

            return "Password updated"


            




