# from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def main():
    virtual_ucsp_login_url: str = "https://accounts.google.com/o/oauth2/v2/auth/identifier?client_id=95208330785-4d7086dmtrllm99c38m6bv0dkvjrm9ot.apps.googleusercontent.com&response_type=code&redirect_uri=https%3A%2F%2Fvirtual.ucsp.edu.pe%2Fadmin%2Foauth2callback.php&state=%2Fauth%2Foauth2%2Flogin.php%3Fwantsurl%3Dhttps%253A%252F%252Fvirtual.ucsp.edu.pe%252F%26sesskey%3DEt6pFTwPgM%26id%3D1&scope=openid%20profile%20email&flowName=GeneralOAuthFlow"
    # virtual_ucsp_login_url: str = "https://virtual.ucsp.edu.pe/login/index.php"

    user_info = {
      "id": "jose.vilca.campana@ucsp.edu.pe",
      "password": "VCJ41207"
    }

    # virtual_ucsp_home_url: str = "https://virtual.ucsp.edu.pe/"

# the anchor of each course is in div.card AND  data-type="1"

    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False, slow_mo=50)
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(virtual_ucsp_login_url)
        # page.click("a[title=Google]")
        # html = page.inner_html("#identifierId")
        html = page.inner_html("body")
        # page.fill('#identifierId', user_info["id"])
        # page.click("#identifierNext")
        # page.fill('[name=password]', user_info["password"])
        # page.click("#passwordNext")
        # html = page.inner_html("li[data-key=mycourses")
        print(html)


if __name__ == "__main__":
    main()
