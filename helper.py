#skeleton code
from urllib2 import urlopen
import json
import csv
import math
from geopy.distance import vincenty



def search_csv(FILEPATH):
	""" Parsing csv """
	garages = {}
	#dictionary for garages
	with open(FILEPATH, 'rb') as csvfile:
		#opencsvfile, what is rb means read something
		data = csv.DictReader(csvfile)
		#dictreader not sure what it does - reads the csv file?
		for element in data:
			print element
			#for every garage check the items
			# print element
			for key, value in element.items():
				if key == "Address" or value == "Location 1":
					#if key is address or value is location1
					garages[element['Address']] =element["Location 1"]
					#then assign location1 to address, why is garages used - becaue it's a dictionary.
					#parsing data
	return garages

		
def intake_address():
	"""takes address from user, raw_input"""
	#takes address from user
	num_data = raw_input("what is your street number? ")
	street_data = raw_input("what street are you on? ").lower()
	address = (num_data, street_data)

	return address


def build_url(address):
	"""passes user data into the google api"""
	#passes user data into the google api
	street_num = address[0]
	street_name = address[1]
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+street_num+"+"+street_name+"+"+"sanfrancisco"
	
	return url

def fetch_data(url):
	"""saving json data into a dictionary"""	
	json_obj = urlopen(url)
	geocode_dict = json.load(json_obj)

	return geocode_dict

def user_geocode(geocode_dict):
	"""returning the lat long of the user by accessing the geocode dictionary"""
	user_data = geocode_dict['results'][0]['geometry']['location']
	user_loc = (user_data['lat'], user_data['lng'])

	return user_loc

def closest_garage(garages, user_location, bound=5):
	closest_garages = []
	print "THIS IS THE USER LOCATION" 
	print user_location
	for garage in garages:
		print garage
		garage_location = (garage.latitude, garage.longitude)
		print garage_location
		dist = distance(garage_location, user_location)
		print dist
		if dist < bound:
			closest_garages.append(garage)
	return closest_garages[:10]





def get_closest_garage(garages, user_location):
	# closest = the first garage
	closest_garaget = None
	closest_garage = None
	for garage, loc in garages.items():
		location = garages[garage]
		location_list = location.split(",")
		print garage, loc 
		garage_coordinates = [] 
		for item in location_list:
			new_item = item.replace("(", "")
			new_item = new_item.replace(")", "").strip()
			garage_coordinates.append(float(new_item))
		if closest:
			d = distance(user_location, garage_coordinates)
			if d < closest:
				closest = d
				closest_garage = garage
		else: 
			closest = distance(user_location, garage_coordinates)
			closest_garage = garage

	return closest_garage 


			# print float(new_item)
			# print item 
			#strip invisibles

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d		


    	#Google Maps API key - AIzaSyCtbTBgDnd4FKa6iOlY8FDO3u1R94sItZc


		# print location_list (works)

		# print garage, loc 
		# print garages[garage]
		# print location
		# print user_location[0]
		#splitting on comma, replace "(" and ")" with empty string '' 
		#cast string to float (and I wll be able to subtract)
		#lat1 = float(garages[garage])- float(user_location[0])
		#lat1 = take garage lat and subtract user lat
		#long1 = take garage long and subtract user long
		#garage_distance = square root (lat1-power2 + long1-power2)
		#lat2 = closest lat and subtract user lat
		#long2 = closest long and subtract user long
		#closest_distance = square root (lat2-power2 + long2-power2)
		#if closest_distance > garage_distance then closest = garage

	#return closest

def main():
	#calling main
	garages = search_csv("garagefinderdata.csv")
	address = intake_address()
	url = build_url(address)
	geocode_dict = fetch_data(url)
	# print geocode_dict
	user_loc = user_geocode(geocode_dict)
	print "The closest garage to you is-- "
	print get_closest_garage(garages, user_loc)
	print user_loc

# main()







	#open list
	#loop for latlong 
	#subtract csv latlong and user latlong
	#save
