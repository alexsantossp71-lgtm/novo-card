import sys
import json
import os
from scrapers.terra_scraper import TerraScraper
from scrapers.brasil247_scraper import Brasil247Scraper
from services.prompt_generator import OllamaPromptGenerator
from services.summarizer import OllamaSummarizer

def save_news(data, index):
    os.makedirs('data', exist_ok=True)
    # Sanitize title for filename
    safe_title = "".join([c for c in data['title'] if c.isalpha() or c.isdigit() or c==' ']).strip().replace(' ', '_')
    filename = f"data/{index}_{safe_title[:50]}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"News saved to: {filename}")

def main():
    # encoding setup
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Initialize
    summarizer = OllamaSummarizer(model="llama3.2:3b")
    prompt_generator = OllamaPromptGenerator(model="llama3.2:3b")

    print("Select Source:")
    print("1. Terra")
    print("2. Brasil 247")
    src_choice = input("Enter number (default 1): ").strip()

    if src_choice == '2':
        scraper = Brasil247Scraper()
        print("Fetching headlines from Brasil 247...")
        headlines = scraper.list_headlines()
    else:
        scraper = TerraScraper()
        print("Fetching headlines from Terra...")
        headlines = scraper.get_headlines()
    
    if not headlines:
        print("No headlines found.")
        return

    # List headlines
    print(f"\nFound {len(headlines)} headlines:\n")
    for i, (title, url) in enumerate(headlines[:20]):
        print(f"{i + 1}. {title}")
    
    # Selection
    print("\n" + "-"*40)
    selection = input("Enter the numbers of the news to process (comma separated, e.g. 1, 3, 5): ")
    
    try:
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
    except ValueError:
        print("Invalid input. Please enter numbers.")
        return

    # Process
    for idx in indices:
        if 0 <= idx < len(headlines):
            title, url = headlines[idx]
            print(f"\nProcessing: {title}...")
            
            # Scrape
            print("  Scraping content...")
            article_data = scraper.scrape(url)
            
            if not article_data.get('content'):
                print("  Failed to extract content or empty content.")
                continue

            # Summarize
            print("  Generating summary (this may take a moment)...")
            summary = summarizer.summarize(article_data['content'])
            
            # Generate Image Prompts
            print("  Generating image prompts...")
            prompts = prompt_generator.generate_prompts(summary)
            
            # Merge data
            full_data = {
                **article_data,
                "summary": summary,
                "prompts": prompts
            }
            
            # Save
            save_news(full_data, idx + 1)
            
            print("  Done!")
        else:
            print(f"Skipping invalid index: {idx + 1}")

if __name__ == "__main__":
    main()
