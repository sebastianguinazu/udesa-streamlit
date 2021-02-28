import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

def main():
    # df, eval = load_datasets()
    df = load_datasets()
    st.sidebar.header('Elija el monitor')
    page = st.sidebar.selectbox("Choose a page", ["Homepage", "Users", "Uso de la API", "Longitud de los mails"])

    if page == "Homepage":
    	st.title("💻 Monitoreo de la API")
    	st.markdown("> Para uso interno")
    	st.markdown("En este dashboard se pueden monitorear varios aspectos del uso de la API")
    	st.markdown("En el menu de la izquierda puede seleccionar los monitores disponibles")
    	st.markdown("### **Detalle de los monitores**")
    	st.markdown("* 🧑 **Users:** muestra informacion del usuario")
    	st.markdown("* 📈 **Uso de la API:** muestra la evolucion en el uso de la API")
    	st.markdown("* ✉️ **Longitud de los mails:** muestra el detalle de la longitud de los mails")

    elif page == "Users":
        st.title("Users de la API")
        # show_eval()
        st.sidebar.header('Elija el user')
        user = st.sidebar.selectbox("Choose user", df['user'].unique())

    elif page == "Uso de la API":
        st.title("Evolucion mensual de los mails consultados")
        # show_eval()
        app_start = datetime.date(2021,2,1)
        today = datetime.date.today()
        start_date = st.date_input('Start date', app_start)
        end_date = st.date_input('End date', today)
        if st.button('Mostrar'):
            # filtro el dataset
            dfperiod = df.loc[(df['date'] >= np.datetime64(start_date)) & (df['date'] <= np.datetime64(end_date))]
            dfcons = dfperiod['datetime'].value_counts()
            # st.write(dfperiod.head())
            st.markdown("En el siguiente grafico se puede observar la evolucion mensual de consultas")
            st.line_chart(dfcons)

    elif page == "Longitud de los mails":
        st.title("Longitud de los mails consultados")
        st.markdown("En el siguiente grafico se muestra un histograma de la longitud de los mails consultados")
        st.bar_chart(df['lenght'].value_counts())



@st.cache(show_spinner=False)
def load_datasets():
    # esto de abajo crea el df emails. Seria ideal que se pueda explicitar
    import requests
    import json
    import pandas as pd

    HOST = 'http://18.189.252.248/'
    USERNAME = 'rankeros'
    PASSWORD = 'rankeros123'

    #### USERNAME
    data_login = {'username': USERNAME, 'password':PASSWORD}
    response = requests.post(HOST+'api-token-auth',data_login)
    token = json.loads(response.content.decode('utf-8'))['token']
    headers = { 'Authorization': f'Token {token}' }

    #### DASHBOARDS

    # emails
    res = requests.get(HOST+'emails_dashboard/',headers=headers)

    emails = pd.read_json(res.content)

    # time vars
    emails['date'] = pd.to_datetime(emails['created'].str.slice(start=0, stop=10), format='%Y-%m-%d')
    emails['datetime'] = [x.to_pydatetime() for x in emails['date']]
    emails['hour'] = emails['created'].str.slice(start=11, stop=13)
    emails['lenght'] = emails['text'].str.len()
    # df['periodo'] =  pd.to_datetime(df['fecha'], format='%d/%m/%Y')
    # eval = df[['periodo', 'mail']].groupby(['periodo']).agg(['count'])
    # eval.columns = ['cantidad']
    # return df, eval
    return emails

def show_eval():
    st.line_chart(eval['cantidad'])

if __name__ == "__main__":
    main()
