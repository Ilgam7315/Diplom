import pytest
from selenium import webdriver
from settings import AUTHORIZATION


@pytest.fixture(scope="session")
def browser():
    """Инициализирует браузер."""
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope='session', autouse=True)
def auth():
    """Возвращает заголовки с Bearer-токеном."""
    return AUTHORIZATION
