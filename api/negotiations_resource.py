from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login, companies, negotiations, ad_requests, campaigns
from flask import request, session, url_for, redirect


class negotiations_operations(Resource):

    def post(self):
        ad_id = request.args.get("ad_id")
        inf_id = request.args.get("inf_id")
        if request.method == "POST":
            ad = ad_requests.query.filter_by(ad_id=ad_id).first()
            campaign_id = ad.campaign_id
            campaign = campaigns.query.filter_by(campaign_id=campaign_id).first()
            company_id = login.query.filter_by(data_id=campaign.company).first().user_id
            data = request.json
            existing_neg = negotiations.query.filter_by(ad_id=ad_id, inf_id=inf_id).first()
            if existing_neg:
                if data["message"] == "":
                    existing_neg.inf_price = data["negotiate_price"]
                    existing_neg.initiator = "Influencer"
                else:
                    existing_neg.inf_price = data["negotiate_price"]
                    existing_neg.initiator = "Influencer"
                    existing_neg.message = data["message"]
            else:
                if data["message"] == "":
                    neg = negotiations(
                        inf_id=inf_id,
                        ad_id=ad_id,
                        company_id=company_id,
                        inf_price=data["negotiate_price"],
                        initiator="Influencer",
                    )
                else:
                    neg = negotiations(
                        inf_id=inf_id,
                        ad_id=ad_id,
                        company_id=company_id,
                        inf_price=data["negotiate_price"],
                        initiator="Influencer",
                        message=data["message"],
                    )

                db.session.add(neg)
            db.session.commit()

            return "Negotiation Details Added"
        
    
    def delete(self):
        ad_id = request.args.get("ad_id")
        inf_id = request.args.get("inf_id")
        neg = negotiations.query.filter_by(ad_id=ad_id, inf_id=inf_id).first()
        db.session.delete(neg)
        db.session.commit()
        return "Negotiation Details Deleted"
