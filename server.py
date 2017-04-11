"""ParkerSpace."""
from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify, Response)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, connect_to_db, db, Parking_location, User_history, Rating

import logging

from geopy.geocoders import Nominatim

from geopy.distance import vincenty

from helper import closest_garage

import geocoder





app = Flask(__name__, static_url_path='/templates/assets')

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    # a = jsonify([1,3])
    return render_template("homepage.html", garages=[])


@app.route("/users")
def user_list():
    """Show list of users."""

    user = User.query.all()

    return render_template("user_list.html", user=user)


@app.route("/garages")
def search_list():

    address = request.args.get('address') 
    print "Address: ", address 
    #putting in comma will print since different datatypes cannot be concatenated 
    location = geocoder.google(address).latlng

    print "Location: ", location
    print(location[0], location[1])

    garages = Parking_location.query.all()
    print "Garages:", garages

    results = closest_garage(garages, location)
    print(len(results))
    print "Restuls", results
    
    garage_data = [garage.address for garage in results]
    # return jsonify(results=garage_data)
    return render_template("garage_list.html", garages=results)






@app.route("/users/<user_id>")
def user_info(user_id):
    """Show user and ratings."""

    user = User.query.filter(User.user_id == user_id).one()
    
    if not user:
        flash('error, this is the wrong input')

    user_history = User_history.query.filter(User_history.user_id == user_id)
    rating = []
    for history in user_history:
        parking_location = Parking_location.query.get(history.parking_id)
        score = Rating.query.filter(Rating.user_id == history.user_id).filter(Rating.parking_id== history.parking_id).one()
        rating.append(dict(location=parking_location, date=history.parking_date, score=score.score))

    print rating
    return render_template("user_detail.html", 
                                    scores=rating,
                                    user=user
                                    )


# @app.route("/garages")
# def garage_list():
#     """Show list of garages."""

#     print "About to query for parking location"
#     parking_locations = Parking_location.query.all()
    
#     print "about to render template"
#     return render_template("garage_list.html", parking_locations=parking_locations)



@app.route("/garage_rating", methods=['POST'])
def add_new_rating():
    """Add new rating to garages."""
    rating = request.form.get("rating")
    parking_id = request.form.get("parking")
    user_id = request.form.get("user")

    existing_rating = (Rating.query.filter(Rating.parking_id ==parking_id,
                        Rating.user_id == user_id).first())
    if existing_rating:
        flash('You have successfully updated your rating!')
        existing_rating.score = int(rating)
    else:
        new_rating = Rating(parking_id=parking_id, 
                            user_id=user_id, score=rating)
        db.session.add(new_rating)
        flash('You have successfully added a new rating!')
    db.session.commit()  

    return redirect('garages/' + str(parking_id))


@app.route("/garages/<parking_id>")
def garage_details(parking_id):
    """Show garage details."""

    garage = Parking_location.query.filter(Parking_location.parking_id == parking_id).one()
    user_rating_score = None

    if session['logged_in']:
        user_rating = Rating.query.filter(Rating.parking_id == garage.parking_id, Rating.user_id == session['logged_in'])
        if user_rating.count():
            user_rating_score = user_rating.one().score

    if len(garage.rating):
        overall_rating = float(sum(rating.score for rating in garage.rating))/len(garage.rating)
    else:
        overall_rating = 0
    # print [rating.score for rating in garage.rating]
    return render_template("garage_details.html", 
                                    garage=garage,
                                    overall_rating=overall_rating,
                                    user_rating=user_rating_score) 

@app.route("/map_data", methods=['GET'])
def map_data():
    parking_locations = Parking_location.query.all()
    data = []
    for location in parking_locations:
        coordinates=dict(lat=location.latitude, lng=location.longitude)
        data.append(dict(id=location.parking_id, coordinates=coordinates))
    return jsonify(data=data)


@app.route("/chart/<user_id>", methods=['GET'])
def chart(user_id):

    user_histories = User_history.query.filter(User_history.user_id == user_id)
    #creating array of 12 0's for 12 months
    data = [0]*12
    for history in user_histories:
        month = history.parking_date.month 
        #index starts from 0 so we are subtracting 1
        data[month-1]+= 1
        # print history.parking_date
    return jsonify(data=data)


@app.route("/record_parking", methods=['POST'])
def record_parking():
    """records parking date"""

    date = request.form.get("parking_date")
    parking_id = request.form.get("parking_id")
    user_id = request.form.get("user")

    new_history = User_history(parking_id=parking_id, parking_date=date, user_id=user_id)
    db.session.add(new_history)
    db.session.commit()

    # print date, parking_id, user_id
    return redirect('/users/' + str(user_id))




@app.route("/register", methods=['GET'])
def register_form():
    """Show register form."""

    return render_template('registration_form.html')




@app.route("/register", methods=['POST'])
def register_process():
    """New user registration."""
    email = request.form.get('uemail')
    password = request.form.get('psw')
    first_name = request.form.get('fname')
    last_name = request.form.get('lname')

    user = User.query.filter(User.email == email).first()

    scores = []


    if user is None:       
        flash("You've created a new account!")
        new_user = User(email=email, password=password, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        session['logged_in'] = new_user.user_id

        return render_template("user_detail.html", user=new_user, scores=[])
    else:
        flash("Email existed. Please log in instead.")
        return render_template("login_form.html")


@app.route("/login_form")
def show_form():
    """Login Form."""

    return render_template("login_form.html")


@app.route("/login_form", methods=['POST'])
def process_form():
    """Checks if email and password match."""

    email = request.form.get('uemail')
    print "Email", email
    password = request.form.get('psw')
    print "PSW", password
    # email = 'phil@phil.com' 
    user = User.query.filter(User.email == email).first()
    print "This is user", user
    # if not user or if user is None:
    if not user:
        flash('Email not recognized, please register for a new account.')
        return render_template('registration_form.html')

    elif user.password != password:
        flash('Password is wrong, please log in again')
        return render_template('login_form.html')
    else:
        session['logged_in'] = user.user_id
        flash('Log in successful!')
        return redirect('users/' + str(user.user_id))


@app.route('/log_out')
def log_out():
    """Log Out"""

    del session['logged_in']
    flash('You have been logged out.')
    return render_template('homepage.html')


print "Here we go"


if __name__ == "__main__":

    print "We are in main"
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')