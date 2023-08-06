import datetime
import sys
import time
from polygon import RESTClient
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
from math import sqrt
from math import isnan
import matplotlib.pyplot as plt
from numpy import mean
from numpy import std
from math import floor


# We can buy, sell, or do nothing each time we make a decision.
# This class defies a nobject for keeping track of our current investments/profits for each currency pair
class portfolio(object):
    def __init__(self, from_, to):
        # Initialize the 'From' currency amont to 1
        self.amount = 1
        self.curr2 = 0
        self.from_ = from_
        self.to = to
        # We want to keep track of state, to see what our next trade should be
        self.Prev_Action_was_Buy = False

    # This defines a function to buy the 'To' currency. It will always buy the max amount, in whole number
    # increments
    def buy_curr(self, price):
        if self.amount >= 1:
            num_to_buy = floor(self.amount)
            self.amount -= num_to_buy
            self.Prev_Action_was_Buy = True
            self.curr2 += num_to_buy * price
            print(
                "Bought %d worth of the target currency (%s). Our current profits and losses in the original currency (%s) are: %f." % (
                num_to_buy, self.to, self.from_, (self.amount - 1)))
        else:
            print("There was not enough of the original currency (%s) to make another buy." % self.from_)

    # This defines a function to sell the 'To' currency. It will always sell the max amount, in a whole number
    # increments
    def sell_curr(self, price):
        if self.curr2 >= 1:
            num_to_sell = floor(self.curr2)
            self.amount += num_to_sell * (1 / price)
            self.Prev_Action_was_Buy = False
            self.curr2 -= num_to_sell
            print(
                "Sold %d worth of the target currency (%s). Our current profits and losses in the original currency (%s) are: %f." % (
                num_to_sell, self.to, self.from_, (self.amount - 1)))
        else:
            print("There was not enough of the target currency (%s) to make another sell." % self.to)


        # Function slightly modified from polygon sample code to format the date string
def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M:%S')

# Function which clears the raw data tables once we have aggregated the data in a 6 minute interval
def reset_raw_data_tables(engine,currency_pairs):
    with engine.begin() as conn:
        for curr in currency_pairs:
            conn.execute(text("DROP TABLE "+curr[0]+curr[1]+"_raw;"))
            conn.execute(text("CREATE TABLE "+curr[0]+curr[1]+"_raw(ticktime text, fxrate  numeric, inserttime text);"))

# This creates a table for storing the raw, unaggregated price data for each currency pair in the SQLite database
def initialize_raw_data_tables(engine,currency_pairs):
    with engine.begin() as conn:
        for curr in currency_pairs:
            conn.execute(text("CREATE TABLE "+curr[0]+curr[1]+"_raw(ticktime text, fxrate  numeric, inserttime text);"))

# This creates a table for storing the (6 min interval) aggregated price data for each currency pair in the SQLite database
def initialize_aggregated_tables(engine,currency_pairs):
    with engine.begin() as conn:
        for curr in currency_pairs:
            conn.execute(text("CREATE TABLE "+curr[0]+curr[1]+"_agg(max_price numeric, min_price numeric, "
                                                              "vol numeric, mean_price numeric, fd numeric);"))



