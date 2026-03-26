from datetime import datetime

class NewsParser:
    """
    Standardizes and cleans raw news data from various sources.
    
    This class is responsible for:
    1. normalizing nested JSON structures from the yfinance API.
    2. Parsing XML items from RSS feeds.
    3. Ensuring consistent output keys: headline, description, date_published, source, url.
    """

    def parse_yfinance_data(self, raw_data):
        """
        Parses raw dictionary data from the yfinance API.
        
        Args:
            raw_data (list): List of raw news dictionaries.
            
        Returns:
            list: List of clean, standardized article dictionaries.
        """
        articles = []
        for item in raw_data:
            # 1. Handle Nested Data Structures
            # Some international tickers return data inside a 'content' sub-dictionary.
            main_data = item
            if 'content' in item and isinstance(item['content'], dict):
                main_data = item['content']
            
            # 2. Extract Headline
            headline = main_data.get('title') or main_data.get('headline')
            
            # 3. Extract Description
            # We prioritize 'summary' as it is usually more descriptive than 'description'.
            description = main_data.get('summary') or main_data.get('description') or "No description available"
            
            # 4. Extract URL
            # The API often nests URLs inside 'clickThroughUrl'.
            url = None
            if 'clickThroughUrl' in main_data:
                if isinstance(main_data['clickThroughUrl'], dict):
                    url = main_data['clickThroughUrl'].get('url')
                else:
                    url = main_data['clickThroughUrl']
            
            # Fallback checks if clickThroughUrl failed
            if not url:
                url = main_data.get('url') or main_data.get('link') or main_data.get('canonicalUrl', {}).get('url')

            # 5. Extract & Format Date
            pub_time = "Unknown"
            if 'pubDate' in main_data:
                # Format: "2026-01-16T11:46:17Z" -> "2026-01-16 11:46:17"
                pub_time = main_data['pubDate'].replace('T', ' ').replace('Z', '')
            elif 'providerPublishTime' in main_data:
                # Format: Unix Timestamp -> "2026-01-16 11:46:17"
                pub_time = datetime.fromtimestamp(main_data['providerPublishTime']).strftime('%Y-%m-%d %H:%M:%S')

            # 6. Extract Source
            source = "Yahoo Finance"
            if 'provider' in main_data and isinstance(main_data['provider'], dict):
                source = main_data['provider'].get('displayName')
            elif 'publisher' in main_data:
                source = main_data['publisher']

            # Only append if we have the minimum requirements (Headline + URL)
            if headline and url:
                articles.append({
                    'headline': headline,
                    'description': description,
                    'date_published': pub_time,
                    'source': source,
                    'url': url
                })
        
        return articles

    def parse_rss_data(self, soup_items):
        """
        Parses XML items from a BeautifulSoup RSS feed object.
        
        Args:
            soup_items (list): List of BeautifulSoup <item> tags.
            
        Returns:
            list: List of clean, standardized article dictionaries.
        """
        articles = []
        for item in soup_items:
            try:
                # RSS feeds have a standard structure (<title>, <link>, <pubDate>)
                articles.append({
                    'headline': item.title.text,
                    'description': item.description.text if item.description else "",
                    'date_published': item.pubDate.text,
                    'source': "Yahoo RSS",
                    'url': item.link.text
                })
            except AttributeError:
                # Skip items that are missing required tags
                continue
                
        return articles