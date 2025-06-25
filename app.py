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

with st.sidebar:
    st.header("Filtre")
    podnik = st.multiselect("Podnik", sorted(df["Podnik"].dropna().unique()))
    kategoria = st.multiselect("Kategoria", sorted(df["Kategoria"].dropna().unique()))
    funkcny  = st.multiselect("Funkčný", sorted(df["Funkčný"].dropna().unique()))
    skupina  = st.multiselect("Skupina", sorted(df["Skupina"].dropna().unique()))
    rok_uc   = st.multiselect("ROK_UC", sorted(df["ROK_UC"].dropna().unique()))
    pl2      = st.multiselect("PL2", sorted(df["PL2"].dropna().unique()))
    rok_from, rok_to = st.slider("ROK výroba",
                                 int(df["ROK_vyroba"].min()),
                                 int(df["ROK_vyroba"].max()),
                                 (int(df["ROK_vyroba"].min()), int(df["ROK_vyroba"].max())))
    mh_from, mh_to   = st.slider("Motohodiny",
                                 int(df["motohodiny"].min()),
                                 int(df["motohodiny"].max()),
                                 (int(df["motohodiny"].min()), int(df["motohodiny"].max())))
    size_max = st.slider("Maximálna veľkosť bublín", 10, 100, 40)

dff = df.copy()
if podnik:    dff = dff[dff["Podnik"].isin(podnik)]
if kategoria: dff = dff[dff["Kategoria"].isin(kategoria)]
if funkcny:   dff = dff[dff["Funkčný"].isin(funkcny)]
if skupina:   dff = dff[dff["Skupina"].isin(skupina)]
if rok_uc:    dff = dff[dff["ROK_UC"].isin(rok_uc)]
if pl2:       dff = dff[dff["PL2"].isin(pl2)]

dff = dff[(dff["ROK_vyroba"] >= rok_from) & (dff["ROK_vyroba"] <= rok_to)]
dff = dff[(dff["motohodiny"] >= mh_from) & (dff["motohodiny"] <= mh_to)]

grouped = (
    dff
    .groupby(["Popis","Podnik","ROK_vyroba","motohodiny"], as_index=False)
    .agg(EUR_sum=("EUR","sum"))
)

fig = px.scatter(
    grouped,
    x="ROK_vyroba", y="motohodiny",
    size=grouped["EUR_sum"].abs(),
    color="Podnik",
    hover_data=["Popis","EUR_sum"],
    size_max=size_max,
    title="Bublinový graf nákladov strojov"
)

st.plotly_chart(fig, use_container_width=True)
