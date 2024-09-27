import requests
import os
import json
from flask import Flask, request, abort

app = Flask(__name__)


def get_user(domain, user):
    wakatime_url = "https://{}/api/v1/users/{}/stats".format(domain, user)
    wakatime_key = os.environ.get("WAKATIME_KEY")

    headers = {
        "Authorization": "Bearer {}".format(wakatime_key),
        "Content-Type": "application/json",
    }

    response = requests.get(wakatime_url, headers=headers)

    if response.status_code != 200:
        print("Error: {}".format(response.text))

    langs = response.json()["data"]["languages"]

    result = {}
    for lang in langs:
        if lang["name"] != "unknown":
            digital = lang["digital"]
            hours, minutes, seconds = digital.split(":")
            time = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
            result[lang["name"]] = time

    return result


@app.route("/")
def index():
    username = request.args.get("user")
    domain = request.args.get("domain")
    if username and domain:
        stats = get_user(domain, username)
        return json.dumps(stats)
    else:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)
