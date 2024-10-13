from flask import Flask, render_template, request, redirect, url_for, session
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
import calendar
import random
from datetime import datetime, timedelta
from models import *
from flask_restful import Api, reqparse, abort
from api.login_resource import login_user
from api.influencer_resource import influencer_operations
from api.password_resource import login_operations
from api.upload_resource import image_operations
from api.campaign_resource import campaign_operations
from api.company_resource import company_operations
from api.negotiations_resource import negotiations_operations
from api.contract_resource import contract_operations
from api.reject_resource import reject_operations
from api.ad_request_resource import ad_request_operations
from api.flag_resource import flag_operations
from api.ban_resource import ban_operations
from api.campaign_flag_resource import campaign_flag_operations
from api.sponsor_offer import sponsor_offer_operations
from api.sp_negotiations_resource import sponsor_negotiations_operations
from api.sponsor_resource import sponsor_operations

secret_key = b'\xa2Z\xa2j\xf3\x93F\xf9\x9aF\xb6\xae\x03\xe4\xedv\x83\xf9\xbf\r$\xd5\x92\xbdiOdb\xa4\x9f\x00\x9f'

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///influencer.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.app_context().push()

def get_company_name(company_id):
    result = companies.query.filter_by(company_id=company_id).first()
    return result.name.title()

def format_title(title):
    return title.title()

def get_logo(company_id):
    result = companies.query.filter_by(company_id = company_id).first()
    return result.logo

def popular_ads(campaign_id):
    result = ad_requests.query.filter(ad_requests.campaign_id == campaign_id, ad_requests.number_of_completions > 150).order_by(ad_requests.number_of_completions.desc()).all()
    return [row for row in result]

def all_ads_camp(campaign_id):
    result = ad_requests.query.filter(ad_requests.campaign_id == campaign_id).order_by(ad_requests.date_posted.asc()).all()
    return [row for row in result]

def get_sp_ads(sp_id):
    sp_camp = campaigns.query.filter_by(company=sp_id).all()
    all_sp_ads = []
    for i in sp_camp:
        all_sp_ads.extend(all_ads_camp(i.campaign_id))
    return all_sp_ads

def remove_time(date):
    date = date.strftime("%d-%m-%Y")
    return str(date).split(' ')[0]

def get_username(inf_id):
    result = login.query.filter_by(data_id=inf_id).first()
    return result.username

def get_sp_username(user_id):
    result = login.query.filter_by(user_id=user_id).first()
    return result.username

def get_inf(inf_id):
    result = influencer.query.filter_by(inf_id=inf_id).first()
    return result



def get_month_name(date):
    return date.strftime('%B %Y')


def insert_commas(number):
    return '{:,}'.format(number)


def format_number(num):
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)



def to_datetime(date):
    dt_obj = datetime.fromisoformat(date)
    dt_obj = dt_obj + timedelta(seconds=59)
    return dt_obj


def get_price(ad_id):
    result = ad_requests.query.filter_by(ad_id=ad_id).first()
    return result.potential_payment






db_niches = influencer.query.with_entities(influencer.niche).all()
l = []
for i in range(len(db_niches)):
    l.extend(db_niches[i][0].split(';'))
    unique_niches = list(set(l))
    unique_niches = [i.title() for i in unique_niches]


# l = login.query.with_entities(login.username).all()
# l = [i[0] for i in l]
# print('skull_fern' in l)
# print(get_month_name(influencer.query.filter_by(inf_id=8).first().date_joined))


# print(get_company_name(5))
# a = campaigns.query.filter(campaigns.end_date > datetime.now().date()).all()
# print(a)

# print(login.query.filter_by(username='lust_goddess').first().data_id)

# print(get_company_name(2))

@app.route('/')
def hello():
    current_date = datetime.now().date()
    ongoing = campaigns.query.filter(campaigns.end_date > current_date).all()
        
    trending = ad_requests.query.filter(ad_requests.number_of_completions > 150).order_by(ad_requests.number_of_completions.desc()).limit(10).all()

    top = influencer.query.order_by(influencer.est_earnings.desc()).limit(8).all()
    if 'admin_logged_in' in session:
        return redirect('/admin')
    if 'logged_in' not in session:
        trigger_js_become_sponsor = request.args.get('trigger_js_become_sponsor', default=False, type=bool)
        if trigger_js_become_sponsor:
            return redirect('/signup_choose')
        # print(ongoing[0][1])
        # print('tata consultancy services'.title())
        # print('ASUSTeK Computer Inc.'.lower())
        return render_template('index.html', ongoing=ongoing, get_company_name=get_company_name, remove_time=remove_time, trending=trending, top=top, get_username=get_username)
    else:
        if session['login_type'] == 'Influencer' and session['username']:
            if_ban = login.query.filter_by(username=session['username']).first()
            if if_ban.warnings == 'Banned':
                inf_id = login.query.filter_by(username=session['username']).first().data_id
                inf = influencer.query.filter_by(inf_id=inf_id).first()
                return render_template('banned.html', inf=inf, username = session['username'])
            else:
                inf_id = login.query.filter_by(username=session['username']).first().data_id
                inf = influencer.query.filter_by(inf_id=inf_id).first()
                profile_pic = inf.profile_pic
                user_id = inf.inf_id
                login_type = session['login_type']
                return render_template('index_logged_in.html', ongoing=ongoing, get_company_name=get_company_name, username = session['username'], remove_time=remove_time, trending=trending, top=top, get_username=get_username, inf=inf, user_id=user_id, login_type=login_type, profile_pic=profile_pic)
        elif session['login_type'] == 'Sponsor' and session['username']:
            if_ban = login.query.filter_by(username=session['username']).first()
            if if_ban.warnings == 'Banned':
                return render_template('banned.html')
            else:
                sp_id  = login.query.filter_by(username=session['username']).first().data_id
                sp = companies.query.filter_by(company_id=sp_id).first()
                profle_pic = sp.logo
                user_id = sp.company_id
                login_type = session['login_type']
                print(session['username'])
                print(session['login_type'])
                return render_template('index_logged_in.html', ongoing=ongoing, get_company_name=get_company_name, username = session['username'], remove_time=remove_time, trending=trending, top=top, get_username=get_username, sp=sp, user_id=user_id, login_type=login_type, profile_pic=profle_pic)
        else:
            return render_template('demo.html', username = session['username'])


@app.route('/campaign/<int:campaign_id>')
def campaign_page(campaign_id):
    campaign = campaigns.query.filter_by(campaign_id=campaign_id).first()
    popular = all_ads_camp(campaign_id)
    company_data = companies.query.filter_by(company_id=campaign.company).first()
    campaign_company = login.query.filter_by(user_id=company_data.user_id).first()
    # print(campaign)
    if 'logged_in' in session:
        username=session['username']
        user_id = login.query.filter_by(username=username).first().data_id
        if session['login_type'] == 'Influencer':
            user = influencer.query.filter_by(inf_id=user_id).first()
            profile_pic = user.profile_pic
            return render_template('campaign_page.html', campaign_id=campaign_id, campaign=campaign, remove_time=remove_time, get_logo=get_logo, get_company_name=get_company_name, popular=popular, campaign_company=campaign_company, username=username, user=user, get_username=get_username, login_type=session['login_type'], profile_pic=profile_pic)
        else:
            user = companies.query.filter_by(company_id=user_id).first()
            profile_pic = user.logo
            recommended = []
            if user.company_id == campaign.company:
                camp_niches = campaign.niches.split(';')
                print(camp_niches)
                all_inf = influencer.query.order_by(influencer.est_reach.desc(), influencer.rating.desc()).all()
                for i in camp_niches:
                    for j in all_inf:
                        if i in j.niche.split(';'):
                            recommended.append(j)
                recommended = recommended[:7] if len(recommended) > 7 else recommended
            return render_template('campaign_page.html', campaign_id=campaign_id, campaign=campaign, remove_time=remove_time, get_logo=get_logo, get_company_name=get_company_name, popular=popular, campaign_company=campaign_company, username=username, user=user, recommended=recommended, get_username=get_username, login_type=session['login_type'], profile_pic=profile_pic)
    else:
        return render_template('campaign_page.html', campaign_id=campaign_id, campaign=campaign, remove_time=remove_time, get_logo=get_logo, get_company_name=get_company_name, popular=popular, campaign_company=campaign_company)

