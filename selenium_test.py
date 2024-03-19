import time
from typing import Dict, List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from playwright.sync_api import sync_playwright
from webdriver_manager.chrome import ChromeDriverManagerpp

from clases.Course import Course, Evaluation

# from http.server import executable
# from turtle import ht


def pass_academico_auth(driver) -> None:
    login_url: str = "https://academico.ucsp.edu.pe/"
    ***REMOVED***
      ***REMOVED***
      ***REMOVED***
    }
    driver.get(login_url)
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
    # html = driver.page_source
    # print(html)


def filter_empty_anchors(tag):
    return tag.name == "a" and tag.get_text() != ""


def get_course_names(driver) -> List[str]:
    raw_html_of_courses_table = driver.find_element(By.ID, "dtg_notas").get_attribute("innerHTML")
    soup = BeautifulSoup(raw_html_of_courses_table, "html.parser")
    course_names_elements = soup.find_all("td", attrs={"align": "left"})
    course_names: List[str] = [course_name.get_text() for course_name in course_names_elements]

    print(">>> course names:")
    print(course_names)
    return course_names


def get_course_name_credit_relation(driver: webdriver) -> Dict[str, int]:
    credits_url: str = "https://academico.ucsp.edu.pe/mat_constancia.aspx"
    driver.get(credits_url)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn_grilla"))
    )
    driver.find_element(By.CLASS_NAME, "btn_grilla").click()
    courses_table = driver.find_element(By.ID, "dtg_cursos")

    raw_html_of_courses_table = courses_table.get_attribute("innerHTML")
    soup = BeautifulSoup(raw_html_of_courses_table, "html.parser")
    rows = soup.find_all("tr", attrs={"style": "font-family:Arial;font-size:8pt;"})
    name_credits_relation: Dict[str, int] = {}

    for row in rows:
        course_name: str = row.find("td", attrs={"style": "width:210px;white-space:nowrap;"}).get_text()
        parentesis_index: int = course_name.find("(")
        if parentesis_index != -1:
            course_name = course_name[:parentesis_index -1]
        course_credits: int = row.find("td", attrs={"style": "width:25px;white-space:nowrap;"}).get_text()
        name_credits_relation[course_name] = course_credits

    print(name_credits_relation)
    return name_credits_relation


def get_courses() -> None:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    pass_academico_auth(driver)

    name_credits_relation = get_course_name_credit_relation(driver)

    evaluaciones_url: str = "https://academico.ucsp.edu.pe/evaluaciones_alumno.aspx"
    driver.get(evaluaciones_url)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn_grilla"))
    )
    driver.find_element(By.CLASS_NAME, "btn_grilla").click()

    course_names = get_course_names(driver)
    courses: List[Course] = []

    XPATH_to_weights_button: str = '//input[@type="image"]'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, XPATH_to_weights_button))
    )
    init_weights_links = driver.find_elements(By.XPATH, XPATH_to_weights_button)
    n_of_weights_links = len(init_weights_links)
    count = 0

    while(count < n_of_weights_links):
        weights_links = driver.find_elements(By.XPATH, XPATH_to_weights_button)
        weights_links[count].click()

        evaluations_div = driver.find_element(By.ID, "trv_evaln0Nodes")
        raw_html_of_evaluations = evaluations_div.get_attribute("innerHTML")

        soup = BeautifulSoup(raw_html_of_evaluations, "html.parser")
        anchors = soup.find_all(filter_empty_anchors)

        evaluations: List[Evaluation] = []

        different_type: bool = True
        for i in range(len(anchors)-1):
            anchor_text: str = anchors[i].get_text()
            new_type: str = Evaluation.get_type_of_string(anchor_text)
            # new_name: str = Evaluation.get_name_of_string(anchor_text)
            # update
            if new_type != Evaluation.last_type:
                Evaluation.last_type = new_type
                Evaluation.last_total_percentage = float(Evaluation.get_percentage_of_string(anchor_text))
                different_type = True

            next_anchor_text = anchors[i+1].get_text()
            next_type: str = Evaluation.get_type_of_string(next_anchor_text)
            if different_type:
                if new_type == next_type:
                    different_type = False
                else:  # when this anchor is the only one and have no sub_evaluations
                    # The problem is we have changed the last_type so it goes for
                    # self.type == self.last_type instead of else
                    evaluations.append(Evaluation(anchor_text))
                    evaluations[-1].percentage = Evaluation.last_total_percentage
                continue
            evaluations.append(Evaluation(anchor_text))

        evaluations.append(Evaluation(anchors[-1].get_text()))
        courses.append(Course(course_names[count], evaluations, name_credits_relation[course_names[count]] ))
        count += 1

    for course in courses:
        print(f"course.name, credits : {course.name}, {course.credits}")
        for evaluation in course.evaluations:
            print(f"\t name, percentage, credits : {evaluation.name}, {evaluation.percentage} %")

    time.sleep(100)
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

    course_links: List = []
    for row in rows:
        if(row.get_attribute("class") != "emptyrow"):
            anchor = row.find_element(By.TAG_NAME, "a")
            course_links.append(anchor.get_attribute("href"))

    return course_links


def update_course_grades():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    pass_virtual_ucsp_login(driver)
    goto_grade_report(driver)
    course_links: List = get_course_grades_links(driver)

    print(">>>>>>>>", len(course_links))
    for link in course_links:
        print("link:", link)

    # not sure how to retrieve the data
    # it's a bunch of shit, with no hierachy
    # Course_name
    # evaluation 1
    # HW
    # evaluation 2
    # HW
    # HW
    # evaluation 3
    # HW
    # evaluation 4
    # HW
    # --- after this, is this unlabeled HW?
    # HW
    # HW
    # HW
    # --- end
    # cat_89848_36036 row_272622_36036 grade
    # cat_89847_36036 row_272621_36036 weight

    time.sleep(100)
    driver.close()


def main():
    update_course_grades()
    get_courses()



if __name__ == "__main__":
    main()
