from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.fields.html5 import DateField,DateTimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from model.models import User 
from datetime import date


class LoginForm(FlaskForm):
	username= StringField("username", validators=[DataRequired()])
	password= StringField("password", validators=[DataRequired()])
	remember_me= BooleanField("remember Me")
	submit= SubmitField("Sign In")


class SignUpForm(FlaskForm):
	username= StringField("username", validators=[DataRequired()])
	email = StringField("email",validators=[DataRequired(),Email()])
	password= StringField("password", validators=[DataRequired()])
	password2= StringField("repeate password", validators=[DataRequired(),EqualTo("password")])
	remember_me= BooleanField("remember Me")
	submit= SubmitField("Sign In")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError("Please use a different user name")

	def validate_email(self,email):
		user =User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError("Please use a different email")

	
class Create_camp(FlaskForm):
	name = StringField("How is the Camp called?", validators=[DataRequired()])
	location=StringField("Where will the camp be?", validators=[DataRequired()])
	group = StringField("What is the name of you Scouting Group?", validators=[DataRequired()])
	start_date= DateField("When does the Camp starts")
	end_date= DateField("and when does it end?")
	key = StringField("Private Key",validators=[DataRequired()])
	submit= SubmitField("Create Camp")

	def validate_end_date(self,end_date):
		if end_date.data is not None or self.start_date.data is not None:
			if end_date.data < self.start_date.data:
				raise ValidationError("End date must not be earlier than start date.")
		else:
			raise ValidationError("Dates must not be empty.")	
	def validate_key(self,key):
		if (len(key.data)<8):
			raise ValidationError("your private key needs to have at least 8 characters")

class Create_car(FlaskForm):
	number_of_seats =IntegerField("Number of available seats:",validators=[DataRequired()])
	starting_location = StringField("Starting location:",validators=[DataRequired()])
	submit= SubmitField("Post Car")