# from bs4 import BeautifulSoup

import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from playwright.sync_api import sync_playwright
from webdriver_manager.chrome import ChromeDriverManager

# from http.server import executable
# from turtle import ht



def get_academico_course_weights():
    ***REMOVED***
    ***REMOVED***
    ***REMOVED***
    }

    academico_login_url: str = "https://academico.ucsp.edu.pe/"
    # academico_principal_url: str = "https://academico.ucsp.edu.pe/principal.html"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    driver.get(academico_login_url)
    driver.find_element(By.XPATH, '//input[@id="txt_usr"]').send_keys(user_info["id"])
    password_field = driver.find_element(By.XPATH, '//input[@id="txt_pwd"]')
    password_field.send_keys(user_info["password"])
    password_field.send_keys(Keys.RETURN)

    driver.switch_to.frame(driver.find_element(By.NAME,"cabecera"))
    student_button_table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'mnu_principaln1'))
    )
    student_button = student_button_table.find_element(By.TAG_NAME, 'a')
    student_button.click()

    print("successful LOG IN")
    html = driver.page_source
    print(html)
    driver.close()

def pass_google_auth(driver):
    ***REMOVED***
      "id": "jose.vilca.campana@ucsp.edu.pe",
    ***REMOVED***
    }
    email_field = driver.find_element(By.ID, 'identifierId')
    email_field.send_keys(user_info["id"])
    email_field.send_keys(Keys.RETURN)

    WebDriverWait(driver, 20).until(
      EC.element_to_be_clickable((By.XPATH, '//input[@type="password"]'))
    )
    password_field = driver.find_element(By.XPATH, '//input[@type="password"]')
    password_field.send_keys(user_info["password"])
    password_field.send_keys(Keys.RETURN)

def pass_virtual_ucsp_login(driver):
    url: str = "https://virtual.ucsp.edu.pe/login/index.php"
    driver.get(url)
    WebDriverWait(driver, 20).until(
      EC.element_to_be_clickable((By.XPATH, '//a[@title="Google"]'))
    )

    driver.find_element(By.XPATH, '//a[@title="Google"]').click()
    pass_google_auth(driver)

def goto_grade_report(driver):
    WebDriverWait(driver, 20).until(
      EC.element_to_be_clickable((By.XPATH, '//img[@class="userpicture"]'))
    )
    profile_picture = driver.find_element(By.XPATH, '//img[@class="userpicture"]')
    profile_picture.click()

    dropdown_buttons = driver.find_elements(By.XPATH, '//a[@class="dropdown-item menu-action"]')
    for button in dropdown_buttons:
        html = button.get_attribute("innerHTML")
        print(html)

    dropdown_buttons[2].click()

def get_course_grades_links(driver):
    tbody = driver.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.XPATH, ".//tr")

    course_links: list = []
    for row in rows:
      if(row.get_attribute("class") != "emptyrow"):
        anchor = row.find_element(By.TAG_NAME, "a")
        course_links.append(anchor.get_attribute("href"))
    return course_links


def main():

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    pass_virtual_ucsp_login(driver)
    goto_grade_report(driver)
    course_links: list = get_course_grades_links(driver)

    print(">>>>>>>>", len(course_links))
    for link in course_links:
        print("link:", link)

    time.sleep(100)
    driver.close()
    # time.sleep(1000)


if __name__ == "__main__":
    # get_academico_course_weights()
    main()
