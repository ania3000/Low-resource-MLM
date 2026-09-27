from typing import List
from tqdm import tqdm
from .config import CleanerConfig
from .cleaning import (
    load_documents,
    remove_internal_duplicates,
    remove_javascript_blocks,
    remove_noparse_tags,
    remove_javascript_garbage_lines,
    remove_html_garbage,
    remove_urls_and_emails,
    fix_linebreaks,
    get_common_lines,
    remove_common_lines,
    remove_source_artifacts,
    split_concatenated_names,
    filter_short_docs
)
from .deduplication import deduplicate_documents


def save_documents(docs: List[str], path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        for doc in docs:
            f.write(doc + "\n\n")

def preprocess_corpus(input_path: str, output_path: str, mode: str, config: CleanerConfig = None) -> None:
    if config is None:
        config = CleanerConfig()

    print("Загрузка и нормализация...")
    docs = load_documents(input_path, config.doc_start_marker)
    print(f"Документов до очистки: {len(docs)}")

    print("Удаление повторов внутри документов...")
    docs = [remove_internal_duplicates(doc) for doc in docs]

    if mode == 'ossetic':
        print("Удаление мусора (для осетинского)...")
        docs = [remove_javascript_blocks(doc) for doc in tqdm(docs, desc="JS blocks")]
        docs = [remove_noparse_tags(doc) for doc in docs]
        docs = [remove_javascript_garbage_lines(doc) for doc in tqdm(docs, desc="JS lines")]
        docs = [remove_html_garbage(doc) for doc in docs]
        docs = [remove_urls_and_emails(doc) for doc in docs]

    print("Удаление частотных строк...")
    docs = [fix_linebreaks(doc) for doc in docs]
    common_lines = get_common_lines(docs, config.common_line_threshold)
    docs = [remove_common_lines(doc, common_lines) for doc in docs]

    if mode == 'ossetic':
        print("Дополнительная нормализация (для осетинского)...")
        docs = [remove_source_artifacts(doc) for doc in docs]
        docs = [split_concatenated_names(doc) for doc in docs]

    print("Фильтрация коротких документов...")
    docs = filter_short_docs(docs, config.min_chars)
    print(f"После фильтрации: {len(docs)}")

    print("Дедупликация...")
    docs = deduplicate_documents(docs, config)
    print(f"После дедупликации: {len(docs)}")

    print("Сохранение результата...")
    docs = [doc for doc in docs if doc]
    save_documents(docs, output_path)
    print("Очистка завершена.")

def split_and_clean_sentences(input_path: str, output_path: str, mode: str) -> None:
    print(f"Чтение файла {input_path}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    print("Токенизация и фильтрация предложений...")
    cleaned_sentences = process_sentences_pipeline(text, mode)

    print(f"Сохранение {len(cleaned_sentences)} предложений в {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        for sentence in cleaned_sentences:
            f.write(sentence + '\n')
            
    print("Завершено!")
