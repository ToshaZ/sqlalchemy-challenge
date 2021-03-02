import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    return (
        f"Welcome to the Home Page<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> (enter date as YYYY-MM-DD)<br/>"
        f"/api/v1.0/<start/end> (enter date as YYYY-MM-DD/YYYY-MM-DD)"
    )

#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Create our session (link) from Python to the DB
        session = Session(engine)

        """Convert the query results to a dictionary using date as the key and prcp as the value."""
        # Starting from the most recent data point in the database. 
        year_precip = session.query(measurement.date, measurement.prcp).\
            filter(measurement.date >= '2016-08-23').order_by(measurement.date).all()

        session.close()

        # Convert list of tuples into normal list
        rain_list =[]
        for date, prcp in year_precip:
            rain_dict={}
            rain_dict[date] = prcp
            rain_list.append(rain_dict)

        return jsonify(rain_list)

#################################################
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    # Query
    results = session.query(station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))

    return jsonify(station_list)

#################################################
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most active station for the last year of data"""
    # Query
    most_active = session.query(measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= '2016-08-23').all()

    session.close()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(most_active))

    return jsonify(tobs_list)

#################################################
@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # take any date and convert to yyyy-mm-dd format for the query
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range"""
    # Query
    st_min_max = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start_date).all()

    session.close()

    # Convert list of tuples into normal list
    start_list = []
    for result in st_min_max:
        r = {}
        r["StartDate"] = start_date
        r["TMIN"] = result[0]
        r["TMAX"] = result[1]
        r["TAVG"] = result[2]
        start_list.append(r)

    return jsonify(start_list)

#################################################
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # take start and end dates and convert to yyyy-mm-dd format for the query
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")

    """When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive"""
    # Query
    st_end_min_max = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start_date).filter(measurement.date >= end_date).all()

    session.close()

    # Convert list of tuples into normal list
    start_end_list = []
    for result in st_end_min_max:
        r = {}
        r["StartDate"] = start_date
        r["EndDate"] = end_date
        r["TMIN"] = result[0]
        r["TMAX"] = result[1]
        r["TAVG"] = result[2]
        start_end_list.append(r)

    return jsonify(start_end_list)

#################################################
if __name__ == '__main__':
    app.run(debug=True)