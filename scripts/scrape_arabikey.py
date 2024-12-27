import logging
import os
import random
import time
from typing import List, Dict,Callable
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from utils import normalize_verb, remove_last_letter_harakat

def scrape_arabikey_for_verbs(verbs: List[str], on_save: Callable[[str,List[Dict[str, str]]], None], check_exist: Callable[[str], bool]) -> Dict[str, List[Dict[str, str]]]:

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("Starting scraping process for verbs from arabikey website.")

    scraped_verb_conjugs = {}
    total_verbs = len(verbs)
    processed_count = 0

    with sync_playwright() as p:
        
        unfound_verbs=[]
        playwright_cache_dir = 'cache/playwright'
        playwright_cache_dir = os.path.join(os.getcwd(), playwright_cache_dir)
        browser = p.chromium.launch_persistent_context(headless=True, user_data_dir=playwright_cache_dir)  
        page = browser.new_page()

        page.goto("https://arabikey.com/arabic-conjugator/")
        logging.info("Navigated to Arabikey conjugation tool.")

        for verb in verbs:

            processed_count += 1
            percentage_done = (processed_count / total_verbs) * 100
            logging.info(f"Progress: {processed_count}/{total_verbs} ({percentage_done:.2f}% completed)")

            if (check_exist(normalize_verb(verb))):
                logging.info(f"Skipping {verb}: already exists in the database.")
                print("\n")
                continue

            page.reload()
            logging.info(f"Searching conjugations for verb: {verb}")
            unfound_verbs.append(verb)

            conjugs = []

            page.wait_for_selector("input#con_verb")
            page.fill("input#con_verb", verb)
            page.click("button#conjugate-btn") 
            logging.debug(f"Filled and submitted verb: {verb}")

            delay = random.uniform(2, 5)
            logging.debug(f"Delaying for {delay:.2f} seconds.")
            time.sleep(delay)

            # suggestion_selector = f"tr[onclick*='{verb}']"
            # page.wait_for_selector(suggestion_selector) 
            # page.click(suggestion_selector)

            page.wait_for_selector("table:nth-of-type(2)")

            second_table = page.locator("table:nth-of-type(2)")
            table_html = second_table.inner_html()

            conjug_verbs_table_parser = BeautifulSoup(table_html, "html.parser")
            table_headers = [th.get_text(strip=True) for th in conjug_verbs_table_parser.find_all('th')]

            table_rows = conjug_verbs_table_parser.find_all('tr')

            for row in table_rows:
                cols = row.find_all('td')
                if cols:
                    row_data = {table_headers[i]: cols[i].get_text(strip=True) for i in range(len(cols))}
                    conjugs.append(row_data)

            perfect_verb_form = next((item for item in conjugs if item.get('الضمائرPronouns') == 'هو'), None)
            if perfect_verb_form:
                perfect_verb = normalize_verb(perfect_verb_form['الماضي المعلومPerfect'])
                if verb==perfect_verb or remove_last_letter_harakat(verb) == remove_last_letter_harakat(perfect_verb):
                    logging.info(f"Saving {verb} to the database.")
                    scraped_verb_conjugs[verb] = conjugs  
                    unfound_verbs.remove(verb)
                    on_save(verb, conjugs)
                else:
                    logging.warning(f"{verb} not saved: mismatch with 'الماضي المعلومPerfect': {perfect_verb}")
            else:
                logging.warning(f"No valid conjugation found for {verb}.")

            page.reload()
            delay = random.uniform(2, 5)
            logging.debug(f"Delaying for {delay:.2f} seconds.")
            time.sleep(delay)
            print("\n")

        logging.info(f"Unfound verbs: {unfound_verbs}")
        browser.close()

    return scraped_verb_conjugs
