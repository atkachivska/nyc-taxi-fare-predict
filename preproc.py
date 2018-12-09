#!/usr/bin/env python3

'''                            :::COLUMNS IN OUTPUT FEATURE FILE:::
s.no, date, time, day_of_week, pickup_lat, pickup_long, pickup borough,
pickup address, drop_lat, drop_long, drop borough, drop address, distance, num of people'''

import csv
import datetime
from geopy.geocoders import Nominatim
import requests, json
import googlemaps
import time

# brooklyn : 40.643721, -74.011587
# queens : 40.755725, -73.800652
# staten island : 40.598183, -74.131374
# bronx : 40.853856, -73.862429
data = [[]]
i =0
#api_key =     ADD KEY HERE
last_read = 0

with open('all/pre_run1.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        last_read = row[0]

print("*****************\n")
print("*****************\n")
print(last_read)
print("*****************\n")
print("*****************\n")

csv_out_file = open('all/pre_run1.csv', 'a')

with open('all/train.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 0
    for row in csv_reader:
        if(i<=int(last_read)):
            i = i+1
            #continue
        if(i>int(last_read)):
            print("")
            print("")
            print("")
            print(row)
            li = []
            flag = 0
            li.append(i)
            # date, time and DOW handling
            date_time = row[2].split()
            if(len(date_time) >= 2):
                date = date_time[0]
                time = date_time[1]
                date_split = date.split('-')
                if(len(date_split) == 3):
                    li.append(date)
                    li.append(time)
                    try:
                        day = datetime.datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
                        li.append(day.weekday())
                    except ValueError:
                        print("ValueError")
                        flag = 1
                else:
                    print("date split")
                    flag = 1
            else:
                print("dae and time")
                flag = 1

            # Get borough and address of pickup location
            if flag == 0:
                geolocator = Nominatim(user_agent="get_location"+str(i))   
                pickup_lat = str(row[4])
                pickup_long = str(row[3])
                location = geolocator.reverse(pickup_lat+","+pickup_long)   #DEBUG: SSL error, upgrade python, issue with certifi
                loc = location.raw
                if('error' in loc):
                    print("error in goe")
                    flag = 1
                elif 'address' in loc and 'city' in loc['address'] and loc['address']['city'] != 'NYC':
                    flag = 1
                    print("address and city")
                else:
                    li.append(pickup_lat)
                    li.append(pickup_long)
                    li.append(loc['address']['county'])
                    li.append(loc['address'])


            # Get borough and address of drop location
            if flag == 0:
                drop_lat = str(row[6])
                drop_long = str(row[5])
                location = geolocator.reverse(drop_lat+","+drop_long)   #DEBUG: SSL error, upgrade python, issue with certifi
                loc = location.raw
                if('error' in loc):
                    flag = 1
                    print("error in geo2")
                elif 'address' in loc and 'city' in loc['address'] and loc['address']['city'] != 'NYC':
                    flag = 1
                    print("address and city2")
                else:
                    li.append(drop_lat)
                    li.append(drop_long)
                    li.append(loc['address']['county'])
                    li.append(loc['address'])


            #get distance between
            if flag == 0:
                gmaps = googlemaps.Client(key=api_key)
                directions_result = gmaps.directions(pickup_lat+","+pickup_long,
                                                     drop_lat+","+drop_long,
                                                     mode="driving")
                
                if len(directions_result)>0:
                    dir_res = directions_result[0]
                    if 'legs' in dir_res:
                        if len(dir_res['legs'])>0:
                            if 'distance' in dir_res['legs'][0]:
                                if 'text' in dir_res['legs'][0]["distance"]:
                                    li.append(dir_res['legs'][0]["distance"]["text"])
                                else:
                                    print("text")
                                    flag = 1
                            else:
                                print("distance")
                                flag = 1

                        else:
                            print("len")
                            flag = 1
                    else:
                        print("legs")
                        flag = 1
                else:
                    print("dir_res")
                    flag = 1

            # num_people
            if flag == 0:
                li.append(row[7])



            if flag == 0:
                data.append(li)
                csv_out_writer = csv.writer(csv_out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_out_writer.writerow(li)
            i = i+1
