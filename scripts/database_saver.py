import sqlite3
from typing import List, Dict 

def save_to_database(data: List[Dict[str, str]], db_name: str = "Quran_words.db"):
    """
    Saves verb data to an SQLite database.
    
    :param data: A list of dictionaries containing verb data.
    :param db_name: The name of the SQLite database file.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create the table if it doesn't already exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS verbs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        verb TEXT,
        root TEXT,
        form TEXT,
        translation TEXT,
        frequency INTEGER
    )
    """)

    for item in data:
        cursor.execute("""
        INSERT INTO verbs (verb, root, form, translation, frequency)
        VALUES (:Verb, :Root, :Form, :Translation, :Frequency)
        """, item)
    
    conn.commit()
    conn.close()