@app.route('/all_campaigns')
def all_campaigns():
    current_date = datetime.now().date()
    ongoing = campaigns.query.filter(campaigns.end_date > current_date, campaigns.warnings==None).all()
    ended = campaigns.query.filter(campaigns.end_date < current_date, campaigns.warnings==None).all()
    if 'logged_in' in session:
        username=session['username']
        user_id = login.query.filter_by(username=username).first().data_id
        if session['login_type'] == 'Sponsor':
            user = companies.query.filter_by(company_id=user_id).first()
            profile_pic = user.logo
        elif session['login_type'] == 'Influencer':
            user = influencer.query.filter_by(inf_id=user_id).first()
            profile_pic = user.profile_pic
        return render_template('all_campaigns.html', ongoing=ongoing, ended=ended, user=user, profile_pic=profile_pic, username=username, get_company_name=get_company_name, remove_time=remove_time, login_type=session['login_type'])
    else:
        return render_template('all_campaigns.html', ongoing=ongoing, ended=ended, get_company_name=get_company_name, remove_time=remove_time)
    
@app.route('/all_ads')
def all_ads():
    all_advert = ad_requests.query.all()
    if 'logged_in' in session:
        username=session['username']
        user_id = login.query.filter_by(username=username).first().data_id
        if session['login_type'] == 'Sponsor':
            user = companies.query.filter_by(company_id=user_id).first()
            profile_pic = user.logo
        elif session['login_type'] == 'Influencer':
            user = influencer.query.filter_by(inf_id=user_id).first()
            profile_pic = user.profile_pic
        return render_template('all_ads.html', all_advert=all_advert, session=session, user=user, username=username, profile_pic=profile_pic, get_username=get_username, login_type=session['login_type'])
    else:
        return render_template('all_ads.html', all_advert=all_advert, session=session, get_username=get_username)

@app.route('/all_influencers')
def all_influencers():
    if 'logged_in' in session:
        username=session['username']
        user_id = login.query.filter_by(username=username).first().data_id
        if session['login_type'] == 'Sponsor':
            user = companies.query.filter_by(company_id=user_id).first()
            profile_pic = user.logo
        elif session['login_type'] == 'Influencer':
            user = influencer.query.filter_by(inf_id=user_id).first()
            profile_pic = user.profile_pic
        return render_template('all_influencers.html', unique_niches=unique_niches, session=session, user=user, username=username, profile_pic=profile_pic, get_username=get_username, login_type=session['login_type'])
    else:
        return render_template('all_influencers.html', unique_niches=unique_niches, session=session, get_username=get_username)



@app.route('/niche/<niche>')
def niche_page(niche):
    niche = niche.title()
    all_influencers = influencer.query.filter(influencer.niche.like(f'%{niche}%')).all()
    if 'logged_in' in session:
        username=session['username']
        user_id = login.query.filter_by(username=username).first().data_id
        if session['login_type'] == 'Sponsor':
            user = companies.query.filter_by(company_id=user_id).first()
            profile_pic = user.logo
        elif session['login_type'] == 'Influencer':
            user = influencer.query.filter_by(inf_id=user_id).first()
            profile_pic = user.profile_pic
        return render_template('niche_page.html', niche=niche, user=user, username=username, profile_pic=profile_pic, all_influencers=all_influencers, get_username=get_username, login_type=session['login_type'])
    else:
        return render_template('niche_page.html', niche=niche, all_influencers=all_influencers, get_username=get_username)


@app.route('/influencer/<username>')
def influencer_page(username):
    inf_id = login.query.filter_by(username=username).first().data_id
    inf = influencer.query.filter_by(inf_id=inf_id).first()
    username = username.lower()
    all_niches = inf.niche.split(';')
    all_ad_ids = [contract.contract_id for contract in all_contracts.query.filter_by(inf_id=inf_id, status='Completed').order_by(all_contracts.date_completed.desc()).all()]
    completed = []
    for i in all_ad_ids:
        completed.append(ad_requests.query.filter_by(ad_id=i).first())
    all_date_completed = []
    for i in completed:
        all_date_completed.append(all_contracts.query.filter_by(contract_id=i.ad_id).first().date_completed)
    # print(completed)
    # print(all_date_completed)
    if 'logged_in' in session:
        username2=session['username']
        inf_id2 = login.query.filter_by(username=username2).first().data_id
        if session['login_type'] == 'Influencer':
            inf2 = influencer.query.filter_by(inf_id=inf_id2).first()
            profile_pic = inf2.profile_pic
        elif session['login_type'] == 'Sponsor':
            inf2 = companies.query.filter_by(company_id=inf_id2).first()
            profile_pic = inf2.logo
        return render_template('influencer_page.html', inf=inf, inf_id2=inf_id2, inf2=inf2, remove_time=remove_time, get_company_name=get_company_name, username=username, profile_pic=profile_pic, all_niches=all_niches, completed=completed, all_date_completed=all_date_completed, get_sp_ads=get_sp_ads, format_number=format_number, username2=username2, get_username=get_username, session=session, login_type=session['login_type'])
    else:
        return render_template('influencer_page.html', inf=inf, remove_time=remove_time, get_company_name=get_company_name, username=username, format_number=format_number, all_niches=all_niches, completed=completed, all_date_completed=all_date_completed)



@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    trigger_js = request.args.get('trigger_js', default=False, type=bool)
    if trigger_js:
        session.pop('logged_in', None)
        session.pop('username', None)
        session.pop('login_type', None)
        session.pop('user_created', None)
        session.pop('signup_type', None)
        session.pop('temp_username', None)
        session.pop('admin_logged_in', None)
        session.modified = True
    return render_template('login_page.html', trigger_js=trigger_js)

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    username = request.form.get('username')
    password = request.form.get('password')
    print(username)
    print(password)
    print(request.method)
    user = login.query.filter_by(username=username).first()
        
    if request.method=="POST":

        if username == 'sarthak265' and password == 'manu%40265!':
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            response = requests.get(f"http://127.0.0.1:5000/login/user?username={username}&password={password}")
            if response.status_code == 500:
                    return render_template('error_page.html', error_code=500, error_text="Internal Server Error")
            if response.status_code == 200:
                login_type = login.query.filter_by(username=username).first().acc_type
                session['logged_in'] = True
                session['username'] = username
                session['login_type'] = login_type
                return redirect('/')
            else:
                # print(response.status_code)
                error_message = response.json().get('error')
                return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    return render_template('error_page.html', error_code=400, error_text="Invalid request method")


@app.route('/logout')
def logout():
    trigger_js_become_sponsor = request.args.get('trigger_js_become_sponsor', default=False, type=bool)
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('login_type', None)
    session.pop('user_created', None)
    session.pop('signup_type', None)
    session.pop('temp_username', None)
    session.pop('top_niches', None)
    session.pop('admin_logged_in', None)
    session.modified = True
    if trigger_js_become_sponsor:
        return redirect('/?trigger_js_become_sponsor=True')
    return redirect('/')


