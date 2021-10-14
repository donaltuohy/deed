import evervault
from flask import Flask, request
import os
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

engine = None

@app.route('/connect', methods=['POST'])
def connect_db():
    global engine
    data = request.get_json()
    print('Connecting to the {} DB'.format(data.dbname))
    engine = create_engine(
        'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
        .format(data.user, data.password, data.host, data.port, data.dbname)
    )
    return 200

@app.route('/columns', methods=['GET'])
def get_columns():
    global engine
    data = request.get_json()
    df = pd.read_sql_table(data.table_name, engine)
    print(df.cols)
    return df.cols

@app.route('encryptColumn', methods=['POST'])
def encrypt_column():
    data = request.get_json()
    df = pd.read_sql_table(data.table_name, engine)
    ev_col = df[data.column_name]
    ev_col = ev_col.apply(lambda x: evervault.encrypt(x))
    print(ev_col)
    df['ev_' + data.column_name] = ev_col
    return 200

if __name__ == '__main__':
    evervault.api_key = evervault.init(os.environ.get('API_KEY'))
    app.run(
      host="0.0.0.0",
      port=8000
    )
