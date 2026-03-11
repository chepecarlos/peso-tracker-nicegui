import os
from datetime import date
import pandas as pd
from nicegui import ui

CSV_FILE = 'pesos.csv'

COLUMNS = [
    {'name': 'date', 'label': 'Date', 'field': 'date', 'sortable': True},
    {'name': 'weight', 'label': 'Weight (lb)', 'field': 'weight', 'sortable': True},
]


def load_data() -> pd.DataFrame:
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=['date', 'weight'])


def save_data(df: pd.DataFrame) -> None:
    df.to_csv(CSV_FILE, index=False)


def build_chart_options(df: pd.DataFrame) -> dict:
    sorted_df = df.sort_values('date')
    dates = sorted_df['date'].tolist()
    weights = sorted_df['weight'].tolist()
    return {
        'title': {'text': 'Weight Progress (lb)'},
        'tooltip': {'trigger': 'axis'},
        'xAxis': {
            'type': 'category',
            'data': dates,
            'axisLabel': {'rotate': 30},
        },
        'yAxis': {
            'type': 'value',
            'name': 'Weight (lb)',
            'scale': True,
        },
        'series': [
            {
                'name': 'Weight',
                'type': 'line',
                'data': weights,
                'smooth': True,
                'markPoint': {
                    'data': [
                        {'type': 'max', 'name': 'Max'},
                        {'type': 'min', 'name': 'Min'},
                    ],
                },
            }
        ],
    }


def main() -> None:
    df = load_data()

    with ui.column().classes('w-full max-w-3xl mx-auto p-4 gap-4'):
        ui.label('⚖️ Weight Tracker').classes('text-3xl font-bold self-center')

        # --- Input form ---
        with ui.card().classes('w-full'):
            ui.label('Add New Entry').classes('text-xl font-semibold')
            with ui.row().classes('w-full items-end gap-4'):
                date_input = ui.date_input(
                    label='Date',
                    value=str(date.today()),
                ).classes('flex-1')
                weight_input = ui.number(
                    label='Weight (lb)',
                    min=0,
                    precision=1,
                    format='%.1f',
                ).classes('flex-1')
                add_btn = ui.button('Add', icon='add')

        # --- Chart ---
        with ui.card().classes('w-full'):
            ui.label('Progress Chart').classes('text-xl font-semibold')
            chart = ui.echart(build_chart_options(df)).classes('w-full h-64')

        # --- Table ---
        with ui.card().classes('w-full'):
            ui.label('All Entries').classes('text-xl font-semibold')
            rows = df.sort_values('date', ascending=False).to_dict('records') if not df.empty else []
            table = ui.table(columns=COLUMNS, rows=rows, row_key='date').classes('w-full')

    def add_entry() -> None:
        nonlocal df
        raw_date = date_input.value
        raw_weight = weight_input.value

        if not raw_date or raw_weight is None:
            ui.notify('Please enter both a date and a weight.', type='warning')
            return

        try:
            entry_date = str(raw_date)
            entry_weight = float(raw_weight)
        except (ValueError, TypeError):
            ui.notify('Invalid date or weight value.', type='negative')
            return

        if entry_weight <= 0:
            ui.notify('Weight must be greater than 0.', type='warning')
            return

        new_row = pd.DataFrame([{'date': entry_date, 'weight': entry_weight}])
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)

        chart.options.clear()
        chart.options.update(build_chart_options(df))
        chart.update()

        table.rows = df.sort_values('date', ascending=False).to_dict('records')
        table.update()

        weight_input.value = None
        ui.notify(f'Added {entry_weight} lb on {entry_date}', type='positive')

    add_btn.on_click(add_entry)


main()
ui.run(title='Weight Tracker', reload=False)