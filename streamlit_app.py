import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Nuestra Agenda", page_icon="☁️")
st.title("☁️ Espacio Compartido")

# conexión
conn = st.connection("gsheets", type=GSheetsConnection)

# nombre de la hoja de Google Sheets
WORKSHEET = "Hoja1"


def cargar_datos():
    try:
        data = conn.read(worksheet=WORKSHEET)
        if data is None or data.empty:
            data = pd.DataFrame(columns=["Título","Fecha","Hora","Descripción","Nota"])
        return data
    except:
        return pd.DataFrame(columns=["Título","Fecha","Hora","Descripción","Nota"])


tab1, tab2 = st.tabs(["📅 Agenda", "📝 Blog"])


# -------- AGENDA --------
with tab1:
    st.subheader("Nuevo Evento")

    with st.form("evento_form"):
        titulo = st.text_input("Título")
        fecha = st.date_input("Fecha")
        hora = st.time_input("Hora")
        desc = st.text_area("Descripción")
        submit = st.form_submit_button("Registrar Evento")

    if submit:
        df_nuevo = pd.DataFrame([{
            "Título": titulo,
            "Fecha": str(fecha),
            "Hora": str(hora),
            "Descripción": desc,
            "Nota": ""
        }])

        existing_data = cargar_datos()
        updated_df = pd.concat([existing_data, df_nuevo], ignore_index=True)

        conn.update(worksheet=WORKSHEET, data=updated_df)

        st.success("Evento guardado ✔")
        st.rerun()


# -------- BLOG / NOTAS --------
with tab2:
    st.subheader("Notas")

    nota = st.text_input("Escribe una nota...")

    if st.button("Enviar"):
        df_nota = pd.DataFrame([{
            "Título": "",
            "Fecha": "",
            "Hora": "",
            "Descripción": "",
            "Nota": nota
        }])

        existing_data = cargar_datos()
        updated_df = pd.concat([existing_data, df_nota], ignore_index=True)

        conn.update(worksheet=WORKSHEET, data=updated_df)

        st.success("Nota guardada ✔")
        st.rerun()


st.divider()
st.subheader("Eventos y Notas")

data = cargar_datos()
st.dataframe(data)
