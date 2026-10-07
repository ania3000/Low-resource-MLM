import re
from typing import List
import nltk

def ensure_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)

def tokenize_sentences(text: str, mode: str) -> List[str]:
    if mode == 'ossetic':
        sentence_endings = re.compile(r'(?<=[.+!?])\s+(?=[\—0-9a-zA-Zа-яА-ЯÆӔæӕ])')
        return sentence_endings.split(text)
    elif mode == 'tajik':
        ensure_nltk_resources()
        sentences = nltk.sent_tokenize(text, language='russian')
        return [s.strip().replace('\t', ' ') for s in sentences if s]
    else:
        raise ValueError(f"Неизвестный режим: {mode}")

def normalize_word(word: str) -> str:
    if len(word) > 1 and word[0].isupper() and word[1:].islower():
        return word
    if not word.islower() and not word.isupper():
        return word.lower()
    return word

def clean_sentence(sentence: str, mode: str) -> str:
    sentence = sentence.strip()
    sentence = re.sub(r'^[\s\.,!?»]+', '', sentence)

    if mode == 'ossetic':
        sentence = re.sub(r"\(\.\.\.\) ", '', sentence)
        sentence = sentence.replace("¬", '')
        sentence = sentence.replace("{", "(")

    garbage_chars = r'[ÀÂÃÄÇÊÌÍÎÏÑÒÓÔÕÙÝÞàáâãäåçèéêëìíîïðñòóôõöùúûüÿāœЉљўџґδӡ]'
    if sentence and re.search(garbage_chars, sentence):
        return ''
    if sentence and len([ch for ch in sentence if ch.isalpha()]) == 1:
        return ''

    if mode == 'ossetic':
        if not re.search(r'[а-яӕæ]', sentence): 
            return ''
        mixed_word_pattern = r'\b(?=\w*[a-zA-Z])(?=\w*[а-яА-ЯӔӕÆæ])\w+\b'
        if sentence and re.search(mixed_word_pattern, sentence): 
            return ''
        if sentence and not re.search(r'[а-яА-ЯӔӕÆæ]', sentence): 
            return ''

        if sentence and re.search(r"М\.", sentence):
            return ''
        if sentence and re.search(r'[MDCLXVI]+', sentence):
            return ''
        if sentence and re.match(r'^[A-ZА-ЯӔÆ][A-ZА-ЯӔÆa-zа-яӕæ]+ [A-ZА-ЯӔÆ][A-ZА-ЯӔÆa-zа-яӕæ]+\.$', sentence):
            return ''

    elif mode == 'tajik':
        if not re.search(r'[а-яӷҷӣқӯҳ]', sentence):  
            return ''
        mixed_word_pattern = r'\b(?=\w*[a-zA-Z])(?=\w*[а-яА-ЯӶӷҶҷӢӣҚқӮӯҲҳ])\w+\b'
        if sentence and re.search(mixed_word_pattern, sentence):  
            return ''
        if sentence and not re.search(r'[а-яА-ЯӶӷҶҷӢӣҚқӮӯҲҳ]', sentence):  
            return ''

    if sentence and sentence[0].isalpha():
        sentence = sentence[0].upper() + sentence[1:]

    if sentence:
        words = sentence.split()
        words = [normalize_word(w) for w in words]
        return " ".join(words)

    return ''

def process_sentences_pipeline(text: str, mode: str) -> List[str]:
    raw_sentences = tokenize_sentences(text, mode)
    cleaned_sentences = []

    for raw_s in raw_sentences:
        s = clean_sentence(raw_s, mode)
        if s:
            cleaned_sentences.append(s)
    return cleaned_sentences
