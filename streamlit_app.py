import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Nuestra Agenda", page_icon="☁️")
st.title("☁️ Espacio Compartido")

conn = st.connection("gsheets", type=GSheetsConnection)

# nombre de la hoja dentro del Google Sheet
WORKSHEET = "Agenda"

tab1, tab2 = st.tabs(["📅 Agenda", "📝 Blog"])

def cargar_datos():
    data = conn.read(worksheet=WORKSHEET)
    if data is None or data.empty:
        data = pd.DataFrame(columns=["Título","Fecha","Hora","Descripción","Nota"])
    return data

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
        st.success("¡Evento guardado!")
        st.cache_data.clear()

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
        st.success("Nota guardada")
        st.cache_data.clear()

st.divider()
st.subheader("Próximos Eventos y Notas")

try:
    data = cargar_datos()
    st.dataframe(data)
except:
    st.info("Todavía no hay datos.")
