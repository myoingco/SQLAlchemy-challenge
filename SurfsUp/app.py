# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the date and prcp for the last 12 months
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>='2016-08-23').group_by(Measurement.date).order_by(Measurement.date).all()

    session.close()

    #create a dictionary using date as key and prcp as the value
    precipitation_list = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        precipitation_list.append(precipitation_dict)

    #Return the JSON representation of your dictionary
    return jsonify(station_list)

@app.route("/api/v1.0/stations")
def stations ():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the station name
    result = session.query(Station.station).all()

    session.close()

    #create a list of stations
    station_list = []
    for station in result:
        station_list.append(station)

    #Return a JSON list of stations from the dataset
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query the dates and temperature observations of the most active station
    Result =  session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>='2016-08-23').filter(Station.station == Measurement.station).filter(Station.name == 'WAIHEE 837.5, HI US').all()

    session.close()

    #Return a JSON list of temperature observations (TOBS)
    tobs_list = []
    for date, tobs in Result:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs 
        tobs_list.append(tobs_dict)

    #Return a JSON list of tobs from the dataset
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
     # Create our session (link) from Python to the DB
    session = Session(engine)

    Results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start_date_only).group_by(Measurement.date).all()

    session.close()

    #Return JSON list of max, min, avg tobs
    start_list = []
    for date,tmin,tmax,tavg in Results:
        start_dict = {}
        start_dict['Date'] = date
        start_dict['TMIN'] = tmin
        start_dict['TMAX'] = tmax
        start_dict['TAVG'] = tavg
        start_list.append(start_dict)

    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def StartDateEndDate(start_date,end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    Resultss = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date<=end_date).group_by(Measurement.date).all()

    session.close()

    #Return JSON list of max, min, avg tobs
    startend_list = []
    for date,Tmin,Tmax,Tavg in Resultss:
        startend_dict = {}
        startend_dict['Date'] = date
        startend_dict['TMIN'] = Tmin
        startend_dict['TMAX'] = Tmax
        startend_dict['TAVG'] = Tavg
        startend_list.append(startend_dict)
    return jsonify(startend_list)

if __name__ == '__main__':
    app.run(debug=True)

