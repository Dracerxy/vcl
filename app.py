
import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request,render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import instances
#test variables
global name
global port
name=" "
app = Flask("VC-Labs")
app.secret_key = "virtual computer lab"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "958768145034-v0gsctgs4409q7tqmmm30a72cv0mmge2.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)
@app.route("/login_validation")
def login_validation():

    return 
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

@app.route("/signup",methods=["GET","POST"])
def sign_up():
    if request.method=="POST":
        usrname=request.form.get("user_name")
        email=request.form.get("g_mail")
        passwd=request.form.get("passwd")

    return redirect("/")
@app.route("/validation",methods=["GET","POST"])
def login_val():
    if request.method=="POST":
        mail=request.form.get("mail")
        passd=request.form.get("passd")
    return redirect("/")
@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    global name
    global port
    name=session["name"]
    port=instances.instance_creation(name.replace(" ","_"))

    return redirect("/protected_area")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return render_template("index.html")
    #"Hello World <a href='/login'><button>Login</button></a>"


@app.route("/protected_area")
@login_is_required
def protected_area():
    global name
    global port
    p=port
    u=name
    u=u.replace(" ","_")
    return render_template("index_1.html",user_name=u,port_no=p)

if __name__ == "__main__":
    os.system("docker start $(docker ps -a -q)")
    app.run(debug=True)
