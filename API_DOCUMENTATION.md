# Flask Calendar API Documentation

## Overview
This Flask Calendar application provides both a web interface and RESTful API endpoints for managing Disaster Recovery (DR) test events. The API is designed to be integrated into other web applications and systems.

## Base URL
```
http://localhost:5000
```

## API Endpoints

### 1. Get All Events
**Endpoint:** `GET /api/events`

**Description:** Retrieve all scheduled events.

**Response:**
```json
{
  "success": true,
  "events": [
    {
      "id": 1,
      "title": "Database DR Test",
      "start": "2025-11-21T09:00",
      "end": "2025-11-21T11:00",
      "description": "Comprehensive database failover test",
      "type": "manual"
    }
  ],
  "total": 1
}
```

### 2. Create New Event
**Endpoint:** `POST /api/events`

**Content-Type:** `application/json`

**Request Body (Manual Event):**
```json
{
  "schedule_type": "manual",
  "title": "Application DR Test",
  "start": "2025-11-21T14:00",
  "end": "2025-11-21T16:00",
  "description": "Testing application failover procedures and recovery protocols"
}
```

**Request Body (Auto Event):**
```json
{
  "schedule_type": "auto"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Event created successfully",
  "event": {
    "id": 2,
    "title": "Application DR Test",
    "start": "2025-11-21T14:00",
    "end": "2025-11-21T16:00",
    "description": "Testing application failover procedures and recovery protocols",
    "type": "manual"
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "errors": [
    "Title must be at least 3 characters long",
    "End time must be after start time"
  ]
}
```

### 3. Get Single Event
**Endpoint:** `GET /api/events/{event_id}`

**Response:**
```json
{
  "success": true,
  "event": {
    "id": 1,
    "title": "Database DR Test",
    "start": "2025-11-21T09:00",
    "end": "2025-11-21T11:00",
    "description": "Comprehensive database failover test",
    "type": "manual"
  }
}
```

### 4. Update Event
**Endpoint:** `PUT /api/events/{event_id}`

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "title": "Updated Database DR Test",
  "start": "2025-11-21T10:00",
  "end": "2025-11-21T12:00",
  "description": "Updated comprehensive database failover test with new requirements"
}
```

**Response:**
```json
{
  "success": true,
  "event": {
    "id": 1,
    "title": "Updated Database DR Test",
    "start": "2025-11-21T10:00",
    "end": "2025-11-21T12:00",
    "description": "Updated comprehensive database failover test with new requirements",
    "type": "manual"
  }
}
```

### 5. Delete Event
**Endpoint:** `DELETE /api/events/{event_id}`

**Response:**
```json
{
  "success": true,
  "message": "Event deleted successfully"
}
```

## Validation Rules

### Manual Events
- **Title:** 3-200 characters, required
- **Description:** 10-1000 characters, required
- **Start:** Valid datetime, cannot be in the past, required
- **End:** Valid datetime, must be after start time, required

### Auto Events
- Automatically scheduled 7 weeks from creation date
- Set to 9:00 AM - 11:00 AM
- Predefined title and description
- No validation required from user

## Error Handling

All API endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error message"
}
```

or for validation errors:

```json
{
  "success": false,
  "errors": [
    "Error message 1",
    "Error message 2"
  ]
}
```

## HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `500` - Internal Server Error

## Integration Examples

### JavaScript/Ajax Example
```javascript
// Create a new manual event
async function createEvent(eventData) {
  try {
    const response = await fetch('/api/events', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(eventData)
    });
    
    const result = await response.json();
    
    if (result.success) {
      console.log('Event created:', result.event);
    } else {
      console.error('Errors:', result.errors);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}

// Usage
createEvent({
  schedule_type: "manual",
  title: "Network DR Test",
  start: "2025-12-01T13:00",
  end: "2025-12-01T15:00",
  description: "Testing network failover and recovery procedures"
});
```

### Python Requests Example
```python
import requests
import json

# Create auto-scheduled event
def create_auto_event():
    url = "http://localhost:5000/api/events"
    data = {"schedule_type": "auto"}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 201:
        result = response.json()
        print(f"Event created: {result['event']['title']}")
    else:
        print(f"Error: {response.json()}")

# Get all events
def get_all_events():
    url = "http://localhost:5000/api/events"
    response = requests.get(url)
    
    if response.status_code == 200:
        result = response.json()
        for event in result['events']:
            print(f"{event['title']} - {event['start']}")
```

### cURL Examples
```bash
# Get all events
curl -X GET http://localhost:5000/api/events

# Create manual event
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "schedule_type": "manual",
    "title": "Security DR Test",
    "start": "2025-12-15T10:00",
    "end": "2025-12-15T12:00",
    "description": "Testing security systems failover and incident response procedures"
  }'

# Create auto event
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{"schedule_type": "auto"}'

# Update event
curl -X PUT http://localhost:5000/api/events/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Security DR Test",
    "description": "Updated security systems test with enhanced procedures"
  }'

# Delete event
curl -X DELETE http://localhost:5000/api/events/1
```

## Web Interface Integration

### Form Submission with API Response
You can also use the web form with API-style responses by adding `?api=true` to the URL:

```html
<form action="/schedule_event?api=true" method="POST">
  <!-- form fields -->
</form>
```

This will return JSON responses instead of redirecting.

## Event Templates

The web interface includes predefined templates for common DR test scenarios:

1. **Basic DR Test** - Standard failover procedures
2. **Database DR Test** - Database-specific testing
3. **Application DR Test** - Application stack testing
4. **Network DR Test** - Network infrastructure testing

These templates can be used as starting points for manual event creation.

## Security Considerations

- Input validation is performed on all user inputs
- XSS protection through proper escaping
- No authentication implemented (add as needed for production)
- CORS headers not configured (add as needed for cross-origin requests)

## Future Enhancements

- User authentication and authorization
- Event categories and tags
- Recurring events
- Email notifications
- Event templates via API
- Bulk operations
- Advanced filtering and search
- Calendar view API endpoints