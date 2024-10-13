from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login
from flask import request, session, url_for, redirect




class ban_operations(Resource):

    def put(self):
        username = request.args.get("username")
        if request.method == "PUT":
            user = login.query.filter_by(username=username).first()
            data = request.json
            if not user:
                abort(404, error="User Not Found")
            else:
                if data['todo'] == 'ban': 
                    user.warnings = 'Banned'
                    db.session.commit()
                    return "User Banned Successfully"
                elif data['todo'] == 'unban':
                    user.warnings = None
                    db.session.commit()
                    return "User Unbanned Successfully"










