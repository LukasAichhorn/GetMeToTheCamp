from home import db
from home import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



@login.user_loader
def load_user(id):
	return User.query.get(int(id))


class User(UserMixin,db.Model):
	id = db.Column(db.Integer,primary_key = True)
	username = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	password_hash = db.Column(db.String(128))
	owned_car = db.relationship("Car",backref="car_owner",lazy="dynamic")
	owned_camp= db.relationship("Camp",backref="camp_owner",lazy="dynamic")


	assigned_seat=db.Column(db.Integer, db.ForeignKey("seat.id"))

	def set_password(self,password):
		self.password_hash=generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password_hash,password)

	def __repr__(self):
		return "<Username: {}>".format(self.username)


class Camp(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	owner_id = db.Column(db.Integer,db.ForeignKey("user.id"))
	name = db.Column(db.String(128), index = True)
	group =db.Column(db.String(64), index = True)
	location= db.Column(db.String(128), index = True)
	start_date= db.Column(db.DateTime, index = True,nullable = True )
	end_date= db.Column(db.DateTime, index = True,nullable = True )
	key = db.Column(db.String(8), index = True, unique = True)
	linked_car = db.relationship("Car",backref="car_id",lazy="dynamic")



	def __repr__(self):
		return "<CampName{} ".format(self.name) + " group:{} ".format(self.group) +" key:{}>".format(self.key)

class Car(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	number_of_seats = db.Column(db.Integer)
	starting_location = db.Column(db.String(140))
	owner_id= db.Column(db.Integer,db.ForeignKey("user.id"))
	seats = db.relationship("Seat",backref="seat_id",lazy="dynamic")
	
	linked_camp = db.Column(db.Integer,db.ForeignKey("camp.id"))	

	def __repr__(self):
		return "<Car=> Owner:{} ".format(self.owner_id, self.number_of_seats) + "Seats:{} ".format(self.number_of_seats)


class Seat(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	available = db.Column(db.Boolean(),default = True)
	reserved = db.Column(db.Boolean(),default = False)
	taken= db.Column(db.Boolean(),default = False)

	related_car = db.Column(db.Integer, db.ForeignKey("car.id"))
	related_user = db.relationship("User",backref="user_id",lazy="dynamic")

	
	def __repr__(self):
			return "<Seat=> Related Car {} >".format(self.related_car)	

class ReservationReq(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	requestor_id= db.Column(db.Integer,db.ForeignKey("user.id"))
	owner_id=db.Column(db.Integer,db.ForeignKey("user.id"))
	status_pending=db.Column(db.Boolean(),default = True)
	status_accepted=db.Column(db.Boolean(),default = False)
	seat_id=db.Column(db.Integer,db.ForeignKey("seat.id"))
	requestor = db.relationship("User", foreign_keys=[requestor_id])
	owner = db.relationship("User", foreign_keys=[owner_id])
	seat=db.relationship("Seat", foreign_keys=[seat_id])