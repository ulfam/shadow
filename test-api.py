#!/usr/bin/env python3
"""
Test script for Shadowing UK API endpoints
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Is it running?")
        return False


def test_process_endpoint():
    """Test process endpoint with a sample YouTube URL"""
    print("\n🎬 Testing process endpoint...")

    # Test data
    test_data = {
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll for testing
        "repeats": 2,
    }

    try:
        response = requests.post(f"{BASE_URL}/api/process", data=test_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Process endpoint working: {data}")
            return data.get("job_id")
        else:
            print(f"❌ Process endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        return None


def test_status_endpoint(job_id):
    """Test status endpoint"""
    if not job_id:
        print("❌ No job ID to test status")
        return False

    print(f"\n📊 Testing status endpoint for job {job_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/status/{job_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status endpoint working: {data}")
            return True
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        return False


def main():
    """Run API tests"""
    print("🧪 Shadowing UK API Tests")
    print("=" * 40)

    # Test health endpoint
    if not test_health():
        print("\n❌ API server is not running or not accessible")
        print("Start the backend with: cd backend && python main.py")
        return

    # Test process endpoint
    job_id = test_process_endpoint()

    # Test status endpoint if we got a job ID
    if job_id:
        test_status_endpoint(job_id)

    print("\n" + "=" * 40)
    print("✅ API tests completed!")
    print("\nTo test with a real video:")
    print("1. Start the backend: cd backend && python main.py")
    print("2. Start the frontend: npm run dev")
    print("3. Open http://localhost:3000 in your browser")


if __name__ == "__main__":
    main()
