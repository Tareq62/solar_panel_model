# NOAA weather data files hosted on ftp://ftp.ncdc.noaa.gov/pub/data/asos-fivemin/6401-2006/
# Extract the following features of interest: temperature, visibility, humidity

def extract_temperature(row):
    pieces = row.split()
    for piece in pieces:
        if piece.endswith("00"):
            return int(piece)/100

def extract_visibility(row):
    pieces = row.split()
    for piece in pieces:
        if piece.endswith("SM"):
            return int(piece.replace("SM", ""))

def extract_humidity(row):
    pieces = row.split()
    for piece in pieces:
        if piece.isdigit() and 0 < int(piece) < 100:
            return int(piece)
