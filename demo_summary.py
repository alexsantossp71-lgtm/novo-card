import sys
from scrapers.terra_scraper import TerraScraper
from services.summarizer import OllamaSummarizer
import json

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("--- Starting Demo ---")
    
    # 1. Setup
    scraper = TerraScraper()
    # Using a smaller/faster model if available, or just standard. Assuming llama3.2:3b per previous context
    summarizer = OllamaSummarizer(model="llama3.2:3b") 
    
    # 2. Get Headlines
    print("Fetching headlines...")
    headlines = scraper.get_headlines()
    if not headlines:
        print("No headlines found.")
        return

    # 3. Pick First Headline
    target_title, target_url = headlines[0]
    print(f"Selected Article: {target_title}")
    print(f"URL: {target_url}")

    # 4. Scrape
    print("Scraping content...")
    article_data = scraper.scrape(target_url)
    if not article_data.get('content'):
        print("No content found.")
        return

    # 5. Summarize
    print("Generating Summary with Ollama...")
    summary = summarizer.summarize(article_data['content'])

    # 6. Show Result
    print("\n--- Final Result (JSON) ---")
    result = {
        **article_data,
        "summary": summary
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
