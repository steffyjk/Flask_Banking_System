import os
import secrets
from PIL import Image

from flask import render_template, url_for, flash, redirect, request, current_app, jsonify
from flask_login import login_user, login_required
from banking_system import db, bcrypt
from banking_system.admin.constants import ADMIN_LOGIN_SUCCESS, FLASH_MESSAGES, ADMIN_LOGIN_UNSUCCESS, USER_DELETED, \
    BRANCH_EXISTED, BRANCH_ADDED, ATM_EXISTED, ATM_ADDED, BANK_MEMBER_DELETED, BANK_MEMBER_ADDED, \
    STATUS_UPDATE
from banking_system.models import Atm, User, Branch, BankDetails, Account, Loan, LoanType, Insurance, InsuranceType, \
    FixedDeposit, Transaction, TransactionType, BankMember, MemberRole, LoanDetails, InsuranceDetails
from banking_system.admin.forms import AddBranch, LoginForm, AddAtm, UserAccountStatus, LoanApprovalStatus, \
    InsuranceApprovalForm, BankMemberData, UpdateFdStatus, AddMemberRole, LoanChoice, InsuranceChoice
from flask import Blueprint

admin = Blueprint('admin', __name__)

# this is for the admin login only
@admin.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email='steffy.inexture@gmail.com').first()
        if user is not None and form.user_password.data == user.user_password:
            login_user(user, remember=form.remember.data)

            flash(ADMIN_LOGIN_SUCCESS, FLASH_MESSAGES['SUCCESS'])
            users = User.query.order_by(User.user_id.desc())
            atms = Atm.query.order_by(Atm.atm_id.desc())
            branchs = Branch.query.order_by(Branch.branch_id.desc())
            return render_template('admin_dashboard.html', users=users, branchs=branchs, atms=atms)
        else:
            flash(ADMIN_LOGIN_UNSUCCESS, FLASH_MESSAGES['FAIL'])
    return render_template('admin_login.html', title='login', form=form)


# this is admin dashboard
@admin.route("/admin_dashboard", methods=['GET', 'POST'])
def admin_dashboard():
    users = User.query.all()
    accounts = Account.query.all()
    atms = Atm.query.order_by(Atm.atm_id.desc())
    branchs = Branch.query.order_by(Branch.branch_id.desc())
    return render_template('admin_dashboard.html', users=users, branchs=branchs, atms=atms, accounts=accounts)


# show all bank user data
@admin.route("/all-user-data", methods=['GET', 'POST'])
def admin_user_data():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=3)
    accounts = Account.query.all()
    return render_template('admin_user_data.html', users=users, accounts=accounts)


# delete bank user from the user table
@admin.route("/delete-user/<user_id>", methods=['GET', 'POST'])
def delete_user(user_id):
    User.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    flash(USER_DELETED, FLASH_MESSAGES['SUCCESS'])
    return redirect(url_for('admin.admin_user_data'))


# show all branches of the bank
@admin.route("/all-branch-data", methods=['GET', 'POST'])
def admin_branch_data():
    page = request.args.get('page', 1, type=int)
    branchs = Branch.query.order_by(Branch.branch_id.desc()).paginate(page=page, per_page=5)
    return render_template('admin_branch_data.html', branchs=branchs)


# show all atm of the bank
@admin.route("/all-atm-data", methods=['GET', 'POST'])
def admin_atm_data():
    page = request.args.get('page', 1, type=int)
    atms = Atm.query.order_by(Atm.atm_id.desc()).paginate(page=page, per_page=5)
    return render_template('admin_atm_data.html', atms=atms)


# show all loan requests from the bank users
@admin.route("/all-loan-data", methods=['GET', 'POST'])
def admin_user_loan_data():
    page = request.args.get('page', 1, type=int)
    user = User.query.paginate(page=page, per_page=5)
    loans = Loan.query.all()
    loantype = LoanType.query.all()
    return render_template('admin_user_loan_data.html', loans=loans, loantype=loantype, user=user)


# for approving the loan requests
@admin.route("/loan-approval-status/<user_id>/<user_name>/<loan_id>/<loan_amount>/<rate_interest>/<paid_amount"
             ">/<loan_type>/<loan_status>", methods=['GET', 'POST'])
