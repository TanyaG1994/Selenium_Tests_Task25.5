import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('D:/chromedriver//chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   # Вводим данные для авторизации и нажимаем кнопку Войти.
   pytest.driver.find_element("id", 'email').send_keys('vasya@mail.com')
   pytest.driver.find_element("id", 'pass').send_keys('12345')
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
   # Переходим на страницу, содержащую карточки питомцев пользователя.
   nav_link = pytest.driver.find_element("link text", u"Мои питомцы")
   nav_link.click()

   yield

   pytest.driver.quit()



# test 1
# Проверяем, что на странице присутствуют карточки всех питомцев.
def test_chislo_pets():
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.text-center th[scope="row"]'))
   )
   cards = pytest.driver.find_elements(By.CSS_SELECTOR, '.text-center th[scope="row"]')
   col_pet = pytest.driver.find_element(By.XPATH, '//div[contains(@class, ".col-sm-4 left")]')
   assert '\n' in col_pet.text
   parts = col_pet.text.split('\n')
   part = parts[1].split(' ')
   chislo = int(part[1])
   assert len(cards) == chislo


# test 2
# Проверяем, что хотя бы у половины питомцев есть фото.
def test_foto_pets():
   pytest.driver.implicitly_wait(10)
   images = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
   col_foto = 0
   for i in range(len(images)):
      if images[i].get_attribute('src') != '':
         col_foto = col_foto + 1

   # Обращаемся к элементу страницы, содержащему число карточек питомцев. И разделяем полученный текст по строкам и по пробелам,
   # чтобы обратиться к конкретному числу.
   col_pet = pytest.driver.find_element(By.XPATH, '//div[contains(@class, ".col-sm-4 left")]')
   assert '\n' in col_pet.text
   parts = col_pet.text.split('\n')
   part = parts[1].split(' ')
   chislo = int(part[1])

   assert col_foto >= chislo//2



# test 3
# У всех питомцев есть имя, возраст и порода.
def test_name_and_kind():
   pytest.driver.implicitly_wait(10)
   names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
   pytest.driver.implicitly_wait(10)
   kinds = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
   pytest.driver.implicitly_wait(10)
   ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
   # Перебираем данные карточек питомцев - имена, возраст и породы и проверяем, что ни один элемент не пуст.
   for i in range(len(names)):
      assert (names[i].text != '') and (kinds[i].text != '') and (ages[i].text != '')



# test 4
# У всех питомцев разные имена.
def test_different_name():
   pytest.driver.implicitly_wait(10)
   names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
   for i in range(len(names)):
      for j in range(len(names)):
         if i != j:
            assert names[i].text != names[j].text



# test 5
# В списке нет повторяющихся питомцев.
def test_different_pets():
   pytest.driver.implicitly_wait(10)
   names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
   pytest.driver.implicitly_wait(10)
   kinds = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
   pytest.driver.implicitly_wait(10)
   ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
   # Перебираем карточки питомцев и сравниваем их друг с другом. Чтобы хотя бы одини из элементов - имена, возраст, породы
   #  не были равны.
   for i in range(len(names)):
      for j in range(len(names)):
         if i != j:
           assert (names[i].text != names[j].text) or (kinds[i].text != kinds[j].text) or (ages[i].text != ages[j].text)