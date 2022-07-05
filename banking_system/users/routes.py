from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func
from banking_system import db, bcrypt
from banking_system.models import Account, Branch, Card, FixedDeposit, Insurance, Loan, \
    Transaction, TransactionType, User
from banking_system.users.forms import AddMoney, RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, \
    ResetPasswordForm, ApplyLoanForm, TransferMoney, ChangeBranch
from banking_system.users.utils import send_reset_email, send_otp_email, role_assign, add_loan_type, loan_type, \
    insurance_type, fd_interest
import random
import datetime
from banking_system.users.constants import FLASH_MESSAGES, NEW_USER_ADDED, SUCCESSFUL_REGISTRATION, \
    ADMIN_NOT_ACTIVATE_UR_ACCOUNT, SUCCESSFUL_LOGIN, UNSUCCESSFUL_LOGIN, LOGOUT_SUCCESS, ACCOUNT_UPDATED, EMAIL_INFO, \
    INVALID_TOKEN, PASSWORD_UPDATED, ACCOUNT_ALREADY_EXISTED, ACCOUNT_CREATED, LOGIN_FIRST, ALREADY_CARD_EXISTED, \
    CARD_CREATED, PENDING_LOAN, TRANSACTION_SUCCESSFULLY, CANT_TRANSFER, \
    PASSWORD_INCORRECT, INSUFFICIENT_BALANCE, PENDING_ACTIVITY, SUCCESS_ACTIVITY, BRANCH_CHANGED, ERROR

users = Blueprint('users', __name__)


