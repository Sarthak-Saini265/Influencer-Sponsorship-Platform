from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login, companies, ad_requests, campaigns, all_contracts, negotiations
from flask import request, session, url_for, redirect


class contract_operations(Resource):

    def post(self):
        ad_id = request.args.get("ad_id")
        inf_id = request.args.get("inf_id")
        if request.method == "POST":
            ad = ad_requests.query.filter_by(ad_id=ad_id).first()
            campaign_id = ad.campaign_id
            campaign = campaigns.query.filter_by(campaign_id=campaign_id).first()
            negotiation_entry = negotiations.query.filter_by(inf_id=inf_id, ad_id=ad_id).first()
            if negotiation_entry:
                if negotiation_entry.initiator == "Influencer":
                    new_contract = all_contracts(
                        inf_id=inf_id,
                        contract_id=ad_id,
                        profit=negotiation_entry.inf_price,
                        status="Accepted",
                    )
                else:
                    new_contract = all_contracts(
                        inf_id=inf_id,
                        contract_id=ad_id,
                        profit=negotiation_entry.sp_price,
                        status="Accepted",
                    )
                db.session.delete(negotiation_entry)
            else:
                new_contract = all_contracts(
                        inf_id=inf_id,
                        contract_id=ad_id,
                        profit=ad.potential_payment,
                        status="Accepted",
                    )

            db.session.add(new_contract)
            db.session.commit()

            return "Contract Details Added"
        

    def put(self):
        username = request.args.get("username")
        inf_id = login.query.filter_by(username=username).first().data_id
        contract_id = request.args.get("contract_id")
        if request.method == "PUT":
            contract = all_contracts.query.filter_by(inf_id=inf_id, contract_id=contract_id).first()
            ad = ad_requests.query.filter_by(ad_id=contract_id).first()
            contract.date_completed = db.func.current_timestamp()
            contract.status = "Completed"
            contract.company_profit = contract.profit*3
            ad.number_of_completions += 1
            db.session.commit()
            return "Contract Status Updated"
    







