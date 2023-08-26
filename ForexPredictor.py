import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow.keras.layers import Dense, LSTM, Conv1D, Dropout
from tensorflow.keras.utils import to_categorical
from sqlalchemy import create_engine  
from tensorflow.keras.optimizers import Adam
from sklearn.utils.class_weight import compute_sample_weight
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from tensorflow.keras import regularizers
from imblearn.over_sampling import SMOTE
from keras.layers import BatchNormalization
from tensorflow.keras import layers, Sequential
import faulthandler; faulthandler.enable()
from pandas import Timedelta
import pandas as pd
from joblib import dump
from keras.layers import LeakyReLU, MaxPooling1D
import faulthandler; faulthandler.enable()
from keras.metrics import Precision, Recall
from tensorflow.keras import backend as K
import tensorflow as tf
from tensorflow.keras.layers import Attention
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten
import shap 


# Check if TensorFlow is built with CUDA
print("Is TensorFlow built with CUDA:", tf.test.is_built_with_cuda())

# Check if TensorFlow can access a GPU
print("Is GPU available:", tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None))


if tf.test.is_gpu_available():
    print("GPU is available")
else:
    print("GPU is not available")

# Print CUDA and cuDNN version if GPU is available
if tf.test.is_gpu_available():
    print("CUDA version:", tf.sysconfig.get_build_info()['cuda_version'])
    print("cuDNN version:", tf.sysconfig.get_build_info()['cudnn_version'])

class ForexPredictor:
    def __init__(self, sequence_length, learning_rate):
        self.pattern_lengths = {'bullish_wigs': 3}
        self.scaler = StandardScaler()
        self.le = LabelEncoder()
