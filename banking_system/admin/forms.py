from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, RadioField, \
    TextAreaField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login IN')


class UserAccountStatus(FlaskForm):
    user_id = StringField('User_id', validators=[DataRequired()], render_kw={'readonly': True})
    user_name = StringField('User_name', validators=[DataRequired()], render_kw={'readonly': True})
    account_number = StringField('Account_number', validators=[DataRequired()], render_kw={'readonly': True})
    account_status = RadioField('Account status', choices=[('1', 'Inactive'), ('2', 'Active')])
    submit = SubmitField('Submit the changes')


class loan_approval_status(FlaskForm):
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

class insurance_approval_form(FlaskForm):
    user_id = StringField('User_id', validators=[DataRequired()], render_kw={'readonly': True})
    user_name = StringField('User name', validators=[DataRequired()], render_kw={'readonly': True})
    insurance_id = StringField('Insurance id', validators=[DataRequired()], render_kw={'readonly': True})
    insurance_amount = StringField('Insurance amount', validators=[DataRequired()], render_kw={'readonly': True})
    insurance_type = StringField('Insurance type', validators=[DataRequired()], render_kw={'readonly': True})
    insurance_status = StringField('Insurance status', validators=[DataRequired()], render_kw={'readonly': True})
    approval_status = RadioField('Approval status', choices=[('1', 'Approve'), ('2', 'Decline')])
    submit = SubmitField('Submit the changes')


class AddBranch(FlaskForm):
    branch_name = StringField('branch name: ', validators=[DataRequired()])
    branch_address = StringField('Branch addresses: ', validators=[DataRequired()])
    submit = SubmitField('Add this branch')


class AddAtm(FlaskForm):
    atm_address = StringField('Atm address: ', validators=[DataRequired()])
    submit = SubmitField('Add this atm')
