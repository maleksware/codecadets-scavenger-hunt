from flask import Flask, request, make_response, render_template
import uuid


global registered_users
registered_users = {}
station_mapping = {}

next_station = {"start": 9262, 9262: 3146, 3146: 1668, 1668: 9145, 9145: 6596, 6596: 3374, 3374: 3232, 3232: 8374, 8374: 2498, 2498: 4779}

station_uuids = [9262, 3146, 1668, 9145, 6596, 3374, 3232, 8374, 2498, 4779]
station_questions = [
    "Welcome to the CodeCadets Wrapped Scavenger Hunt! Go to the printer on level 3 for your next clue.",
    "-... .. -. / --- -. / .-.. ...- .-.. / ..--- ",
    "01000011 01101000 01100101 01100011 01101011 00100000 01110100 01101000 01100101 00100000 01010000 01101001 01100001 01101110 01101111",
    "⠝⠑⠭⠞ ⠉⠇⠥⠑ ⠤ ⠇⠧⠇ ⠒ ⠎⠉⠥⠇⠏⠞⠥⠗⠑",
    "R28gdG8gdGhlIG1haW50ZW5hbmNlIGN1cGJvYXJkIG9uIEx2bCAy=",
    "43 68 65 63 6b 20 74 68 65 20 46 6f 6f 64 20 43 6f 72 6e 65 72 20 6f 6e 20 4c 76 6c 20 31",
    r"SC%C2%B2%E2%81%B0%E2%81%B6",
    "902953 7924613 (Hint: Look Around...)",
    "103 150 145 143 153 40 164 150 145 40 114 145 147 157 40 127 141 154 154",
    "Congratulations! You have completed the Scavenger Hunt! Please return to the start (2nd floor) so we can record your points.",
]


class Station:
    def __init__(self, question, id, number):
        self.question = question
        self.id = id
        self.number = number


class User:
    def __init__(self, uuid, progress):
        self.uuid = uuid
        self.progress = progress


for i in range(len(station_questions)):
    station_mapping[station_uuids[i]] = Station(station_questions[i], station_uuids[i], i + 1)

app = Flask(__name__)

@app.route("/start")
def reg_new_user():
    global registered_users
    new_user_id = str(uuid.uuid4())

    resp = make_response(render_template("index.html", question=station_mapping[next_station["start"]].question))
    resp.set_cookie("uuid", new_user_id, max_age=60*60*24)

    registered_users[new_user_id] = User(new_user_id, 0)

    return resp

@app.route("/station/<int:station_id>")
def process_station(station_id):
    if station_id in station_mapping:
        cur_user_id = request.cookies.get("uuid")
        global registered_users

        if cur_user_id in registered_users:
            cur_station = station_mapping[station_id].number
            user_progress = registered_users[cur_user_id].progress # last visited station

            if cur_station <= user_progress + 1:
                registered_users[cur_user_id].progress = cur_station
                return make_response(render_template("index.html", question=station_mapping[next_station[station_id]].question))
            else:
                return make_response(render_template("dont_shortcut.html"))
        else:
            return make_response(render_template("not_registered.html"))
    else:
        return make_response(render_template("no_station.html"))
