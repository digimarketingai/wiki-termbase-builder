"""
termbase_builder.py
A Wikipedia + Google Translate bilingual termbase builder for translation students.
https://github.com/digimarketingai/wiki-termbase-builder
"""

import requests
import csv
import time
import sys

try:
    from deep_translator import GoogleTranslator
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False


class TermbaseBuilder:
    """Builds a bilingual termbase from Wikipedia categories with Google Translate fallback."""

    def __init__(
        self,
        source_lang="en",
        target_lang="ja",
        category="Translation studies",
        max_terms=50,
        output_file="termbase.csv",
        delay=0.2,
    ):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.category = category
        self.max_terms = max_terms
        self.output_file = output_file
        self.delay = delay
        self.api = f"https://{source_lang}.wikipedia.org/w/api.php"
        self.headers = {"User-Agent": "TermbaseBuilder/1.0 (github.com/digimarketingai)"}
        self.termbase = []
        self._stats = {"wiki": 0, "google": 0, "failed": 0}

        if HAS_GOOGLE:
            self._translator = GoogleTranslator(source=source_lang, target=target_lang)
        else:
            self._translator = None

    # ── WIKIPEDIA CRAWLING ──────────────────────────────────

    def _get_category_members(self):
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{self.category}",
            "cmtype": "page",
            "cmlimit": self.max_terms,
            "format": "json",
        }
        try:
            r = requests.get(self.api, params=params, headers=self.headers, timeout=10)
            r.raise_for_status()
            data = r.json()
            members = data.get("query", {}).get("categorymembers", [])
            return [m["title"] for m in members]
        except requests.RequestException as e:
            print(f"\n❌ Failed to fetch category '{self.category}': {e}")
            sys.exit(1)

    def _get_wiki_translation(self, title):
        params = {
            "action": "query",
            "titles": title,
            "prop": "langlinks",
            "lllang": self.target_lang,
            "format": "json",
        }
        try:
            r = requests.get(self.api, params=params, headers=self.headers, timeout=10)
            r.raise_for_status()
            pages = r.json()["query"]["pages"]
            for page in pages.values():
                links = page.get("langlinks", [])
                if links:
                    return links[0]["*"]
        except requests.RequestException:
            pass
        return None

    # ── GOOGLE TRANSLATE FALLBACK ───────────────────────────

    def _get_google_translation(self, title):
        if not self._translator:
            return None
        try:
            return self._translator.translate(title)
        except Exception:
            return None

    # ── MAIN BUILD ──────────────────────────────────────────

    def build(self):
        print("=" * 60)
        print(f"  📚 Termbase Builder")
        print(f"  Category : {self.category}")
        print(f"  Languages: {self.source_lang} → {self.target_lang}")
        print(f"  Max terms: {self.max_terms}")
        print(f"  Output   : {self.output_file}")
        print("=" * 60)

        if not HAS_GOOGLE:
            print("\n⚠  deep-translator not installed. Google fallback disabled.")
            print("   Install it with: pip install deep-translator\n")

        print(f"\n🔍 Fetching articles from Category:{self.category}...\n")
        titles = self._get_category_members()

        if not titles:
            print("❌ No articles found in this category. Check the spelling.")
            return []

        print(f"   Found {len(titles)} articles. Translating...\n")

        self.termbase = []
        self._stats = {"wiki": 0, "google": 0, "failed": 0}

        for i, title in enumerate(titles, 1):
            # try Wikipedia first
            translation = self._get_wiki_translation(title)
            source = "wikipedia"

            # fallback to Google
            if translation is None:
                translation = self._get_google_translation(title)
                source = "google"

            if translation:
                self.termbase.append((title, translation, source))
                tag = "W" if source == "wikipedia" else "G"
                self._stats[source if source == "google" else "wiki"] += 1
                print(f"  [{tag}] {i:>3}. {title:<45} → {translation}")
            else:
                self._stats["failed"] += 1
                print(f"  [✗] {i:>3}. {title:<45} → —")

            time.sleep(self.delay)

        self._save_csv()
        self._print_summary()
        return self.termbase

    # ── CSV EXPORT ──────────────────────────────────────────

    def _save_csv(self):
        with open(self.output_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([self.source_lang, self.target_lang, "domain", "source"])
            for src, tgt, origin in self.termbase:
                writer.writerow([src, tgt, self.category, origin])

    def _print_summary(self):
        print("\n" + "=" * 60)
        print(f"  ✅ Done! {len(self.termbase)} terms saved to {self.output_file}")
        print(f"     Wikipedia links : {self._stats['wiki']}")
        print(f"     Google Translate: {self._stats['google']}")
        print(f"     Not found       : {self._stats['failed']}")
        print("=" * 60)
