import requests
from bs4 import BeautifulSoup
import json
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
            link = url + link_elem['href']

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

    # Write data to a JSON file
    with open('index.html', 'w') as f:
        f.write('<html><body>')
        for item in data:
            f.write('<h1>' + item['Headline'] + '</h1>')
            f.write('<p>' + item['Summary'] + '</p>')
            f.write('<a href="' + item['URL'] + '">Read more</a>')
            for paragraph in item['ArticleText']:
                f.write('<p>' + paragraph + '</p>')
        f.write('</body></html>')

scrape_rnz()  # Run the function
