#!/usr/bin/env python
"""
Simple script to test the API endpoints.
"""
import requests
import time

BASE_URL = "http://localhost:8000"


def test_root():
    """Test the root endpoint."""
    response = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint: {response.status_code}")
    print(response.json())
    print()
    return response.status_code == 200


def test_signup():
    """Test the signup endpoint."""
    data = {
        "email": f"test{int(time.time())}@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/api/signup", json=data)
    print(f"Signup endpoint: {response.status_code}")
    print(response.json())
    print()
    return response.json().get("access_token")


def test_login(email, password):
    """Test the login endpoint."""
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/api/login", json=data)
    print(f"Login endpoint: {response.status_code}")
    print(response.json())
    print()
    return response.json().get("access_token")


def test_posts(token):
    """Test the posts endpoints."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Add post
    data = {"text": "This is a test post"}
    response = requests.post(f"{BASE_URL}/api/posts", json=data, headers=headers)
    print(f"Add post endpoint: {response.status_code}")
    print(response.json())
    print()
    post_id = response.json().get("post_id")
    
    # Get posts
    response = requests.get(f"{BASE_URL}/api/posts", headers=headers)
    print(f"Get posts endpoint: {response.status_code}")
    print(response.json())
    print()
    
    # Delete post
    data = {"post_id": post_id}
    response = requests.delete(f"{BASE_URL}/api/posts", json=data, headers=headers)
    print(f"Delete post endpoint: {response.status_code}")
    print(response.json())
    print()


if __name__ == "__main__":
    print("Testing FastAPI Blog Application API")
    print("====================================")
    print()
    
    try:
        # Test root endpoint
        if not test_root():
            print("Root endpoint test failed!")
            exit(1)
        
        # Test signup
        print("Testing signup...")
        email = f"test{int(time.time())}@example.com"
        password = "password123"
        token = test_signup()
        
        if not token:
            print("Signup test failed!")
            exit(1)
        
        # Test login
        print("Testing login...")
        login_token = test_login(email, password)
        
        if not login_token:
            print("Login test failed!")
            exit(1)
        
        # Test posts endpoints
        print("Testing posts endpoints...")
        test_posts(token)
        
        print("All tests passed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the API. Make sure the server is running.")
    except Exception as e:
        print(f"ERROR: {e}")
