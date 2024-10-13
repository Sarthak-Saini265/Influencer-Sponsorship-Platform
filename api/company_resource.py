from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login, companies
from flask import request, session, url_for, redirect


class company_operations(Resource):

    def put(self):
        username = request.args.get("username")

        if request.method == "PUT":
            user = login.query.filter_by(username=username).first()
            sp_id = login.query.filter_by(username=username).first().data_id
            sp = companies.query.filter_by(company_id=sp_id).first()
            data = request.json
            if data['username'] != user.username:
                if data["username"] not in [i[0] for i in login.query.with_entities(login.username).all()]:
                    user.username = data["username"]
                else:
                    abort(409, error="Username already exists")
            if data["name"] != sp.name:
                sp.name = data["name"]
            if data["domain"] != sp.domain:
                sp.domain = data["domain"]
            if data["year_founded"] != sp.year_founded:
                sp.year_founded = data["year_founded"]
            if data["industry"] != sp.industry:
                sp.industry = data["industry"]
            if data["country"] != sp.country:
                sp.country = data["country"]
            if data["budget"] != sp.budget:
                sp.budget = int(data["budget"]) / 1000
            if data["linkedin"] != sp.linkedin_url:
                sp.linkedin_url = data["linkedin"]

            db.session.commit()

            return "Information updated"


