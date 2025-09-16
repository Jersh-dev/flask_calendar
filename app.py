from flask import Flask, render_template, request, jsonify

# Create the Flask app
app = Flask(__name__)

# Temporary in-memory store for events
# (will reset every time the app restarts)
events = []

@app.route("/")
def index():
    # Render the main HTML template (from templates/index.html)
    return render_template("index.html")

@app.route("/events")
def get_events():
    # Return all events as JSON so FullCalendar can load them
    return jsonify(events)

@app.route("/add", methods =["POST"])
def add_event():
    # Get the event data sent by the frontend (JSON body)
    data = request.get_json

    # Add the new event to the events list
    events.append({
        "title": data["title"], #event title
        "start": data["date"] #event date (FullCalendar uses ISO format)
    })

    # Send back confirmation to the frontend
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)