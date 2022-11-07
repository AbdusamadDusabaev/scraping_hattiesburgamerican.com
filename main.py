from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import csv


def get_and_save_data(browser, file_name):
    page = browser.page_source
    bs_object = BeautifulSoup(page, "lxml")
    more_info_block = bs_object.find(name="div", class_="MuiGrid-root MuiGrid-container MuiGrid-item MuiGrid-direction-xs-column MuiGrid-grid-xs-6 css-o0lgju")
    links = more_info_block.find_all(name="div", class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-1 css-1doag2i")
    link = links[2].div.a["href"]
    text = more_info_block.find_all(name="p", class_="MuiTypography-root MuiTypography-body1 css-r439jj")[-1]
    result = [text.text.strip(), link]
    with open(file_name, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(result)


def scraper(url, file_name):
    user_agent = UserAgent().chrome
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    browser = webdriver.Chrome(options=options)
    with open(file_name, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Data", "Url"])

    try:
        index = 0
        browser.get(url)
        while len(browser.find_elements(By.CLASS_NAME, "css-3x7hfc")) > 0:
            time.sleep(3)
            blocks = browser.find_elements(By.CLASS_NAME, "css-1iaprke")
            index += 1
            print(index)
            for block in blocks:
                block.click()
                get_and_save_data(browser, file_name)
            button_next = browser.find_elements(By.CLASS_NAME, "css-3x7hfc")[-1]
            button_next.click()
    finally:
        browser.close()
        browser.quit()


if __name__ == "__main__":
    scraper(url="https://www.hattiesburgamerican.com/public-notices", file_name="articles.csv")
