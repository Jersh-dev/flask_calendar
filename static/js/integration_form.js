// Integration Form JavaScript

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
    const startField = document.getElementById('start');
    const endField = document.getElementById('end');
    
    if (startField) {
        startField.min = now;
    }
    if (endField) {
        endField.min = now;
    }
});