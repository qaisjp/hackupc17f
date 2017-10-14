from flask import Flask
from flask import render_template, request
from datetime import date
# from .get_routes import get_routes
from .mlh import get_events
from .sky_loc import get_location_id

app = Flask(__name__)

errNotFoundLoc = "We couldn't find that place... try a different one."

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')

    outbound = request.form['outbound']

    # try and find placeid from "outbound"
    if outbound == "":
        return render_template('index.html', error=errNotFoundLoc)

    loc = get_location_id(outbound)
    if loc is None:
        return render_template('index.html', error=errNotFoundLoc)

    (id, name) = loc
    return render_template('index.html', error=id + " -> " + name)


@app.route('/region/')
@app.route('/region/<region>')
def region(region=""):
    # eu-2018
    # northamerica-2018
    if (region != "europe") and (region != "north-america") and (region != ""):
        region = ""

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
