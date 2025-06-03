import requests
import logging
from pprint import pformat

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('api_tests.log')
    ]
)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"

def log_request(response, *args, **kwargs):
    """Логирует детали запроса и ответа"""
    logger.info(f"Request: {response.request.method} {response.request.url}")
    logger.info(f"Headers: {pformat(dict(response.request.headers))}")
    if response.request.body:
        logger.info(f"Body: {response.request.body}")
    logger.info(f"Response: {response.status_code} - {response.text}")

def logged_request(method, url, **kwargs):
    """Обёртка для логирования запросов"""
    if "hooks" not in kwargs:
        kwargs["hooks"] = {}
    kwargs["hooks"]["response"] = [log_request]
    return requests.request(method, url, **kwargs)

# Переопределяем requests.get и requests.post для логирования
requests.get = lambda *args, **kwargs: logged_request('get', *args, **kwargs)
requests.post = lambda *args, **kwargs: logged_request('post', *args, **kwargs)

try:
    logger.info("Starting API tests...")

    # 1. Логинимся как уже зарегистрированный пользователь
    logger.info("Step 1: Logging in...")
    login = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": "librarian@example.com", "password": "securepass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login.status_code == 200, f"Login failed: {login.text}"
    token = login.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    logger.info("Login successful")

    # 2. Создаём книгу
    logger.info("Step 2: Creating book...")
    book_data = {
        "title": "Dune",
        "author": "Frank Herbert",
        "year": 1965,
        "isbn": "9780441172719",
        "copies": 2
    }
    book_response = requests.post(f"{BASE_URL}/api/books", json=book_data, headers=headers)
    assert book_response.status_code == 201, f"Book creation failed: {book_response.text}"
    book = book_response.json()
    logger.info(f"Book created: {book}")

    # 3. Создаём читателя
    logger.info("Step 3: Creating reader...")
    reader_data = {
        "name": "Paul Atreides",
        "email": "paul@arrakis.com"
    }
    reader_response = requests.post(f"{BASE_URL}/api/readers", json=reader_data, headers=headers)
    assert reader_response.status_code == 201, f"Reader creation failed: {reader_response.text}"
    reader = reader_response.json()
    logger.info(f"Reader created: {reader}")

    # 4. Выдача книги
    logger.info("Step 4: Borrowing book...")
    borrow_params = {"book_id": book["id"], "reader_id": reader["id"]}
    borrow_response = requests.post(
        f"{BASE_URL}/api/borrow/",
        params=borrow_params,
        headers=headers
    )
    assert borrow_response.status_code == 201, f"Borrow failed: {borrow_response.text}"
    borrow = borrow_response.json()
    logger.info(f"Book borrowed: {borrow}")

    # 5. Список выдач
    logger.info("Step 5: Listing borrows...")
    borrows_response = requests.get(f"{BASE_URL}/api/borrow/", headers=headers)
    assert borrows_response.status_code == 200
    logger.info(f"All borrows: {borrows_response.json()}")

    # 6. Возврат книги
    logger.info("Step 6: Returning book...")
    return_response = requests.post(f"{BASE_URL}/api/borrow/{borrow['id']}/return", headers=headers)
    assert return_response.status_code == 200
    logger.info(f"Book returned: {return_response.json()}")

    # 7. Проверка после возврата
    logger.info("Step 7: Checking borrows after return...")
    borrows_after_return = requests.get(f"{BASE_URL}/api/borrow/", headers=headers)
    assert borrows_after_return.status_code == 200
    logger.info(f"Borrows after return: {borrows_after_return.json()}")

    logger.info("All tests completed successfully!")

except Exception as e:
    logger.error(f"Test failed: {str(e)}")
    raise


