import requests

BASE_URL = "http://localhost:8000"

# 1. Регистрируем нового пользователя
register_response = requests.post(
    f"{BASE_URL}/api/auth/register",
    json={"email": "postgres@example.com", "password": "1234"}
)

print("REGISTER:", register_response.status_code, register_response.json())

# 2. Логинимся
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    data={"username": "postgres@example.com", "password": "1234"},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

print("LOGIN:", login_response.status_code, login_response.json())

token = login_response.json().get("access_token")

# 3. Доступ к защищённому эндпоинту
books_response = requests.get(
    f"{BASE_URL}/api/books",
    headers={"Authorization": f"Bearer {token}"}
)

print("BOOKS:", books_response.status_code, books_response.json())
