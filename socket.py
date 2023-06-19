
import asyncio
import websockets
import json
from datetime import datetime
import psycopg2
from psycopg2 import pool
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from decimal import Decimal, ROUND_HALF_UP

class Socket:
    def __init__(self, market_data):
        self.market_data = market_data

    async def echo(self, websocket, path):
        async for message in websocket:
            # Parse the incoming JSON message
            data = json.loads(message) 
            print(f'Parsed data: {data}')

            # Extract time and prices
            time = data.get('Time') or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            current_prices = data.get('Prices')
            if current_prices is not None:
                self.market_data.insert_current_prices(time, current_prices)

            # Send your data
            await websocket.send(json.dumps(data))

class MarketData:
    def __init__(self):
        print("Initializing MarketData")
        self.previous_prices_updated = False
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.update_previous_prices, IntervalTrigger(hours=24))
        self.scheduler.start()
        self.open_db_pool()

    def open_db_pool(self):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1, 
            maxconn=10, 
            host="192.168.1.220",
            port="54443",
            database="market_data",
            user="john",
            password="deduu"
        )

    def close_db_pool(self):
        psycopg2.pool.SimpleConnectionPool.closeall(self.connection_pool)


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
                     conn.rollback()
                 finally:
                     self.connection_pool.putconn(conn)
                 print("Lost connection to the database. Reconnecting...")
                 self.open_db_pool()
        return wrapper

            
    @retry_db_operation
    def insert_current_prices(self, cur, time, current_prices):
        print("Inserting current prices")
        try:
            # Convert time to a datetime object and then format it into a string that PostgreSQL can understand
            if time is not None:
                time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            else:
                 time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')

            for item, current_price in current_prices.items():
                #print(f"Inserting {item} with current price {current_price}")
                cur.execute("SELECT id FROM items WHERE name = %s", (item,))
                row = cur.fetchone()
                if row is None:
                    print(f"No item found for name '{item}', adding to database.")
                    cur.execute("INSERT INTO items (name) VALUES (%s) RETURNING id", (item,))
                    item_id = cur.fetchone()[0]
                else:
                    item_id = row[0]
 
                # Get the most recent price for the current item
                cur.execute("""
                   SELECT price 
                   FROM price_data 
                   WHERE item_id = %s 
                """, (item_id,))
                previous_price_row = cur.fetchone()
                if previous_price_row is None:
                    daily_change = Decimal('000.000')
                    cur.execute("""
                       INSERT INTO price_data (item_id, time, price, daily_change)
                       VALUES (%s, timestamp %s, %s, %s)
                    """, (item_id, time_str, current_price, daily_change))
                else:
                    previous_price = previous_price_row[0]
                    daily_change = (Decimal(current_price) - previous_price).quantize(Decimal('000.000'))
                    print(f'Daily change for {item}: {daily_change}')  # Print the daily change
                    # Update the current price and daily change
                    cur.execute("""
                       UPDATE price_data
                       SET time = timestamp %s, price = %s, daily_change = %s
                       WHERE item_id = %s
                    """, (time_str, current_price, daily_change, item_id))

            print("Current prices and daily changes updated successfully")
        except psycopg2.Error as e:
            print(f"An error occurred while updating current prices: {e}")

    @retry_db_operation
    def update_previous_prices(self, cur):
        print("Updating previous prices")
        try:
            # Get all items from the items table
            cur.execute("SELECT * FROM items")
            rows = cur.fetchall()
            for row in rows:
                item_id = row[0]
                item_name = row[1]
                # Get the most recent price for the current item
                cur.execute("""
                    SELECT price 
                    FROM price_data 
                    WHERE item_id = %s 
                    ORDER BY time DESC 
                    LIMIT 1
                """, (item_id,))
                previous_price = cur.fetchone()[0]
                # Update the previous_price field where the item_id matches and the time is equal to the current time
                cur.execute("""
                    UPDATE price_data 
                    SET previous_price = %s 
                    WHERE item_id = %s AND time = timestamp %s
                """, (previous_price, item_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
           # conn.commit()
            print("Previous prices updated successfully")
        except psycopg2.Error as e:
            print(f"An error occurred while updating previous prices: {e}")

if __name__ == "__main__":
    try:
        market_data = MarketData()
        socket = Socket(market_data)

        start_server = websockets.serve(socket.echo, '192.168.1.220', 5050)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("Terminating application. Closing database connection pool...")
        market_data.close_db_pool()
