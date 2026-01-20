import requests
import json
import random
import string

BASE_URL = "http://127.0.0.1:8000"

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

email = f"{generate_random_string()}@example.com"
password = "TestPassword123!"
name = f"Test User {generate_random_string()}"

print(f"--- Attempting Signup with {email} ---")
signup_url = f"{BASE_URL}/auth/signup"
signup_data = {
    "email": email,
    "password": password,
    "full_name": name,
    "role": "tenant"
}
try:
    resp = requests.post(signup_url, json=signup_data)
    print(f"Signup Status: {resp.status_code}")
    print(f"Signup Response: {resp.text}")
except Exception as e:
    print(f"Signup Error: {e}")

print("\n--- Attempting Login ---")
login_url = f"{BASE_URL}/auth/token"
login_data = {
    "username": email, # OAuth2PasswordRequestForm uses username
    "password": password
}
# Note: FastAPI OAuth2PasswordRequestForm accepts form data, not JSON
try:
    resp = requests.post(login_url, data=login_data)
    print(f"Login Status: {resp.status_code}")
    if resp.status_code == 200:
        token = resp.json()["access_token"]
        print("Login Success (Token received)")
        
        # Now try AI
        print("\n--- Attempting AI Analysis ---")
        analyze_url = f"{BASE_URL}/issues/analyze" # Wait, analyze endpoint might be different. 
        # Check routes/analyze.py? No, it's usually mounted.
        # Let's try to create an issue which triggers AI.
        
        create_issue_url = f"{BASE_URL}/issues/"
        issue_data = {
            "title": "Test Issue",
            "description": "Test Description",
            "location": "Test Location",
            "issue_type": "Test Type",
            "tone": "Professional",
            "landlord_email": "landlord@example.com"
        }
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.post(create_issue_url, json=issue_data, headers=headers)
        print(f"Create Issue Status: {resp.status_code}")
        print(f"Create Issue Response: {resp.text}")

    else:
        print(f"Login Failed: {resp.text}")

except Exception as e:
    print(f"Login Error: {e}")

