"""
Python script which scrapes dev.bg job board.
"""

import os
import csv
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Additional variables
JOB_FILTER = '?_job_location=sofiya%2Cremote'
CSV_FILENAME = 'job_ads.csv'


# Load existing job URLs
def load_existing_urls(filename):
    """
    Load existing job URLs to avoid duplicates
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return {row['Link'] for row in csv.DictReader(file)}
    except FileNotFoundError:
        print("File not found. Creating new CSV on write...")
        return set()


csv_job_urls = load_existing_urls(CSV_FILENAME)


# Telegram bot function
def telegram_bot_message(bot_message):
    """
    Function for creating the Telegram bot.
    """
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    message_url = ('https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id
                   + '&parse_mode=Markdown&text=' + bot_message)
    bot_response = requests.post(message_url, timeout=10)
    return bot_response.json()


# Scraping function
def scrape_jobs(url, selectors):
    """
    Main scraping logic.
    """
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    job_ads = soup.find_all(*selectors['container'])
    excluded_keywords = ['PHP', '.NET', 'JAVA', 'JavaScript', 'React',
                         'Angular', 'C++', 'C#', 'Database', 'Splunk',
                         'PowerBI', 'Golang', 'French', 'Spanish',
                         'German', 'Italian', 'Swedish', 'Risk', 'Audit']
    jobs_data = []

    if response.status_code == 200:
        for job in job_ads:
            try:
                title = job.find(*selectors['title'])
                date = job.find(*selectors['date'])
                link = job.find(*selectors['link'])
                job_url = link['href']

                if title and date and link:
                    job_title = title.text.strip().upper()
                    if not any(keyword.upper() in job_title for keyword in excluded_keywords):
                        jobs_data.append({
                            'Job title': title.text.strip(),
                            'Date posted': date.text.strip().replace('.', ''),
                            'Link': job_url})
                else:
                    print("Skipping job - missing required elements.")
            except Exception as e:
                print(f"Error processing job: {e}")
                continue
    else:
        print(f"There was an error processing the request. Status code is {response.status_code}.")
    return jobs_data


# dev.bg links
dev_bg_links = ['https://dev.bg/company/jobs/operations/',
                'https://dev.bg/company/jobs/back-end-development/',
                'https://dev.bg/company/jobs/data-science/',
                'https://dev.bg/company/jobs/junior-intern/']

# dev.bg selectors
dev_bg_selectors = {
    'container': ('div', {'class': 'inner-right listing-content-wrap'}),
    'title': ('h6', {'class': 'job-title ab-title-placeholder ab-cb-title-placeholder'}),
    'date': ('span', {'class': 'date date-with-icon'}),
    'link': ('a', {})
}


def main():
    """
    Main function
    """
    all_jobs = []

    for job_link in dev_bg_links:
        all_jobs.extend(scrape_jobs(job_link + JOB_FILTER, dev_bg_selectors))

    if not all_jobs:
        print("No jobs found.")
        return

    # Remove duplicate jobs with pandas
    df_jobs = pd.DataFrame(all_jobs)
    df_jobs.drop_duplicates(subset=['Job title', 'Date posted', 'Link'], inplace=True)

    # Filter new jobs by checking URLs against loaded CSV URLs
    new_jobs = df_jobs[~df_jobs['Link'].isin(csv_job_urls)]

    # Send Telegram notifications for new jobs only
    for _, job in new_jobs.iterrows():
        message = (f"🔍 New Job Found:\n\n{job['Job title']}"
                   f"\nPosted: {job['Date posted']}"
                   f"\nLink: {job['Link']}")
        telegram_bot_message(message)

    # Combine old URLs with new jobs
    updated_jobs = pd.concat([df_jobs, pd.DataFrame(
        {'Job title': [], 'Date posted': [], 'Link': []})], ignore_index=True)
    updated_jobs.to_csv(CSV_FILENAME, index=False)


if __name__ == "__main__":
    main()
