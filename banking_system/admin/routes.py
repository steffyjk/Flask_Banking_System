from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required, login_manager
from banking_system import db, bcrypt
from banking_system.models import Atm, User, Branch, BankDetails, Account, Loan, LoanType
from banking_system.admin.forms import AddBranch, LoginForm, AddAtm, UserAccountStatus
from flask import Blueprint

admin = Blueprint('admin', __name__)


@admin.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email='steffy.inexture@gmail.com').first()
        if user is not None and form.user_password.data == user.user_password:
            login_user(user, remember=form.remember.data)

            flash('admin Login successfully..', 'success')
            users = User.query.order_by(User.user_id.desc())
            atms = Atm.query.order_by(Atm.atm_id.desc())
            branchs = Branch.query.order_by(Branch.branch_id.desc())
            return render_template('admin_dashboard.html', users=users, branchs=branchs, atms=atms)
        else:
            flash('Login unsuccessfully..please check email and password', 'danger')
    return render_template('admin_login.html', title='login', form=form)


@admin.route("/admin_dashboard", methods=['GET', 'POST'])
def admin_dashboard():
    users = User.query.all()
    accounts = Account.query.all()
    atms = Atm.query.order_by(Atm.atm_id.desc())
    branchs = Branch.query.order_by(Branch.branch_id.desc())
    return render_template('admin_dashboard.html', users=users, branchs=branchs, atms=atms, accounts=accounts)


@admin.route("/all-user-data", methods=['GET', 'POST'])
def admin_user_data():
    users = User.query.all()
    accounts = Account.query.all()
    return render_template('admin_user_data.html', users=users, accounts=accounts)


@admin.route("/all-branch-data", methods=['GET', 'POST'])
def admin_branch_data():
    branchs = Branch.query.order_by(Branch.branch_id.desc())
    return render_template('admin_branch_data.html', branchs=branchs)


@admin.route("/all-atm-data", methods=['GET', 'POST'])
def admin_atm_data():
    atms = Atm.query.order_by(Atm.atm_id.desc())
    return render_template('admin_atm_data.html', atms=atms)


@admin.route("/all-loan-data", methods=['GET', 'POST'])
def admin_user_loan_data():
    user = User.query.all()
    loans = Loan.query.all()
    loantype = LoanType.query.all()
    return render_template('admin_user_loan_data.html', loans=loans, loantype=loantype, user=user)

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
        flash(f'{user_name}s account status has been changed', 'success')
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


@admin.route("/add_branch", methods=['GET', 'POST'])
def add_branch():
    form = AddBranch()
    if form.validate_on_submit():
        table_branch = Branch.query.filter_by(branch_name=form.branch_name.data).first()
        if table_branch:
            flash('this branch has already exist!', 'danger')
            return redirect(url_for('admin.add_branch'))
        else:
            bank = BankDetails.query.all()
            # print("$$$$$$$$$$$$$$$$$",bank[0])
            branch = Branch(
                branch_name=form.branch_name.data,
                branch_address=form.branch_address.data,
                bank_id=bank[0].bank_id
            )
            db.session.add(branch)
            try:
                db.session.commit()
                flash(f'branch is added successfully', 'success')
                return redirect(url_for('admin.admin_dashboard'))
            except Exception as e:
                flash(f'{e}', 'danger')
    return render_template('add_branch.html', title='add-branch', form=form)


@admin.route("/add_atm", methods=['GET', 'POST'])
def add_atm():
    form = AddAtm()
    if form.validate_on_submit():
        table_atm = Atm.query.filter_by(atm_address=form.atm_address.data).first()
        if table_atm:
            flash('Atm has already exist at this area!', 'danger')
            return redirect(url_for('admin.add_atm'))
        else:
            bank = BankDetails.query.all()
            # print("$$$$$$$$$$$$$$$$$",bank[0])
            atm = Atm(
                atm_address=form.atm_address.data,
                bank_id=bank[0].bank_id
            )
            db.session.add(atm)
            try:
                db.session.commit()
                flash(f'Atm is added successfully', 'success')
                return redirect(url_for('admin.admin_dashboard'))
            except Exception as e:
                flash(f'{e}', 'danger')
    return render_template('add_atm.html', title='add-atm', form=form)
