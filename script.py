import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from datetime import datetime  # Import datetime module
import time

data = []  # Hold our scraped data
s = requests.Session()  # Use a single session for all requests

def scrape_rnz():
    global data
    url = 'https://rnz.co.nz'
    response = s.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Clear old data
    data = []

    # Scrape new data
    items = soup.select('.o-digest')
    for item in items:
        headline_elem = item.select_one('.o-digest__headline')
        summary_elem = item.select_one('.o-digest__summary')
        link_elem = item.select_one('.u-blocklink .faux-link')

        # Only proceed if all elements were found
        if headline_elem and summary_elem and link_elem:
            headline = headline_elem.text
            summary = summary_elem.text
            link = url + link_elem['href'].strip()

            # Scrape article page
            time.sleep(2)  # wait for 2 seconds to avoid being blocked
            article_response = s.get(link)
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            article_text = []
            for selector in ['.article__body p', '.episode-body p', '.page__body p']:
                elements = article_soup.select(selector)
                for element in elements:
                    article_text.append(element.text)

            data.append({'Headline': headline, 'Summary': summary, 'URL': link, 'ArticleText': article_text})

    # Get current date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    
    # Render homepage.html
    homepage_template = env.get_template('homepage.html')
    with open('index.html', 'w') as f:
        f.write(homepage_template.render(data=data, today=today))
    
    # Render article.html for each article
    article_template = env.get_template('article.html')
    for i, article in enumerate(data):
        with open(f'article_{i}.html', 'w') as f:
            f.write(article_template.render(article=article))

scrape_rnz()  # Run the function
