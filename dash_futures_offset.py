# app.py
from pathlib import Path
import pandas as pd

import dash
from dash import html, dcc
from dash import dash_table
from dash.dependencies import Input, Output
import pyodbc

DATA_PATH = Path("./data/futures")  # can be a file or a directory


def load_delivs():
    with open('./sql/deliv_excel.sql', 'r') as file:
        sql_delivs = file.read()
    conn_str_znet = (
        "DRIVER={Oracle in OraClient12Home1};"
        "DBQ=//pdal1orac02.d90.tes.local:1521/zainet;"
        "Uid=Tracread;"
        "Pwd=sungard;"
    )
    conn = pyodbc.connect(conn_str_znet)
    cursor = conn.cursor()
    cursor.execute(sql_delivs) 
    rows = cursor.fetchall()
    df = pd.DataFrame.from_records(rows, columns=[column[0] for column in cursor.description])
    cursor.close()
    conn.close()
    return df

def load_csv(path: Path) -> pd.DataFrame:
    if path.is_dir():
        csvs = sorted(path.glob("*.csv"))
        if not csvs:
            raise FileNotFoundError(f"No .csv files found in directory: {path.resolve()}")
        path = csvs[0]  # simplest: take first CSV
    if not path.exists():
        raise FileNotFoundError(f"CSV path not found: {path.resolve()}")

    df = pd.read_csv(path)

    if "ym" not in df.columns:
        raise ValueError("Expected column 'ym' in the CSV.")

    # Normalize ym to datetime (assumes ym is parseable, e.g. '2026-03-01' or similar)
    df["ym"] = pd.to_datetime(df["ym"], errors="coerce")
    return df

delivs_df = load_delivs()
delivs_df['DMO'] = pd.to_datetime(delivs_df['DMO'], errors='coerce')
df = load_csv(DATA_PATH)

# Dropdown options
month_options = [{"label": m, "value": m} for m in range(1, 13)]
years = sorted([int(y) for y in df["ym"].dropna().dt.year.unique()])
year_options = [{"label": y, "value": y} for y in years]

app = dash.Dash(__name__)
app.title = "Futures Viewer"

app.layout = html.Div(
    style={"maxWidth": "1200px", "margin": "24px auto", "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto"},
    children=[
        html.H2("All Data"),
        dash_table.DataTable(
            id="table-all",
            data=df.to_dict("records"),
            columns=[{"name": c, "id": c} for c in df.columns],
            page_size=20,
            sort_action="native",
            filter_action="native",
            style_table={"overflowX": "auto"},
        ),
        html.Hr(),
        html.Div(
            style={"display": "flex", "gap": "12px", "alignItems": "center", "flexWrap": "wrap"},
            children=[
                html.Div(
                    children=[
                        html.Label("Year"),
                        dcc.Dropdown(
                            id="dd-year",
                            options=year_options,
                            value=years[0] if years else None,
                            clearable=False,
                            style={"minWidth": "180px"},
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Label("Month"),
                        dcc.Dropdown(
                            id="dd-month",
                            options=month_options,
                            value=1,
                            clearable=False,
                            style={"minWidth": "180px"},
                        ),
                    ]
                ),
                html.Div(id="selected-date", style={"marginLeft": "8px"}),
            ],
        ),
        html.H2(style={"marginTop": "16px"}, children="Filtered Data (ym == first day of selected month)"),
        dash_table.DataTable(
            id="table-filtered",
            data=[],
            columns=[{"name": c, "id": c} for c in df.columns],
            page_size=20,
            sort_action="native",
            style_table={"overflowX": "auto"},
        ),
        #dash datatable for first 5 rows of delivs_df
        html.H2(style={"marginTop": "16px"}, children="Delivs Data (from SQL)"),
        dash_table.DataTable(
            id="zainet-filtered",
            data=[],
            columns=[{"name": c, "id": c} for c in delivs_df.columns],
            page_size=5,
            sort_action="native",
            style_table={"overflowX": "auto"},
        ),
    ],
)


@app.callback(
    Output("table-filtered", "data"),
    Output("zainet-filtered", "data"),
    Output("selected-date", "children"),
    Input("dd-year", "value"),
    Input("dd-month", "value"),
)
def update_filtered(year, month):
    if year is None or month is None:
        return [], ""

    target = pd.Timestamp(int(year), int(month), 1)
    dff = df[df["ym"] == target].copy()
    znet_filt = delivs_df[delivs_df['DMO']==target].copy()
    msg = f"Selected target date: {target.date()} — rows: {len(dff)}"
    return dff.to_dict("records"),znet_filt.to_dict("records"), msg


if __name__ == "__main__":
    app.run_server(debug=True) 

