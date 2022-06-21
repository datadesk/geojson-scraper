# geojson-scraper
Retrieves individual geojsons for cities in a county

Uses the openstreetmap API to get OSM ids for cities,
which are then used to download geojson files from MapIt
OpenStreetMap: https://nominatim.openstreetmap.org/ui/search.html?
  ex: https://nominatim.openstreetmap.org/ui/search.html?city=Arcadia&format=geojson
Map It: https://global.mapit.mysociety.org/
  ex: https://global.mapit.mysociety.org/code/osm_rel/3529862.html

Requirements: Array of city names and the county you're searching for them in.
