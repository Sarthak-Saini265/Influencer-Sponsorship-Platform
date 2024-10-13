from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class login(db.Model):
    user_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    acc_type = db.Column(db.String(20), nullable = False)
    data_id  = db.Column(db.Integer)
    last_logged_in = db.Column(db.String(255), default=datetime.now().strftime("%d/%m/%y"))
    warnings = db.Column(db.String(30))

    def __repr__(self):
        return f"{self.user_id}-{self.username} {self.password} {self.acc_type}"

class influencer(db.Model):
    inf_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('login.user_id'),unique = True, nullable = False)
    name = db.Column(db.String(30), unique = False, nullable = False)
    gender = db.Column(db.String(15), nullable = False)
    niche = db.Column(db.String(70), unique=False, nullable=False)
    no_of_followers = db.Column(db.Integer, default=0)
    contracts_completed = db.Column(db.Integer, default=0)
    est_earnings = db.Column(db.Integer, default=0)
    no_of_posts = db.Column(db.Integer, nullable = False)
    est_reach = db.Column(db.Integer, default=0)
    rating = db.Column(db.Integer, default=0)
    profile_pic = db.Column(db.String(255), unique = False, default='https://img.freepik.com/premium-vector/user-profile-icon-flat-style-member-avatar-vector-illustration-isolated-background-human-permission-sign-business-concept_157943-15752.jpg', nullable = False)
    country = db.Column(db.String(70), unique=False, nullable=False)
    date_joined = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return f"{self.inf_id}-{self.name} {self.niche} {self.no_of_followers}"   

class companies(db.Model):
    company_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('login.user_id'),unique = True, nullable = False)
    name = db.Column(db.String(50), unique = False, nullable = False)
    domain = db.Column(db.String(50), unique = False, nullable = False)
    year_founded = db.Column(db.Integer, unique = False, default=2000)
    industry = db.Column(db.String(70), unique=False, nullable=False)
    country = db.Column(db.String(40), unique=False, nullable=False)
    linkedin_url = db.Column(db.String(200), unique=False, nullable=True)
    budget = db.Column(db.Integer, unique = False, nullable = False)
    logo = db.Column(db.String(255), unique = False, nullable = False)


    def __repr__(self):
        return f"{self.company_id}-{self.name} {self.domain} {self.country}"   
    
class campaigns(db.Model):
    campaign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique = False, nullable = False)
    description = db.Column(db.String(255), unique = False, nullable = False)
    start_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    end_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    company = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    spending = db.Column(db.Integer, unique = False, nullable = False)
    niches = db.Column(db.String(255), unique = False, nullable = False)
    warnings = db.Column(db.String(30))

    def __repr__(self):
        return f"{self.campaign_id}-{self.name} {self.description} {self.end_date}"
    
class ad_requests(db.Model):
    ad_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.campaign_id'))
    task = db.Column(db.String(255), unique = False, nullable = False)
    requirements = db.Column(db.String(255), unique = False, nullable = False)
    potential_payment = db.Column(db.Integer, unique = False, nullable = False)
    status = db.Column(db.String(20), unique = False, default='Pending')
    date_posted = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    number_of_completions = db.Column(db.Integer, unique = False, default=0)

    def __repr__(self):
        return f"{self.ad_id}-{self.campaign_id}-{self.task}-{self.status}-{self.number_of_completions}"   

class all_contracts(db.Model):
    inf_id = db.Column(db.Integer, db.ForeignKey('influencer.inf_id'), primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('ad_requests.ad_id'), primary_key=True, autoincrement=True)
    profit = db.Column(db.Integer, unique=False)
    company_profit = db.Column(db.Integer, unique=False)
    date_completed = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(20), unique = False)

    def __repr__(self):
        return f"{self.inf_id}-{self.contract_id} {self.profit}"

class negotiations(db.Model):
    inf_id = db.Column(db.Integer, db.ForeignKey('influencer.inf_id'), primary_key=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('ad_requests.ad_id'), primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    inf_price = db.Column(db.Integer, unique=False, nullable=True)
    sp_price = db.Column(db.Integer, unique=False, nullable=True)
    initiator = db.Column(db.String(20), unique = False)
    message = db.Column(db.String(255), unique = False)

    def __repr__(self):
        return f"{self.inf_id}-{self.ad_id} {self.inf_price}"




