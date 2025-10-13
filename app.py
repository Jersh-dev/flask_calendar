# app.py
# This is the main Flask application for the Calendar Project
# It demonstrates a consolidated form approach with API capabilities

# Import necessary modules from Flask framework
from flask import Flask, render_template, request,redirect, url_for, jsonify
# datetime for handling date/time operations, timedelta for date arithmetic
from datetime import datetime, timedelta
# re module for regular expressions (used in validations)
import re


# Create the Flask app
# __name__ tells Flask where to look for templates and static files
app = Flask(__name__)

# ============================================================================
# DATA STORAGE - In-Memory (Development Only)
# ============================================================================
# In a production app, you would use a database like PostgreSQL or MySQL
# This list will reset every time the app restarts (not persistent)
events = [] # List to store all event dictionaries
event_counter = 1 # Simple counter to assign unique IDs to events

# ============================================================================
# HELPER FUNCTIONS - Utility functions for event management
# ============================================================================
def get_event_by_id(event_id):
    """
    Find and return an event by its unique ID.
    
    Args:
        event_id (int): The unique identifier for the event
        
    Returns:
        dict or None: The event dictionary if found, None if not found
        
    This function demonstrates linear search through a list.
    In a database application, this would be a SQL SELECT query.
    """
    for ev in events:
        # Check if current event's ID matches what we're looking for
        if ev["id"] == event_id:
            return ev # Event found
    return None # Event not found

def save_event(updated_event):
    """
    Update an existing event in the events list.
    
    Args:
        updated_event (dict): Event dictionary with updated information
        
    This function finds the event by ID and replaces it with new data.
    In a database application, this would be a SQL UPDATE query.
    """
    # Use enumerate to get both index and event object
    for i, ev in enumerate(events):
        # Find the event with matching ID
        if ev["id"] == updated_event["id"]:
            # Replace the old event with the updated one
            events[i] = updated_event
            return 
def validate_event_data(data, is_auto=False):
    """
    Comprehensive validation function for event data.
    
    This function implements both client-side and server-side validation rules.
    It's designed to prevent invalid data from entering the system and provide
    clear feedback to users about what needs to be fixed.
    
    Args:
        data (dict): Form data or JSON data containing event information
        is_auto (bool): If True, skip validation (auto events are pre-validated)
        
    Returns:
        list: List of error messages (empty if no errors)
        
    Validation Rules:
    - Title: Required, minimum 3 characters, maximum 200 characters
    - Start Date: Required, must be in the future, valid datetime format
    - End Date: Required, must be after start date, valid datetime format
    - Description: Required, minimum 10 characters, maximum 1000 characters
    """
    errors = [] # Initialize empy list to collect error messages
    if not is_auto:
        # Only validate manual events - auto events have predefined valid data

        # ===== TITLE VALIDATION =====
        # Check if title exists and meets length requirements
        if not data.get('title') or len(data['title'].strip()) < 3:
            errors.append("Title must be at least 3 characters long")
        elif len(data['title'].strip()) > 200:
            errors.append("Title must be less than 200 characters")

        # ===== START DATE VALIDATION =====
        if not data.get('start'):
            errors.append("Start date and time are required")
        else:
            try:
                # Parse the ISO format datetime string (YYYY-MM-DDTHH:MM)
                start_dt = datetime.fromisoformat(data['start'])
                # Ensure the event is scheduled for the future
                if start_dt < datetime.now():
                    errors.append("Start dates cannot be in the past")
            except ValueError:
                # Handle invalid datetime format
                errors.append("Invalid start date format")

        # ===== END DATE VALIDATION =====
        if not data.get('end'):
            errors.append("End date and time are required")
        else:
            try:
                # Parse the end datetime
                end_dt = datetime.fromisoformat(data['end'])
                # Cross-validate with start date if it exists
                if data.get('start'):
                    start_dt = datetime.fromisoformat(data['start'])
                    # Ensure logical time ordering (end after start)
                    if end_dt <= start_dt:
                        errors.append("End time must be after start time")
            except ValueError:
                errors.append("Invalid end date format")

        # ===== DESCRIPTION VALIDATION =====
        if not data.get('description') or len(data['description'].strip()) < 10:
            errors.append("Description must be at least 10 characters long")
        elif len(data['description'].strip()) > 1000: 
            errors.append("Description must be less than 1000 characters")

    return errors   # Return list of errors (empty if validation passed)
                      
