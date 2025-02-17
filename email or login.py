import time
import pandas as pd
from sqlalchemy import create_engine
from tkinter import Tk
from tkinter.filedialog import askdirectory

# Database connection details
db_config = {
    'user': '****',
    'password': '****',
    'host': '****',
    'database': '****',
    'port': ****
}

# Example inputs
email_list = ['amirowji1989@gmail.com','rmamanazarov0503@gmail.com','aminelamuscupro@icloud.com']
login_list = []

# Start measuring time
script_start_time = time.time()

def fetch_data(email_list=None, login_list=None, output_folder=None):
    """
    Fetch trades data based on email or login and save to the output folder.
    """
    # Ensure the output folder is provided
    if not output_folder:
        print("No folder selected. Exiting script.")
        return

    # Create the database connection string and engine
    connection_string = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    engine = create_engine(connection_string)

    def format_tuple(input_list):
        if len(input_list) > 1:
            return f"({','.join([repr(x) for x in input_list])})"
        else:
            return f"('{input_list[0]}')"

    def convert_unix_timestamp(timestamp):
        if len(str(timestamp)) == 13:  # Check for milliseconds
            return pd.to_datetime(timestamp, unit='ms', errors='coerce')
        else:  # Assume seconds
            return pd.to_datetime(timestamp, unit='s', errors='coerce')

    try:
        if email_list:
            # Fetch customer IDs for the provided emails
            emails = format_tuple(email_list)
            customers_query = f"SELECT id AS customer_id, email FROM customers WHERE email IN {emails};"
            customers_df = pd.read_sql(customers_query, engine)
            print("Customers fetched by email:")
            print(customers_df.head())

            if customers_df.empty:
                print("No customers found for the provided email(s).")
                return

            customer_ids = customers_df['customer_id'].tolist()

            # Fetch accounts for the customers
            accounts_query = f"""
            SELECT id AS account_id, login, type AS type_account, customer_id, breachedby, starting_balance
            FROM accounts 
            WHERE customer_id IN {format_tuple(customer_ids)};
            """
            accounts_df = pd.read_sql(accounts_query, engine)

            # Merge accounts with customer data
            accounts_df = pd.merge(accounts_df, customers_df, on='customer_id', how='left')
            print("Accounts after merging with customers:")
            print(accounts_df.head())

        elif login_list:
            # Fetch accounts directly by login
            logins = format_tuple(login_list)
            accounts_query = f"""
            SELECT id AS account_id, login, type AS type_account, customer_id, breachedby, starting_balance
            FROM accounts 
            WHERE login IN {logins};
            """
            accounts_df = pd.read_sql(accounts_query, engine)

            if accounts_df.empty:
                print("No accounts found for the provided login(s).")
                return

            # Fetch customer data for the accounts
            customer_ids = accounts_df['customer_id'].tolist()
            customers_query = f"""
            SELECT id AS customer_id, email FROM customers 
            WHERE id IN {format_tuple(customer_ids)};
            """
            customers_df = pd.read_sql(customers_query, engine)

            # Merge accounts with customer data
            accounts_df = pd.merge(accounts_df, customers_df, on='customer_id', how='left')
            print("Accounts after merging with customers:")
            print(accounts_df.head())

        else:
            print("No emails or logins provided. Exiting script.")
            return

        # Fetch trades for the accounts
        login_ids = format_tuple(accounts_df['login'].tolist())
        trades_query = f"""
        SELECT id, open_time, close_time, symbol, open_price, close_price, login, volume, close_time_str, 
               commission, digits, open_time_str, profit, reason, sl, swap, ticket, tp, type_str, created_at,
               CASE 
                   WHEN login LIKE '70%' OR login LIKE '30%' THEN lots
                   ELSE volume / 100
               END AS FinalLot
        FROM trades
        WHERE login IN {login_ids};
        """
        trades_df = pd.read_sql(trades_query, engine)

        if trades_df.empty:
            print("No trades found for the provided accounts.")
            return

        # Convert UNIX timestamps to human-readable format
        trades_df['open_time'] = trades_df['open_time'].apply(convert_unix_timestamp)
        trades_df['close_time'] = trades_df['close_time'].apply(convert_unix_timestamp)

        # Format timestamps
        trades_df['open_time'] = trades_df['open_time'].dt.strftime('%m/%d/%Y %I:%M:%S %p')
        trades_df['close_time'] = trades_df['close_time'].dt.strftime('%m/%d/%Y %I:%M:%S %p')

        # Merge trades with account data
        combined_df = pd.merge(trades_df, accounts_df, on='login', suffixes=('_trade', '_account'))
        print("Combined DataFrame after merging trades and accounts:")
        print(combined_df.head())

        # Fill missing starting_balance with NaN and ensure correct column order
        if 'starting_balance' not in combined_df.columns:
            combined_df['starting_balance'] = pd.NA

        final_df = combined_df[
            ['account_id', 'login', 'open_time', 'ticket', 'type_str', 'FinalLot', 'symbol', 'open_price', 'sl', 'tp',
             'close_time', 'close_price', 'commission', 'swap', 'profit', 'type_account', 'email', 'breachedby',
             'reason', 'starting_balance']
        ]

        # Save to CSV in the output folder
        csv_file_name = f"{output_folder}/trades_data.csv"
        final_df.to_csv(csv_file_name, index=False)
        print(f"Data has been written to {csv_file_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

    # End measuring time
    script_end_time = time.time()
    print(f"Time taken to run the script: {script_end_time - script_start_time} seconds")

# Select output folder and run the function
print("Please select a folder to save the output file...")
Tk().withdraw()
output_folder = askdirectory()

if output_folder:
    # Fetch data for emails
    if email_list:
        fetch_data(email_list=email_list, output_folder=output_folder)

    # Fetch data for logins
    if login_list:
        fetch_data(login_list=login_list, output_folder=output_folder)
else:
    print("No folder selected. Exiting script.")
