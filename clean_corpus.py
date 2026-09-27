import argparse
from corpus_cleaner import preprocess_corpus, CleanerConfig

def main():
    parser = argparse.ArgumentParser(description="Инструмент очистки и дедупликации корпусов.")
    
    parser.add_argument("-i", "--input", required=True, help="Путь к входному файлу корпуса")
    parser.add_argument("-o", "--output", required=True, help="Путь к выходному файлу")
    parser.add_argument(
        "-m", "--mode", 
        choices=["ossetic", "tajik"], 
        default="tajik", 
        help="Выбор языка (default: tajik)"
    )
    parser.add_argument("--min-chars", type=int, default=200, help="Минимальная длина документа в символах")
    parser.add_argument("--lsh-threshold", type=float, default=0.8, help="Порог схожести для LSH-дедупликации (0.0 - 1.0)")

    args = parser.parse_args()

    # Передаем кастомные параметры, если они были переданы через CLI
    config = CleanerConfig(
        min_chars=args.min_chars,
        lsh_threshold=args.lsh_threshold
    )

    preprocess_corpus(
        input_path=args.input,
        output_path=args.output,
        mode=args.mode,
        config=config
    )

if __name__ == "__main__":
    main()
