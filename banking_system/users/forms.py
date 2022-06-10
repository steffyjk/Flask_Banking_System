from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from banking_system.models import User

#used in banking system
class RegistrationForm(FlaskForm):
	user_name = StringField('Username: ', validators=[DataRequired(), Length(min=2, max=20)])
	user_email = StringField('Email: ', validators=[DataRequired(), Email()])
	user_phone_number = IntegerField('Phone number: ', validators=[DataRequired(), Length(10)])
	user_first_name = StringField('First name: ', validators=[DataRequired()])
	user_last_name =  StringField('Last name: ', validators=[DataRequired()])
	user_address =  StringField('Address: ', validators=[DataRequired()])
	user_age = IntegerField('Age: ', validators=[DataRequired(), Length(10)])
	date_of_birth = DateField('Date of birth', format='%Y-%m-%d' )
	# role = 'user'
	user_password = PasswordField('Password', validators= [DataRequired()])
	confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('user_password')])
	submit = SubmitField('Sign Up')

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken please Choose differnt one')

	def validate_email(self,email):
		email = User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError('That email is taken please Choose differnt one')

class LoginForm(FlaskForm):
	user_email = StringField('Email',validators=[DataRequired(), Email()])
	user_password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login IN')
