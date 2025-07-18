# sabellas_project3
# sabellas_project
🔍 Automated Web Profile Scraper
Tools: Python · Selenium · BeautifulSoup · Requests · Pandas
Status: Private Deployment

📌 Project Overview
This private automation tool was designed to extract and parse structured profile data from a secure web portal using session-based authentication and dynamic element interaction.

Key capabilities include:

Automated login flow using stored credentials (from login_info.py)

Dynamic page navigation and scraping using Selenium WebDriver

HTML parsing and data normalization via BeautifulSoup

Structured output of profile data for downstream analytics or storage

Session reuse and modular scraping architecture (splitting scraping, parsing, and exporting into independent files)

.
├── login_info.py         # Stores login credentials securely
├── profile_scraper.py    # Main orchestrator script
├── selenium_scraped.py   # Browser-controlled scraping logic
├── scraped.py            # HTML response logic
├── parsed_data.py        # Profile parser and formatter

🛡️ Licensing Note
This repository contains augmented reference code.
All subsequent versions and deployments are the sole property of the client.

