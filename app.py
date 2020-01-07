import os
import configparser
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import or_

"""
REST API with one method:
1) GET / call with the number parameter which returns all calls
(2 numbers, start / end time, cost), in which the number from
the parameter participated (that is, both incoming and outgoing).
Take data from the database. Data Format: JSON
"""

"""
Initializing Flask app and setting db connection for SQLAlchemy
and generate object for SQLAlchemy and Marshmallow
"""
app = Flask(__name__)
config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.ini"))
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://%s:%s@%s/%s" % (
    config["mysqlDB"]["user"],
    config["mysqlDB"]["password"],
    config["mysqlDB"]["host"],
    config["mysqlDB"]["database"],
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Calling(db.Model):
    Call_Id = db.Column(db.Integer, primary_key=True)
    first_number = db.Column(db.String(100))
    second_number = db.Column(db.String(100))
    start_call = db.Column(db.String(100))
    end_call = db.Column(db.String(100))
    cost = db.Column(db.Integer)

    def __init__(self, first_number, second_number, start_call, end_call, cost):
        self.first_number = first_number
        self.second_number = second_number
        self.start_call = start_call
        self.end_call = end_call
        self.cost = cost


class NumberSchema(ma.Schema):
    class Meta:
        fields = (
            "first_number",
            "second_number",
            "start_call",
            "end_call",
            "cost",
        )


number_schema = NumberSchema()
numbers_schema = NumberSchema(many=True)

"""
Set routes to “/calling” and HTTP method as GET, which can
we used for getting values from database in JSON format.
"""


@app.route("/calling", methods=["GET"])
def get_numbers():
    """
    Getting all values from database
    """
    all_numbers = Calling.query.all()
    result = numbers_schema.dump(all_numbers)
    return jsonify(result)


@app.route("/calling/<number>", methods=["GET"])
def get_number(number):
    """
    Getting all values in which the number from the parameter
    participated (that is, both incoming and outgoing).
    """
    records = Calling.query.filter(
        or_(
            Calling.first_number.like(f"%{number}%"),
            Calling.second_number.like(f"%{number}%"),
        )
    ).all()
    return numbers_schema.jsonify(records)


@app.route("/", methods=["GET"])
def get():
    return jsonify({"msg": "Hello"})


if __name__ == "__main__":
    app.run(debug=True)
