from flask import Flask, render_template, request, redirect, url_for
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
    return redirect(url_for('.region', region=request.form['region'], s_id=id, s_nam=name))


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


# @app.route('/to/<season>/<outbound_id>/<destination>')
@app.route('/to/<outbound_id>/<destination>')
# def get_to(season, outbound_id, destination):
def get_to(outbound_id, destination):
    # if season == "na":
    #     season = "united states"
    # else:
    #     season = "latvia"

    locations = [destination, destination.split(',')[0], destination.split(',')[1]]
    loc = None
    i = 0
    while loc is None:
        loc = get_location_id(locations[i])
        i += 1
        if i == len(locations): break

    if loc is None:
        return """
    <div class="card red darken-1">
            <div class="card-content white-text">
              <span class="card-title">Uh oh.</span>
              <p>We can't find any flights to {0}. Try another hackathon.</p>
            </div>
          </div>""".format(destination)
    
    (id, name) = loc
    return "Going to" + id + '=>' + name

@app.route('/auth/login')
def login():
    pass

@app.route('/auth/register')
def register():
    pass