def loan_approval(user_id,
                  user_name,
                  loan_id,
                  loan_amount,
                  rate_interest,
                  paid_amount,
                  loan_type,
                  loan_status
                  ):
    form = LoanApprovalStatus()
    if form.validate_on_submit():
        approval_status = form.approval_status.data
        loan = Loan.query.filter_by(user_id=user_id).first()
        if approval_status == '1':
            loan.loan_status = 'Active'
            add_loan_money_to_user(user_id, loan_amount, loan_type)
        else:
            loan.loan_status = 'Inactive'
        db.session.commit()
        flash(STATUS_UPDATE.format(user_name, 'loan'), FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('admin.admin_user_loan_data'))
    elif request.method == 'GET':
        form.user_id.data = user_id
        form.user_name.data = user_name
        form.loan_id.data = loan_id
        form.loan_amount.data = loan_amount
        form.rate_interest.data = rate_interest
        form.paid_amount.data = paid_amount
        form.loan_type.data = loan_type
        form.loan_status.data = loan_status

    return render_template(
        'loan_request_approval.html',
        user_id=user_id,
        user_name=user_name,
        loan_id=loan_id,
        loan_amount=loan_amount,
        rate_interest=rate_interest,
        paid_amount=paid_amount,
        loan_type=loan_type,
        loan_status=loan_status,
        title='account-status', form=form
    )


# add loan amount to the user's account balance transfer
def add_loan_money_to_user(user_id, loan_amount, loan_type):
    user = User.query.filter_by(user_id=user_id).first()
    account = Account.query.filter_by(user_id=user.user_id).first()
    account.account_balance += int(loan_amount)
    transaction = Transaction(transaction_amount=loan_amount, sender_id=1, receiver_id=user.user_id, user_id=user_id)
    db.session.add(transaction)
    db.session.commit()
    transaction = Transaction.query.filter_by(transaction_amount=loan_amount, sender_id=1,
                                              receiver_id=user.user_id).first()
    type = TransactionType(transaction_id=transaction.transaction_id, transaction_type=f'Loan-{loan_type}')
    db.session.add(type)
    db.session.commit()


# show all requests of the insurance from the bank users
@admin.route("/all-insurance-data", methods=['GET', 'POST'])
def admin_user_insurance_data():
    users = User.query.all()
    insurances = Insurance.query.all()
    insurancetypes = InsuranceType.query.all()
    return render_template('admin_user_insurance_data.html', insurances=insurances, insurancetypes=insurancetypes,
                           users=users)


# approve the insurance status for bank users
@admin.route(
    "/insurance-approval-status/<user_id>/<user_name>/<insurance_id>/<insurance_amount>/<insurance_type"
    ">/<insurance_status>",
    methods=['GET', 'POST'])
def insurance_approval(user_id,
                       user_name,
                       insurance_id,
                       insurance_amount,
                       insurance_type,
                       insurance_status
                       ):
    form = InsuranceApprovalForm()
    if form.validate_on_submit():
        approval_status = form.approval_status.data
        insurance = Insurance.query.filter_by(user_id=user_id).first()
        if approval_status == '1':
            insurance.insurance_status = 'Active'
        else:
            insurance.insurance_status = 'Inactive'
        db.session.commit()
        flash(STATUS_UPDATE.format(user_name=user_name, activity='insurance'), FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('admin.admin_user_insurance_data'))
    elif request.method == 'GET':
        form.user_id.data = user_id
        form.user_name.data = user_name
        form.insurance_id.data = insurance_id
        form.insurance_amount.data = insurance_amount
        form.insurance_type.data = insurance_type
        form.insurance_status.data = insurance_status

    return render_template(
        'insurance_request_approval.html',
        user_id=user_id,
        user_name=user_name,
        insurance_id=insurance_id,
        insurance_amount=insurance_amount,
        insurance_type=insurance_type,
        insurance_status=insurance_status,
        title='account-status', form=form
    )


# show all fixed deposits data requested by the bank users
@admin.route("/all-fd-data", methods=['GET', 'POST'])
def admin_user_fd_data():
    users = User.query.all()
    account = Account.query.all()
    fds = FixedDeposit.query.all()

    return render_template('admin_user_fd_data.html', fds=fds,
                           users=users, account=account)


