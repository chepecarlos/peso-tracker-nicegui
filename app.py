import os
import pandas as pd
from nicegui import ui

# Constants
GOAL_LB = 300.0
CSV_FILE = 'pesos.csv'

# Load weights data or create demo data
if not os.path.exists(CSV_FILE):
    data = {'Weight (lb)': [150, 200, 250], 'Date': ['2023-01-01', '2023-02-01', '2023-03-01']}
    df = pd.DataFrame(data)
    df.to_csv(CSV_FILE, index=False)
else:
    df = pd.read_csv(CSV_FILE)

# Define the app layout
ui.label('Weight Tracker')

# Table to display weights
ui.table(df, headings=['Date', 'Weight (lb)'])

# EChart for the line chart
ui.echart(df['Date'], df['Weight (lb)'], title='Weight Progress')

# Add a dashed goal line
ui.echart_line(x=['2023-01-01', '2023-03-01'], y=[GOAL_LB, GOAL_LB], style='dashed', color='red', name='Goal')

# Progress UI
ui.label('Progress towards goal: {} lb'.format(df['Weight (lb)'].iloc[-1]))

# Start the app
ui.run()