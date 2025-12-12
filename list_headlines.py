from scrapers.terra_scraper import TerraScraper

def main():
    scraper = TerraScraper()
    print("Fetching headlines from Terra...")
    headlines = scraper.get_headlines()
    
    if not headlines:
        print("No headlines found.")
        return

    print(f"\nFound {len(headlines)} headlines:\n")
    for i, (title, url) in enumerate(headlines[:15]): # Limit to 15
        print(f"{i + 1}. {title}")
        print(f"   URL: {url}")
        print("-" * 40)

if __name__ == "__main__":
    main()
