from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, RadioField, \
    TextAreaField, FileField, EmailField
from wtforms.validators import DataRequired, Email


# login form for the admin
class LoginForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login IN')


# change the account status for the bank user
class UserAccountStatus(FlaskForm):
    user_id = StringField('User_id', validators=[DataRequired()], render_kw={'readonly': True})
    user_name = StringField('User_name', validators=[DataRequired()], render_kw={'readonly': True})
    account_number = StringField('Account_number', validators=[DataRequired()], render_kw={'readonly': True})
    account_status = RadioField('Account status', choices=[('1', 'Inactive'), ('2', 'Active')])
    submit = SubmitField('Submit the changes')


# loan approving for the bank user through admin panel only
class LoanApprovalStatus(FlaskForm):
    user_id = StringField('User_id', validators=[DataRequired()], render_kw={'readonly': True})
    user_name = StringField('User name', validators=[DataRequired()], render_kw={'readonly': True})
    loan_id = StringField('Loan id', validators=[DataRequired()], render_kw={'readonly': True})
    loan_amount = StringField('Loan amount', validators=[DataRequired()], render_kw={'readonly': True})
    rate_interest = StringField('Rate interest', validators=[DataRequired()], render_kw={'readonly': True})
    paid_amount = StringField('Paid amount', validators=[DataRequired()], render_kw={'readonly': True})
    loan_type = StringField('Loan type', validators=[DataRequired()], render_kw={'readonly': True})
    loan_status = StringField('Loan status', validators=[DataRequired()], render_kw={'readonly': True})
    approval_status = RadioField('Approval status', choices=[('1', 'Approve'), ('2', 'Decline')])
    submit = SubmitField('Submit the changes')


# approve insurance request which is sent by bank user
class insurance_approval_form(FlaskForm):
    user_id = StringField('User_id', validators=[DataRequired()], render_kw={'readonly': True})
    user_name = StringField('User name', validators=[DataRequired()], render_kw={'readonly': True})
    insurance_id = StringField('Insurance id', validators=[DataRequired()], render_kw={'readonly': True})
    insurance_amount = StringField('Insurance amount', validators=[DataRequired()], render_kw={'readonly': True})
    insurance_type = StringField('Insurance type', validators=[DataRequired()], render_kw={'readonly': True})
    insurance_status = StringField('Insurance status', validators=[DataRequired()], render_kw={'readonly': True})
    approval_status = RadioField('Approval status', choices=[('1', 'Approve'), ('2', 'Decline')])
    submit = SubmitField('Submit the changes')


# add new branch of bank
class AddBranch(FlaskForm):
    branch_name = StringField('branch name: ', validators=[DataRequired()])
    branch_address = StringField('Branch addresses: ', validators=[DataRequired()])
    submit = SubmitField('Add this branch')


# admin can add new atm of the bank
class AddAtm(FlaskForm):
    atm_address = StringField('Atm address: ', validators=[DataRequired()])
    submit = SubmitField('Add this atm')


# about bank member data
class BankMemberData(FlaskForm):
    image_file = FileField('add photo: ', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    bank_member_name = StringField('Member name: ', validators=[DataRequired()])
    bank_member_position = RadioField('Member Position', choices=[('CEO', 'CEO'),
                                                              ('CTO', 'CTO'),
                                                              ('Accountant', 'Accountant'),
                                                              ('Main Leader', 'Main leader')])
    bank_member_about = TextAreaField('about member', validators=[DataRequired()])
    bank_member_email_id = EmailField('Email id', validators=[DataRequired()])
    bank_member_contact = IntegerField('Contact number', validators=[DataRequired()])

    submit = SubmitField('Update the members')
