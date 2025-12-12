from .base_scraper import BaseScraper
from typing import Dict

class G1Scraper(BaseScraper):
    def scrape(self, url: str) -> Dict[str, str]:
        soup = self.get_soup(url)
        if not soup:
            return {}

        data = {'url': url}

        # Extract Title
        title_tag = soup.find('h1', class_='content-head__title') or soup.find('h1')
        data['title'] = title_tag.get_text(strip=True) if title_tag else "No Title Found"

        # Extract Subtitle/Summary
        subtitle_tag = soup.find('h2', class_='content-head__subtitle')
        data['summary'] = subtitle_tag.get_text(strip=True) if subtitle_tag else ""

        # Extract Author
        author_tag = soup.find('p', class_='content-publication-data__from')
        data['author'] = author_tag.get_text(strip=True) if author_tag else "Unknown"

        # Extract Date
        date_tag = soup.find('time')
        data['date'] = date_tag['datetime'] if date_tag and 'datetime' in date_tag.attrs else ""

        # Extract Content
        # G1 content is usually in 'article' tag or specific divs
        article_body = soup.find('article')
        if article_body:
            paragraphs = article_body.find_all('p')
            # Filter out empty paragraphs or metadata
            content = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
            data['content'] = "\n\n".join(content)
        else:
            data['content'] = ""

        return data
