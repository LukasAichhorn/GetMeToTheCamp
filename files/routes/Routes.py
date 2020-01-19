from flask import render_template # for showing tempalte html files from the template Folder
from flask import flash,redirect,request,url_for
from home import app, db, bootstrap,login #get app variable flask is associated
from files import templates #implement html structures
from files import mockData	#importing file with mock data objects
from templates.forms.form_login import LoginForm, SignUpForm, Create_camp, Create_car #getting all login form objects from the LoginForm class
from flask_login import current_user, login_user , login_required,logout_user
from model.models import User,Car,Camp,Seat,ReservationReq
from werkzeug.urls import url_parse
from flask_nav import Nav
from flask_nav.elements import Navbar,View
import sys

def get_notification_count():
	if current_user.is_authenticated:
		notifs = ReservationReq.query.filter(ReservationReq.requestor_id == current_user.id or ReservationReq.owner_id == current_user.id).all()
		count = str(len(notifs))
		return count



@app.route('/', methods=["GET","POST"])
@app.route('/index',methods=["GET","POST"])
def index():
	count =get_notification_count()
	form=Create_camp()
	all_camps = Camp.query.all()

	if form.validate_on_submit():
		
		camp= Camp(owner_id = current_user.id,name=form.name.data,group=form.group.data,location= form.location.data,start_date=form.start_date.data,end_date=form.end_date.data,key=form.key.data)
		db.session.add(camp)
		db.session.commit()
		flash("Congrats you successfully created a camp")
		newAddedCampId=Camp.query.order_by(Camp.id.desc()).first()
		return redirect(url_for("camp",campId=newAddedCampId.id))

	
	if request.method == "GET":
		all_camps = Camp.query.all()

		return render_template("index.html",form=form,all_camps=all_camps,notif_c=count)
		
	return render_template("index.html",form=form,all_camps=all_camps)




