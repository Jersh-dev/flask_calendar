/*
 * Schedule Event Form JavaScript
 * 
 * This file provides interactive functionality for the consolidated event
 * scheduling form. It demonstrates several important JavaScript concepts:
 * 
 * - DOM manipulation and event handling
 * - Progressive enhancement (form works without JavaScript)
 * - Form validation and user feedback
 * - Dynamic interface updates
 * - Template-based form generation
 * - Browser API usage (localStorage, etc.)
 */

/**
 * Handle schedule type selection (Manual vs Auto)
 * 
 * This function demonstrates dynamic interface updates based on user choice.
 * It manages the visual state, form fields, and validation requirements
 * dynamically to provide a smooth user experience.
 * 
 * @param {string} type - Either 'manual' or 'auto'
 */
function selectScheduleType(type) {
    // Update visual state of schedule type buttons
    // Remove 'selected' class from all options first
    document.querySelectorAll('.schedule-option').forEach(option => {
        option.classList.remove('selected');
    });
    // Add 'selected' class to the chosen option
    document.querySelector(`[data-type="${type}"]`).classList.add('selected');
    
    // Update the hidden form field that tracks the selected type
    // This ensures the server receives the correct schedule type
    document.getElementById('schedule_type').value = type;
    
    // Show/hide appropriate form sections based on selection
    const manualForm = document.getElementById('manual-form');
    const autoInfo = document.getElementById('auto-info');
    
    if (type === 'auto') {
        // Auto scheduling: hide manual form, show auto info
        manualForm.classList.remove('active');
        autoInfo.style.display = 'block';
        // Remove required attributes since auto doesn't need manual input
        clearRequiredFields();
    } else {
        // Manual scheduling: show manual form, hide auto info
        manualForm.classList.add('active');
        autoInfo.style.display = 'none';
        // Add required attributes for manual fields
        setRequiredFields();
    }
}

/**
 * Remove required attributes from manual form fields
 * 
 * This function is called when switching to auto scheduling mode.
 * It prevents form validation errors for fields that aren't needed
 * in auto mode.
 */
function clearRequiredFields() {
    document.querySelectorAll('#manual-form input, #manual-form textarea').forEach(field => {
        field.removeAttribute('required');
    });
}

/**
 * Add required attributes to essential manual form fields
 * 
 * This function is called when switching to manual scheduling mode.
 * It ensures proper validation for user-entered data.
 */
function setRequiredFields() {
    document.getElementById('title').setAttribute('required', '');
    document.getElementById('description').setAttribute('required', '');
    document.getElementById('start').setAttribute('required', '');
    document.getElementById('end').setAttribute('required', '');
}

/**
 * Load predefined event templates
 * 
 * This function demonstrates template-based form filling, which improves
 * user experience by providing common event configurations. It shows how
 * to manipulate form values programmatically and could be extended to
 * load templates from a server or localStorage.
 */
function loadTemplate() {
    // Get the selected template from the dropdown
    const template = document.getElementById('template').value;
    const titleField = document.getElementById('title');
    const descField = document.getElementById('description');
    
    // Template definitions - in a real app, these might come from an API
    const templates = {
        'basic': {
            title: 'Basic Disaster Recovery Test',
            description: 'Standard DR test covering basic system failover procedures, data backup verification, and recovery time validation. Includes testing of critical business functions and communication protocols.'
        },
        'database': {
            title: 'Database Disaster Recovery Test',
            description: 'Comprehensive database DR test including database failover, backup restoration, data integrity verification, replication testing, and performance validation. Covers both primary and secondary database systems.'
        },
        'application': {
            title: 'Application Disaster Recovery Test',
            description: 'Full application stack DR test covering application server failover, load balancer configuration, session management, API endpoint testing, and user interface functionality validation.'
        },
        'network': {
            title: 'Network Disaster Recovery Test',
            description: 'Network infrastructure DR test including network failover procedures, routing table updates, firewall configuration, VPN connectivity, and network performance monitoring.'
        }
    };
    
    // Apply the selected template to form fields
    if (template && templates[template]) {
        titleField.value = templates[template].title;
        descField.value = templates[template].description;
        
        // Optional: Could trigger validation or other form updates here
        // validateForm(); // Example of chaining functionality
    }
}

