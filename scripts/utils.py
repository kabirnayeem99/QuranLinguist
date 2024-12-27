import re


def normalize_verb(verb: str) -> str:
    verb = re.sub(r'آ', 'ا', verb)
    
    verb = re.sub(r'يٓ', 'ي', verb)
    
    verb = re.sub(r'ىٰ', 'ى', verb)
    
    verb = re.sub(r'ـٓ', '', verb)

    verb = re.sub(r'ءَا', 'آ', verb)

    verb = re.sub(r'ٱ', 'اِ', verb)

    # harakat_pattern = r'[\u064B-\u0652]' 
    # verb = re.sub(harakat_pattern, '', verb)
    
    return verb

def remove_last_letter_harakat(word: str) -> str:
    """
    Removes the harakat (diacritic) from the last letter of the given word.
    
    :param word: The Arabic word as a string.
    :return: The word with the last letter's harakat removed.
    """
    # Regular expression to match the last letter followed by a harakat
    harakat_pattern = r'([\u0621-\u064A])[\u064B-\u0652]$'
    
    # Replace the last letter's harakat with just the letter
    word = re.sub(harakat_pattern, r'\1', word)
    
    return word