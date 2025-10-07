# 🧑‍💻 Hands-On Coding Exercise: Build Your Own Consolidated Form

## 🎯 Learning Objective
Write the consolidated form functionality yourself, step by step, to understand how each piece works.

---

## 📋 Exercise 1: Basic Flask App Setup

### Your Task
Create a new Python file called `my_calendar_app.py` and set up the basic Flask structure.

### What to Write
```python
# TODO: Add the necessary imports
# Hint: You'll need Flask, render_template, request, redirect, url_for, jsonify
# Also import datetime, timedelta, and re

# TODO: Create the Flask app instance

# TODO: Set up the basic data structures
# events = []
# event_counter = 1

# TODO: Create a basic route that returns "Hello World"
@app.route("/")
def index():
    # Your code here
    pass

# TODO: Add the if __name__ == "__main__" block to run the app
```

### Test Your Work
Run your app and make sure you see "Hello World" at `http://localhost:5000`

---

## 📋 Exercise 2: Build Validation Functions

### Your Task
Write the validation function that checks if event data is valid.

### What to Write
```python
def validate_event_data(data, is_auto=False):
    """
    Your task: Write validation logic that checks:
    
    For manual events (is_auto=False):
    1. Title exists and is at least 3 characters
    2. Start date exists and is in the future
    3. End date exists and is after start date
    4. Description exists and is at least 10 characters
    
    For auto events (is_auto=True):
    - No validation needed (they're pre-built)
    
    Return: A list of error messages (empty list if no errors)
    """
    errors = []
    
    # TODO: Write your validation logic here
    # Hint: Use data.get('field_name') to safely get form data
    # Hint: Use datetime.fromisoformat() to parse dates
    # Hint: Use datetime.now() to get current time
    
    return errors
```

### Test Cases to Handle
- Empty title: Should return error
- Title too short: Should return error  
- Past date: Should return error
- End before start: Should return error
- Valid data: Should return empty list

---

## 📋 Exercise 3: Event Creation Functions

### Your Task
Write functions that create event objects with the right structure.

### What to Write
```python
def create_auto_event():
    """
    Your task: Create an event that is automatically scheduled
    
    Requirements:
    - Schedule for 7 weeks from now
    - Set time to 9:00 AM
    - Duration of 2 hours
    - Use standard title and description
    - Add type: "auto"
    
    Return: Dictionary with event data
    """
    # TODO: Calculate the date 7 weeks from now
    # TODO: Set the time to 9:00 AM (hour=9, minute=0)
    # TODO: Create and return the event dictionary
    pass

def create_manual_event(form_data):
    """
    Your task: Create an event from form data
    
    Requirements:
    - Extract title, start, end, description from form_data
    - Strip whitespace from text fields
    - Add type: "manual"
    
    Return: Dictionary with event data
    """
    # TODO: Extract data from form_data dictionary
    # TODO: Clean up the text fields (strip whitespace)
    # TODO: Create and return the event dictionary
    pass
```

### Expected Output Format
```python
{
    "title": "Event Title",
    "start": "2025-12-01T09:00",
    "end": "2025-12-01T11:00", 
    "description": "Event description",
    "type": "auto" or "manual"
}
```

---

## 📋 Exercise 4: The Consolidated Route

### Your Task
Write the main route that handles both GET (show form) and POST (process form).

### What to Write
```python
@app.route("/schedule_event", methods=["GET", "POST"])
def schedule_event():
    """
    Your task: Handle both showing the form and processing submissions
    
    GET request: Show the empty form
    POST request: 
    1. Get the schedule_type from form
    2. Create appropriate event (auto or manual)
    3. Validate the event data
    4. If errors, show form with errors
    5. If success, save event and redirect
    """
    global event_counter
    
    if request.method == "POST":
        # TODO: Get schedule_type from request.form
        # TODO: Create event based on type (auto or manual)
        # TODO: Validate the event data
        # TODO: Handle errors by returning template with errors
        # TODO: If valid, save event and redirect to index
        pass
    
    # TODO: Handle GET request - show the form
    pass
```

### Steps to Implement
1. Check if POST or GET request
2. For POST: Get form data and determine type
3. Create event using your helper functions
4. Validate using your validation function
5. Handle errors or success appropriately

