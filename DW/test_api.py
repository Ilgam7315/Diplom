import requests
import allure
from settings import *
from data import *
from conftest import *


@allure.feature('API Tests')
class TestAPITest:
    @pytest.mark.api
    @allure.story('Поиск по названию на кириллице')
    def test_search_book_in_catalog(self, auth):
        body = {
            "searchPhrase": SEARCH_PHRASE,
            "resultCount": RESULT_COUNT
        }
        response = requests.post(
            f'{API_BASE_URL_V2}search/results',
            json=body,
            headers=auth
        )
        print(f'Response Status Code: {response.status_code}')
        print(f'Response Body: {response.text}')
        assert response.status_code == 204

    @pytest.mark.api
    @allure.story('Добавление книги в "Корзину"')
    def test_add_available_book_to_cart(self, auth):
        body = {
            "id": BOOK_ID_AVAILABLE
        }
        response = requests.post(
            f'{API_BASE_URL_V1}cart/product',
            json=body,
            headers=auth
        )
        assert response.status_code == 200

    @pytest.mark.api
    @allure.story('Добавление книги, отсутствующей в продаже')
    def test_add_book_not_in_stock(self, auth):
        body = {
            "id": BOOK_ID_UNAVAILABLE
        }
        response = requests.post(
            f'{API_BASE_URL_V1}cart/product',
            json=body,
            headers=auth
        )
        assert response.status_code == 500
        assert 'message' in response.json()

    @pytest.mark.api
    @allure.story('Добавление книги в "Корзину" неверным HTTP-методом')
    def test_add_incorrect_method_to_cart(self, auth):
        body = {
            "id": BOOK_ID_AVAILABLE
        }
        response = requests.put(
            f'{API_BASE_URL_V1}cart/product',
            json=body,
            headers=auth
        )
        assert response.status_code == 405

    @pytest.mark.api
    @allure.story('Добавление и удаление книги из "Корзины"')
    def test_add_and_remove_book_from_cart(self, auth):
        body = {
            "id": BOOK_ID_AVAILABLE
        }
        add_response = requests.post(
            f'{API_BASE_URL_V1}cart/product',
            json=body,
            headers=auth
        )
        assert add_response.status_code == 200, "Ошибка добавления книги в корзину"
        delete_response = requests.delete(
            f'{API_BASE_URL_V1}cart/product/2142706',
            headers=auth
        )
        if delete_response.status_code == 204:
            print("Корзина очищена успешно!")
        elif delete_response.status_code == 404:
            print("Товар в корзине не найден.")
