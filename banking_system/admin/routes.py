
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required, login_manager
from banking_system import db, bcrypt
from banking_system.models import User, Branch, Atm
from banking_system.admin.forms import AddBranch, LoginForm
from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route("/admin_login", methods = ['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email='steffy.inexture@gmail.com').first()
        if user is not None and form.user_password.data == user.user_password:
            # print(user,"######")        
            login_user(user, remember=form.remember.data)

            flash('admin Login successfully..', 'success')
            # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
            users = User.query.order_by(User.user_id.desc())
            branchs = Branch.query.order_by(Branch.branch_id.desc())
            atms = Atm.query.order_by(Atm.atm_id.desc())
            return render_template('admin_dashboard.html', users = users, branchs =branchs,atms=atms)
        else:
            flash('Login unsuccessfull..please check email and password', 'danger')
    return render_template('admin_login.html', title='login', form=form)

@admin.route("/admin_dashboard", methods = ['GET', 'POST'])
def admin_dashboard():
    users = User.query.all()
    branchs = Branch.query.order_by(Branch.branch_id.desc())
    atms = Atm.query.order_by(Atm.atm_id.desc())
    return render_template('admin_dashboard.html', title='admin_dashboard',users=users,branchs=branchs,atms=atms)

@admin.route("/add_branch", methods = ['GET', 'POST'])
def add_branch():
    form = AddBranch()
    if form.validate_on_submit():
        branch = Branch(branch_name=form.branch_name.data,branch_address=form.branch_address.data)
        db.session.add(branch)
        try:
            db.session.commit()    
            flash(f'branch is added successfully', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f'{e}','danger')
    return render_template('add_branch.html',title='add-branch',form=form)

