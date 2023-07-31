import streamlit as st
import myauthenticator as stauth
import sqlfunctions
import pandas as pd
from Inserisci_Spese import formRegistrazione, authenticator
#from st_aggrid import AgGrid, GridUpdateMode
#from st_aggrid.grid_options_builder import GridOptionsBuilder

# initialize session state
if 'config' not in st.session_state:
    config = sqlfunctions.getconfigfromsql()
    st.session_state['config'] = config
else:
    config = st.session_state['config']

if 'register_expanded' not in st.session_state:
    st.session_state['register_expanded'] = False

if 'show_register_success' not in st.session_state:
    st.session_state['show_register_success'] = False


# with open('./users.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)


if st.session_state['authentication_status']:
    data = {
        'data': ['2023-07-30', '2023-07-31', '2023-08-01'],
        'nome': ['Mario', 'Luigi', 'Luca'],
        'importo': [100, 200, 50],
        'categoria': ['Alimentari', 'Elettronica', 'Abbigliamento'],
        'sottocategoria': ['Frutta', 'Smartphone', 'Magliette'],
        'note': ['', 'Nessuna nota', 'Promozione']
    }

    df = pd.DataFrame(data)
    df['Seleziona'] = [False] * len(df)

    st.title('Web App con Streamlit')
    edited_df = st.data_editor(df)
    # Verifica se il pulsante "Cancella" è stato premuto e rimuovi le righe selezionate
    if st.button('Cancella'):
        if (edited_df['Seleziona']==True).any():
            # Ottieni gli indici delle righe selezionate
            selected_indices = edited_df[edited_df['Seleziona']].index
            # Rimuovi le righe selezionate dal DataFrame
            df.drop(selected_indices, inplace=True)
            # Mostra un messaggio di successo dopo l'eliminazione delle righe
            st.success('Righe eliminate con successo!')

    # Mostra il DataFrame dopo l'eliminazione delle righe
    st.subheader('DataFrame dopo l\'eliminazione')
    st.dataframe(df)


    authenticator.logout('Logout','sidebar')
else:
    if st.session_state['show_register_success']:
        st.success('Utente registrato con successo. Effettua il login')
        st.session_state['show_register_success'] = False
        st.session_state['authentication_status'] = None
    name, authentication_status, username = authenticator.login('Login','main')
    if authentication_status==False:
        st.error('Email o password non corretti')
        formRegistrazione()
    elif authentication_status==None:
        formRegistrazione()

st.write(st.session_state)
