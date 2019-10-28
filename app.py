# import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# import Flask
from flask import Flask,jsonify

######################################################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database and tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

################################
# Create an app
app = Flask(__name__)
################################
# Flask Routes
# Define what to do when user hits the index route
@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api.v1.0/start_date/<start><br/>"
        f"/api.v1.0/start_date/end_date<start>/<end>"
    )
# create precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session link
    session = Session(engine)

    """Return the dictionary for date and precipitation info"""
    # Query precipitation for last 12 months of  data
    query_date="2016-08-23"
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date>=query_date).all()

    session.close()
    
    # Create a dictionary as date the key and prcp as the value
    precipitation = []
    for result in results:
        row = {}
        row[result[0]] = result[1]
        precipitation.append(row)

    return jsonify(precipitation )

# create stations route    
@app.route("/api/v1.0/stations")
def stations():
    # Create the session link
    session = Session(engine)
    
    """Return a JSON list of stations from the dataset."""
    results = session.query(Station.station,Station.name).all()
    
    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))
    
    # jsonify the list
    return jsonify(station_list)

# create temperatures route
@app.route("/api/v1.0/tobs")
def tobs():
    # create session link
    session = Session(engine)
    
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    # query tempratures from a year from the last data point. 
    query_date = "2016-08-23"
    results = session.query(Measurement.tobs).filter(Measurement.date >= query_date).all()

    session.close()

    # convert list of tuples to normal list
    tobs_list = list(np.ravel(results))

    # jsonify the list
    return jsonify(tobs_list)

# create start route
@app.route("/api/v1.0/start_date/<start>")
def start(start_date):
    # create session link
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."""

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    return jsonify(results)



if __name__ == "__main__":
    app.run(debug=True)
