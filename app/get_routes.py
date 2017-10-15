import urllib.request
import requests
import json

f = open('key.txt')
API_KEY = f.read()
f.close()

def get_routes(origin_id, destination_id, date_out, date_in):
    session_params = {
        'cabinclass':"Economy",
        'country':"UK",
        'currency':'GBP',
        'locale':'en-GB',
        'locationSchema':'iata',
        'originplace': origin_id,
        'destinationplace': destination_id,
        'outbounddate':date_out,
        'inbounddate':date_in,
        'adults':1,
        'apiKey': API_KEY,
        'limit':3
    }

    response = requests.post('http://partners.api.skyscanner.net/apiservices/pricing/v1.0', session_params)
    print(response.status_code)
    link = response.headers['Location'] 
    print(link)

    request_params = {
        'sortType': 'price',
        'sortOrder':'asc',
        'apiKey': API_KEY
    }
    flights = requests.get(link, params=session_params, headers={'Cache-Control': 'no-cache',
                                    'accept': 'application/json'})

    print(flights.status_code)

    json_response = json.loads(flights.text)
    itineraries = json_response['Itineraries']

    result = []

    print(itineraries[0])
    if itineraries[0]:
        flights = itineraries[0]
        for index, flight in flights:
            pricing_options = flights['PricingOptions']

            flight_price = pricing_options[0]['Price']
            flight_url = pricing_options[0]['DeeplinkUrl']

            print({'price': flight_price, 'url': flight_url})
            result.append({'price': flight_price, 'url': flight_url})

    # Get the top 3 results
    return result