# registration route to register user
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
            flash(f'{e}', FLASH_MESSAGES['FAIL'])
        user = User.query.filter_by(user_email=form.user_email.data).first()
        role_assign(user.user_id)
        account_creation(user.user_id)
        if current_user.is_authenticated:
            if current_user.user_email == 'steffy.inexture@gmail.com':
                flash(NEW_USER_ADDED, FLASH_MESSAGES['SUCCESS'])
                return redirect(url_for('admin.admin_dashboard'))

        flash(SUCCESSFUL_REGISTRATION, FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


# # assign the role of any user [ bank user / bank admin ]
# def role_assign(user_id):
#     user_role = UserType(user_id=user_id, user_role='user')
#     db.session.add(user_role)
#     db.session.commit()


# create the bank account at the initial stage
@users.route("/account-creation", methods=['GET', 'POST'])
def account_creation(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    branch = Branch.query.first()
    branch_id = branch.branch_id
    # account_number = random.randint(1, 1000)
    account = db.session.query(func.max(Account.account_number)).first()
    if account[0]:
        account_number = account[0] + 1
    else:
        account_number = 1000000
    account = Account(account_number=account_number, user_id=user.user_id, branch_id=branch_id, account_balance=5000)
    db.session.add(account)
    db.session.commit()


@users.route("/change_branch", methods=['GET', 'POST'])
@login_required
def change_branch():
    user = User.query.filter_by(user_id=current_user.user_id).first()
    account = Account.query.filter_by(user_id=current_user.user_id).first()
    branches = Branch.query.all()

    form = ChangeBranch()

    if form.validate_on_submit():
        print("this is branch selected by the user: ", form.myField.data)
        selected_branch = form.myField.data
        branch = Branch.query.filter_by(branch_name=selected_branch).first()
        if branch:
            account.branch_id = branch.branch_id
            db.session.commit()
            flash(BRANCH_CHANGED, FLASH_MESSAGES['SUCCESS'])
        else:
            flash(ERROR, FLASH_MESSAGES['FAIL'])

        return redirect(url_for('users.dashboard'))
    elif request.method == 'GET':
        form.user_id.data = user.user_id
        form.user_name.data = user.user_name
        form.account_number.data = account.account_number
        form.myField.choices = [i.branch_name for i in Branch.query.all()]

    return render_template('change_branch.html', user=user, account=account, branches=branches, form=form)


# Login route to log in registered user to the website
@users.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        account = Account.query.filter_by(user_id=user.user_id).first()
        if account:
            if account.account_status == 'Inactive':
                flash(ADMIN_NOT_ACTIVATE_UR_ACCOUNT, FLASH_MESSAGES['FAIL'])
                return redirect(url_for('users.login'))
            elif account.account_status == 'Active':
                if user is not None and form.user_password.data == user.user_password:
                    login_user(user, remember=form.remember.data)
                    flash(SUCCESSFUL_LOGIN, FLASH_MESSAGES['SUCCESS'])

                    return redirect(url_for('users.dashboard'))
                else:
                    flash(UNSUCCESSFUL_LOGIN, FLASH_MESSAGES['FAIL'])
    return render_template('login.html', title='login', form=form)


# User dashboard to show all the functionalities which is performed by the user only
@users.route("/user-dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
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


# logout route to logout the session after login and all procedure
@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash(LOGOUT_SUCCESS, FLASH_MESSAGES['SUCCESS'])
    return redirect(url_for('main.home'))


# Profile route to see the personal data of any user
@users.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():

        current_user.user_name = form.user_name.data
        current_user.user_phone_number = form.user_phone_number.data
        current_user.user_first_name = form.user_first_name.data
        current_user.user_last_name = form.user_last_name.data
        current_user.user_address = form.user_address.data
        current_user.user_age = form.user_age.data
        current_user.date_of_birth = form.date_of_birth.data

        db.session.commit()
        flash(ACCOUNT_UPDATED, FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('users.dashboard'))
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.user_phone_number.data = current_user.user_phone_number
        form.user_first_name.data = current_user.user_first_name
        form.user_last_name.data = current_user.user_last_name
        form.user_address.data = current_user.user_address
        form.user_age.data = current_user.user_age
        form.date_of_birth.data = current_user.date_of_birth
        form.user_email.data = current_user.user_email

    return render_template('user_profile.html', title='Account', form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        send_reset_email(user)
        flash(EMAIL_INFO, FLASH_MESSAGES['INFO'])
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash(INVALID_TOKEN, FLASH_MESSAGES['WARNING'])
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # user.user_password = hashed_password
        user.user_password = form.user_password.data
        db.session.commit()
        flash(PASSWORD_UPDATED, FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route("/request-account", methods=['GET', 'POST'])
def request_account():
    if current_user.is_authenticated:
        account = Account.query.filter_by(user_id=current_user.user_id)
        if account:
            flash(ACCOUNT_ALREADY_EXISTED, FLASH_MESSAGES['FAIL'])
            return redirect(url_for('users.dashboard'))
        else:
            user = User.query.filter_by(user_id=current_user.user_id).first()
            branch = Branch.query.first()
            branch_id = branch.branch_id
            account = db.session.query(func.max(Account.account_number)).first()
            if account[0]:
                account_number = account[0] + 1
            else:
                account_number = 1000000

            account = Account(account_number=account_number, user_id=user.user_id, branch_id=branch_id)
            db.session.add(account)
            db.session.commit()
            flash(ACCOUNT_CREATED, FLASH_MESSAGES['SUCCESS'])
            return redirect(url_for('users.dashboard'))
    else:
        flash(LOGIN_FIRST, FLASH_MESSAGES['FAIL'])
        return redirect('main.home')


# Request for the card if not have card yet
@users.route("/request-card", methods=['GET', 'POST'])
@login_required
def request_card():
    if current_user.is_authenticated:
        account = Account.query.filter_by(user_id=current_user.user_id).first()
        if account:
            card = Card.query.filter_by(account_number=account.account_number).first()
            if card:
                flash(ALREADY_CARD_EXISTED, FLASH_MESSAGES['FAIL'])
                return redirect(url_for('users.dashboard'))
            else:
                user = User.query.filter_by(user_id=current_user.user_id).first()
                account = Account.query.filter_by(user_id=user.user_id).first()
                card = db.session.query(func.max(Card.card_number)).first()
                if card[0]:
                    card_number = card[0] + 1
                else:
                    card_number = 10000
                cvv_number = random.randint(111, 999)
                card_pin = random.randint(1111, 9999)
                expiry_date = datetime.datetime(2026, 7, 19, 12, 0, 0)
                account_number = account.account_number
                card = Card(card_number=card_number, cvv_number=cvv_number, card_pin=card_pin, expiry_date=expiry_date,
                            account_number=account_number)
                db.session.add(card)
                db.session.commit()
                flash(CARD_CREATED, FLASH_MESSAGES['SUCCESS'])
                return redirect(url_for('users.dashboard'))
        else:
            account_creation()
    else:
        flash(LOGIN_FIRST, FLASH_MESSAGES['FAIL'])
        return redirect('main.home')


# apply for loan via this route [ request goes to admin panel with INACTIVE STATUS]
# giving the PERSONAL/EDUCATION/HOME/OTHER loan option right now
@users.route("/apply-for-loan", methods=['GET', 'POST'])
@login_required
def apply_loan():
    form = ApplyLoanForm()
    user = User.query.filter_by(user_id=current_user.user_id).first()
    if form.validate_on_submit():
        loan = Loan.query.filter_by(user_id=user.user_id).first()
        if loan:
            flash(PENDING_ACTIVITY.format(activity='LOAN'), FLASH_MESSAGES['FAIL'])
            return redirect(url_for('users.dashboard'))
        else:
            user_id = form.user_id.data
            user_name = form.user_name.data
            loan_amount = form.loan_amount_choices.data
            rate_interest = form.loan_rate_interests.data
            loan_type = form.loan_type.data
            if loan_amount == '1':
                loan_amount = '1000'
            elif loan_amount == '2':
                loan_amount = '5000'
            elif loan_amount == '3':
                loan_amount = '10000'
            else:
                loan_amount = '15000'

            if rate_interest == '1':
                rate_interest = '6.5'
            else:
                rate_interest = '6.7'

            if loan_type == '1':
                loan_type = 'Personal loan'
            elif loan_type == '2':
                loan_type = 'Education loan'
            elif loan_type == '3':
                loan_type = 'Home loan'
            else:
                loan_type = 'Other'

            # print()

            loan = Loan(user_id=user.user_id, loan_amount=loan_amount, rate_interest=rate_interest)
            db.session.add(loan)
            db.session.commit()
            loan_ = Loan.query.filter_by(user_id=user.user_id).first()
            add_loan_type(loan_type, loan_.loan_id)
            flash(SUCCESS_ACTIVITY.format(activity='loan'), FLASH_MESSAGES['SUCCESS'])
            return redirect(url_for('users.dashboard'))

    elif request.method == 'GET':
        form.user_id.data = user.user_id
        form.user_name.data = user.user_name

    return render_template(
        'applyloan.html',
        user_id=current_user.user_id,
        user_name=current_user.user_name,
        title='apply for loan',
        form=form
    )


@users.route("/send-otp/<current_user>")
def send_otp_fun(current_user):
    print("yaya")
    otp = send_otp_email(current_user)
    # return JsonResponse({"status": "save"})


# # After applying for loan add the type of loan to loantype table with loan id data
# def add_loan_type(loan_type, loan_id):
#     loan_type = str(loan_type)
#     loan = LoanType(loan_id=loan_id, loan_type=loan_type)
#     db.session.add(loan)
#     db.session.commit()


# Request for loan route by user
@users.route("/request-loan", methods=['GET', 'POST'])
def request_loan():
    if current_user.is_authenticated:
        user = Loan.query.filter_by(user_id=current_user.user_id).first()
        if user:
            flash(PENDING_LOAN, FLASH_MESSAGES['FAIL'])
            return redirect(url_for('users.dashboard'))
        else:
            user = User.query.filter_by(user_id=current_user.user_id).first()
            loan = Loan(user_id=user.user_id)
            db.session.add(loan)
            db.session.commit()
            loan_type()
            flash(SUCCESS_ACTIVITY.format(activity='LOAN'), FLASH_MESSAGES['SUCCESS'])
            return redirect(url_for('users.dashboard'))
    else:
        flash(LOGIN_FIRST, FLASH_MESSAGES['FAIL'])
        return redirect('main.home')


# # add loan type
# def loan_type():
#     loan = Loan.query.filter_by(user_id=current_user.user_id).first()
#     loan_type = LoanType(loan_id=[loan.loan_id])
#     db.session.add(loan_type)
#     db.session.commit()


# Request for insurance requested to admin panel with INACTIVE STATUS
@users.route("/request-insurance", methods=['GET', 'POST'])
@login_required
def request_insurance():
    if current_user.is_authenticated:
        user = Insurance.query.filter_by(user_id=current_user.user_id).first()
        if user:
            flash(PENDING_ACTIVITY.format(activity='INSURANCE'), FLASH_MESSAGES['FAIL'])
            return redirect(url_for('users.dashboard'))
        else:
            user = User.query.filter_by(user_id=current_user.user_id).first()
            insurance = Insurance(user_id=user.user_id)
            db.session.add(insurance)
            db.session.commit()
            insurance_type()
            flash(SUCCESS_ACTIVITY.format(activity='INSURANCE'), FLASH_MESSAGES['SUCCESS'])
            return redirect(url_for('users.dashboard'))
    else:
        flash(LOGIN_FIRST, FLASH_MESSAGES['FAIL'])
        return redirect('main.home')


# # add type of insurance after applying for the insurance
# def insurance_type():
#     insurance = Insurance.query.filter_by(user_id=current_user.user_id).first()
#     insurance_type = InsuranceType(insurance_id=insurance.insurance_id)
#     db.session.add(insurance_type)
#     db.session.commit()


# add_fixed_deposit
@users.route("/add_fixed_deposit", methods=['GET', 'POST'])
@login_required
def add_fixed_deposit():
    if current_user.is_authenticated:
        account = Account.query.filter_by(user_id=current_user.user_id).first()
        fixed_deposit = FixedDeposit(account_number=account.account_number)
        db.session.add(fixed_deposit)
        db.session.commit()
        flash(SUCCESS_ACTIVITY.format(activity='FIXED DEPOSIT'), FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('users.dashboard'))
    else:
        flash(LOGIN_FIRST, FLASH_MESSAGES['FAIL'])
        return redirect('main.home')


# add_money
@users.route("/addmoney", methods=['GET', 'POST'])
@login_required
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

            receiver_id = reciever.user_id
            sender_id = current_user.user_id
            print(transaction_amount)
            print(account.account_balance)
            if transaction_amount <= account.account_balance:
                if receiver_id != account.user_id:
                    reciever.account_balance += transaction_amount
                    account.account_balance -= transaction_amount
                    transaction = Transaction(
                        transaction_amount=transaction_amount,
                        receiver_id=receiver_id,
                        sender_id=sender_id,
                        user_id=sender_id
                    )

                    db.session.add(transaction)
                    db.session.commit()
                    flash(TRANSACTION_SUCCESSFULLY, FLASH_MESSAGES['SUCCESS'])
                    transaction = Transaction.query.filter_by(
                        transaction_amount=transaction_amount,
                        receiver_id=receiver_id,
                        sender_id=sender_id,
                        user_id=sender_id
                    ).first()
                    transaction_id = transaction.transaction_id
                    transaction_type = 'credit'
                    transaction_type(transaction_type, transaction_id)
                    return redirect(url_for('users.dashboard'))
                else:
                    flash(CANT_TRANSFER, FLASH_MESSAGES['FAIL'])
                    return redirect(url_for('users.add_money'))
            else:
                flash(INSUFFICIENT_BALANCE.format(data=account.account_balance), FLASH_MESSAGES['FAIL'])
                return redirect(url_for('users.add_money'))
        else:
            flash(PASSWORD_INCORRECT, FLASH_MESSAGES['FAIL'])
            return render_template('add_money.html', title='add_money', form=form)
    return render_template('add_money.html', title='add_money', form=form)


# # add the transaction type after any transaction
# def def_transaction_type(transaction_type, transaction_id):
#     transaction_type = TransactionType(
#         transaction_type=transaction_type,
#         transaction_id=transaction_id
#     )
#     db.session.add(transaction_type)
#     db.session.commit()


# transfer money
@users.route("/Transfer-money", methods=['GET', 'POST'])
@login_required
def transfer_money():
    user = User.query.filter_by(user_id=current_user.user_id).first()
    account = Account.query.filter_by(user_id=user.user_id).first()
    loan = Loan.query.filter_by(user_id=user.user_id).first()
    fd = FixedDeposit.query.filter_by(account_number=account.account_number).first()

    form = TransferMoney()

    if form.validate_on_submit():

        transfer_choice = form.transfer_choice.data
        transfer_amount = form.transfer_amount.data
        otp_btn = form.otp_btn.data
        if transfer_choice == '1':
            account.saving_balance += transfer_amount
            account.account_balance -= transfer_amount
        elif transfer_choice == '2':
            account.saving_balance -= transfer_amount
            account.account_balance += transfer_amount
        elif transfer_choice == '3':
            account.account_balance -= transfer_amount
            loan.loan_amount -= transfer_amount
        elif transfer_choice == '4':
            account.account_balance -= transfer_amount
            fd.fd_amount += transfer_amount
        else:
            flash('something went wrong', 'danger')
            return redirect(url_for('users.dashboard'))

        if otp_btn:
            send_otp_email(current_user)

        transfer = Transaction(
            user_id=user.user_id,
            transaction_amount=transfer_amount,
            sender_id=user.user_id,
            receiver_id=user.user_id,
        )
        db.session.add(transfer)
        db.session.commit()

        flash('transaction done', 'success')
        return redirect(url_for('users.dashboard'))

    elif request.method == 'GET':
        form.user_id.data = user.user_id
        form.user_name.data = user.user_name

    return render_template('transfermoney.html', form=form)


count = 0


@users.route("/fd-money-transfer/", methods=['GET', 'POST'])
@login_required
def fd_interest_money():
    date = datetime.datetime.now()
    global count
    account = Account.query.filter_by(user_id=current_user.user_id).first()
    fd = FixedDeposit.query.filter_by(account_number=account.account_number).first()
    now = datetime.datetime.now()
    old_date = fd.fd_create_date
    if old_date.date() < now.date():
        count += 1
        if count == 1:
            print("fd_amount= ", fd.fd_amount)
            print("fd_rate_interest=", fd.rate_interest)
            amount = (fd.fd_amount * fd.rate_interest) / 100
            account.account_balance += ((fd.fd_amount * fd.rate_interest) / 100)
            db.session.commit()
            flash(f"{amount} has been added", 'success')
        else:
            flash('already done cant do twice', 'danger')
    elif old_date.date() == now.date():
        print("yes same")
        if old_date.time() < now.date():
            count += 1
            if count == 1:
                print("fd_amount= ", fd.fd_amount)
                print("fd_rate_interest=", fd.rate_interest)
                amount = (fd.fd_amount * fd.rate_interest) / 100
                account.account_balance += ((fd.fd_amount * fd.rate_interest) / 100)
                db.session.commit()
                flash(f"{amount} has been added", 'success')
            else:
                flash('already done cant do twice', 'danger')
            print("yes the time")
        else:
            print("no way time")
    else:
        print("no way")

    duration = 60

    print("DDSDS", fd.fd_create_date - now)
    return redirect(url_for('users.dashboard'))