is_first_six_minute = True
# This function is called every 6 minutes to aggregate the data, store it in the aggregate table,
# and then delete the raw data
def aggregate_raw_data_tables(engine, currency_pairs):
    global is_first_six_minute
    with engine.begin() as conn:
        for curr in currency_pairs:
            # result = conn.execute(text("SELECT AVG(fxrate) as avg_price, COUNT(fxrate) as tot_count FROM " + curr[0] + curr[1] + "_raw;"))
            # result = conn.execute(text("SELECT * FROM " + curr[0] + curr[1] + "_raw;"))
            result = conn.execute(text("SELECT fxrate FROM " + curr[0] + curr[1] + "_raw;"))

            # Step 1: get Max, Min, Max-Min, Mean Value for every 6 minutes
            price_every_6_minutes = [row[0] for row in result]
            if price_every_6_minutes:
                max_price = max(price_every_6_minutes)
                min_price = min(price_every_6_minutes)
                vol = max_price - min_price
                mean_price = sum(price_every_6_minutes) / len(price_every_6_minutes)
            else:
                max_price = min_price = vol = mean_price = 0

            if is_first_six_minute:
                is_first_six_minute = False

            # Step 2:  Keltner Upper Bands
            upper_bands = [mean_price + i * 0.025 * vol for i in range(100)]

            # Step 3: Keltner Lower Bands
            lower_bands = [mean_price - i * 0.025 * vol for i in range(100)]

            # Step 4:
            # count N. How determin "cross" ?
            # If a price "P", stay in between two bands, that means "cross".
            N = 0
            for p in price_every_6_minutes:
                # check upper bands
                for j in range(1, 100):
                    if upper_bands[j-1] <= p <= upper_bands[j]:
                        N += 1
                # check lower bands
                for j in range(1, 100):
                    if lower_bands[j - 1] <= p <= lower_bands[j]:
                        N += 1

            if vol == 0 or is_first_six_minute:
                fd = 0
            else:
                fd = N / vol

            conn.execute(text("INSERT INTO " + curr[0] + curr[1] +
                "_agg (max_price, min_price, vol, mean_price, fd) "
                "VALUES (:max_price, :min_price, :vol, :mean_price, :fd);"),
                 [{"max_price": max_price, "min_price": min_price, "vol": vol, "mean_price":mean_price,
                   "fd": fd}])

# This main function repeatedly calls the polygon api every 1 seconds for 24 hours
# and stores the results.
def main(currency_pairs):
    import os
    os.makedirs("sqlite", exist_ok=True)

    # The api key given by the professor
    key = "beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq"

    # Number of list iterations - each one should last about 1 second
    count = 0
    agg_count = 0

    # Create an engine to connect to the database; setting echo to false should stop it from logging in std.out
    # change db name --> three_pairs.db
    engine = create_engine("sqlite+pysqlite:///sqlite/final.db", echo=False, future=True)

    # Create the needed tables in the database
    initialize_raw_data_tables(engine, currency_pairs)
    initialize_aggregated_tables(engine, currency_pairs)

    # Open a RESTClient for making the api calls
    # change "with RESTClient(key) as client" -->  client = RESTClient(key)
    client = RESTClient(key)
    # with RESTClient(key) as client:
    # Loop that runs until the total duration of the program hits 24 hours.
    while count < 36000:  # 86400 seconds = 24 hours
        # Make a check to see if 6 minutes has been reached or not
        if agg_count == 3600:
            # Aggregate the data and clear the raw data tables
            aggregate_raw_data_tables(engine, currency_pairs)
            reset_raw_data_tables(engine, currency_pairs)
            agg_count = 0

        # Only call the api every 1 second, so wait here for 0.75 seconds, because the
        # code takes about .15 seconds to run
        time.sleep(0.75)

        # Increment the counters
        count += 1
        agg_count += 1
        print(f"Progress: {count} / 36000")

        # Loop through each currency pair
        for currency in currency_pairs:
            # Set the input variables to the API
            from_ = currency[0]
            to = currency[1]

            # Call the API with the required parameters
            try:
                resp = client.get_real_time_currency_conversion(from_, to, amount=100, precision=2)
            except:
                continue

            # This gets the Last Trade object defined in the API Resource
            last_trade = resp.last
            # Format the timestamp from the result
            dt = ts_to_datetime(last_trade.timestamp)

            # Get the current time and format it
            insert_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Calculate the price by taking the average of the bid and ask prices
            avg_price = (last_trade.bid + last_trade.ask) / 2

            # Write the data to the SQLite database, raw data tables
            with engine.begin() as conn:
                conn.execute(text(
                    "INSERT INTO " + from_ + to + "_raw(ticktime, fxrate, inserttime) VALUES (:ticktime, :fxrate, :inserttime)"),
                    [{"ticktime": dt, "fxrate": avg_price, "inserttime": insert_time}])




