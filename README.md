Email or Login Wise Traders Metrics

Overview

This repository contains Python scripts designed to analyze trader activities based on provided email addresses or login credentials. The scripts extract trade data from a database, calculate key metrics such as risk, margin, trade lots, and generate reports for further analysis.

Files

1. email or login.py

Fetches trade data based on given email addresses or login IDs.

Retrieves account and customer details.

Extracts trade history and related metrics.

Saves the extracted data to a CSV file for further processing.

Allows users to specify the output folder for saving results.

2. new_risk_margin.py

Processes the extracted trade data to calculate:

Risk amount and percentage.

Margin amount and percentage.

Maximum lot sizes at any given time.

Maximum risk exposure at any given time.

Risk-to-Reward Ratio (RRR) for trades.

Highest leverage used.

Computes various trader performance metrics such as:

Percentage of trades with or without SL and TP.

Biggest losing day and trade.

Average winning and losing PnL.

Failure rate for reaching funded phase.

Funded account breach percentage.

Generates a detailed Excel report with multiple sheets.

Requirements

Python 3.x

Required Python Libraries:

pandas

sqlalchemy

mysql-connector-python

tkinter

numpy

openpyxl

Installation

Clone this repository:

git clone https://github.com/yourusername/Email-or-login-wise-traders-metrics.git
cd Email-or-login-wise-traders-metrics

Install dependencies:

pip install pandas sqlalchemy mysql-connector-python numpy openpyxl

Usage

Running the Scripts

Execute email or login.py

Modify email_list or login_list with the relevant details.

Run the script:

python "email or login.py"

Choose the output folder when prompted.

This generates a CSV file containing trade details.

Execute new_risk_margin.py

Ensure the CSV file from email or login.py exists.

Run the script:

python "new_risk_margin.py"

This generates an Excel file with detailed trader performance metrics.

Output Files

trades_data.csv:

Raw extracted trade data with account details.

Trades_Processed_Data_with_Metrics.xlsx:

Includes various sheets such as:

Processed_Data: Cleaned and formatted trade data.

Max_Lot_Trades: Traders with the highest lot sizes.

Max_Risk_Trades: Traders with the highest risk exposure.

Max_Margin_Trades: Traders with the highest margin usage.

Summary: Overall trade summary per email.

Last_Month_Summary: Trade summary for the past month.

Account Metrics by Email: Performance metrics for each email account.

Notes

Ensure the correct database credentials are set before execution.

Scripts require access to MySQL databases containing trade, account, and customer information.

Modify SQL queries if your database structure differs.

License
