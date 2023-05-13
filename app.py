# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine)

# Save references to each table
measurement = Base.classes.measurement
station_class = Base.classes.station

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
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    # create session link from python to db
    session = Session(engine)
    # Query all precipitation
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()
    # Create a dictionary from the row data and append to a list of precipitation
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # create session link 
    session = Session(engine)
    
    # query all stations
    results = session.query(station_class.station).all()
    
    session.close()
    
    # convert list of tuples into normal list
    stations_list = list(np.ravel(results))
        
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # create session link 
    session = Session(engine)
    
    # query all stations
    tobs_results = session.query(measurement.date, measurement.tobs).filter(measurement.date >= '2016-08-23').\
        filter(measurement.station == 'USC00519281').all()

    session.close()
    
    # convert list of tuples into normal list
    all_tobs = []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
                        
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    # create session link
    session = Session(engine)
    
    # covert date string to date
    # date should be entered as "YYYY-MM-DD"
    date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    # query all stations
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= date).all()
    
    session.close()
    
    # convert list of tuples into normal list
    temps_stats = list(np.ravel(results))
    return jsonify(temps_stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # create session link
    session = Session(engine)
    
    # covert date string to date
    # date should be entered as "YYYY-MM-DD/YYYY-MM-DD"
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    
    # query all stations
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    
    session.close()
    
    # convert list of tuples into normal list
    all_start_end = list(np.ravel(results))
    return jsonify(all_start_end)

if __name__ == '__main__':
    app.run()

