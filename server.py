from flask import Flask, render_template, request, session, flash
import json
import requests
from requests.auth import HTTPBasicAuth
import os
from flask_sqlalchemy import SQLAlchemy
import smartcar


client = smartcar.AuthClient(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    redirect_uri='http://localhost:5000/my_account/vehicle',
    scope=['read_vehicle_info', 'read_location', 'read_odometer']
)

# need to add yelp api key to secrets.sh
YELP_API_KEY  = os.environ["YELP_API_KEY"]
app = Flask(__name__)
# need to define secret key here!
app.secret_key = os.environ["FLASK_SECRET_KEY"]




@app.route("/registration", methods=["GET"])
def render_registration_form():
    """render registration form"""

    return render_template("home.html")


@app.route("/registration", methods=["POST"])
def get_user_info():
    """get user info and add info to db"""
    #f_name = request.form.get
    #l_name = request.form.get
    #email = request.form.get
    # birthday = request.form.get
    # password = request.form.get
    create_date = datetime.datetime.utcnow()
    authorization_key = access_token = r_dict["access_token"]
    #zipcode = requst.form.get

    user = User(f_name=f_name, l_name=l_name, email=email, birthday=birthday,
                password=password, create_date=create_date,
                authorization_key=authorization_key, zipcode=zipcode)

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return redirect("/login")


@app.route("/login", methods=["GET"])
def render_login_form():
    """render template for login form"""
    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def user_login():
    """ checks user login info against the info saved in db """

    # email_address = request.form.get("user_email")
    password = request.form.get("user_password")

    # check to see if this user exists in our db
    # client = User.query.filter(User.email == email_address).first()

    # if user does not exist, have user register
    if client is None:
        flash("No User Found, Please Register")
        return redirect("/registration")
    # if user exists, then check the password
    else:
        if client.check_password(password):
            session["user_id"] = client.user_id

            user_id = User.query.get(session["user_id"])

            user = User.query.filter(User.user_id == user_id).first()

            authorization_key = user.authorization_key

            refresh_token = authorization_key["refresh_token"]

            r = client.exchange_refresh_token(refresh_token)

            r_dict = json.dumps(r)

            new_auth_key = r_dict["access_token"]

            user.authorization_key = new_auth_key

            db.session.commit()

            return redirect("/home")

        else:
            flash("Password is Incorrect, Please try Again")
            return redirect("/login")



@app.route('/home', methods=["GET"])
def render_account_page():
    auth_url = client.get_auth_url(force=True)
    # query the database for the user profile section
    # make sure there is a connect the car button on this page
    # make sure there is a service shop button
    # query the database for vehicle info
    # query the database for services needed

    # when the user marks the service as completed, then change the status to
    # completed

    # use absolute milage when calculating services needed

    user_id = User.query.get(session["user_id"])

    user = User.query.filter(User.user_id == user_id).first()

    auth_key = user.authorization_key["access_token"]

    response = client.get_vehicle_ids(auth_key, offset=0, limit=20)

    vid = response['vehicles'][0]

    vehicle = smartcar.Vehicle(vid, auth_key)

    vehicle_info = vehicle.info()

    vehicle_make = vehicle_info["make"]
    vehicle_model = vehicle_info["model"]
    vehicle_year = vehicle_info["year"]

    vehicle = Vehicle.query.filter(Vehicle.vehicle_make == vehicle_make and
                                   Vehicle.vehicle_model_name == vehicle_model
                                   and Vehicle.vehicle_year == vehicle_year).one()


    

    db.session.add(car)
    db.session.commit()

    return render_template("home.html")


@app.route('/my_account/vehicle', methods=["GET"])
def get_authorization_status():
    # key in the data will either be "code" for access allowed
    # key will be error and error_description for denied access

    data = request.args

    r_dict = json.dumps(data)

    if data.get("error") is not None:
        return render_template("error_page.hteml")

    code = request.args.get('code')

    access = client.exchange_code(code)

    user = User.query.get(session["user_id"])

    user.authorization_key = code

    db.session.commit()

    return redirect("/home")


@app.route('/service_shops', methods=["GET"])
def get_service_shops():

    # things i need to do:
    # need to get vehicle location
    # have access to user id
    # so
    # query user from database
    # get vehicle associated with user
    # get vehicle info (need access token associated with user)
    # so will need to do a check to make sure access token is valid (consider writing this into a function)

    user_id = session.get("user_id")
    user = User.query.get(user_id).first()
    vehicle = UserVehicle.query.filter_by(user_id=user_id).first()
    # may need to check if key has expired or not here
    sm_vehicle = smartcar.Vehicle(vehicle.uservehicle_id, user.authorization_key)

    location = sm_vehicle.location()

    # querying yelp api below
    yelp_url = "https://api.yelp.com/v3/businesses/search"
    header = {"Authorization": "Bearer {}".format(YELP_API_KEY)}
    # probably want to make categories something which varies depending on what service is required
    # will need to do something to set that up
    categories = "autorepair"
    payload = {"latitude": location["latitude"], "longitude": location["longitude"],
               "radius": 20000, "sort_by": "distance", "categories": categories}

    response = requests.get(yelp_url, headers=header, params=payload)
    # check here if response goes through fine?
    return response.text["businesses"]

@app.errorhandler(404)
def page_not_found(error):
    return json.dumps({"status": "404", "reason": "endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return json.dumps({"status": "500", "reason": "server failure"}), 500


@app.errorhandler(405)
def method_error(error):
    return json.dumps({"status": "405", "reason": "method is not allowed"}), 405


@app.errorhandler(400)
def bad_request(error):
    return json.dumps({"status": "400", "reason": "invalid request"}), 400


###############################################################################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
