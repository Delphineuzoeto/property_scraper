import schedule
import time
from scraper import run_scraper
from sheets import push_to_sheets
import pandas as pd

def job():
    print("starting schedule scrape ...")
    df = run_scraper()
    df.to_csv("property_data.csv", index=False)
    push_to_sheets(df, "https://docs.google.com/spreadsheets/d/1JNPErA1aUhHZgYiwBoNHTlA2OXEjztq6EnD0I1CdE5E/edit" )
    print("Done, sheet updated")

job()

schedule.every(2).hours.do(job)
print('scheduler running..press  Ctrl+c to stop')
while True:
    schedule.run_pending()
    time.sleep(60)
