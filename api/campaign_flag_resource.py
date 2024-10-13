from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, campaigns
from flask import request, session, url_for, redirect




class campaign_flag_operations(Resource):

    def put(self):
        campaign_id = request.args.get("campaign_id")
        if request.method == "PUT":
            data = request.json
            campaign = campaigns.query.filter_by(campaign_id=campaign_id).first()
            if not campaign:
                abort(404, error="Campaign Not Found")
            else:
                if data['todo'] == "flag":
                    campaign.warnings = 'Flagged'
                    db.session.commit()
                    return "Campaign Flagged Successfully"
                elif data['todo'] == "unflag":
                    campaign.warnings = None
                    db.session.commit()
                    return "Campaign Unflagged Successfully"
    

    def delete(self):
        campaign_id = request.args.get("campaign_id")
        campaign = campaigns.query.filter_by(campaign_id=campaign_id).first()
        if not campaign:
            abort(404, error="Campaign Not Found")
        else:
            db.session.delete(campaign)
            db.session.commit()
            return "Campaign Deleted Successfully"











