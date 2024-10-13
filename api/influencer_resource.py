from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login, influencer
from flask import request, session, url_for, redirect


class influencer_operations(Resource):

    def post(self):
        username = request.args.get("username")
        if request.method == "POST":
            data = request.json

            form_data = data[0]
            niches = data[1]
            print(data[-1])

            user = login.query.filter_by(username=username).first()
            name = form_data["first_name"] + " " + form_data["last_name"]
            niches = [i.title() for i in niches]
            niches_db_post = ";".join(niches)

            inf = influencer(
                user_id=user.user_id,
                name=name,
                gender=form_data["gender"],
                niche=niches_db_post,
                no_of_followers=form_data["insta_followers"],
                no_of_posts=form_data["insta_posts"],
                profile_pic=data[-1],
                country=form_data["country"],
            )

            db.session.add(inf)
            db.session.commit()

            user.data_id = inf.inf_id
            db.session.commit()

            return "User Created"

    def put(self):
        username = request.args.get("username")

        if request.method == "PUT":
            user = login.query.filter_by(username=username).first()
            inf_id = login.query.filter_by(username=username).first().data_id
            inf = influencer.query.filter_by(inf_id=inf_id).first()
            data = request.json
            if data['username'] != user.username:
                if data["username"] not in [i[0] for i in login.query.with_entities(login.username).all()]:
                    user.username = data["username"]
                else:
                    abort(409, error="Username already exists")
            if (data["first_name"] != inf.name.split(" ")[0]or data["last_name"] != inf.name.split(" ")[1]):
                inf.name = data["first_name"] + " " + data["last_name"]
            if data["gender"] != inf.gender:
                inf.gender = data["gender"]
            if data["country"] != inf.country:
                inf.country = data["country"]

            db.session.commit()

            return "Information updated"
