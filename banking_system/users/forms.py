from flask import flash
from jinja2 import pass_eval_context
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from banking_system.models import Account, User
from validate_email_address import validate_email


# used in banking system
class RegistrationForm(FlaskForm):
    user_name = StringField('Username: ', validators=[DataRequired(), Length(min=2, max=20)])
    user_email = StringField('Email: ', validators=[DataRequired(), Email()])
    user_phone_number = IntegerField('Phone number: ', validators=[DataRequired()])
    user_first_name = StringField('First name: ', validators=[DataRequired()])
    user_last_name = StringField('Last name: ', validators=[DataRequired()])
    user_address = StringField('Address: ', validators=[DataRequired()])
    user_age = IntegerField('Age: ', validators=[DataRequired()])
    date_of_birth = DateField('Date of birth', format='%Y-%m-%d')
    # role = 'user'
    user_password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('user_password')])
    submit = SubmitField('Sign Up')

    def validate_user_name(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).first()
        if user:
            raise ValidationError('That username is taken please Choose different one')

    # def validate_user_email(self,user_email):

    # if not isExists:
    # raise ValidationError('Email address does not exist')

    def validate_user_email(self, user_email):
        # isExists = validate_email('user_email.data', verify=True)
        # print("#########################",isExists)
        email = User.query.filter_by(user_email=user_email.data).first()
        if email:
            raise ValidationError('That email is taken please Choose different one')
    # elif isExists:
    # 	pass
    # else:
    # 	raise ValidationError('Email id does not exist')


class LoginForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login IN')


class UpdateAccountForm(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    user_email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'readonly': True})
    submit = SubmitField('Update', )

    def validate_username(self, user_name):
        if user_name.data != current_user.user_name:
            user = User.query.filter_by(user_name=user_name.data).first()
            if user:
                raise ValidationError('That username is taken please Choose different one')

    def validate_email(self, user_email):
        if user_email.data != current_user.user_email:
            user_email = User.query.filter_by(user_email=user_email.data).first()
            if user_email:
                raise ValidationError('That email is taken please Choose different one')


class RequestResetForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, user_email):
        user = User.query.filter_by(user_email=user_email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. YOu must register first! ')


class ResetPasswordForm(FlaskForm):
    user_password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password', )


class AddMoney(FlaskForm):
    reciver_account = IntegerField('Enter receiver account number: ', validators=[DataRequired()])
    credit_amount = IntegerField('Amount you wanna add: ', validators=[DataRequired()])
    user_password = PasswordField('Enter Password', validators=[DataRequired()])
    submit = SubmitField('Credit the balance', )

    def validate_reciver_account(self, reciver_account):
        account = Account.query.filter_by(account_number=reciver_account.data).first()
        if account:
            pass
        else:
            raise ValidationError('No account is exist in this number')


class WithdrawMoney(FlaskForm):
    reciver_account = IntegerField('Enter receiver account number: ', validators=[DataRequired()])
    credit_amount = IntegerField('Amount you wanna add: ', validators=[DataRequired()])
    user_password = PasswordField('Enter Password', validators=[DataRequired()])
    submit = SubmitField('Credit the balance', )

    def validate_reciver_account(self, reciver_account):
        account = Account.query.filter_by(account_number=reciver_account.data).first()
        if account:
            pass
        else:
            raise ValidationError('No account is exist in this number')

    def validate_user_password(self, user_password):
        if user_password != current_user.user_password:
            raise ValidationError('Incorrect password')


class MoveToSavingBalance(FlaskForm):
    amount = IntegerField('Select the amount you wanna add: ', validators=[DataRequired()])
    user_password = PasswordField('Enter Password', validators=[DataRequired()])
    submit = SubmitField('Credit the balance', )

    def validate_amount(self, amount):
        account = Account.query.filter_by(user_id=current_user.user_id)
        if account.account_balance < amount:
            raise ValidationError('Insufficient balance !')

    def validate_user_password(self, user_password):
        if user_password != current_user.user_password:
            raise ValidationError('Incorrect password')


class MoveToAccountBalance(FlaskForm):
    amount = IntegerField('Select the amount you wanna add: ', validators=[DataRequired()])
    user_password = PasswordField('Enter Password', validators=[DataRequired()])
    submit = SubmitField('Credit the balance', )

    def validate_amount(self, amount):
        account = Account.query.filter_by(user_id=current_user.user_id)
        if account.account_balance < amount:
            raise ValidationError('Insufficient balance !')

    def validate_user_password(self, user_password):
        if user_password != current_user.user_password:
            raise ValidationError('Incorrect password')
