from flask import Flask, render_template, request
import json
import requests
from requests.auth import HTTPBasicAuth

CLIENT_ID = "e1f8b92a-f1e0-4634-ab36-fc2dbce549ff"
CLIENT_SECRET = "76bad7ba-947b-4a56-8fd3-e152bbb30bd0"

app = Flask(__name__)


@app.route('/my_account', methods=["GET"])
def render_account_page():
    return render_template("my_account.html")


@app.route('/my_account/vehicle', methods=["GET"])
def get_authorization_status():
    # key in the data will either be "code" for access allowed
    # key will be error and error_description for denied access

    data = request.args

    if data.get("error") is not None:
        return render_template("error_page.hteml")

    code = data.get("code")

    url = "https://auth.smartcar.com/oauth/token"
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://localhost:5000/my_account/vehicle'}

    r = requests.post(url, headers=header, data=data,
                      auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))

    r_dict = r.json()


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
