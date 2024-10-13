from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login, companies, campaigns, ad_requests
from flask import request, session, url_for, redirect
from datetime import datetime, timedelta



class ad_request_operations(Resource):

    def post(self):
        username = request.args.get("username")
        campaign_id = request.args.get("campaign_id")
        if request.method == "POST":
            data = request.json
            new_ad = ad_requests(
                campaign_id=campaign_id,
                task=data['task'],
                requirements=data['requirements'],
                potential_payment=int(data['potential_payment']),
            )
            db.session.add(new_ad)
            db.session.commit()
            return "Ad Request Added"

    def put(self):
        username = request.args.get("username")
        ad_id = request.args.get("ad_id")
        if request.method == "PUT":
            data = request.json
            ad = ad_requests.query.filter_by(ad_id=ad_id).first()
            if data['task'] != ad.task:
                ad.task = data['task']
            if data['requirements'] != ad.requirements:
                ad.requirements = data['requirements']
            if data['potential_payment'] != ad.potential_payment:
                ad.potential_payment = int(data['potential_payment'])

            db.session.commit()
        
            return "Ad Request Updated"
        
    
    def delete(self):
        username = request.args.get("username")
        ad_id = request.args.get("ad_id")
        if request.method == "DELETE":
            ad = ad_requests.query.filter_by(ad_id=ad_id).first()
            db.session.delete(ad)
            db.session.commit()
            return "Ad Request Deleted"


