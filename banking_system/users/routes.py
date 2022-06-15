from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required, login_manager
from banking_system import db, bcrypt
from banking_system.models import Account, Branch, User, User_type
from banking_system.users.forms import RegistrationForm, LoginForm, UpdateAccountForm,RequestResetForm,ResetPasswordForm
from banking_system.users.utils import send_reset_email
from flask import Blueprint
import random


users = Blueprint('users', __name__)


@users.route("/register", methods = ['GET',  'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # u.password = u.password.decode("utf-8", "ignore")
        # hashed_password = bcrypt.generate_password_hash(form.user_password.data).decode('utf-8')
        user = User(user_name=form.user_name.data,user_password=form.user_password.data,
        user_email=form.user_email.data,user_phone_number=form.user_phone_number.data,
        user_first_name=form.user_first_name.data,user_last_name=form.user_last_name.data,
        user_address=form.user_address.data,user_age=form.user_age.data,date_of_birth=form.date_of_birth.data)
        
        db.session.add(user)
        
        try:
            db.session.commit()    
            flash(f'your account has been created you are all set for login', 'success')
            
        except Exception as e:
            flash(f'{e}','danger')
        user = User.query.filter_by(user_email=form.user_email.data).first()
        role_assign(user.user_id)
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)

def role_assign(user_id):
    user_role = User_type(user_id=user_id, user_role='user')
    db.session.add(user_role)
    db.session.commit()



# @login_manager.user_loader
@users.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        if user is not None and form.user_password.data == user.user_password:
            # print(user,"######")        
            login_user(user, remember=form.remember.data)

            flash('Login successfully..', 'success')
            return redirect(url_for('users.dashboard'))
        else:
            flash('Login unsuccessfull..please check email and password', 'danger')
    return render_template('login.html', title='login', form=form)

@users.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():
    return render_template('user_dashboard.html', title='user_dashboard')

@users.route("/logout")
def logout():
    logout_user()
    flash('Logout successfully..', 'success')
    return redirect(url_for('main.home'))

@users.route("/profile", methods=['GET',  'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
      
        current_user.user_name = form.user_name.data
        
        db.session.commit()
        flash('your account has been update!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        
    return render_template('user_profile.html', title='Account', form=form)


@users.route("/reset_password", methods = ['GET',  'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password.','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods = ['GET',  'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user =User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # user.user_password = hashed_password
        user.user_password = form.user_password.data
        db.session.commit()
        flash(f'your password has been updated!, you are now able to login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@users.route("/request-account", methods = ['GET', 'POST'])
def request_account():
    if current_user.is_authenticated:
        # print('this is current user:',current_user.user_name)
        user = User.query.filter_by(user_id = current_user.user_id).first()
        # print('this is user: ',user)
        branch=Branch.query.first()
        branch_id = branch.branch_id
        account_number = random.randint(1,1000)
        account = Account(account_number=account_number,user_id=user.user_id,branch_id=branch_id)
        db.session.add(account)
        db.session.commit()
        flash(f'your account has been created')

        return redirect(url_for('users.dashboard'))
    else:
        flash(f"you need to login first")
        return redirect('main.home')
