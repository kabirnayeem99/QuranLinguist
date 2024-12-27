import sqlite3
from typing import List, Dict 


def setup_database():
    conn = sqlite3.connect("Quran_words.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verb_conjugations (
            verb TEXT,
            pronoun TEXT,
            imperfect_passive TEXT,
            perfect_passive TEXT,
            emphatic_imperative TEXT,
            imperative TEXT,
            emphatic_imperfect TEXT,
            subjunctive TEXT,
            jussive TEXT,
            imperfect TEXT,
            perfect TEXT,
            PRIMARY KEY (verb, pronoun)
        )
    """)

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

    conn.commit()
    conn.close()
    return conn

def save_verbs_to_db(data: List[Dict[str, str]], db_name: str = "Quran_words.db"):
    """
    Saves verb data to an SQLite database.
    
    :param data: A list of dictionaries containing verb data.
    :param db_name: The name of the SQLite database file.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    

    for item in data:
        cursor.execute("""
        INSERT INTO verbs (verb, root, form, translation, frequency)
        VALUES (:Verb, :Root, :Form, :Translation, :Frequency)
        """, item)
    
    conn.commit()
    conn.close()

def save_verb_conjugs_to_db(verb: str, verb_conj: List[Dict[str, str]], db_name: str = "Quran_words.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    for row in verb_conj:
        cursor.execute("""
            INSERT OR IGNORE INTO verb_conjugations (
                verb,
                pronoun,
                imperfect_passive,
                perfect_passive,
                emphatic_imperative,
                imperative,
                emphatic_imperfect,
                subjunctive,
                jussive,
                imperfect,
                perfect
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            verb,
            row.get('الضمائرPronouns', ''),
            row.get('المضارع المجهولImperfect Passive', ''),
            row.get('الماضي المجهولPerfect Passive', ''),
            row.get('الأمر المؤكدEmphatic Imperative', ''),
            row.get('الأمرImperative', ''),
            row.get('المضارع المؤكد الثقيلEmphatic Imperfect', ''),
            row.get('المضارع المنصوبSubjunctive', ''),
            row.get('المضارع المجزومJussive', ''),
            row.get('المضارع المعلومImperfect', ''),
            row.get('الماضي المعلومPerfect', '')
        ))

    conn.commit()

def check_verb_exists(verb: str, db_name: str = "Quran_words.db") -> bool:
    """
    Checks if the verb exists in the 'verb_conjugations' table in the database.

    :param verb: The verb to check.
    :param db_name: The name of the SQLite database file.
    :return: True if the verb exists in the 'verb_conjugations' table, otherwise False.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM verb_conjugations WHERE verb = ?
    """, (verb,))
    
    # Fetch one result, if the verb exists, it will return 1, otherwise None.
    result = cursor.fetchone()

    conn.close()

    return result is not None