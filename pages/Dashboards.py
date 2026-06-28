import streamlit as st

st.set_page_config(page_title="My Dashboard", layout="wide")

# Define pages for navigation
pages = {
    "Overview": [
        st.Page("pages/Home.py", title="Home"),
    ],
    "Analytics": [
        st.Page("pages/1_Barra.py", title="Barras"),
        st.Page("pages/2_Bola.py", title="Bola"),
        st.Page("pages/3_Bigode.py", title="Bigodes"),
        st.Page("pages/4_Pontos.py", title="Pontos"),
        st.Page("pages/5_Quadrado.py", title="Quadrados"),
        st.Page("pages/6_Mapa.py", title="Mapa"),
        st.Page("pages/7_Tabela.py", title="Tabela"),
    ]
}

pg = st.navigation(pages)
pg.run()