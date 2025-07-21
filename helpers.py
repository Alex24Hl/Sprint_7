import requests
import random
import string
from urls import BASE_URL


def register_new_courier_and_return_login_password():

    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{BASE_URL}/courier', data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass

def delete_courier(login, password):
    login_response = requests.post(
        f'{BASE_URL}/courier/login',
        data={"login": login, "password": password}
    )
    if login_response.status_code != 200:
        return None
    courier_id = login_response.json().get('id')
    return requests.delete(f'{BASE_URL}/courier/{courier_id}')

def create_test_order(color=None):
    payload = {
        "firstName": "Тест",
        "lastName": "Тестович",
        "address": "Москва, ул. Пресненская набережная, 10",
        "metroStation": 1,
        "phone": "+79999999999",
        "rentTime": 1,
        "deliveryDate": "2025-07-30",
        "comment": "Тестовый заказ",
        "color": color or []
    }
    return requests.post(f'{BASE_URL}/orders', json=payload)

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))