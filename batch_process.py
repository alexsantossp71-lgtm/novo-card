import sys
import json
import os
from scrapers.terra_scraper import TerraScraper
from services.summarizer import OllamaSummarizer

def save_news(data, index):
    os.makedirs('data', exist_ok=True)
    # Sanitize title for filename
    safe_title = "".join([c for c in data['title'] if c.isalpha() or c.isdigit() or c==' ']).strip().replace(' ', '_')
    filename = f"data/{index}_{safe_title}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {filename}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python batch_process.py <indices_comma_separated>")
        return

    sys.stdout.reconfigure(encoding='utf-8')
    
    indices_str = sys.argv[1]
    target_indices = [int(x.strip()) - 1 for x in indices_str.split(',')]
    
    print(f"Processing indices: {[i+1 for i in target_indices]}")

    scraper = TerraScraper()
    summarizer = OllamaSummarizer(model="llama3.2:3b")
    
    print("Fetching headlines...")
    headlines = scraper.get_headlines()
    
    if not headlines:
        print("No headlines found.")
        return

    for idx in target_indices:
        if 0 <= idx < len(headlines):
            title, url = headlines[idx]
            print(f"\n[{idx+1}] Processing: {title}")
            
            # Scrape
            article_data = scraper.scrape(url)
            if not article_data.get('content'):
                print("  -> Failed to get content.")
                continue

            # Summarize
            print("  -> Generating summary...")
            summary = summarizer.summarize(article_data['content'])
            
            # Merge
            full_data = {
                **article_data,
                "summary": summary
            }
            
            save_news(full_data, idx + 1)
        else:
            print(f"Index {idx+1} out of bounds.")

if __name__ == "__main__":
    main()
