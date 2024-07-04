
# Job Description Scraper and Generator

## Overview

This project is designed to scrape job descriptions from the infonet.fr site, extract relevant job information, and use GPT-4 to generate comprehensive job descriptions. The resulting data is saved in a JSON file for further use by developers.

## Features

- **URL Extraction**: Extracts job URLs from the provided sitemap while filtering out non-job URLs.
- **Web Scraping**: Uses Selenium with headless Chromium to scrape job details from each URL.
- **Data Processing**: Extracts relevant job information including job title, description, required skills, education, and pros/cons.
- **Text Generation**: Utilizes GPT-4 to generate a detailed job description based on the scraped information.
- **Proxy Management**: Distributes web requests through a list of proxies to avoid IP blocking.
- **Progress Tracking**: Displays progress of the scraping and generation process using a progress bar.

## Configuration

- **API_KEY**: Your OpenAI API key.
- **PROXY_FILE**: Path to your proxy list file.
- **SITEMAP_URL**: URL of the sitemap containing job URLs.
- **TEST_MODE**: If `True`, limits the extraction to 5 URLs for testing purposes.
- **TEST_LIMIT**: Number of URLs to process in test mode.

## Installation

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up your OpenAI API key**:
    Replace `API_KEY` in the script with your actual OpenAI API key.

5. **Add your proxy list**:
    Ensure you have a proxy list file at the path specified in `PROXY_FILE`.

## Usage

Run the script using the following command:
```sh
python script.py
```

The script will extract URLs, scrape job information, and generate detailed job descriptions using GPT-4. The output will be saved in a file named `output.json`.

## Project Structure

- **script.py**: The main script that orchestrates URL extraction, web scraping, data processing, and text generation.
- **requirements.txt**: Contains the list of dependencies required to run the project.
- **README.md**: Project documentation.

## Contributing

If you wish to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

For any questions or concerns, please open an issue on the GitHub repository or contact the project maintainer.
 
