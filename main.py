# from bs4 import BeautifulSoup

import time

from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# from http.server import executable
# from turtle import ht



def get_academico_course_weights():
    user_info = {
      "id": "201-10-48429",
      "password": "VCJ41207"
    }

    academico_login_url: str = "https://academico.ucsp.edu.pe/"
    academico_principal_url: str = "https://academico.ucsp.edu.pe/principal.html"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    driver.get(academico_login_url)
    driver.find_element(By.XPATH, '//input[@id="txt_usr"]').send_keys(user_info["id"])
    password_field = driver.find_element(By.XPATH, '//input[@id="txt_pwd"]')
    password_field.send_keys(user_info["password"])
    password_field.send_keys(Keys.RETURN)

    driver.switch_to.frame(driver.find_element(By.NAME,"cabecera"))
    student_button_table = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_element_located((By.ID, 'mnu_principaln1'))
    )
    student_button = student_button_table.find_element(By.TAG_NAME, 'a')
    student_button.click()

    print("successful LOG IN")
    html = driver.page_source
    print(html)
    driver.close()



def main():
    virtual_ucsp_login_url: str = "https://virtual.ucsp.edu.pe/login/index.php"

    user_info = {
      "id": "jose.vilca.campana@ucsp.edu.pe",
      "password": "VCJ41207"
    }

    # virtual_ucsp_home_url: str = "https://virtual.ucsp.edu.pe/"

# the anchor of each course is in div.card AND  data-type="1"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        # browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(virtual_ucsp_login_url)
        page.click("a[title=Google]")

        page.fill('input#identifierId', user_info["id"])
        page.locator('text=Siguiente').click()
        page.fill('input[type=password]', user_info["password"])
        page.locator('text=Siguiente').click()
        html = page.inner_html("li[data-key=mycourses]")
        print(html)
        time.sleep(1000)


if __name__ == "__main__":
    get_academico_course_weights()
    # main()
