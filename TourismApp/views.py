from django.shortcuts import render

import numpy as np
from geopy.geocoders import Nominatim
import wikipedia


def index(request):
    return render(request, 'index.html', context={})


def getImages(place):
    images_array = []

    images = wikipedia.page(place).images
    for img in images:
        if img[-3:] in ('png', 'jpg', 'jpeg'):
            images_array.append(img)

    return images_array


def getWiki(place):
    result = wikipedia.summary(place, 10)
    return result



# Returns the distance in KM
def geocalc(lat0, lon0, lat1, lon1):
    EARTH_R = 6372.8

    lat0 = np.radians(lat0)
    lon0 = np.radians(lon0)
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)

    # StackOverflow
    dlon = lon0 - lon1
    y = np.sqrt((np.cos(lat1) * np.sin(dlon)) ** 2 +
                (np.cos(lat0) * np.sin(lat1) - np.sin(lat0) *
                 np.cos(lat1) * np.cos(dlon)) ** 2)
    x = np.sin(lat0) * np.sin(lat1) + \
        np.cos(lat0) * np.cos(lat1) * np.cos(dlon)
    c = np.arctan2(y, x)
    return EARTH_R * c


def getNearestCity(place):
    place = place.lower()

    geolocator = Nominatim(user_agent="my_user_agent")

    CityCenterListData = ["Delhi", "Bangalore",  "Chennai", "Amritsar", 'Jammu', "Kashmir", "Coimbatore", "Visakhapatnam", "PCMC", "Patna", "Vadodara", "Ludhiana", "Agra", "Nashik", "Ranchi", "Faridabad", "Meerut", "Rajkot", "Kalyan", "Vasai",
                          "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi", "Allahabad", "Howrah", "Gwalior", "Jabalpur", "Madurai", "Jodhpur", "Salem",
                          "Raipur", "Kota", "Chandigarh", "Jalandhar",  'Manipal']


    # Later I will simply replace this code by fetching the lat and long from the database

    LatitudeList = []
    LongitudeList = []
    for address in CityCenterListData:
        loc = geolocator.geocode(address)
        LatitudeList.append(loc.latitude)
        LongitudeList.append(loc.longitude)

    lat = 0
    long = 0
    loc = geolocator.geocode(place)
    lat = loc.latitude
    long = loc.longitude
    MinValue = 999999999
    MinValuePlace = ""
    for i1 in range(0, len(CityCenterListData)):
        TempValue = geocalc(lat, long, LatitudeList[i1], LongitudeList[i1])
        if TempValue < MinValue:
            MinValue = TempValue
            MinValuePlace = CityCenterListData[i1]
    return (MinValuePlace, MinValue)


def placeNear(request):
    nearCity = "Delhi"
    distance = 0
    images_array = []
    if request.method == 'POST':
        city = request.POST.get('city')
        nearCity, distance = getNearestCity(city)
        if nearCity=='Delhi':
            wiki_result=getWiki('Delhi, capital of India')
            images_array = getImages('Delhi, capital of India')
        else:
            wiki_result = getWiki(nearCity)
            images_array = getImages(nearCity)

    context = {'nearCity': nearCity.title(), 'wiki_result': wiki_result,
               'images_array': images_array[:12], 'distance': int(distance)}

    return render(request, 'placeNear.html', context=context)

    # CityCenterListData = ["Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "PMC", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal",
    #                       "Coimbatore", "Visakhapatnam", "PCMC", "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Ranchi", "Faridabad", "Meerut", "Rajkot", "Kalyan", "Vasai",
    #                       "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi", "Allahabad", "Howrah", "Gwalior", "Jabalpur", "Madurai", "Vijayawada", "Jodhpur", "Salem",
    #                       "Raipur", "Kota", "Chandigarh", "Guwahati", "Solapur", "Hubli–Dharwad", "Mysore", "Tiruchirappalli", "Bareilly", "Aligarh", "Tiruppur", "Gurgaon", "Moradabad",
    #                       "Jalandhar", "Bhubaneswar", "Warangal", "Mira", "Jalgaon", "Guntur", "Thiruvananthapuram", "Bhiwandi", "Saharanpur", "Gorakhpur", "Bikaner", "Amravati", "Noida",
    #                       "Jamshedpur", "Bhilai", "Cuttack", "Firozabad", "Kochi", "Nellore", "Bhavnagar", "Dehradun", "Durgapur", "Asansol", "Rourkela", "Nanded", "Kolhapur", "Ajmer", "Akola",
    #                       "Gulbarga", "Jamnagar", "Ujjain", "Loni", "Siliguri", "Jhansi", "Ulhasnagar", "Jammu"]
