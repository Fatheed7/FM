from flask import (Flask, redirect, url_for)
import os
from scout_apm.flask import ScoutApm
from memory_profiler import profile

if os.path.exists("env.py"):
    import env

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
ScoutApm(app)

app.config["SCOUT_MONITOR"] = True
app.config["SCOUT_KEY"] = os.environ.get("SCOUT_KEY")
app.config["SCOUT_NAME"] = "FM_RECRUITMENT"

@app.route('/')
def index():
    target_url = 'https://fm-client-app.vercel.app/'
    return redirect(target_url)


@app.route('/<path:invalid_route>')
def invalid_route(invalid_route):
    # Route back to index page on invalid route
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
