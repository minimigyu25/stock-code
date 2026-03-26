import time
import random
import re
import requests
import yfinance as yf
from bs4 import BeautifulSoup

class NewsScraper:
    """
    Handles the fetching and scraping of news articles.
    
    Capabilities:
    1. Fetch list of recent news from Yahoo Finance via API.
    2. Visit individual article URLs to scrape full textual content.
    3. Clean and normalize text data (remove artifacts, fix spacing).
    """

    def __init__(self):
        # Emulate a real browser to avoid being blocked by Yahoo's anti-bot protections
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }

    def fetch_via_yfinance(self, ticker):
        """
        Fetches the initial list of news metadata using the yfinance API.
        
        Args:
            ticker (str): The stock ticker (e.g., 'TATATECH.NS')
            
        Returns:
            list: A list of raw news dictionaries provided by Yahoo.
        """
        print(f"📡 Fetching news metadata for {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            return news if news else []
        except Exception as e:
            print(f"❌ Error fetching metadata: {e}")
            return []

    def clean_text(self, text):
        """
        Sanitizes raw scraped text by removing invisible characters, 
        legal disclaimers, and correcting whitespace.
        
        Args:
            text (str): Raw text from the HTML.
            
        Returns:
            str: Cleaned, human-readable text.
        """
        if not text:
            return ""

        # 1. Remove invisible Unicode characters (Zero-width spaces, etc.)
        text = text.replace('\u200b', '').replace('\u2060', '').replace('\ufeff', '')

        # 2. Remove standard footer patterns (e.g., "Reporting by...")
        # This removes the journalist credits usually found at the bottom of Reuters/Bloomberg articles
        text = re.sub(r'\(\s*Reporting by.*?\)', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\(\s*Editing by.*?\)', '', text, flags=re.IGNORECASE)

        # 3. Fix Whitespace issues
        # Convert non-breaking spaces to normal spaces
        text = text.replace('\xa0', ' ')
        # Collapse multiple spaces into one
        text = re.sub(r' +', ' ', text)
        
        # 4. Paragraph Formatting
        # Consolidate multiple newlines into a single paragraph break
        text = re.sub(r'\n\s*\n', '\n\n', text) 
        text = re.sub(r'\n+', '\n', text)
        
        return text.strip()

    def scrape_full_article(self, url):
        """
        Visits the specific article URL to extract the full body text.
        Includes random delays to act politely towards the server.
        
        Args:
            url (str): The direct link to the news article.
            
        Returns:
            str: The full, cleaned text of the article.
        """
        # skip non-yahoo links (e.g., external ads or specialized reports)
        if not url or "yahoo.com" not in url:
            return "Skipped (External Link or Video)"

        # Log only the first 60 chars of URL to keep terminal clean
        print(f"   🕵️‍♂️ Scraping full text: {url[:60]}...")
        
        try:
            # Polite delay (1-2 seconds) to prevent Rate Limiting (Error 429)
            time.sleep(random.uniform(1, 2))
            
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return f"Error: HTTP Status {response.status_code}"

            soup = BeautifulSoup(response.content, 'html.parser')

            # --- Extraction Strategy ---
            # Yahoo usually wraps the main content in 'data-testid="article-body"'
            article_body = soup.find('div', {'data-testid': 'article-body'})
            
            # Fallback for older Yahoo layouts
            if not article_body:
                article_body = soup.find('div', class_='caas-body')

            if article_body:
                # Find all paragraph tags <p> inside the body
                paragraphs = article_body.find_all('p')
                
                # Join paragraphs with a newline
                raw_text = "\n".join([p.text.strip() for p in paragraphs])
                
                # Apply cleaning rules
                return self.clean_text(raw_text)
            
            return "Error: Could not find article body in HTML."

        except Exception as e:
            return f"Error during scraping: {str(e)}"