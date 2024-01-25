# Indeed Job Scraper

This GitHub repository contains a basic web scraping tool designed for extracting job-related information from Indeed. The code is structured as a Scrapy spider, aimed at collecting detailed job listings efficiently and systematically. The tool is fundamental, allowing for further modifications and enhancements to meet specific data collection requirements.

## Overview

The `IndeedJobSpider` is a Python class inheriting from `scrapy.Spider`, tasked with navigating through Indeed's job listings, extracting valuable information, and organizing the data into a structured format. The primary focus is on part-time job listings in specific locations, with the default set to 'Alberta'.

## Features

- **Flexible Query Parameters**: Users can specify the job type, location, and other search criteria. The spider constructs the search URL dynamically based on these parameters.
- **Pagination Handling**: The spider automatically navigates through search result pages, ensuring comprehensive data collection up to a predefined number of pages.
- **Data Extraction**: Information such as job title, company name, location, posted time, job key, and a brief job description is meticulously extracted from each job listing.
- **Structured Output**: Extracted data is neatly organized and saved in a CSV format, facilitating easy analysis and storage.

## Data Fields

The following data fields are extracted for each job listing:

- `location`: The geographical location of the job listing.
- `page`: The page number from the search results where the job listing was found.
- `company`: The name of the company offering the job.
- `jobName`: The title of the job.
- `salary`: The salary information provided for the job (if available).
- `position`: The position of the job listing on the search results page.
- `job location`: The specific location of the job within the broader search location.
- `relativeTime`: The time since the job was posted.
- `jobkey`: A unique identifier for the job listing.
- `jobDescription`: A brief description or snippet from the job listing.

## Usage

1. **Installation**: Ensure you have `scrapy` installed in your Python environment.
2. **Settings**: Modify the search parameters in the `start_requests` method if needed.
3. **Run Spider**: Navigate to the spider's directory and run the spider using the `scrapy crawl indeed_jobs` command.
4. **Data Retrieval**: Collected data will be saved in the `data` directory as a CSV file, named with the spider's name and the timestamp of when the crawl was executed.

## Customization and Further Development

While the current version of the spider serves as a robust foundation for basic job data collection, users are encouraged to tailor the code to their specific needs. Potential areas for further development include:

- **Keyword Filtering**: Implementing functionality for filtering job listings based on specific keywords or phrases.
- **Advanced Data Fields**: Extracting additional data fields such as job requirements, qualifications, and full job descriptions.
- **Error Handling**: Enhancing the spider's robustness by implementing comprehensive error handling and data validation mechanisms.

## Contribution

Contributions to enhance the functionality or performance of this spider are welcome. Please feel free to fork the repository, make your improvements, and submit a pull request.

---

Please note that web scraping should be conducted responsibly and in compliance with Indeed's terms of service or any applicable legal guidelines. The user of this tool is responsible for any data collected or actions taken using this script.
