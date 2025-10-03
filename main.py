import os
from selenium import webdriver
from stepstone_scraper import StepStoneScraper
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

sheet_endpoint = os.getenv("SHEET_ENDPOINT")
token = os.getenv("TOKEN")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

bot = StepStoneScraper(chrome_options)

bot.search_jobs()
bot.apply_last_24h_filter()
jobs = bot.get_recent_jobs()

x = datetime.now()

bearer_headers = {
    "Authorization": f"Bearer {token}"
}

for job in jobs:
    sheet_inputs = {
        "job": {
            "title": job["title"],
            "city": job["city"],
            "company": job["company"],
            "posted": job["time_posted"],
            "runtime": x.strftime("%I:%M"),
            "rundate": x.strftime("%d/%m/%Y"),
            "link": job["link"],
        }
    }

    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        headers=bearer_headers
    )


