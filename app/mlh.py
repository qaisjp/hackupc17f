from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests, time
import urllib
from datetime import date, datetime

year = str(datetime.today().year)

def request_events(season):
    mlh_url = "https://mlh.io/seasons/%s/events" % (season)
    mlh_html = requests.get(mlh_url)
    soup = BeautifulSoup(mlh_html.content, "lxml")
    event_list = soup.find_all('div', {'class':'col-lg-3'})
    events = []
    for event_for in event_list:
        event_id = str(event_for)
        event_id = event_id[(event_id.find("event")+12):(event_id.find("event")+15)]
        if event_id in events:
            continue
    
        link_tag = event_for.find('a')
        link = link_tag.get('href')

        img_tag = (event_for.findAll('img'))
        backgroundImage = img_tag[0]['src']
        logo = img_tag[1]['src']

        event_head = str(event_for.find_all('h3'))
        index = event_head.find(">") + 1
        event_head = event_head[index:]
        index = event_head.find("<")
        event_head = event_head[:index]

        event_date = str(event_for.find_all('p'))
        dates = event_for.find_all('meta')
        start_date = dates[0]['content']
        end_date = dates[1]['content']
        

        #This is for getting the city
        event_loc = str(event_for.find_all('span'))
        index = event_loc.find(">") + 1
        event_loc = event_loc[index:]
        index = event_loc.find("<")
        event_loc_city = event_loc[:index]

        #This is for getting the state, I added +9 because after it was ending -
        #- at "</span>, ". +9 just moves the pointer forward.
        event_loc = event_loc[index+9:]
        index = event_loc.find(">") + 1
        event_loc = event_loc[index:]
        index = event_loc.find("<")
        event_loc_state = event_loc[:index]
        event_loc = event_loc_city+ ", " + event_loc_state

        # create an event entry
        event = {}
        event["name"] = event_head
        event["location"] = event_loc
        event["start_date"] = datetime.strptime(start_date, "%Y-%m-%d").date()
        event["end_date"] = datetime.strptime(end_date, '%Y-%m-%d').date()
        event["link"] = link
        event["logo"] = logo
        event["id"] = event_id

        # append to the event list
        events.append(event)

    # return the event list
    return events

def get_events(season=""):
    if not season:
        na_events = request_events("na-" + year)
        eu_events = request_events("eu-" + year)
        return na_events + eu_events
    else:
        if season == "north-america":
            season = "na-" + year
        else:
            season = "eu-" + year
        return request_events(season)
