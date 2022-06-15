from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from banking_system.models import User

class LoginForm(FlaskForm):
	user_email = StringField('Email',validators=[DataRequired(), Email()])
	user_password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login IN')

class AddBranch(FlaskForm):
	branch_name = StringField('branch name: ',validators=[DataRequired()])
	branch_address = StringField('Branch addresss: ',validators=[DataRequired()])
	submit = SubmitField('Add this branch')