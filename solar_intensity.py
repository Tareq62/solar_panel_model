# Calculates theoretical solar intensity in kWh/m^2 given latitude, longtitude, and date/time

import os
import sys
import numpy as np 
import pandas as pd 
import datetime as datetime
import math
from math import cos, asin, sin, sqrt, atan2, pi, degrees, radians, ceil, floor
from secrets import APIKEY
import datetime, time
from polyline import decode
import requests
from bisect import bisect_left

def solar_intensity(lat=40.713, lng=-74.006, date_time=datetime.datetime.now()):
    # day_of_year = datetime.datetime.strptime(date_time, '%m/%d/%Y').timetuple().tm_yday
    day_of_year = date_time.timetuple().tm_yday
    declination_angle = degrees(asin(sin(radians(23.45)) * sin(2 * pi/365 * (day_of_year - 81))))
    # print 'declination_angle = ' + str(declination_angle)
    # equation of time to account for orbital eccentricity and axial wobble
    e_o_t = 9.87 * sin(2.0 * 2 * pi / 365 * (day_of_year - 81)) - 7.53 * cos(2 * pi / 365 * (day_of_year - 81)) - 1.5 * sin(2 * pi / 365 * (day_of_year - 81))
    gmt_diff = floor(lng / 15) # hour difference from GMT (+5 for EST)
    lstm = 15.0 * gmt_diff # local standard time meridian (edge of time zone)
    tc = 4.0 * (lng - lstm) + e_o_t # time correction factor
    local_solar_time = date_time + datetime.timedelta(0, tc/60.0)
    lst_dec = local_solar_time.hour + local_solar_time.minute / 60.0 + local_solar_time.second / 3600.0
    hour_angle = 15.0 * (lst_dec - 12.0)
    # print 'hour angle past solar noon = ' + str(hour_angle)
    # with a flat panel, the elevation angle is the incident angle
    elevation_angle = degrees(asin(sin(radians(declination_angle)) * sin(radians(lat)) + cos(radians(declination_angle)) * cos(radians(lat)) * cos(radians(hour_angle))))
    # print elevation_angle
    rad_from_vert = pi / 2 - radians(elevation_angle) # zenith angle in radians for airmass formula
    if rad_from_vert < pi / 2:
        air_mass = 1 / (cos(rad_from_vert) + 0.50572 * (96.07995 - degrees(rad_from_vert)) ** (-1.6364))
    else:
        air_mass = None
    e_0 = 1367 * (1 + 0.033 * cos(2 * pi * (day_of_year - 3) / 365))
    if air_mass:
        intensity = cos(rad_from_vert) * e_0 * 0.7 ** (air_mass ** 0.678)
        return intensity
    else:
        return 0

def integrate(intensity_list):
    integral = 0
    for index, item in enumerate(intensity_list):
        if index < (len(intensity_list) - 1):
            delta_t = float((intensity_list[index + 1].get('t') - intensity_list[index].get('t')) / 3600.0)
            # print delta_t
            avg_intensity = float(intensity_list[index + 1].get('intensity') + intensity_list[index].get('intensity')) / 2.0
            integral += delta_t * avg_intensity
    return integral / 1000.0

print "{} kWh/m^2".format(round(integrate(test_list), 4))
