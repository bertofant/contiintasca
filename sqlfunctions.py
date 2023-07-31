import psycopg2

CONFIGDBSTRING = "dbname='ghonjgob' user='ghonjgob' password='ynto7jSSSvboDVrZYeDkpMjMDE_rUhGF' host='snuffleupagus.db.elephantsql.com'  "

def create_table(table,keylist):
    conn = psycopg2.connect(CONFIGDBSTRING)
    cur = conn.cursor()
    # Build sql command like "CREATE TABLE IF NOT EXISTS config (username TEXT, name TEXT, password TEXT, PRIMARY KEY (username))"
    sqlcmd = f"CREATE TABLE IF NOT EXISTS {table} ("
    for (key,keytype) in keylist:
        sqlcmd += f"{key} "
        sqlcmd += f"{keytype},"
    sqlcmd += f" PRIMARY KEY ({key[0]}))"
    cur.execute(sqlcmd)
    conn.commit()
    conn.close()

def insert_in_table(table,list_data):
    conn = psycopg2.connect(CONFIGDBSTRING)
    cur = conn.cursor()
    sqlcmd = f"INSERT INTO {table} VALUES ("
    for count, data in enumerate(list_data):
        if count < (len(list_data)-1):
            sqlcmd += f"'{data}',"
        else:
            sqlcmd += f"'{data}')"
    #cur.execute(f"INSERT INTO config VALUES ('{username}', '{name}', '{password}')")
    cur.execute(sqlcmd)
    conn.commit()
    conn.close()

def view_table(table):
    conn = psycopg2.connect(CONFIGDBSTRING)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows =  cur.fetchall()
    conn.close()
    return rows

def delete_from_table(table,primarykey,value):
    conn = psycopg2.connect(CONFIGDBSTRING)
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table} WHERE {primarykey}={value}")
    conn.commit()
    conn.close()

def update_in_config_table(usernmane,name,password):
    conn = psycopg2.connect(CONFIGDBSTRING)
    cur = conn.cursor()
    cur.execute("UPDATE config SET name=%s, password=%s WHERE username=%s",(name, password, usernmane) )
    conn.commit()
    conn.close()



def getconfigfromsql():
    config = {}
    config['cookie'] = {'expiry_days': 30, 'key': 'markthisplace_key', 'name':'markthisplace_name' }
    credentials_dict={}
    usernames_dict={}
    accounts = view_table("config")
    for account in accounts:
        usernames_dict[account[0]]={'email': account[0], 'name': account[1], 'password': account[2] }
    credentials_dict['usernames'] = usernames_dict

    config['credentials']=credentials_dict
    preauth_dict = {}
    preauth_dict['emails'] = None
    config['preauthorized'] = preauth_dict
    return config

def writeconfigtosql(config):
    create_table("config",[("username","TEXT"), ("name","TEXT"), ("password","TEXT")])
    # Load existing confi to avoid writing data that already exists
    stored_config = getconfigfromsql()
    stored_usernames = stored_config['credentials']['usernames'].keys()
    for username, infos in config['credentials']['usernames'].items():
        if username not in stored_usernames:
            name = infos['name']
            password = infos['password']
            insert_in_table("config", [f"{username}",f"{name}",f"{password}"] )
        # else:
        #     print(f'skipping sql insert of {username}')



