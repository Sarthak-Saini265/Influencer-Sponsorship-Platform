from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login
from flask import request, session, url_for, redirect




class flag_operations(Resource):

    def put(self):
        username = request.args.get("username")
        if request.method == "PUT":
            data = request.json
            user = login.query.filter_by(username=username).first()
            if not user:
                abort(404, error="User Not Found")
            else:
                if data['todo'] == "flag":
                    user.warnings = 'Flagged'
                    db.session.commit()
                    return "User Flagged Successfully"
                elif data['todo'] == "unflag":
                    user.warnings = None
                    db.session.commit()
                    return "User Unflagged Successfully"











