import requests
import requests_cache
from requests_cache import CachedSession



def fetch_html(url: str) -> str:
    """
    Fetches the HTML content of a given URL.
    
    :param url: The URL to fetch.
    :return: The HTML content as a string.
    """

    html_cached_session = CachedSession('cache/html_cache_283838', backend='sqlite')

    response = html_cached_session.get(url)
    response.raise_for_status()
    return response.text