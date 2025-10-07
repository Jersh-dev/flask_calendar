# Flask Calendar Project - Consolidated DR Test Scheduler

## 🎯 Project Overview

This Flask Calendar application provides a **consolidated, robust form** for scheduling Disaster Recovery (DR) tests with both **web interface** and **RESTful API** capabilities. The main deliverable is a form that can be easily integrated into other web applications through APIs.

## ✨ Key Features

### 🔄 Consolidated Functionality
- **Single Form Interface**: Combined manual and auto-scheduling in one robust form
- **Smart Validation**: Comprehensive client-side and server-side validation
- **Template System**: Pre-built templates for common DR test scenarios
- **Responsive Design**: Professional, mobile-friendly interface

### 🚀 API-Ready Design
- **RESTful API Endpoints**: Full CRUD operations for events
- **JSON Responses**: Structured responses for easy integration
- **Error Handling**: Comprehensive validation and error reporting
- **External Integration**: Ready to be consumed by other applications

### 🛡️ Robust Validation
- **Input Validation**: Prevents invalid data entry
- **Business Rules**: Enforces logical constraints (end after start, future dates, etc.)
- **Error Messages**: Clear, actionable feedback to users
- **XSS Protection**: Secure handling of user inputs

## 📁 Project Structure

```
flask_calendar/
├── app.py                      # Main Flask application with consolidated routes
├── requirements.txt            # Python dependencies
├── API_DOCUMENTATION.md        # Comprehensive API documentation
├── test_api.py                # API testing and demonstration script
├── integration_example.py      # Example of integrating into another app
├── templates/
│   ├── index.html             # Calendar dashboard
│   ├── schedule_event.html    # Consolidated scheduling form
│   └── edit_event.html        # Event editing form
├── integration_templates/
│   ├── dashboard.html         # Example integration dashboard
│   └── schedule_form.html     # Example embedded form
└── static/
    ├── css/
    │   └── calendar.css       # Calendar styles
    └── js/
        └── calendar.js        # Calendar functionality
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application
```bash
# Start the Flask application
python app.py
```

Visit `http://localhost:5000` to access the web interface.

### 3. Test the API
```bash
# Run the comprehensive API test suite
python test_api.py
```

## 🎨 Using the Consolidated Form

### Web Interface
1. Visit `http://localhost:5000`
2. Click **"Schedule DR Test"**
3. Choose between:
   - **Auto Schedule**: Automatically schedules 7 weeks from today
   - **Manual Schedule**: Custom date, time, and details
4. Fill in the form (with built-in validation)
5. Submit to schedule the event

### Form Features
- **Schedule Type Toggle**: Switch between auto and manual scheduling
- **Real-time Validation**: Immediate feedback on form inputs
- **Template Loading**: Quick-fill templates for common scenarios
- **Smart Defaults**: Business hours, reasonable durations
- **Error Prevention**: Date/time constraints, required fields

## 🔌 API Integration

### Basic API Usage

```python
import requests

# Create a manual event
event_data = {
    "schedule_type": "manual",
    "title": "Database DR Test Q4 2025",
    "start": "2025-12-15T09:00",
    "end": "2025-12-15T11:00",
    "description": "Quarterly database disaster recovery test"
}

response = requests.post("http://localhost:5000/api/events", json=event_data)
result = response.json()

if result["success"]:
    print(f"Event created: {result['event']['title']}")
else:
    print(f"Errors: {result['errors']}")
```

### Auto-schedule Event
```python
# Create auto-scheduled event (7 weeks from today)
auto_data = {"schedule_type": "auto"}
response = requests.post("http://localhost:5000/api/events", json=auto_data)
```

### Get All Events
```python
response = requests.get("http://localhost:5000/api/events")
events = response.json()["events"]
```

## 🔧 Integration Example

See `integration_example.py` for a complete example of how to integrate this calendar form into another web application.

### Run Integration Example
```bash
# Terminal 1: Start calendar service
python app.py

# Terminal 2: Start integration example
python integration_example.py

# Visit http://localhost:5001 to see the integrated dashboard
```

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/events` | Get all events |
| `POST` | `/api/events` | Create new event |
| `GET` | `/api/events/{id}` | Get specific event |
| `PUT` | `/api/events/{id}` | Update event |
| `DELETE` | `/api/events/{id}` | Delete event |

Full API documentation available in `API_DOCUMENTATION.md`.

## ✅ Validation Rules

### Manual Events
- **Title**: 3-200 characters, required
- **Description**: 10-1000 characters, required
- **Start Date**: Must be in the future, required
- **End Date**: Must be after start date, required

### Auto Events
- **Schedule**: Automatically set to 7 weeks from creation
- **Time**: 9:00 AM - 11:00 AM business hours
- **Title/Description**: Predefined professional content

## 🧪 Testing

### Run API Tests
```bash
python test_api.py
```

This comprehensive test suite validates:
- ✅ Event creation (manual and auto)
- ✅ Event retrieval and updates
- ✅ Validation error handling
- ✅ API response formats
- ✅ Integration patterns

### Manual Testing
1. **Form Validation**: Try submitting invalid data
2. **Auto Scheduling**: Test the auto-schedule feature
3. **Template Loading**: Test the quick-fill templates
4. **API Calls**: Use the test script or cURL commands

## 🔄 Migration from Old System

The new consolidated system maintains backward compatibility:

- **Legacy Routes**: `/add_event` redirects to `/schedule_event`
- **Same Data Model**: Existing events continue to work
- **Enhanced Features**: Additional validation and API capabilities

## 🌟 Benefits for External Integration

### For Web Applications
- **Easy Embedding**: Use the form in iframes or embed directly
- **API Integration**: Full programmatic control
- **Consistent Styling**: Professional, customizable design
- **Error Handling**: Robust validation and user feedback

### For System Integration
- **RESTful API**: Standard HTTP methods and JSON responses
- **Comprehensive Documentation**: Clear integration examples
- **Error Reporting**: Detailed validation messages
- **Flexible Scheduling**: Both manual and automatic options

## 🛠️ Customization

### Styling
- Modify `templates/schedule_event.html` for custom styling
- Update CSS variables for brand colors
- Add custom JavaScript for enhanced interactions

### Business Logic
- Modify validation rules in `app.py`
- Add custom templates in the form
- Extend API endpoints for additional features

### Integration
- Use the `CalendarService` class pattern from the integration example
- Implement authentication/authorization as needed
- Add custom fields or event types

## 🚀 Production Deployment

### Security Considerations
- Add authentication/authorization
- Configure CORS for cross-origin requests
- Implement rate limiting
- Add HTTPS/SSL certificates

### Performance Optimization
- Use a proper database (PostgreSQL, MySQL)
- Add caching for frequent queries
- Implement connection pooling
- Add monitoring and logging

### Scalability
- Deploy with WSGI server (Gunicorn, uWSGI)
- Use load balancer for multiple instances
- Add database replication
- Implement background job processing

## 📞 Support

This form is designed to be **production-ready** and **integration-friendly**. The API endpoints provide everything needed to incorporate DR test scheduling into existing applications.

**Key Integration Points:**
- Form can be embedded in any web application
- API provides full programmatic access
- Validation ensures data quality
- Error handling provides clear feedback
- Templates speed up common use cases

For additional customization or integration support, refer to the comprehensive examples in `integration_example.py` and `test_api.py`.