def create_auto_event():
    """
    Create an automatically scheduled Disaster Recovery test event.
    
    This function demonstrates the Factory Pattern - it creates a standardized
    event object with predefined values. Auto events are scheduled exactly
    7 weeks (49 days) from the current date and time.
    
    Business Rules for Auto Events:
    - Scheduled 7 weeks in the future (business requirement)
    - Set to 9:00 AM (standard business hours)
    - Duration of 2 hours (typical DR test duration)
    - Standardized title and description
    
    Returns:
        dict: Complete event dictionary ready to be saved
    """
    #Calculate target date: current date + 7 weeks
    auto_date = datetime.now() + timedelta(weeks=7)

    # Set to business hours (9 AM) and clear seconds/microseconds for clean time
    # replace() creates a new datetime object with specified components changed    
    auto_date = auto_date.replace(hour = 9, minute = 0, second = 0, microsecond = 0)

    #Return a complete event dictionary with all required fields
    return {
        "title" : "Auto Scheduled DR Test", #Standardized title
        # Format datetime as ISO string for HTML datetime-local inputs
        "start": auto_date.strftime("%Y-%m-%dT%H:%M"),
        # End time is start time + 2 hours
        "end" : (auto_date + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M"),
        "description" : "Automatically scheduled Disaster Recovery Test - 7 weeks from creation date",
        "type" : "auto" # Mark as auto generated for tracking purposes
        }

def create_manual_event(form_data):
    """
    Create a manual event from user-provided form data.
    
    This function also uses the Factory Pattern but creates events from
    user input rather than predefined values. It's responsible for
    data cleaning and structuring.
    
    Args:
        form_data (dict): Raw form data from request.form or JSON
        
    Returns:
        dict: Cleaned and structured event dictionary
        
    Data Cleaning Process:
    - Strip whitespace from text fields
    - Preserve datetime strings as-is (already validated)
    - Add event type marker for tracking
    """    
    return {
        # Clean text fields by removing leading/trailing whitespace
        "title": form_data['title'].strip(),
        # Datetime fields are used as-is (HTML datetime-local format)
        "start": form_data['start'],
        "end": form_data['end'],
        # Clean description text
        "description": form_data['description'].strip(),
        "type": "manual"  # Mark as user-created for tracking purposes
    }    

# ============================================================================
# FLASK ROUTES - URL endpoints that handle HTTP requests
# ============================================================================

@app.route("/")
def index():
    """
    Home Page route - displayes the main calendar interface.

    This is the root URL (/) of the application. When users visit
    http://localhost:5000, this function is called.
    
    Returns:
        str: Rendered HTML template with event data
        
    Template Context:
        events (list): All events passed to template for server-side rendering
        (Though the calendar itself loads events via AJAX from /events)    
    """

    # render_template() loads the HTML template and injects Python variables
    # The template can access 'events' variable using Jinja2 syntax {{ events }}
    return render_template("index.html", events=events)

@app.route("/events")
def get_events():
    """
    API endpoint to return all events as JSON.
    
    This route is called by JavaScript in the browser to load calendar events
    dynamically. It's an example of a simple REST API endpoint.
    
    Returns:
        Response: JSON array of all events
        
    Response Format:
        [
            {
                "id": 1,
                "title": "Event Title",
                "start": "2025-10-15T09:00",
                "end": "2025-10-15T11:00",
                "description": "Event description",
                "type": "manual"
            },
            ...
        ]
    """
    # Jsonify() converts Python list/dict to JSON response with proper headers
    return jsonify(events)

@app.route("/edit_event/<int:event_id>", methods =["GET", "POST"])
def edit_event(event_id):
    """
    Edit an existing event route.
    
    This route demonstrates URL parameters (<int:event_id>) and handles both
    displaying the edit form (GET) and processing the update (POST).
    
    Args:
        event_id (int): The unique ID of the event to edit (from URL)
        
    Returns:
        GET: Rendered edit form with current event data
        POST: Redirect to home page after successful update
    """

    # Find the event to edit using our helper function
    event = get_event_by_id(event_id)

    #Handle form submission (POST request)
    if request.method == "POST":
           # Update event with new form data
           # In a real app, you'd validate this data first
           event["title"] = request.form["title"]
           event["start"] = request.form["start"]
           #Save the updated event back to storage
           save_event(event)
           #Redirect to home page using url_for() for URL Generation
           return redirect(url_for("index"))
    
    # Handle form display (GET request)
    # Pass the current event data to pre-populate the form    
    return render_template("edit_event.html", event=event)

@app.route("/add_event", methods =["GET", "POST"])
def add_event():
    """
    Consolidated route for both manual and automatic event scheduling.
    
    This is the main deliverable - a robust, consolidated form that can handle
    both manual and automatic event scheduling. This route demonstrates:
    
    1. Form consolidation - One interface for multiple event types
    2. API integration readiness - Designed for external application use
    3. Comprehensive validation - Multi-layer error checking
    4. Factory pattern - Different creation methods for different event types
    5. Flexible response handling - Web forms or JSON API responses
    
    The route determines the scheduling type and creates the appropriate event,
    making it suitable for integration into other web applications via API.
    """

    global event_counter

    if request.method == "POST":
        #Determine scheudling method from form data
        # This SPOE handles both manual and auto scheduling
        schedule_type = request.form.get("schedule_type")

        if schedule_type == "auto":
            #Auto-schedule DR test using our factory function
            #this creates events automatically based on system availability
            event_data = create_auto_event()
            #Validate the auto-generated event data
            errors = validate_event_data(event_data, is_auto=True)
        else:
            # Manual event creation from user input
            # User provides specific date, time, and details
            event_data = create_manual_event(request.form)
            # Validate the user-provided form data
            errors = validate_event_data(request.form, is_auto=False)

        if errors:
            # Return form with error messages and preserve user input
            # This prevents users from losing their data on validation errors
            return render_template("schedule_event.html", errors=errors, form_data = request.form)
        
        # No errors - create and save the event
        # Assign unique ID and add to our event storage
        event_data["id"] = event_counter
        events.append(event_data)
        event_counter += 1 

        #Smart response handling for both web forms and API Calls
        #check if this is an API request(JSON content tyupe or api parameter)
        if request.headers.get('Content-Type') == 'application/json' or request.args.get('api') == 'true':
            # Return JSON response for API Integration
            return jsonify({
                "success" : True,
                "message" : "Event scheduled successfully",
                "event" : event_data
            }), 201
        
        # Regular web for submission - redirect to prevent duplicate submissions
        return redirect(url_for("index"))

    #GET request - display the consolidated scheduling form
    return render_template("schedule_event.html")


@app.route("/schedule_event", methods=["GET"])
def schedule_event():
    """
    Route to render the consolidated scheduling form (GET only).
    This provides a stable endpoint used by templates and links.
    """
    return render_template("schedule_event.html")


@app.route("/auto_schedule", methods=["POST"])
def auto_schedule():
    """
    Create an auto-scheduled event (7 weeks from now) and redirect to index.
    """
    global event_counter
    event = create_auto_event()
    event["id"] = event_counter
    events.append(event)
    event_counter += 1
    return redirect(url_for("index"))

# API Endpoints for external integration
# These endpoints allow other applications to interact with our calendar system

@app.route("/api/events", methods=["GET", "POST"])
def api_events():
    """
    RESTful API endpoint for event management.
    
    This endpoint provides programmatic access to the event system, making it
    suitable for integration with other applications, mobile apps, or external
    services. It follows REST conventions for predictable API behavior.
    
    GET: Retrieve all events with metadata
    POST: Create a new event via JSON data
    
    Returns:
        JSON responses with consistent structure for easy parsing
    """
    if request.method == "GET":
        # Return all events with metadata for API consumers
        # Include total count for pagination support in future versions
        return jsonify({
            "success": True,
            "events": events,
            "total": len(events)            
        }) 
    elif request.method == "POST": 
        global event_counter
        # Extract JSON data from request body
        # This allows rich data structures beyond simple for data
        data = request.get_json()

        # Validate that JSON data was provided
        if not data:
            return jsonify({"success" : False, "error" : "No JSON data provided"}), 400
        
        # Determine the type of event to create based on JSON data
        schedule_type = data.get("schedule_type", "manual")

        if schedule_type == "auto":
            # Create auto-scheduled event using factory function
            event_data = create_auto_event()
            # Validate the generated event data
            errors = validate_event_data(event_data, is_auto=True)
        else:
            # Create manual event from provided JSON data
            event_data = create_manual_event(data)
            # Validate the provided data
            errors = validate_event_data(data, is_auto=False)

        # Return validation errors if any exist
        if errors:
            return jsonify({"success": False, "errors": errors}), 400

        # save the valid event to our storage system
        event_data["id"] = event_counter
        events.append(event_data)
        event_counter += 1

        # Return success response with the created event data
        return jsonify({
            "success": True,
            "message": "Event created successfully",
            "event": event_data
        }), 201        
    
@app.route("/api/events/<int:event_id>", methods=["GET", "PUT", "DELETE"])
def api_event_detail(event_id):
    """
    RESTful API endpoint for individual event management.
    
    This endpoint handles CRUD operations on specific events, following REST
    conventions with appropriate HTTP methods. The event_id parameter is
    extracted from the URL using Flask's route parameter syntax.
    
    GET: Retrieve a specific event by ID
    PUT: Update an existing event with new data
    DELETE: Remove an event from the system
    
    Args:
        event_id (int): The unique identifier for the event (from URL)
        
    Returns:
        JSON responses with appropriate HTTP status codes
    """    
    #find the event using our helper function
    #This demonstrates centralized event lookup logic
    event = get_event_by_id(event_id)

    #Handle case where event doesn't exist
    if not event:
        return jsonify({"success": False, "error": "Event not found"}), 404
    
    if request.method == "GET":
        #Return the event data as JSON
        return jsonify({"success": True, "event": event})
    
    elif request.method == "POST":
        #Handle event updates via JSON data
        data= request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400
        
        #Validate the update data using our validation function
        errors = validate_event_data(data, is_auto=False)
        if errors:
            return jsonify({"success": False, "errors": errors}), 400
        

        # Update event fields with new data
        # Use .get() with fallback to preserve existing values if not provided
        event.update({
            "title": data.get("title", event["title"]),
            "start": data.get("start", event["start"]),
            "end": data.get("end", event["end"]),
            "description": data.get("description", event["description"])
        })        

        #Save the updated event to storage
        save_event(event)
        return jsonify({"success": True, "event": event})
    
    elif request.method == "DELETE":
        #Remove the event from our storage system
        #This demonstrates list comprehension for filtering
        global events
        events = [e for e in events if e["id"] != event_id]
        return jsonify({"success": True, "message": "Event deleted successfully"})
    
if __name__ == "__main__":
    """
    Application entry point.
    
    This block only runs when the script is executed directly (not imported).
    The debug=True parameter enables:
    - Automatic reloading when files change
    - Detailed error pages for debugging
    - Interactive debugger in the browser
    
    In production, you would set debug=False for security and performance.
    """    
    app.run(debug=True)