import pandas as pd
import numpy as np
import os
from tkinter import Tk
from datetime import datetime, timedelta
from tkinter.filedialog import askopenfilename


# Function to extract the base package name
def extract_base_type_account(type_account):
    if 'Stellar 1-Step' in type_account:
        return 'Stellar 1-Step'
    elif 'Stellar 2-Step' in type_account:
        return 'Stellar 2-Step'
    elif 'Stellar Lite' in type_account:
        return 'Stellar Lite'
    elif 'Evaluation' in type_account:
        return 'Evaluation'
    elif 'Express' in type_account:
        return 'Express'
    else:
        return type_account.split('|')[0].strip()


# Function to clean the symbol name
def clean_symbol(symbol):
    if symbol.endswith('.i'):
        return symbol[:-2]  # Remove the '.i' suffix
    return symbol


# Function to convert account size strings to integers
def convert_account_size(size_str):
    size_str = size_str.strip().upper()
    if size_str.endswith('K'):
        return int(size_str[:-1]) * 1000
    else:
        try:
            return int(size_str)
        except ValueError:
            return None


# Function to open a file dialog and select a CSV file
def select_file():
    Tk().withdraw()  # Hide the root window
    file_path = askopenfilename(
        title="Select the CSV file",
        filetypes=[("CSV files", "*.csv")]
    )
    return file_path


# Use the function to get the file path
file_path = select_file()

# Load the selected file into a DataFrame
df = pd.read_csv(file_path)

