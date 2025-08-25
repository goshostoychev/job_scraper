"""
Python script which scrapes dev.bg job board
"""

import os
import csv
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Additional variables
CSV_FILENAME = 'job_ads.csv'
csv_job_urls = []


# Telegram bot function
def telegram_bot_message(bot_message):
    """
    Function for creating the Telegram bot
    """
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    message_url = ('https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id
                   + '&parse_mode=Markdown&text=' + bot_message)
    bot_response = requests.post(message_url, timeout=10)
    return bot_response.json()


# Open the csv
try:
    with open(CSV_FILENAME, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_job_urls.append(row['Link'])
except FileNotFoundError:
    print("File not found")
    csv_job_urls = []


# Main scraping logic
def scrape_jobs(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    job_ads = soup.find_all('div', class_='inner-right listing-content-wrap')
    jobs_data = []
    excluded_keywords = ['PHP', '.NET', 'JAVA', 'JavaScript', 'React',
                         'Angular', 'C++', 'C#', 'Database', 'Splunk',
                         'PowerBI', 'Golang', 'French', 'Spanish', 'German']

    if response.status_code == 200:
        for job in job_ads:
            try:
                title = job.find('h6', class_='job-title ab-title-placeholder ab-cb-title-placeholder')
                date = job.find('span', class_='date date-with-icon')
                link = job.find('a')
                job_url = link['href']

                if title and date and link:
                    job_title = title.text.strip().upper()
                    if not any(keyword.upper() in job_title for keyword in excluded_keywords):
                        jobs_data.append({
                            'Job Title': title.text.strip(),
                            'Date posted': date.text.strip(),
                            'Link': job_url})
                        if job_url not in csv_job_urls:
                            telegram_bot_message(f"🔍 New Job "
                                                 f"Found:\n\n{job_url}")
                else:
                    print("Skipping job - missing required elements.")
            except Exception as e:
                print(f"Error processing job: {e}")
                continue
    else:
        print(f"There was an error processing the request. Status code is {response.status_code}.")
    return jobs_data


JOB_FILTER = '?_job_location=sofiya%2Cremote'

sites = ['https://dev.bg/company/jobs/operations/',
         'https://dev.bg/company/jobs/back-end-development/',
         'https://dev.bg/company/jobs/data-science/',
         'https://dev.bg/company/jobs/technical-support/']

all_jobs = []

for site in sites:
    jobs = scrape_jobs(site + JOB_FILTER)
    all_jobs.extend(jobs)

with open(CSV_FILENAME, 'w+', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Job Title', 'Date posted', 'Link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for final_job in all_jobs:
        writer.writerow(
            {'Job Title': final_job['Job Title'],
             'Date posted': final_job['Date posted'],
             'Link': final_job['Link']
             })
