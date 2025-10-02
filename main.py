import os
from selenium import webdriver
from stepstone_scraper import StepStoneScraper

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

bot = StepStoneScraper(chrome_options)

bot.search_jobs()
bot.apply_last_24h_filter()
jobs = bot.get_recent_jobs()



