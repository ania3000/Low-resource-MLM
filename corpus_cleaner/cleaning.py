import re
import unicodedata
from collections import Counter
from typing import List, Set

def normalize_text(text: str) -> str:
    return unicodedata.normalize('NFC', text.strip())

def load_documents(path: str, doc_marker: str = "===") -> List[str]:
    with open(path, 'r', encoding='utf-8') as f:
        lines = [normalize_text(line) for line in f]
      
    docs, current_doc = [], []
    for line in lines:
        if line.startswith(doc_marker):
            if current_doc:
                docs.append("\n".join(current_doc).strip())
                current_doc = []
            continue
        current_doc.append(line)
    
    if current_doc:
        docs.append("\n".join(current_doc).strip())

    return [doc for doc in docs if doc]

def remove_internal_duplicates(doc: str) -> str:
    lines, seen, cleaned = doc.splitlines(), set(), []
    for line in lines:
        if line not in seen:
            cleaned.append(line)
            seen.add(line)
    return "\n".join(cleaned)

def remove_javascript_blocks(text: str) -> str:
    text = text.replace('\xa0', ' ')
    text = text.replace('ӏ', 'l').replace('Ӏ', 'l').replace('ӏd', 'id')
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'\$\([^)]+\)\.(ready|setup|on|click|play)?\s*\([^)]*\)\s*\{.*?\}\s*;?', '', text, flags=re.DOTALL)
    text = re.sub(r'function\s*\([^)]*\)\s*\{.*?\}', '', text, flags=re.DOTALL)
    text = re.sub(r'setup\s*\([^)]*\)\s*\{.*?\}', '', text, flags=re.DOTALL)
    
    js_keywords = [
        r'html5videoFunctions', r'flashvars', r'playlistUrl', r'playlistParams',
        r'gaVideosCounter', r'tnsVideosCounter', r'\btype\s*:\s*[\'"]?(flash|html5|download)[\'"]?',
        r'container.?id', r'\bauto(start|play)\b', r'id\s*:\s*["\']?\d+["\']?',
        r'sourceid', r'article_id', r'adv\s*:\s*["\']?\d+["\']?', r'viewCount',
        r'["\']?directLink["\']?\s*:\s*["\']?.*?["\']?'
    ]
    for pattern in js_keywords:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    return text

def remove_javascript_garbage_lines(text: str) -> str:
    lines = text.splitlines()
    js_like_patterns = [
        r'Ваш браузер.*?видео', r'typeof', r'\$\(\)', r'\[.*?\]\s*=\s*', r'html5video',
        r'flashvars', r'player\(".*?"\)', r'(?:\d+:\d+)\s*/\s*\d+\.\d+Mb', r'Sputnik',
        r'viewCount', r'Subject', r'adv\s*:', r'\.setup\(', r'rianplayer', r'\.play\(\)',
        r'autostart',
    ]
    cleaned = [line for line in lines if not any(re.search(pat, line, re.IGNORECASE) for pat in js_like_patterns)]
    return "\n".join(cleaned)

def remove_noparse_tags(text: str) -> str:
    return re.sub(r'<\/?noparse>', '', text, flags=re.IGNORECASE)

def remove_html_garbage(text: str) -> str:
    text = re.sub(r'</?[a-z][^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'&[a-z]+;', '', text)
    return text

def remove_urls_and_emails(text: str) -> str:
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    return text

def remove_source_artifacts(text: str) -> str:
    return re.sub(r'\bSputnik\s*/\s*', '', text)

def split_concatenated_names(text: str) -> str:
    return re.sub(r'(?<=[а-яё])(?=[А-ЯЁ])', ' ', text)

def fix_linebreaks(text: str) -> str:
    pattern = re.compile(r'(?<![\.\?!…])\n(?!\n)')
    return pattern.sub(' ', text)

def get_common_lines(docs: List[str], threshold: int) -> Set[str]:
    line_counts = Counter()
    for doc in docs:
        for line in doc.splitlines():
            line_counts[line.strip()] += 1
    return {line for line, count in line_counts.items() if count > threshold}

def remove_common_lines(doc: str, common_lines: Set[str]) -> str:
    return "\n".join([line for line in doc.splitlines() if line.strip() not in common_lines])

def filter_short_docs(docs: List[str], min_chars: int) -> List[str]:
    def is_valid(doc: str) -> bool:
        cleaned = re.sub(r'[\W_]+', '', doc)
        return len(cleaned) >= min_chars
    return [doc for doc in docs if is_valid(doc)]
