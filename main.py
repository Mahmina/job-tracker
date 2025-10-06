import os
import time
from selenium import webdriver
from stepstone_scraper import StepStoneScraper
import requests
from datetime import datetime
from dotenv import load_dotenv
import smtplib

load_dotenv()

sheet_endpoint = os.getenv("SHEET_ENDPOINT")
token = os.getenv("TOKEN")
google_sheet_result = os.getenv("GOOGLE_SHEET_RESULT")
my_email = os.getenv("MY_EMAIL")
password = os.getenv("PASSWORD")

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


time.sleep(5)

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)

    message = f"Subject:Stepstone Job Report\n\nYour Daily Job Listings Are Ready – View in Google Sheets{google_sheet_result}"

    connection.sendmail(
        from_addr=my_email,
        to_addrs=my_email,
        msg=message.encode("utf-8")
    )

