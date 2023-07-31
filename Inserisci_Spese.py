import streamlit as st
import myauthenticator as stauth
import sqlfunctions
import pandas as pd
from sqlalchemy import create_engine
#import yaml
#from yaml import SafeLoader


def formRegistrazione():
    with st.expander('Nuovo utente? Registrati qui', expanded=st.session_state['register_expanded']):
        try:
            if authenticator.register_user('Registrazione Nuovo Utente', location= 'main', preauthorization=False):
                st.session_state['show_register_success'] = True
                st.session_state['register_expanded'] = False
                # with open('./users.yaml','w') as file:
                #     yaml.dump(config, file, default_flow_style=False)
                sqlfunctions.writeconfigtosql(config)
                st.session_state['config'] = config
                st.experimental_rerun()
        except Exception as e:
            st.error(e)


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

authenticator = stauth.MyAuthenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


if st.session_state['authentication_status']:
    st.header('This is the home page for a registered user')
    st.text('This is sample text')
    df = pd.DataFrame(columns=['Nome','Cognome','Spesa'])
    df.loc[0] = ['Robi','Rossi',100]
    df.loc[1] = ['Mario','Bianchi',200]
    print('Created dataframe')
    print(df)
    print('Launch DB engine....')
    engine = create_engine('postgresql+psycopg2://ghonjgob:ynto7jSSSvboDVrZYeDkpMjMDE_rUhGF@snuffleupagus.db.elephantsql.com/ghonjgob', echo=False, pool_pre_ping=True)
    print('Engine Launched.')
    print('Loading Dataframe to SQL DB...')
    df.to_sql('spese', con=engine, if_exists='replace')
    print('Dataframe loaded.')
    st.text('You have saved data to a database')

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
