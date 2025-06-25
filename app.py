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

# Prepare sorted lists
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

    # Replace sliders with number_input for Typing values
    min_rok = int(df["ROK_vyroba"].min())
    max_rok = int(df["ROK_vyroba"].max())
    rok_from = st.number_input("Rok výroba od", min_value=min_rok, max_value=max_rok, value=min_rok, step=1)
    rok_to   = st.number_input("Rok výroba do", min_value=min_rok, max_value=max_rok, value=max_rok, step=1)

    min_mh = int(df["motohodiny"].min())
    max_mh = int(df["motohodiny"].max())
    mh_from = st.number_input("Motohodiny od", min_value=min_mh, max_value=max_mh, value=min_mh, step=1)
    mh_to   = st.number_input("Motohodiny do", min_value=min_mh, max_value=max_mh, value=max_mh, step=1)

    size_max = st.slider("Maximálna veľkosť bublín", 10, 100, 40)

# Apply filters
dff = df.copy()
if podnik:    dff = dff[dff["Podnik"].isin(podnik)]
if kategoria: dff = dff[dff["Kategoria"].isin(kategoria)]
if funkcny:   dff = dff[dff["Funkčný"].isin(funkcny)]
if skupina:   dff = dff[dff["Skupina"].isin(skupina)]
if rok_uc:    dff = dff[dff["ROK_UC"].isin(rok_uc)]
if pl2:       dff = dff[dff["PL2"].isin(pl2)]
dff = dff[(dff["ROK_vyroba"] >= rok_from) & (dff["ROK_vyroba"] <= rok_to)]
dff = dff[(dff["motohodiny"] >= mh_from) & (dff["motohodiny"] <= mh_to)]

# Aggregate data
grouped = (
    dff
    .groupby(["Popis","Podnik","ROK_vyroba","motohodiny"], as_index=False)
    .agg(EUR_sum=("EUR","sum"))
)

# Plot
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
fig.update_layout(xaxis_title="Rok výroba", yaxis_title="Motohodiny")

st.plotly_chart(fig, use_container_width=True)
