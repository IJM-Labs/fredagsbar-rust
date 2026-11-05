
from flask import Flask, request

app = Flask(__name__)


# midlertidig database
events = [{
    "id": 1,
    "title": "Quizaften",
    "date": "2023-11-15",
    "capacity": 3,
    "participants": ["osman", "jeppe"],
},
{
    "id": 2,
    "title": "ludoaften",
    "date": "2023-11-20",
    "capacity": 5,
    "participants": ["mads"],
},
{
    "id": 3,
    "title": "brætspilsaften",
    "date": "2023-11-25",
    "capacity": 2,
    "participants": [],
},
]


# find event ud fra id
def find_event(event_id):
    for event in events:
        if event["id"] == event_id:
            return event
    return None


#endpoint der viser, at api kald kører
@app.route("/")
def index():
    return {"message": "fredagsbar event api kører"}, 200


#returnerer alle events
@app.route("/events", methods=["GET"])
def get_events():
    return events, 200



#returnerer et event ud fra id
@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = find_event(event_id)
    if event is None:
        return {"error": "eventet findes ikke"}, 404

    return event, 200


#opretter et nyt event
@app.route("/events", methods= ["POST"])
def create_event():
    data = request.get_json(silent=True)

    # tjekker, at requesten indeholder json
    if not isinstance(data, dict):
        return {"error": "requesten skal indeholde JSON"}, 400

    title = data.get("title")
    date = data.get("date")
    capacity = data.get("capacity")

    # title og dato må ikke være tomme eller mangle 
    if not isinstance(title,str) or not title.strip():
        return {"error": "title er påkrævet"}, 400

    if not isinstance(date,str) or not date.strip():
        return {"error": "date er påkrævet"}, 400

    # capacity skal være et positivt heltal
    if(
        not isinstance(capacity, int)
        or isinstance(capacity, bool)
        or capacity <= 0
    ):
        return {"error": "capacity skal være et positivt heltal"}, 400

    # opretter et nyt event
    new_event = {
       "id": max((event["id"] for event in events), default=0) + 1,
        "title": title.strip(),
        "date": date.strip(),
        "capacity": capacity,
        "participants": [],
    }

    events.append(new_event)
    return new_event, 201


@app.route("/events/<int:event_id>/signups", methods=["POST"])
def signup(event_id):
    #tilmeld en person til et event
    event = find_event(event_id)

    if event is None:
        return {"error": "eventet findes ikke"}, 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "requesten skal indeholde JSON"}, 400

    name = data.get("name")

    if not isinstance(name,str) or not name.strip():
        return {"error": "name er påkrævet"}, 400

    name = name.strip()

    if name in event["participants"]:
        return {"error": "personen er allerede tilmeldt eventet"}, 409

    if len(event["participants"]) >= event["capacity"]:
        return {"error": "eventet er fuldt"}, 409

    event["participants"].append(name)

    return event, 201


@app.route("/events/<int:event_id>/signups/<string:name>", methods=["DELETE"])
def delete_signup(event_id, name):
    # sletter en person fra et event
    event =find_event(event_id)

    if event is None:
        return {"error": "eventet findes ikke"}, 404

    if name not in event["participants"]:
        return {"error": "personen er ikke tilmeldt eventet"}, 404

    event["participants"].remove(name)
    return "", 204


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # sletter et event
    event = find_event(event_id)

    if event is None:
        return {"error": "eventet findes ikke"}, 404
        

    events.remove(event)
    return "", 204

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port=5001, debug=True)
    





    




    


