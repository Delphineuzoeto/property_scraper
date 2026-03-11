import gspread
from  google.oauth2.service_account import Credentials
import pandas as pd


def connect_to_sheets():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    return client

def push_to_sheets(df, sheet_url):
    client = connect_to_sheets()
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)
    df = df.fillna("")

    worksheet.clear()
    worksheet.update([df.columns.tolist()] + df.values.tolist())

    print(f"{len(df)} properties pushed to Google Sheets")


if __name__ == "__main__":
    df = pd.read_csv("property_data.csv")
    push_to_sheets(df, "https://docs.google.com/spreadsheets/d/1JNPErA1aUhHZgYiwBoNHTlA2OXEjztq6EnD0I1CdE5E/edit" )

