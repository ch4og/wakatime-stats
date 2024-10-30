import requests
import json
from flask import Flask, request, abort

app = Flask(__name__)


def get_user(domain, user):
    wakatime_url = "https://{}/api/v1/users/{}/stats".format(domain, user)

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.get(wakatime_url, headers=headers)

    if response.status_code != 200:
        print("Error: {}".format(response.text))

    data = response.json()["data"]
    langs = data["languages"]

    result = {}
    stoplist = ["unknown", "markdown", "json", "yaml", "text", "xml", "css"]
    for lang in langs:
        if lang["name"].lower() not in stoplist:
            digital = lang["digital"]
            hours, minutes, seconds = digital.split(":")
            time = f"{int(hours)}h {int(minutes)}m"
            result[lang["name"]] = time

    return result


def get_total(domain, user):
    wakatime_url = "https://{}/api/v1/users/{}/stats".format(domain, user)

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.get(wakatime_url, headers=headers)

    if response.status_code != 200:
        print("Error: {}".format(response.text))

    data = response.json()["data"]
    langs = data["languages"]
    for lang in langs:
        if lang["name"] == "unknown":
            unknown = lang["total_seconds"]
            break

    result = {}
    total_seconds = data["total_seconds"] - unknown
    result["total"] = f"{int(total_seconds/3600)}h {int(total_seconds%3600/60)}m"

    return result


@app.route("/")
def index():
    username = request.args.get("user")
    domain = request.args.get("domain")
    total = request.args.get("total")
    if username and domain and total:
        if total == "true":
            total = get_total(domain, username)
            return json.dumps(total)
        else:
            abort(403)
    elif username and domain:
        stats = get_user(domain, username)
        return json.dumps(stats)
    else:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)
