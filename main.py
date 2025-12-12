import argparse
import json
import os
from scrapers.g1_scraper import G1Scraper

def save_to_json(data, filename):
    os.makedirs('data', exist_ok=True)
    filepath = os.path.join('data', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filepath}")

def main():
    parser = argparse.ArgumentParser(description="News Scraper System")
    parser.add_argument('url', help="URL of the news article to scrape")
    parser.add_argument('--source', default='g1', help="Source type (default: g1)")
    
    args = parser.parse_args()

    scraper = None
    if args.source.lower() == 'g1':
        scraper = G1Scraper()
    else:
        print(f"Source '{args.source}' not supported yet.")
        return

    print(f"Scraping {args.url}...")
    article_data = scraper.scrape(args.url)

    if article_data:
        print("Scraping successful!")
        filename = f"article_{os.urandom(4).hex()}.json"
        save_to_json(article_data, filename)
    else:
        print("Failed to scrape the article.")

if __name__ == "__main__":
    main()
