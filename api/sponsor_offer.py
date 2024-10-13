from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login, companies, negotiations, ad_requests, campaigns
from flask import request, session, url_for, redirect


class sponsor_offer_operations(Resource):

    def post(self): 
        ad_id = request.args.get("ad_id")
        inf_id = request.args.get("inf_id")
        username = request.args.get("username")
        sp_id = login.query.filter_by(username=username).first().data_id
        ad = ad_requests.query.filter_by(ad_id=ad_id).first()
        if request.method == "POST":
            existing_neg = negotiations.query.filter_by(ad_id=ad_id, inf_id=inf_id).first()
            if existing_neg:
                abort(409, message="Offer already made")
            else:
                neg = negotiations(
                    inf_id=inf_id,
                    ad_id=ad_id,
                    company_id=sp_id,
                    sp_price=ad.potential_payment,
                    initiator="Sponsor",
                )
                db.session.add(neg)
                db.session.commit()
                return "Offer Made"
            
        