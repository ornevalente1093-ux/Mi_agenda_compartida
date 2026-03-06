import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Nuestra Agenda", layout="centered")

# Conexión con tu planilla
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("☁️ Espacio Compartido")

tab1, tab2 = st.tabs(["📅 Agenda", "📝 Blog"])

with tab1:
    st.subheader("Nuevo Evento")
    with st.form("agenda_form", clear_on_submit=True):
        t = st.text_input("Título")
        f = st.date_input("Fecha", datetime.now())
        h = st.time_input("Hora", datetime.now())
        d = st.text_area("Descripción")
        if st.form_submit_button("Guardar"):
            df_actual = conn.read()
            nueva = pd.DataFrame([{"fecha": str(f), "hora": str(h), "titulo": t, "descripcion": d, "tipo": "agenda"}])
            df_final = pd.concat([df_actual, nueva], ignore_index=True)
            conn.update(data=df_final)
            st.success("¡Guardado!")

with tab2:
    st.subheader("Notas")
    nota = st.chat_input("Escribe una nota...")
    if nota:
        df_actual = conn.read()
        nueva_n = pd.DataFrame([{"fecha": datetime.now().strftime("%d/%m/%Y"), "hora": datetime.now().strftime("%H:%M"), "titulo": "Nota", "descripcion": nota, "tipo": "blog"}])
        df_final = pd.concat([df_actual, nueva_n], ignore_index=True)
        conn.update(data=df_final)
        st.info("Nota enviada")

st.write("---")
st.subheader("Historial")
try:
    df = conn.read()
    if not df.empty:
        for i, row in df.iloc[::-1].iterrows():
            st.write(f"**{row['fecha']}** - {row['titulo']}")
            st.caption(row['descripcion'])
except:
    st.write("Todavía no hay nada anotado.")
