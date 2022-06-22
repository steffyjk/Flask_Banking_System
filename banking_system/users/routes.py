from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required, login_manager
from banking_system import db, bcrypt
from banking_system.models import Account, Branch, Card, FixedDeposit, Insurance, InsuranceType, Loan, LoanType, \
    Transaction, TransactionType, User, UserType
from banking_system.users.forms import AddMoney, RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, \
    ResetPasswordForm
from banking_system.users.utils import send_reset_email
from flask import Blueprint
import random
import datetime
from banking_system.users.constant import *

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            user_name=form.user_name.data,
            user_password=form.user_password.data,
            user_email=form.user_email.data,
            user_phone_number=form.user_phone_number.data,
            user_first_name=form.user_first_name.data,
            user_last_name=form.user_last_name.data,
            user_address=form.user_address.data,
            user_age=form.user_age.data,
            date_of_birth=form.date_of_birth.data
        )

        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            flash(f'{e}', 'danger')
        user = User.query.filter_by(user_email=form.user_email.data).first()
        role_assign(user.user_id)
        account_creation(user.user_id)
        if current_user.is_authenticated:
            if current_user.user_email == 'steffy.inexture@gmail.com':
                flash('new user added successfully', 'success')
                return redirect(url_for('admin.admin_dashboard'))

        flash(SUCCESSFUL_REGISTRATION, FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


def role_assign(user_id):
    user_role = UserType(user_id=user_id, user_role='user')
    db.session.add(user_role)
    db.session.commit()


@users.route("/account-creation", methods=['GET', 'POST'])
def account_creation(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    branch = Branch.query.first()
    branch_id = branch.branch_id
    account_number = random.randint(1, 1000)
    account = Account(account_number=account_number, user_id=user.user_id, branch_id=branch_id)
    db.session.add(account)
    db.session.commit()


@users.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        account = Account.query.filter_by(user_id=user.user_id).first()
        if account:
            if account.account_status == 'Inactive':
                flash('Hey! admin does not activate your account yet! cant login rn', 'danger')
                return redirect(url_for('users.login'))
            elif account.account_status == 'Active':
                if user is not None and form.user_password.data == user.user_password:
                    login_user(user, remember=form.remember.data)
                    flash(SUCCESSFUL_LOGIN, FLASH_MESSAGES['SUCCESS'])

                    return redirect(url_for('users.dashboard'))
                else:
                    flash(UNSUCCESSFUL_LOGIN, FLASH_MESSAGES['FAIL'])
    return render_template('login.html', title='login', form=form)


@users.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    users = User.query.filter_by(user_id=current_user.user_id).first()
    account = Account.query.filter_by(user_id=current_user.user_id).first()
    if account:
        card = Card.query.filter_by(account_number=account.account_number).first()

        transaction = Transaction.query.filter(
            (Transaction.receiver_id == current_user.user_id) |
            (Transaction.sender_id == current_user.user_id)
        ).all()
        transaction_type = None
        for tran in transaction:
            transaction_type = TransactionType.query.filter(
                (TransactionType.transaction_id == tran.transaction_id)
            ).all()

        loan = Loan.query.filter_by(user_id=account.user_id).first()
        insurance = Insurance.query.filter_by(user_id=account.user_id).first()
        fixed_deposit = None

        fixed_deposit = FixedDeposit.query.filter_by(account_number=account.account_number).first()
        return render_template(
            'user_dashboard.html',
            title='user_dashboard',
            account=account, card=card,
            loan=loan,
            insurance=insurance,
            fixed_deposit=fixed_deposit,
            transaction=transaction,
            transaction_type=transaction_type)
    else:
        account_creation()
        card = Card.query.filter_by(account_number=account.account_number).first()
        loan = Loan.query.filter_by(user_id=account.user_id).first()
        insurance = Insurance.query.filter_by(user_id=account.user_id).first()
        transaction = Transaction.query.filter(
            (Transaction.receiver_id == current_user.user_id) |
            (Transaction.sender_id == current_user.user_id)
        ).all()
        if transaction is not None:
            for tran in transaction:
                transaction_type = TransactionType.query.filter(
                    (TransactionType.transaction_id == tran.transaction_id)
                ).all()
        fixed_deposit = FixedDeposit.query.filter_by(account_number=account.account_number).first()
        return render_template(
            'user_dashboard.html',
            title='user_dashboard',
            account=account, card=card,
            loan=loan,
            insurance=insurance,
            fixed_deposit=fixed_deposit,
            transaction=transaction,
            transaction_type=transaction_type)


@users.route("/logout")
def logout():
    logout_user()
    flash('Logout successfully..', 'success')
    return redirect(url_for('main.home'))


@users.route("/profile", methods=['GET', 'POST'])
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


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
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


@users.route("/request-account", methods=['GET', 'POST'])
def request_account():
    if current_user.is_authenticated:
        account = Account.query.filter_by(user_id=current_user.user_id)
        if account:
            flash(f'you have already account', 'danger')
            return redirect(url_for('users.dashboard'))
        else:
            user = User.query.filter_by(user_id=current_user.user_id).first()
            branch = Branch.query.first()
            branch_id = branch.branch_id
            account_number = random.randint(1, 1000)
            account = Account(account_number=account_number, user_id=user.user_id, branch_id=branch_id)
            db.session.add(account)
            db.session.commit()
            flash(f'your account has been created', 'success')
            return redirect(url_for('users.dashboard'))
    else:
        flash(f"you need to login first")
        return redirect('main.home')


@users.route("/request-card", methods=['GET', 'POST'])
def request_card():
    if current_user.is_authenticated:
        account = Account.query.filter_by(user_id=current_user.user_id).first()
        if account:
            card = Card.query.filter_by(account_number=account.account_number).first()
            if card:
                flash(f'you have already Card', 'danger')
                return redirect(url_for('users.dashboard'))
            else:
                user = User.query.filter_by(user_id=current_user.user_id).first()
                account = Account.query.filter_by(user_id=user.user_id).first()
                card_number = random.randint(1, 1000)
                cvv_number = random.randint(111, 999)
                card_pin = random.randint(1111, 9999)
                expiry_date = datetime.datetime(2026, 7, 19, 12, 0, 0)
                account_number = account.account_number
                card = Card(card_number=card_number, cvv_number=cvv_number, card_pin=card_pin, expiry_date=expiry_date,
                            account_number=account_number)
                db.session.add(card)
                db.session.commit()
                flash(f'your card has been created', 'success')
                return redirect(url_for('users.dashboard'))
        else:
            account_creation()
    else:
        flash(f"you need to login first")
        return redirect('main.home')


@users.route("/request-loan", methods=['GET', 'POST'])
def request_loan():
    if current_user.is_authenticated:
        user = Loan.query.filter_by(user_id=current_user.user_id).first()
        if user:
            flash(f'you have already current loan going on finish that  first', 'danger')
            return redirect(url_for('users.dashboard'))
        else:
            user = User.query.filter_by(user_id=current_user.user_id).first()
            loan = Loan(user_id=user.user_id)
            db.session.add(loan)
            db.session.commit()
            loan_type()
            flash(f'your loan has been requested with inactive status', 'success')
            return redirect(url_for('users.dashboard'))
    else:
        flash(f"you need to login first")
        return redirect('main.home')


def loan_type():
    loan = Loan.query.filter_by(user_id=current_user.user_id).first()
    loan_type = LoanType(loan_id=loan.loan_id)
    db.session.add(loan_type)
    db.session.commit()


@users.route("/request-insurance", methods=['GET', 'POST'])
def request_insurance():
    if current_user.is_authenticated:
        user = Insurance.query.filter_by(user_id=current_user.user_id).first()
        if user:
            flash(f'you have already current Insurance already', 'danger')
            return redirect(url_for('users.dashboard'))
        else:
            user = User.query.filter_by(user_id=current_user.user_id).first()
            insurance = Insurance(user_id=user.user_id)
            db.session.add(insurance)
            db.session.commit()
            insurance_type()
            flash(f'your insurance has been requested with inactive status', 'success')
            return redirect(url_for('users.dashboard'))
    else:
        flash(f"you need to login first")
        return redirect('main.home')


def insurance_type():
    insurance = Insurance.query.filter_by(user_id=current_user.user_id).first()
    insurance_type = InsuranceType(insurance_id=insurance.insurance_id)
    db.session.add(insurance_type)
    db.session.commit()


# add_fixed_deposit
@users.route("/add_fixed_deposit", methods=['GET', 'POST'])
def add_fixed_deposit():
    if current_user.is_authenticated:
        account = Account.query.filter_by(user_id=current_user.user_id).first()
        fixed_deposit = FixedDeposit(account_number=account.account_number)
        db.session.add(fixed_deposit)
        db.session.commit()
        flash(f'your fixed depopsite has been requested with inactive status', 'success')
        return redirect(url_for('users.dashboard'))
    else:
        flash(f"you need to login first")
        return redirect('main.home')


# add_money
@users.route("/addmoney", methods=['GET', 'POST'])
def add_money():
    form = AddMoney()
    if form.validate_on_submit():
        if form.user_password.data == current_user.user_password:
            account = Account.query.filter_by(user_id=current_user.user_id).first()
            reciver_account_number = form.reciver_account.data
            reciever = Account.query.filter_by(account_number=reciver_account_number).first()
            # sender = Account.query.filter_by(account_number=reciver_account_number).first()
            transaction_amount = form.credit_amount.data
            print("##################", reciever.account_balance)
            reciever.account_balance += transaction_amount
            account.account_balance -= transaction_amount
            receiver_id = reciever.user_id
            sender_id = current_user.user_id
            if transaction_amount < account.account_balance:
                if receiver_id != account.user_id:
                    transaction = Transaction(
                        transaction_amount=transaction_amount,
                        receiver_id=receiver_id,
                        sender_id=sender_id,
                        user_id=sender_id
                    )

                    db.session.add(transaction)
                    db.session.commit()
                    flash(f"transaction is successfully done", 'success')
                    transaction = Transaction.query.filter_by(
                        transaction_amount=transaction_amount,
                        receiver_id=receiver_id,
                        sender_id=sender_id,
                        user_id=sender_id
                    ).first()
                    transaction_id = transaction.transaction_id
                    transaction_type = 'credit'
                    def_transaction_type(transaction_type, transaction_id)
                    return redirect(url_for('users.dashboard'))
                else:
                    flash(f'you can not transfer to yourself it doesnot make any sense', 'danger')
                    return redirect(url_for('users.add_money'))
            else:
                flash(f'unsufficient balance you have only: {account.account_balance}', 'danger')
                return redirect(url_for('users.add_money'))
        else:
            flash(f'password is incorrect', 'danger')
            return render_template('add_money.html', title='add_money', form=form)
    return render_template('add_money.html', title='add_money', form=form)


def def_transaction_type(transaction_type, transaction_id):
    transaction_type = TransactionType(
        transaction_type=transaction_type,
        transaction_id=transaction_id
    )
    db.session.add(transaction_type)
    db.session.commit()
