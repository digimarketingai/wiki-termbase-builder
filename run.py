"""
run.py — Run from terminal. Use --help to see all options.

Examples:
    python run.py
    python run.py --source en --target zh --category "Cardiology"
    python run.py -s en -t fr -c "Contract law" -m 100 -o legal.csv
"""

import argparse
from termbase_builder import TermbaseBuilder


def main():
    parser = argparse.ArgumentParser(
        description="📚 Wiki Termbase Builder — build bilingual glossaries from Wikipedia",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python run.py
  python run.py -s en -t zh -c "Cardiology" -m 30
  python run.py --source en --target ko --category "Contract law"
  python run.py -t fr -o french_terms.csv

common language codes:
  en  English       zh  Chinese (Simplified)
  fr  French        ja  Japanese
  de  German        ko  Korean
  es  Spanish       ar  Arabic
  pt  Portuguese    ru  Russian
        """,
    )

    parser.add_argument(
        "-s", "--source",
        default="en",
        help="source language code (default: en)",
    )
    parser.add_argument(
        "-t", "--target",
        default="ja",
        help="target language code (default: ja)",
    )
    parser.add_argument(
        "-c", "--category",
        default="Translation studies",
        help='Wikipedia category name (default: "Translation studies")',
    )
    parser.add_argument(
        "-m", "--max",
        type=int,
        default=50,
        help="max number of terms to fetch (default: 50)",
    )
    parser.add_argument(
        "-o", "--output",
        default="termbase.csv",
        help="output CSV file name (default: termbase.csv)",
    )

    args = parser.parse_args()

    builder = TermbaseBuilder(
        source_lang=args.source,
        target_lang=args.target,
        category=args.category,
        max_terms=args.max,
        output_file=args.output,
    )
    builder.build()


if __name__ == "__main__":
    main()
