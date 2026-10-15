# app.py
"""
Daily Ops dashboard:
- Positions by risk group (TYPE) with toggle: discounted, non-discounted, both (side-by-side), or diff
- Simple deliveries table by selected Year/Month
- Interactive tables (sort/filter/paginate)
"""

from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd

from data_fetcher import RecOpsData
print("start loading data")
data_fetcher = RecOpsData()
data_fetcher.initialize_state()  # Load data on startup, with error handling as needed
print("done loading data")

#from make_bi import pos_dict, pos_nd

# --------------------------
# Build positions dataframe
# --------------------------
# Assumes pos_dict['voluntary'] and pos_nd['voluntary'] are DataFrames:
# index: TYPE (risk groups), columns: year numbers (e.g., 2024, 2025, ...)
print("starting calcs")
df_d = data_fetcher.pos_dict['voluntary'].reset_index().melt(
    id_vars='TYPE', var_name='YEAR', value_name='DELTA'
)
df_nd = data_fetcher.pos_nd['voluntary'].reset_index().melt(
    id_vars='TYPE', var_name='YEAR', value_name='DELTA_ND'
)
pos_df = df_d.merge(df_nd, on=['TYPE', 'YEAR'])
pos_df['YEAR'] = pos_df['YEAR'].astype(str)

# Years available for the positions view
year_options = sorted(data_fetcher.pos_df['YEAR'].unique(), key=lambda x: int(x))

# --------------------------
# Demo deliveries data + helper
# --------------------------
delivs_df = pd.DataFrame({
    'DMO': pd.to_datetime(['2026-01-01', '2026-02-01', '2026-03-01', '2026-04-01', '2026-05-01']),
    'DELIVERY': [100, 150, 200, 250, 300]
})
print("done with data init")

def get_rec_delivs(year, month):
    """Return deliveries for a given year & month as a DataFrame."""
    try:
        y = int(year)
        m = int(month)
    except Exception:
        return pd.DataFrame(columns=['DMO', 'DELIVERY'])

    filtered = delivs_df[
        (delivs_df['DMO'].dt.year == y) & (delivs_df['DMO'].dt.month == m)
    ].copy()
    return filtered

# --------------------------
# Table builder
# --------------------------
def make_table(df: pd.DataFrame, table_id: str):
    if df is None or df.empty:
        return html.Div('No rows')
    return dash_table.DataTable(
        id=table_id,
        columns=[{'name': str(c), 'id': str(c)} for c in df.columns],
        data=df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        page_size=20,
        style_table={'overflowX': 'auto'},
        style_cell={'padding': '6px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '12px', 'textAlign': 'right'},
        style_header={'backgroundColor': '#f2f2f2', 'fontWeight': '600', 'textAlign': 'center'},
    )

def build_position_views(selected_year: str):
    # Slice for the selected year
    fy = pos_df[pos_df['YEAR'] == str(selected_year)].copy()
    if fy.empty:
        # Keep column skeletons so DataTable renders headers
        return (
            pd.DataFrame(columns=['TYPE', 'Discounted']),
            pd.DataFrame(columns=['TYPE', 'Non-Discounted']),
            pd.DataFrame(columns=['TYPE', 'Diff (Disc - NonDisc)']),
        )

    fy['DIFF'] = fy['DELTA'] - fy['DELTA_ND']

    disc = fy[['TYPE', 'DELTA']].rename(columns={'DELTA': 'Discounted'}).sort_values('TYPE')
    nond = fy[['TYPE', 'DELTA_ND']].rename(columns={'DELTA_ND': 'Non-Discounted'}).sort_values('TYPE')
    diff = fy[['TYPE', 'DIFF']].rename(columns={'DIFF': 'Diff (Disc - NonDisc)'}).sort_values('TYPE')
    return disc, nond, diff

# --------------------------
# Dash app
# --------------------------
app = Dash(__name__)
app.title = "Daily Ops Dashboard"

app.layout = html.Div(
    [
        html.H2("Daily Operations Dashboard"),
        html.Div(
            [
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': y, 'value': y} for y in year_options],
                    value=year_options[0] if year_options else None,
                    placeholder='Year',
                    style={'minWidth': '120px'}
                ),
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': m, 'value': m} for m in range(1, 13)],
                    value=1,
                    placeholder='Month',
                    style={'minWidth': '120px'}
                ),
                dcc.RadioItems(
                    id='pos-view',
                    options=[
                        {'label': 'Discounted', 'value': 'disc'},
                        {'label': 'Non-Discounted', 'value': 'nond'},
                        {'label': 'Both (side-by-side)', 'value': 'both'},
                        {'label': 'Diff', 'value': 'diff'},
                    ],
                    value='both',
                    labelStyle={'marginRight': '16px'},
                    style={'display': 'flex', 'alignItems': 'center'}
                ),
            ],
            style={'display': 'flex', 'gap': '12px', 'alignItems': 'center', 'flexWrap': 'wrap', 'marginBottom': '12px'}
        ),

        html.Div(id='positions-output', style={'marginTop': '8px'}),
        html.Hr(),
        html.H4("Deliveries (by DMO)"),
        html.Div(id='delivs-output'),
    ],
    style={'padding': '16px'}
)

@app.callback(
    Output('positions-output', 'children'),
    Output('delivs-output', 'children'),
    Input('year-dropdown', 'value'),
    Input('month-dropdown', 'value'),
    Input('pos-view', 'value')
)
def update_outputs(year, month, view_mode):
    # Positions
    disc_df, nond_df, diff_df = build_position_views(year if year else '')
    pos_children = []

    if view_mode == 'disc':
        pos_children = [
            html.H4(f"Positions — Discounted ({year})"),
            make_table(disc_df, 'tbl-disc')
        ]
    elif view_mode == 'nond':
        pos_children = [
            html.H4(f"Positions — Non-Discounted ({year})"),
            make_table(nond_df, 'tbl-nond')
        ]
    elif view_mode == 'diff':
        pos_children = [
            html.H4(f"Positions — Diff (Discounted - Non-Discounted) ({year})"),
            make_table(diff_df, 'tbl-diff')
        ]
    else:  # both
        pos_children = [
            html.Div(
                [
                    html.Div([html.H4(f"Discounted ({year})"), make_table(disc_df, 'tbl-disc')], style={'flex': 1, 'minWidth': '320px'}),
                    html.Div([html.H4(f"Non-Discounted ({year})"), make_table(nond_df, 'tbl-nond')], style={'flex': 1, 'minWidth': '320px'}),
                ],
                style={'display': 'flex', 'gap': '16px', 'flexWrap': 'wrap'}
            )
        ]

    # Deliveries
    ddf = get_rec_delivs(year, month)
    delivs_children = html.Div(
        [
            html.Div(f"Selected: {year}-{str(month).zfill(2)}"),
            make_table(ddf.assign(DMO=ddf['DMO'].dt.strftime('%Y-%m-%d')) if not ddf.empty else ddf, 'tbl-delivs')
        ]
    )

    return pos_children, delivs_children


if __name__ == "__main__":
    app.run_server(debug=True, port=8000)