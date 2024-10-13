from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login, influencer
from flask import request, session, url_for, redirect




class image_operations(Resource):
    def put(self):
        data = request.json
        username = request.args.get("username")
        
        if request.method == "PUT":
            inf_id = login.query.filter_by(username=username).first().data_id
            inf = influencer.query.filter_by(inf_id=inf_id).first()

            inf.profile_pic = data["image_url"]

            db.session.commit()

            return "Profile Picture Updated"


            




