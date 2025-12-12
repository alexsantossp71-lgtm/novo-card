import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from typing import Dict, Optional

class BaseScraper(ABC):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    @abstractmethod
    def scrape(self, url: str) -> Dict[str, str]:
        """
        Scrape appropriate data from the given URL.
        Returns a dictionary with keys like 'title', 'content', 'author', 'date'.
        """
        pass
