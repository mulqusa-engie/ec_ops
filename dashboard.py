"""We are going to make a dashboard for daiily operations of the book aby adapting code and data stored in variables 
from ./make_bi including interactive tables
This will include:
-position for each risk group (toggle betwen discouunted, non discounted, 
and two tables- nondiscount discounted and diff discount and non discounted)"""

import dash
from dash import html, dcc, Input, Output
import dash_table
from ec_ops.make_bi import pos_dict, pos_nd
import pandas as pd

# make a dataframe for the voluntary position, with columns for year and type, and values for delta and delta_nd
df = pos_dict['voluntary'].reset_index().melt(id_vars='TYPE', var_name='YEAR', value_name='DELTA')
df_nd = pos_nd['voluntary'].reset_index().melt(id_vars='TYPE', var_name='YEAR', value_name='DELTA_ND')
df = df.merge(df_nd, on=['TYPE', 'YEAR'])   
df['YEAR'] = df['YEAR'].astype(str)
df['ym'] = pd.to_datetime(df['YEAR'] + '-01-01')

# make a dataframe for the delivs data, with columns for DMO and DELIVERY, and filter for DMO in 2026
delivs_df = pd.DataFrame({
    'DMO': ['2026-01-01', '2026-02-01', '2026-03-01', '2026-04-01', '2026-05-01'],
    'DELIVERY': [100, 150, 200, 250, 300]
})
delivs_df['DMO'] = pd.to_datetime(delivs_df['DMO'])

#
# make a function to get the delivs data for a given year and month, and return a dataframe with columns for DMO and DELIVERY
def get_rec_delivs(year, month):
    # in the real function, we would query the database for the delivs data for the given year and month
    # for now, we will just filter the delivs_df for the given year and month
    filtered_df = delivs_df[(delivs_df['DMO'].dt.year == int(year)) & (delivs_df['DMO'].dt.month == int(month))]
    return filtered_df
# make a function to convert a dataframe to a html table for display in dash
def df_to_table(dframe):
    if dframe is None or dframe.shape[0] == 0:
        return html.Div('No rows')
    # ensure all cell values and headers are plain Python strings to avoid
    # serialization issues with numpy/pandas types in Dash
    headers = [str(col) for col in dframe.columns]
    rows = []
    for i in range(len(dframe)):
        cells = []
        for col in dframe.columns:
            val = dframe.iloc[i][col]
            try:
                cells.append(html.Td(str(val)))
            except Exception:
                cells.append(html.Td(''))
        rows.append(html.Tr(cells))
    return html.Table([
        html.Thead(html.Tr([html.Th(h) for h in headers])),
        html.Tbody(rows)
    ])
# make a dash app with a dropdown for year and month, and a button to get the data, and a div to display the data
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Futures Delivery Data'),
    html.Div([
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(y), 'value': str(y)} for y in range(2020, 2030)],
            value='2026'
        ),
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': str(m), 'value': str(m)} for m in range(1, 13)],
            value='1'
        ),
        html.Button('Get Data', id='get-data-button', n_clicks=0),
    ], style={'display': 'flex', 'gap': '10px'}),
    html.Div(id='status'),
    html.Div(id='output-data')
])
# make a callback to update the output data when the button is clicked
@app.callback(
    Output('output-data', 'children'),
    Input('get-data-button', 'n_clicks'),
    Input('year-dropdown', 'value'),
    Input('month-dropdown', 'value')
)
def update_output(n_clicks, year, month):
    if n_clicks > 0:
        df = get_rec_delivs(year, month)
        return html.Div([
            html.H2(f'Delivs for {year}-{month}'),
            df_to_table(df)
        ])
    else:
        return html.Div('Click the button to get data')

# make a dash app with a dropdown for year and month, and a table to display the data
app = dash.Dash(__name__)
year_options = [{'label': str(y), 'value': str(y)} for y in sorted(df['YEAR'].unique())]
month_options = [{'label': str(m), 'value': str(m)} for m in range(1, 13)]
app.layout = html.Div([
    html.H1('Futures Delivery Data'),
    html.Div([
        dcc.Dropdown(
            id='year-dropdown',
            options=year_options,
            value=year_options[0]['value'] if year_options else None
        ),
        dcc.Dropdown(
            id='month-dropdown',
            options=month_options,
            value=month_options[0]['value'] if month_options else None
        ),
    ], style={'display': 'flex', 'gap': '10px'}),
    html.Div(id='status'),
    html.Div(id='output-data')
])
@app.callback(
    Output('output-data', 'children'),
    Input('year-dropdown', 'value'),
    Input('month-dropdown', 'value')
)
def update_output(year, month):
    if year and month:
        df = get_rec_delivs(year, month)
        return html.Div([
            html.H2(f'Delivs for {year}-{month}'),
            df_to_table(df)
        ])
    else:
        return html.Div('Select a year and month to get data')

# make a dash app with two tables, one for the discounted position and one for the non discounted position, and a dropdown to select the year and month for the data

# Dropdown options
month_options = [{"label": m, "value": m} for m in range(1, 13)]
years = sorted([int(y) for y in df["ym"].dropna().dt.year.unique()])
year_options = [{"label": y, "value": y} for y in years]
#in the the comment below write what is needed to finish above code (including any removing any duplicate code)
# We need to create a dash app with two tables, one for the discounted position and one for the non discounted position, and a dropdown to select the year and month for the data. We can use the get_rec_delivs function to get the data for the selected year and month, and then display it in the tables. We also need to make sure that we are not duplicating code for the dropdowns and the table display.
# We can create a single dropdown for year and month, and then use the selected values to filter the data for both tables. We can also create a single function to convert the dataframe to a html table, and use it for both tables. We can also add some styling to the tables to make them look better.
# We can also add some error handling to the get_rec_delivs function, in case there is an issue with the data retrieval. We can display an error message in the status div if there is an issue. We can also add a loading indicator while the data is being retrieved.
# Overall, we need to create a more cohesive and user-friendly dashboard that allows the user to easily select the year and month, and view the discounted and non discounted positions in a clear and organized manner. We also need to ensure that we are not duplicating code and that we are handling any potential errors gracefully.
# We can also add some additional features to the dashboard, such as the ability to download the data as a csv file, or to filter the data by other criteria such as type or mapping. We can also add some visualizations such as charts or graphs to help the user better understand the data. We can also add some interactivity to the tables, such as sorting and filtering options, to allow the user to explore the data in more depth. Overall, we want to create a comprehensive and user-friendly dashboard that provides valuable insights into the futures delivery data for daily operations.
# make a dash app with two tables, one for the discounted position and one for the non discounted position, and a dropdown to select the year and month for the data
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Futures Delivery Data'),
    html.Div([
        dcc.Dropdown(
            id='year-dropdown',
            options=year_options,
            value=year_options[0]['value'] if year_options else None
        ),
        dcc.Dropdown(
            id='month-dropdown',
            options=month_options,
            value=month_options[0]['value'] if month_options else None
        ),
    ], style={'display': 'flex', 'gap': '10px'}),
    html.Div(id='status'),
    html.Div(id='output-data')
])
@app.callback(
    Output('output-data', 'children'),
    Input('year-dropdown', 'value'),
    Input('month-dropdown', 'value')
    )
def update_output(year, month):
    if year and month:
        df = get_rec_delivs(year, month)
        return html.Div([
            html.H2(f'Delivs for {year}-{month}'),
            df_to_table(df)
        ])
    else:
        return html.Div('Select a year and month to get data')
#write the code belwo to finsih the above app, including any necessary imports and functions


