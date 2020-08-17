#Import Dependencies 
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#Setup Database 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect an existing database into the model
Base = automap_base()

#Reflect tables 
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Setup Flask 
app = Flask(__name__)

#Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"AvailableRoutes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"     
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
#     #Create a link from Python to the DB
    session = Session(engine)

    #query results to a dictionary
    results = session.query(Measurement.date, Measurement.prcp).all()

    #session.close()
    precipitation_data = []

    for x in results:
        precipitation_data_dict = {}
        precipitation_data_dict[x[0]] = x[1]
        precipitation_data.append(precipitation_data_dict)

    session.close()
    
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
#     #Create a link 
    session = Session(engine)

    results1 = session.query(Station.station).all()

    session.close()

    return jsonify(results1)

@app.route("/api/v1.0/tobs")
def tobs():
    #Create a link
    session = Session(engine)
    
    previous_year = dt.date(2017,8,23)- dt.timedelta(days=365)
    
    last_12_months= session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= previous_year).\
    filter(Measurement.station == 'USC00519281').\
    order_by(Measurement.tobs).all()

    temp_data = []

    for x in last_12_months:
       temp_data_dict = {}
       temp_data_dict[x[0]] = x[1]
       temp_data.append(temp_data_dict)

    session.close()

    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def one_date(start):

    session = Session(engine)

    temp_result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    one_date = []

    for y in temp_result:
        temp_result_dict = {}
        temp_result_dict["Minimum Temp"]=temp_result[0][0]
        temp_result_dict["Max Temp"]=temp_result[0][2]
        temp_result_dict["Avg Temp"]=temp_result[0][1]
        one_date.append(temp_result_dict)
    
    session.close()

    return jsonify(one_date)

@app.route("/api/v1.0/<start>/<end>")
def two_date(start,end):   

    session = Session(engine)

    temp_result1 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    two_date = []

    for i in temp_result1:
        temp_result1_dict = {}
        temp_result1_dict["Minimum Temp"]=temp_result1[0][0]
        temp_result1_dict["Max Temp"]=temp_result1[0][2]
        temp_result1_dict["Avg Temp"]=temp_result1[0][1]
        two_date.append(temp_result1_dict)

    session.close()

    return jsonify(two_date)


if __name__ == '__main__':
    app.run(debug=True)