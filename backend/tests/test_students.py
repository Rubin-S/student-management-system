# backend/tests/test_students.py
def test_create_student(test_client):
    # 1. Create a test user first to get a token
    user_data = {"email": "test@example.com", "password": "testpassword"}
    test_client.post("/users/", json=user_data)

    # 2. Log in with the test user to get an access token
    login_data = {"username": user_data["email"], "password": user_data["password"]}
    login_response = test_client.post("/token", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Use the token to create a student
    student_data = {
        "first_name": "Test",
        "last_name": "Student",
        "email": "test.student@example.com"
    }
    response = test_client.post("/students/", json=student_data, headers=headers)

    # 4. Assert that the request was successful and the data is correct
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["first_name"] == student_data["first_name"]
    assert response_data["email"] == student_data["email"]
    assert "id" in response_data