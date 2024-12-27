from database_saver import save_to_database
from html_fetcher import fetch_html
from verb_scraper import fetch_verbs_from_multiple_pages 

def main():
    url_template = "https://corpus.quran.com/verbs.jsp?page={}"
    max_page = 11  
    all_verbs = fetch_verbs_from_multiple_pages(fetch_html_func=fetch_html, url_template=url_template, max_pages=max_page)
    save_to_database(all_verbs)
    print(f"Data saved to SQLite database.")

if __name__ == "__main__":
    main()
