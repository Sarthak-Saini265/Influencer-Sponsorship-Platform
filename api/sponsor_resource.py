from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login, companies
from flask import request, session, url_for, redirect


class sponsor_operations(Resource):

    def post(self):
        username = request.args.get("username")
        if request.method == "POST":
            data = request.json

            form_data = data[0]

            user = login.query.filter_by(username=username).first()

            sp = companies(
                user_id=user.user_id,
                name=form_data["name"],
                domain=form_data["domain"],
                year_founded=form_data["year_founded"],
                industry=form_data["industry"],
                country=form_data["country"],
                budget=form_data["budget"],
                linkedin_url=form_data["linkedin"],
                logo=data[1],
            )

            db.session.add(sp)
            db.session.commit()

            user.data_id = sp.company_id
            db.session.commit()

            return "User Created"

