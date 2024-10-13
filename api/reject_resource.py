from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login, companies, ad_requests, campaigns, all_contracts, negotiations
from flask import request, session, url_for, redirect


class reject_operations(Resource):

    def post(self):
        username = request.args.get("username")
        inf_id = login.query.filter_by(username=username).first().data_id
        contract_id = request.args.get("contract_id")
        if request.method == "POST":
            negotiation_entry = negotiations.query.filter_by(inf_id=inf_id, ad_id=contract_id).first()
            if negotiation_entry:
                db.session.delete(negotiation_entry)

            rejected_contract = all_contracts(
                inf_id=inf_id,
                contract_id=contract_id,
                status="Rejected",
            )

            db.session.add(rejected_contract)
            db.session.commit()

            return "Rejected Contract Details Added"