import urllib
import json

f = open('key.txt')
apiKey = f.read()
f.close()

def get_location_id(query):
    link = "http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/UK/gbp/en-GB?" + urllib.parse.urlencode({
        'query': query,
        'apiKey': apiKey
    })

   # get dictionary from URL
    with urllib.request.urlopen(link) as url:
        dictionary = json.loads(url.read().decode())

    print(dictionary)

    if not dictionary["Places"]:
        return

    place = dictionary["Places"][0]
    if place is None:
        return
   

    if place is None:
        return
    
    return (place['PlaceId'], place['PlaceName'] + ", " + place["CountryName"])
