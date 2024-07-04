import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from tqdm import tqdm
import json
import openai
import random

# Configuration
API_KEY = 'sk-proj-RZ0LiDtZsP3yuMOk9mSHT3BlbkFJ85KBlBotL0iox0wDxGGv'
PROXY_FILE = '/Users/simonazoulay/Presentation_Text/Texts_add_bloc_for_jobs/proxyscrape_premium_http_proxies.txt'
SITEMAP_URL = 'https://sitemaps.infonet.fr/codeRomeJobs/sitemap_code_rome.xml.gz'
TEST_MODE = True
TEST_LIMIT = 5

# Regex pattern to filter URLs
URL_PATTERN = re.compile(r'^https://infonet.fr/metiers/[A-Z]\d{4}/\d{5}-[a-z\-]+$')

# Function to extract URLs from the sitemap
def extract_urls(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, 'xml')
    urls = [loc.text for loc in soup.find_all('loc') if URL_PATTERN.match(loc.text)]
    return urls[:TEST_LIMIT] if TEST_MODE else urls

# Function to get a random user agent
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# Function to initialize Selenium WebDriver with a random proxy and user agent
def get_driver(proxies):
    proxy = random.choice(proxies)
    user_agent = get_random_user_agent()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server=http://{proxy}')
    chrome_options.add_argument(f'user-agent={user_agent}')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(90)  # Augmenter le délai d'attente pour le chargement des pages
    return driver

# Function to scrape data from a single URL using Selenium
def scrape_page(driver, url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data = {
        'url': url,
        'metier': soup.select_one('body > main > div.bg-primary > div > div.mt-n2 > div > h1').text if soup.select_one('body > main > div.bg-primary > div > div.mt-n2 > div > h1') else '',
        'presentation_metier': soup.select_one('body > main > div.bg-primary > div > div.mt-n2 > div > p').text if soup.select_one('body > main > div.bg-primary > div > div.mt-n2 > div > p') else '',
        'competences': soup.select_one('body > main > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(3)').text if soup.select_one('body > main > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(3)') else '',
        'etudes': soup.select_one('body > main > div:nth-of-type(2) > div:nth-of-type(4) > div > div:nth-of-type(3) > ul').text if soup.select_one('body > main > div:nth-of-type(2) > div:nth-of-type(4) > div > div:nth-of-type(3) > ul') else '',
        'avantages_inconveniant': soup.select_one('body > main > div:nth-of-type(2) > div:nth-of-type(5) > div > div > div:nth-of-type(3)').text if soup.select_one('body > main > div:nth-of-type(2) > div:nth-of-type(5) > div > div > div:nth-of-type(3)') else ''
    }
    return data

# Function to generate text using GPT-4
def generate_text(prompt):
    client = openai.OpenAI(api_key=API_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un expert du monde de l’emploi. Utilise les informations fournies pour rédiger une fiche métier claire et informative. Intègre ces informations harmonieusement dans un texte fluide et bien structuré, sans les répéter mot pour mot."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.2
    )
    return completion.choices[0].message.content

# Main function to orchestrate scraping and text generation
def main():
    urls = extract_urls(SITEMAP_URL)
    with open(PROXY_FILE) as f:
        proxies = f.read().splitlines()

    driver = get_driver(proxies)
    results = []
    for url in tqdm(urls):
        result = scrape_page(driver, url)
        prompt = (
            f"Rédige une fiche métier pour le poste de {result['metier']}.\n\n"
            f"Voici quelques informations pour t'aider :\n"
            f"- Présentation du métier : {result['presentation_metier']}\n"
            f"- Compétences requises : {result['competences']}\n"
            f"- Études et formation : {result['etudes']}\n"
            f"- Avantages et inconvénients : {result['avantages_inconveniant']}\n\n"
            "Utilise ces informations pour rédiger une fiche métier fluide et claire, en intégrant harmonieusement ces éléments sans les répéter mot pour mot par ailleurs tu ne construira le plan et paragraphes sur ces bases, informations fournie.Pour chaque fiche à générer tu décideras de l'approche la plus utile pour nos lecteurs."
        )
        result['text_bloc_complementary'] = generate_text(prompt)
        results.append(result)

    driver.quit()

    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

# Run the script
if __name__ == "__main__":
    main()
