import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_test():
    # 1. Login
    print("Logging in...")
    try:
        resp = requests.post(f"{BASE_URL}/auth/token", data={
            "username": "test@example.com",
            "password": "password"
        })
        if resp.status_code != 200:
            print(f"Login failed: {resp.status_code} {resp.text}")
            # Try signup if login fails
            print("Attempting signup...")
            signup_resp = requests.post(f"{BASE_URL}/auth/signup", json={
                "full_name": "Test User",
                "phone_number": "1234567890",
                "email": "test@example.com",
                "password": "password",
                "role": "tenant"
            })
            if signup_resp.status_code == 200:
                 resp = requests.post(f"{BASE_URL}/auth/token", data={
                    "username": "test@example.com",
                    "password": "password"
                })
            else:
                 print(f"Signup failed: {signup_resp.status_code} {signup_resp.text}")
                 return

        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login success.")

        # 2. Trigger AI Generation (via Issue Creation or Direct Analysis)
        # Testing direct analysis since that's what failed with 500 in browser manual trigger
        print("Triggering Analysis...")
        analyze_resp = requests.post(f"{BASE_URL}/analyze/tenant", json={
            "location": "Bangalore",
            "issue_type": "Maintenance",
            "description": "Mold on ceiling",
            "tone": "Firm",
            "date": "2024-01-01"
        }, headers=headers)

        print(f"Analysis Status: {analyze_resp.status_code}")
        print(f"Analysis Response: {analyze_resp.text}")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    run_test()
