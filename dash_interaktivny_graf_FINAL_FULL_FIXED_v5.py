
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Načítanie dát
excel_path = "Opravy strojov.xlsx"
df = pd.read_excel(excel_path, sheet_name="DATA_PY")

# Pretypovanie číselných stĺpcov
df["ROK_výroba"] = pd.to_numeric(df["ROK_výroba"], errors="coerce")
df["mth"] = pd.to_numeric(df["mth"], errors="coerce")
df["ROK_UC"] = pd.to_numeric(df["ROK_UC"], errors="coerce")
df["EUR"] = pd.to_numeric(df["EUR"], errors="coerce")

# Premenovanie stĺpca pre názov stroja
df = df.rename(columns={"Popis": "Stroj"})

# Odstránenie záznamov so zápornými hodnotami EUR
# df = df[df["EUR"] >= 0]  # Záznamy so zápornými hodnotami EUR sú teraz zachované

# Inicializácia Dash aplikácie
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Interaktívna analýza nákladov na stroje"),

    html.Div([
        html.Label("Podnik"),
        dcc.Dropdown(
            options=[{"label": x, "value": x} for x in sorted(df["Podnik"].dropna().unique())],
            multi=True,
            id="filter_podnik"
        ),
    ]),

    html.Div([
        html.Label("Kategória"),
        dcc.Dropdown(
            options=[{"label": x, "value": x} for x in sorted(df["Kategoria"].dropna().unique())],
            multi=True,
            id="filter_kategoria"
        ),
    ]),

    html.Div([
        html.Label("Funkčný"),
        dcc.Dropdown(
            options=[{"label": str(x), "value": x} for x in sorted(df["Funkčný"].dropna().unique(), key=str)],
            multi=True,
            id="filter_funkcny"
        ),
    ]),

    html.Div([
        html.Label("Skupina"),
        dcc.Dropdown(
            options=[{"label": str(x), "value": x} for x in sorted(df["Skupina"].dropna().unique(), key=str)],
            multi=True,
            id="filter_skupina"
        ),
    ]),

    html.Div([
        html.Label("Rok účtovania"),
        dcc.Dropdown(
            options=[{"label": str(x), "value": x} for x in sorted(df["ROK_UC"].dropna().unique())],
            multi=True,
            id="filter_rok_uc"
        ),
    ]),

    html.Div([
        html.Label("Typ nákladu (PL2)"),
        dcc.Dropdown(
            options=[{"label": x, "value": x} for x in sorted(df["PL2"].dropna().unique())],
            multi=True,
            id="filter_pl2"
        ),
    ]),

    html.Div([
        html.Label("Rozsah ROK_výroba"),
        dcc.Input(id='rok_vyroba_min', type='number', placeholder='Min'),
        dcc.Input(id='rok_vyroba_max', type='number', placeholder='Max'),
    ], style={"margin-top": "10px"}),

    html.Div([
        html.Label("Rozsah MTH"),
        dcc.Input(id='mth_min', type='number', placeholder='Min'),
        dcc.Input(id='mth_max', type='number', placeholder='Max'),
    ], style={"margin-top": "10px"}),

    dcc.Graph(id="bubble_chart")
])

@app.callback(
    Output("bubble_chart", "figure"),
    Input("filter_podnik", "value"),
    Input("filter_kategoria", "value"),
    Input("filter_funkcny", "value"),
    Input("filter_skupina", "value"),
    Input("filter_rok_uc", "value"),
    Input("filter_pl2", "value"),
    Input("rok_vyroba_min", "value"),
    Input("rok_vyroba_max", "value"),
    Input("mth_min", "value"),
    Input("mth_max", "value"),
)
def update_chart(podnik, kategoria, funkcny, skupina, rok_uc, pl2, rok_min, rok_max, mth_min, mth_max):
    dff = df.copy()

    if podnik:
        dff = dff[dff["Podnik"].isin(podnik)]
    if kategoria:
        dff = dff[dff["Kategoria"].isin(kategoria)]
    if funkcny:
        dff = dff[dff["Funkčný"].isin(funkcny)]
    if skupina:
        dff = dff[dff["Skupina"].astype(str).isin([str(s) for s in skupina])]
    if rok_uc:
        dff = dff[dff["ROK_UC"].isin(rok_uc)]
    if pl2:
        dff = dff[dff["PL2"].isin(pl2)]
    if rok_min is not None:
        dff = dff[dff["ROK_výroba"] >= rok_min]
    if rok_max is not None:
        dff = dff[dff["ROK_výroba"] <= rok_max]
    if mth_min is not None:
        dff = dff[dff["mth"] >= mth_min]
    if mth_max is not None:
        dff = dff[dff["mth"] <= mth_max]

    agg_df = dff.groupby(["Stroj", "ROK_výroba", "mth", "Podnik", "Kategoria", "Funkčný", "Skupina"])["EUR"].sum().reset_index()

    fig = px.scatter(
        agg_df,
        x="ROK_výroba",
        y="mth",
        size="EUR",
        color="Podnik",
        hover_name="Stroj",
        size_max=60,
        title="Bublinový graf nákladov strojov"
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True)
