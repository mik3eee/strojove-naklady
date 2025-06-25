import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Bublinový graf strojov", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("Opravy strojov.xlsx", sheet_name="DATA_PY")
    df["ROK_vyroba"] = pd.to_numeric(df["ROK_výroba"], errors="coerce")
    df["motohodiny"] = pd.to_numeric(df["mth"], errors="coerce")
    return df

df = load_data()

# Vytvoríme si predvolené zoznamy pre multiselect, zoradené ako string
podnik_list    = sorted(df["Podnik"].dropna().unique(), key=lambda x: str(x))
kategoria_list = sorted(df["Kategoria"].dropna().unique(), key=lambda x: str(x))
funkcny_list   = sorted(df["Funkčný"].dropna().unique(), key=lambda x: str(x))
skupina_list   = sorted(df["Skupina"].dropna().unique(), key=lambda x: str(x))
rok_uc_list    = sorted(df["ROK_UC"].dropna().unique(), key=lambda x: str(x))
pl2_list       = sorted(df["PL2"].dropna().unique(), key=lambda x: str(x))

with st.sidebar:
    st.header("Filtre")
    podnik    = st.multiselect("Podnik", podnik_list)
    kategoria = st.multiselect("Kategoria", kategoria_list)
    funkcny   = st.multiselect("Funkčný", funkcny_list)
    skupina   = st.multiselect("Skupina", skupina_list)
    rok_uc    = st.multiselect("ROK_UC", rok_uc_list)
    pl2       = st.multiselect("PL2", pl2_list)

    rok_from, rok_to = st.slider(
        "ROK výroba",
        int(df["ROK_vyroba"].min()),
        int(df["ROK_vyroba"].max()),
        (int(df["ROK_vyroba"].min()), int(df["ROK_vyroba"].max()))
    )
    mh_from, mh_to = st.slider(
        "Motohodiny",
        int(df["motohodiny"].min()),
        int(df["motohodiny"].max()),
        (int(df["motohodiny"].min()), int(df["motohodiny"].max()))
    )
    size_max = st.slider("Maximálna veľkosť bublín", 10, 100, 40)

# Aplikácia filtrov
dff = df.copy()
if podnik:    dff = dff[dff["Podnik"].isin(podnik)]
if kategoria: dff = dff[dff["Kategoria"].isin(kategoria)]
if funkcny:   dff = dff[dff["Funkčný"].isin(funkcny)]
if skupina:   dff = dff[dff["Skupina"].isin(skupina)]
if rok_uc:    dff = dff[dff["ROK_UC"].isin(rok_uc)]
if pl2:       dff = dff[dff["PL2"].isin(pl2)]
dff = dff[(dff["ROK_vyroba"] >= rok_from) & (dff["ROK_vyroba"] <= rok_to)]
dff = dff[(dff["motohodiny"] >= mh_from) & (dff["motohodiny"] <= mh_to)]

# Agregácia dát
grouped = (
    dff
    .groupby(["Popis","Podnik","ROK_vyroba","motohodiny"], as_index=False)
    .agg(EUR_sum=("EUR","sum"))
)

# Vykreslenie bublinového grafu
fig = px.scatter(
    grouped,
    x="ROK_vyroba",
    y="motohodiny",
    size=grouped["EUR_sum"].abs(),
    color="Podnik",
    hover_data=["Popis","EUR_sum","ROK_vyroba","motohodiny"],
    size_max=size_max,
    title="Bublinový graf nákladov strojov"
)
fig.update_layout(
    xaxis_title="Rok výroba",
    yaxis_title="Motohodiny"
)

st.plotly_chart(fig, use_container_width=True)
