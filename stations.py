import requests
from xml.etree import cElementTree as ElementTree

ALL_STATIONS_URL = "http://w1.weather.gov/xml/current_obs/index.xml"

def get_all_stations_xml():
    """
    Bulk fetch all the data from NWS' stations endpoint.
    """
    r = requests.get(ALL_STATIONS_URL)
    r.raise_for_status()
    return r.content

def parse_all_stations_xml(xml_raw):
    """
    Parse stations from the NWS all stations XML file.

    :param bytes xml_raw: xml file content straight from NWS
    :rtype: Iterable[ElementTree]
    """
    for station in ElementTree.fromstring(xml_raw).findall("station"):
        yield station

def extract_lat_lon(station_tree):
    """
    Extracts a dict from a station ETree with station_id, lat, lon
    
    :param ElementTree station_tree: Station object
    :rtype: dict
    """ 
    return {
        "station_id": station_tree.find('station_id').text,
        "lat_lon": (float(station_tree.find('latitude').text),
                    float(station_tree.find('longitude').text))
    }

if __name__ == "__main__":
    stations = parse_all_stations_xml(get_all_stations_xml())
    for i in range(5):
        print extract_lat_lon(stations.next())
