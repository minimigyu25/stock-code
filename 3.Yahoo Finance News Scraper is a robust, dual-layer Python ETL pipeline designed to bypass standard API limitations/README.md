# 📰 Yahoo Finance News Scraper & Batch ETL Pipeline

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A professional-grade Python pipeline designed to scrape, clean, and structure financial news for multiple stock tickers at once. Unlike standard API fetchers, this tool implements a **"Deep Scraper"** that visits individual article links to extract the full body text, bypassing the short summary limitations of the Yahoo Finance API. It supports **Batch Processing** via Excel and outputs organized JSON data ready for LLMs, Sentiment Analysis, or Dashboards.

---

## 🚀 Key Features

- ⚡ **Batch Processing**: Reads a list of stocks from an Excel file (`stocks_list.xlsx`) and processes them sequentially
- 🕵️‍♂️ **Deep Scraping**: Automatically visits article URLs to scrape the full content (paragraphs) using BeautifulSoup
- 🧠 **Smart Logic**:
  - Auto-detects exchange suffixes (e.g., adds `.NS` for NSE if missing)
  - Respects server limits with random sleep intervals (Polite Scraping)
  - Cleans "invisible" text artifacts and standardized formatting
- 📊 **Structured Output**:
  - **Individual Backups**: Saves separate JSON files for every ticker
  - **Master File**: Aggregates all news into one list
  - **Grouped Output**: Pivots data by ticker (Symbol → [Articles]) for easy consumption

---

## 📂 Project Structure

```
yahoo-finance-news-scraper/
│
├── src/                     # Source Code
│   ├── __init__.py          # Package initializer
│   ├── pipeline.py          # Main Batch Orchestrator (Runs the scraping loop)
│   ├── scraper.py           # Core logic: Fetches API data & Deep scrapes HTML
│   ├── parser.py            # Data Cleaning & Normalization logic
│   └── convert_format.py    # Post-processing: Groups Master data by Ticker
│
├── output/                  # Raw and Master JSON files are saved here
│   ├── MASTER_ALL_STOCKS.json
│   └── [Ticker]_news.json
│
├── FINAL_GROUPED_DATA.json  # The final clean output (Grouped by Ticker)
├── stocks_list.xlsx         # Input Excel file with list of stocks
├── requirements.txt         # Project dependencies
├── .gitignore               # Git configuration to ignore large data files
└── README.md                # Project Documentation
```

---

## 🛠️ Installation

### 1. Prerequisites

- **Python 3.8+**
- **pip** (Python Package Manager)

### 2. Set up Environment

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/yahoo-finance-news-scraper.git
cd yahoo-finance-news-scraper

# Create Virtual Environment (Recommended)
python -m venv venv

# Activate Virtual Environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🏃‍♂️ Usage Guide

### Step 1: Prepare the Input File

Update the `stocks_list.xlsx` file in the root folder. It must contain a column named **Symbol**.

**Example `stocks_list.xlsx` format:**

| Symbol      | Company Name              | Industry      |
|-------------|---------------------------|---------------|
| ABB         | ABB India Ltd.            | Capital Goods |
| TATATECH    | Tata Technologies         | Technology    |
| ADANISOL    | Adani Energy Solutions    | Power         |

> **Note**: The script automatically handles `.NS` suffixes if configured in `pipeline.py`

### Step 2: Run the Batch Scraper

This command will read the Excel file, scrape news for every stock, and save individual/master backups to the `output/` folder.

```bash
python -m src.pipeline
```

- It will wait **3-7 seconds** between stocks to avoid IP bans
- Check the terminal for progress logs

### Step 3: Generate Final Grouped Data

Once the scraper finishes, run this script to restructure the data into the final `FINAL_GROUPED_DATA.json` format.

```bash
python -m src.convert_format
```

---

## 📄 Data Output Format

The final output (`FINAL_GROUPED_DATA.json`) is a dictionary where keys are tickers and values are lists of full-text articles.

```json
{
    "ABB.NS": [
        {
            "headline": "ABB India Ltd Q3 Earnings Call...",
            "description": "Full text of the article goes here... (cleaned and formatted)",
            "date_published": "2025-11-12 01:04:10",
            "source": "GuruFocus.com",
            "url": "https://finance.yahoo.com/news/..."
        },
        {
            "headline": "Another News Article...",
            "description": "Summary...",
            "date_published": "2025-11-10 12:00:00",
            "source": "Reuters",
            "url": "..."
        }
    ],
    "TATATECH.NS": [
        {
            "headline": "Tata Tech shares rise...",
            "description": "Full article text...",
            "date_published": "2026-01-16 14:30:00",
            "source": "Reuters",
            "url": "..."
        }
    ]
}
```

---

## 🏗️ Technologies Used

| Library        | Purpose                                                      |
|----------------|--------------------------------------------------------------|
| yfinance       | Fetching real-time news metadata and timestamps              |
| BeautifulSoup4 | "Deep scraping" full text from individual article HTML pages |
| pandas & openpyxl | Reading the Excel input file and managing data frames     |
| requests       | Handling HTTP requests with custom User-Agents               |
| json           | Standardizing data storage                                   |

---

## 🔧 Configuration

You can customize the scraper behavior by modifying the following parameters in `src/pipeline.py`:

- **Sleep intervals**: Adjust the random delay between requests
- **Exchange suffix**: Configure automatic suffix addition (e.g., `.NS`, `.BO`)
- **Output paths**: Change where JSON files are saved

---

## 📊 Use Cases

This pipeline is ideal for:

- 📈 **Financial Analysis**: Build sentiment analysis models on stock news
- 🤖 **LLM Training**: Create datasets for financial chatbots
- 📉 **Market Research**: Track news trends across multiple tickers
- 📱 **Dashboard Integration**: Feed cleaned data into visualization tools
- 🧪 **Academic Research**: Analyze media coverage patterns

---

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**.

- **Respect robots.txt**: Ensure you are compliant with the target website's scraping policies
- **Rate Limiting**: The script includes intentional delays. Removing them may result in your IP being blocked
- **Copyright**: Content scraped belongs to the respective publishers (Reuters, Bloomberg, Yahoo, etc.). Do not republish without permission
- **No Warranty**: This software is provided "as is" without warranty of any kind

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

## 🙏 Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for providing the Yahoo Finance API wrapper
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing capabilities
- The open-source community for continuous inspiration

---

**⭐ If you find this project useful, please consider giving it a star!**