/**
 * Initialize date/time field constraints and behavior
 * 
 * This function demonstrates working with HTML5 date/time inputs and
 * implementing logical constraints (end time must be after start time).
 * It also shows event listener management for dynamic form behavior.
 */
function initializeDateFields() {
    // Get current date/time for minimum value constraints
    const now = new Date();
    // Convert to the format required by datetime-local inputs (YYYY-MM-DDTHH:MM)
    const minDateTime = now.toISOString().slice(0, 16);
    
    const startField = document.getElementById('start');
    const endField = document.getElementById('end');
    
    // Set minimum date to today for start field
    if (startField) {
        startField.min = minDateTime;
        
        // Add event listener to update end field minimum when start changes
        // This ensures end time is always after start time
        startField.addEventListener('change', function() {
            if (endField) {
                endField.min = this.value;
                // If end time is now before start time, clear it
                if (endField.value && endField.value < this.value) {
                    endField.value = '';
                }
            }
        });
    }
    
    // Set minimum date to today for end field
    if (endField) {
        endField.min = minDateTime;
    }
}

/**
 * Client-side form validation
 * 
 * This function provides immediate feedback to users before form submission.
 * It demonstrates validation patterns, error collection, and preventing
 * form submission for invalid data. This improves user experience by
 * catching errors before server round-trip.
 * 
 * @param {Event} e - The form submit event
 */
function validateForm(e) {
    // Get the current schedule type to determine what to validate
    const scheduleType = document.getElementById('schedule_type').value;
    
    // Only validate manual scheduling fields (auto has no user input)
    if (scheduleType === 'manual') {
        // Get form field values and trim whitespace
        const title = document.getElementById('title').value.trim();
        const description = document.getElementById('description').value.trim();
        const start = document.getElementById('start').value;
        const end = document.getElementById('end').value;
        
        // Collect validation errors in an array
        let errors = [];
        
        // Validate title length
        if (title.length < 3) {
            errors.push('Title must be at least 3 characters long');
        }
        
        // Validate description length
        if (description.length < 10) {
            errors.push('Description must be at least 10 characters long');
        }
        
        // Validate required datetime fields
        if (!start) {
            errors.push('Start date and time are required');
        }
        
        if (!end) {
            errors.push('End date and time are required');
        }
        
        // Validate that end time is after start time
        if (start && end && new Date(end) <= new Date(start)) {
            errors.push('End time must be after start time');
        }
        
        // If there are validation errors, prevent form submission
        if (errors.length > 0) {
            e.preventDefault(); // Stop the form from submitting
            // Display errors to user (in a real app, you might use better UI)
            alert('Please fix the following errors:\n' + errors.join('\n'));
            return false;
        }
    }
    
    // Form is valid, allow submission
    return true;
}

/**
 * Initialize the form when the DOM is fully loaded
 * 
 * This demonstrates the DOMContentLoaded event pattern for safe DOM
 * manipulation. It ensures all HTML elements exist before JavaScript
 * tries to interact with them.
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize datetime field constraints and behavior
    initializeDateFields();
    
    // Add form validation to prevent invalid submissions
    const form = document.getElementById('scheduleForm');
    if (form) {
        // Attach validation to form submit event
        form.addEventListener('submit', validateForm);
    }
    
    // Set default schedule type to manual when page loads
    // This ensures the form has a consistent initial state
    selectScheduleType('manual');
    
    // Optional: Add keyboard shortcuts for power users
    // Example: Ctrl+Enter to submit form
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            if (form && validateForm({ preventDefault: () => {} })) {
                form.submit();
            }
        }
    });
});