import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Načítanie dát
df = pd.read_excel('Opravy strojov.xlsx', sheet_name='DATA_PY')

# Konverzia typov a premenovanie
df['ROK_výroba'] = pd.to_numeric(df['ROK_výroba'], errors='coerce')
df['mth'] = pd.to_numeric(df['mth'], errors='coerce')
df.rename(columns={'mth': 'motohodiny'}, inplace=True)

# Inicializácia aplikácie
app = Dash(__name__)

# Layout
app.layout = html.Div([
    # Filtre
    html.Div([
        html.Div([
            html.Label('Podnik'),
            dcc.Dropdown(
                id='podnik-dropdown',
                options=[{'label': i, 'value': i} for i in sorted(df['Podnik'].dropna().unique(), key=lambda x: str(x))],
                multi=True,
                placeholder='Vyber...'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '5px'}),
        html.Div([
            html.Label('Kategoria'),
            dcc.Dropdown(
                id='kategoria-dropdown',
                options=[{'label': i, 'value': i} for i in sorted(df['Kategoria'].dropna().unique(), key=lambda x: str(x))],
                multi=True,
                placeholder='Vyber...'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '5px'}),
        html.Div([
            html.Label('Funkčný'),
            dcc.Dropdown(
                id='funkcny-dropdown',
                options=[{'label': i, 'value': i} for i in sorted(df['Funkčný'].dropna().unique(), key=lambda x: str(x))],
                multi=True,
                placeholder='Vyber...'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '5px'}),
        html.Div([
            html.Label('Skupina'),
            dcc.Dropdown(
                id='skupina-dropdown',
                options=[{'label': i, 'value': i} for i in sorted(df['Skupina'].dropna().unique(), key=lambda x: str(x))],
                multi=True,
                placeholder='Vyber...'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '5px'}),
        html.Div([
            html.Label('ROK_UC'),
            dcc.Dropdown(
                id='rok_uc-dropdown',
                options=[{'label': i, 'value': i} for i in sorted(df['ROK_UC'].dropna().unique(), key=lambda x: str(x))],
                multi=True,
                placeholder='Vyber...'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '5px'}),
        html.Div([
            html.Label('PL2'),
            dcc.Dropdown(
                id='pl2-dropdown',
                options=[{'label': i, 'value': i} for i in sorted(df['PL2'].dropna().unique(), key=lambda x: str(x))],
                multi=True,
                placeholder='Vyber...'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '5px'}),
    ], style={'borderBottom': 'thin lightgrey solid', 'padding': '10px'}),

    # Rozsahy pre rok výroby a motohodiny
    html.Div([
        html.Div([
            html.Label('ROK_výroba od'),
            dcc.Input(id='rok-vyroba-from', type='number', placeholder='Min', style={'width': '100%'})
        ], style={'width': '15%', 'display': 'inline-block', 'padding': '5px'}),
        html.Div([
            html.Label('ROK_výroba do'),
            dcc.Input(id='rok-vyroba-to', type='number', placeholder='Max', style={'width': '100%'})
        ], style={'width': '15%', 'display': 'inline-block', 'padding': '5px'}),
        html.Div([
            html.Label('Motohodiny od'),
            dcc.Input(id='motohodiny-from', type='number', placeholder='Min', style={'width': '100%'})
        ], style={'width': '15%', 'display': 'inline-block', 'padding': '5px'}),
        html.Div([
            html.Label('Motohodiny do'),
            dcc.Input(id='motohodiny-to', type='number', placeholder='Max', style={'width': '100%'})
        ], style={'width': '15%', 'display': 'inline-block', 'padding': '5px'}),
    ], style={'borderBottom': 'thin lightgrey solid', 'padding': '10px'}),

    # Slider pre nastavovanie veľkosti bublín
    html.Div([
        html.Label('Nastavenie maximálnej veľkosti bublín'),
        dcc.Slider(
            id='size-max-slider',
            min=10,
            max=100,
            step=5,
            value=40,
            marks={i: str(i) for i in range(10, 101, 10)}
        )
    ], style={'width': '50%', 'padding': '10px'}),

    # Graf
    dcc.Graph(id='bubble-graph')
])

@app.callback(
    Output('bubble-graph', 'figure'),
    Input('podnik-dropdown', 'value'),
    Input('kategoria-dropdown', 'value'),
    Input('funkcny-dropdown', 'value'),
    Input('skupina-dropdown', 'value'),
    Input('rok_uc-dropdown', 'value'),
    Input('pl2-dropdown', 'value'),
    Input('rok-vyroba-from', 'value'),
    Input('rok-vyroba-to', 'value'),
    Input('motohodiny-from', 'value'),
    Input('motohodiny-to', 'value'),
    Input('size-max-slider', 'value'),
)
def update_graph(podnik, kategoria, funkcny, skupina, rok_uc, pl2,
                 rok_from, rok_to, moto_from, moto_to, size_max):
    dff = df.copy()
    if podnik:
        dff = dff[dff['Podnik'].isin(podnik)]
    if kategoria:
        dff = dff[dff['Kategoria'].isin(kategoria)]
    if funkcny:
        dff = dff[dff['Funkčný'].isin(funkcny)]
    if skupina:
        dff = dff[dff['Skupina'].isin(skupina)]
    if rok_uc:
        dff = dff[dff['ROK_UC'].isin(rok_uc)]
    if pl2:
        dff = dff[dff['PL2'].isin(pl2)]
    if rok_from is not None:
        dff = dff[dff['ROK_výroba'] >= rok_from]
    if rok_to is not None:
        dff = dff[dff['ROK_výroba'] <= rok_to]
    if moto_from is not None:
        dff = dff[dff['motohodiny'] >= moto_from]
    if moto_to is not None:
        dff = dff[dff['motohodiny'] <= moto_to]

    grouped = (
        dff.groupby(['Popis', 'Podnik', 'ROK_výroba', 'motohodiny'], as_index=False)
           .agg(
               EUR_sum=('EUR', 'sum'),
               ROK_UC_list=('ROK_UC', lambda x: ','.join(sorted(map(str, x.unique())))),
               PL2_list=('PL2', lambda x: ','.join(sorted(x.unique(), key=str)))
           )
    )
    if grouped.empty:
        return px.scatter()

    # Absolútne hodnoty pre veľkosť
    grouped['EUR_abs'] = grouped['EUR_sum'].abs()

    # Vytvorenie grafu s nastavením size_max podľa slidera
    fig = px.scatter(
        grouped,
        x='ROK_výroba',
        y='motohodiny',
        size='EUR_abs',
        color='Podnik',
        custom_data=['Popis', 'Podnik', 'EUR_sum', 'ROK_UC_list', 'PL2_list'],
        size_max=size_max
    )
    fig.update_traces(
        hovertemplate=(
            'Popis: %{customdata[0]}<br>'
            'Podnik: %{customdata[1]}<br>'
            'EUR (súčet): %{customdata[2]:,.0f}<br>'
            'ROK_UC: %{customdata[3]}<br>'
            'PL2: %{customdata[4]}<br>'
            'Rok výroba: %{x}<br>'
            'Motohodiny: %{y}<extra></extra>'
        )
    )
    fig.update_layout(
        title='Bublinový graf nákladov strojov',
        xaxis_title='Rok výroba',
        yaxis_title='Motohodiny',
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

if __name__ == '__main__':
    app.run()
