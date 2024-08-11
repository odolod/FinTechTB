import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.metrics import MeanAbsoluteError
import pandas_ta as ta
import datetime as dt

def get_period_from_interval(interval):
    period = "1y"
    if interval == '1mo' : period = '5y'
    if interval == '3mo' : period = '10y'
    if interval == '5d' : period = '2y'

    return period 

def load_data(symbol, interval):
    df = yf.Ticker(symbol).history(interval=interval, period=get_period_from_interval(interval))
    
    return df

def predict_lstm(df):
    # подготовка данных
    # новый фрейм данных только с столбцом Close.
    data = df.filter(['Close'])
    # преобразуем в Numpy array
    dataset = data.values
    # количество строк train
    training_data_len = int(np.ceil( len(dataset) * .95 ))

    print(training_data_len)
    
    # маштабируем данные
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)

    # создаем и масштабируем трэйн
    train_data = scaled_data[0:int(training_data_len), :]
    # Разделим данные на наборы данных x_train и y_train.
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])
        if i<= 61:
            print(x_train)
            print(y_train)
            print()

    # преобразуем в array
    x_train, y_train = np.array(x_train), np.array(y_train)

    # меняем размеры
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    return x_train, y_train

def predict_ta_lstm(df):
    # загрузка данных
    #df = load_data(symbol, interval)
    # подготовка данных
    data = df
    # добавим несколько технических индикаторов, таких как RSI и скользящие средние
    data['rsi'] = ta.rsi(data.Close, length=15)
    data['ema_20'] = ta.ema(data.Close, length=20)
    data['ema_50'] = ta.ema(data.Close, length=50)

    # drop NaN
    data = data.dropna(axis=0)
    
    print("data2",data.head)

    y = data['Close']
    del data['Close']
    del data['Dividends']
    del data['Stock Splits']
    
    print("data3",data.head)
    # scaling data
    x_scaler = MinMaxScaler(feature_range=(0,1)).fit(data)
    x_scaled = x_scaler.transform(data)

    y_scaler = MinMaxScaler(feature_range=(0,1)).fit(y.values.reshape(-1, 1))
    y_scaled = y_scaler.transform(y.values.reshape(-1, 1))

    # разделим на обучение и проверку
    test_size = 0.3
    len_x = len(data)
    x_train = x_scaled[:int(len_x*(1-test_size))]
    y_train = y_scaled[:int(len_x*(1-test_size))]
    x_test = x_scaled[int(len_x*(1-test_size)):]
    y_test = y_scaled[int(len_x*(1-test_size)):]

    # обучим модель
    model = Sequential()
    model.add(LSTM(10, input_shape=(None, 1), activation='relu'))
    model.add(Dense(1))

    model.compile(optimizer='Adam', loss='mean_squared_error', metrics=[MeanAbsoluteError])

    history = model.fit(x_train, y_train, epochs=100)

    # предсказание на следуюший период
    data_today = data.iloc[-1]

    data_today_scaled = x_scaler.transform(data_today.values.reshape(1, -1))
    predict_today = model.predict(data_today_scaled)
    inversed = y_scaler.inverse_transform(predict_today)

    return inversed

#df = load_data("MSFT", "1d")
#print(predict_ta_lstm("MSFT", "1d"))