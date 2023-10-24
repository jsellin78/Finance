import psycopg2
import pandas as pd
import numpy as np
import tensorflow as tf
import sqlalchemy
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import keyboard 
from tensorflow_addons.metrics import F1Score
import os
import json
import time 
from io import BytesIO
from db_manager import DbManager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import warnings
import pytz
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
warnings.simplefilter("ignore", UserWarning)

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  

def create_f1score(**kwargs):
    num_classes = 1 
    return F1Score(num_classes=num_classes)

class DatabaseManager:
    SKIP_FILE = 'skip_patterns.json'

    def __init__(self, db_conn=None):
        self.db_conn = DbManager()
        self.engine = sqlalchemy.create_engine(
            "postgresql://john:john93@192.168.1.186:5432/forex_data"
        )

        self.db_conn.fiftheen_seq_we_want()
        self.db_conn.create_pattern_we_dont_want_fiftheen() 

    @staticmethod
    def load_skip_patterns():
        try:
            with open(DatabaseManager.SKIP_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_skip_patterns(patterns):
        with open(DatabaseManager.SKIP_FILE, 'w') as f:
            json.dump(patterns, f)


    def matches_conditions(self, row):
        # Check each condition separately
        conditions = [
            (36 <= row['upwiq'] <= 41) and (36 <= row['downwiq'] <= 41) and (10 <= row['body'] <= 12),
            (30 <= row['upwiq'] <= 32) and (30 <= row['downwiq'] <= 32) and (58 <= row['body'] <= 65),
            (47 <= row['upwiq'] <= 58) and (47 <= row['downwiq'] <= 58) and (17 <= row['body'] <= 22),
            (56 <= row['upwiq'] <= 58) and (56 <= row['downwiq'] <= 58) and (47 <= row['body'] <= 50),
            (37 <= row['upwiq'] <= 41) and (37 <= row['downwiq'] <= 41) and (17 <= row['body'] <= 20)
        ]
        return any(conditions)


    def predict_and_sort(self):
        skip_patterns = self.load_skip_patterns()
        processed_patterns = set() 

        all_predictions = []

        i = 0
        latest_records = self.db_conn.load_latest_records()
        for ticker, group in latest_records.groupby('ticker'):
            if len(group) < 3:
                continue

            group_features = group[['body', 'upwiq', 'downwiq', 'candle']].values

            sequences = self.db_conn.create_seq_for_match(group_features, 3)


            for idx, _ in enumerate(sequences):
                corresponding_date = group.iloc[-1]['date']  # Date should be that of the last record in the group
                all_predictions.append((ticker, corresponding_date, i))
                i += 1

        all_predictions.sort(key=lambda x: x[1], reverse=False)

        for prediction in all_predictions:
            print(f"Processing prediction: {prediction}")
            ticker, date, _ = prediction
            start_date = date - pd.Timedelta(days=2)  # Subtract 2 because the date is now that of the last record in the sequence
            end_date = date
            prices = self.db_conn.fetch_candlestick_data(ticker, start_date, end_date)

            # Calculate the body of the last candlestick
            latest_three_records = latest_records[latest_records['ticker'] == ticker].tail(3)
            print(f"Unique tickers being processed: {latest_three_records['ticker'].unique()}")

            current_pattern = []  # Initialize the current_pattern list here
            candle_values = []

            for idx, (index, record) in enumerate(latest_three_records.iterrows()):
                values = {
                    key: record[key] for key in [
                        'upwiq', 'downwiq', 'body', 'candle', 'open', 'high', 'low', 'close', 
                        'prevclose', 'rsi', 'macd_signal', 'moving_average', 'bollinger_top', 
                        'bollinger_bottom', 'atr', 'volume', 'historical_volatility', 
                        'pricechange', 'percentchange'
                    ]
                }
                if record['candle'] == 'bullish':
                    values['candle'] = 'bullish'
                elif record['candle'] == 'bearish':
                    values['candle'] = 'bearish'
                else:
                    values['candle'] = 'unknown' 


                candle_values.append(values['candle'])
                current_pattern.append(values)

            # Convert current pattern to string
            current_pattern_str = json.dumps(current_pattern, sort_keys=True)
            processed_patterns.add(current_pattern_str)
            if current_pattern_str in skip_patterns:
                continue  # Skip this pattern

            filename = f"{ticker}_{date.strftime('%Y%m%d')}_candlestick.png"
            img_streams = self.db_conn.plot_candlestick_chart([prices], filename, current_pattern)
            latest_record = latest_three_records.iloc[-1]

            good_patterns = self.db_conn.fetch_predicted_values()

            good_patterns = good_patterns.sort_values(by='sequence_id')

            thresholds = {
                'upwiq': 3,
                'downwiq': 3,
                'body': 3,
            }

            sequence_id = self.db_conn.get_next_sequence_id()
             
            # Ensure latest_three_records has exactly 3 records
            if len(latest_three_records) != 3:
                raise ValueError("The latest_three_records should have exactly 3 rows.")

            for pattern_start_idx in range(0, len(good_patterns), 3):
                matched_rows = []
                # Get three-row pattern from good_patterns
                three_row_pattern = good_patterns.iloc[pattern_start_idx:pattern_start_idx + 3]
    
                # If there are not enough rows to form a three-row pattern, break
                if len(three_row_pattern) != 3 or len(three_row_pattern['sequence_id'].unique()) != 1:
                    continue

                matches = []
                    
                # Compare the three_row_pattern with the records in the good patterns order by sequence_id 
                for i in range(3):  # Since each pattern has 3 rows
                    good_pt = three_row_pattern.iloc[i]
                    latest_record_row = latest_three_records.iloc[i]
                    matched_attributes = []  

                    if self.db_conn.within_threshold(latest_record_row['upwiq'], good_pt['upwiq'], thresholds['upwiq']):
                        matched_attributes.append('upwiq')

                    if (self.db_conn.within_threshold(latest_record_row['downwiq'], good_pt['downwiq'], thresholds['downwiq']) or 
                       latest_record_row['downwiq'] > thresholds['downwiq_absolute']):
                       matched_attributes.append('downwiq')

                    if self.db_conn.within_threshold(latest_record_row['body'], good_pt['body'], thresholds['body']):
                        matched_attributes.append('body')

                    #  ])
                    if len(matched_attributes) == 3:
                            matched_rows.append({
                                'row': i + 1,
                                'sequence_id': three_row_pattern['sequence_id'].iloc[0],
                                'ticker': latest_record_row['ticker'],
                                'date': latest_record_row['date'],
                                'upwiq': latest_record_row['upwiq'],
                                'downwiq': latest_record_row['downwiq'],
                                'body': latest_record_row['body']
                            })


                    # if two rows of the pattern matched, print them out
                    if len(matched_rows) == 2:
                        for matched_row in matched_rows:
                            current_time = datetime.now().strftime('%Y %B %d %H %M %S')
                            print(f"Email sent at {current_time}")
                            print(f"row {matched_row['row']} for sequence_id {matched_row['sequence_id']} and ticker {matched_row['ticker']}: two values matched.")
                            print(f"matched values: date: {matched_row['date']}, upwiq: {matched_row['upwiq']}, downwiq: {matched_row['downwiq']}, body: {matched_row['body']}")

                    # if three rows of the pattern matched, send an email
                    if len(matched_rows) == 3:
                        for matched_row in matched_rows:
                            current_time = datetime.now().strftime('%Y %B %d %H %M %S')
                            print(f"Email sent at {current_time}")
                            self.send_email_warning(matched_row['ticker'], matched_row['date'], matched_row['sequence_id'])
                            print(f"row {matched_row['row']} for sequence_id {matched_row['sequence_id']} and ticker {matched_row['ticker']}: all values matched.")
                            print(f"matched values: date: {matched_row['date']}, upwiq: {matched_row['upwiq']}, downwiq: {matched_row['downwiq']}, body: {matched_row['body']}")



                    if self.matches_conditions(latest_record_row):
                            print(f"Conditions matched for Row {i + 1}: upwiq: {latest_record_row['upwiq']}, downwiq: {latest_record_row['downwiq']}, body: {latest_record_row['body']}")

                         matches.append(True)
                    else:        
                         matches.append(False)

                     for idx, (_, record) in enumerate(latest_three_records.iterrows()):
                         for img_stream in img_streams:
                             self.db_conn.store_image_in_db(
                                 sequence_id, ticker, candle_values[idx], record['upwiq'], record['downwiq'], 
                                 record['body'], record['date'], record['open'], record['high'], record['low'], 
                                 record['close'], record['prevclose'], record['rsi'], record['macd_signal'], 
                                 record['moving_average'], record['bollinger_top'], record['bollinger_bottom'], 
                                 record['atr'], record['volume'], record['historical_volatility'], 
                                 record['pricechange'], record['percentchange'], img_stream
                             )



    def send_email_warning(self, ticker, sequence_id, date):
        print("send_email_warning called")  
        sender = 'jsellin78@gmail.com'
        receivers = ['john.sellin@hotmail.com']
        subject = f'pattern was created for ticker {ticker} with sequence_id {sequence_id} on date {date}'
        body = 'Pattern created'
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(receivers)
        
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender, 'nnro aocd ezla pqps')
            server.sendmail(sender, receivers, msg.as_string())
            server.quit()
            print('Successfully sent email')
        except Exception as e:  # catch all exceptions
            print(f'Error: Unable to send email. Error message: {str(e)}')



    def close_connection(self):
        self.engine.dispose()



def main_job():
    predictor = DatabaseManager()
    db_conn = DbManager()
    latest_records = db_conn.load_latest_records()
    predictor.predict_and_sort()
    predictor.close_connection()

    ticker_data_list = []
    for ticker in latest_records['ticker'].unique():
        start_date = latest_records.loc[latest_records['ticker'] == ticker, 'date'].max() - pd.Timedelta(days=2)
        end_date = latest_records.loc[latest_records['ticker'] == ticker, 'date'].max()
        ticker_data = predictor.db_conn.fetch_candlestick_data(ticker, start_date, end_date)
        ticker_data_list.append(ticker_data)

if __name__ == "__main__":
    stockholm_timezone = pytz.timezone('Europe/Stockholm')
    scheduler = BackgroundScheduler(timezone=stockholm_timezone)
    job = scheduler.add_job(main_job, CronTrigger(minute='0,15,30,45'))
    scheduler.start()

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()






