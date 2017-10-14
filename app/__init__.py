from flask import Flask
from flask import render_template
from datetime import date
# from .get_routes import get_routes
from .mlh import get_events

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/region/')
@app.route('/region/<region>')
def region(region=""):
    # eu-2018
    # northamerica-2018
    if (region != "europe") and (region != "north-america") and (region != ""):
        region = "europe"

    # if region == "north-america":
    #     season elif region=="europe": "eu" else: "north-america"


    events = get_events(region)
    
    # get_routes("UK-sky", "PARI-sky", date(2017, 10, 16), date(2017, 10, 21))

    # get_routes("UK", "US", date(2017, 10, 16), date(2017, 10, 18))

    return render_template('region.html', region=region, events=events)

@app.route('/auth/login')
def login():
    pass

@app.route('/auth/register')
def register():
    pass