# Convert the 'open_time' and 'close_time' columns to datetime format
df['open_time'] = pd.to_datetime(df['open_time'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df['close_time'] = pd.to_datetime(df['close_time'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')

# Print available column names for diagnostics
print("Available columns in the DataFrame:")
print(df.columns)

# Assuming the column name is correct
df['Base_Package'] = df['type_account'].apply(extract_base_type_account)
df['Clean_Symbol'] = df['symbol'].apply(clean_symbol)
df['Account_Size'] = df['type_account'].apply(lambda x: convert_account_size(x.split('|')[-1].strip()))

print("Package and account size extraction complete")

# Diagnostics: Print the first few rows to ensure correct processing
print("First few rows after processing:")
print(df.head())

old_leverage_mapping = {
    'Stellar 1-Step': {
        'ADAUSD': 2, 'BCHUSD': 2, 'BTCUSD': 2, 'DOGUSD': 2, 'ETHUSD': 2,
        'LNKUSD': 2, 'LTCUSD': 2, 'XLMUSD': 2, 'XMRUSD': 2, 'XRPUSD': 2,
        'AUDCAD': 30, 'AUDJPY': 30, 'AUDNZD': 30, 'AUDSGD': 30, 'AUDUSD': 30,
        'CADCHF': 30, 'CADJPY': 30, 'CHFJPY': 30, 'EURAUD': 30, 'EURCAD': 30,
        'EURCHF': 30, 'EURGBP': 30, 'EURHKD': 30, 'EURHUF': 30, 'EURJPY': 30,
        'EURNOK': 30, 'EURNZD': 30, 'EURSGD': 30, 'EURTRY': 30, 'EURUSD': 30,
        'GBPAUD': 30, 'GBPCAD': 30, 'GBPCHF': 30, 'GBPJPY': 30, 'GBPNZD': 30,
        'GBPSGD': 30, 'GBPUSD': 30, 'MXNJPY': 30, 'NOKJPY': 30, 'NZDCAD': 30,
        'NZDCHF': 30, 'NZDJPY': 30, 'NZDSGD': 30, 'NZDUSD': 30, 'SGDJPY': 30,
        'USDCAD': 30, 'USDCHF': 30, 'USDCNH': 30, 'USDDKK': 30, 'USDHUF': 30,
        'USDJPY': 30, 'USDMXN': 30, 'USDNOK': 30, 'USDPLN': 30, 'USDSGD': 30,
        'USDTRY': 30, 'USDZAR': 30, 'ZARJPY': 30, 'USDHKD': 30, 'AUDCHF': 30,
        'NDX100': 5, 'SPX500': 5, 'US30': 5, 'GER30': 5, 'US2000': 5,
        'UK100': 5, 'VIX': 5, 'SWI20': 5, 'NTH25': 5, 'JP225': 5,
        'HK50': 5, 'FRA40': 5, 'EUSTX50': 5, 'AUS200': 5, 'XAUUSD': 10,
        'XPTUSD': 10, 'XAGUSD': 10, 'USOUSD': 10, 'UKOUSD': 10
    },
    'Stellar 2-Step': {
        'ADAUSD': 2, 'BCHUSD': 2, 'BTCUSD': 2, 'DOGUSD': 2, 'ETHUSD': 2,
        'LNKUSD': 2, 'LTCUSD': 2, 'XLMUSD': 2, 'XMRUSD': 2, 'XRPUSD': 2,
        'AUDCAD': 100, 'AUDJPY': 100, 'AUDNZD': 100, 'AUDSGD': 100, 'AUDUSD': 100,
        'CADCHF': 100, 'CADJPY': 100, 'CHFJPY': 100, 'EURAUD': 100, 'EURCAD': 100,
        'EURCHF': 100, 'EURGBP': 100, 'EURHKD': 100, 'EURHUF': 100, 'EURJPY': 100,
        'EURNOK': 100, 'EURNZD': 100, 'EURSGD': 100, 'EURTRY': 100, 'EURUSD': 100,
        'GBPAUD': 100, 'GBPCAD': 100, 'GBPCHF': 100, 'GBPJPY': 100, 'GBPNZD': 100,
        'GBPSGD': 100, 'GBPUSD': 100, 'MXNJPY': 100, 'NOKJPY': 100, 'NZDCAD': 100,
        'NZDCHF': 100, 'NZDJPY': 100, 'NZDSGD': 100, 'NZDUSD': 100, 'SGDJPY': 100,
        'USDCAD': 100, 'USDCHF': 100, 'USDCNH': 100, 'USDDKK': 100, 'USDHUF': 100,
        'USDJPY': 100, 'USDMXN': 100, 'USDNOK': 100, 'USDPLN': 100, 'USDSGD': 100,
        'USDTRY': 100, 'USDZAR': 100, 'ZARJPY': 100, 'USDHKD': 100, 'AUDCHF': 100,
        'NDX100': 20, 'SPX500': 20, 'US30': 20, 'GER30': 20, 'US2000': 20,
        'UK100': 20, 'VIX': 20, 'SWI20': 20, 'NTH25': 20, 'JP225': 20,
        'HK50': 20, 'FRA40': 20, 'EUSTX50': 20, 'AUS200': 20, 'XAUUSD': 40,
        'XPTUSD': 40, 'XAGUSD': 40, 'USOUSD': 40, 'UKOUSD': 40
    },
    'Stellar Lite': {
        'ADAUSD': 2, 'BCHUSD': 2, 'BTCUSD': 2, 'DOGUSD': 2, 'ETHUSD': 2,
        'LNKUSD': 2, 'LTCUSD': 2, 'XLMUSD': 2, 'XMRUSD': 2, 'XRPUSD': 2,
        'AUDCAD': 100, 'AUDJPY': 100, 'AUDNZD': 100, 'AUDSGD': 100, 'AUDUSD': 100,
        'CADCHF': 100, 'CADJPY': 100, 'CHFJPY': 100, 'EURAUD': 100, 'EURCAD': 100,
        'EURCHF': 100, 'EURGBP': 100, 'EURHKD': 100, 'EURHUF': 100, 'EURJPY': 100,
        'EURNOK': 100, 'EURNZD': 100, 'EURSGD': 100, 'EURTRY': 100, 'EURUSD': 100,
        'GBPAUD': 100, 'GBPCAD': 100, 'GBPCHF': 100, 'GBPJPY': 100, 'GBPNZD': 100,
        'GBPSGD': 100, 'GBPUSD': 100, 'MXNJPY': 100, 'NOKJPY': 100, 'NZDCAD': 100,
        'NZDCHF': 100, 'NZDJPY': 100, 'NZDSGD': 100, 'NZDUSD': 100, 'SGDJPY': 100,
        'USDCAD': 100, 'USDCHF': 100, 'USDCNH': 100, 'USDDKK': 100, 'USDHUF': 100,
        'USDJPY': 100, 'USDMXN': 100, 'USDNOK': 100, 'USDPLN': 100, 'USDSGD': 100,
        'USDTRY': 100, 'USDZAR': 100, 'ZARJPY': 100, 'USDHKD': 100, 'AUDCHF': 100,
        'NDX100': 15, 'SPX500': 15, 'US30': 15, 'GER30': 15, 'US2000': 15,
        'UK100': 15, 'VIX': 15, 'SWI20': 15, 'NTH25': 15, 'JP225': 15,
        'HK50': 15, 'FRA40': 15, 'EUSTX50': 15, 'AUS200': 15, 'XAUUSD': 25,
        'XPTUSD': 25, 'XAGUSD': 25, 'USOUSD': 25, 'UKOUSD': 25
    },
    'Evaluation': {
        'ADAUSD': 2, 'BCHUSD': 2, 'BTCUSD': 2, 'DOGUSD': 2, 'ETHUSD': 2,
        'LNKUSD': 2, 'LTCUSD': 2, 'XLMUSD': 2, 'XMRUSD': 2, 'XRPUSD': 2,
        'AUDCAD': 100, 'AUDJPY': 100, 'AUDNZD': 100, 'AUDSGD': 100, 'AUDUSD': 100,
        'CADCHF': 100, 'CADJPY': 100, 'CHFJPY': 100, 'EURAUD': 100, 'EURCAD': 100,
        'EURCHF': 100, 'EURGBP': 100, 'EURHKD': 100, 'EURHUF': 100, 'EURJPY': 100,
        'EURNOK': 100, 'EURNZD': 100, 'EURSGD': 100, 'EURTRY': 100, 'EURUSD': 100,
        'GBPAUD': 100, 'GBPCAD': 100, 'GBPCHF': 100, 'GBPJPY': 100, 'GBPNZD': 100,
        'GBPSGD': 100, 'GBPUSD': 100, 'MXNJPY': 100, 'NOKJPY': 100, 'NZDCAD': 100,
        'NZDCHF': 100, 'NZDJPY': 100, 'NZDSGD': 100, 'NZDUSD': 100, 'SGDJPY': 100,
        'USDCAD': 100, 'USDCHF': 100, 'USDCNH': 100, 'USDDKK': 100, 'USDHUF': 100,
        'USDJPY': 100, 'USDMXN': 100, 'USDNOK': 100, 'USDPLN': 100, 'USDSGD': 100,
        'USDTRY': 100, 'USDZAR': 100, 'ZARJPY': 100, 'USDHKD': 100, 'AUDCHF': 100,
        'NDX100': 50, 'SPX500': 50, 'US30': 50, 'GER30': 50, 'US2000': 50,
        'UK100': 50, 'VIX': 50, 'SWI20': 50, 'NTH25': 50, 'JP225': 50,
        'HK50': 50, 'FRA40': 50, 'EUSTX50': 50, 'AUS200': 50, 'XAUUSD': 50,
        'XPTUSD': 50, 'XAGUSD': 50, 'USOUSD': 50, 'UKOUSD': 50
    },
    'Express': {
        'ADAUSD': 2, 'BCHUSD': 2, 'BTCUSD': 2, 'DOGUSD': 2, 'ETHUSD': 2,
        'LNKUSD': 2, 'LTCUSD': 2, 'XLMUSD': 2, 'XMRUSD': 2, 'XRPUSD': 2,
        'AUDCAD': 100, 'AUDJPY': 100, 'AUDNZD': 100, 'AUDSGD': 100, 'AUDUSD': 100,
        'CADCHF': 100, 'CADJPY': 100, 'CHFJPY': 100, 'EURAUD': 100, 'EURCAD': 100,
        'EURCHF': 100, 'EURGBP': 100, 'EURHKD': 100, 'EURHUF': 100, 'EURJPY': 100,
        'EURNOK': 100, 'EURNZD': 100, 'EURSGD': 100, 'EURTRY': 100, 'EURUSD': 100,
        'GBPAUD': 100, 'GBPCAD': 100, 'GBPCHF': 100, 'GBPJPY': 100, 'GBPNZD': 100,
        'GBPSGD': 100, 'GBPUSD': 100, 'MXNJPY': 100, 'NOKJPY': 100, 'NZDCAD': 100,
        'NZDCHF': 100, 'NZDJPY': 100, 'NZDSGD': 100, 'NZDUSD': 100, 'SGDJPY': 100,
        'USDCAD': 100, 'USDCHF': 100, 'USDCNH': 100, 'USDDKK': 100, 'USDHUF': 100,
        'USDJPY': 100, 'USDMXN': 100, 'USDNOK': 100, 'USDPLN': 100, 'USDSGD': 100,
        'USDTRY': 100, 'USDZAR': 100, 'ZARJPY': 100, 'USDHKD': 100, 'AUDCHF': 100,
        'NDX100': 50, 'SPX500': 50, 'US30': 50, 'GER30': 50, 'US2000': 50,
        'UK100': 50, 'VIX': 50, 'SWI20': 50, 'NTH25': 50, 'JP225': 50,
        'HK50': 50, 'FRA40': 50, 'EUSTX50': 50, 'AUS200': 50, 'XAUUSD': 50,
        'XPTUSD': 50, 'XAGUSD': 50, 'USOUSD': 50, 'UKOUSD': 50
    }
}

## Define the mappings for leverage and contract size for different packages and pairs
updated_leverage_mapping = {
    'Stellar 1-Step': {
        'ADAUSD': 1, 'BCHUSD': 1, 'BTCUSD': 1, 'DOGUSD': 1, 'ETHUSD': 1,
        'LNKUSD': 1, 'LTCUSD': 1, 'XLMUSD': 1, 'XMRUSD': 1, 'XRPUSD': 1,
        'AUDCAD': 30, 'AUDCHF': 30, 'AUDJPY': 30, 'AUDNZD': 30, 'AUDSGD': 30,
        'AUDUSD': 30, 'CADCHF': 30, 'CADJPY': 30, 'CHFJPY': 30, 'EURAUD': 30,
        'EURCAD': 30, 'EURCHF': 30, 'EURGBP': 30, 'EURHKD': 30, 'EURHUF': 30,
        'EURJPY': 30, 'EURNOK': 30, 'EURNZD': 30, 'EURSGD': 30, 'EURTRY': 30,
        'EURUSD': 30, 'GBPAUD': 30, 'GBPCAD': 30, 'GBPCHF': 30, 'GBPJPY': 30,
        'GBPNZD': 30, 'GBPSGD': 30, 'GBPUSD': 30, 'MXNJPY': 30, 'NOKJPY': 30,
        'NZDCAD': 30, 'NZDCHF': 30, 'NZDJPY': 30, 'NZDSGD': 30, 'NZDUSD': 30,
        'SGDJPY': 30, 'USDCAD': 30, 'USDCHF': 30, 'USDCNH': 30, 'USDDKK': 30,
        'USDHKD': 30, 'USDHUF': 30, 'USDJPY': 30, 'USDMXN': 30, 'USDNOK': 30,
        'USDPLN': 30, 'USDSEK': 30, 'USDSGD': 30, 'USDTRY': 30, 'USDZAR': 30,
        'ZARJPY': 30, 'AUS200': 5, 'EUSTX50': 5, 'FRA40': 5, 'GER30': 5,
        'HK50': 5, 'JP225': 5, 'NDX100': 5, 'NTH25': 5, 'SPX500': 5,
        'SWI20': 5, 'UK100': 5, 'US2000': 5, 'US30': 5, 'UKOUSD': 10,
        'USOUSD': 10, 'XAGUSD': 10, 'XAUUSD': 10, 'XPTUSD': 10
    },
    'Stellar 2-Step': {
        'ADAUSD': 1, 'BCHUSD': 1, 'BTCUSD': 1, 'DOGUSD': 1, 'ETHUSD': 1,
        'LNKUSD': 1, 'LTCUSD': 1, 'XLMUSD': 1, 'XMRUSD': 1, 'XRPUSD': 1,
        'AUDCAD': 100, 'AUDCHF': 100, 'AUDJPY': 100, 'AUDNZD': 100, 'AUDSGD': 100,
        'AUDUSD': 100, 'CADCHF': 100, 'CADJPY': 100, 'CHFJPY': 100, 'EURAUD': 100,
        'EURCAD': 100, 'EURCHF': 100, 'EURGBP': 100, 'EURHKD': 100, 'EURHUF': 100,
        'EURJPY': 100, 'EURNOK': 100, 'EURNZD': 100, 'EURSGD': 100, 'EURTRY': 100,
        'EURUSD': 100, 'GBPAUD': 100, 'GBPCAD': 100, 'GBPCHF': 100, 'GBPJPY': 100,
        'GBPNZD': 100, 'GBPSGD': 100, 'GBPUSD': 100, 'MXNJPY': 100, 'NOKJPY': 100,
        'NZDCAD': 100, 'NZDCHF': 100, 'NZDJPY': 100, 'NZDSGD': 100, 'NZDUSD': 100,
        'SGDJPY': 100, 'USDCAD': 100, 'USDCHF': 100, 'USDCNH': 100, 'USDDKK': 100,
        'USDHKD': 100, 'USDHUF': 100, 'USDJPY': 100, 'USDMXN': 100, 'USDNOK': 100,
        'USDPLN': 100, 'USDSEK': 100, 'USDSGD': 100, 'USDTRY': 100, 'USDZAR': 100,
        'ZARJPY': 100, 'AUS200': 15, 'EUSTX50': 15, 'FRA40': 15, 'GER30': 15,
        'HK50': 15, 'JP225': 15, 'NDX100': 15, 'NTH25': 15, 'SPX500': 15,
        'SWI20': 15, 'UK100': 15, 'US2000': 15, 'US30': 15, 'UKOUSD': 25,
        'USOUSD': 25, 'XAGUSD': 25, 'XAUUSD': 25, 'XPTUSD': 25
    },
    'Stellar Lite': {
        'ADAUSD': 1, 'BCHUSD': 1, 'BTCUSD': 1, 'DOGUSD': 1, 'ETHUSD': 1,
        'LNKUSD': 1, 'LTCUSD': 1, 'XLMUSD': 1, 'XMRUSD': 1, 'XRPUSD': 1,
        'AUDCAD': 100, 'AUDCHF': 100, 'AUDJPY': 100, 'AUDNZD': 100, 'AUDSGD': 100,
        'AUDUSD': 100, 'CADCHF': 100, 'CADJPY': 100, 'CHFJPY': 100, 'EURAUD': 100,
        'EURCAD': 100, 'EURCHF': 100, 'EURGBP': 100, 'EURHKD': 100, 'EURHUF': 100,
        'EURJPY': 100, 'EURNOK': 100, 'EURNZD': 100, 'EURSGD': 100, 'EURTRY': 100,
        'EURUSD': 100, 'GBPAUD': 100, 'GBPCAD': 100, 'GBPCHF': 100, 'GBPJPY': 100,
        'GBPNZD': 100, 'GBPSGD': 100, 'GBPUSD': 100, 'MXNJPY': 100, 'NOKJPY': 100,
        'NZDCAD': 100, 'NZDCHF': 100, 'NZDJPY': 100, 'NZDSGD': 100, 'NZDUSD': 100,
        'SGDJPY': 100, 'USDCAD': 100, 'USDCHF': 100, 'USDCNH': 100, 'USDDKK': 100,
        'USDHKD': 100, 'USDHUF': 100, 'USDJPY': 100, 'USDMXN': 100, 'USDNOK': 100,
        'USDPLN': 100, 'USDSEK': 100, 'USDSGD': 100, 'USDTRY': 100, 'USDZAR': 100,
        'ZARJPY': 100, 'AUS200': 15, 'EUSTX50': 15, 'FRA40': 15, 'GER30': 15,
        'HK50': 15, 'JP225': 15, 'NDX100': 15, 'NTH25': 15, 'SPX500': 15,
        'SWI20': 15, 'UK100': 15, 'US2000': 15, 'US30': 15, 'UKOUSD': 25,
        'USOUSD': 25, 'XAGUSD': 25, 'XAUUSD': 25, 'XPTUSD': 25
    },
    'Evaluation': {
        'ADAUSD': 1, 'BCHUSD': 1, 'BTCUSD': 1, 'DOGUSD': 1, 'ETHUSD': 1,
        'LNKUSD': 1, 'LTCUSD': 1, 'XLMUSD': 1, 'XMRUSD': 1, 'XRPUSD': 1,
        'AUDCAD': 100, 'AUDCHF': 100, 'AUDJPY': 100, 'AUDNZD': 100, 'AUDSGD': 100,
        'AUDUSD': 100, 'CADCHF': 100, 'CADJPY': 100, 'CHFJPY': 100, 'EURAUD': 100,
        'EURCAD': 100, 'EURCHF': 100, 'EURGBP': 100, 'EURHKD': 100, 'EURHUF': 100,
        'EURJPY': 100, 'EURNOK': 100, 'EURNZD': 100, 'EURSGD': 100, 'EURTRY': 100,
        'EURUSD': 100, 'GBPAUD': 100, 'GBPCAD': 100, 'GBPCHF': 100, 'GBPJPY': 100,
        'GBPNZD': 100, 'GBPSGD': 100, 'GBPUSD': 100, 'MXNJPY': 100, 'NOKJPY': 100,
        'NZDCAD': 100, 'NZDCHF': 100, 'NZDJPY': 100, 'NZDSGD': 100, 'NZDUSD': 100,
        'SGDJPY': 100, 'USDCAD': 100, 'USDCHF': 100, 'USDCNH': 100, 'USDDKK': 100,
        'USDHKD': 100, 'USDHUF': 100, 'USDJPY': 100, 'USDMXN': 100, 'USDNOK': 100,
        'USDPLN': 100, 'USDSEK': 100, 'USDSGD': 100, 'USDTRY': 100, 'USDZAR': 100,
        'ZARJPY': 100, 'AUS200': 15, 'EUSTX50': 15, 'FRA40': 15, 'GER30': 15,
        'HK50': 15, 'JP225': 15, 'NDX100': 15, 'NTH25': 15, 'SPX500': 15,
        'SWI20': 15, 'UK100': 15, 'US2000': 15, 'US30': 15, 'UKOUSD': 25,
        'USOUSD': 25, 'XAGUSD': 25, 'XAUUSD': 25, 'XPTUSD': 25
    },
    'Express': {
        'ADAUSD': 1, 'BCHUSD': 1, 'BTCUSD': 1, 'DOGUSD': 1, 'ETHUSD': 1,
        'LNKUSD': 1, 'LTCUSD': 1, 'XLMUSD': 1, 'XMRUSD': 1, 'XRPUSD': 1,
        'AUDCAD': 100, 'AUDCHF': 100, 'AUDJPY': 100, 'AUDNZD': 100, 'AUDSGD': 100,
        'AUDUSD': 100, 'CADCHF': 100, 'CADJPY': 100, 'CHFJPY': 100, 'EURAUD': 100,
        'EURCAD': 100, 'EURCHF': 100, 'EURGBP': 100, 'EURHKD': 100, 'EURHUF': 100,
        'EURJPY': 100, 'EURNOK': 100, 'EURNZD': 100, 'EURSGD': 100, 'EURTRY': 100,
        'EURUSD': 100, 'GBPAUD': 100, 'GBPCAD': 100, 'GBPCHF': 100, 'GBPJPY': 100,
        'GBPNZD': 100, 'GBPSGD': 100, 'GBPUSD': 100, 'MXNJPY': 100, 'NOKJPY': 100,
        'NZDCAD': 100, 'NZDCHF': 100, 'NZDJPY': 100, 'NZDSGD': 100, 'NZDUSD': 100,
        'SGDJPY': 100, 'USDCAD': 100, 'USDCHF': 100, 'USDCNH': 100, 'USDDKK': 100,
        'USDHKD': 100, 'USDHUF': 100, 'USDJPY': 100, 'USDMXN': 100, 'USDNOK': 100,
        'USDPLN': 100, 'USDSEK': 100, 'USDSGD': 100, 'USDTRY': 100, 'USDZAR': 100,
        'ZARJPY': 100, 'AUS200': 15, 'EUSTX50': 15, 'FRA40': 15, 'GER30': 15,
        'HK50': 15, 'JP225': 15, 'NDX100': 15, 'NTH25': 15, 'SPX500': 15,
        'SWI20': 15, 'UK100': 15, 'US2000': 15, 'US30': 15, 'UKOUSD': 25,
        'USOUSD': 25, 'XAGUSD': 25, 'XAUUSD': 25, 'XPTUSD': 25
    }
}

contract_size_mapping = {
    'ADAUSD': 100, 'BCHUSD': 1, 'BTCUSD': 1, 'DOGUSD': 1000, 'ETHUSD': 1,
    'LNKUSD': 100, 'LTCUSD': 1, 'XLMUSD': 100, 'XMRUSD': 1, 'XRPUSD': 100,
    'AUDCAD': 100000, 'AUDJPY': 100000, 'AUDNZD': 100000, 'AUDSGD': 100000, 'AUDUSD': 100000,
    'CADCHF': 100000, 'CADJPY': 100000,'USDSEK': 100000, 'CHFJPY': 100000, 'EURAUD': 100000, 'EURCAD': 100000,
    'EURCHF': 100000, 'EURGBP': 100000, 'EURHKD': 100000, 'EURHUF': 100000, 'EURJPY': 100000,
    'EURNOK': 100000, 'EURNZD': 100000, 'EURSGD': 100000, 'EURTRY': 100000, 'EURUSD': 100000,
    'GBPAUD': 100000, 'GBPCAD': 100000, 'GBPCHF': 100000, 'GBPJPY': 100000, 'GBPNZD': 100000,
    'GBPSGD': 100000, 'GBPUSD': 100000, 'MXNJPY': 100000, 'NOKJPY': 100000, 'NZDCAD': 100000,
    'NZDCHF': 100000, 'NZDJPY': 100000, 'NZDSGD': 100000, 'NZDUSD': 100000, 'SGDJPY': 100000,
    'USDCAD': 100000, 'USDCHF': 100000, 'USDCNH': 100000, 'USDDKK': 100000, 'USDHUF': 100000,
    'USDJPY': 100000, 'USDMXN': 100000, 'USDNOK': 100000, 'USDPLN': 100000, 'USDSGD': 100000,
    'USDTRY': 100000, 'USDZAR': 100000, 'ZARJPY': 100000, 'USDHKD': 100000, 'AUDCHF': 100000,
    'NDX100': 10, 'SPX500': 10, 'US30': 10, 'GER30': 10, 'US2000': 10,
    'UK100': 10, 'VIX': 10, 'SWI20': 10, 'NTH25': 10, 'JP225': 10,
    'HK50': 10, 'FRA40': 10, 'EUSTX50': 10, 'AUS200': 10, 'XAUUSD': 100,
    'XPTUSD': 100, 'XAGUSD': 5000, 'USOUSD': 100, 'UKOUSD': 100
}

# Define the multipliers for each pair
multiplier_mapping = {
    'ADAUSD': 100, 'BCHUSD': 100, 'BTCUSD': 1, 'DOGUSD': 100, 'ETHUSD': 100,
    'LNKUSD': 100, 'LTCUSD': 100, 'XLMUSD': 100, 'XMRUSD': 100, 'XRPUSD': 100,
    'AUDCAD': 100000, 'AUDJPY': 1000, 'AUDNZD': 100000, 'AUDSGD': 100000, 'AUDUSD': 100000,
    'CADCHF': 100000, 'CADJPY': 1000, 'CHFJPY': 1000, 'EURAUD': 100000, 'EURCAD': 100000,
    'EURCHF': 100000, 'EURGBP': 100000, 'EURHKD': 100000, 'EURHUF': 1000, 'EURJPY': 1000,
    'EURNOK': 100000, 'EURNZD': 100000, 'EURSGD': 100000, 'EURTRY': 100000, 'EURUSD': 100000,
    'GBPAUD': 100000, 'GBPCAD': 100000, 'GBPCHF': 10000, 'GBPJPY': 1000, 'GBPNZD': 100000,
    'GBPSGD': 100000, 'GBPUSD': 100000, 'MXNJPY': 1000, 'NOKJPY': 1000, 'NZDCAD': 100000,
    'NZDCHF': 100000, 'NZDJPY': 1000, 'NZDSGD': 100000, 'NZDUSD': 100000, 'SGDJPY': 1000,
    'USDCAD': 100000, 'USDCHF': 100000, 'USDCNH': 100000, 'USDDKK': 100000, 'USDHUF': 1000,
    'USDJPY': 1000, 'USDMXN': 100000, 'USDNOK': 100000, 'USDPLN': 100000, 'USDSGD': 100000,
    'USDTRY': 100000, 'USDZAR': 100000, 'ZARJPY': 1000, 'USDHKD': 100000, 'AUDCHF': 100000,
    'NDX100': 10, 'SPX500': 10, 'US30': 10, 'GER30': 10, 'US2000': 10,
    'UK100': 10, 'VIX': 10, 'SWI20': 10, 'NTH25': 10, 'JP225': 10,
    'HK50': 10, 'FRA40': 10, 'EUSTX50': 10, 'AUS200': 10, 'XAUUSD': 100,
    'XPTUSD': 100, 'XAGUSD': 1000, 'USOUSD': 100, 'UKOUSD': 100
}

# Conversion values provided
conversion_values = {
    'ADAUSD': 0.34, 'AUDCAD': 0.92, 'AUDCHF': 0.58, 'AUDJPY': 98.78, 'AUDNZD': 1.10,
    'AUDSGD': 0.88, 'AUDUSD': 0.67, 'AUS200': 7992.18, 'BCHUSD': 342.82, 'BTCUSD': 60835.74,
    'CADCHF': 0.63, 'CADJPY': 107.76, 'CHFJPY': 170.48, 'DOGUSD': 0.10, 'ETHUSD': 2662.46,
    'EURAUD': 1.65, 'EURCAD': 1.51, 'EURCHF': 0.96, 'EURGBP': 0.85, 'EURHKD': 8.63,
    'EURHUF': 394.55, 'EURJPY': 162.82, 'EURNOK': 11.71, 'EURNZD': 1.81, 'EURSGD': 1.45,
    'EURTRY': 37.49, 'EURUSD': 1.11, 'EUSTX50': 4877.02, 'FRA40': 7499.84, 'GBPAUD': 1.93,
    'GBPCAD': 1.77, 'GBPCHF': 1.12, 'GBPJPY': 190.78, 'GBPNZD': 2.12, 'GBPSGD': 1.70,
    'GBPUSD': 1.30, 'GER30': 18433.03, 'HK50': 17508.00, 'JP225': 38190.00, 'LNKUSD': 10.41,
    'LTCUSD': 67.47, 'MXNJPY': 7.88, 'NDX100': 19797.57, 'NOKJPY': 13.92, 'NTH25': 909.44,
    'NZDCAD': 0.83, 'NZDCHF': 0.53, 'NZDJPY': 89.83, 'NZDSGD': 0.80, 'NZDUSD': 0.61,
    'SGDJPY': 112.22, 'SPX500': 5611.41, 'SWI20': 12278.35, 'UK100': 8338.90, 'UKOUSD': 76.84,
    'US2000': 2178.20, 'US30': 40916.98, 'USDCAD': 1.36, 'USDCHF': 0.86, 'USDCNH': 7.14,
    'USDDKK': 6.74, 'USDHKD': 7.79, 'USDHUF': 356.22, 'USDJPY': 146.93, 'USDMXN': 18.69,
    'USDNOK': 10.57, 'USDPLN': 3.85, 'USDSEK': 10.32, 'USDSGD': 1.31, 'USDTRY': 33.82,
    'USDZAR': 17.74, 'USOUSD': 74.29, 'XAGUSD': 29.27, 'XAUUSD': 2499.64, 'XLMUSD': 0.10,
    'XPTUSD': 961.37, 'XRPUSD': 0.61, 'ZARJPY': 8.30
}

# Function to validate SL placement without modifying SL
def is_valid_sl(row):
    # Ignore trades where SL is 0, indicating no SL was set
    if row['sl'] == 0:
        return True

    # Check SL placement for buy and sell trades
    if row['type_str'] == 'buy' and row['sl'] >= row['open_price']:
        return False
    elif row['type_str'] == 'sell' and row['sl'] <= row['open_price']:
        return False
    return True


# Function to calculate Risk Amount and Risk Percentage, labeling invalid SL trades

def calculate_risk(row):
    """
    Calculate the risk amount and percentage for a trade based on starting_balance.

    Parameters:
        row (Series): A row of the DataFrame containing trade details.

    Returns:
        Tuple: (Risk Amount, Risk Percentage)
    """
    # Ensure type_str is standardized
    row['type_str'] = row['type_str'].strip().lower()
    package = row['Base_Package']
    starting_balance = row['starting_balance']
    symbol = row['Clean_Symbol']
    contract_size = contract_size_mapping.get(symbol, None)

    # Debug: Print the row details for verification
    print(f"Processing trade - Type: {row['type_str']}, Open Price: {row['open_price']}, SL: {row['sl']}")

    # Skip risk calculation if SL is 0, indicating no SL was set
    if row['sl'] == 0:
        print("SL is 0, skipping risk calculation.")
        return pd.NA, pd.NA  # Leave Risk_Amount and Risk_Percentage blank

    # Check SL validity without modifying SL
    if row['type_str'] == 'buy' and row['sl'] >= row['open_price']:
        print("Invalid SL for buy trade detected. SL >= Open Price.")
        return "Modified SL", "Modified SL"  # Label invalid SL for buy trades
    elif row['type_str'] == 'sell' and row['sl'] <= row['open_price']:
        print("Invalid SL for sell trade detected. SL <= Open Price.")
        return "Modified SL", "Modified SL"  # Label invalid SL for sell trades

    # Calculate risk if SL is valid and contract size is defined
    if contract_size is not None and pd.notna(row['sl']) and row['sl'] != 0:
        if symbol in ['US30', 'NDX100', 'US2000', 'SPX500']:
            risk_amount = abs((row['open_price'] - row['sl']) * row['FinalLot'] * contract_size)
        elif symbol.startswith('USD'):
            risk_amount = abs((row['open_price'] - row['sl']) * row['FinalLot'] * contract_size) / row['sl']
        elif symbol.endswith('USD'):
            risk_amount = abs((row['open_price'] - row['sl']) * row['FinalLot'] * contract_size)
        else:
            # Conversion rate determination
            if symbol == 'HK50':
                conversion_rate = conversion_values.get('USDHKD', None)
            elif symbol == 'JP225':
                conversion_rate = conversion_values.get('USDJPY', None)
            elif symbol == 'AUS200':
                conversion_rate = conversion_values.get('AUDUSD', None)
            elif symbol in ['EUSTX50', 'FRA40', 'GER30']:
                conversion_rate = conversion_values.get('EURUSD', None)
            elif symbol == 'UK100':
                conversion_rate = conversion_values.get('GBPUSD', None)
            else:
                # Generic currency conversion logic
                counter_currency = symbol[-3:]
                conversion_symbol = f'USD{counter_currency}'
                conversion_rate = conversion_values.get(conversion_symbol, None)

                if conversion_rate is None:
                    inverse_conversion_symbol = f'{counter_currency}USD'
                    inverse_conversion_rate = conversion_values.get(inverse_conversion_symbol, None)
                    if inverse_conversion_rate is not None:
                        conversion_rate = 1 / inverse_conversion_rate

            if conversion_rate is not None:
                risk_amount = abs((row['open_price'] - row['sl']) * row['FinalLot'] * contract_size) / conversion_rate
            else:
                print(f"Missing conversion rate for {symbol}. Risk calculation skipped.")
                return pd.NA, pd.NA

        risk_percentage = (risk_amount / starting_balance) * 100 if starting_balance else pd.NA
        return risk_amount, risk_percentage

    print("Contract size is None or SL is not valid. Skipping risk calculation.")
    return pd.NA, pd.NA


# Apply the updated risk calculations
df['Risk_Amount'], df['Risk_Percentage'] = zip(*df.apply(calculate_risk, axis=1))
print("Risk calculation with debugging complete.")
# Convert the 'open_time' and 'close_time' columns to datetime format with proper parsing
df['open_time'] = pd.to_datetime(df['open_time'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df['close_time'] = pd.to_datetime(df['close_time'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')


def get_leverage(package, symbol, open_time):
    """
    Get the leverage for a given symbol based on the package and open time.
    Uses old leverage mapping if the trade's open time is before 2024-10-25.
    """
    leverage_mapping = old_leverage_mapping if open_time < pd.Timestamp('2024-10-25') else updated_leverage_mapping
    return leverage_mapping.get(package, {}).get(symbol, None)


def calculate_margin(row):
    """
    Calculate the margin for a trade, regardless of SL values.

    Parameters:
        row (Series): A row of the DataFrame containing trade details.

    Returns:
        Tuple: (Margin Value, Margin Percentage) or (pd.NA, pd.NA) if missing values prevent calculation.
    """
    package = row.get('Base_Package', None)
    starting_balance = row.get('starting_balance', None)
    symbol = row.get('Clean_Symbol', None)
    contract_size = contract_size_mapping.get(symbol, None)
    leverage = get_leverage(package, symbol, row['open_time'])

    # Validate required fields
    if contract_size is None or leverage is None or starting_balance is None:
        print(f"Skipping margin calculation for {symbol}: Missing contract size, leverage, or starting_balance.")
        return pd.NA, pd.NA

    try:
        # Margin calculation based on symbol type
        if symbol in ['US30', 'NDX100', 'US2000', 'SPX500']:
            margin_value = (row['FinalLot'] * row['open_price'] * contract_size) / leverage
        elif symbol.startswith('USD'):
            margin_value = (row['FinalLot'] * contract_size) / leverage
        elif symbol.endswith('USD'):
            margin_value = (row['FinalLot'] * row['open_price'] * contract_size) / leverage
        else:
            # Handle non-USD symbols with currency conversion
            if symbol == 'HK50':
                conversion_rate = conversion_values.get('USDHKD', None)
            elif symbol == 'JP225':
                conversion_rate = conversion_values.get('USDJPY', None)
            elif symbol == 'AUS200':
                conversion_rate = conversion_values.get('AUDUSD', None)
            elif symbol in ['EUSTX50', 'FRA40', 'GER30']:
                conversion_rate = conversion_values.get('EURUSD', None)
            elif symbol == 'UK100':
                conversion_rate = conversion_values.get('GBPUSD', None)
            else:
                # Generic currency conversion logic
                counter_currency = symbol[-3:]
                conversion_symbol = f'USD{counter_currency}'
                conversion_rate = conversion_values.get(conversion_symbol, None)

                if conversion_rate is None:
                    # Try inverse conversion
                    inverse_conversion_symbol = f'{counter_currency}USD'
                    inverse_conversion_rate = conversion_values.get(inverse_conversion_symbol, None)
                    if inverse_conversion_rate is not None:
                        conversion_rate = 1 / inverse_conversion_rate

            if conversion_rate is not None:
                margin_value = ((row['FinalLot'] * row['open_price'] * contract_size) / leverage) / conversion_rate
            else:
                print(f"Missing conversion rate for {symbol}. Margin calculation skipped.")
                return pd.NA, pd.NA

        # Calculate margin percentage relative to starting_balance
        margin_percentage = (margin_value / starting_balance) * 100 if starting_balance else pd.NA
        return margin_value, margin_percentage

    except Exception as e:
        print(f"Error calculating margin for {symbol}: {e}")
        return pd.NA, pd.NA



# Apply the margin calculations to the DataFrame
df['Margin_Value'], df['Margin_Percentage'] = zip(*df.apply(calculate_margin, axis=1))
print("Margin calculation complete.")



# Custom function to try parsing dates with multiple formats
def try_parsing_date(text):
    for fmt in ('%Y.%m.%d %H:%M:%S', '%Y-%m-%d %H:%M:%S'):
        try:
            return pd.to_datetime(text, format=fmt)
        except ValueError:
            continue
    return pd.NaT

# Apply the custom date parsing function
df['open_time'] = df['open_time'].apply(try_parsing_date)
df['close_time'] = df['close_time'].apply(try_parsing_date)
print("Date parsing complete")
# Function to calculate max "at-a-time" lots, risk amount, and risk percentage for each login

def calculate_max_at_a_time_lots_and_risk(df_group):
    """
    Calculate the maximum "at-a-time" lots, risk amount, and risk percentage for each group of trades.

    Parameters:
        df_group (DataFrame): A grouped DataFrame (e.g., grouped by login).

    Returns:
        max_lot_trades (DataFrame): DataFrame containing trades contributing to the maximum lot size.
        max_risk_trades (DataFrame): DataFrame containing trades contributing to the maximum risk and risk percentage.
    """
    max_lots = 0
    max_risk = 0
    max_risk_percentage = 0
    active_trades = []
    max_lot_trades = pd.DataFrame()
    max_risk_trades = pd.DataFrame()

    # Ensure trades are sorted by open_time
    df_group = df_group.sort_values(by='open_time')

    for _, row in df_group.iterrows():
        # Remove trades that no longer overlap with the current trade
        active_trades = [
            trade for trade in active_trades
            if trade['close_time'] > row['open_time'] and trade['open_time'] < row['close_time']
        ]

        # Add the current trade to active trades
        active_trades.append(row.to_dict())

        # Calculate the total lot size of all overlapping trades
        current_lots = sum(trade['FinalLot'] for trade in active_trades)

        # Calculate the cumulative risk amount and risk percentage
        current_risk = sum(
            trade['Risk_Amount'] for trade in active_trades
            if trade['Risk_Amount'] is not None and trade['Risk_Amount'] != "Modified SL"
        )
        starting_balance = row.get('starting_balance', None)
        current_risk_percentage = (current_risk / starting_balance * 100) if starting_balance else pd.NA

        # Update max lots and save the corresponding trades
        if current_lots > max_lots:
            max_lots = current_lots
            max_lot_trades = pd.DataFrame(active_trades)
            max_lot_trades['Max Lot'] = max_lots

        # Update max risk and save the corresponding trades
        if current_risk > max_risk:
            max_risk = current_risk
            max_risk_percentage = current_risk_percentage
            max_risk_trades = pd.DataFrame(active_trades)
            max_risk_trades['Max Risk'] = max_risk
            max_risk_trades['Max Risk Percentage'] = max_risk_percentage

    return max_lot_trades, max_risk_trades



# Group the DataFrame by login and apply the function to each group
grouped = df.groupby('login')
results = grouped.apply(calculate_max_at_a_time_lots_and_risk)

# Separate results into max lot and max risk DataFrames
lot_results = [res[0] for res in results if not res[0].empty]
risk_results = [res[1] for res in results if not res[1].empty]

# Combine results into final DataFrames
if lot_results:
    max_lot_trades = pd.concat(lot_results, ignore_index=True)
else:
    max_lot_trades = pd.DataFrame(columns=[
        'login', 'account_id', 'ticket', 'type_str', 'symbol',
        'FinalLot', 'open_time', 'close_time', 'open_price',
        'sl', 'tp', 'close_price', 'Max Lot', 'email'
    ])

if risk_results:
    max_risk_trades = pd.concat(risk_results, ignore_index=True)
else:
    max_risk_trades = pd.DataFrame(columns=[
        'login', 'account_id', 'ticket', 'type_str', 'symbol',
        'FinalLot', 'Risk_Amount', 'Risk_Percentage', 'open_time',
        'close_time', 'open_price', 'sl', 'tp', 'close_price',
        'Max Risk', 'Max Risk Percentage', 'email'
    ])

print("Max lots and risk calculations are complete.")




# Function to calculate max "at-a-time" margin for each login
def calculate_max_at_a_time_margin(df_group):
    """
    Calculate the maximum "at-a-time" margin and margin percentage for each group (e.g., login).

    Parameters:
        df_group (DataFrame): A grouped DataFrame for a specific login.

    Returns:
        DataFrame: Rows contributing to the maximum margin and percentage.
    """
    max_margin = 0
    max_margin_percentage = 0
    active_trades = []
    max_margin_trades = pd.DataFrame()

    for i, row in df_group.iterrows():
        # Remove trades that have ended
        active_trades = [
            trade for trade in active_trades
            if trade['close_time'] > row['open_time']
        ]

        # Add the current trade to active trades
        active_trades.append(row.to_dict())

        # Calculate cumulative margin for all active trades
        current_margin = sum(
            trade['Margin_Value'] for trade in active_trades
            if pd.notna(trade['Margin_Value'])
        )

        # Calculate margin percentage based on starting_balance
        starting_balance = row['starting_balance']
        current_margin_percentage = (current_margin / starting_balance * 100) if starting_balance else pd.NA

        # Update max values and save the contributing trades
        if current_margin > max_margin:
            max_margin = current_margin
            max_margin_percentage = current_margin_percentage
            max_margin_trades = pd.DataFrame(active_trades)
            max_margin_trades['Max Margin'] = max_margin
            max_margin_trades['Max Margin Percentage'] = max_margin_percentage

    return max_margin_trades



# Group by login and apply the function to each group
grouped = df.groupby('login')
margin_results = grouped.apply(calculate_max_at_a_time_margin)

# Combine results into a DataFrame
if isinstance(margin_results, pd.DataFrame) and not margin_results.empty:
    max_margin_trades = margin_results.reset_index(drop=True)
else:
    max_margin_trades = pd.DataFrame(columns=[
        'login', 'account_id', 'ticket', 'type_str', 'symbol',
        'FinalLot', 'Margin_Value', 'open_time', 'close_time',
        'Max Margin', 'Max Margin Percentage', 'email'
    ])

print("Max margin at-a-time calculation complete.")



# Function to calculate Risk to Reward Ratio (RRR)
def calculate_rrr(row):
    # Ignore trades where SL is not set or is marked as modified in the 'Risk_Amount'
    if row['sl'] == 0 or 'Modified SL' in str(row['Risk_Amount']):
        return None

    # Calculate risk as the absolute difference between open price and SL
    risk = abs(row['open_price'] - row['sl'])

    # Determine reward based on TP or close price if TP is not set (TP=0)
    if row['tp'] == 0:
        reward = abs(row['open_price'] - row['close_price'])
    else:
        reward = abs(row['open_price'] - row['tp'])

    # Avoid calculation if risk or reward is zero to prevent division by zero
    if risk == 0 or reward == 0:
        return None

    # Calculating the Risk to Reward Ratio, keeping risk as 1
    rrr = f"1:{reward / risk:.2f}"
    return rrr


# Apply the RRR calculation function to the DataFrame
df['RRR'] = df.apply(calculate_rrr, axis=1)

print("RRR calculations have been added to the DataFrame.")

# Ensure 'open_time' is in datetime format in max_risk_trades
max_risk_trades['open_time'] = pd.to_datetime(max_risk_trades['open_time'], errors='coerce')

# Initialize summary data
summary_data = []

for email in df['email'].unique():
    try:
        # Filter trades for the specific email and year 2024
        email_data = df[(df['email'] == email) & (df['open_time'].dt.year == 2024)]

        # Filter out rows with "Modified SL" or missing values in Risk_Percentage
        valid_risk_data = email_data[email_data['Risk_Percentage'].apply(lambda x: isinstance(x, (int, float)))]

        # Metrics calculations
        total_trades = len(email_data)
        trades_without_sl = email_data['sl'].isna().sum() + (email_data['sl'] == 0).sum()
        percent_trades_without_sl = (trades_without_sl / total_trades * 100) if total_trades > 0 else 0
        trades_with_risk_over_5 = (valid_risk_data['Risk_Percentage'] > 5).sum()
        trades_with_margin_over_75 = (email_data['Margin_Percentage'] > 75).sum()

        # Logins with Risk % > 5
        logins_with_risk_over_5 = valid_risk_data.groupby('login')['Risk_Percentage'].apply(
            lambda x: (x > 5).any()).sum()
        logins_with_margin_over_75 = email_data.groupby('login')['Margin_Percentage'].apply(
            lambda x: (x > 75).any()).sum()

        # Logins with Max At-a-Time Risk % >= 5
        email_max_risk_trades = max_risk_trades[
            (max_risk_trades['email'] == email) &
            (max_risk_trades['Max Risk Percentage'] >= 5) &
            (max_risk_trades['open_time'].dt.year == 2024)
            ]
        logins_with_max_at_a_time_risk_over_5 = email_max_risk_trades['login'].nunique()

        # Cumulative FinalLot per login and top 3 by cumulative FinalLot
        email_max_lot_trades = max_lot_trades[(max_lot_trades['email'] == email) &
                                              (max_lot_trades['open_time'].dt.year == 2024)]
        cumulative_lot_trades = email_max_lot_trades.groupby('login').agg({'FinalLot': 'sum'}).reset_index()
        top_3_lots = cumulative_lot_trades.nlargest(3, 'FinalLot')

        # Prepare cumulative FinalLot, login, and symbols for each top lot
        lot_info = []
        for _, row in top_3_lots.iterrows():
            cumulative_final_lot = row['FinalLot']
            login = row['login']
            symbols = ', '.join(email_max_lot_trades[email_max_lot_trades['login'] == login]['symbol'].unique())
            lot_info.extend([cumulative_final_lot, login, symbols])

        # Ensure 3 sets of FinalLot, login, and symbol columns
        while len(lot_info) < 9:
            lot_info.extend([None, None, None])

        # Collect summary data
        summary_data.append([
                                email, total_trades, trades_without_sl, percent_trades_without_sl,
                                trades_with_risk_over_5, trades_with_margin_over_75,
                                logins_with_risk_over_5, logins_with_margin_over_75,
                                logins_with_max_at_a_time_risk_over_5
                            ] + lot_info)

    except KeyError as e:
        print(f"Skipping {email} due to missing data: {e}")
        continue

# Define columns for the summary DataFrame
summary_columns = [
    'Email', 'Total Trades Count', 'Trades without SL', '% of Trades without SL',
    'Trades with Risk % > 5', 'Trades with Margin % > 75',
    'Logins with Risk % > 5', 'Logins with Margin % > 75',
    'Logins with Max At-a-Time Risk % >= 5',
    'FinalLot (1st Max Lot)', 'Login (1st Max Lot)', 'Symbol (1st Max Lot)',
    'FinalLot (2nd Max Lot)', 'Login (2nd Max Lot)', 'Symbol (2nd Max Lot)',
    'FinalLot (3rd Max Lot)', 'Login (3rd Max Lot)', 'Symbol (3rd Max Lot)'
]

# Create a DataFrame for the summary
summary_df = pd.DataFrame(summary_data, columns=summary_columns)



def convert_rr_to_float(rr_string):
    if isinstance(rr_string, str):
        try:
            return float(rr_string.split(':')[1])
        except (IndexError, ValueError):
            return np.nan  # Return NaN if there's an error in splitting or converting
    return np.nan  # Return NaN if rr_string is not a string
# Calculate average win to average loss ratio per email
average_metrics_by_email = []

for email, group in df.groupby('email'):
    # Calculate average win and average loss
    average_win = group[group['profit'] > 0]['profit'].mean()
    average_loss = group[group['profit'] < 0]['profit'].mean()

    # Calculate win to loss ratio
    if average_loss != 0:  # Avoid division by zero
        win_loss_ratio = abs(average_win / average_loss)
        ratio_formatted = f"1:{win_loss_ratio:.2f}"
    else:
        ratio_formatted = "No losses"

    # Store the results
    average_metrics_by_email.append({
        'Email': email,
        'Win to Loss Ratio': ratio_formatted
    })

# Convert to DataFrame
average_metrics_df = pd.DataFrame(average_metrics_by_email)

# Optionally, write to Excel or merge with existing DataFrame
# Here's how to merge it with the 'account_metrics_df' if it exists
if 'account_metrics_df' in globals():
    account_metrics_df = account_metrics_df.merge(average_metrics_df, on='Email', how='left')

# Print the DataFrame to check the results
print(average_metrics_df.head())


# List to store each email's metrics as dictionaries
account_metrics_by_email = []

for email, group in df.groupby('email'):

    # Filter unique logins for each category within each email group
    # Filter unique logins for each category within each email group
    # Ensure P1 logins exclude Real accounts
    p1_logins = group[(group['type_account'].str.contains('P1|Stellar 1-Step|Express', na=False)) &
                      (~group['type_account'].str.contains('Real', na=False))]['login'].nunique()

    p2_logins = group[group['type_account'].str.contains('P2', na=False)]['login'].nunique()
    real_logins = group[group['type_account'].str.contains('Real', na=False)]['login'].nunique()

    # Calculate the average R:R
    group['RR_numeric'] = group['RRR'].apply(convert_rr_to_float)
    average_rr = group['RR_numeric'].mean()
    # Combined PnL of all FN accounts for this email
    combined_pnl = group[group['type_account'].str.contains('Real', na=False)]['profit'].sum()

    # Failure to reach Funded Phase % for this email
    failure_to_reach_funded_phase = (real_logins / p1_logins) * 100 if p1_logins > 0 else 0

    # Funded Breach % for this email
    # Updated condition to handle empty strings
    # Fill NaN values with an empty string before any operations
    df['breachedby'] = df['breachedby'].fillna('')

    breached_real_logins = df[(df['type_account'].str.contains('Real', na=False)) &
                              (df['breachedby'].str.contains('Daily Loss Limit|Monthly Loss Limit', na=False) & df[
                                  'breachedby'] != '')]['login'].nunique()
    funded_breach_percentage = (breached_real_logins / real_logins) * 100 if real_logins > 0 else 0

    # Highest Margin % for this email
    highest_margin = group['Margin_Percentage'].max()

    # Biggest Losing Day PnL for this email
    group['open_date'] = group['open_time'].dt.date  # Extract date from open_time
    daily_pnl = group.groupby('open_date')['profit'].sum()
    biggest_losing_day_pnl = daily_pnl.min()

    # Biggest Losing Trade PnL for this email
    biggest_losing_trade_pnl = group['profit'].min()

    # Average Losing PnL for this email
    average_losing_pnl = group[group['profit'] < 0]['profit'].mean()

    # Average Winning PnL for this email
    average_winning_pnl = group[group['profit'] > 0]['profit'].mean()

    # % of Trades with SL (SL is not null and not zero)
    percent_trades_with_sl = ((group['sl'].notna() & (group['sl'] != 0)).sum() / len(group)) * 100

    # % of Trades without SL (SL is either null or zero)
    percent_trades_without_sl = ((group['sl'].isna() | (group['sl'] == 0)).sum() / len(group)) * 100

    # % of Trades with TP (TP is not null and not zero)
    percent_trades_with_tp = ((group['tp'].notna() & (group['tp'] != 0)).sum() / len(group)) * 100

    # % of Trades without TP (TP is either null or zero)
    percent_trades_without_tp = ((group['tp'].isna() | (group['tp'] == 0)).sum() / len(group)) * 100

    # Max Traded Lots in a Day for this email
    daily_lots = group.groupby('open_date')['FinalLot'].sum()
    max_traded_lots_in_a_day = daily_lots.max()

    # Store metrics for this email in a dictionary
    account_metrics_by_email.append({
        'Email': email,
        'Average R:R': average_rr, # Add the average R:R here
        'Combined PnL of all FN accounts': combined_pnl,
        'Failure to reach Funded Phase %': failure_to_reach_funded_phase,
        'Funded Breach %': funded_breach_percentage,
        'Highest Margin %': highest_margin,
        'Biggest Losing Day PnL': biggest_losing_day_pnl,
        'Biggest Losing Trade PnL': biggest_losing_trade_pnl,
        'Average Losing PnL': average_losing_pnl,
        'Average Winning PnL': average_winning_pnl,
        '% of Trades with TP': percent_trades_with_tp,
        '% of Trades with SL': percent_trades_with_sl,
        '% of Trades without SL': percent_trades_without_sl,
        'Max Traded Lots in a Day': max_traded_lots_in_a_day,
        'Unique logins for P1 accounts': p1_logins,
        'Unique logins for P2 accounts': p2_logins,
        'Unique logins for Real (FN) accounts': real_logins
    })


account_metrics_df = pd.DataFrame(account_metrics_by_email)
if 'account_metrics_df' in globals():
    account_metrics_df = account_metrics_df.merge(average_metrics_df, on='Email', how='left')

# Get the current date and calculate the date one month ago
current_date = datetime.now()
one_month_ago = current_date - timedelta(days=30)

# Filter the data for the last one month
df_last_month = df[(df['open_time'] >= one_month_ago) & (df['open_time'] <= current_date)]

# Initialize summary data for the last one month
summary_data_last_month = []

for email in df_last_month['email'].unique():
    try:
        # Filter data for the current email
        email_data = df_last_month[df_last_month['email'] == email]

        # Filter valid risk data
        valid_risk_data = email_data[email_data['Risk_Percentage'].apply(lambda x: isinstance(x, (int, float)))]

        # Metrics calculations
        total_trades = len(email_data)
        trades_without_sl = email_data['sl'].isna().sum() + (email_data['sl'] == 0).sum()
        percent_trades_without_sl = (trades_without_sl / total_trades * 100) if total_trades > 0 else 0
        trades_with_risk_over_5 = (valid_risk_data['Risk_Percentage'] > 5).sum()
        trades_with_margin_over_75 = (email_data['Margin_Percentage'] > 75).sum()

        # Logins with Risk % > 5
        logins_with_risk_over_5 = valid_risk_data.groupby('login')['Risk_Percentage'].apply(lambda x: (x > 5).any()).sum()
        logins_with_margin_over_75 = email_data.groupby('login')['Margin_Percentage'].apply(lambda x: (x > 75).any()).sum()

        # Logins with Max At-a-Time Risk % >= 5
        email_max_risk_trades = max_risk_trades[
            (max_risk_trades['email'] == email) &
            (max_risk_trades['Max Risk Percentage'] >= 5) &
            (max_risk_trades['open_time'] >= one_month_ago) &
            (max_risk_trades['open_time'] <= current_date)
        ]
        logins_with_max_at_a_time_risk_over_5 = email_max_risk_trades['login'].nunique()

        # Cumulative FinalLot per login and top 3 by cumulative FinalLot
        email_max_lot_trades = max_lot_trades[
            (max_lot_trades['email'] == email) &
            (max_lot_trades['open_time'] >= one_month_ago) &
            (max_lot_trades['open_time'] <= current_date)
        ]
        cumulative_lot_trades = email_max_lot_trades.groupby('login').agg({'FinalLot': 'sum'}).reset_index()
        top_3_lots = cumulative_lot_trades.nlargest(3, 'FinalLot')

        # Prepare cumulative FinalLot, login, and symbols for each top lot
        lot_info = []
        for _, row in top_3_lots.iterrows():
            cumulative_final_lot = row['FinalLot']
            login = row['login']
            symbols = ', '.join(email_max_lot_trades[email_max_lot_trades['login'] == login]['symbol'].unique())
            lot_info.extend([cumulative_final_lot, login, symbols])

        # Ensure 3 sets of FinalLot, login, and symbol columns
        while len(lot_info) < 9:
            lot_info.extend([None, None, None])

        # Collect summary data for the last month
        summary_data_last_month.append([
            email, total_trades, trades_without_sl, percent_trades_without_sl,
            trades_with_risk_over_5, trades_with_margin_over_75,
            logins_with_risk_over_5, logins_with_margin_over_75,
            logins_with_max_at_a_time_risk_over_5
        ] + lot_info) 

    except KeyError as e:
        print(f"Skipping {email} due to missing data: {e}")
        continue

# Define columns for the one-month summary DataFrame
summary_columns_last_month = [
    'Email', 'Total Trades Count', 'Trades without SL', '% of Trades without SL',
    'Trades with Risk % > 5', 'Trades with Margin % > 75',
    'Logins with Risk % > 5', 'Logins with Margin % > 75',
    'Logins with Max At-a-Time Risk % >= 5',
    'FinalLot (1st Max Lot)', 'Login (1st Max Lot)', 'Symbol (1st Max Lot)',
    'FinalLot (2nd Max Lot)', 'Login (2nd Max Lot)', 'Symbol (2nd Max Lot)',
    'FinalLot (3rd Max Lot)', 'Login (3rd Max Lot)', 'Symbol (3rd Max Lot)'
]

# Create a DataFrame for the one-month summary
summary_df_last_month = pd.DataFrame(summary_data_last_month, columns=summary_columns_last_month)
# Define the output path
output_directory = r"C:/Users/sunjida.ferdous/PycharmProjects/pythonProject"
output_file = f"{output_directory}\\Trades_Processed_Data_with_Metrics.xlsx"

# Create the directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Save the data to Excel
with pd.ExcelWriter(output_file, mode='w') as writer:
    # Write processed data and summaries to separate sheets
    df.to_excel(writer, sheet_name='Processed_Data', index=False)
    max_lot_trades.to_excel(writer, sheet_name='Max_Lot_Trades', index=False)
    max_risk_trades.to_excel(writer, sheet_name='Max_Risk_Trades', index=False)
    max_margin_trades.to_excel(writer, sheet_name='Max_Margin_Trades', index=False)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    summary_df_last_month.to_excel(writer, sheet_name='Last_Month_Summary', index=False)
    account_metrics_df.to_excel(writer, sheet_name='Account Metrics by Email', index=False)

print(f"Processed data has been saved successfully to {output_file}")
