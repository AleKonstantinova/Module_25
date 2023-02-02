import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(autouse=True)
def testing():
    s = Service(ChromeDriverManager().install())
    pytest.driver = webdriver.Chrome(service=s)
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    pytest.driver.implicitly_wait(10)

    yield

    pytest.driver.quit()


def test_show_my_pets():
    pytest.driver.find_element(By.ID, 'email').send_keys('alenka-terexina@mail.ru')

    pytest.driver.find_element(By.ID, 'pass').send_keys('copyBook')

    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')

    # left_column = pytest.driver.find_element(By.CLASS_NAME, '\\.col-sm-4.left')
    left_column = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, '\\.col-sm-4.left'))
    )

    pet_count = int(left_column.text.replace('\n', ' ').split(' ')[2])

    # table_rows = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
    table_rows = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.table.table-hover tbody tr'))
    )

    assert pet_count == len(table_rows)

    names = {}
    unique_pets = {}
    for row in table_rows:
        tds = row.find_elements(By.TAG_NAME, 'td')
        name = tds[0].text.strip()
        type = tds[1].text.strip()
        age = tds[2].text.strip()
        names[name] = True
        unique_pets[name + type + age] = True

        assert name != ''
        assert type != ''
        assert age != ''
