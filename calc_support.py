#!/usr/bin/python

import sys
import operator
import pandas as pd

def calc_indv_gain(open_value, close_value):
    gain = close_value - open_value
    if gain < 0:
        gain = 0
    return gain

def calc_indv_loss(open_value, close_value):
    loss = open_value - close_value
    if loss < 0:
        loss = 0
    return loss

def calc_gain(df_data):
    gain = df_data.apply(lambda row: calc_indv_gain(row['Open'], row['Close']), axis=1)
    return gain

def calc_loss(df_data):
    loss = df_data.apply(lambda row: calc_indv_loss(row['Open'], row['Close']), axis=1)
    return loss

def calc_spread(df_data):
    spread = df_data['High'] - df_data['Low']
    return spread

def calc_mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def calc_mov_avg(df_data, index, days):
    # Get the largest index of the data (starting date)
    last = len(df_data.index) - 1
    # Can't calculate any values until you have a complete range to average
    if index > last - days:
        mean = None
    # Once you get 10 days, 15 days, etc. from start of sample
    else:
        current_slice = df_data[index:index+days]
        mean = current_slice['Adj Close'].mean()
    return mean

def calc_high(df_data, index, days):
    # Get the largest index of the data (starting date)
    last = len(df_data.index) - 1
    # If starting date is less than {days} ago, using starting date as end point
    if index + days > last:
        end_search = last
    else:
        end_search = index + days
    current_slice = df_data[index:end_search]
    high = current_slice['Adj Close'].max()
    return high

def calc_low(df_data, index, days):
    # Get the largest index of the data (starting date)
    last = len(df_data.index) - 1
    # If starting date is less than {days} ago, using starting date as end point
    if index + days > last:
        end_search = last
    else:
        end_search = index + days
    current_slice = df_data[index:end_search]
    low = current_slice['Adj Close'].min()
    return low

def calc_per_gain(df_data, index, days):
    # Get the largest index of the data (starting date)
    last = len(df_data.index) - 1
    # Can't calculate any values until you have a complete range to average
    if index >= last - days:
        gain = None
    # Once you get 10 days, 15 days, etc. from start of sample
    else:
        column = str(days) + ' MA'
        today = df_data.get_value(index, column)
        yesterday = df_data.get_value(index+1, column)
        gain = ((today / yesterday) - 1) * 100
    return gain

def calc_avg_gain_s(df_data, index, days):
    # Get the largest index of the data (starting date)
    last = len(df_data.index) - 1
    # Can't calculate any values until you have a complete range to average
    if index > last - days:
        avg_gain = None
    # Once you get 14 days, 28 days, etc. from start of sample
    else:
        current_slice = df_data[index:index+days]
        gain_values = []
        for func_index in current_slice.index:
            current_gain = df_data.get_value(func_index, 'Gain')
            if current_gain != 0:
                gain_values.append(current_gain)
        avg_gain = calc_mean(gain_values)
    return avg_gain

def calc_avg_loss_s(df_data, index, days):
    # Get the largest index of the data (starting date)
    last = len(df_data.index) - 1
    # Can't calculate any values until you have a complete range to average
    if index > last - days:
        avg_loss = None
    # Once you get 14 days, 28 days, etc. from start of sample
    else:
        current_slice = df_data[index:index+days]
        loss_values = []
        for func_index in current_slice.index:
            current_loss = df_data.get_value(func_index, 'Loss')
            if current_loss != 0:
                loss_values.append(current_loss)
        avg_loss = calc_mean(loss_values)
    return avg_loss

def calc_avg_gain_e(df_data, index, days):
    # Get the largest index of the data (starting date)
    last = len(df_data.index) - 1
    # Can't calculate any values until you have a complete range to average
    if index > last - days:
        avg_gain = None
    # The first data point calculated is the same as the simple avg. gain
    elif index == last - days:
        avg_gain_s_col = str(days) + ' Sim. Avg. Gain'
        avg_gain = df_data.get_value(index, avg_gain_s_col)
    # Else use the previous exponential avg. gain and current gain to calculate value
    else:
        avg_gain_e_col = str(days) + ' Exp. Avg. Gain'
        prev_avg_gain = df_data.get_value(index+1, avg_gain_e_col)
        curr_gain = df_data.get_value(index, 'Gain')
        avg_gain = ((prev_avg_gain*13) + curr_gain) / 14
    return avg_gain

def calc_avg_loss_e(df_data, index, days):
    # Get the largest index of the data (starting date)
    last = len(df_data.index) - 1
    # Can't calculate any values until you have a complete range to average
    if index > last - days:
        avg_loss = None
    # The first data point calculated is the same as the simple avg. loss
    elif index == last - days:
        avg_loss_s_col = str(days) + ' Sim. Avg. Loss'
        avg_loss = df_data.get_value(index, avg_loss_s_col)
    # Else use the previous exponential avg. loss and current loss to calculate value
    else:
        avg_loss_e_col = str(days) + ' Exp. Avg. Loss'
        prev_avg_loss = df_data.get_value(index+1, avg_loss_e_col)
        curr_loss = df_data.get_value(index, 'Loss')
        avg_loss = ((prev_avg_loss*13) + curr_loss) / 14
    return avg_loss

def calc_rsi_s(df_data, index, days):
    # Get the largest index of the data (starting date)
    last = len(df_data.index) - 1
    # Can't calculate any values until you have a complete range to average
    if index > last - days:
        rsi = None
    # Once you get 14 days, 28 days, etc. from start of sample
    else:
        avg_gain_col = str(days) + ' Sim. Avg. Gain'
        avg_loss_col = str(days) + ' Sim. Avg. Loss'
        avg_gain = df_data.get_value(index, avg_gain_col)
        avg_loss = df_data.get_value(index, avg_loss_col)
        if avg_loss == 0 or avg_loss == 0.0:
            rsi = None
        else:
            rsi = 100 - (100 / (1 + avg_gain/avg_loss))
        return rsi

def calc_rsi_e(df_data, index, days):
    # Get the largest index of the data (starting date)
    last = len(df_data.index) - 1
    # Can't calculate any values until you have a complete range to average
    if index > last - days:
        rsi = None
    # Once you get 14 days, 28 days, etc. from start of sample
    else:
        avg_gain_col = str(days) + ' Exp. Avg. Gain'
        avg_loss_col = str(days) + ' Exp. Avg. Loss'
        avg_gain = df_data.get_value(index, avg_gain_col)
        avg_loss = df_data.get_value(index, avg_loss_col)
        if avg_loss == 0 or avg_loss == 0.0:
            rsi = None
        else:
            rsi = 100 - (100 / (1 + avg_gain/avg_loss))
        return rsi

def calc_ema(df_data, index, days):
    # Get the largest index of the data (starting date)
    last = len(df_data.index) - 1
    # Can't calculate any values until you have a complete range to average
    if index > last - days:
        ema = None
    # The first data point calculated is the same as the simple moving average
    elif index == last - days:
        MA_col = str(days) + ' MA'
        ema = df_data.get_value(index, MA_col)
    # Else use the previous EMA and current adj. close to calculate value
    else:
        EMA_col = str(days) + ' EMA'
        prev_ema = df_data.get_value(index+1, EMA_col)
        curr_adj_close = df_data.get_value(index, 'Adj Close')
        multiplier = float(2.0 / (float(days) + 1.0))
        ema = ((curr_adj_close - prev_ema) * multiplier) + prev_ema
    return ema