@admin.route("/update-fd-status/<user_id>", methods=['GET', 'POST'])
def update_fd_status(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    account = Account.query.filter_by(user_id=user.user_id).first()
    fd = FixedDeposit.query.filter_by(account_number=account.account_number).first()
    form = UpdateFdStatus()
    if form.validate_on_submit():
        status = form.fd_status.data
        fd.fd_status = status
        db.session.commit()
        flash(STATUS_UPDATE.format(user_name=user.user_name, activity='Fd'), FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('admin.admin_user_fd_data'))
    elif request.method == 'GET':
        form.user_id.data = user.user_id
        form.user_name.data = user.user_name
        form.fd_id.data = fd.fd_id
        form.fd_amount.data = fd.fd_amount

    return render_template(
        'update_fd_status.html',
        title='fd-status', form=form
    )


@admin.route("/delete-fd/<user_id>", methods=['GET', 'POST'])
def delete_fd(user_id):
    print("this is user_id from ajax: ", user_id)
    user = User.query.filter_by(user_id=user_id).first()
    print("this is name: ", user.user_name)
    flash(f"{user.user_name} this is the name", 'success')
    return redirect(url_for('admin.admin_user_fd_data'))


# approve/decline the fixed deposites requests from the bank users
@admin.route(
    "/fd-approval-status/<user_id>/<user_name>/<insurance_id>/<insurance_amount>/<insurance_type>/<insurance_status>",
    methods=['GET', 'POST'])
def fd_approval(user_id,
                user_name,
                insurance_id,
                insurance_amount,
                insurance_type,
                insurance_status
                ):
    form = InsuranceApprovalForm()
    if form.validate_on_submit():
        approval_status = form.approval_status.data
        insurance = Insurance.query.filter_by(user_id=user_id).first()
        if approval_status == '1':
            insurance.insurance_status = 'Active'
        else:
            insurance.insurance_status = 'Inactive'
        db.session.commit()
        flash(STATUS_UPDATE.format(user_name=user_name, activity='FD'), FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('admin.admin_user_insurance_data'))
    elif request.method == 'GET':
        form.user_id.data = user_id
        form.user_name.data = user_name
        form.insurance_id.data = insurance_id
        form.insurance_amount.data = insurance_amount
        form.insurance_type.data = insurance_type
        form.insurance_status.data = insurance_status

    return render_template(
        'insurance_request_approval.html',
        user_id=user_id,
        user_name=user_name,
        insurance_id=insurance_id,
        insurance_amount=insurance_amount,
        insurance_type=insurance_type,
        insurance_status=insurance_status,
        title='account-status', form=form
    )


# change the account status of the bank user's account [ ACTIVE / DEACTIVE ]
@admin.route("/change-account-status/<user_id>/<user_name>/<account_number>", methods=['GET', 'POST'])
def account_status(user_id, user_name, account_number):
    form = UserAccountStatus()
    if form.validate_on_submit():
        account_status = form.account_status.data
        account = Account.query.filter_by(user_id=user_id).first()
        if account_status == '1':
            account.account_status = 'Inactive'
        else:
            account.account_status = 'Active'
        db.session.commit()
        flash(STATUS_UPDATE.format(user_name=user_name, activity='Account'), FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('admin.admin_dashboard'))
    elif request.method == 'GET':
        form.user_id.data = user_id
        form.user_name.data = user_name
        form.account_number.data = account_number

    return render_template('user_account_status.html',
                           user_id=int(user_id),
                           user_name=user_name,
                           account_number=1,
                           title='account-status', form=form)


# add new branch of the bank
@admin.route("/add_branch", methods=['GET', 'POST'])
def add_branch():
    form = AddBranch()
    if form.validate_on_submit():
        table_branch = Branch.query.filter_by(branch_name=form.branch_name.data).first()
        if table_branch:
            flash(BRANCH_EXISTED, FLASH_MESSAGES['FAIL'])
            return redirect(url_for('admin.add_branch'))
        else:
            bank = BankDetails.query.all()
            branch = Branch(
                branch_name=form.branch_name.data,
                branch_address=form.branch_address.data,
                bank_id=bank[0].bank_id
            )
            db.session.add(branch)
            try:
                db.session.commit()
                flash(BRANCH_ADDED, FLASH_MESSAGES['SUCCESS'])
                return redirect(url_for('admin.admin_dashboard'))
            except Exception as e:
                flash(f'{e}', FLASH_MESSAGES['FAIL'])
    return render_template('add_branch.html', title='add-branch', form=form)


# add new atm of the bank
@admin.route("/add_atm", methods=['GET', 'POST'])
def add_atm():
    form = AddAtm()
    if form.validate_on_submit():
        table_atm = Atm.query.filter_by(atm_address=form.atm_address.data).first()
        if table_atm:
            flash(ATM_EXISTED, FLASH_MESSAGES['FAIL'])
            return redirect(url_for('admin.add_atm'))
        else:
            bank = BankDetails.query.all()
            atm = Atm(
                atm_address=form.atm_address.data,
                bank_id=bank[0].bank_id
            )
            db.session.add(atm)
            try:
                db.session.commit()
                flash(ATM_ADDED, FLASH_MESSAGES['SUCCESS'])
                return redirect(url_for('admin.admin_dashboard'))
            except Exception as e:
                flash(f'{e}', FLASH_MESSAGES['FAIL'])
    return render_template('add_atm.html', title='add-atm', form=form)


# show all bank members of current bank
@admin.route("/bank-show-all-member", methods=['GET', 'POST'])
@login_required
def show_bank_member():
    member = BankMember.query.all()
    return render_template('show_bank_member.html', member=member)


# add data to the about page to show the details of the bank member
@admin.route("/bank-about-member", methods=['GET', 'POST'])
@login_required
def bank_about_member():
    form = BankMemberData()
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture_about(form.image_file.data)
        data = BankMember(
            image_file=picture_file,
            bank_member_name=form.bank_member_name.data,
            bank_member_position=form.bank_member_position.data,
            bank_member_about=form.bank_member_about.data,
            bank_member_email_id=form.bank_member_email_id.data,
            bank_member_contact=form.bank_member_contact.data
        )
        db.session.add(data)
        db.session.commit()
        flash(BANK_MEMBER_ADDED, FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('admin.admin_dashboard'))
    elif request.method == 'GET':
        form.bank_member_position.choices = [i.member_role for i in MemberRole.query.all()]

    return render_template('add_bank_member.html', title='New bank member',
                           form=form, legend='New bank member')


# save image of the bank member fetched from the form data into static pic folder
def save_picture_about(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# delete bank member from the membership of the bank
@admin.route("/delete-bank-member/<member_id>/<member_position>", methods=['GET', 'POST'])
@login_required
def delete_bank_member(member_id, member_position):
    member = BankMember.query.filter_by(bank_member_id=member_id).delete()
    db.session.commit()
    flash(BANK_MEMBER_DELETED, FLASH_MESSAGES['SUCCESS'])
    print(member)
    return redirect(url_for('admin.admin_dashboard'))

# add new insurance detail for choices [ personal loan, education loan ] of the bank
@admin.route("/show_member_role_list", methods=['GET', 'POST'])
def show_member_role_list():
    page = request.args.get('page', 1, type=int)
    roles = MemberRole.query.paginate(page=page, per_page=3)
    return render_template('show_all_member_role.html', roles=roles)


# add new insurance detail for choices [ personal loan, education loan ] of the bank
@admin.route("/show_loan_choices", methods=['GET', 'POST'])
def show_loan_choices():
    page = request.args.get('page', 1, type=int)
    loans = LoanDetails.query.paginate(page=page, per_page=3)
    return render_template('show_all_provided_loans.html', loans=loans)

# add new insurance detail for choices [ personal loan, education loan ] of the bank
@admin.route("/show_insurance_choices", methods=['GET', 'POST'])
def show_insurance_choices():
    page = request.args.get('page', 1, type=int)
    insurances = InsuranceDetails.query.paginate(page=page, per_page=3)
    return render_template('show_all_provided_insurances.html', insurances=insurances)

# add new bank member role of the bank
@admin.route("/add-bank-role", methods=['GET', 'POST'])
def member_role_list():
    form = AddMemberRole()
    if form.validate_on_submit():
        role_name = form.role_name.data
        role = MemberRole.query.filter_by(member_role=role_name).first()
        if role:
            flash("this role is already exist", 'danger')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            add_role = MemberRole(member_role=role_name)
            db.session.add(add_role)
            db.session.commit()
            flash("new role has been added", 'success')
            return redirect(url_for('admin.admin_dashboard'))

    return render_template('add_member_role_list.html', title='add-member-role-list', form=form)

# add new loan detail for choices [ personal loan, education loan ] of the bank
@admin.route("/add-loan-options", methods=['GET', 'POST'])
def loan_choices():
    form = LoanChoice()
    if form.validate_on_submit():
        loan_choice = form.loan_choice.data
        loan = LoanDetails.query.filter_by(loan_name=loan_choice).first()
        if loan:
            flash("this loan is already exist", 'danger')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            add_loan = LoanDetails(loan_name=loan_choice)
            db.session.add(add_loan)
            db.session.commit()
            flash("new loan detail has been added", 'success')
            return redirect(url_for('admin.admin_dashboard'))

    return render_template('add_loan_choice_list.html', title='add-loan-choice-list', form=form)

# add new insurance detail for choices [ personal loan, education loan ] of the bank
@admin.route("/add-insurance-options", methods=['GET', 'POST'])
def insurance_choices():
    form = InsuranceChoice()
    if form.validate_on_submit():
        insurance_choice = form.insurance_choice.data
        insurance = InsuranceDetails.query.filter_by(insurance_name=insurance_choice).first()
        if insurance:
            flash("this insurance is already exist", 'danger')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            add_insurance = InsuranceDetails(insurance_name=insurance_choice)
            db.session.add(add_insurance)
            db.session.commit()
            flash("new insurance detail has been added", 'success')
            return redirect(url_for('admin.admin_dashboard'))

    return render_template('add_insurance_choice_list.html', title='add-loan-choice-list', form=form)


@admin.route("/delete",methods=["POST","GET"])
def delete():
    for getid in request.form.getlist('checkdelete'):
        print(getid)
        MemberRole.query.filter_by(id=getid).delete()
        db.session.commit()
    return jsonify('Records deleted successfully')

