import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from datetime import datetime

class Brasil247Scraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.brasil247.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def list_headlines(self):
        """
        Fetches the main headlines from the Brasil 247 homepage.
        Returns a list of dictionaries with 'title' and 'url'.
        """
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            headlines = []
            # Brasil 247 usually puts headlines in h2/h3 tags with links inside
            # We filter for internal links to avoid ads/external sites
            
            seen_urls = set()
            
            # Inspect h2 and h3 tags
            for tag_name in ['h2', 'h3']:
                for header in soup.find_all(tag_name):
                    link = header.find('a', href=True)
                    if link:
                        title = link.get_text(strip=True)
                        url = link['href']
                        
                        # Validate URL and Title
                        if not title or len(title) < 10:
                            continue
                            
                        # Handle relative URLs
                        if url.startswith('/'):
                            url = self.base_url + url
                        
                        # Filter out non-article links (heuristic)
                        if "brasil247.com" in url and url not in seen_urls:
                             # Basic filter to avoid category pages if possible, 
                             # though B247 structure is /category/title-slug, so counting slashes helps
                             path = url.replace(self.base_url, "")
                             if len(path.strip('/').split('/')) >= 2:
                                headlines.append((title, url))
                                seen_urls.add(url)
            
            return headlines[:15] # Return top 15

        except Exception as e:
            print(f"Error listing headlines from Brasil 247: {e}")
            return []

    def scrape(self, url):
        """
        Scrapes a specific article URL to extract content.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')

            # 1. Title
            title_tag = soup.select_one('h1.article__headline')
            title = title_tag.get_text(strip=True) if title_tag else "Sem Título"

            # 2. Date
            date_tag = soup.select_one('time.article__time')
            published_date = date_tag.get_text(strip=True) if date_tag else "Data não encontrada"

            # 3. Content
            # Get lead/subtitle first
            lead_tag = soup.select_one('h2.article__lead')
            lead_text = lead_tag.get_text(strip=True) if lead_tag else ""

            # Get main body
            content_div = soup.select_one('div.article__text')
            if content_div:
                paragraphs = content_div.find_all('p')
                body_text = "\n\n".join([p.get_text(strip=True) for p in paragraphs])
            else:
                body_text = ""
            
            full_content = f"{lead_text}\n\n{body_text}".strip()

            # 4. Author
            author_tag = soup.select_one('h2.authorBox__hdl a') or soup.find('meta', attrs={'name': 'author'})
            if author_tag:
                if hasattr(author_tag, 'get_text'): # It's an element
                     author = author_tag.get_text(strip=True)
                else: # It's a meta tag
                     author = author_tag.get('content', 'Desconhecido')
            else:
                author = "Brasil 247"

            return {
                'title': title,
                'url': url,
                'published_at': published_date,
                'author': author,
                'content': full_content
            }

        except Exception as e:
            print(f"Error scraping article {url}: {e}")
            return None
