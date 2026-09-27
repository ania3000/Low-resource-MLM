import argparse
from corpus_cleaner import split_and_clean_sentences

def main():
    parser = argparse.ArgumentParser(description="Разбиение на предложения и фильтрация.")
    parser.add_argument("-i", "--input", required=True, help="Путь к обработанному корпусу")
    parser.add_argument("-o", "--output", required=True, help="Путь для сохранения предложений")
    parser.add_argument(
        "-m", "--mode", 
        choices=["ossetic", "tajik"], 
        default="tajik", 
        help="Режим (ossetic/tajik)"
    )

    args = parser.parse_args()
    split_and_clean_sentences(
        input_path=args.input,
        output_path=args.output,
        mode=args.mode
    )

if __name__ == "__main__":
    main()
