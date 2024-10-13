from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login, companies, campaigns
from flask import request, session, url_for, redirect
from datetime import datetime, timedelta


def to_datetime(date):
    dt_obj = datetime.fromisoformat(date)
    dt_obj = dt_obj + timedelta(seconds=59)
    return dt_obj

class campaign_operations(Resource):

    def post(self):
        username = request.args.get("username")
        if request.method == "POST":
            data = request.json

            user = login.query.filter_by(username=username).first()
            sp_id = user.data_id
            

            camp = campaigns(
                name=data['name'],
                description=data['description'],
                start_date=to_datetime(data['start_date']),
                end_date=to_datetime(data['end_date']),
                company=sp_id,
                spending=int(data['budget']) / 1000,
                niches=data['niches'],
            )

            db.session.add(camp)

            db.session.commit()

            return "Campaign Created"

        
    def put(self):
        username = request.args.get("username")
        campaign_id = request.args.get("campaign_id")
        if request.method == "PUT":
            data = request.json
            camp = campaigns.query.filter_by(campaign_id=campaign_id).first()
            if data['name'] != camp.name:
                camp.name = data['name']
            if data['description'] != camp.description:
                camp.description = data['description']
            if data['start_date'] != camp.start_date:
                camp.start_date = to_datetime(data['start_date'])
            if data['end_date'] != camp.end_date:
                camp.end_date = to_datetime(data['end_date'])
            if data['budget'] != camp.spending:
                camp.spending = int(data['budget'])/1000
            if data['niches'] != camp.niches:
                camp.niches = data['niches']

            db.session.commit()
        
            return "Campaign Updated"
        
    

    def delete(self):
        username = request.args.get("username")
        campaign_id = request.args.get("campaign_id")
        if request.method == "DELETE":
            camp = campaigns.query.filter_by(campaign_id=campaign_id).first()
            db.session.delete(camp)
            db.session.commit()
            return "Campaign Deleted"



    
        