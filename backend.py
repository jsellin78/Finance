
import asyncio
import websockets
import json
from datetime import datetime
import psycopg2
from psycopg2 import pool
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from decimal import Decimal, InvalidOperation
import traceback


class DatabaseOperations:
    def __init__(self):
        self.open_db_pool()
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                self.create_items_table_if_not_exists(cur)
                conn.commit()  
        finally:
            self.connection_pool.putconn(conn)
        self.scheduler = BackgroundScheduler()
        self.start_scheduler()  
        self.scheduler.start()

    def retry_db_operation(func):
        def wrapper(self, *args, **kwargs):
            while True:
                conn = self.connection_pool.getconn()
                try:
                    with conn.cursor() as cur:
                        result = func(self, cur, *args, **kwargs)
                        conn.commit()
                        return result
                except Exception as e:
                    print(f"An error occurred: {e}")
                    traceback.print_exc()
                    conn.rollback()
                finally:
                    self.connection_pool.putconn(conn)
                print("Lost connection to the database. Reconnecting...")
                self.open_db_pool()
        return wrapper

    def open_db_pool(self):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1, 
            maxconn=10, 
            host="192.168.1.220",
            port="5432",
            database="market_data",
            user="john",
            password="deduu"
        )
        print("Database connection pool opened successfully.")



    @retry_db_operation
    def get_all_items(self, cur):
        cur.execute("SELECT currency_name FROM items")
        return [row[0] for row in cur.fetchall()]

    def start_scheduler(self):
        items = self.get_all_items()
        for item in items:
            self.scheduler.add_job(
                self.update_previous_price, 
                CronTrigger(hour=8, minute=33), 
                args=[item]
            )
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                self.create_items_table_if_not_exists(cur)
                conn.commit()  
        finally:
            self.connection_pool.putconn(conn)


    def create_items_table_if_not_exists(self, cur):
        print("Creating table 'items' if not exists...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS items (
                currency_name CHAR(6) PRIMARY KEY,
                current_price NUMERIC,
                previous_price NUMERIC,
                date TIMESTAMP NOT NULL,  
                daily_change decimal(6)
            );
        """)
        print("Table 'items' created successfully.")


    def close_db_pool(self):
        psycopg2.pool.SimpleConnectionPool.closeall(self.connection_pool)




    def calculate_diff(self, current_price, previous_price):
        # extract the decimal places from the input argument
        if current_price is None or previous_price is None or current_price == '' or previous_price == '':
            return '0'
        try: 
            current_price = str(current_price)
            previous_price = str(previous_price)
            decimal_places1 = len(current_price.split(".")[1]) if "." in current_price else 0 
            decimal_places2 = len(previous_price.split(".")[1]) if "." in previous_price else 0
            # take the maximum decimal places for calculating difference
            max_decimal_places = max(decimal_places1, decimal_places2)
            # get the decimal part difference
            decimal_part_diff = round(float(current_price) - float(previous_price), max_decimal_places)
            # format the decimal_part_diff to the required decimal places
            output = "{:.{dp}f}".format(decimal_part_diff, dp=max_decimal_places)
            # check if output is negative
            is_negative = output.startswith("-")
            # extract the decimal part after the dot
            output_decimal_part = output.split('.')[1]
            # remove leading zeros
            output_decimal_part = output_decimal_part.lstrip('0')
            # apply the sign to the output if necessary
            output_decimal_part = "-" + output_decimal_part if is_negative else output_decimal_part
            # if the output is empty or "-", return '0'
            if output_decimal_part == '' or output_decimal_part == '-':
                return '0'
            # log the inputs and output
            print(f"current_price: {current_price}, previous_price: {previous_price}, output: {output_decimal_part}")
            # return the output
            return output_decimal_part
        except Exception as e:
            print(f"An error occurred while calculating the difference: {e}")
            return '0'


    # example usage:
    #print(calculate_diff("0.85150", "0.85200"))



    def update_daily_change(self, cur, item):
        cur.execute("""
        SELECT current_price, previous_price
        FROM items
        WHERE currency_name = %s
        """, (item,))
        row = cur.fetchone()
        if row is not None:
            current_price, previous_price = row
            # skip the calculation if either price is None
            if current_price is None or previous_price is None:
                print(f"Skipping daily change calculation for item '{item}' due to missing price data")
                return
            daily_change = self.calculate_diff(current_price, previous_price)
            cur.execute("""
            UPDATE items
            SET daily_change = %s
            WHERE currency_name = %s
            """, (daily_change, item))
        else:
            print(f"No price data found for item '{item}'")



    def format_six_digits(self, number): #Format the price of the specific currency 
        number_str = str(number)
        if '.' not in number_str:
            number_str += '.'
        while len(number_str) < 7:
            number_str += '0'
        if len(number_str) > 7:
            if '.' in number_str[:7]:
                number_str = number_str[:7]
            else:
                number_str = number_str[:6] + '.' + number_str[6:]
        return Decimal(number_str)


    @retry_db_operation
    def check_and_update_items(self, cur, item):
        cur.execute("SELECT id FROM items WHERE name = %s", (item,))
        row = cur.fetchone()
        if row is None:
            print(f"No item found for name '{item}', adding to database.")
            cur.execute("INSERT INTO items (name) VALUES (%s) RETURNING id", (item,))
            item_id = cur.fetchone()[0]
            print(f"Inserted into items: name={item}, id={item_id}")
        else:
            item_id = row[0]
        return item_id


    def get_current_price(self, cur, item):
        cur.execute("SELECT current_price FROM items WHERE currency_name = %s", (item,))
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            print(f"No current price found for item '{item}'")
            return None

    def update_previous_price(self, item):
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                current_price = self.get_current_price(cur, item)
                if current_price is not None:
                    cur.execute("""
                        UPDATE items
                        SET previous_price = %s
                        WHERE currency_name = %s
                        """, (current_price, item))
                conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            self.connection_pool.putconn(conn)

    @retry_db_operation
    def get_previous_price_and_daily_change(self, cur, item_name):
        cur.execute("""
        SELECT previous_price, daily_change 
        FROM items 
        WHERE currency_name = %s
        """, (item_name,))
        price_data_row = cur.fetchone()
        previous_price = self.format_six_digits(price_data_row[0])
        daily_change = price_data_row[1]
        return previous_price, daily_change


    def insert_new_price(self, cur, item, formatted_price, time):
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S') # parse the string into a datetime object
        formatted_time = time.strftime('%Y-%m-%d %H:%M') 
        cur.execute("""
            INSERT INTO items (currency_name, current_price, date) 
            VALUES (%s, %s, %s)
            ON CONFLICT (currency_name) 
            DO UPDATE SET current_price = EXCLUDED.current_price
        """, (item, formatted_price, formatted_time))



    def process_prices(self, cur, time, price_dict): #This code formats the incoming digits from the websocket to six.   
        processed_items = []
        for item, price in price_dict.items():
            formatted_price = self.format_six_digits(price)
            if formatted_price is None:
                print(f"Skipping item '{item}' due to incorrect price format")
                continue
            processed_items.append((item, formatted_price)) #item should be the currency name and current_price is the value of the currency   

        print(f"Processed items '{processed_items}'")
        return time, processed_items

    @retry_db_operation
    def insert_current_price(self, cur, time, current_price):
        print("Starting to insert current prices...")
        try:
            time, processed_items = self.process_prices(cur, time, current_price)
            for item, formatted_price in processed_items:
                self.insert_new_price(cur, item, formatted_price, time)
                self.update_daily_change(cur, item)
            print("Finished inserting current prices.")
        except psycopg2.Error as e:
            print(f"An error occurred while updating current prices: {e}")

class Socket:
    def __init__(self, db_manager, market_data):
        self.market_data = market_data
        self.db_manager = db_manager

    async def echo(self, websocket, path):
        async for message in websocket:
            # Parse the incoming JSON message
            data = json.loads(message) 
            #print(f'Parsed data: {data}')

            # Extract time and prices
            time = data.get('Time') or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            current_price = data.get('Prices')
            if current_price is not None:
                self.db_manager.insert_current_price(time, current_price)

            await websocket.send(json.dumps(data))


class MarketData:
    def __init__(self, db_manager):
        print("Initializing MarketData")
        self.previous_prices_updated = False
        self.start_of_day_prices = {} 
        self.db_manager = db_manager

    def close_db_pool(self):
        self.db_manager.close_db_pool()


if __name__ == "__main__":
    try:
        db_manager = DatabaseOperations()
        market_data = MarketData(db_manager)  
        socket = Socket(db_manager, market_data)
        start_server = websockets.serve(socket.echo, '192.168.1.220', 5089)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("Terminating application. Closing database connection pool...")
        market_data.close_db_pool()
