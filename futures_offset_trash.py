
import sys
import pyodbc
import pandas as pd
import dash
from dash import html



def get_rec_delivs():
    with open('./sql/deliv_excel.sql', 'r') as file:
        sql_query = file.read()
    conn_str = (
        "DRIVER={Oracle in OraClient12Home1};"
        "DBQ=//pdal1orac02.d90.tes.local:1521/pdal1orac02;"
        "Uid=Tracread;"
        "Pwd=sungard;"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    df = pd.DataFrame.from_records(rows, columns=[column[0] for column in cursor.description])
    cursor.close()
    conn.close()
    return df

def df_to_table(dframe):
    """Convert a pandas DataFrame to a Dash html.Table safely (stringify values)."""
    if dframe is None or dframe.shape[0] == 0:
        return html.Div('No rows')
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


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Label('Year'),
    html.Select(
        id='year-picker',
        children=[
            html.Option(str(year), value=str(year), selected=(str(year) == '2026'))
            for year in range(2020, 2031)
        ]
    ),
    html.Label('Month'),
    html.Select(
        id='month-picker',
        children=[
            html.Option(str(month), value=str(month), selected=(str(month) == '1'))
            for month in range(1, 13)
        ]
    ),
    html.Button('Get Data', id='get-data-button', n_clicks=0),
        html.Div(id='status'),
        html.Div(id='output')
])

# Run initial data load (caught) and keep a cached dataframe for callbacks
try:
    cached_df = get_rec_delivs('2022', '1')
    init_error = None
except Exception as _e:
    cached_df = pd.DataFrame()
    init_error = str(_e)

# make a picker for year and month using html select, with options for year 2020-2030 and month 1-12
app.layout = html.Div([
    html.Label('Year'),
    html.Select(
        id='year-picker',
        children=[html.Option(str(year), value=str(year), selected=(str(year) == '2022')) for year in range(2020, 2031)]
    ),
    html.Label('Month'),
    html.Select(
        id='month-picker',
        children=[html.Option(str(month), value=str(month), selected=(str(month) == '1')) for month in range(1, 13)]
    ),
    html.Button('Get Data', id='get-data-button', n_clicks=0),
    html.Div(id='status'),
    html.H5('Initial data (head)'),
    df_to_table(cached_df.head()),
    html.Br(),
    html.Div(id='output')
])

def update_output(n_clicks, year, month):
    if n_clicks > 0:
        df = get_rec_delivs(year, month)
        # show the head of the dataframe regardless of filter
        head_df = df.head()

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

        # filtered data: DMO equals first of month
        try:
            m_int = int(month)
        except Exception:
            m_int = int(str(month)) if month is not None else 1
        filt = (df['DMO'] == f"{year}-{m_int:02d}-01")
        filtered_df = df[filt]

        return html.Div([
            html.H4(f'Data for Year: {year} Month: {month}'),
            html.H5('Top rows (head)'),
            df_to_table(head_df),
            html.Br(), html.Br(), html.Br(),
            html.H5('Filtered rows (DMO on first of month)'),
            df_to_table(filtered_df)
        ])
    else:
        return 'Select a year and month and click the button to get data.'


# clientside callback to immediately show running status when button is clicked
app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0) {
            return 'Query running...';
        }
        return '';
    }
    """,
    dash.dependencies.Output('status', 'children'),
    [dash.dependencies.Input('get-data-button', 'n_clicks')]
)
    # once user calls "Get Data", add a string saying pulling data



if __name__ == '__main__':
    app.run_server(debug=True)
