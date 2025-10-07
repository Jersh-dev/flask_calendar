# 🚀 Starter Template: Build Your Own Calendar App

## Use this as your starting point to code the consolidated form yourself!

from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta
import re

# Create the Flask app
app = Flask(__name__)

# In-memory storage (will reset when app restarts)
events = []
event_counter = 1

# Helper function - you'll implement this
def get_event_by_id(event_id):
    """Find an event by its ID"""
    # TODO: Your code here
    pass

# Exercise 1: Write the validation function
def validate_event_data(data, is_auto=False):
    """
    Validate event data and return list of errors
    
    Your task: Implement validation rules
    - Title: required, min 3 chars, max 200 chars
    - Description: required, min 10 chars, max 1000 chars (for manual events)
    - Start: required, must be in future (for manual events)
    - End: required, must be after start (for manual events)
    """
    errors = []
    
    # TODO: Add your validation logic here
    
    return errors

# Exercise 2: Write the event creation functions
def create_auto_event():
    """
    Create an auto-scheduled event (7 weeks from now, 9 AM, 2 hours)
    
    Your task: Return a dictionary with:
    - title: "Auto Scheduled DR Test"
    - start: 7 weeks from now at 9 AM (format: "YYYY-MM-DDTHH:MM")
    - end: 2 hours after start
    - description: "Automatically scheduled Disaster Recovery Test"
    - type: "auto"
    """
    # TODO: Calculate date 7 weeks from now
    # TODO: Set time to 9:00 AM
    # TODO: Return event dictionary
    pass

def create_manual_event(form_data):
    """
    Create a manual event from form data
    
    Your task: Extract and clean form data, return event dictionary
    """
    # TODO: Extract form fields
    # TODO: Clean data (strip whitespace)
    # TODO: Return event dictionary with type: "manual"
    pass

# Exercise 3: Write the main consolidated route
@app.route("/schedule_event", methods=["GET", "POST"])
def schedule_event():
    """
    Consolidated route for event scheduling
    
    Your task: 
    - GET: Show the form
    - POST: Process form, validate, create event, handle errors
    """
    global event_counter
    
    if request.method == "POST":
        # TODO: Get schedule_type from form
        # TODO: Create event based on type
        # TODO: Validate event data
        # TODO: If errors, show form with errors
        # TODO: If valid, save event and redirect
        pass
    
    # GET request - show form
    # TODO: Render the schedule_event.html template
    pass

# Exercise 4: Write the API endpoints
@app.route("/api/events", methods=["GET", "POST"])
def api_events():
    """
    API endpoint for events
    
    Your task:
    - GET: Return all events as JSON
    - POST: Create event from JSON data
    """
    if request.method == "GET":
        # TODO: Return JSON with all events
        pass
    
    elif request.method == "POST":
        # TODO: Get JSON data
        # TODO: Validate and create event
        # TODO: Return JSON response
        pass

# Basic routes (already implemented for you)
@app.route("/")
def index():
    """Main page - shows calendar"""
    return render_template("index.html", events=events)

@app.route("/events")
def get_events():
    """Return events as JSON for calendar display"""
    return jsonify(events)

# Legacy route for backward compatibility
@app.route("/add_event", methods=["GET", "POST"])
def add_event():
    """Redirect to new consolidated route"""
    return redirect(url_for("schedule_event"))

if __name__ == "__main__":
    app.run(debug=True)


# ============================================================================
# TEMPLATE STARTER: templates/schedule_event.html
# ============================================================================

'''
<!DOCTYPE html>
<html>
<head>
    <title>Schedule DR Test</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/schedule_event.css') }}">
</head>
<body>
    <h1>Schedule Disaster Recovery Test</h1>
    
    <!-- Exercise: Add error display -->
    {% if errors %}
    <div class="error-messages">
        <!-- TODO: Display error messages -->
    </div>
    {% endif %}
    
    <form method="POST" id="scheduleForm">
        <!-- Exercise: Add schedule type selection -->
        <div class="schedule-type">
            <!-- TODO: Add clickable options for auto/manual -->
        </div>
        
        <!-- Exercise: Add hidden field for schedule_type -->
        <!-- TODO: <input type="hidden" name="schedule_type" id="schedule_type" value="manual"> -->
        
        <!-- Exercise: Add manual form fields -->
        <div class="manual-form active" id="manual-form">
            <!-- TODO: Add form fields for title, start, end, description -->
        </div>
        
        <!-- Exercise: Add submit button -->
        <!-- TODO: Add submit and cancel buttons -->
    </form>
    
    <script src="{{ url_for('static', filename='js/schedule_event.js') }}"></script>
</body>
</html>
'''

# ============================================================================
# TESTING COMMANDS
# ============================================================================

'''
# Test the API with these curl commands:

# Get all events
curl -X GET http://localhost:5000/api/events

# Create auto event
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{"schedule_type": "auto"}'

# Create manual event
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "schedule_type": "manual",
    "title": "Test Event",
    "start": "2025-12-01T10:00",
    "end": "2025-12-01T12:00",
    "description": "This is a test event description"
  }'
'''