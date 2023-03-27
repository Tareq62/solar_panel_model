# solar_panel_model
Training a model to predict solar panel intensity based on local weather data. See solar_regression.ipynb for the full tour. 

Weather data inputs:

* Temperature (Kelvin)
* Hours of daylight
* Humidity
* Precipitation
* Theoretical solar intensity, depending on:
    * Latitude
    * Longitude
    * Day of year
    * Time of day (5-minute resolution)

Output:

* Predicted solar intensity (MW)
* Error score compared to actual solar panel data

Assumptions based on NOAA input data:
* Temperature is in Celsius * 1000, parsed as first 3- or 4-digit number ending in "00"
* Visibility is parsed as a number followed by "SM"
* Humidity is parsed as a 1- or 2-digit number representing relative humidity in percentage


## Sources

NOAA weather data files

ftp://ftp.ncdc.noaa.gov/pub/data/asos-fivemin/6401-2006

Solar panel performance data

https://www.nrel.gov/grid/solar-power-data.html