#        self.model = self.build_model()
        self.sequence_length = sequence_length
        self.learning_rate = learning_rate
        self.early_stopping = self.early_stopping = EarlyStopping(monitor='val_loss', patience=100000)
        self.X_train = None  
        self.X_val = None  
        self.y_train = None  
        self.y_val = None  


    def create_engine(self):
        self.pattern_set = create_engine('postgresql://john:john93@192.168.1.186:5432/forex_data') 
        self.test_set = create_engine('postgresql://john:john93@192.168.1.186:5432/forex_data')  


    def load_data(self):
        connection = self.pattern_set.connect()
        try:
            self.ohlc_pattern = pd.read_sql_table('three_wigs', con=connection)
        except:
            connection.rollback()
            raise
        finally:
            connection.close()
        connection = self.test_set.connect()
        try:
            self.ohlc = pd.read_sql_table('fiftheen', con=connection)
            print("Shape of the ohlc data:", self.ohlc.shape) # Print shape of ohlc_pattern
        except:
            connection.rollback()
            raise
        finally:
            connection.close()



    def preprocess_data(self):
        self.ohlc = pd.get_dummies(self.ohlc, columns=['candle'])
        self.ohlc_pattern = pd.get_dummies(self.ohlc_pattern, columns=['candle'])
        self.features_pattern = self.ohlc_pattern[['body', 'upwiq', 'downwiq', 'candle_bullish', 'candle_bearish']].values
        self.features = self.ohlc[['body', 'upwiq', 'downwiq', 'candle_bullish', 'candle_bearish']].values
        self.target = self.ohlc['true_tag'].values
        self.target_pattern = self.ohlc_pattern.groupby('sequence_id')['date'].diff().fillna(pd.Timedelta(seconds=0))
        self.ohlc = self.ohlc.sort_values(['ticker', 'date'], ascending=[True, True])


    def create_sequences(self, features, target, sequence_length):
        features_seq = []
        target_seq = []
        for i in range(sequence_length, len(features)):
            features_seq.append(features[i - sequence_length:i])
            target_seq.append(target[i - 1])  # to make sure we're getting the target corresponding to the last element of the sequence
        return np.array(features_seq), np.array(target_seq)


    def create_seq_for_match(self, features, target, sequence_length):
        features_seq = []
        target_seq = []
        for i in range(0, len(features), sequence_length):
            if i + sequence_length <= len(features):  # this ensures that we don't create a sequence that goes beyond the end of the dataset
                features_seq.append(features[i:i + sequence_length])
                target_seq.append(target[i + sequence_length - 1])  # to make sure we're getting the target corresponding to the last element of the sequence
        return np.array(features_seq), np.array(target_seq)



    # Initialize an empty set to store the patterns that have been found.
    found_patterns = set()


    def data_processing(self):
        self.features_seq_pattern, self.target_seq_pattern = self.create_sequences(self.features_pattern, self.target_pattern, self.sequence_length)
        flattened_features_seq_pattern = self.features_seq_pattern.reshape(-1, self.features_seq_pattern.shape[-1])
        scaled_flattened_features_seq_pattern = self.scaler.fit_transform(flattened_features_seq_pattern)
        self.features_seq_pattern = scaled_flattened_features_seq_pattern.reshape(self.features_seq_pattern.shape)
        self.test_sequences = np.array([self.features[i - self.sequence_length:i] for i in range(self.sequence_length, len(self.features))])
        flattened_test_sequences = self.test_sequences.reshape(-1, self.test_sequences.shape[-1])
        scaled_flattened_test_sequences = self.scaler.transform(flattened_test_sequences)
        self.test_sequences = scaled_flattened_test_sequences.reshape(self.test_sequences.shape)



    def encode_target(self):
        self.target_seq_pattern_encoded = self.le.fit_transform(self.target_seq_pattern)
        self.target_seq_pattern_encoded = to_categorical(self.target_seq_pattern_encoded)


    def scaler(self):    
        # Flatten, Scale and Reshape the pattern sequences
        scaled_flattened_features_seq_pattern = self.scaler.fit_transform(self.flattened_features_seq_pattern)
        self.features_seq_pattern = scaled_flattened_features_seq_pattern.reshape(self.features_seq_pattern.shape)
        # Create sequences for test data
        test_sequences = np.array([self.features[i - self.sequence_length:i] for i in range(self.sequence_length, len(self.features))])
        # Flatten, Scale and Reshape the test sequences
        flattened_test_sequences = test_sequences.reshape(-1, test_sequences.shape[-1])
        scaled_flattened_test_sequences = self.scaler.transform(flattened_test_sequences)
        test_sequences = scaled_flattened_test_sequences.reshape(test_sequences.shape)

    def LabelEncoder(self):
        # Encoding target labels
        self.target_seq_pattern_encoded = self.le.fit_transform(self.target_seq_pattern)
        self.target_seq_pattern_encoded = to_categorical(self.target_seq_pattern_encoded)

    def compute_class_weights(self):
        # Compute class weights only for the pattern data
        self.class_weights = compute_sample_weight('balanced', self.target_seq_pattern)
        self.class_weights_dict = dict(enumerate(self.class_weights))

    def split_data(self):
        # Use the pattern data for training and split it into training and validation sets
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(self.features_seq_pattern, self.target_seq_pattern_encoded, test_size=0.2, random_state=42)


    def apply_smote(self):
        unique_classes = np.unique(np.argmax(self.y_train, axis=1))
        if len(unique_classes) > 1:
            # Flatten the sequences for SMOTE
            X_train_flat = self.X_train.reshape(self.X_train.shape[0], -1)
            y_train_flat = np.argmax(self.y_train, axis=1)  # inverse of to_categorical
            # Apply SMOTE
            smote = SMOTE(k_neighbors=3, random_state=42)  # Use 3 neighbors instead of the default 5
            X_train_smote, y_train_smote = smote.fit_resample(X_train_flat, y_train_flat)
            # Reshape the sequences back to their original shape
            self.X_train_smote = X_train_smote.reshape(-1, self.X_train.shape[1], self.X_train.shape[2])
            self.y_train_smote = to_categorical(y_train_smote)
        else:
            # There's only one class, so just return the original dataset
            self.X_train_smote = self.X_train
            self.y_train_smote = self.y_train


    def build_model(self):
        input_shape = (self.X_train.shape[1], self.X_train.shape[2])
        inputs = Input(shape=input_shape)

        x = Conv1D(filters=64, kernel_size=1, kernel_initializer='he_normal')(inputs)
        x = LeakyReLU(alpha=0.01)(x)
        x = BatchNormalization()(x)
        x = Dropout(0.2)(x)

        x = Conv1D(filters=32, kernel_size=2, kernel_initializer='he_normal')(x)
        x = LeakyReLU(alpha=0.01)(x)
        x = MaxPooling1D(pool_size=2)(x)
        x = BatchNormalization()(x)
        x = Dropout(0.2)(x)

        x = LSTM(50, return_sequences=True, dropout=0.2, recurrent_dropout=0.2)(x)
        x = LSTM(25, return_sequences=True, dropout=0.2, recurrent_dropout=0.2)(x)

        # Attention layer
        attention_output = Attention()([x, x]) # Query and value are both the output of LSTM

        x = Flatten()(attention_output)
        x = Dense(100, activation='relu', kernel_initializer='he_normal')(x)
        x = BatchNormalization()(x)
        x = Dropout(0.2)(x)

        x = Dense(100, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4), kernel_initializer='he_normal')(x)
        x = BatchNormalization()(x)
        
        x = Dense(100, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4), kernel_initializer='he_normal')(x)
        x = BatchNormalization()(x)

        outputs = Dense(self.y_train.shape[1], activation='softmax')(x)

        model = Model(inputs, outputs)
        self.model = model

        return model


    def compile_model(self):
        # Compile the model
        self.learning_rate = 0.02
        optimizer = Adam(learning_rate=self.learning_rate)
        precision = Precision()
        recall = Recall()
        f1_score = F1Score()
        self.model.compile(loss='categorical_crossentropy',
                        optimizer=optimizer,
                        metrics=['accuracy', precision, recall, f1_score])



    def train_model(self):
            # Train the model
            history = self.model.fit(self.X_train, self.y_train, validation_data=(self.X_val, self.y_val), epochs=400, batch_size=32, class_weight=self.class_weights_dict, callbacks=[self.early_stopping])
            # Accessing precision and recall
            precision = history.history['precision']
            recall = history.history['recall']
            val_precision = history.history['val_precision']
            val_recall = history.history['val_recall']        # ...
            f1_score_values = history.history['f1_score']
            self.predictions = self.model.predict(self.test_sequences)
            self.model.save("pre111.h5")
            self.predictions = self.model.predict(self.test_sequences)

    def predict(self):
        class_indices = {index: name for index, name in enumerate(self.le.classes_)}
        results_dict = {}
        timestamp_column = 'date'  # Assuming the timestamps are available in a column named 'date', adjust the column name if needed
        self.ohlc = self.ohlc.sort_values('date')
        for ticker in self.ohlc['ticker'].unique():
            ticker_data = self.ohlc[self.ohlc['ticker'] == ticker]

            # Loop over each pattern length
            for pattern, length in self.pattern_lengths.items():
                features_ticker = ticker_data[['body', 'upwiq', 'downwiq', 'candle_bullish', 'candle_bearish']].values

                # Use create_seq_for_match to create fixed length sequences
                test_sequences_ticker, _ = self.create_seq_for_match(features_ticker, np.zeros(len(features_ticker)), self.sequence_length)
                
                flattened_test_sequences_ticker = test_sequences_ticker.reshape(-1, test_sequences_ticker.shape[-1])
                scaled_flattened_test_sequences_ticker = self.scaler.transform(flattened_test_sequences_ticker)
                test_sequences_ticker = scaled_flattened_test_sequences_ticker.reshape(test_sequences_ticker.shape)
                predictions_ticker = self.model.predict(test_sequences_ticker)

                # Threshold for filtering sequences
                threshold = 0.85  # Adjust based on your requirements

                # Get the predicted class and its probability for each sequence
                max_probs = predictions_ticker.max(axis=1)
                max_class_indices = predictions_ticker.argmax(axis=1)

                # Filter sequences where the max probability is above the threshold
                filter_mask = max_probs > threshold
                filtered_indices = np.where(filter_mask)[0] + self.sequence_length
                filtered_class_indices = max_class_indices[filter_mask]

                # Store the matched patterns in the dictionary
                for index, class_index in zip(filtered_indices, filtered_class_indices):
                    class_name = class_indices[class_index]
                    if ticker not in results_dict:
                        results_dict[ticker] = {}
                    if class_name not in results_dict[ticker]:
                        results_dict[ticker][class_name] = []

                    timestamp = ticker_data.iloc[index][timestamp_column]
                    sequence = ticker_data.iloc[index-self.sequence_length+1:index+1]  # Extracting the sequence

                    if len(results_dict[ticker][class_name]) >= 3:  # If we have already got 5 sequences, skip this one
                        continue


                    if results_dict[ticker][class_name]:  # If there are already some sequences
                        for _, prev_timestamp, _ in results_dict[ticker][class_name]:
                            prev_index, prev_timestamp, prev_sequence = results_dict[ticker][class_name][-1]
                            time_diff = pd.to_datetime(timestamp) - pd.to_datetime(prev_timestamp)
                            if time_diff < pd.Timedelta(minutes=15):  # If the time difference is less than 15 minutes, skip this sequence
                                continue

                            # If this sequence is identical to the previous sequence, skip this sequence
                            if np.array_equal(sequence, prev_sequence):
                                continue
                    results_dict[ticker][class_name].append((index, timestamp, sequence))  # Including sequence in the storage

        # Print only matched patterns found in the patterns_set

        for pattern in self.pattern_lengths:
            for ticker, patterns in results_dict.items():
                if pattern in patterns.keys():
                    for match in patterns[pattern]:
                        index, timestamp, sequence = match  # Unpacking sequence
                        print(f"Results for Ticker: {ticker}")
                        print(f"Pattern: {pattern}")
                        print(f"  Matched Row: {index}, Ticker: {ticker}, Timestamp: {timestamp}")
                        print(f"  Corresponding sequence:\n{sequence}\n")  # Printing sequence



    def predict_and_sort(self, batch_size=3):
        class_indices = {index: name for index, name in enumerate(self.le.classes_)}
        all_predictions = []
        timestamp_column = 'date'
        self.ohlc = self.ohlc.sort_values('date')
        for ticker in self.ohlc['ticker'].unique():
            ticker_data = self.ohlc[self.ohlc['ticker'] == ticker]

            # Split the timestamps into batches
            timestamp_batches = [ticker_data[i:i + batch_size] for i in range(0, len(ticker_data), batch_size)]

            for timestamp_batch in timestamp_batches:
                features_ticker = timestamp_batch[['body', 'upwiq', 'downwiq', 'candle_bullish', 'candle_bearish']].values
                test_sequences_ticker, _ = self.create_seq_for_match(features_ticker, np.zeros(len(features_ticker)), self.sequence_length)

                if test_sequences_ticker.size == 0:
                    print(f"No data for ticker: {ticker}")
                    continue

                flattened_test_sequences_ticker = test_sequences_ticker.reshape(-1, test_sequences_ticker.shape[-1])
                scaled_flattened_test_sequences_ticker = self.scaler.transform(flattened_test_sequences_ticker)
                test_sequences_ticker = scaled_flattened_test_sequences_ticker.reshape(test_sequences_ticker.shape)
                predictions_ticker = self.model.predict(test_sequences_ticker)

                # Create a set to keep track of indices already added to the predictions
                added_indices = set()

                for pattern, length in self.pattern_lengths.items():
                    # Sort the predictions first by date and then by probability (from lowest to highest)
                    for i in range(0, len(predictions_ticker)):
                        # Only add this prediction if it hasn't been added before
                        if i not in added_indices:
                            max_prob_index = np.argmax(predictions_ticker[i])
                            max_prob = predictions_ticker[i][max_prob_index]
                            class_name = class_indices[max_prob_index]
                            corresponding_date = timestamp_batch.iloc[i][timestamp_column]  # Use timestamp_batch instead of ticker_data
                            all_predictions.append((ticker, corresponding_date, i, max_prob, class_name))
                            added_indices.add(i)  # Mark this index as added

            # If there are remaining timestamps not processed in the last batch
            if len(ticker_data) % batch_size != 0:
                remaining_data = ticker_data.iloc[-(len(ticker_data) % batch_size):]
                features_ticker = remaining_data[['body', 'upwiq', 'downwiq', 'candle_bullish', 'candle_bearish']].values
                test_sequences_ticker, _ = self.create_seq_for_match(features_ticker, np.zeros(len(features_ticker)), self.sequence_length)

                if test_sequences_ticker.size != 0:
                    flattened_test_sequences_ticker = test_sequences_ticker.reshape(-1, test_sequences_ticker.shape[-1])
                    scaled_flattened_test_sequences_ticker = self.scaler.transform(flattened_test_sequences_ticker)
                    test_sequences_ticker = scaled_flattened_test_sequences_ticker.reshape(test_sequences_ticker.shape)
                    predictions_ticker = self.model.predict(test_sequences_ticker)

                    for pattern, length in self.pattern_lengths.items():
                        for i in range(0, len(predictions_ticker)):
                            if i not in added_indices:
                                max_prob_index = np.argmax(predictions_ticker[i])
                                max_prob = predictions_ticker[i][max_prob_index]
                                class_name = class_indices[max_prob_index]
                                corresponding_date = remaining_data.iloc[i][timestamp_column]
                                all_predictions.append((ticker, corresponding_date, i, max_prob, class_name))
                                added_indices.add(i)

        all_predictions.sort(key=lambda x: (x[1], x[3]), reverse=False)

        for prediction in all_predictions:
            ticker, date, index, prob, class_name = prediction
            print(f"Ticker: {ticker}, Date: {date}, Index: {index}, Probability: {prob * 100}%, Predicted Class: {class_name}")

class F1Score(tf.keras.metrics.Metric):
    def __init__(self, name='f1_score', **kwargs):
        super(F1Score, self).__init__(name=name, **kwargs)
        self.precision_obj = Precision()
        self.recall_obj = Recall()

    def update_state(self, y_true, y_pred, sample_weight=None):
        self.precision_obj.update_state(y_true, y_pred, sample_weight)
        self.recall_obj.update_state(y_true, y_pred, sample_weight)

    def result(self):
        precision = self.precision_obj.result()
        recall = self.recall_obj.result()
        return 2 * ((precision * recall) / (precision + recall + K.epsilon()))

    def reset_state(self):
        self.precision_obj.reset_state()
        self.recall_obj.reset_state()



forex_predictor = ForexPredictor(sequence_length=3, learning_rate=0.02)
forex_predictor.create_engine()
forex_predictor.load_data()
forex_predictor.preprocess_data()
forex_predictor.data_processing()
forex_predictor.encode_target()
forex_predictor.compute_class_weights()
forex_predictor.split_data()
forex_predictor.apply_smote()
forex_predictor.build_model()
forex_predictor.compile_model()
forex_predictor.train_model()
forex_predictor.predict_and_sort()



