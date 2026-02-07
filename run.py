"""
run.py — Edit the 5 settings below, then run: python run.py
"""

from termbase_builder import TermbaseBuilder

# ╔══════════════════════════════════════════════════════════╗
# ║  ✏️  EDIT YOUR SETTINGS HERE                            ║
# ╚══════════════════════════════════════════════════════════╝

SOURCE_LANG = "en"                  # source language code
TARGET_LANG = "zh"                  # target language code
CATEGORY    = "Translation studies" # Wikipedia category name
MAX_TERMS   = 50                    # max number of terms
OUTPUT_FILE = "termbase.csv"        # output file name

# ╔══════════════════════════════════════════════════════════╗
# ║  🚀  DON'T CHANGE ANYTHING BELOW THIS LINE              ║
# ╚══════════════════════════════════════════════════════════╝

if __name__ == "__main__":
    builder = TermbaseBuilder(
        source_lang=SOURCE_LANG,
        target_lang=TARGET_LANG,
        category=CATEGORY,
        max_terms=MAX_TERMS,
        output_file=OUTPUT_FILE,
    )
    builder.build()
