from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
import time

WEBSITE_URL = "https://www.stepstone.de/"
JOB_TITLE = "Frontend-Entwickler/in"
DESIRED_LOCATION = "Deutschland"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get(WEBSITE_URL)

wait = WebDriverWait(driver, 10)
input_elements = wait.until(
    ec.presence_of_all_elements_located(
        (By.CSS_SELECTOR, '#app-searchBar [data-genesis-element="FORM_INPUT"]')
    )
)

job_title_input = next(el for el in input_elements
                       if el.get_attribute("placeholder") == "(Jobtitel, Kompetenz oder Firmenname)")
location_input = next(el for el in input_elements
                      if el.get_attribute("placeholder") == "(Ort oder 5-stellige PLZ)")
job_title_input.clear()
job_title_input.send_keys(JOB_TITLE)
location_input.clear()
location_input.send_keys(DESIRED_LOCATION)

radius = wait.until(
    ec.element_to_be_clickable(
        (By.XPATH, '//*[@id="app-searchBar"]//*[contains(@id, "stepstone-menubar")]')
    )
)
radius.click()

radius_button = wait.until(
    ec.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-genesis-element="CARD"] button[value="5"]')
    )
)
radius_button.click()

part_time_checkbox = wait.until(
    ec.element_to_be_clickable(
        (By.CSS_SELECTOR, '#app-searchBar fieldset [data-at="searchbar-part-time"]')

    )
)
part_time_checkbox.click()

search_btn = wait.until(
    ec.element_to_be_clickable(
        (By.CSS_SELECTOR, '#app-searchBar [data-at="searchbar-search-button"]')
    )
)
search_btn.click()

last_24_jobs = wait.until(
    ec.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-at="desktop-filters-container"] [data-at="facet-link"]')
    )
)
last_24_jobs.click()

new_top_card = wait.until(
    ec.presence_of_element_located(
        (By.XPATH, "//*[normalize-space(text())='NEU']")
    )
)
time.sleep(6)

job_cards = wait.until(
    ec.presence_of_all_elements_located(
        (By.CSS_SELECTOR, '[data-genesis-element="CARD"][data-at="job-item"]')
    )
)

desired_time_str = {"Stunden", "Stunde", "Minuten", "Minute"}
for card in job_cards:
    time_posted = card.find_element(By.CSS_SELECTOR, '[data-at="job-item-middle"] [data-at="job-item-timeago"]').text

    if any(word in time_posted for word in desired_time_str):
        job_title = card.find_element(By.XPATH, ".//h2").text
        city = card.find_element(By.CSS_SELECTOR, '[data-at="job-item-location"]').text
        company_name = card.find_element(By.CSS_SELECTOR, '[data-at="job-item-company-name"]').text
        job_link = card.find_element(By.XPATH, ".//h2/a").get_attribute("href")

        # print(job_title)
        # print(city)
        # print(company_name)
        # print(job_link)
        # print(time_posted)

