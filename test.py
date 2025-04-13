import requests

BASE_URL = "http://0.0.0.0:5001"  


test_user = {
    "Curtin_ID": "6666",
    "Password": "TestPassword",
    "Student_name": "Test User",
    "Student_email": "testser@example.com"
}

def test_register():
    print("\n[TEST] Registering User...")
    response = requests.post(f"{BASE_URL}/register", json=test_user)
    print(response.json())

def test_login():
    print("\n[TEST] Logging in User...")
    response = requests.post(f"{BASE_URL}/login", json={
        "Curtin_ID": test_user["Curtin_ID"],
        "Password": test_user["Password"]
    })
    result = response.json()
    print(result)

    if "token" in result:
        return result["token"] 
    else:
        return None

def test_chat(token):
    print("\n[TEST] Sending Chat Message...")
    headers = {"Authorization": f"Bearer {token}"}  
    response = requests.post(f"{BASE_URL}/chat", json={"message": "Hello, AI!"}, headers=headers)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)


if __name__ == "__main__":
    test_register()
    jwt_token = test_login()
    if jwt_token:
        test_chat(jwt_token)
    else:
        print("\n eerror！")
