# ParkerSF

Deployed using AWS LightSail http://54.70.254.58/

# Introduction

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

### How it works
When SFparks first loads, the homepage displays all parks and open spaces queried from the database. If a user is logged in, their favorite parks will also be mapped.

![Homepage](/static/img/homepage.png)

#### Geocoding & searching
The user provides a starting location and routing profile for the search query.

For a starting location, the user can input an address which is translated to latitude/longitude coordinates using the Mapbox geocoding API or chose to use their current location, which is filled in to the search form using the HTML5 geolocation API. The user also specifies timing and routing conditions, which are posted to the server with their starting coordinates.

![Search](/static/img/search.png)

#### Server-side logic
To make the final distances API call less 'expensive', the database is first queried for parks that fall within a bounding box-based heuristic based on average walking and cycling speeds. The server then calls a method on these Park objects to create GeoJSON objects for each park that meets this criteria. Finally the Mapbox distance API is used to calculate the travel time to each of those parks based on the user’s specified routing profile. The GeoJSON objects are updated with this value and loaded onto a new page that renders a new map layer for parks that are within the travel time + routing profile determined by the user.

![Search](/static/img/results.png)
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
email: phil@phil.com
password: 1234
