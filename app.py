
# Import dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database setup
engine = create_engine("sqlite:///Resources//hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#Database setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    precipitation = session.query(Measurement.date, Measurement.prcp).all()
    session.close
    preciptation_dict = []
    for date, prcp in precipitation:
            preciptation_dict[date] = prcp
    return jsonify(preciptation_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station, Station.name).all()
    session.close
    station_list = list(np.ravel(stations))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    mostactive = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).limit(5).all()
    onemostactive = mostactive[0][0]
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    ayearagodate = (dt.datetime.strptime(most_recent_date[0], '%Y-%m-%d') - dt.timedelta(days=365)).date()
    twelve_month_station = session.query(Measurement.tobs).filter(Measurement.station == onemostactive).\
                                                        filter(Measurement.date >= ayearagodate).all()
    session.close
    return jsonify(twelve_month_station)

if __name__ == "__main__":
    app.run(debug=True)

