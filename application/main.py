from flask import Flask, session
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')
app.secret_key = "esof_3675" # secret key for extra session
# main function
if __name__ == "__main__":
    app.run(host="10.100.25.158", port=5000,debug=True)