---

## 📋 Exercise 5: Basic API Endpoint

### Your Task
Create an API endpoint that can create events via JSON.

### What to Write
```python
@app.route("/api/events", methods=["GET", "POST"])
def api_events():
    """
    Your task: Create API endpoints for events
    
    GET: Return all events as JSON
    POST: Create new event from JSON data
    """
    if request.method == "GET":
        # TODO: Return all events in JSON format
        # Format: {"success": True, "events": events, "total": count}
        pass
    
    elif request.method == "POST":
        # TODO: Get JSON data from request
        # TODO: Validate it's not empty
        # TODO: Use same logic as web form but with JSON data
        # TODO: Return JSON response
        pass
```

### JSON Response Format
```python
# Success response
{
    "success": True,
    "message": "Event created successfully", 
    "event": {...}
}

# Error response  
{
    "success": False,
    "errors": ["Error message 1", "Error message 2"]
}
```

---

## 📋 Exercise 6: Create the HTML Template and Static Files

### Your Task
Create `templates/schedule_event.html` and separate CSS/JS files in the `static` directory.

### Step 1: Create the CSS File
Create `static/css/schedule_event.css`:
```css
/* TODO: Add CSS styles for:
   - body layout and typography
   - .container styling
   - .schedule-option buttons
   - .schedule-option.selected state
   - .manual-form hiding/showing
   - .error-messages styling
   - form elements (input, textarea, button)
   - responsive design considerations
*/
```

### Step 2: Create the JavaScript File
Create `static/js/schedule_event.js`:
```javascript
// TODO: Implement these functions:

function selectScheduleType(type) {
    // Update visual selection
    // Update hidden field
    // Show/hide manual form
}

function clearRequiredFields() {
    // Remove required attributes from form fields
}

function setRequiredFields() {
    // Add required attributes to form fields
}

function loadTemplate() {
    // Load predefined templates into form fields
}

function initializeDateFields() {
    // Set minimum dates and handle date changes
}

function validateForm(e) {
    // Client-side form validation
}

// Initialize when DOM loads
document.addEventListener('DOMContentLoaded', function() {
    // Set up event listeners and initialize form
});
```

### Step 3: Create the HTML Template
Create `templates/schedule_event.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Schedule DR Test</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/schedule_event.css') }}">
</head>
<body>
    <!-- TODO: Add your HTML structure here -->
    
    <script src="{{ url_for('static', filename='js/schedule_event.js') }}"></script>
</body>
</html>
```

### Benefits of This Approach
- **Separation of Concerns**: HTML structure, CSS styling, and JavaScript behavior are in separate files
- **Maintainability**: Easier to update styles or functionality without touching other code
- **Reusability**: CSS and JS can be shared across multiple templates
- **Performance**: Browsers can cache static files separately
- **Development**: Better IDE support with syntax highlighting and debugging

---

## 📋 Exercise 7: Implement JavaScript Functionality

### Your Task
Complete the JavaScript functions in `static/js/schedule_event.js`.

### Function 1: selectScheduleType()
```javascript
function selectScheduleType(type) {
    /*
    Your task: Make the schedule type toggle work
    
    Steps:
    1. Remove 'selected' class from all .schedule-option elements
    2. Add 'selected' class to the clicked option (find by data-type attribute)
    3. Update the hidden schedule_type input field value
    4. Show manual form if type is 'manual', hide if type is 'auto'
    5. Update required attributes on form fields accordingly
    */
}
```

### Function 2: Form Validation
```javascript
function validateForm(e) {
    /*
    Your task: Validate form before submission
    
    For manual events, check:
    1. Title is at least 3 characters
    2. Start and end dates are filled
    3. End is after start
    4. Description is at least 10 characters
    
    If errors found:
    - Prevent form submission (e.preventDefault())
    - Show alert with error messages
    */
}
```

### Function 3: Initialize Date Fields
```javascript
function initializeDateFields() {
    /*
    Your task: Set up date field constraints
    
    1. Set minimum date to today for start and end fields
    2. Add event listener to start field that updates end field minimum
    3. Ensure end date is always after start date
    */
}
```

