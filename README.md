# ParkerSF

Deployed using AWS LightSail http://54.70.254.58/

Parker SF relieves anyone trying to find parking in the bustling city of SF. ParkerSF will take in a user input location and return 10 sorted closest parking garages near the destination. The locations of the garages are return as markers on a Google map linking to the garages displayed in the side bar. The map feature provides users a visualization of how far the garage is from the destination, allowing the user to select the most convenient garage possible. In addition, this application also allows the user to compare the ratings of every garage to select the best garage available as well as a chart and table to visualize the user’s past parking history.

### Technology Stack:

#### Backend:

+ Python  
+ Flask 
+ Flask Mail  
+ Python Libraries: Passlib  
+ PostgreSQL  
+ SQLAlchemy
+ Python Geocoder

#### Frontend:

+ Javascript
+ Jinja2
+ jQuery
+ Ajax
+ HTML5
+ CSS
+ Bootstrap

#### APIs:

+ Google Maps
+ Chart.js 


## Overview & Features

### Password Authentification
Users must log in to use app features. Clicking the Get Started button triggers a modal window. I'm encrypting and hashing the entered passwords using the Python library Passlib, and then comparing that to the user's encrypted/hashed password that is stored in the Postgres database. If the passwords match up, the user gets a JSON Web Token is redirected to their profile.  

### Get Up and Go

Clicking the Get Up and Go button triggers a modal window that asks if the user would like to order a Lyft 

Once the user makes their decision, an AJAX POST request gets sent to the server and a few things happen over on the server-side: The app uses SQLAlchemy to query the database for the user's stored preferences, and then uses those preferences to make two API calls to Yelp (one to get all applicable restaurants, and one to get all applicable activities). It then removes any locations that the user has already been to while using the app, picks a random choice from the remaining destinations (using the Python library Random). If the user is getting a Lyft, it stores the coordinates of the first destination in the session. It then sends a confirmation email to the user using Flask Mail. The callback function of the AJAX request updates the HTML in the modal window.  


The user can use their current location if their browser supports geolocation, or enter their address. This uses the user's location and the destination coordinates stored in the session to send a request to the Lyft API to get an estimate on how much a Lyft ride to the first surprise detination would cost. If the user decides to order the Lyft, they'll be taken over to Lyft to authorize access to their Lyft account, and then their Lyft will be on its way!


### Planning Trips
Users can also plan a trip for a later date using a sliding form that I created using jQuery. They enter what neighborhood they want to go to, how much they want to spend, and what type of food they want to eat and the API calls to Yelp will use those specific parameters instead of the user's stored preferences


### Trip Tracker
Once a trip begins, users have access to an interactive Trip Tracker that I've implemented using the Twilio API. The user can text the Trip Tracker to get the address or name of their next destination. In the development process, I used an ngrok tunnel to allow for Twilio to redirect the incoming texts as POST requests to my local Flask server.  


### Joining a Trip
I created a matching algorithm to find users with open trips who also have similar tastes and preferences. I've ranked each matched user from most similar to least, and users can swipe through to join an interesting user's trip. I added the swiping animation using jQuery, and designed the cards using Bootstrap.  


### User Profile
Over on the user profile, I've used the Google Maps API to display the user's past destinations using emoji map markers. (I wrote a Javascript function to randomly select each emoji to use for the map marker). Each map marker also displays an info window on mouseover. The info window displays the name of the destination, an image from Yelp, and a link to its Yelp page. (All of that info is stored in my Postgres database, and passed over the client side with JSON).  


### Database Model
I modeled my database using SQL, SQLAlchemy

## Run ParkerSF on your machine

First, clone or fork this repo:
```
git clone https://github.com/lydiayhuang/HB-Final-Project.git
cd HB-Final-Project
```
Create and activate a virtual environment:
```
virtualenv env
source env/bin/activate
```
Install the dependencies:
```
pip install -r requirements.txt
```
Use Gmail username and password to use to send confirmation emails. Store this info in a file called secrets.sh  
Source secret keys:  
```
source secrets.sh
```
If you have PostgreSQL on your machine, create a database called parking_location and run the seed file:
```
createdb parking_location 
python seed.py
```

Run the server:
```
python server.py
```
Navigate to localhost:5000 in your browser and use these account credentials to get started right away (or go through the registration flow and create your own account):  
email: porterleon@example.org  
password: @VZDTeoS$0