@app.route('/influencer/<username>/personal/profile')
def inf_personal_page(username):
    if 'logged_in' in session and username == session['username'] and session['login_type'] == 'Influencer':
        if_flag = login.query.filter_by(username=username).first()
        inf_id = login.query.filter_by(username=username).first().data_id
        inf = influencer.query.filter_by(inf_id=inf_id).first()
        username = username.lower()
        current_date = datetime.now().strftime("%A, %d %B %Y")
        month = datetime.now().strftime("%B")
        all_inf_contracts = all_contracts.query.filter_by(inf_id=inf_id).all()
        monthly_earnings = {}
        for i in all_inf_contracts:
            if i.date_completed.strftime("%B") in monthly_earnings and monthly_earnings[i.date_completed.strftime("%B")] is not None:
                monthly_earnings[i.date_completed.strftime("%B")] += i.profit if i.profit is not None else 0
            else:
                monthly_earnings[i.date_completed.strftime("%B")] = i.profit
        
        # print(monthly_earnings)
        months_in_order = list(calendar.month_name)[1:]
        sorted_monthly_earnings = {month: monthly_earnings[month] for month in months_in_order if month in monthly_earnings}
        # print(sorted_monthly_earnings)
        months = list(sorted_monthly_earnings.keys())
        profit = list(sorted_monthly_earnings.values())
        
        earnings_current_month = round(monthly_earnings[month]) if month in monthly_earnings and monthly_earnings[month] is not None else 0

        total_earnings = round(sum([i for i in profit if i is not None]))

        # ad_ids = [contract.contract_id for contract in all_inf_contracts]
        # campaign_ids = [ad_requests.query.filter_by(ad_id=i).first().campaign_id for i in ad_ids]
        # company_ids = [campaigns.query.filter_by(campaign_id=i).first().company for i in campaign_ids]
        # company_freq_dic = {}
        # for i in company_ids:
        #     if i in company_freq_dic:
        #         company_freq_dic[i] += 1
        #     else:
        #         company_freq_dic[i] = 1
        # company_names = list(company_freq_dic.keys())
        # company_names = [companies.query.filter_by(company_id=i).first().name for i in company_names]
        # company_frequencies = list(company_freq_dic.values())
        # print(company_freq_dic)
        all_contracted = all_contracts.query.filter_by(inf_id=inf_id).order_by(all_contracts.status).all()
        ad_contract_page = [ad_requests.query.filter_by(ad_id=i.contract_id).first() for i in all_contracted]
        # print(ad_tasks_contract_page)
        inf_initiator = negotiations.query.filter_by(inf_id=inf_id, initiator='Influencer').all()
        sp_initiator = negotiations.query.filter_by(inf_id=inf_id, initiator='Sponsor').all()


        return render_template('inf_personal_profile_page.html', username=username, if_flag=if_flag, inf=inf, get_month_name=get_month_name, current_date=current_date, month=month, get_username=get_username, months=months, profit=profit, earnings_current_month=earnings_current_month, total_earnings=total_earnings, insert_commas=insert_commas, all_contracted=all_contracted, ad_contract_page=ad_contract_page, inf_initiator=inf_initiator, sp_initiator=sp_initiator, format_number=format_number, get_company_name=get_company_name, get_price=get_price, login_type=session['login_type'])
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")









@app.route('/influencer/<username>/personal/profile/edit', methods=['GET', 'POST'])
def inf_personal_profile_edit_page(username):
    if 'logged_in' in session and username == session['username']:
        inf_id = login.query.filter_by(username=username).first().data_id
        inf = influencer.query.filter_by(inf_id=inf_id).first()
        first_name = inf.name.split(' ')[0]
        last_name = " ".join(inf.name.split(' ')[1:])
        username = username.lower()
        return render_template('profile_edit_page.html', username=username, inf=inf, get_username=get_username, first_name=first_name, last_name=last_name, login_type=session['login_type'])
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")
    


@app.route('/influencer/<username>/profile/edit', methods=['GET', 'POST'])
def inf_profile_edit_puter(username):
    if 'logged_in' in session and username == session['username']:
        username = username.lower()
        if request.method=="POST":
            form_data = request.form
            print(form_data)
            response = requests.put(f"http://127.0.0.1:5000/influencer/profile/edit?username={username}", json=form_data)

            if response.status_code == 500:
                return render_template('error_page.html', error_code=500, error_text="Internal Server Error")

            if response.status_code == 200:
                if form_data['username'] != username:
                    return redirect(f'/logout')
                else:
                    return redirect(f'/influencer/{username}/personal/profile')
            else:
                # print(response.status_code)
                # print(response.json())
                error_message = response.json().get('error')
                return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")


@app.route('/influencer/<username>/password/edit', methods=['GET', 'POST'])
def password_edit_page(username):
    username = username.lower()
    if request.method == "POST":
        form_data = request.form
        print(form_data)
        response = requests.put(f"http://127.0.0.1:5000/influencer/user/edit?username={username}", json=form_data)
        if response.status_code == 500:
            return render_template('error_page.html', error_code=500, error_text="Internal Server Error")
        if response.status_code == 200:
            return redirect(f'/logout')
        else:
            error_message = response.json().get('error')
            return render_template('error_page.html', error_code=response.status_code, error_text=error_message)


@app.route('/influencer/signup/choose', methods=['GET', 'POST'])
def influencer_signup_choose():
    if request.method == "POST":
        session['signup_type'] = 'Influencer'
    return redirect('/signup_page')


@app.route('/sponsor/signup/choose', methods=['GET', 'POST'])
def sponsor_signup_choose():
    if request.method == "POST":
        session['signup_type'] = 'Sponsor'
    return redirect('/signup_page')
    

@app.route('/signup_choose')
def signup_choose():
    if 'user_created' in session:
        if session['user_created'] != True:
            session.pop('signup_type', None)
            session.modified = True
            return render_template('signup_choose.html')
    else:
        return render_template('signup_choose.html')


