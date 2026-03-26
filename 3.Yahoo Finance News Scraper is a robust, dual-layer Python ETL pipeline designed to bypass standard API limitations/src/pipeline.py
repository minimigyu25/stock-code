import os
import json
import time
import random
import pandas as pd
from src.scraper import NewsScraper
from src.parser import NewsParser

# ==========================================
# 1. CORE LOGIC (Process One Ticker)
# ==========================================
def process_ticker(ticker, scraper, parser, output_dir):
    """
    Runs the full scraping pipeline for a single ticker.
    Returns: list of articles (or empty list if failed).
    """
    print(f"\n🚀 Processing: {ticker}...")
    
    # A. Fetch preliminary data (Fast List)
    raw_data = scraper.fetch_via_yfinance(ticker)
    
    # B. Parse basic metadata
    articles = parser.parse_yfinance_data(raw_data)

    if not articles:
        print(f"   ⚠️ No news found for {ticker}.")
        return []

    print(f"   📨 Found {len(articles)} articles. Starting deep scrape...")

    # C. Enrichment Loop (Deep Scrape)
    # We scrape ALL articles found.
    for i, article in enumerate(articles):
        url = article['url']
        
        # Scrape and clean full text
        full_text = scraper.scrape_full_article(url)
        
        if len(full_text) > 50: 
            article['description'] = full_text
        else:
            # Keep the short summary if deep scrape failed/skipped
            pass 

    # D. Save Individual File (Backup)
    # We save individual files just in case the batch crashes halfway
    ticker_clean = ticker.replace('.NS', '').replace('.BO', '') # Clean name for filename
    file_path = os.path.join(output_dir, f"{ticker_clean}_news.json")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)
        
    print(f"   ✅ Saved {len(articles)} articles to {file_path}")
    return articles

# ==========================================
# 2. BATCH CONTROLLER (Excel Logic)
# ==========================================
def run_batch_pipeline(excel_path, exchange_suffix='.NS'):
    """
    Reads tickers from Excel and processes them one by one.
    """
    print(f"📂 Reading Excel file: {excel_path}")
    
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"❌ Error reading Excel: {e}")
        return

    # Normalize column names (strip spaces, handle case)
    df.columns = df.columns.str.strip()
    
    if 'Symbol' not in df.columns:
        print("❌ Error: Excel file must have a column named 'Symbol'")
        print(f"   Found columns: {list(df.columns)}")
        return

    # Initialize Scraper classes once
    scraper = NewsScraper()
    parser = NewsParser()
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    all_data_master = [] # To store EVERYTHING in one big file at the end

    # Loop through every row in the Excel
    total_stocks = len(df)
    for index, row in df.iterrows():
        symbol = str(row['Symbol']).strip()
        
        # Skip empty rows
        if not symbol or symbol.lower() == 'nan':
            continue

        # Construct Ticker (e.g., "ABB" -> "ABB.NS")
        # Logic: If user already put ".NS", don't add it again.
        if not symbol.endswith('.NS') and not symbol.endswith('.BO'):
            ticker = f"{symbol}{exchange_suffix}"
        else:
            ticker = symbol

        print(f"--------------------------------------------------")
        print(f"[{index + 1}/{total_stocks}] Starting Pipeline for {ticker}")

        # RUN THE SCRAPER
        try:
            articles = process_ticker(ticker, scraper, parser, output_dir)
            
            # Add ticker name to every article object (useful for the master file)
            for a in articles:
                a['ticker'] = ticker
            
            all_data_master.extend(articles)
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR on {ticker}: {e}")

        # IMPORTANT: Sleep to prevent IP Ban
        # We wait 3 to 7 seconds between stocks
        sleep_time = random.uniform(3, 7)
        print(f"💤 Sleeping for {sleep_time:.1f} seconds to respect Yahoo...")
        time.sleep(sleep_time)

    # Save Master JSON (All stocks in one file)
    master_path = os.path.join(output_dir, "MASTER_ALL_STOCKS.json")
    with open(master_path, 'w', encoding='utf-8') as f:
        json.dump(all_data_master, f, indent=4, ensure_ascii=False)
    
    print("\n==================================================")
    print("🎉 BATCH PROCESSING COMPLETE")
    print(f"📂 Individual files saved in: {output_dir}/")
    print(f"📂 Master consolidated file: {master_path}")
    print("==================================================")

if __name__ == "__main__":
    # --- CONFIGURATION ---
    # 1. Put your Excel filename here (Make sure it's in the project folder)
    INPUT_EXCEL = "stocks_list.xlsx" 
    
    # 2. Choose Exchange: '.NS' (NSE) or '.BO' (BSE)
    EXCHANGE = ".NS"
    
    run_batch_pipeline(INPUT_EXCEL, exchange_suffix=EXCHANGE)