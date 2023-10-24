
import psycopg2
import psycopg2.extras
import json
import logging
import sys
import subprocess
from datetime import datetime
import psutil
import time 
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import traceback
import asyncio
import websockets
import socket 
from decimal import Decimal, InvalidOperation
import threading
import aioconsole
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

COLOR = "\033[1;32m"
RESET_COLOR = "\033[00m"

def check_and_kill_port(port):
    """Check if the given port is in use and, if so, kill the process using it"""
    for proc in psutil.process_iter(['pid', 'name']):
        for conn in proc.connections(kind='inet'):
            if conn.laddr.port == port:
                proc.kill()
                return


class DatabaseOperations:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=ip_address,
            port="5432",
            database="forex_data",
            user="john",
            password=""
        )



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
        try:
            return Decimal(number_str)
        except InvalidOperation:
            print(f"Could not convert '{number_str}' to decimal")
            return None



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
            if output_decimal_part == '':# or output_decimal_part == '-':
                return '0'
            # log the inputs and output
           # print(f"current_price: {current_price}, previous_price: {previous_price}, output: {output_decimal_part}")
            return output_decimal_part
        except Exception as e:
            print(f"An error occurred while calculating the difference: {e}")
            return '0'


    def create_tables(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS daily(
            id SERIAL PRIMARY KEY, 
            date TIMESTAMP NOT NULL,
            open NUMERIC,
            high NUMERIC,
            low NUMERIC,
            close NUMERIC,
            ticker CHAR(6) NOT NULL,
            prevclose NUMERIC, 
            candle CHAR(7), 
            body NUMERIC,
            upwiq NUMERIC, 
            downwiq NUMERIC,
            start_pt BOOLEAN DEFAULT FALSE,
            rsi NUMERIC, 
            macd NUMERIC, 
            macd_signal NUMERIC, 
            moving_average NUMERIC, 
            bollinger_bottom NUMERIC, 
            bollinger_top NUMERIC, 
            atr NUMERIC, 
            volume NUMERIC, 
            historical_volatility NUMERIC,
            pricechange NUMERIC, 
            percentchange NUMERIC,
            UNIQUE(ticker, date)
        );
        """
        try:
            cur = self.connection.cursor()
            print("Attempting to create table...")
            cur.execute(create_table_sql)
            print("Table created successfully.")

            print("Hypertable created successfully.")
            self.connection.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error encountered while creating table: ", error)


    def create_sequence_table(self):
        cur = self.connection.cursor()
        cur.execute("""
           CREATE TABLE IF NOT EXISTS daily_bull(
                sequence_id int, 
                id SERIAL PRIMARY KEY, 
                date TIMESTAMP NOT NULL,
                open NUMERIC,
                high NUMERIC,
                low NUMERIC,
                close NUMERIC,
                ticker CHAR(6) NOT NULL,
                prevclose NUMERIC, 
                candle CHAR(7), 
                body NUMERIC,
                upwiq NUMERIC, 
                downwiq NUMERIC,
                start_pt BOOLEAN DEFAULT FALSE,
                rsi NUMERIC, 
                macd NUMERIC, 
                macd_signal NUMERIC, 
                moving_average NUMERIC, 
                bollinger_bottom NUMERIC, 
                bollinger_top NUMERIC, 
                atr NUMERIC, 
                volume NUMERIC, 
                historical_volatility NUMERIC,
                pricechange NUMERIC,
                percentchange NUMERIC,
                UNIQUE(ticker, date)
            )
        """)
        self.connection.commit()
        cur.close()


    def delete_rows_from_sequence(self, ids):
        cur = self.connection.cursor()
        cur.execute(f"""
            DELETE FROM fiftheen_sequences
            WHERE id IN %s
        """, (tuple(ids),))
        self.connection.commit()
        cur.close()


    def copy_rows_to_sequence(self, ids, pattern_desc): 
        cur = self.connection.cursor()
        cur.execute("SELECT nextval('fiftheen_sequences_sequence_id_seq')")
        next_id = cur.fetchone()[0]
        cur.execute(f"""
            INSERT INTO minute_sequences (sequence_id, id, date, open, high, low, close, ticker, prevclose, candle, body, upwiq, downwiq, start_pt, tag)
            SELECT {next_id}, id, date, open, high, low, close, ticker, prevclose, candle, body, upwiq, downwiq, start_pt, %s
            FROM minute
            WHERE id IN %s
        """, (pattern_desc, tuple(ids),))
        self.connection.commit()
        cur.close()


    def insert_ohlc_data(self, time, ticker, open, high, low, close, upwiq, downwiq, body, prevclose, macd_signal, rsi, moving_average, bollinger_top, bollinger_bottom, atr, volume, historical_volatility, pricechange, percentchange):
        time = datetime.strptime(time, "%Y-%m-%d %H:%M")

        if close < prevclose:  # Bearish Candle 
            upwiq = self.calculate_diff(high, open)  
            downwiq = self.calculate_diff(close, low)  
            body = self.calculate_diff(open, close)  
            candle = 'bearish' 
        if close > prevclose:  # Bullish Candle
            upwiq = self.calculate_diff(high, close)  
            downwiq = self.calculate_diff(open, low)  
            body = self.calculate_diff(close, open)  
            candle = 'bullish'
            print(f'upwiq: {upwiq}, downwiq: {downwiq}, body: {body}, candle: {candle}')


        sql = """
            INSERT INTO daily(date, open, high, low, close, ticker, body, upwiq, downwiq, prevclose, macd_signal, rsi, moving_average, bollinger_top, bollinger_bottom, atr, volume, historical_volatility, candle, pricechange, percentchange)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (ticker, date) DO NOTHING;
        """
        try:
            cur = self.connection.cursor()
            # Modify the tuple to account for the new values
            cur.execute(sql, (time, open, high, low, close, ticker, body, upwiq, downwiq, prevclose, macd_signal, rsi, moving_average, bollinger_top, bollinger_bottom, atr, volume, historical_volatility, candle, pricechange, percentchange))
            self.connection.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()  # Rollback the transaction after an exception
            print(error)


    def process_prices(self, time, price_dict):
        processed_items = []
        for item, price_data in price_dict.items():
            formatted_open = self.format_six_digits(price_data['open'])
            formatted_high = self.format_six_digits(price_data['high'])
            formatted_low = self.format_six_digits(price_data['low'])
            formatted_close = self.format_six_digits(price_data['close'])
            formatted_prevclose = self.format_six_digits(price_data['prevclose'])
            
            if None in (formatted_open, formatted_high, formatted_low, formatted_close, formatted_prevclose):
                print(f"Skipping item '{item}' due to incorrect price format")
                continue
                
            processed_items.append((item, formatted_open, formatted_high, formatted_low, formatted_close, formatted_prevclose))
            
        print(f"Processed items '{processed_items}'")
        return time, processed_items


class Socket:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.retry_wait = 1
        self.last_received_time = time.time()  
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.start_email_warning_job()
        self.email_warnings_count = 0



    def start_email_warning_job(self):
        self.scheduler.add_job(self.check_and_send_warning_email, 'interval', minutes=1)  # Runs every 1 minute

    def check_and_send_warning_email(self):
            elapsed_time = time.time() - self.last_received_time  
            if elapsed_time >= 905:  
                if self.email_warnings_count < 2:  
                    self.send_email_warning()
                    self.email_warnings_count += 1  
                else:
                    self.scheduler.shutdown()  # Shutdown the scheduler when 2 email warnings are sent
                    print("Exiting due to no data received in last 30 minutes.")
                    sys.exit(0)  # Exit the entire application after sending two email warnings

    async def echo(self, websocket, path):
       ticker = None
       async for message in websocket:
           self.last_received_time = time.time()  # Update the time when a message is received.
           try:
               # Process the received message here.
               data_list = json.loads(message)

               for data in data_list:
                   ticker = data.get('Currency')
                   price_dict = {
                        'open': data.get('Open'),
                        'high': data.get('High'),
                        'low': data.get('Low'),
                        'close': data.get('Close'),
                        'prevclose': data.get('PrevClose'),
                        'rsi': data.get('RSI'),
                        'macd_signal': data.get('MACDSignal'),
                        'moving_average': data.get('MovingAverage'),
                        'bollinger_top': data.get('BollingerTop'),
                        'bollinger_bottom': data.get('BollingerBottom'),
                        'atr': data.get('ATR'),
                        'volume': data.get('Volume'),
                        'pricechange': data.get('PriceChange'),
                        'percentchange': data.get('PercentageChange'),
                        'historical_volatility': data.get('HistoricalVolatility'),
                   }

                   missing_keys = [key for key, value in price_dict.items() if value is None]

                   if missing_keys:
                       missing_keys_str = ', '.join(missing_keys)
                       print(f"Received incomplete data for ticker {data.get('Currency')}. Missing keys: {missing_keys_str}. Skipping...")
                       continue  # This will skip the current iteration and move on to the next data set


                   timestamp, processed_prices = self.db_manager.process_prices(time=data['time'], price_dict={ticker: price_dict})

                   for item, formatted_open, formatted_high, formatted_low, formatted_close, formatted_prevclose in processed_prices:
                    self.db_manager.insert_ohlc_data(
                        time = timestamp,
                        ticker = item,
                        open = formatted_open,
                        high = formatted_high,
                        low = formatted_low,
                        close = formatted_close,
                        upwiq = None, 
                        downwiq = None, 
                        body = None,
                        prevclose = formatted_prevclose,
                        macd_signal = price_dict['macd_signal'],
                        rsi = price_dict['rsi'],
                        moving_average = price_dict['moving_average'],
                        bollinger_top = price_dict['bollinger_top'],
                        bollinger_bottom = price_dict['bollinger_bottom'],
                        atr = price_dict['atr'],
                        volume = price_dict['volume'],
                        historical_volatility = price_dict['historical_volatility'],
                        pricechange = price_dict['pricechange'],
                        percentchange = price_dict['percentchange']
                    )
                    await websocket.send(json.dumps(data))
           except Exception as e:
               logging.error('Unexpected error in echo: %s', str(e))

    async def handle_reconnect(self, websocket, path, error):
        print(f"WebSocket connection lost due to {error}. Retrying in {self.retry_wait} seconds.")
        await asyncio.sleep(self.retry_wait)  # Wait for the specified amount of time
        self.retry_wait *= 2  # Exponential backoff
        try:
            await self.echo(websocket, path)  # Attempt to reconnect
            self.retry_wait = 1  # If the reconnection is successful, reset the waiting time
        except Exception as e:
            print(f"Reconnection failed due to {e}.")


    def send_email_warning(self):
        print("send_email_warning called")  
        sender = 'sender'
        receivers = ['reciver']
        subject = 'Warning: Data Not Received'
        body = 'No data has been received in the last 15 minutes!'
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(receivers)
        
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender, 'apppassword')
            server.sendmail(sender, receivers, msg.as_string())
            server.quit()
            print('Successfully sent email')
        except Exception as e:  # catch all exceptions
            print(f'Error: Unable to send email. Error message: {str(e)}')

class DatabaseOperationsOnDemand:
    def __init__(self, db_manager):
        self.db_manager = db_manager



    async def perform_operation(self):
        while True:
            try:
                user_input = await aioconsole.ainput("Press 'p' to perform operation, 'q' to quit: d to delete")
                if user_input.lower() == 'q':
                    break

                if user_input.lower() == 'p':
                    ids_input = await aioconsole.ainput("Enter the ids separated by comma: ")
                    ids = list(map(int, ids_input.split(",")))
                    pattern_desc = await aioconsole.ainput("Enter the pattern description: ")
                    self.db_manager.copy_rows_to_sequence(ids, pattern_desc)

                if user_input.lower() == 'd':
                    ids_input = await aioconsole.ainput("Enter the ids to delete separated by comma: ")
                    ids = list(map(int, ids_input.split(",")))
                    self.db_manager.delete_rows_from_sequence(ids)

            except Exception as e:
                logging.error('Error in perform_operation: %s', str(e))
                logging.error(traceback.format_exc())




async def main():
    db_manager = None
    try:
        global ip_address
        hostname = socket.gethostname()  
        ip_address = socket.gethostbyname(hostname)

        db_manager = DatabaseOperations()
        db_manager.create_tables()
        db_manager.create_sequence_table()
        db_operations_on_demand = DatabaseOperationsOnDemand(db_manager)
        operations_task = asyncio.create_task(db_operations_on_demand.perform_operation())
        port=6007
        check_and_kill_port(int(port))
        time.sleep(4)
        socket_instance = Socket(db_manager)  # Here 'socket_instance' is the instance of your Socket class
        start_server = websockets.serve(socket_instance.echo, ip_address, port, ping_interval=None)
        await asyncio.gather(start_server, operations_task)
    except KeyboardInterrupt:
        print("Terminating application.")
    finally:
        print("Closing database connection pool...")
        if db_manager is not None:
            db_manager.connection.close()
        print("Database connection closed.")

if __name__ == '__main__':
    asyncio.run(main())






