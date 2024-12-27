from bs4 import BeautifulSoup
from typing import List, Dict, Callable
from html_fetcher import fetch_html

def fetch_verbs_from_multiple_pages(fetch_html_func: Callable[[str], str], url_template: str, max_pages: int) -> List[Dict[str, str]]:
    """
    Fetches verb data from multiple pages based on a URL template and a maximum number of pages.
    
    :param fetch_html_func: Function to fetch HTML content from a URL.
    :param url_template: The URL template containing a placeholder for the page number.
    :param max_pages: The maximum number of pages to scrape.
    :return: A list of all verb data scraped from the pages.
    """
    page_number = 1
    all_verbs = []

    while True:
        url = url_template.format(page_number)
        verb_data = extract_verbs(fetch_html_func=fetch_html_func, url=url)
        
        if not verb_data or page_number > max_pages:
            break  

        all_verbs.extend(verb_data)  
        page_number += 1  

    return all_verbs

def extract_verbs(fetch_html_func: Callable[[str], str], url: str) -> List[Dict[str, str]]:
    """
    Extracts verb data from a single page using the provided URL.
    
    :param fetch_html_func: A function to fetch HTML content from a URL.
    :param url: The URL of the webpage to scrape.
    :return: A list of dictionaries containing verb data from the page.
    """
    html_content = fetch_html_func(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    table = soup.find('table', class_='verbTable')
    if not table:
        return []  

    rows = table.find_all('tr')[1:] 

    verbs = []
    for row in rows:
        cols = row.find_all('td')
        verbs.append({
            "Verb": cols[0].text.strip(),
            "Root": cols[1].text.strip(),
            "Form": cols[2].text.strip(),
            "Frequency": cols[3].text.strip(),
            "Translation": cols[4].text.strip()
        })

    return verbs
