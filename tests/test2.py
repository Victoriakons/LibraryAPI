import requests

BASE_URL = "http://localhost:8000"

# 1. Регистрируем нового пользователя
register_response = requests.post(
    f"{BASE_URL}/api/auth/register",
    json={"email": "librarian@example.com", "password": "securepass"}
)
print("REGISTER:", register_response.status_code, register_response.json())

# 2. Логинимся
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    data={"username": "librarian@example.com", "password": "securepass"},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)
print("LOGIN:", login_response.status_code, login_response.json())

token = login_response.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

# 3. Создаём книги
book_payloads = [
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "year": 1937,
        "isbn": "9780261103344",
        "copies": 3
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "isbn": "9780451524935",
        "copies": 2
    }
]

created_books = []
for payload in book_payloads:
    response = requests.post(f"{BASE_URL}/api/books", json=payload, headers=headers)
    print("CREATE BOOK:", response.status_code, response.json())
    created_books.append(response.json())

# 4. Получаем список книг
books_response = requests.get(f"{BASE_URL}/api/books", headers=headers)
print("GET BOOKS:", books_response.status_code, books_response.json())

# 5. Обновляем первую книгу
book_id = created_books[0]["id"]
update_payload = {"copies": 10}
update_response = requests.put(f"{BASE_URL}/api/books/{book_id}", json=update_payload, headers=headers)
print("UPDATE BOOK:", update_response.status_code, update_response.json())

# 6. Удаляем вторую книгу
book_id_to_delete = created_books[1]["id"]
delete_response = requests.delete(f"{BASE_URL}/api/books/{book_id_to_delete}", headers=headers)
print("DELETE BOOK:", delete_response.status_code)

# 7. Проверяем, что книга удалена
check_response = requests.get(f"{BASE_URL}/api/books/{book_id_to_delete}", headers=headers)
print("GET DELETED BOOK:", check_response.status_code, check_response.text)
