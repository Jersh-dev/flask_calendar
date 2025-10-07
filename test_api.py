#!/usr/bin/env python3
"""
API Test Script for Flask Calendar Application
Demonstrates how to interact with the calendar API programmatically
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

def test_api():
    """Test all API endpoints"""
    print("🧪 Testing Flask Calendar API")
    print("=" * 50)
    
    # Test 1: Get all events (should be empty initially)
    print("\n1. Getting all events...")
    response = requests.get(f"{API_BASE}/events")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success: Found {data['total']} events")
        for event in data['events']:
            print(f"   - {event['title']} ({event['start']})")
    else:
        print(f"❌ Failed to get events: {response.status_code}")
        return False
    
    # Test 2: Create an auto-scheduled event
    print("\n2. Creating auto-scheduled event...")
    auto_event_data = {
        "schedule_type": "auto"
    }
    
    response = requests.post(f"{API_BASE}/events", json=auto_event_data)
    if response.status_code == 201:
        data = response.json()
        auto_event_id = data['event']['id']
        print(f"✅ Success: Created auto event (ID: {auto_event_id})")
        print(f"   Title: {data['event']['title']}")
        print(f"   Start: {data['event']['start']}")
    else:
        print(f"❌ Failed to create auto event: {response.status_code}")
        print(f"   Error: {response.json()}")
        return False
    
    # Test 3: Create a manual event
    print("\n3. Creating manual event...")
    start_time = datetime.now() + timedelta(days=30)
    end_time = start_time + timedelta(hours=3)
    
    manual_event_data = {
        "schedule_type": "manual",
        "title": "API Test DR Exercise",
        "start": start_time.strftime("%Y-%m-%dT%H:%M"),
        "end": end_time.strftime("%Y-%m-%dT%H:%M"),
        "description": "This is a test event created via the API to demonstrate functionality and validate the integration capabilities of the calendar system."
    }
    
    response = requests.post(f"{API_BASE}/events", json=manual_event_data)
    if response.status_code == 201:
        data = response.json()
        manual_event_id = data['event']['id']
        print(f"✅ Success: Created manual event (ID: {manual_event_id})")
        print(f"   Title: {data['event']['title']}")
        print(f"   Start: {data['event']['start']}")
    else:
        print(f"❌ Failed to create manual event: {response.status_code}")
        print(f"   Error: {response.json()}")
        return False
    
    # Test 4: Get specific event
    print(f"\n4. Getting event details (ID: {manual_event_id})...")
    response = requests.get(f"{API_BASE}/events/{manual_event_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success: Retrieved event details")
        print(f"   Title: {data['event']['title']}")
        print(f"   Description: {data['event']['description'][:50]}...")
    else:
        print(f"❌ Failed to get event: {response.status_code}")
        return False
    
    # Test 5: Update event
    print(f"\n5. Updating event (ID: {manual_event_id})...")
    update_data = {
        "title": "Updated API Test DR Exercise",
        "description": "This event has been updated via the API to demonstrate the update functionality. The new description includes additional details about the enhanced testing procedures."
    }
    
    response = requests.put(f"{API_BASE}/events/{manual_event_id}", json=update_data)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success: Updated event")
        print(f"   New Title: {data['event']['title']}")
    else:
        print(f"❌ Failed to update event: {response.status_code}")
        print(f"   Error: {response.json()}")
        return False
    
    # Test 6: Test validation errors
    print("\n6. Testing validation (should fail)...")
    invalid_event_data = {
        "schedule_type": "manual",
        "title": "AB",  # Too short
        "start": "2024-01-01T10:00",  # In the past
        "end": "2024-01-01T09:00",  # Before start
        "description": "Too short"  # Too short
    }
    
    response = requests.post(f"{API_BASE}/events", json=invalid_event_data)
    if response.status_code == 400:
        data = response.json()
        print(f"✅ Success: Validation working correctly")
        print(f"   Errors found: {len(data['errors'])}")
        for error in data['errors']:
            print(f"   - {error}")
    else:
        print(f"❌ Validation test failed: Expected 400, got {response.status_code}")
        return False
    
    # Test 7: Get all events again (should show created events)
    print("\n7. Getting all events again...")
    response = requests.get(f"{API_BASE}/events")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success: Found {data['total']} events")
        for event in data['events']:
            print(f"   - {event['title']} ({event['start']}) [Type: {event['type']}]")
    else:
        print(f"❌ Failed to get events: {response.status_code}")
        return False
    
    # Test 8: Delete event
    print(f"\n8. Deleting event (ID: {manual_event_id})...")
    response = requests.delete(f"{API_BASE}/events/{manual_event_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success: {data['message']}")
    else:
        print(f"❌ Failed to delete event: {response.status_code}")
        return False
    
    # Test 9: Verify deletion
    print(f"\n9. Verifying deletion (should get 404)...")
    response = requests.get(f"{API_BASE}/events/{manual_event_id}")
    if response.status_code == 404:
        print(f"✅ Success: Event properly deleted")
    else:
        print(f"❌ Event still exists: {response.status_code}")
        return False
    
    print("\n🎉 All API tests passed!")
    print("=" * 50)
    return True

def demonstrate_integration():
    """Demonstrate how to integrate the API into another application"""
    print("\n🔧 Integration Example")
    print("=" * 30)
    
    class CalendarClient:
        """Simple client class for calendar integration"""
        
        def __init__(self, base_url="http://localhost:5000"):
            self.base_url = base_url
            self.api_url = f"{base_url}/api"
        
        def schedule_dr_test(self, title, start_date, duration_hours=2, description=""):
            """Schedule a DR test with simplified parameters"""
            start_dt = datetime.fromisoformat(start_date)
            end_dt = start_dt + timedelta(hours=duration_hours)
            
            event_data = {
                "schedule_type": "manual",
                "title": title,
                "start": start_dt.strftime("%Y-%m-%dT%H:%M"),
                "end": end_dt.strftime("%Y-%m-%dT%H:%M"),
                "description": description or f"Disaster Recovery Test: {title}"
            }
            
            response = requests.post(f"{self.api_url}/events", json=event_data)
            return response.json() if response.status_code == 201 else None
        
        def auto_schedule_dr_test(self):
            """Auto-schedule a DR test 7 weeks out"""
            event_data = {"schedule_type": "auto"}
            response = requests.post(f"{self.api_url}/events", json=event_data)
            return response.json() if response.status_code == 201 else None
        
        def get_upcoming_tests(self):
            """Get all upcoming DR tests"""
            response = requests.get(f"{self.api_url}/events")
            if response.status_code == 200:
                data = response.json()
                return data['events']
            return []
    
    # Demonstrate usage
    print("Creating calendar client...")
    calendar = CalendarClient()
    
    print("\nScheduling a DR test...")
    future_date = (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%dT14:00")
    result = calendar.schedule_dr_test(
        title="Quarterly Database DR Test",
        start_date=future_date,
        duration_hours=4,
        description="Comprehensive quarterly database disaster recovery test including failover procedures, backup restoration, and performance validation."
    )
    
    if result and result['success']:
        print(f"✅ Scheduled: {result['event']['title']}")
        print(f"   Date: {result['event']['start']}")
    else:
        print("❌ Failed to schedule test")
        return False
    
    print("\nAuto-scheduling a DR test...")
    auto_result = calendar.auto_schedule_dr_test()
    if auto_result and auto_result['success']:
        print(f"✅ Auto-scheduled: {auto_result['event']['title']}")
        print(f"   Date: {auto_result['event']['start']}")
    else:
        print("❌ Failed to auto-schedule test")
        return False
    
    print("\nGetting all upcoming tests...")
    tests = calendar.get_upcoming_tests()
    print(f"Found {len(tests)} scheduled tests:")
    for test in tests:
        test_date = datetime.fromisoformat(test['start'])
        days_until = (test_date - datetime.now()).days
        print(f"   - {test['title']} (in {days_until} days)")
    
    print("\n✅ Integration example completed successfully!")
    return True

if __name__ == "__main__":
    print("Flask Calendar API Test Suite")
    print("Make sure the Flask app is running on http://localhost:5000")
    print()
    
    try:
        # Test basic connectivity
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print("❌ Flask app is not running or not accessible")
            print("Please start the app with: python app.py")
            exit(1)
        
        # Run tests
        if test_api():
            demonstrate_integration()
        else:
            print("❌ API tests failed")
            exit(1)
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask app")
        print("Please make sure the app is running on http://localhost:5000")
        print("Start it with: python app.py")
        exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        exit(1)