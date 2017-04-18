"""Models and database functions for ParkerSpace."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ParkerSpace."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)



    parking_visited = db.relationship("Parking_location",
                             secondary="user_history",
                             backref="users")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s first_name=%s last_name%s>" % (self.user_id,
                                               self.email, self.first_name, 
                                               self.last_name)


# user_Phil = User(email='phil@phil.com', password=1234, first_name='Phil', last_name='Liao')

print "About to define Parking_location"
class Parking_location(db.Model):
    """Parked location of User."""
    print "define parking location"
    __tablename__ = "Parking_location"

    parking_id = db.Column(db.Integer, autoincrement=True, primary_key=True, )
    address = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float,nullable=False)

    print "about to establsih rating relationship in parking location"
    rating = db.relationship("Rating",
                           backref=db.backref("Parking_location",
                                              order_by=parking_id))

# pick from table and create new parking_location tables
   

class User_history(db.Model):
    
    __tablename__ = "user_history"

    parking_id = db.Column(db.Integer, db.ForeignKey('Parking_location.parking_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    history_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    parking_date = db.Column(db.DateTime, nullable=True)

    
    


class Rating(db.Model):
    """Ratings of the parking garages."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    parking_id = db.Column(db.Integer, db.ForeignKey('Parking_location.parking_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)



    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("ratings",
                                              order_by=rating_id))


    # Define relationship to parking location
    parking = db.relationship("Parking_location",
                            backref=db.backref("ratings",
                                               order_by=rating_id))

 
    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Rating rating_id=%s parking_id=%s user_id=%s score=%s>"
        return s % (self.rating_id, self.parking_id, self.user_id,
                    self.score)




##############################################################################
# Helper functions

def connect_to_db(app):

    print "Just started connect_to_db"
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///parking_location'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

    db.create_all()
    print "Tables created"