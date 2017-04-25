"""ParkerSF."""
from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify, Response, url_for)
from flask_debugtoolbar import DebugToolbarExtension
from model import User, connect_to_db, db, Parking_location, User_history, Rating
import logging
from helper import closest_garage
import geocoder
import math



app = Flask(__name__, static_url_path='/templates/assets')

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

def check_login_status(user_id):
    return str(session.get('logged_in', None)) == str(user_id)
        

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
    """Search closes garage to destination."""

    shouldReload = request.args.get('shouldReload', False) 
    if shouldReload:
        parking_id = request.args.get('parking_id') 
    else:
        parking_id = None

    address = request.args.get('address') 
    location = geocoder.google(address).latlng
    garages = Parking_location.query.all()
    results = closest_garage(garages, location)
    garage_data = [garage.address for garage in results]
    

    for garage in results:
        user_rating_score = 0
        if 'logged_in' in session.keys():
            user_rating = Rating.query.filter(Rating.parking_id == garage.parking_id, Rating.user_id == session['logged_in'])
        

            if user_rating.count():
                user_rating_score = user_rating.one().score
            garage.temp_userRating = user_rating_score
        else:
            garage.temp_userRating = None

        if len(garage.rating):
            print 'rating', len(garage.rating), [rating.score if rating.score else 0 for rating in garage.rating]
            overall_rating = float(sum(rating.score if rating.score else 0 for rating in garage.rating))/len(garage.rating)
        else:
            overall_rating = 0
        garage.temp_overallRating = overall_rating
    # return jsonify(results=garage_data)
    return render_template("garage_list.html", parking_id=parking_id, 
                                               search_address=address, 
                                               garages=results, 
                                            
                                               shouldReload= shouldReload)






@app.route("/users/<user_id>")
def user_info(user_id):
    """Show user and ratings."""
    print session
    print user_id

    if not check_login_status(user_id):
        return redirect('/')

    user = User.query.filter(User.user_id == user_id).one()
    
    if not user:
        flash('error, this is the wrong input')

    user_history = User_history.query.filter(User_history.user_id == user_id)
    rating = []
    histories = {}

    for history in user_history:
        parking_location = Parking_location.query.get(history.parking_id)
        score = Rating.query.filter(Rating.user_id == history.user_id).filter(Rating.parking_id== history.parking_id).first()
        if score:
            score = score.score

        histories.setdefault(parking_location.address, dict(score=score, dates=[]))
        histories[parking_location.address]['dates'].append(history.parking_date)

        # rating.append(dict(location=parking_location, date=history.parking_date, score=score))

    
    print histories
    return render_template("user_detail.html", 
                                    scores=histories,
                                    user=user
                                    )


# @app.route("/garages")
# def garage_list():
#     """Show list of garages."""

#     garage = Parking_location.query.filter(Parking_location.parking_id == parking_id).one()

#     print "About to query for parking location"
#     parking_locations = Parking_location.query.all()
    
#     print "about to render template"
#     return render_template("garage_list.html", garage=garage, parking_locations=parking_locations)

# @app.route('/weather.json')
# def weather():
#     """Return a weather-info dictionary for this zipcode."""

#     zipcode = request.args.get('zipcode')
#     weather_info = WEATHER.get(zipcode, DEFAULT_WEATHER)
#     return jsonify(weather_info)

@app.route("/garage_rating", methods=['POST'])
def add_new_rating():
    """Add new rating to garages."""

    if 'logged_in' not in session.keys():
        return redirect('/')
    address = request.form.get("search_address")
    rating = request.form.get("ratings")
    parking_id = request.form.get("parking")
    user_id = request.form.get("user")
    shouldReload = bool(request.form.get("reload", False))

    existing_rating = (Rating.query.filter(Rating.parking_id ==parking_id,
                        Rating.user_id == user_id).first())
    if existing_rating:
        flash('You have successfully updated your rating!')
        existing_rating.score = rating
    else:
        new_rating = Rating(parking_id=parking_id, 
                            user_id=user_id, score=rating)
        db.session.add(new_rating)
        flash('You have successfully added a new rating!')
    db.session.commit()  

    return redirect(url_for('search_list', address=address, parking_id=parking_id, rating=rating, shouldReload=shouldReload))





@app.route("/garages/<parking_id>")
def garage_details(parking_id):
    """Show garage details."""

    garage = Parking_location.query.filter(Parking_location.parking_id == parking_id).one()
    user_rating_score = None

    if 'logged_in' in session.keys():
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

    if not check_login_status(user_id):
        return redirect('/')

    user_histories = User_history.query.filter(User_history.user_id == user_id).all()
    #creating array of 12 0's for 12 months
    data = [0]*12
    for history in user_histories:
        if history.parking_date:
            month = history.parking_date.month 
            #index starts from 0 so we are subtracting 1
            data[month-1]+= 1
            # print history.parking_date
    return jsonify(data=data)


# @app.route("/d3chart/<user_id>", methods=['GET'])
# def d3chart(user_id):

#     if not check_login_status(user_id):
#         return redirect('/')

#     user_histories = User_history.query.filter(User_history.user_id == user_id)
#     unq_parking_location = []
#     addresses = []
#     for history in user_histories:
#         location = Parking_location.query.get(history.parking_id)
#         if history.parking_id not in unq_parking_location:
#             unq_parking_location.append(history.parking_id)
#             addresses.append(location.address)
    
#     matrix_length = 12+1+len(unq_parking_location)+1
#     print(unq_parking_location)
#     print(addresses)
#     # matrix = [[0 for x in range(matrix_length)] for y in range(matrix_length)] 
    
#     matrix = []
#     for id in unq_parking_location:
#         user_histories = User_history.query.filter(User_history.parking_id == id, User_history.user_id == user_id)
#         data = [0]*matrix_length
#         for history in user_histories:
#             month = history.parking_date.month 
#             #index starts from 0 so we are subtracting 1
#             data[month-1]+= 1
#         matrix.append(data)
#     empty_stroke = 0
    
#     for line in matrix:
#         empty_stroke += sum(line)

#     rMatrix = []
#     for line in matrix:
#         rMatrix.append(line[13:] + line[:13])

#     matrix.append([0]*(matrix_length-1)+[math.floor(empty_stroke*.1)])
#     rMatrix.append([0]*12 + [math.floor(empty_stroke*.1)] + [0]*(matrix_length - 13))

#     print(matrix + rMatrix)
#     return jsonify(data=matrix + rMatrix,
#                     names=addresses, 
#                     respondents=empty_stroke)


@app.route("/record_parking", methods=['POST'])
def record_parking():
    """records parking date"""

    if 'logged_in' not in session.keys():
        return redirect('/')


    date = request.form.get("parking_date")
    parking_id = request.form.get("parking_id")
    user_id = request.form.get("user")

    new_history = User_history(parking_id=parking_id, parking_date=date, user_id=user_id)
    db.session.add(new_history)
    db.session.commit()
    flash('You have recorded this date.')

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
        flash("Email exists. Please log in instead.")
        return render_template("login_form.html")


# @app.route("/login_form")
# def show_form():
#     """Login Form."""

#     return render_template("login_form.html")


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
        return render_template('homepage.html')

    elif user.password != password:
        flash('Password is wrong, please log in again')
        return render_template('login_form.html')
    else:
        session['logged_in'] = user.user_id
        flash('You are now logged in!')
        return redirect("/")


@app.route('/log_out')
def log_out():
    """Log Out"""

    if 'logged_in' not in session.keys():
        return redirect('/')

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