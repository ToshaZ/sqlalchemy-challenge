import numpy as np

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
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
        # Create our session (link) from Python to the DB
        session = Session(engine)

        """Convert the query results to a dictionary using date as the key and prcp as the value."""
        # Query
        results = session.query(measurement.date, measurement.prcp).all()

        session.close()

        # Convert list of tuples into normal list
        all_names = list(np.ravel(results))

        return jsonify(all_names)

#@app.route("/api/v1.0/stations")
#def stations():

#@app.route("/api/v1.0/tobs")
#def tobs():

#@app.route("/api/v1.0/<start>" and "/api/v1.0/<start>/<end>")
#def <start> and <start>/<end>()

if __name__ == '__main__':
    app.run()