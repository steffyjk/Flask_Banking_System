from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from banking_system.models import User
# from validate_email import validate_email

from datetime import datetime

# string_input_with_date = "25/10/2017"
# past = datetime.strptime(string_input_with_date, "%d/%m/%Y")


#used in banking system
class RegistrationForm(FlaskForm):
	user_name = StringField('Username: ', validators=[DataRequired(), Length(min=2, max=20)])
	user_email = StringField('Email: ', validators=[DataRequired(), Email()])
	user_phone_number = StringField('Phone number: ', validators=[DataRequired()])
	user_first_name = StringField('First name: ', validators=[DataRequired()])
	user_last_name =  StringField('Last name: ', validators=[DataRequired()])
	user_address =  StringField('Address: ', validators=[DataRequired()])
	user_age = IntegerField('Age: ', validators=[DataRequired()])
	date_of_birth = DateField('Date of birth', format='%Y-%m-%d' )
	# role = 'user'
	user_password = PasswordField('Password', validators= [DataRequired()])
	confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('user_password')])
	submit = SubmitField('Sign Up')
	

	def validate_user_name(self,user_name):
		user = User.query.filter_by(user_name=user_name.data).first()
		if user:
			raise ValidationError('That username is taken please Choose differnt one')

	def validate_user_email(self,user_email):
		email = User.query.filter_by(user_email=user_email.data).first()
		if email:
			raise ValidationError('That email is taken please Choose differnt one')

	def validate_user_age(self,user_age):
		if (user_age.data)<=0:
			raise ValidationError('Age must be > 0 ')

	# def validate_date_of_birth(self,date_of_birth):
	# 	present = datetime.now()
	# 	dob = date_of_birth.data
	# 	print()
	# 	print("################################")
	# 	print(dob)
	# 	present = datetime.now()
	# 	# print(dob.date)
	# 	dob.date() < present.date()
	# 	if dob.date()>present.date() :
			# raise ValidationError('date must be valid brth date')



	def validate_user_phone_number(self,user_phone_number):
		print("########################")
		# print(user_phone_number.value)
		print(len(str(user_phone_number)))
		if len(user_phone_number.data)!=10:
			raise ValidationError('Phone number must be 10 digits only')

class LoginForm(FlaskForm):
	user_email = StringField('Email',validators=[DataRequired(), Email()])
	user_password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login IN')

class UpdateAccountForm(FlaskForm):
	user_name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	
	submit = SubmitField('Update',)

	def validate_user_name(self,user_name):
		if user_name.data != current_user.user_name:
			user = User.query.filter_by(user_name=user_name.data).first()
			if user:
				raise ValidationError('That username is taken please Choose differnt one')


class RequestResetForm(FlaskForm):
	user_email = StringField('Email',validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self,user_email):
		user = User.query.filter_by(user_email= user_email.data).first()
		if user is None:
			raise ValidationError('There is no account with that email. YOu must register first! ')


class ResetPasswordForm(FlaskForm):
	user_password = PasswordField('Password', validators= [DataRequired()])
	confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password',)


