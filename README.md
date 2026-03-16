# 🏠 Nigeria Property Price Tracker

An automated web scraper that collects real estate listing data from PropertyPro.ng across Nigeria. Auto-updates every 2 hours and pushes live data to Google Sheets.

## 📊 What it collects
- Property name & type
- Price
- Location
- Number of bedrooms
- Property URL

## ⚡ How it works
1. `scraper.py` — scrapes PropertyPro.ng listing pages
2. `sheets.py` — pushes clean data to Google Sheets
3. `scheduler.py` — runs automatically every 2 hours

## 🚀 Setup
```bash
python -m venv propvenv
source propvenv/bin/activate
pip install -r requirements.txt
python scheduler.py
```

## 🛠️ Built with
- Python, BeautifulSoup, Requests
- Pandas
- gspread + Google Sheets API
- schedule

## 📍 Data Source
- PropertyPro.ng
