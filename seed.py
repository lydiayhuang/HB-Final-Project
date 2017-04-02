"""Utility file to seed database """

from sqlalchemy import func
from model import User, Parking_location, User_history, Rating
from model import connect_to_db, db
from server import app
import datetime
import csv


def load_garages():
    """Load garages from u.user into database."""

    print "load_garages"
    print Parking_location

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Parking_location.query.delete()


    garages = {}
    #dictionary for garages
    with open("seed_data/garages.csv") as csvfile:
        #opencsvfile, what is rb means read something
        data = csv.DictReader(csvfile)
        #dictreader not sure what it does - reads the csv file?
        for element in data:
            # print element
    # Read u.user file and insert data
    # for row in open("seed_data/garages"):
            address = element['Address']
            location = element['Location 1']
            latitude, longitude = location[1:-1].split(",")
            print latitude

            location = Parking_location(
                    address=address,
                    latitude=latitude,
                    longitude=longitude)

        # We need to add to the session or it won't ever be stored
            db.session.add(location)

    # Once we're done, we should commit our work
    db.session.commit()

def add_users():

    users = {}
    with open("seed_data/mock.csv") as csvfile:
        data = csv.DictReader(csvfile)
        for element in data:


            email = element['email']
            password = element['password']
            first_name = element['first_name']
            last_name = element['last_name']
 

            user = User(email=email, 
                        password=password, 
                        first_name=first_name,
                        last_name=last_name)
            db.session.add(user)

    db.session.commit()


def add_history():

    history = {}
    with open("seed_data/history.csv") as csvfile:
        data = csv.DictReader(csvfile)
        for element in data:


            parking_id = element['parking_id']
            user_id = element['user_id']
            parking_date = element['parking_date']
            
 

            history = User_history(parking_id=parking_id, 
                        user_id=user_id, 
                        parking_date=parking_date,
                        )
            db.session.add(history)

    db.session.commit()



def add_rating():

    print "populating ratings"
    ratings = {}
    with open("seed_data/ratings.csv") as csvfile:
        data = csv.DictReader(csvfile)
        for element in data:


            parking_id = element['parking_id']
            user_id = element['user_id']
            score = element['score']
            
 

            rating = Rating(parking_id=parking_id, 
                        user_id=user_id, 
                        score=score
                        )
            db.session.add(rating)

    db.session.commit()
    print "finished populating ratines"



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()


    # Import different types of data
    load_garages()
    add_users()
    add_history()
    print 'seeded'
    add_rating()
