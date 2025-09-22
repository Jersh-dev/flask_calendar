from flask import Flask, render_template, request,redirect, url_for, jsonify
from datetime import datetime
# Create the Flask app
app = Flask(__name__)

# Temporary in-memory store for events
# (will reset every time the app restarts)
events = []

@app.route("/")
def index():
    # Render the main HTML template (from templates/index.html)
    # Pass in the current list of events (though FullCalendar loads via /events)
    return render_template("index.html", events=events)

@app.route("/events")
def get_events():
    # Return all events as JSON so FullCalendar can load them
    return jsonify(events)

@app.route("/add", methods =["POST"])
def add_event():
    if request.method == "POST":
        # Grab form data from the request
        title = request.form.get("title")
        start = request.form.get("start")
        end = request.form.get("end")
        description = request.form.get("description")

    # Add the new event to the events list
        events.append({
            "title": title, #event title
            "start": start, #event start time
            "end": end, #event end time
            "description": description #event description
        })
        # Redirect user back to calendar after adding the event
        return redirect(url_for("index"))   
 
    # If GET request → show the form page
    return render_template("add_event.html")

if __name__ == "__main__":
    app.run(debug=True)