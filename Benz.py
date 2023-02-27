import pandas as pd
import requests
from bs4 import BeautifulSoup


def retrieve_historical_data(symbol, start_date, end_date):
    url = f"https://finance.yahoo.com/quote/{symbol}/history?p={symbol}"

    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError("Failed to retrieve data: {}".format(response.status_code))

    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find_all('table', class_="W(100%) M(0)")

    if len(table) == 0:
        raise ValueError("No tables found on page")

    headers = [th.text for th in table[0].find_all("th")]

    rows = []
    for row in table[0].find_all("tr")[1:]:
        rows.append([td.text for td in row.find_all("td")])

    df = pd.DataFrame(rows, columns=headers)

    # Clean up the data and convert to appropriate data types
    df = df.rename(columns={"Close*": "Close", "Adj Close**": "Adj Close"})
    df["Date"] = pd.to_datetime(df["Date"])
    df["Open"] = pd.to_numeric(df["Open"].str.replace(",", ""))
    df["High"] = pd.to_numeric(df["High"].str.replace(",", ""))
    df["Low"] = pd.to_numeric(df["Low"].str.replace(",", ""))
    df["Close"] = pd.to_numeric(df["Close"].str.replace(",", ""))
    df["Adj Close"] = pd.to_numeric(df["Adj Close"].str.replace(",", ""))
    df["Volume"] = pd.to_numeric(df["Volume"].str.replace(",", ""))

    df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    return df


def save_data_to_csv(df, filename):
    df.to_csv(filename, index=False)

    print(f"Data saved successfully to {filename}")


# Example usage:

if __name__ == "__main__":
    symbol = "MBG.DE"
    start_date = "1996-10-31"
    end_date = "2023-02-20"
    filename = "MBG_DE_historical_prices.csv"

    data = retrieve_historical_data(symbol, start_date, end_date)
    save_data_to_csv(data, filename)
