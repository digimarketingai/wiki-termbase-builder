# 📚 Wiki Termbase Builder

A simple Python tool that **automatically builds bilingual glossaries** from Wikipedia — designed for **translation students** and language professionals.

Give it a Wikipedia category and a language pair, and it crawls every article title, finds the equivalent term in your target language via Wikipedia's interlanguage links, and falls back to Google Translate when no link exists. The output is a clean CSV you can import into CAT tools like **SDL Trados**, **memoQ**, **OmegaT**, or any spreadsheet app.

## ✨ Features

- **Wikipedia-first approach** — uses human-curated interlanguage links (high quality)
- **Google Translate fallback** — fills gaps automatically so you always get a result
- **Source tagging** — every term is tagged `wikipedia` or `google` so you know what to review
- **CSV output** — directly importable into professional CAT tools and termbases
- **UTF-8 with BOM** — opens correctly in Excel for CJK languages (Chinese, Japanese, Korean)
- **Zero configuration** — edit 5 lines, run one command

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/digimarketingai/wiki-termbase-builder.git
cd wiki-termbase-builder
