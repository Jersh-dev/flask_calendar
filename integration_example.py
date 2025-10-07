"""
Example Integration: Using Flask Calendar in Another Web Application
This demonstrates how to integrate the calendar form and API into an existing web application.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import json
from datetime import datetime, timedelta

# Example main application
app = Flask(__name__)

# Configuration for the calendar service
CALENDAR_SERVICE_URL = "http://localhost:5000"
CALENDAR_API_URL = f"{CALENDAR_SERVICE_URL}/api"

class CalendarService:
    """Service class to interact with the calendar API"""
    
    @staticmethod
    def create_event(event_data):
        """Create a new event via API"""
        try:
            response = requests.post(f"{CALENDAR_API_URL}/events", json=event_data)
            return response.json(), response.status_code
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}, 500
    
    @staticmethod
    def get_all_events():
        """Get all events via API"""
        try:
            response = requests.get(f"{CALENDAR_API_URL}/events")
            return response.json(), response.status_code
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}, 500
    
    @staticmethod
    def update_event(event_id, event_data):
        """Update an event via API"""
        try:
            response = requests.put(f"{CALENDAR_API_URL}/events/{event_id}", json=event_data)
            return response.json(), response.status_code
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}, 500
    
    @staticmethod
    def delete_event(event_id):
        """Delete an event via API"""
        try:
            response = requests.delete(f"{CALENDAR_API_URL}/events/{event_id}")
            return response.json(), response.status_code
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}, 500

@app.route("/")
def dashboard():
    """Main dashboard showing scheduled DR tests"""
    # Get events from calendar service
    events_data, status_code = CalendarService.get_all_events()
    
    if status_code == 200 and events_data["success"]:
        events = events_data["events"]
        
        # Process events for display
        upcoming_events = []
        past_events = []
        
        for event in events:
            event_date = datetime.fromisoformat(event["start"])
            if event_date > datetime.now():
                days_until = (event_date - datetime.now()).days
                event["days_until"] = days_until
                upcoming_events.append(event)
            else:
                past_events.append(event)
        
        # Sort by date
        upcoming_events.sort(key=lambda x: x["start"])
        past_events.sort(key=lambda x: x["start"], reverse=True)
        
        return render_template("dashboard.html", 
                             upcoming_events=upcoming_events,
                             past_events=past_events,
                             calendar_url=CALENDAR_SERVICE_URL)
    else:
        error_message = events_data.get("error", "Could not connect to calendar service")
        return render_template("dashboard.html", 
                             error=error_message,
                             calendar_url=CALENDAR_SERVICE_URL)

@app.route("/schedule", methods=["GET", "POST"])
def schedule_test():
    """Schedule a new DR test (embedded form or redirect)"""
    if request.method == "POST":
        # Handle form submission via API
        event_data = {
            "schedule_type": request.form.get("schedule_type", "manual"),
            "title": request.form.get("title"),
            "start": request.form.get("start"),
            "end": request.form.get("end"),
            "description": request.form.get("description")
        }
        
        result, status_code = CalendarService.create_event(event_data)
        
        if status_code == 201 and result["success"]:
            return redirect(url_for("dashboard"))
        else:
            errors = result.get("errors", [result.get("error", "Unknown error")])
            return render_template("schedule_form.html", errors=errors, form_data=request.form)
    
    # For GET requests, either show embedded form or redirect to calendar service
    embed_form = request.args.get("embed", "false").lower() == "true"
    
    if embed_form:
        return render_template("schedule_form.html")
    else:
        # Redirect to the calendar service's form
        return redirect(f"{CALENDAR_SERVICE_URL}/schedule_event")

@app.route("/api/schedule", methods=["POST"])
def api_schedule_test():
    """API endpoint for scheduling tests from other systems"""
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "error": "No JSON data provided"}), 400
    
    result, status_code = CalendarService.create_event(data)
    return jsonify(result), status_code

@app.route("/api/events")
def api_get_events():
    """API endpoint to get all events (proxy to calendar service)"""
    result, status_code = CalendarService.get_all_events()
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True, port=5001)

# Template: dashboard.html
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>DR Test Management Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .actions { text-align: center; margin: 30px 0; }
        .btn { padding: 12px 24px; margin: 0 10px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn-primary { background-color: #007bff; color: white; }
        .btn-success { background-color: #28a745; color: white; }
        .btn-secondary { background-color: #6c757d; color: white; }
        .btn:hover { opacity: 0.8; }
        .events-section { margin: 30px 0; }
        .event-card { border: 1px solid #ddd; border-radius: 5px; padding: 20px; margin: 15px 0; background: #fafafa; }
        .event-title { font-size: 18px; font-weight: bold; color: #333; margin-bottom: 10px; }
        .event-date { color: #666; margin-bottom: 10px; }
        .event-description { color: #555; }
        .days-until { background: #e7f3ff; color: #0066cc; padding: 4px 8px; border-radius: 3px; font-size: 12px; }
        .error { background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .no-events { text-align: center; color: #666; font-style: italic; margin: 40px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 Disaster Recovery Test Management</h1>
        
        {% if error %}
        <div class="error">
            <strong>Error:</strong> {{ error }}
            <br><br>
            <small>Make sure the calendar service is running at {{ calendar_url }}</small>
        </div>
        {% endif %}
        
        <div class="actions">
            <a href="{{ url_for('schedule_test') }}" class="btn btn-primary">📅 Schedule New DR Test</a>
            <a href="{{ url_for('schedule_test', embed='true') }}" class="btn btn-secondary">📝 Quick Schedule</a>
            <a href="{{ calendar_url }}" class="btn btn-success" target="_blank">🗓️ View Full Calendar</a>
        </div>
        
        {% if upcoming_events %}
        <div class="events-section">
            <h2>🔜 Upcoming DR Tests</h2>
            {% for event in upcoming_events %}
            <div class="event-card">
                <div class="event-title">{{ event.title }}</div>
                <div class="event-date">
                    📅 {{ event.start|replace('T', ' at ') }}
                    {% if event.days_until >= 0 %}
                        <span class="days-until">{{ event.days_until }} days</span>
                    {% endif %}
                </div>
                <div class="event-description">{{ event.description }}</div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if past_events %}
        <div class="events-section">
            <h2>📋 Recent DR Tests</h2>
            {% for event in past_events[:5] %}
            <div class="event-card">
                <div class="event-title">{{ event.title }}</div>
                <div class="event-date">📅 {{ event.start|replace('T', ' at ') }}</div>
                <div class="event-description">{{ event.description }}</div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if not upcoming_events and not past_events and not error %}
        <div class="no-events">
            <h3>No DR tests scheduled</h3>
            <p>Click "Schedule New DR Test" to get started!</p>
        </div>
        {% endif %}
        
        <div style="text-align: center; margin-top: 40px; color: #666; font-size: 14px;">
            <p>Integrated with Flask Calendar Service</p>
        </div>
    </div>
</body>
</html>
"""

