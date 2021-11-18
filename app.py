import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func ,inspect

from flask import Flask, jsonify

#create engine (start your engine)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect database
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

inspector = inspect(engine)
inspector.get_table_names()

# data_setup = datetime(Measurement.date)

# Flask Setup
app = Flask(__name__)

# Query for the dates and temperature observations from the last year.

@app.route("/")
def home():
    return("/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "/api/v1.0/2017-01-01<br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    results1 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>="2016-08-23").all()
    prcp_dict = list(np.ravel(results1))
#  Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
    prcp_dict = []
    for temps in results1:
        dt_dict = {}
        dt_dict["date"] = Measurement.date
        dt_dict["tobs"] = Measurement.tobs
        prcp_dict.append(dt_dict)

#  Return the JSON representation of your dictionary.
    return jsonify(prcp_dict)
    
   
# * `/api/v1.0/stations`
#   * Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    results2 = session.query(Station.station, Station.name).all()

    sec_dict = list(np.ravel(results2))
# # #  Convert the query results to a Dictionary.
    sec_dict = []
    for sta in results2:
         sta_dict = {}
         sta_dict["station"] = Station.station
         sta_dict["name"] = Station.name
         sec_dict.append(sta_dict)
    return jsonify(sec_dict)

# # * `/api/v1.0/tobs`
# #   * Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    results3 = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date>="2016-08-23").\
            filter(Measurement.date<="2017-08-23").all()

            
    temp_dict = list(np.ravel(results3))

#  Convert the query results to a Dictionary.
    third_dict = []
    for temps in results3:
         temp_dict = {}
         temp_dict["date"] = Measurement.date
         temp_dict["tobs"] = Measurement.tobs
         third_dict.append(temp_dict)
    return jsonify(temp_dict)

# # * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

# Calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date

@app.route("/api/v1.0/<start>")
def start(start):

    print("Received start date api request.")

    #First we find the last date in the database
    final_date_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
    start_day_list = list(final_date_query)

    #get the temperatures
    return jsonify(start_day_list)

# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_end_day_list = list(start_end_day)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return jsonify(start_end_day_list)

# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)
