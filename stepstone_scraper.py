from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

WEBSITE_URL = "https://www.stepstone.de/"
JOB_TITLE = "Frontend-Entwickler/in"
DESIRED_LOCATION = "Deutschland"


class StepStoneScraper:
    def __init__(self, chrome_options):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.driver.get(WEBSITE_URL)
        self.wait = WebDriverWait(self.driver, 10)

    def search_jobs(self):
        """Fill in job title and location,
        apply 5km radius and part_time filter,
        then submit search"""
        input_elements = self.wait.until(
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

        radius = self.wait.until(
            ec.element_to_be_clickable(
                (By.XPATH, '//*[@id="app-searchBar"]//*[contains(@id, "stepstone-menubar")]')
            )
        )
        radius.click()

        radius_button = self.wait.until(
            ec.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-genesis-element="CARD"] button[value="5"]')
            )
        )
        radius_button.click()

        part_time_checkbox = self.wait.until(
            ec.element_to_be_clickable(
                (By.CSS_SELECTOR, '#app-searchBar fieldset [data-at="searchbar-part-time"]')

            )
        )
        part_time_checkbox.click()

        search_btn = self.wait.until(
            ec.element_to_be_clickable(
                (By.CSS_SELECTOR, '#app-searchBar [data-at="searchbar-search-button"]')
            )
        )
        search_btn.click()

    def apply_last_24h_filter(self):
        """Click the 'Neuer als 24h' filter and wait for the page to load new data."""
        last_24_jobs = self.wait.until(
            ec.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-at="desktop-filters-container"] [data-at="facet-link"]')
            )
        )
        last_24_jobs.click()

        new_top_card = self.wait.until(
            ec.presence_of_element_located(
                (By.XPATH, "//*[normalize-space(text())='NEU']")
            )
        )
        # Add 6 seconds sleep just to be sure the page is fully loaded.
        time.sleep(6)

    def get_recent_jobs(self):
        """Extract job cards posted recently (minutes/hours only)."""
        job_cards = self.wait.until(
            ec.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '[data-genesis-element="CARD"][data-at="job-item"]')
            )
        )

        desired_time_str = {"Stunden", "Stunde", "Minuten", "Minute"}
        jobs = []

        for card in job_cards:
            time_posted = card.find_element(By.CSS_SELECTOR,
                                            '[data-at="job-item-middle"] [data-at="job-item-timeago"]').text

            if any(word in time_posted for word in desired_time_str):
                job_title = card.find_element(By.XPATH, ".//h2").text
                city = card.find_element(By.CSS_SELECTOR, '[data-at="job-item-location"]').text
                company_name = card.find_element(By.CSS_SELECTOR, '[data-at="job-item-company-name"]').text
                job_link = card.find_element(By.XPATH, ".//h2/a").get_attribute("href")

                jobs.append({
                    "title": job_title,
                    "city": city,
                    "company": company_name,
                    "link": job_link,
                    "time_posted": time_posted
                })

        return jobs
