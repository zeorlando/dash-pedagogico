import streamlit as st
import pandas as pd
import plotly_express as px
from functools import reduce

notas = pd.read_csv('notas.csv', sep=';', encoding = 'iso-8859-1')
alunos = pd.read_csv('alunos.csv', sep=';', encoding = 'iso-8859-1')
turmas = pd.read_csv('turmas.csv', sep=';', encoding = 'iso-8859-1')
medias = pd.read_csv('medias_v2.csv', sep=';', encoding = 'iso-8859-1')

alunos_turmas = pd.merge(alunos, turmas, how='inner', on='idturma')

medias['mediafinal'] = medias['mediafinal'].str.replace(',', '.')
medias['mediafinal'] = medias['mediafinal'].astype(float)
medias['anoletivo'] = medias['anoletivo'].astype(str)

alunos_ano_vigente = notas['nome_x'].sort_values().unique()

with st.sidebar:
    nome_aluno = st.multiselect(
        'Informe o nome do(a) aluno(a)',
        alunos_ano_vigente
    )
    ano_analise = st.multiselect(
        'Escolha o(s) ano(s) de análise',
        medias[medias['nome'].isin(nome_aluno)]['anoletivo'].unique()
    )

aluno_selecionado = medias[medias['nome'].isin(nome_aluno)]
dados_grafico_temporal = aluno_selecionado[['descrdisciplina', 'anoletivo', 
                                            'descrcurso','B1mediabim', 'B2mediabim', 'B3mediabim']]

media_aluno = dados_grafico_temporal.melt(id_vars=['descrdisciplina', 'anoletivo', 'descrcurso'], 
                                    var_name='trimestre', value_name='Nota')

media_aluno['tri'] = media_aluno['trimestre'].apply(lambda x: '1' if x=='B1mediabim' else 
                                                    ('2' if x == 'B2mediabim' else '3'))

media_aluno['ano/tri'] = media_aluno['anoletivo'].map(str) + '/' + media_aluno['tri'].map(str)

media_aluno = media_aluno.sort_values(by=['anoletivo', 'ano/tri'])

media_aluno = media_aluno[media_aluno['anoletivo'].isin(ano_analise)]

fig = px.line(media_aluno, x='ano/tri', y='Nota', range_y = [0,10.5], 
              line_group='descrdisciplina', color='descrdisciplina', markers=True, title='Desempenho por trimestre')
fig.add_shape(
    type="line", line_color="red", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=7, y1=7, yref="y"
)
st.plotly_chart(fig)

mediasTri = medias
mediasTri['anoletivo'] = mediasTri['anoletivo'].astype(int)

lista_ano_int = [int(item) for item in ano_analise]
id_turma = alunos[(alunos['nome'].isin(nome_aluno))]['idturma'].unique().tolist()
rms = alunos[(alunos['idturma'].isin(id_turma))]['rm'].unique().tolist()

media_aluno_grupo = mediasTri[(mediasTri['rm'].isin(rms))]

B1mediabim = media_aluno_grupo[['rm','nome','anoletivo','descrcurso','descrdisciplina','B1mediabim']]
B1mediabim.dropna(inplace=True)

B2mediabim = media_aluno_grupo[['rm','nome','anoletivo','descrcurso','descrdisciplina','B2mediabim']]
B2mediabim.dropna(inplace=True)

B3mediabim = media_aluno_grupo[['rm','nome','anoletivo','descrcurso','descrdisciplina','B3mediabim']]
B3mediabim.dropna(inplace=True)

selecionadoT1 = B1mediabim[B1mediabim['anoletivo'].isin(lista_ano_int)]
mediaT1 = round(selecionadoT1.groupby(['descrdisciplina', 'anoletivo'])['B1mediabim'].mean().reset_index(),2)

selecionadoT2 = B2mediabim[B2mediabim['anoletivo'].isin(lista_ano_int)]
mediaT2 = round(selecionadoT2.groupby(['descrdisciplina', 'anoletivo'])['B2mediabim'].mean().reset_index(),2)

selecionadoT3 = B3mediabim[B3mediabim['anoletivo'].isin(lista_ano_int)]
mediaT3 = round(selecionadoT3.groupby(['descrdisciplina', 'anoletivo'])['B3mediabim'].mean().reset_index(),2)

dfs = [mediaT1, mediaT2, mediaT3]
mediaGeral = reduce(lambda  left,right: pd.merge(left,right,on=['descrdisciplina', 'anoletivo'],
                                            how='outer'), dfs)

media_grupo = mediaGeral.melt(id_vars=['descrdisciplina', 'anoletivo'], var_name='trimestre',
                                         value_name='Nota')

media_grupo['tri'] = media_grupo['trimestre'].apply(lambda x: '1' if x=='B1mediabim' else 
                                                    ('2' if x == 'B2mediabim' else '3'))

if ano_analise != []:
    media_grupo['ano/tri'] = media_grupo['anoletivo'].map(str) + '/' + media_grupo['tri'].map(str)

    media_grupo['descrdisciplina_junto'] = media_grupo['descrdisciplina'].map(str) + ' - TURMA'
    media_grupo = media_grupo.sort_values(by=['anoletivo', 'ano/tri'])

    media_aluno_individual = media_aluno
    media_aluno_individual['descrdisciplina_junto'] = media_aluno_individual['descrdisciplina'].map(str) + ' - ALUNO(A)' 

    media_aluno_conc_mediagrupo = pd.concat([media_grupo,media_aluno_individual])

    lista_disciplinas = media_aluno_conc_mediagrupo['descrdisciplina'].unique().tolist()

    select_disciplina = st.multiselect(
        'Informe a disciplina que deseja analisar o desempenho em relação a turma',
        lista_disciplinas
    )

    for disciplina in select_disciplina:
        media_disc = media_aluno_conc_mediagrupo[media_aluno_conc_mediagrupo['descrdisciplina'] == disciplina]
        fig = px.line(media_disc, x='ano/tri', y='Nota', range_y = [0,10.5], 
                line_group='descrdisciplina_junto', color='descrdisciplina_junto', 
                markers=True, title=f'Desempenho aluno em relação a turma - {disciplina}')
        fig.add_shape(
            type="line", line_color="red", line_width=3, opacity=1, line_dash="dot",
            x0=0, x1=1, xref="paper", y0=7, y1=7, yref="y"
        )
        st.plotly_chart(fig)