# Save the template
with open("templates/dashboard.html", "w") as f:
    f.write(DASHBOARD_TEMPLATE)

# Template: schedule_form.html (embedded version)
SCHEDULE_FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Schedule DR Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        textarea { height: 100px; resize: vertical; }
        .btn { padding: 12px 24px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; margin: 10px 5px; }
        .btn-primary { background-color: #007bff; color: white; }
        .btn-secondary { background-color: #6c757d; color: white; }
        .btn:hover { opacity: 0.8; }
        .error { background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .schedule-type { display: flex; gap: 20px; margin-bottom: 20px; }
        .schedule-option { flex: 1; padding: 15px; border: 2px solid #ddd; border-radius: 5px; text-align: center; cursor: pointer; }
        .schedule-option.selected { border-color: #007bff; background-color: #e7f3ff; }
        .manual-form { display: none; }
        .manual-form.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Schedule DR Test</h1>
        
        {% if errors %}
        <div class="error">
            <strong>Please fix the following errors:</strong>
            <ul>
                {% for error in errors %}
                <li>{{ error }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        <form method="POST">
            <div class="schedule-type">
                <div class="schedule-option" onclick="selectType('auto')">
                    <h4>Auto Schedule</h4>
                    <p>7 weeks from today</p>
                </div>
                <div class="schedule-option selected" onclick="selectType('manual')">
                    <h4>Manual Schedule</h4>
                    <p>Custom date & time</p>
                </div>
            </div>
            
            <input type="hidden" name="schedule_type" id="schedule_type" value="manual">
            
            <div class="manual-form active" id="manual-form">
                <div class="form-group">
                    <label for="title">Test Name *</label>
                    <input type="text" name="title" id="title" required 
                           value="{{ form_data.title if form_data else '' }}"
                           placeholder="e.g., Database DR Test Q4 2025">
                </div>
                
                <div class="form-group">
                    <label for="start">Start Date & Time *</label>
                    <input type="datetime-local" name="start" id="start" required
                           value="{{ form_data.start if form_data else '' }}">
                </div>
                
                <div class="form-group">
                    <label for="end">End Date & Time *</label>
                    <input type="datetime-local" name="end" id="end" required
                           value="{{ form_data.end if form_data else '' }}">
                </div>
                
                <div class="form-group">
                    <label for="description">Description *</label>
                    <textarea name="description" id="description" required
                              placeholder="Describe the scope and objectives of this DR test...">{{ form_data.description if form_data else '' }}</textarea>
                </div>
            </div>
            
            <div style="text-align: center;">
                <button type="submit" class="btn btn-primary">Schedule Test</button>
                <a href="{{ url_for('dashboard') }}" class="btn btn-secondary">Cancel</a>
            </div>
        </form>
    </div>
    
    <script>
        function selectType(type) {
            document.querySelectorAll('.schedule-option').forEach(opt => opt.classList.remove('selected'));
            event.target.closest('.schedule-option').classList.add('selected');
            document.getElementById('schedule_type').value = type;
            
            const manualForm = document.getElementById('manual-form');
            if (type === 'auto') {
                manualForm.classList.remove('active');
                manualForm.querySelectorAll('input, textarea').forEach(field => field.removeAttribute('required'));
            } else {
                manualForm.classList.add('active');
                manualForm.querySelectorAll('input, textarea').forEach(field => field.setAttribute('required', ''));
            }
        }
        
        // Set minimum date to today
        document.addEventListener('DOMContentLoaded', function() {
            const now = new Date().toISOString().slice(0, 16);
            document.getElementById('start').min = now;
            document.getElementById('end').min = now;
        });
    </script>
</body>
</html>
"""

# Save the template  
with open("templates/schedule_form.html", "w") as f:
    f.write(SCHEDULE_FORM_TEMPLATE)

print("Integration example created successfully!")
print("Files created:")
print("- integration_example.py (main application)")
print("- templates/dashboard.html")
print("- templates/schedule_form.html")
print()
print("To run the integration example:")
print("1. Start the calendar service: python app.py")
print("2. In another terminal, start the integration app: python integration_example.py")
print("3. Visit http://localhost:5001 to see the integrated dashboard")