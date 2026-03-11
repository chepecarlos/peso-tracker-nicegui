from nicegui import ui

# Demo data
weight_data = [
    {'date': '2026-01-01', 'weight': 70},
    {'date': '2026-01-15', 'weight': 68},
    {'date': '2026-01-31', 'weight': 66},
]

# Goal configuration
goal_weight = 65

# Function to calculate goal progress
def calculate_progress(current_weight):
    return ((goal_weight - current_weight) / (goal_weight - weight_data[0]['weight'])) * 100

# UI setup
ui.label('Peso Tracker').style('font-size: 24px;')
ui.table(weight_data)

# Display progress
for entry in weight_data:
    ui.label(f"Date: {entry['date']}, Weight: {entry['weight']} kg, Progress: {calculate_progress(entry['weight']):.2f}%")

ui.run()