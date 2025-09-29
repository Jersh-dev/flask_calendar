# app.py
# This is the python application for the Flask Calendar Project

from flask import Flask, render_template, request,redirect, url_for, jsonify
from datetime import datetime, timedelta

# Create the Flask app
app = Flask(__name__)

# Temporary in-memory store for events
# (will reset every time the app restarts)
events = []
event_counter = 1

def get_event_by_id(event_id):
    for ev in events:
        if ev["id"] == event_id:
            return ev
    return None

def save_event(updated_event):
    for i, ev in enumerate(events):
        if ev["id"] == updated_event["id"]:
            events[i] = updated_event
            return 



@app.route("/auto_schedule", methods =["POST"])
def auto_schedule():
    global event_counter
    """Automatically schedule a Disaster Recovery Test 7 weeks from today"""
    auto_date = datetime.now() + timedelta(weeks=7)

    event = {
        "id": event_counter,
        "title": "Auto Scheduled DR Test",
        "start": auto_date.strftime("%Y-%m-%dT%H:%M"),
        "end": (auto_date + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M"), # example end time
        "description": "Automated DR Test"
    }
    events.append(event)
    event_counter += 1
    return redirect(url_for("index"))


@app.route("/")
def index():
    # Render the main HTML template (from templates/index.html)
    # Pass in the current list of events (though FullCalendar loads via /events)
    return render_template("index.html", events=events)

@app.route("/events")
def get_events():
    # Return all events as JSON so FullCalendar can load them
    return jsonify(events)

@app.route("/edit_event/<int:event_id>", methods =["GET", "POST"])
def edit_event(event_id):
    # Get the event from your storage (db, JSON, etc.)
    event = get_event_by_id(event_id)# You'll need to implement this

    if request.method == "POST":
        # Update event with new form data
        event["title"] = request.form["title"]
        event["start"] = request.form["start"]
        save_event(event)# You'll need to implement this
        return redirect(url_for("index"))
    return render_template("edit_event.html", event=event)

@app.route("/add_event", methods =["GET", "POST"])
def add_event():
    global event_counter
    if request.method == "POST":
        # Grab form data from the request
        title = request.form.get("title")
        start = request.form.get("start")
        end = request.form.get("end")
        description = request.form.get("description")

    # Add the new event to the events list
        events.append({
            "id": event_counter, #assign a unique ID
            "title": title, #event title
            "start": start, #event start time
            "end": end, #event end time
            "description": description #event description
        })
        event_counter += 1
        # Redirect user back to calendar after adding the event
        return redirect(url_for("index"))   

    # If GET request → show the form page
    return render_template("add_event.html")

if __name__ == "__main__":
    app.run(debug=True)