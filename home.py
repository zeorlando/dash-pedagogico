import streamlit as st
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import close_all_sessions

with st.sidebar:
    button_load_files = st.button('Carregar dados')

file_path_views = open('path_views.txt', 'r')
path_views = file_path_views.read()

if button_load_files:
    db = create_engine(path_views)
    conn = db.connect()

    query_notas_atividades = pd.read_sql_query('SELECT * FROM viewnotasatividades', conn)
    notas_atividades = pd.DataFrame(query_notas_atividades)
    notas_atividades.to_csv('notas_atividades.csv', sep=';', encoding = 'iso-8859-1', index = False)

    query_medias = pd.read_sql_query('SELECT * FROM viewmedias', conn)
    medias = pd.DataFrame(query_medias)
    medias.to_csv('medias.csv', sep=';', encoding = 'iso-8859-1', index = False)

    query_alunos = pd.read_sql_query('SELECT * FROM viewalunos', conn)
    alunos = pd.DataFrame(query_alunos)
    alunos.to_csv('alunos.csv', sep=';', encoding = 'iso-8859-1', index = False)

    query_turmas = pd.read_sql_query('SELECT * FROM viewturmas', conn)
    turmas = pd.DataFrame(query_turmas)
    turmas.to_csv('turmas.csv', sep=';', encoding = 'iso-8859-1', index = False)
    
    conn.close()
    db.dispose()
    close_all_sessions()