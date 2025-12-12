from .base_scraper import BaseScraper
from typing import List, Dict, Tuple

class TerraScraper(BaseScraper):
    def scrape(self, url: str) -> Dict[str, str]:
        soup = self.get_soup(url)
        if not soup:
            return {}

        data = {'url': url}
        
        # Title
        title_tag = soup.find('h1') or soup.find('h1', class_='article__header__title')
        data['title'] = title_tag.get_text(strip=True) if title_tag else "No Title"

        # Date Extraction
        date = ""
        # Try different meta tags
        meta_candidates = [
            ('property', 'article:published_time'),
            ('name', 'publish-date'),
            ('name', 'publishdate')
        ]
        
        for attr, value in meta_candidates:
            meta = soup.find('meta', {attr: value})
            if meta:
                date = meta.get('content')
                if date: break
        
        if not date:
            time_tag = soup.find('time')
            if time_tag:
                 if 'datetime' in time_tag.attrs:
                     date = time_tag['datetime']
                 else:
                     date = time_tag.get_text(strip=True)
        
        data['date'] = date

        # Content Extraction
        # Priority: article tag -> div with specific classes -> fallback to p tags in body
        article = soup.find('article')
        if not article:
             article = soup.find('div', class_='article__content')
        
        if article:
             paragraphs = article.find_all('p')
             data['content'] = "\n\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        else:
             # Fallback: grab all P tags that are not in header/footer/nav
             # This is a bit rough, but functional for a general scraper
             paragraphs = soup.find_all('p')
             content = []
             for p in paragraphs:
                 # Exclude headers, footers, etc based on parents
                 if p.find_parent(['header', 'footer', 'nav']):
                     continue
                 text = p.get_text(strip=True)
                 if len(text) > 40:
                     content.append(text)
             data['content'] = "\n\n".join(content)
        
        return data

    def get_headlines(self) -> List[Tuple[str, str]]:
        url = "https://www.terra.com.br/noticias/"
        soup = self.get_soup(url)
        if not soup:
            return []

        headlines = []
        candidates = soup.find_all(['h2', 'h3'])
        for tag in candidates:
            parent_link = tag.find_parent('a')
            if parent_link and parent_link.get('href'):
                text = tag.get_text(strip=True)
                link = parent_link.get('href')
                if len(text) > 20: 
                    headlines.append((text, link))
            
            link_inside = tag.find('a')
            if link_inside and link_inside.get('href'):
                text = link_inside.get_text(strip=True)
                link = link_inside.get('href')
                if len(text) > 20:
                    headlines.append((text, link))

        seen = set()
        unique_headlines = []
        for t, l in headlines:
            if l not in seen and t not in seen:
                seen.add(l)
                seen.add(t)
                unique_headlines.append((t, l))

        return unique_headlines
