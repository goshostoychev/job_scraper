# Job Scraper

An automated job monitoring system that scrapes dev.bg for new job postings and sends real-time notifications via Telegram. Built to streamline the job search process by eliminating manual browsing and ensuring you never miss new opportunities.

## Features

- **Multi-category scraping**: Monitors multiple job categories simultaneously (Operations, Backend Development, Data Science, Junior/Intern positions)
- **Smart filtering**: Excludes jobs with unwanted technologies/languages using keyword filtering
- **Duplicate detection**: Prevents duplicate notifications from jobs posted in multiple categories
- **Real-time notifications**: Sends Telegram messages only for genuinely new job postings
- **Location filtering**: Supports remote and Sofia-based job filtering
- **Data persistence**: Saves job data to CSV for tracking and analysis
- **Error handling**: Robust error handling for network issues and parsing problems
- **Automation ready**: Designed for scheduled execution via cron jobs

## Technologies Used

- **Python 3.x**
- **BeautifulSoup4** - HTML parsing and web scraping
- **Requests** - HTTP requests handling
- **CSV** - Data storage and processing
- **Telegram Bot API** - Push notifications
- **python-dotenv** - Environment variable management
- **Pandas** - for removing duplicate results

## Prerequisites

- Python 3.x installed
- Telegram Bot Token (obtain from @BotFather)
- Telegram Chat ID

## Installation

1. Clone the repository:

```bash
git clone https://github.com/goshostoychev/job-scraper.git
cd job-scraper
```

1. Install required packages:

```bash
pip install -r requirements
```

1. Create a `.env` file in the project root:

```
TELEGRAM_TOKEN=your_bot_token_here
CHAT_ID=your_chat_id_here
```

## Configuration

### Monitored Job Categories

The script currently monitors these dev.bg categories:

- Operations/DevOps roles
- Backend Development
- Data Science
- Junior/Intern positions

### Keyword Filtering

Jobs containing these keywords are automatically excluded:

- Programming languages: PHP, .NET, Java, JavaScript, React, Angular, C++, C#, Golang
- Tools: Database, Splunk, PowerBI
- Languages: French, Spanish, German, Italian, Swedish

### Location Filtering

Currently set to monitor:

- Sofia-based positions
- Remote positions

## Usage

### Manual Execution

```bash
python job_scraper.py
```

### Automated Execution (Recommended)

Set up a cron job to run hourly:

```bash
crontab -e
```

Add this line:

```
0 * * * * /usr/bin/python3 /path/to/your/job_scraper.py
```

## How It Works

1. **Data Loading**: Reads existing job URLs from CSV file to track previously seen postings.
2. **Web Scraping**: Scrapes configured dev.bg job categories using requests and BeautifulSoup.
3. **Filtering**: Applies keyword and location filters to exclude unwanted positions.
4. **Duplicate Detection**: Compares new jobs against existing database to identify genuinely new postings.
5. **Notifications**: Sends Telegram messages only for new job postings.
6. **Data Storage**: Updates CSV file with all current job postings for future comparisons.

## Output

- **CSV File**: `job_ads.csv` containing job title, posting date, and URL
- **Telegram Notifications**: Real-time messages for new job postings
- **Console Output**: Status messages and error reporting

## Project Structure

```
job-scraper-bot/
├── job_scraper.py        # Main scraping script
├── job_ads.csv           # Job data storage (generated)
├── .env                  # Environment variables (create this)
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## Error Handling

The script includes comprehensive error handling for:

- Network connectivity issues
- Missing HTML elements
- File I/O operations
- API rate limiting
- Malformed job postings

## Customization

### Adding New Job Categories

Add URLs to the `dev_bg_urls` list:

```python
dev_bg_urls = [
    'https://dev.bg/company/jobs/operations/',
    'https://dev.bg/company/jobs/your-new-category/',
    # Add more URLs here
]
```

### Modifying Filters

Update the `excluded_keywords` list or `JOB_FILTER` parameter to match your preferences.

### Changing Notification Format

Modify the `telegram_bot_message()` calls to customize message content.



## License

This project is licensed under the MIT License.



## Disclaimer

This tool is for personal use only. Please respect the terms of service of the websites being scraped and implement appropriate rate limiting to avoid overloading servers.