@app.route('/signup_page')
def signup_page():
    return render_template('signup_page.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    data = request.form
    signup_type = session['signup_type']

    response = requests.post(f"http://127.0.0.1:5000/signup/user?signup_type={signup_type}", json=data)

    if response.status_code == 500:
        return render_template('error_page.html', error_code=500, error_text="Internal Server Error")

    if response.status_code == 200:
        session['user_created'] = True
        if signup_type == 'Influencer':
            return redirect(f'/inf_profile_creator/{data["username"]}')
        else:
            return redirect(f'/sponsor_profile_creator/{data["username"]}')
    else:
        error_message = response.json().get('error')
        return render_template('error_page.html', error_code=response.status_code, error_text=error_message)


@app.route('/inf_profile_creator/<username>', methods=['GET', 'POST'])
def influencer_profile_creator(username):
    return render_template('influencer_profile_creator.html', username=username, unique_niches=unique_niches)

@app.route('/sponsor_profile_creator/<username>', methods=['GET', 'POST'])
def sponsor_profile_creator(username):
    return render_template('sponsor_profile_creator.html', username=username)


@app.route('/influencer/<username>/new_profile', methods=['GET', 'POST'])
def influencer_new_profile_submit(username):
    data = request.form
    niches = request.form.getlist('niches[]')
    profile_pic_url = request.form.get('hidden_image_url')
    if not profile_pic_url:
        profile_pic_url = 'https://img.freepik.com/premium-vector/user-profile-icon-flat-style-member-avatar-vector-illustration-isolated-background-human-permission-sign-business-concept_157943-15752.jpg'

    data_to_send = []
    data_to_send.append(data)
    data_to_send.append(niches)
    data_to_send.append(profile_pic_url)
    print(profile_pic_url)
    print(data_to_send)
    
    response = requests.post(f"http://127.0.0.1:5000/influencer/new_profile?username={username}", json=data_to_send)

    if response.status_code == 500:
        return render_template('error_page.html', error_code=500, error_text="Internal Server Error")

    if response.status_code == 200:
        return redirect(url_for('login_page', trigger_js=True))
    else:
        error_message = response.json().get('error')
        return render_template('error_page.html', error_code=response.status_code, error_text=error_message)

@app.route('/sponsor/<username>/new_profile', methods=['GET', 'POST'])
def sponsor_new_profile_submit(username):
    data = request.form
    profile_pic_url = request.form.get('hidden_image_url')
    if not profile_pic_url:
        profile_pic_url = "https://img.freepik.com/premium-vector/user-profile-icon-flat-style-member-avatar-vector-illustration-isolated-background-human-permission-sign-business-concept_157943-15752.jpg"

    data_to_send = []
    data_to_send.append(data)
    data_to_send.append(profile_pic_url)

    response = requests.post(f"http://127.0.0.1:5000/sponsor/new_profile?username={username}", json=data_to_send)

    if response.status_code == 500:
        return render_template('error_page.html', error_code=500, error_text="Internal Server Error")

    if response.status_code == 200:
        return redirect(url_for('login_page', trigger_js=True))
    
    else:
        error_message = response.json().get('error')
        return render_template('error_page.html', error_code=response.status_code, error_text=error_message)


@app.route('/influencer/<username>/upload/profile_pic', methods=['GET', 'POST'])
def image_upload(username):

    if request.method == "POST":
        data = request.form
        response = requests.put(f'http://127.0.0.1:5000/img_upload?username={username}', json=data)

        if response.status_code == 500:
            return render_template('error_page.html', error_code=500, error_text="Internal Server Error")

        if response.status_code == 200:
            return redirect(f'/influencer/{username}/personal/profile')
        else:
            error_message = response.json().get('error')
            return render_template('error_page.html', error_code=response.status_code, error_text=error_message)




@app.route('/sponsor/<username>')
def sponsor_page(username):
    sp_id  = login.query.filter_by(username=username).first().data_id
    sp = companies.query.filter_by(company_id=sp_id).first()
    launched_campaigns = campaigns.query.filter_by(company=sp_id).all()
    if 'logged_in' in session:
        user_id = login.query.filter_by(username=session['username']).first().data_id
        login_type = session['login_type']
        if login_type == 'Sponsor':
            user = companies.query.filter_by(company_id=user_id).first()
            profile_pic = user.logo
        elif login_type == 'Influencer':
            print(session['login_type'])
            user = influencer.query.filter_by(inf_id=user_id).first()
            profile_pic = user.profile_pic

        return render_template('sponsor_page.html', username=username, username2=session['username'], sp=sp, launched_campaigns=launched_campaigns, user=user, profile_pic=profile_pic, remove_time=remove_time, session=session, login_type=login_type, format_title=format_title)
    else:
        return render_template('sponsor_page.html', username=username, sp=sp, launched_campaigns=launched_campaigns, remove_time=remove_time, format_title=format_title)

@app.route('/sponsor/<username>/personal/profile')
def sponsor_personal_page(username):
    if 'logged_in' in session and username == session['username'] and session['login_type'] == 'Sponsor':
        if_flag = login.query.filter_by(username=username).first()
        sp_id  = login.query.filter_by(username=session['username']).first().data_id
        sp = companies.query.filter_by(company_id=sp_id).first()
        login_type = session['login_type']
        current_date = datetime.now().strftime("%A, %d %B %Y")
        all_campaigns = campaigns.query.filter_by(company=sp_id).all()
        all_spendings = [camp.spending for camp in campaigns.query.filter_by(company=sp_id).all()]
        month = datetime.now().strftime("%B")
        total_spendings = sum(all_spendings)
        all_ad_ids = []
        for i in all_campaigns:
            all_ad_ids.extend([i.ad_id for i in ad_requests.query.filter_by(campaign_id=i.campaign_id).all()])
        all_ad_ids = list(set(all_ad_ids))
        all_sp_contracts = []
        for i in all_ad_ids:
            all_sp_contracts.extend(all_contracts.query.filter_by(contract_id=i).all())
        monthly_profit = {}
        for i in all_sp_contracts:
            if i.date_completed.strftime("%B") in monthly_profit and monthly_profit[i.date_completed.strftime("%B")] is not None:
                monthly_profit[i.date_completed.strftime("%B")] += i.company_profit if i.company_profit is not None else 0
            else:
                monthly_profit[i.date_completed.strftime("%B")] = i.company_profit
        months_in_order = list(calendar.month_name)[1:]
        sorted_monthly_profit = {month: monthly_profit[month] for month in months_in_order if month in monthly_profit}
        # print(sorted_monthly_earnings)
        months = list(sorted_monthly_profit.keys())
        profit = list(sorted_monthly_profit.values())

        profit_current_month = round(monthly_profit[month]) if month in monthly_profit and monthly_profit[month] is not None else 0

        total_profit = round(sum([i for i in profit if i is not None]))

        no_of_completions = len(all_sp_contracts)
        def format_number(num):
            if num >= 1000 and num < 1000000:
                return f"{num / 1000:.2f}K"
            elif num >= 1000000:
                return f"{num / 1000000:.2f}M"
            else:
                return num
    
            
        
        sp_initiator = negotiations.query.filter_by(company_id=sp_id, initiator='Sponsor').all()
        inf_initiator = negotiations.query.filter_by(company_id=sp_id, initiator='Influencer').all()
        

        return render_template('sponsor_personal_profile_page.html', username=username, if_flag=if_flag, get_username=get_username, login_type=login_type, sp=sp, format_title=format_title, current_date=current_date, all_campaigns=all_campaigns, insert_commas=insert_commas, sp_initiator=sp_initiator, inf_initiator=inf_initiator, total_spendings=total_spendings, month=month, total_profit=total_profit, profit_current_month=profit_current_month, months=months, profit=profit, format_number=format_number, no_of_completions=no_of_completions, get_price=get_price, get_company_name=get_company_name, get_inf=get_inf)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")






@app.route('/sponsor/<username>/personal/profile/edit', methods=['GET', 'POST'])
def sponsor_personal_profile_edit_page(username):
    if 'logged_in' in session and username == session['username']:
        sp_id = login.query.filter_by(username=username).first().data_id
        sp = companies.query.filter_by(company_id=sp_id).first()
        username = username.lower()
        return render_template('sp_profile_edit_page.html', username=username, sp=sp, get_username=get_username, format_title=format_title, login_type=session['login_type'])
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")
    


@app.route('/sponsor/<username>/profile/edit', methods=['GET', 'POST'])
def sponsor_profile_edit_puter(username):
    if 'logged_in' in session and username == session['username']:
        username = username.lower()
        if request.method=="POST":
            form_data = request.form
            print(form_data)
            response = requests.put(f"http://127.0.0.1:5000/sponsor/profile/edit?username={username}", json=form_data)

            if response.status_code == 500:
                return render_template('error_page.html', error_code=500, error_text="Internal Server Error")

            if response.status_code == 200:
                if form_data['username'] != username:
                    return redirect(f'/logout')
                else:
                    return redirect(f'/sponsor/{username}/personal/profile')
            else:
                # print(response.status_code)
                # print(response.json())
                error_message = response.json().get('error')
                return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")


@app.route('/sponsor/<username>/password/edit', methods=['GET', 'POST'])
def sponsor_password_edit_page(username):
    username = username.lower()
    if request.method == "POST":
        form_data = request.form
        print(form_data)
        response = requests.put(f"http://127.0.0.1:5000/user/password/edit?username={username}", json=form_data)
        if response.status_code == 500:
            return render_template('error_page.html', error_code=500, error_text="Internal Server Error")
        if response.status_code == 200:
            return redirect(f'/logout')
        else:
            error_message = response.json().get('error')
            return render_template('error_page.html', error_code=response.status_code, error_text=error_message)


@app.route('/sponsor/<username>/create_campaign')
def create_campaign_page(username):
    sp_id = login.query.filter_by(username=username).first().data_id
    sp = companies.query.filter_by(company_id=sp_id).first()
    login_type = session['login_type']
    return render_template('create_campaign_page.html', username=username, login_type=login_type, sp=sp)




@app.route('/sponsor/<username>/campaign/create', methods=['GET', 'POST'])
def create_campaign(username):
    if 'logged_in' in session and session['login_type'] == 'Sponsor':
        if request.method == 'POST':
            data = request.form

            
            response = requests.post(f'http://127.0.0.1:5000/sponsor/campaign/new?username={username}', json=data)

            if response.status_code == 500:
                return render_template('error_page.html', error_code=500, error_text="Internal Server Error")

            if response.status_code == 200:
                return redirect(f'/sponsor/{username}/personal/profile')
            else:
                error_message = response.json().get('error')
                return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
            
@app.route('/sponsor/<username>/campaign_edit_page/<int:campaign_id>')
def campaign_edit_page(username, campaign_id):
    if 'logged_in' in session and session['login_type'] == 'Sponsor' and session['username'] == username:
        sp_id = login.query.filter_by(username=username).first().data_id
        sp = companies.query.filter_by(company_id=sp_id).first()
        username = username.lower()
        campaign = campaigns.query.filter_by(campaign_id=campaign_id).first()
        return render_template('campaign_edit_page.html', username=username, campaign_id=campaign_id, campaign=campaign, sp=sp, get_username=get_username, format_title=format_title, login_type=session['login_type'])
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")

@app.route('/sponsor/<username>/campaign/edit/<int:campaign_id>', methods=['GET', 'POST'])
def campaign_edit(username, campaign_id):
    if 'logged_in' in session and session['login_type'] == 'Sponsor' and session['username'] == username:
        if request.method == 'POST':
            data = request.form
            response = requests.put(f'http://127.0.0.1:5000/sponsor/campaign/edit?username={username}&campaign_id={campaign_id}', json=data)

            if response.status_code == 500:
                return render_template('error_page.html', error_code=500, error_text="Internal Server Error")

            if response.status_code == 200:
                return redirect(f'/sponsor/{username}/personal/profile')
            else:
                error_message = response.json().get('error')
                return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")


@app.route('/sponsor/<username>/campaign/<int:campaign_id>/delete')
def campaign_delete(username, campaign_id):
    if 'logged_in' in session and session['login_type'] == 'Sponsor' and session['username'] == username:
        response = requests.delete(f'http://127.0.0.1:5000/sponsor/campaign/delete?username={username}&campaign_id={campaign_id}')
        if response.status_code == 500:
            return render_template('error_page.html', error_code=500, error_text="Internal Server Error")

        if response.status_code == 200:
            return redirect(f'/sponsor/{session["username"]}/personal/profile')
        else:
            error_message = response.json().get('error')
            return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")
    


@app.route('/all_sponsors')
def all_sponsors():
    all_sp = companies.query.all()
    if 'logged_in' in session:
        username=session['username']
        user_id = login.query.filter_by(username=username).first().data_id
        if session['login_type'] == 'Sponsor':
            user = companies.query.filter_by(company_id=user_id).first()
            profile_pic = user.logo
        elif session['login_type'] == 'Influencer':
            user = influencer.query.filter_by(inf_id=user_id).first()
            profile_pic = user.profile_pic
        return render_template('all_sponsors.html', user=user, profile_pic=profile_pic, username=username, all_sp=all_sp, get_username=get_username, format_title=format_title, login_type=session['login_type'])
    else:
        return render_template('all_sponsors.html', all_sp=all_sp, get_username=get_username, format_title=format_title)


@app.route('/ad/<int:ad_id>', methods=['GET', 'POST'])
def ad_request_page(ad_id):
    trigger_js = request.args.get('trigger_js', default=False, type=bool)
    trigger_js2 = request.args.get('trigger_js2', default=False, type=bool)
    ad = ad_requests.query.filter_by(ad_id=ad_id).first()
    campaign_id = ad.campaign_id
    campaign = campaigns.query.filter_by(campaign_id=campaign_id).first()
    ad_sponsor = login.query.filter_by(data_id=campaign.company).first()
    all_requirements = ad.requirements.split(';')
    all_inf = influencer.query.order_by(influencer.est_reach.desc(), influencer.rating.desc()).all()
    if 'logged_in' in session:
        username=session['username']
        user_id = login.query.filter_by(username=username).first().data_id
        login_type = session['login_type']
        if session['login_type'] == 'Sponsor':
            user = companies.query.filter_by(company_id=user_id).first()
            profile_pic = user.logo
            camp_niches = campaign.niches.split(';')
            recommended = []
            for i in camp_niches:
                for j in all_inf:
                    if i in j.niche.split(';'):
                        recommended.append(j)
            recommended = recommended[:7] if len(recommended) > 7 else recommended
            return render_template('ad_request_page.html', ad_id=ad_id, ad=ad, campaign=campaign, ad_sponsor=ad_sponsor, user_id=user_id, campaign_id=campaign_id, session=session,  login_type=login_type, all_requirements=all_requirements, username=username, user=user, recommended=recommended, profile_pic=profile_pic, remove_time=remove_time, get_logo=get_logo, get_company_name=get_company_name, trigger_js=trigger_js, trigger_js2=trigger_js2, get_username=get_username, format_title=format_title)
        else:
            user = influencer.query.filter_by(inf_id=user_id).first()
            first_time = negotiations.query.filter_by(ad_id=ad_id, inf_id=user.inf_id).first()
            contracts = all_contracts.query.all()
            contract_exist = all_contracts.query.filter_by(contract_id=ad_id, inf_id=user.inf_id).first()
            contract_index = contracts.index(contract_exist) + 1 if contract_exist else None
            print(contract_exist)
            all_negot = negotiations.query.all()
            negot_true = negotiations.query.filter_by(ad_id=ad_id, inf_id=user.inf_id).first()
            print(negot_true)
            negot_index = all_negot.index(negot_true) + 1 if negot_true else None
            print(negot_index)
            profile_pic = user.profile_pic
        return render_template('ad_request_page.html', ad_id=ad_id, ad=ad, campaign=campaign, ad_sponsor=ad_sponsor, first_time=first_time, contract_exist=contract_exist, contract_index=contract_index, campaign_id=campaign_id, session=session,  login_type=login_type, all_requirements=all_requirements, username=username, user=user, profile_pic=profile_pic, remove_time=remove_time, get_logo=get_logo, get_company_name=get_company_name, trigger_js=trigger_js, trigger_js2=trigger_js2, negot_true=negot_true, negot_index=negot_index, format_title=format_title)
    
    return render_template('ad_request_page.html', ad_id=ad_id, ad=ad, campaign=campaign, ad_sponsor=ad_sponsor, campaign_id=campaign_id, session=session, all_requirements=all_requirements, remove_time=remove_time, get_logo=get_logo, get_company_name=get_company_name, format_title=format_title, trigger_js=trigger_js, trigger_js2=trigger_js2)

@app.route('/ad/<int:ad_id>/neg/<int:inf_id>', methods=['GET', 'POST'])
def inf_negotiate(ad_id, inf_id):
    if request.method == 'POST':    
        data = request.form
        response = requests.post(f'http://127.0.0.1:5000/ad/negotiate?ad_id={ad_id}&inf_id={inf_id}', json=data)
        if response.status_code == 200:
            return redirect(url_for('ad_request_page',ad_id=ad_id, trigger_js=True))
        else:
            error_message = response.json().get('error')
            return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    else:
        return render_template('error_page.html', error_code=405, error_text="Method Not Allowed")
    
@app.route('/sponsor/ad/<int:ad_id>/neg/<int:inf_id>', methods=['GET', 'POST'])
def sp_negotiate(ad_id, inf_id):
    if request.method == 'POST':    
        data = request.form
        response = requests.post(f'http://127.0.0.1:5000/sponsor/ad/negotiate?ad_id={ad_id}&inf_id={inf_id}', json=data)
        if response.status_code == 200:
            return redirect(url_for('ad_request_page',ad_id=ad_id, trigger_js=True))
        else:
            error_message = response.json().get('error')
            return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    else:
        return render_template('error_page.html', error_code=405, error_text="Method Not Allowed")

@app.route('/ad/<int:ad_id>/accept/<int:inf_id>', methods=['GET', 'POST'])
def inf_accept(ad_id, inf_id):
    response = requests.post(f'http://127.0.0.1:5000/ad/accept?ad_id={ad_id}&inf_id={inf_id}')
    if response.status_code == 200:
        return redirect(url_for('ad_request_page',ad_id=ad_id, trigger_js2=True))
    else:
        error_message = response.json().get('error')
        return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    
@app.route('/ad/<int:ad_id>/cancel/<int:inf_id>', methods=['GET', 'POST'])
def inf_cancel(ad_id, inf_id):
    inf = login.query.filter_by(data_id=inf_id).first()
    response = requests.delete(f'http://127.0.0.1:5000/ad/negotiate/delete?ad_id={ad_id}&inf_id={inf_id}')
    if response.status_code == 200:
        return redirect(f'/influencer/{inf.username}/personal/profile')
    else:
        error_message = response.json().get('error')
        return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    
@app.route('/sponsor/ad/<int:ad_id>/cancel/<int:inf_id>', methods=['GET', 'POST'])
def sp_cancel(ad_id, inf_id):
    inf = login.query.filter_by(data_id=inf_id).first()
    response = requests.delete(f'http://127.0.0.1:5000/ad/negotiate/delete?ad_id={ad_id}&inf_id={inf_id}')
    if response.status_code == 200:
        return redirect(f'/sponsor/{session["username"]}/personal/profile')
    else:
        error_message = response.json().get('error')
        return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    

@app.route('/influencer/<username>/contract/<int:contract_id>/complete', methods=['GET', 'POST'])
def contract_complete(username, contract_id):
    if 'logged_in' in session and session['login_type'] == 'Influencer' and session['username'] == username:
        response = requests.put(f'http://127.0.0.1:5000/influencer/contract/complete?username={username}&contract_id={contract_id}')
        if response.status_code == 200:
            return redirect(f'/influencer/{username}/personal/profile')
        else:
            error_message = response.json().get('error')
            return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")


@app.route('/influencer/<username>/contract/<int:contract_id>/reject', methods=['GET', 'POST'])
def contract_reject(username, contract_id):
    if 'logged_in' in session and session['username'] == username:
        response = requests.post(f'http://127.0.0.1:5000/influencer/contract/reject?username={username}&contract_id={contract_id}')
        if response.status_code == 200:
            return redirect(f'/ad/{contract_id}')
        else:
            error_message = response.json().get('error')
            return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")
    
@app.route('/sponsor/<username>/campaign/<int:campaign_id>/create_ad')
def create_ad_request_page(username, campaign_id):
    sp_id = login.query.filter_by(username=username).first().data_id
    sp = companies.query.filter_by(company_id=sp_id).first()
    login_type = session['login_type']
    return render_template('create_ad_request_page.html', username=username, campaign_id=campaign_id, login_type=login_type, sp=sp)

@app.route('/sponsor/<username>/campaign/<int:campaign_id>/ad/create', methods=['GET', 'POST'])
def create_ad_request(username, campaign_id):
    if 'logged_in' in session and session['login_type'] == 'Sponsor' and session['username'] == username:
        if request.method == 'POST':
            data = request.form
            response = requests.post(f'http://127.0.0.1:5000/sponsor/ad_request/new?username={username}&campaign_id={campaign_id}', json=data)
            if response.status_code == 200:
                return redirect(f'/campaign/{campaign_id}')
            else:
                error_message = response.json().get('error')
                return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
        else:
            return render_template('error_page.html', error_code=405, error_text="Method Not Allowed")
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")


@app.route('/sponsor/<username>/ad_request_edit_page/<int:ad_id>')
def ad_request_edit_page(username, ad_id):
    if 'logged_in' in session and session['login_type'] == 'Sponsor' and session['username'] == username:
        sp_id = login.query.filter_by(username=username).first().data_id
        sp = companies.query.filter_by(company_id=sp_id).first()
        username = username.lower()
        ad = ad_requests.query.filter_by(ad_id=ad_id).first()
        return render_template('ad_request_edit_page.html', username=username, ad_id=ad_id, ad=ad, sp=sp, get_username=get_username, format_title=format_title, login_type=session['login_type'])
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")
    
@app.route('/sponsor/<username>/ad_request/edit/<int:ad_id>', methods=['GET', 'POST'])
def ad_request_edit(username, ad_id):
    if 'logged_in' in session and session['login_type'] == 'Sponsor' and session['username'] == username:
        if request.method == 'POST':
            data = request.form
            response = requests.put(f'http://127.0.0.1:5000/sponsor/ad_request/edit?username={username}&ad_id={ad_id}', json=data)

            if response.status_code == 500:
                return render_template('error_page.html', error_code=500, error_text="Internal Server Error")

            if response.status_code == 200:
                return redirect(f'/ad/{ad_id}')
            else:
                error_message = response.json().get('error')
                return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")

@app.route('/sponsor/<username>/ad_request/delete/<int:ad_id>', methods=['GET', 'POST'])
def ad_request_delete(username, ad_id):
    if 'logged_in' in session and session['login_type'] == 'Sponsor' and session['username'] == username:
        ad_camp_id = ad_requests.query.filter_by(ad_id=ad_id).first().campaign_id
        response = requests.delete(f'http://127.0.0.1:5000/sponsor/ad_request/delete?username={username}&ad_id={ad_id}')
        if response.status_code == 200:
            return redirect(f'/campaign/{ad_camp_id}')
        else:
            error_message = response.json().get('error')
            return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")
    

@app.route('/admin')
def admin_page():
    if 'admin_logged_in' in session:

        thirty_days_ago = datetime.now() - timedelta(days=30)
        all_users = login.query.all()
        all_dates = []
        for i in all_users:
            if datetime.strptime(i.last_logged_in, '%d/%m/%y') >= thirty_days_ago and datetime.strptime(i.last_logged_in, '%d/%m/%y') <= datetime.now():
                all_dates.append(i.last_logged_in)
        print(len(all_dates))
        no_of_inf = len(login.query.filter_by(acc_type='Influencer').all())
        no_of_sponsors = len(login.query.filter_by(acc_type='Sponsor').all())
        ongoing = campaigns.query.filter(campaigns.end_date > datetime.now().date()).all()
        ended = campaigns.query.filter(campaigns.end_date < datetime.now().date()).all()
        campaign_duration = []
        for i in campaigns.query.all():
            campaign_duration.append(i.end_date - i.start_date)
        avg_campaign_duration = sum(campaign_duration, timedelta()) / len(campaign_duration)
        avg_campaign_duration = avg_campaign_duration.days
        comp_contracts = all_contracts.query.filter_by(status='Completed').all()
        comp_this_month = []
        for i in comp_contracts:
            if i.date_completed.strftime("%B") == datetime.now().strftime("%B"):
                comp_this_month.append(i)
        contract_value = []
        sp_profit = []
        for i in all_contracts.query.all():
            contract_value.append(i.profit if i.profit is not None else 0)
            sp_profit.append(i.company_profit if i.company_profit is not None else 0)
        avg_contract_value = round(sum(contract_value) / len(contract_value), 1)
        avg_sp_profit = round(sum(sp_profit) / len(sp_profit), 1)
        all_ads = ad_requests.query.all()
        ad_niches = {}
        for i in all_ads:
            ad_campaign = campaigns.query.filter_by(campaign_id=i.campaign_id).first()
            if ad_campaign.niches not in ad_niches:
                ad_niches[ad_campaign.niches] = i.number_of_completions if i.number_of_completions is not None else 0
            else:
                ad_niches[ad_campaign.niches] += i.number_of_completions if i.number_of_completions is not None else 0
        all_ad_niches = {}
        for i in ad_niches:
            for j in i.split(';'):
                if j not in all_ad_niches:
                    all_ad_niches[j] = ad_niches[i] if ad_niches[i] is not None else 0
                else:
                    all_ad_niches[j] += ad_niches[i] if ad_niches[i] is not None else 0
        print(all_ad_niches)
        print(sum(all_ad_niches.values()))
        if 'top_niches' in session:
            top_niches = session['top_niches']
        else:
            top_niches = sorted(all_ad_niches.items(), key=lambda x: x[1], reverse=True)
            top_niches = top_niches[:10]
            random.shuffle(top_niches)
            session['top_niches'] = top_niches
        dash_niches = []
        dash_no_completions = []
        for i, j in enumerate(top_niches):
            dash_niches.append(j[0])
            dash_no_completions.append(j[1])
        print(dash_niches)
        print(dash_no_completions)
        # dash_niches = list(all_ad_niches.keys())
        # dash_no_completions = list(all_ad_niches.values())
        
        return render_template('admin_page.html', active_users=len(all_dates), no_of_users=len(all_users), no_of_inf=no_of_inf, no_of_sponsors=no_of_sponsors, ongoing_campaigns=len(ongoing), ended_campaigns=len(ended), avg_campaign_duration=avg_campaign_duration, fulfilled_contracts=len(comp_contracts), fulfilled_this_month=len(comp_this_month), avg_contract_value=avg_contract_value, avg_sp_profit=avg_sp_profit, insert_commas=insert_commas, dash_niches=dash_niches, dash_no_completions=dash_no_completions)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")

@app.route('/admin/users')
def admin_users_page():
    if 'admin_logged_in' in session:
        flagged_inf = [i[0] for i in [influencer.query.filter_by(inf_id=i.data_id).all() for i in login.query.filter_by(acc_type='Influencer', warnings='Flagged').all()]]
        banned_inf = [i[0] for i in [influencer.query.filter_by(inf_id=i.data_id).all() for i in login.query.filter_by(acc_type='Influencer', warnings='Banned').all()]]
        flagged_sp = [i[0] for i in [companies.query.filter_by(company_id=i.data_id).all() for i in login.query.filter_by(acc_type='Sponsor', warnings='Flagged').all()]]
        banned_sp = [i[0] for i in [companies.query.filter_by(company_id=i.data_id).all() for i in login.query.filter_by(acc_type='Sponsor', warnings='Banned').all()]]

        
        
        if 'search' in request.args:
            search = request.args.get('search').lower()
            print(search)
            query = (
                influencer.query
                .join(login, influencer.inf_id == login.data_id)
                .filter(login.acc_type == 'Influencer')
            )
            query = query.filter(or_(
                influencer.name.ilike(f'%{search}%'),
                login.username.ilike(f'%{search}%')
            ))
            all_inf = query.all()
        else:
            all_inf = [i[0] for i in [influencer.query.filter_by(inf_id=i.data_id).all() for i in login.query.filter_by(acc_type='Influencer', warnings=None).limit(10).all()]]
        
        
        if 'search_sp' in request.args:
            search_sp = request.args.get('search_sp').lower()
            print(search_sp)
            query = (
                companies.query
                .join(login, companies.company_id == login.data_id)
                .filter(login.acc_type == 'Sponsor')
            )
            query = query.filter(or_(
                companies.name.ilike(f'%{search_sp}%'),
                login.username.ilike(f'%{search_sp}%')
            ))
            all_sp = query.all()
        else:
            all_sp = [i[0] for i in [companies.query.filter_by(company_id=i.data_id).all() for i in login.query.filter_by(acc_type='Sponsor', warnings=None).limit(10).all()]]

        
        print(flagged_inf)
        return render_template('admin_users_page.html', all_inf=all_inf, all_sp=all_sp, get_username=get_username, get_sp_username=get_sp_username, flagged_inf=flagged_inf, banned_inf=banned_inf, flagged_sp=flagged_sp, banned_sp=banned_sp, format_title=format_title)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")


@app.route('/admin/user/<username>/flag', methods=['GET', 'POST'])
def admin_flag_user(username):
    if 'admin_logged_in' in session:
        if request.method == 'POST':
            data = {
                'todo': 'flag',
            }
            response = requests.put(f'http://127.0.0.1:5000/admin/user/flag?username={username}', json=data)
            if response.status_code == 200:
                return redirect('/admin/users')
            else:
                error_message = response.json().get('error')
                return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
        else:
            return render_template('error_page.html', error_code=405, error_text="Method Not Allowed")
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")
    
@app.route('/admin/user/<username>/unflag', methods=['GET', 'POST'])
def admin_unflag_user(username):
    if 'admin_logged_in' in session:
        if request.method == 'POST':
            data = {
                'todo': 'unflag',
            }
            response = requests.put(f'http://127.0.0.1:5000/admin/user/flag?username={username}', json=data)
            if response.status_code == 200:
                return redirect('/admin/users')
            else:
                error_message = response.json().get('error')
                return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
        else:
            return render_template('error_page.html', error_code=405, error_text="Method Not Allowed")
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")

@app.route('/admin/user/<username>/ban', methods=['GET', 'POST'])
def admin_ban_user(username):
    if 'admin_logged_in' in session:
        data = {
            'todo': 'ban',
        }
        if request.method == 'POST':
            response = requests.put(f'http://127.0.0.1:5000/admin/user/ban?username={username}', json=data)
            if response.status_code == 200:
                return redirect('/admin/users')
            else:
                error_message = response.json().get('error')
                return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
        else:
            return render_template('error_page.html', error_code=405, error_text="Method Not Allowed")
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")
    
@app.route('/admin/user/<username>/unban', methods=['GET', 'POST'])
def admin_unban_user(username):
    if 'admin_logged_in' in session:
        data = {
            'todo': 'unban',
        }
        if request.method == 'POST':
            response = requests.put(f'http://127.0.0.1:5000/admin/user/ban?username={username}', json=data)
            if response.status_code == 200:
                return redirect('/admin/users')
            else:
                error_message = response.json().get('error')
                return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
        else:
            return render_template('error_page.html', error_code=405, error_text="Method Not Allowed")
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")


@app.route('/admin/search/inf', methods=['GET', 'POST'])
def admin_search_influencers():
    search = request.args.get('search').lower()
    return redirect(url_for('admin_users_page', search=search))

@app.route('/admin/search/sp', methods=['GET', 'POST'])
def admin_search_sponsors():
    search_sp = request.args.get('search').lower()
    return redirect(url_for('admin_users_page', search_sp=search_sp))


@app.route('/admin/all_campaigns')
def admin_all_campaigns():
    if 'admin_logged_in' in session:
        current_date = datetime.now().date()
        flagged = campaigns.query.filter_by(warnings='Flagged').all()
        ongoing = campaigns.query.filter(campaigns.end_date > current_date, campaigns.warnings == None).all()
        ended = campaigns.query.filter(campaigns.end_date < current_date).all()
        return render_template('admin_all_campaigns.html', ongoing=ongoing, ended=ended, flagged=flagged, get_company_name=get_company_name, remove_time=remove_time)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")


@app.route('/admin/campaign/<int:campaign_id>/flag', methods=['GET', 'POST'])
def admin_flag_campaign(campaign_id):
    if 'admin_logged_in' in session:
        data = {
            'todo': 'flag',
        }
        response = requests.put(f'http://127.0.0.1:5000/admin/campaign/flag?campaign_id={campaign_id}', json=data)
        if response.status_code == 200:
            return redirect('/admin/all_campaigns')
        else:
            error_message = response.json().get('error')
            return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")

@app.route('/admin/campaign/<int:campaign_id>/unflag', methods=['GET', 'POST'])
def admin_unflag_campaign(campaign_id):
    if 'admin_logged_in' in session:
        data = {
            'todo': 'unflag',
        }
        response = requests.put(f'http://127.0.0.1:5000/admin/campaign/flag?campaign_id={campaign_id}', json=data)
        if response.status_code == 200:
            return redirect('/admin/all_campaigns')
        else:
            error_message = response.json().get('error')
            return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")

@app.route('/admin/campaign/<int:campaign_id>/remove', methods=['GET', 'POST'])
def admin_remove_campaign(campaign_id):
    if 'admin_logged_in' in session:
        data = {
            'todo': 'remove',
        }
        response = requests.delete(f'http://127.0.0.1:5000/admin/campaign/flag?campaign_id={campaign_id}', json=data)
        if response.status_code == 200:
            return redirect('/admin/all_campaigns')
        else:
            error_message = response.json().get('error')
            return render_template('error_page.html', error_code=response.status_code, error_text=error_message)
    else:
        return render_template('error_page.html', error_code=403, error_text="Access Denied")



@app.route('/search_handler', methods=['GET', 'POST'])
def search_handler():
    search = request.args.get('search').lower()
    return redirect(url_for('search_results', search=search))
    

@app.route('/search')
def search_results():
    if 'search' in request.args:
        search = request.args.get('search')
        search_val = 0
        range_val = 0
        try:
            search_val = int(search)
            if search_val >= 1000000:
                range_val = 100000
            else:
                range_val = 500
        except:
            search = request.args.get('search').lower()
        query = (
            influencer.query
            .join(login, influencer.inf_id == login.data_id)
            .filter(login.acc_type == 'Influencer')
            )
        query = query.filter(or_(
            influencer.name.ilike(f'%{search}%'),
            influencer.niche.ilike(f'%{search}%'),
            and_(
            influencer.no_of_followers >= search_val - range_val,
            influencer.no_of_followers <= search_val + range_val
            ),
            login.username.ilike(f'%{search}%')
            ))
        search_inf = query.all()

        query = (
            companies.query
            .join(login, companies.company_id == login.data_id)
            .filter(login.acc_type == 'Sponsor')
            )
        query = query.filter(or_(
            companies.name.ilike(f'%{search}%'),
            login.username.ilike(f'%{search}%')
            ))
        search_sp = query.all()

        search_campaign = campaigns.query.filter(or_(
            campaigns.name.ilike(f'%{search}%'),
            campaigns.description.ilike(f'%{search}%'),
            campaigns.niches.ilike(f'%{search}%')
        )).all()

        search_ad = ad_requests.query.filter(ad_requests.task.ilike(f'%{search}%')).all()

        if 'logged_in' in session:
            username=session['username']
            user_id = login.query.filter_by(username=username).first().data_id
            if session['login_type'] == 'Sponsor':
                user = companies.query.filter_by(company_id=user_id).first()
                profile_pic = user.logo
            elif session['login_type'] == 'Influencer': 
                user = influencer.query.filter_by(inf_id=user_id).first()
                profile_pic = user.profile_pic
            return render_template('search.html', search_inf=search_inf, user=user, profile_pic=profile_pic, username=username, search_sp=search_sp, search_campaign=search_campaign, search_ad=search_ad, get_company_name=get_company_name, format_title=format_title, get_username=get_username, login_type=session['login_type'])
        else:
            return render_template('search.html', search_inf=search_inf, search_sp=search_sp, search_campaign=search_campaign, search_ad=search_ad, get_company_name=get_company_name, format_title=format_title, get_username=get_username)
    else:
        return render_template('error_page.html', error_code=400, error_text="No Arguments Given")


@app.route('/sponsor/offer/<int:inf_id>', methods=['GET', 'POST'])
def sponsor_offer_url_maker(inf_id):
    data = request.form
    ad_id = data['selected_ad']
    return redirect(f'/sponsor/{ad_id}/offer/{inf_id}')

@app.route('/sponsor/<int:ad_id>/offer/<int:inf_id>', methods=['GET', 'POST'])
def sponsor_offer(ad_id, inf_id):
    inf_username = login.query.filter_by(data_id=inf_id).first().username
    response = requests.post(f'http://127.0.0.1:5000/sponsor/offer?ad_id={ad_id}&inf_id={inf_id}&username={session["username"]}')
    if response.status_code == 200:
        return redirect(f'/influencer/{inf_username}')
    else:
        error_message = response.json().get('error')
        return render_template('error_page.html', error_code=response.status_code, error_text=error_message)





api.add_resource(login_user, "/login/user", "/signup/user")
api.add_resource(influencer_operations, "/influencer/new_profile", "/influencer/profile/edit")
api.add_resource(login_operations, "/user/password/edit")
api.add_resource(image_operations, "/img_upload")
api.add_resource(campaign_operations, "/sponsor/campaign/new", "/sponsor/campaign/edit", "/sponsor/campaign/delete")
api.add_resource(company_operations, "/sponsor/profile/edit")
api.add_resource(negotiations_operations, "/ad/negotiate", "/ad/negotiate/delete")
api.add_resource(contract_operations, "/ad/accept", "/influencer/contract/complete")
api.add_resource(reject_operations, "/influencer/contract/reject")
api.add_resource(ad_request_operations, "/sponsor/ad_request/new", "/sponsor/ad_request/edit", "/sponsor/ad_request/delete")
api.add_resource(flag_operations, "/admin/user/flag")
api.add_resource(ban_operations, "/admin/user/ban")
api.add_resource(campaign_flag_operations, "/admin/campaign/flag")
api.add_resource(sponsor_operations, "/sponsor/new_profile")
api.add_resource(sponsor_offer_operations, "/sponsor/offer")
api.add_resource(sponsor_negotiations_operations, "/sponsor/ad/negotiate")



if __name__ == "__main__":
    app.run(debug=True)


