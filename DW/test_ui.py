import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from DW.settings import BASE_URL


@allure.feature('Тестирование пользовательского интерфейса на сайте "Читай-Город"')
class TestChitaiGorodUITests:

    @allure.story('Загрузка главной страницы')
    @allure.title('Главная страница отображается корректно')
    def test_homepage_load(self, browser):
        with allure.step('Открытие главной страницы'):
            browser.get("https://www.chitai-gorod.ru/")

        with allure.step('Ожидание появления элемента логотипа'):
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'header__logo-wrapper'))
            )

        with allure.step('Проверка имени вкладки'):
            title = browser.title
            assert 'Читай-город' in title, f'Название страницы неверное: {title}'

        allure.attach(browser.get_screenshot_as_png(), name='Screenshot', attachment_type=AttachmentType.PNG)

    @allure.story('Проверка работоспособности формы поиска')
    @allure.title('Форма поиска функционирует корректно')
    def test_search_field(self, browser):
        with allure.step('Открываем главную страницу'):
            browser.get(BASE_URL)

        with allure.step('Заполняем форму поиска'):
            search_field = browser.find_element(By.XPATH, "//input[@name='search' or contains(@placeholder,'Что будем искать')]")
            search_field.clear()
            search_field.send_keys('Гарри Поттер')
            search_field.submit()

        with allure.step('Отправляем запрос'):
            submit_button = browser.find_element(By.XPATH, "//input[@name='search' or contains(@placeholder,'Что будем искать')]")
            submit_button.click()

        with allure.step('Ожидаем заголовка с результатами поиска'):
            wait = WebDriverWait(browser, 10)
            result_header = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'search-title'))
            )
            print("Фактическое содержание заголовка:", result_header.text)

    @allure.story('Проверка наличия раздела "Акции"')
    @allure.title('Раздел "Акции" присутствует на главной странице')
    def test_sales_section(self, browser):
        with allure.step('Открываем главную страницу'):
            browser.get(BASE_URL)

        with allure.step('Ищем блок акций'):
            sales_block = browser.find_element(By.XPATH, '//a[@href="/promotions"]')

            assert sales_block.is_displayed(), 'Раздел "Акции" не найден.'

        allure.attach(browser.get_screenshot_as_png(), name='Sales Section Screenshot',
                      attachment_type=AttachmentType.PNG)

    @allure.story('Проверка страницы "Магазины"')
    @allure.title('Страница "Магазины" доступна и корректна')
    def test_about_us_page(self, browser):
        with allure.step('Открываем главную страницу'):
            browser.get(BASE_URL)

        with allure.step('Переходим на страницу "Магазины"'):
            about_link = browser.find_element(By.XPATH, '//a[@href="/shops"]')
            about_link.click()

        with allure.step('Проверяем название страницы'):
            page_title = browser.find_element(By.CSS_SELECTOR, '.header-top-menu__link').text
            assert 'Магазины' in page_title, f'Неправильное название страницы: {page_title}'

        allure.attach(browser.get_screenshot_as_png(), name='About Us Page Screenshot',
                      attachment_type=AttachmentType.PNG)

    @allure.story('Закрытие всплывающего окна "Ваш город..."')
    @allure.title('Окно выбора города закрывается корректно')
    def test_close_popup_window(self, browser):
        with allure.step('Открываем главную страницу'):
            browser.get(BASE_URL)

        with allure.step('Ждем появление всплывающего окна'):
            wait = WebDriverWait(browser, 10)
            popup = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//h5[contains(text(), 'Ваш город')]//ancestor::div[@class='header-location-popup']"))
            )

        with allure.step('Нажимаем кнопку подтверждения выбора города'):
            close_button = popup.find_element(By.CSS_SELECTOR,
                                              '.chg-app-button.chg-app-button--primary')
            close_button.click()

        with allure.step('Ждем исчезновение всплывающего окна'):
            wait.until(EC.invisibility_of_element_located(
                (By.XPATH, "//h5[contains(text(), 'Ваш город')]//ancestor::div[@class='header-location-popup']")))
