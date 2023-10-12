import yfinance as yf
from apscheduler.schedulers.blocking import BlockingScheduler
from pymongo import MongoClient
from datetime import datetime

ticker = "ICICIBANK.NS"

# function to retrieve and store the real-time data
def get_and_store_data():
    # Yahoo Finance Ticker instance
    icici = yf.Ticker(ticker)

    # Getting real-time data for ICICI Bank
    data = icici.history(period="15m")

    # Connect to MongoDB
    client = MongoClient("mongodb://127.0.0.1:27017/stock_data_db")
    db = client["stock_data_db"]

    collection = db[ticker]

    # Storing the data in the database
    collection.insert_one({
        "timestamp": datetime.now(),
        "data": data.to_dict()
    })

    client.close()


# Creating  a scheduler and schedule data retrieval every 15 minutes
scheduler = BlockingScheduler()
scheduler.add_job(get_and_store_data, 'interval', minutes=15,
                  start_date='2023-10-16 11:15:00', end_date='2023-10-20 14:15:00')

# Start the scheduler
scheduler.start()

