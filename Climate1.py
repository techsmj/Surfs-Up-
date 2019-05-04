import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify,render_template


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def index():

    

    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/precipitation<br/>"
        f"/api/stations<br>"
        f"/api/temperature<br>"
    )


@app.route("/api/precipitation")
def precipitation():
    """Return a list of all precipatition for date"""
    # Query all passengers
    scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-22').\
                    order_by(Measurement.date).all()
  # Convert list of tuples into normal list
    #all_names = list(np.ravel(scores))
    
    all_prcp = []
    for  date, prcp in scores:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp

        all_prcp.append(precipitation_dict)

  

    return jsonify(all_prcp)

@app.route("/api/stations")
def stations():
    """Return a list of all passenger names"""
    # Query all passengers
    station= session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).\
                    order_by(func.count(Measurement.station).desc()).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station))
    
    return jsonify(all_stations)

@app.route("/api/temperature")
def temperature():
    """Return a list of temperature"""
    # Query all passengers
    temps= session.query( Measurement.date, Measurement.tobs).filter(Measurement.station=="USC00519281", Measurement.date > '2016-08-19').\
                    order_by(Measurement.date).all()
    # Convert list of tuples into normal list
    all_temp = list(np.ravel(temps))

    return jsonify(all_temp)


@app.route("/api/<start_date>")
def calc_temps(start_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
 
    start_results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date == start_date).all()

    data1_list = []
    for x in start_results:
        table = {}
        table["Start Date"] = start_date
        table["Average Temperature"] = float(x[0])
        table["Highest Temperature"] = float(x[1])
        table["Lowest Temperature"] = float(x[2])
        data1_list.append(table)
    return jsonify(data1_list)
#print(calc_temps('2012-02-28', '2012-03-05'))

@app.route("/api/<start_date>/<end_date>")

def calc_temp(start_date, end_date):
    
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
 
    results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    data_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Average Temperature"] = float(result[0])
        row["Highest Temperature"] = float(result[1])
        row["Lowest Temperature"] = float(result[2])
        data_list.append(row)
    return jsonify(data_list)  


if __name__ == '__main__':
    app.run(debug=True)
