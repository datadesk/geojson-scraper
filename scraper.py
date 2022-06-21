import requests
import json
from bs4 import BeautifulSoup
# Script summary
# Uses the openstreetmap API to get OSM ids for cities,
# which are then used to download geojson files from MapIt
# OpenStreetMap: https://nominatim.openstreetmap.org/ui/search.html?
# Map It: https://global.mapit.mysociety.org/
# Requirements: Array of city names and the county you're searching for them in.


# given an array of city names
# gets list of OSM IDs from open street map to feed into mapit,
def get_osm_list(county, cityarray):
    apistart = 'https://nominatim.openstreetmap.org/search?city='
    apiend = '&format=geojson'
    osmarray = []

    i = 0
    while i < len(cityarray):
        response = openstreetmap_api_call(apistart + cityarray[i] + apiend)
        osm = get_osm(county, response)
        osmarray.append(osm)
        i = i + 1

    return osmarray


# Makes single call to openstreetmap API
def openstreetmap_api_call(api):
    response = requests.get(api)
    if response.status_code == 200:
        print(f"successfully fetched the data")
        return response.json()
    else:
        print(f"Hello person, there's a {response.status_code} error with your request")


# gets single OSM ID
def get_osm(county, jsondictionary):
    results = (jsondictionary["features"])
    osm = None
    i = 0
    while (osm is None) and i < len(results):
        props = results[i]["properties"]
        if (county in props['display_name']) \
                and ("boundary" in props['category']):
            osm = props['osm_id']
        else:
            i = i + 1
    if osm is None:
        osm = -1
    return osm


#creates all geojson, returns array of missing geojsons
def get_all_geojson(cityarray, osmarray):
    i = 0
    missing = []
    while i < len(osmarray):
        if osmarray[i] > 0:
            maybemissing = get_geojson(cityarray[i], osmarray[i])
            if maybemissing is not None:
                missing.append(maybemissing)
        else:
            print("MISSING: " + cityarray[i])
            missing.append(cityarray[i])
        i = i + 1
    return missing


# Get single GeoJson
def get_geojson(cityname, cityosm):
    url = "https://global.mapit.mysociety.org/code/osm_rel/"+str(cityosm)+".html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    request = requests.get(url, headers=headers).text
    soup = BeautifulSoup(request, 'lxml')
    section = soup.find("section")
    geojsonurlend = None
    print(url)

    if section is not None:
        for link in section.findAll('a', href=True, text='GeoJSON'):
            geojsonurlend = link['href']

        #Entering geojson link
        geojsonurl = "https://global.mapit.mysociety.org/" + geojsonurlend
        geojsonrequest = requests.get(geojsonurl, headers=headers).text
        print(geojsonrequest)

        with open(cityname+'.geojson', 'w') as f:
            f.write(geojsonrequest)
        print("Created Json File")

    else:
        print('MISSING:' + cityname)
        return cityname


if __name__ == "__main__":
    cityarray = ["Agoura Hills","Alhambra","Arcadia","Artesia","Avalon","Azusa",
                 "Baldwin Park","Bell","Bell Gardens","Bellflower","Beverly Hills",
                 "Bradbury","Burbank","Calabasas","Carson","Cerritos",
                 "City of Industry","Claremont","Commerce","Compton","Covina",
                 "Cudahy","Culver City","Diamond Bar","Downey","Duarte","El Monte",
                 "El Segundo","Gardena","Glendale","Glendora","Hawaiian Gardens",
                 "Hawthorne","Hermosa Beach","Hidden Hills","Huntington Park",
                 "Inglewood","Irwindale","La Cañada Flintridge","La Habra Heights",
                 "La Mirada","La Puente","La Verne","Lakewood","Lancaster","Lawndale",
                 "Lomita","Long Beach","Los Angeles","Lynwood","Malibu","Manhattan Beach",
                 "Maywood","Monrovia","Montebello","Monterey Park","Norwalk",
                 "Palmdale","Palos Verdes Estates","Paramount","Pasadena","Pico Rivera",
                 "Pomona","Rancho Palos Verdes","Redondo Beach","Rolling Hills",
                 "Rolling Hills Estates","Rosemead","San Dimas","San Fernando",
                 "San Gabriel","San Marino","Santa Clarita","Santa Fe Springs",
                 "Santa Monica","Sierra Madre","Signal Hill","South El Monte",
                 "South Gate","South Pasadena","Temple City","Torrance","Vernon",
                 "Walnut","West Covina","West Hollywood","Westlake Village","Whittier"]
    osm_array = get_osm_list("Los Angeles County", cityarray)
    missing = get_all_geojson(cityarray, osm_array)
    print(missing)



