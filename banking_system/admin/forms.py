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
    user_id = StringField('User_id', validators=[DataRequired()])
    user_name = StringField('User_name', validators=[DataRequired()])
    account_number = StringField('Account_number', validators=[DataRequired()])
    account_status = RadioField('Account status', choices=[('1', 'Inactive'), ('2', 'Active')])
    submit = SubmitField('Submit the changes')


class AddBranch(FlaskForm):
    branch_name = StringField('branch name: ', validators=[DataRequired()])
    branch_address = StringField('Branch addresses: ', validators=[DataRequired()])
    submit = SubmitField('Add this branch')

class AddAtm(FlaskForm):
    atm_address = StringField('Atm address: ', validators=[DataRequired()])
    submit = SubmitField('Add this atm')