@app.route('/login',methods =["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("index"))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash("Invalid username or password")
			return redirect(url_for("login"))
		
		login_user(user,remember= form.remember_me.data)

		next_page = request.args.get("next")
		if not next_page or url_parse(next_page).netloc !='':
			next_page= url_for("index")

		return redirect(next_page)

	return render_template("login.html", form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for("index"))


@app.route("/camp/<campId>",methods =["GET","POST"])
@login_required
def camp(campId):
	count =get_notification_count()
	form= Create_car()
	#insert form with submit button
	camp = Camp.query.filter_by(id=campId).first()
	cars= Car.query.filter_by(linked_camp=campId).all()
	
	seats=Seat.query.join(Car).filter_by(linked_camp=campId).all()
	
	if form.validate_on_submit():
		car =Car(number_of_seats=form.number_of_seats.data,starting_location=form.starting_location.data,owner_id=current_user.id,linked_camp=campId)
		db.session.add(car)
		db.session.commit()
		related_car=Car.query.order_by(Car.id.desc()).first()
		seats_list=list()
		for seat in range(form.number_of_seats.data):
			seat=Seat(related_car=related_car.id)
			seats_list.append(seat)

		db.session.add_all(seats_list)
		db.session.commit()	
		flash("Congrats you successfully posted a Car")
		return redirect(url_for("camp",campId = campId))
	
	if request.method == "GET":
		camp = Camp.query.filter_by(id=campId).first()
		cars= Car.query.filter_by(linked_camp=campId).all()	
		seats=Seat.query.join(Car).filter_by(linked_camp=campId).all()
		return render_template("camp.html",camp=camp,cars=cars,form=form,seats=seats,notif_c=count)

	return render_template("camp.html",camp=camp,cars=cars,form=form,seats=seats)

@app.route("/signin", methods =["GET","POST"])
def signIn():

	if current_user.is_authenticated:
		return redirect(url_for("index"))

	form = SignUpForm()
	if form.validate_on_submit():
		user =User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("Congrats you successfully created your account, please login")
		return redirect(url_for("login"))

	return render_template("signIn.html",form=form)


@app.route('/profile/<username>')
@login_required
def profile(username):
	count =get_notification_count()
	user = User.query.filter_by(username=username).first_or_404()
	user_camps = Camp.query.filter_by(owner_id=user.id).all()
	cars = Car.query.filter_by(owner_id=user.id).all()
	seats = Seat.query.join(Car).filter_by(owner_id=user.id).all()
	notifications = ReservationReq.query.all()

	



	return render_template("profile.html",reqs=notifications,user = user, cars= cars,seats=seats,user_camps=user_camps, notif_c=count)

@app.route("/delete/<table>/<elem_id>")
@login_required
def delete(table,elem_id):
	print("delete request for table:" + table + "with id:"+ elem_id, file=sys.stderr)

	if table == "Car":
		car = Car.query.filter_by(id=elem_id).first()
		print(car , file=sys.stderr)
		associated_seats = Seat.query.join(Car).filter_by(id=car.id).all() 
		for seat in associated_seats:
			print("I delete Seat id.nr:"+ str(seat.id), file=sys.stderr)
			associated_Req=ReservationReq.query.filter_by(seat_id=seat.id).first()
			if associated_Req:
				db.session.delete(associated_Req)

			db.session.delete(seat)
			db.session.commit()

		print("I delete Car id.nr:"+str(car.id), file=sys.stderr)
		db.session.delete(car)
		db.session.commit()	

	if table == "Seat":
		seat = Seat.query.filter_by(id=elem_id).first()
		related_Req = ReservationReq.query.filter_by(seat_id=seat.id).first()
		db.session.delete(related_Req)
		db.session.delete(seat)
		db.session.commit()


	if table =="Camp":		
		camp = Camp.query.filter_by(id=elem_id).first()
		associated_cars= Car.query.join(Camp).filter_by(id=camp.id).all()

		for car in associated_cars:
			associated_seats= Seat.query.join(Car).filter_by(id=car.id).all()
			for seat in associated_seats:
				print("I delete seat with id.nr: "+str(seat.id), file=sys.stderr)
				associated_Req=ReservationReq.query.filter_by(seat_id=seat.id).first()
				if associated_Req:
					db.session.delete(associated_Req)

				db.session.delete(seat) 
				db.session.commit()

			print("I delete car with id.nr: "+str(car.id), file=sys.stderr)	
			db.session.delete(car)
			db.session.commit()
		print("I delete Camp with id.nr: "+str(camp.id), file=sys.stderr)
		db.session.delete(camp)
		db.session.commit()	

	if table == "ReservationReq":
		row=ReservationReq.query.filter_by(id=elem_id).first()
		db.session.delete(row)
		db.session.commit()


	return redirect(request.headers.get("Referer"))				
	#return redirect(url_for("profile",username=current_user.username))

@app.route("/update/<table>/<elem_id>")
@login_required
def update(table,elem_id):

	if table == "Seat":

		a_seat = Seat.query.filter_by(id=elem_id).first()
		a_seat.available = False
		a_seat.reserved = True
		db.session.commit()

		#create reservationReqEntry
		requestor_id=current_user.id
		seatOwner=Car.query.filter_by(id=a_seat.related_car).first()
		newReservationReq=ReservationReq(seat_id=a_seat.id,requestor_id=requestor_id,owner_id=seatOwner.id)
		db.session.add(newReservationReq)
		db.session.commit()

	if table == "ReservationReq":
		a_reservation = ReservationReq.query.filter_by(id=elem_id).first()
		related_seat = Seat.query.filter_by(id=a_reservation.seat_id).first()
		if a_reservation.status_pending:
			a_reservation.status_accepted= True
			a_reservation.status_pending=False
			related_seat.reserved=False
			related_seat.taken=True
			db.session.commit()
			flash("You set reservation status to accepted")
		else:
			flash("something went wrong")



	return redirect(request.headers.get("Referer"))

