import json
import os
from collections import defaultdict

def restructure_json():
    # 1. Path to your existing Master File (from the previous step)
    input_path = 'output/MASTER_ALL_STOCKS.json'
    output_path = 'FINAL_GROUPED_DATA.json'
    
    # Check if file exists
    if not os.path.exists(input_path):
        print(f"❌ Error: Could not find {input_path}")
        print("   Did you run the batch scraper pipeline first?")
        return

    print(f"📂 Reading raw data from: {input_path}...")
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading JSON: {e}")
        return

    # 2. Grouping Logic
    # We use a dictionary where Key = Ticker, Value = List of Articles
    grouped_data = defaultdict(list)
    
    print(f"🔄 Processing {len(raw_data)} articles...")

    for article in raw_data:
        # Get the ticker (e.g. "ABB.NS")
        ticker = article.get('ticker', 'UNKNOWN_TICKER')
        
        # Create a clean copy of the article WITHOUT the 'ticker' field inside
        # (Since the ticker is now the parent key, we don't need to repeat it)
        clean_article = {
            k: v for k, v in article.items() if k != 'ticker'
        }
        
        # Append to the correct list
        grouped_data[ticker].append(clean_article)

    # 3. Save the new format
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(grouped_data, f, indent=4, ensure_ascii=False)

    print("--------------------------------------------------")
    print(f"✅ CONVERSION COMPLETE!")
    print(f"📊 Organized {len(raw_data)} articles into {len(grouped_data)} stocks.")
    print(f"📂 New file saved at: {output_path}")
    print("--------------------------------------------------")

if __name__ == "__main__":
    restructure_json()