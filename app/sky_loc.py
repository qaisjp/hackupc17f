import urllib, json

def get_location_id(query):
    link = "http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/UK/gbp/en-GB?query=" + query + "&apiKey=" + apiKey

   # get dictionary from URL
    with urllib.request.urlopen(link) as url:
        dictionary = json.loads(url.read().decode())

    print(dictionary)

   # get cityID
    if dictionary["Places"][0]['PlaceId'] is None:
        print("Error: CityID not found; got ", query)
        return
    else:
        return dictionary["Places"][0]['PlaceId']