### Function 4: Template Loading (Bonus)
```javascript
function loadTemplate() {
    /*
    Your task: Implement template dropdown functionality
    
    1. Get selected template value
    2. Look up template data from predefined object
    3. Fill in title and description fields with template data
    */
}
```

### Integration with HTML
Your JavaScript needs to work with these HTML elements:
- `.schedule-option` - clickable schedule type buttons
- `#schedule_type` - hidden input field
- `#manual-form` - container for manual form fields
- `#scheduleForm` - the main form element
- `#title`, `#start`, `#end`, `#description` - form input fields

---

## 📋 Exercise 8: Test Your Code

### Manual Testing Checklist
Create this testing plan and work through it:

```
□ App starts without errors
□ Form loads at /schedule_event
□ Can toggle between Auto/Manual
□ Auto schedule works (creates event 7 weeks out)
□ Manual form validates required fields
□ Manual form prevents past dates
□ Manual form prevents end before start
□ Valid manual events get created
□ Events show up when you navigate back
□ API endpoint /api/events returns JSON
□ API endpoint accepts POST with JSON data
```

### API Testing
Write these curl commands and test them:

```bash
# Test GET all events
curl -X GET http://localhost:5000/api/events

# Test create auto event  
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{"schedule_type": "auto"}'

# Test create manual event
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "schedule_type": "manual",
    "title": "My Test Event",
    "start": "2025-12-01T10:00", 
    "end": "2025-12-01T12:00",
    "description": "This is my test description that is longer than 10 characters"
  }'
```

---

## 📋 Exercise 9: Add Error Handling

### Your Task
Improve your code to handle edge cases and errors gracefully.

### What to Add
```python
# TODO: Add try/catch blocks around date parsing
# TODO: Handle missing form fields gracefully  
# TODO: Add proper HTTP status codes to API responses
# TODO: Add input sanitization to prevent XSS
# TODO: Add length limits to prevent overly long inputs
```

---

## 📋 Exercise 10: Extend the Functionality

### Your Task
Add one new feature of your choice:

#### Option A: Event Templates
Add a dropdown that pre-fills common event types:
- Basic DR Test
- Database DR Test  
- Application DR Test
- Network DR Test

#### Option B: Event Editing
Add the ability to edit existing events:
- New route: `/edit_event/<id>`
- Pre-populate form with existing data
- Update instead of create

#### Option C: Event Categories
Add categories to events:
- Add category field to form
- Color-code events by category
- Filter events by category

---

## 🎯 Learning Verification

### Code Review Checklist
After completing the exercises, review your code for:

```
□ Functions have clear, descriptive names
□ Code is properly indented and formatted
□ Comments explain the "why" not just the "what"
□ Error handling covers edge cases
□ Input validation is comprehensive
□ No duplicate code (DRY principle)
□ Variables have meaningful names
□ Functions do one thing well (Single Responsibility)
```

### Understanding Check
Can you explain to someone else:

```
□ Why we consolidated two routes into one
□ How the validation function works
□ What makes an API RESTful
□ How client-side and server-side validation differ
□ Why we separate data creation from route handling
□ How the JavaScript toggle functionality works
□ What happens when form validation fails
```

---

## 🏆 Bonus Challenges

### Challenge 1: Add Authentication
Research and implement basic user login/logout functionality.

### Challenge 2: Add Database
Replace the in-memory list with a SQLite database using SQLAlchemy.

### Challenge 3: Add Email Notifications  
Send confirmation emails when events are created.

### Challenge 4: Add Calendar View
Create a visual calendar that displays events by month.

---

## 💡 Key Learning Outcomes

By completing these exercises, you will have learned:

1. **Route Consolidation**: How to combine similar functionality into cleaner code
2. **Data Validation**: Client-side and server-side validation strategies  
3. **API Design**: RESTful endpoint creation and JSON handling
4. **Error Handling**: Graceful error management and user feedback
5. **Template Design**: Dynamic HTML with conditional content
6. **JavaScript Integration**: Making forms interactive and user-friendly
7. **Testing Strategies**: Manual and automated testing approaches
8. **Code Organization**: Separation of concerns and maintainable structure

Each exercise builds on the previous one, giving you hands-on experience with real-world web development patterns and best practices.

Remember: The goal is understanding, not just completion. Take time to experiment with the code, break things intentionally, and fix them to deepen your learning!