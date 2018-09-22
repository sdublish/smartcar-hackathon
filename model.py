"""Models and database functions for smartcar_hackathon db."""

# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


db = SQLAlchemy()


##############################################################################

class User(db.Model):
    """User model."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(110), nullable=False)
    create_date = db.Column(db.DateTime)
    authorization_key = db.Column(db.String(100))
    zipcode = db.Column(db.Integer)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} fname={} lname={} email={}>".format(self.user_id, self.fname,
                                                                                 self.lname, self.email)
class Vehicle(db.Model):
    """Vehicle model."""

    __tablename__ = "vehicles"

    model_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    vehicle_make = db.Column(db.String(75), nullable=False)
    vehicle_model_name = db.Column(db.String(100), nullable=False)
    vehicle_year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Vehicle_id={} Vehicle_make={} Vehicle_model={} Vehicle_year={} Last_service={}>".format(self.vehicle_id, self.vehicle_make,
                                                                                                    self.vehicle_model, self.vehicle_year)


class UserVehicle(db.Model):
    """Individual vehicles."""

    __tablename__ = "uservehicles"

    uservehicle_id = db.Column(db.String(60), nullable=False, primary_key=True)
    nickname = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    model_id = db.Column(db.Integer, db.ForeignKey('vehicles.model_id'))
    #last tire odometer goes here


    #Define relationship to user
    user = db.relationship("User", backref=db.backref("uservehicles"), order_by=uservehicle_id)

    #Define relationship to model
    model = db.relationship("Vehicle", backref=db.backref("uservehicles"), order_by=uservehicle_id)    





class Service(db.Model):
    """Services."""

    __tablename__ = "services"

    service_id = db.Column(db.Integer, nullable=False, primary_key=True)
    service_name = db.Column(db.String(100))
    model_id = db.Column(db.Integer, db.ForeignKey('vehicles.model_id'))

    #Define relationship to model
    model = db.relationship("Vehicle", backref=db.backref("services"), order_by=service_id)    



class UserVehicleService(db.Model):
    """Services needed and completed by Individual vehicles."""

    __tablename__ = "uservehicleservices"

    uservehicleservice_id = db.Column(db.Integer, nullable=False, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'))
    uservehicle_id = db.Column(db.String(60), db.ForeignKey('uservehicles.uservehicle_id'))
    #odometer suggested here
    #odometer completed here

    #Define relationship to service
    service = db.relationship("Service", backref=db.backref("uservehicleservices"), order_by=uservehicleservice_id)

    #Define relationship to uservehicle
    uservehicle = db.relationship("UserVehicle", backref=db.backref("uservehicleservices"), order_by=uservehicleservice_id)



class YelpCategory(db.Model):
    """Yelp Categories."""

    __tablename__ = "yelpcategories"

    yelpcategory_id = db.Column(db.String(40), nullable=False, primary_key=True)
    yelpcategory_search = db.Column(db.String(40), nullable=False)
 


class YelpCategoryService(db.Model):
    """Relational Table betweServices."""

    __tablename__ = "yelpcategoryservices"

    yelpcategoryservice_id = db.Column(db.Integer, nullable=False, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'))
    yelpcategory_id = db.Column(db.String(40), db.ForeignKey('yelpcategories.yelpcategory_id'))

    #Define relationship to service
    service = db.relationship("Service", backref=db.backref("yelpcategoryservice"), order_by=yelpcategoryservice_id)

    #Define relationship to yelpcategory
    yelpcategory = db.relationship("YelpCategory", backref=db.backref("yelpcategorieservices"), order_by=yelpcategoryservice_id)





##############################################################################
# Helper functions


def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")


def connect_to_db(app, db_uri='postgres:///servicecar'):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    init_app()
