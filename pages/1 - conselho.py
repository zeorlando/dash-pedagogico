import streamlit as st
import pandas as pd

from st_aggrid import AgGrid, JsCode

# AJUSTES DAS TABELAS
notas = pd.read_csv('notas_atividades.csv', sep=';', encoding = 'iso-8859-1')
notas['rm'] = notas['rm'].astype(int)
notas['anoletivo'] = notas['anoletivo'].astype(int)
notas_ano_vigente = notas[(notas['anoletivo'] == 2024)]
notas_ano_vigente.to_csv('notas_ano_vigente.csv', sep=';', encoding = 'iso-8859-1', index = False)

alunos = pd.read_csv('alunos.csv', sep=';', encoding = 'iso-8859-1')
alunos.dropna(subset=["anoletivo"], inplace=True)
alunos['rm'] = alunos['rm'].astype(int)
alunos['idturma'] = alunos['idturma'].astype(int)
alunos['anoletivo'] = alunos['anoletivo'].astype(int)
alunos = alunos[['rm','nome', 'idturma','status', 'situacaoturma', 'anoletivo']]
alunos = alunos[(alunos['status'] == 'A') & 
                (alunos['situacaoturma'] == 'A') & 
                (alunos['anoletivo'] == 2024)]

turmas = pd.read_csv('turmas.csv', sep=";", encoding='iso-8859-1')
turmas['idturma'] = turmas['idturma'].astype(int)
turmas['anoletivo'] = turmas['anoletivo'].astype(int) 

tab_turmas_alunos = pd.merge(alunos, turmas, how='inner', on='idturma')
tab_turmas_alunos.rename(columns={'descrturma':'turma'}, inplace=True)
tab_turmas_alunos = tab_turmas_alunos[(tab_turmas_alunos['anoletivo_x'] == 2024) &
                                      (tab_turmas_alunos['status'] == 'A') &
                                      (tab_turmas_alunos['situacaoturma'] == 'A')]

tab_notas_alunos = pd.merge(notas_ano_vigente, tab_turmas_alunos, how='inner', on=['rm', 'turma'])
tab_notas_alunos = tab_notas_alunos[['rm', 'nome_x', 'anoletivo', 'curso', 'disciplina', 'turma', 'idatividade', 'bimestre', 'nota']]
tab_notas_alunos.rename(columns={'nome_x':'nome'}, inplace=True)

tab_notas_pivot = tab_notas_alunos.pivot_table(index = ['rm', 'nome', 'turma', 'curso','disciplina', 'bimestre'], columns = ['idatividade'], values = 'nota')

df_notas_trim = pd.DataFrame(tab_notas_pivot.to_records())

# ARTE
arte = df_notas_trim[df_notas_trim['disciplina'] == 'ARTE']
try:
    if len(arte) > 0:
        arte = arte[['rm', 'nome', 'turma', 'disciplina', 'bimestre','DE ART', 'TE ART']]
        arte['media'] = (arte['DE ART'] + arte['TE ART']).round(2)
    else:
        print('Nenhuma nota digitada ainda')
except:
    print('Notas faltando')

# ED.FÍSICA
ed_fisica = df_notas_trim[df_notas_trim['disciplina'] == 'EDUCAÇÃO FÍSICA']
try:
    if len(ed_fisica) > 0:
        ed_fisica = ed_fisica[['rm', 'nome', 'turma', 'disciplina', 'bimestre','DE ED. FIS', 'PO']]
        ed_fisica['media'] = (ed_fisica['DE ED. FIS'] + ed_fisica['PO']).round(2)
    else:
        print('Nenhuma nota digitada ainda')
except:
    print('Notas faltando')

# INGLÊS ETAPA 1
ingles_etapa1 = df_notas_trim[
    (df_notas_trim['disciplina'] == 'INGLÊS') & 
    ((df_notas_trim['curso'] == '3° ANO EF') | 
     (df_notas_trim['curso'] == '4° ANO EF') | 
     (df_notas_trim['curso'] == '5° ANO EF'))]
try:
    if len(ingles_etapa1) > 0:
        ingles_etapa1 = ingles_etapa1[['rm', 'nome', 'turma', 'disciplina', 'bimestre','AA1', 'DE', 'TE']]
        ingles_etapa1['media'] = ((ingles_etapa1['AA1'] + ingles_etapa1['DE'] + ingles_etapa1['TE'])/2).round(2)
    else:
        print('Nenhuma nota digitada ainda')
except:
    print('Notas faltando')

# INGLÊS ETAPA 2
ingles_etapa2 = df_notas_trim[
    (df_notas_trim['disciplina'] == 'INGLÊS') & 
    ((df_notas_trim['curso'] != '3° ANO EF') & 
     (df_notas_trim['curso'] != '4° ANO EF') & 
     (df_notas_trim['curso'] != '5° ANO EF'))]
try:
    if len(ingles_etapa2) > 0:
        ingles_etapa2 = ingles_etapa2[['rm', 'nome', 'turma', 'disciplina','bimestre','AA1','DE', 'TE']]
        ingles_etapa2['media'] = ((ingles_etapa2['AA1'] + ingles_etapa2['DE'] + ingles_etapa2['TE'])/2).round(2)
    else:
        print('Nenhuma nota digitada ainda')
except:
    print('Notas faltando')

# ESPANHOL
espanhol = df_notas_trim[df_notas_trim['disciplina'] == 'ESPANHOL']
try:
    if len(espanhol) > 0:
        espanhol = espanhol[['rm', 'nome', 'turma', 'disciplina', 'bimestre','AA1','DE', 'TE']]
        espanhol['media'] = ((espanhol['AA1'] + espanhol['DE'] + espanhol['TE'])/2).round(2)
    else:
        print('Nenhuma nota digitada ainda')
except:
    print('Notas faltando')

# PORTUGUÊS ETAPA 1
try:
    lp_etapa1 = df_notas_trim[
        (df_notas_trim['disciplina'] == 'LÍNGUA PORTUGUESA') & 
        ((df_notas_trim['curso'] == '3° ANO EF') | 
         (df_notas_trim['curso'] == '4° ANO EF') | 
         (df_notas_trim['curso'] == '5° ANO EF'))]
    lp_etapa1 = lp_etapa1[['rm', 'nome', 'turma', 'disciplina', 'bimestre','AA1', 'DE', 'TE']]
    lp_etapa1['media'] = ((lp_etapa1['AA1'] + lp_etapa1['DE'] + lp_etapa1['TE'])/2).round(2)
except:
    print('Notas faltando')

# MATEMÁTICA ETAPA 1
try:
    mat_etapa1 = df_notas_trim[
        (df_notas_trim['disciplina'] == 'MATEMÁTICA') & 
        ((df_notas_trim['curso'] == '3° ANO EF') | 
         (df_notas_trim['curso'] == '4° ANO EF') | 
         (df_notas_trim['curso'] == '5° ANO EF'))]
    mat_etapa1 = mat_etapa1[['rm', 'nome', 'turma', 'disciplina','bimestre','AA1', 'DE', 'TE']]
    mat_etapa1['media'] = ((mat_etapa1['AA1'] + mat_etapa1['DE'] + mat_etapa1['TE'])/2).round(2)
except:
    print('Notas faltando')

# CIÊNCIAS ETAPA 1
try:
    cie_etapa1 = df_notas_trim[
        (df_notas_trim['disciplina'] == 'CIÊNCIAS') & 
        ((df_notas_trim['curso'] == '3° ANO EF') | 
         (df_notas_trim['curso'] == '4° ANO EF') | 
         (df_notas_trim['curso'] == '5° ANO EF'))]
    cie_etapa1 = cie_etapa1[['rm', 'nome', 'turma', 'disciplina','bimestre','AA1', 'DE', 'TE']]
    cie_etapa1['media'] = ((cie_etapa1['AA1'] + cie_etapa1['DE'] + cie_etapa1['TE'])/2).round(2)
except:
    print('Notas faltando')

# GEOGRAFIA ETAPA 1
try:
    geo_etapa1 = df_notas_trim[
        (df_notas_trim['disciplina'] == 'GEOGRAFIA') & 
        ((df_notas_trim['curso'] == '4° ANO EF') | 
         (df_notas_trim['curso'] == '5° ANO EF'))]
    geo_etapa1 = geo_etapa1[['rm', 'nome', 'turma', 'disciplina', 'bimestre','AA1', 'DE', 'TE']]
    geo_etapa1['media'] = ((geo_etapa1['AA1'] + geo_etapa1['DE'] + geo_etapa1['TE'])/2).round(2)
except:
    print('Notas faltando')

# HISTÓRIA ETAPA 1
try:
    his_etapa1 = df_notas_trim[
        (df_notas_trim['disciplina'] == 'HISTÓRIA') & 
        ((df_notas_trim['curso'] == '4° ANO EF') | 
         (df_notas_trim['curso'] == '5° ANO EF'))]
    his_etapa1 = his_etapa1[['rm', 'nome', 'turma', 'disciplina','bimestre','AA1', 'DE', 'TE']]
    his_etapa1['media'] = ((his_etapa1['AA1'] + his_etapa1['DE'] + his_etapa1['TE'])/2).round(2)
except:
    print('Notas faltando')

# HISTÓRIA/GEOGRAFIA ETAPA 1
try:
    hisEgeo_etapa1 = df_notas_trim[
        (df_notas_trim['disciplina'] == 'HISTÓRIA/GEOGRAFIA') & 
        ((df_notas_trim['curso'] == '3° ANO EF'))]
    hisEgeo_etapa1 = hisEgeo_etapa1[['rm', 'nome', 'turma', 'disciplina','bimestre','AA1', 'DE', 'TE']]
    hisEgeo_etapa1['media'] = ((hisEgeo_etapa1['AA1'] + hisEgeo_etapa1['DE'] + hisEgeo_etapa1['TE'])/2).round(2)
except:
    print('Notas faltando')

# PORTUGUÊS ETAPA 2
try:
    lp_etapa2 = df_notas_trim[
        (df_notas_trim['disciplina'] == 'LÍNGUA PORTUGUESA') & 
        ((df_notas_trim['curso'] != '3° ANO EF') & 
         (df_notas_trim['curso'] != '4° ANO EF') & 
         (df_notas_trim['curso'] != '5° ANO EF'))]
    lp_etapa2 = lp_etapa2[['rm', 'nome', 'turma', 'disciplina','bimestre','AA1', 'AA2','DE', 'TE']]
    lp_etapa2['media'] = ((lp_etapa2['AA1'] + lp_etapa2['AA2'] + lp_etapa2['DE'] + lp_etapa2['TE'])/3).round(2)
except:
    print('Notas faltando')

# MATEMÁTICA ETAPA 2
try:
    mat_etapa2 = df_notas_trim[
        (df_notas_trim['disciplina'] == 'MATEMÁTICA') & 
        (df_notas_trim['curso'] != '3° ANO EF') & 
        (df_notas_trim['curso'] != '4° ANO EF') & 
        (df_notas_trim['curso'] != '5° ANO EF')]
    mat_etapa2 = mat_etapa2[['rm', 'nome', 'turma', 'disciplina','bimestre','AA1', 'AA2','DE', 'TE']]
    mat_etapa2['media'] = ((mat_etapa2['AA1'] + mat_etapa2['AA2'] + mat_etapa2['DE'] + mat_etapa2['TE'])/3).round(2)
except:
    print('Notas faltando')

# CIÊNCIAS ETAPA 2
try:
    cie_etapa2 = df_notas_trim[
        (df_notas_trim['disciplina'] == 'CIÊNCIAS') & 
        (df_notas_trim['curso'] != '3° ANO EF') & 
        (df_notas_trim['curso'] != '4° ANO EF') & 
        (df_notas_trim['curso'] != '5° ANO EF')]
    cie_etapa2 = cie_etapa2[['rm', 'nome', 'turma', 'disciplina','bimestre','AA1', 'AA2','DE', 'TE']]
    cie_etapa2['media'] = ((cie_etapa2['AA1'] + cie_etapa2['AA2'] + cie_etapa2['DE'] + cie_etapa2['TE'])/3).round(2)
except:
    print('Notas faltando')

# GEOGRAFIA ETAPA 2
try:
    geo_etapa2 = df_notas_trim[
        (df_notas_trim['disciplina'] == 'GEOGRAFIA') & 
        (df_notas_trim['curso'] != '3° ANO EF') & 
        (df_notas_trim['curso'] != '4° ANO EF') & 
        (df_notas_trim['curso'] != '5° ANO EF')]
    geo_etapa2 = geo_etapa2[['rm', 'nome', 'turma', 'disciplina','bimestre','AA1', 'AA2','DE', 'TE']]
    geo_etapa2['media'] = ((geo_etapa2['AA1'] + geo_etapa2['AA2'] + geo_etapa2['DE'] + geo_etapa2['TE'])/3).round(2)
except:
    print('Notas faltando')

# HISTÓRIA ETAPA 2
try:
    his_etapa2 = df_notas_trim[
        (df_notas_trim['disciplina'] == 'HISTÓRIA') & 
        (df_notas_trim['curso'] != '3° ANO EF') & 
        (df_notas_trim['curso'] != '4° ANO EF') & 
        (df_notas_trim['curso'] != '5° ANO EF')]
    his_etapa2 = his_etapa2[['rm', 'nome', 'turma', 'disciplina','bimestre','AA1', 'AA2','DE', 'TE']]
    his_etapa2['media'] = ((his_etapa2['AA1'] + his_etapa2['AA2'] + his_etapa2['DE'] + his_etapa2['TE'])/3).round(2)
except:
    print('Notas faltando')

# MONTAGEM DO DF FINAL
disciplinas = [arte, ed_fisica, ingles_etapa1, ingles_etapa2, espanhol, lp_etapa1, mat_etapa1, cie_etapa1, geo_etapa1, his_etapa1, hisEgeo_etapa1, lp_etapa2, mat_etapa2, cie_etapa2, geo_etapa2, his_etapa2]
tab_rec = pd.concat(disciplinas)
analise_rec = tab_rec[['rm', 'nome', 'turma', 'disciplina', 'bimestre','media','AA1', 'AA2','TE', 'DE', 'TE ART', 'DE ART', 'PO', 'DE ED. FIS']]

def arredondaMedia (analise_rec):
    decimal = round((analise_rec['media'] % 1),2)
    if (decimal < 0.25):
        analise_rec['media'] = round(analise_rec['media'] - decimal)
    elif ((decimal >= 0.25) & (decimal < 0.75)):
        novo_decimal = 0.50
        analise_rec['media'] = round(((analise_rec['media'] + novo_decimal) - decimal),2)
    else:
        analise_rec['media'] = ((analise_rec['media'] // 1) + 1)

    return analise_rec['media']

analise_rec['media'] = analise_rec.apply(arredondaMedia, axis = 1)
analise_rec = analise_rec.rename(columns={'bimestre': 'trimestre'})


tab_turmas_alunos_filtro_turma = tab_turmas_alunos[tab_turmas_alunos['turma'].str.contains('3|4|5|6|7|8|9')]
tab_turmas_alunos_filtro_turma = tab_turmas_alunos_filtro_turma.sort_values(by=['turma'])

# PROCESSO DE REC
medias_boletim = pd.read_csv('medias.csv', sep=';', encoding = 'iso-8859-1')

medias_boletim['anoletivo'] = medias_boletim['anoletivo'].astype(int)
medias_boletim['rm'] = medias_boletim['rm'].astype(int)

medias_boletim['B1media'] = medias_boletim['B1media'].str.replace(',', '.')
medias_boletim['B1recup'] = medias_boletim['B1recup'].str.replace(',', '.')
medias_boletim['B1mediabim'] = medias_boletim['B1mediabim'].str.replace(',', '.')

medias_boletim['B2media'] = medias_boletim['B2media'].str.replace(',', '.')
medias_boletim['B2recup'] = medias_boletim['B2recup'].str.replace(',', '.')
medias_boletim['B2mediabim'] = medias_boletim['B2mediabim'].str.replace(',', '.')

medias_boletim['B3media'] = medias_boletim['B3media'].str.replace(',', '.')
medias_boletim['B3recup'] = medias_boletim['B3recup'].str.replace(',', '.')
medias_boletim['B3mediabim'] = medias_boletim['B3mediabim'].str.replace(',', '.')

medias_boletim['B1media'] = medias_boletim['B1media'].astype(float)
medias_boletim['B1recup'] = medias_boletim['B1recup'].astype(float)
medias_boletim['B1mediabim'] = medias_boletim['B1mediabim'].astype(float)

medias_boletim['B2media'] = medias_boletim['B2media'].astype(float)
medias_boletim['B2recup'] = medias_boletim['B2recup'].astype(float)
medias_boletim['B2mediabim'] = medias_boletim['B2mediabim'].astype(float)

medias_boletim['B3media'] = medias_boletim['B3media'].astype(float)
medias_boletim['B3recup'] = medias_boletim['B3recup'].astype(float)
medias_boletim['B3mediabim'] = medias_boletim['B3mediabim'].astype(float)

medias_boletim['mediaparcial'] = medias_boletim['mediaparcial'].str.replace(',', '.')
medias_boletim['mediaparcial'] = medias_boletim['mediaparcial'].astype(float)


medias = medias_boletim[medias_boletim["anoletivo"] == 2024]

turmas_descricao = df_notas_trim[['rm', 'turma']].drop_duplicates()

medias_notas = medias.merge(turmas_descricao, on='rm', how='inner')

medias_notas = medias_notas[['rm', 'nome', 'anoletivo', 'turma', 'descrdisciplina', 'B1media',
       'B1recup', 'B1mediabim', 'B1faltas', 'B2media', 'B2recup', 'B2mediabim',
       'B2faltas', 'B3media', 'B3recup', 'B3mediabim', 'B3faltas', 'mediaparcial', 'totalfaltas',
       'mediafinal']]

medias_notas = medias_notas.rename(columns=
                                   {'descrdisciplina': 'disciplina',
                                    'B1media': 'T1media',
                                    'B1recup':'T1recup',
                                    'B1mediabim':'T1mediaTRI',
                                    'B1faltas':'T1faltas',
                                    'B2media': 'T2media',
                                    'B2recup':'T2recup',
                                    'B2mediabim':'T2mediaTRI',
                                    'B2faltas':'T2faltas',
                                    'B3media': 'T3media',
                                    'B3recup':'T3recup',
                                    'B3mediabim':'T3mediaTRI',
                                    'B3faltas':'T3faltas',}
                                   )

colunas_usadas = ['rm', 'nome_x', 'turma_x','disciplina', 'trimestre', 'media', 'mediaparcial', 
                  'T1recup', 'T1mediaTRI', 'T1faltas', 
                  'T2recup', 'T2mediaTRI', 'T2faltas',
                  'T3recup', 'T3mediaTRI', 'T3faltas',
                  'AA1', 'AA2', 'TE', 'DE', 'PO', 'DE ED. FIS', 'TE ART', 'DE ART'] 

medias_notas_processo = medias_notas.merge(analise_rec, on=['rm', 'disciplina'], how='inner')
medias_notas_processo.to_csv('notas.csv', sep=';', encoding = 'iso-8859-1', index = False)

medias_notas_processo = medias_notas_processo[colunas_usadas]

# VERIFICA NOTAS FALTANTES
#medias_notas_processo[medias_notas_processo['media'].isna()]

# BARRA DE FILTROS PRINCIPAIS
with st.sidebar:
    turma = st.multiselect(
        'Escolha a turma',
        tab_turmas_alunos_filtro_turma['turma'].unique()
    )

    trimestre = st.multiselect(
        'Escolha o trimestre',
        medias_notas_processo['trimestre'].unique()
    )

selecao = medias_notas_processo[(medias_notas_processo['turma_x'].isin(turma)) & 
                                (medias_notas_processo['media'] > 0) &
                                (medias_notas_processo['trimestre'].isin(trimestre))].sort_values(by=['turma_x','nome_x', 'disciplina'])

selecao_media_parcial = medias_notas_processo[(medias_notas_processo['turma_x'].isin(turma)) &
                                              (medias_notas_processo['media'] > 0)]

selecao = selecao.fillna(value='')

media_parcial_abaixo = selecao_media_parcial[selecao_media_parcial['mediaparcial'] < 7]

def gera_lista(coluna):
    return selecao[coluna].to_list()

disciplinas_x = selecao['disciplina'].unique().tolist()

trimestres =  {
    1 : ['T1recup', 'T1mediaTRI', 'T1faltas'],
    2 : ['T2recup', 'T2mediaTRI', 'T2faltas'],
    3 : ['T3recup', 'T3mediaTRI', 'T3faltas'],
}

def gera_fechamento_tri(disciplina, trimestre, media):
    if ((disciplina in disciplinas_x) & (media < 7)):
        lista_fechamento_tri = [
            {'Atividades':'Rec', 'Nota':gera_lista(trimestres[trimestre][0])[i], 'Trimestre':gera_lista('trimestre')[i]}, 
            {'Atividades':'Média Tri', 'Nota':gera_lista(trimestres[trimestre][1])[i],'Trimestre':gera_lista('trimestre')[i]},

        ]
        return lista_fechamento_tri
    elif ((disciplina in disciplinas_x) & (media >= 7)):
        lista_fechamento_tri = [
            {'Atividades':'Média Tri', 'Nota':gera_lista(trimestres[trimestre][1])[i],'Trimestre':gera_lista('trimestre')[i]},
        ]
        return lista_fechamento_tri

def gera_atividades(disciplina):
        if (disciplina == 'ARTE'):
            lista_atividades = [
                {'Atividades': 'TE ART', 'Nota': gera_lista('TE ART')[i], 'Trimestre':gera_lista('trimestre')[i]}, 
                {'Atividades': 'DE ART', 'Nota': gera_lista('DE ART')[i], 'Trimestre':gera_lista('trimestre')[i]},
            ]
        elif (disciplina == 'EDUCAÇÃO FÍSICA'):
            lista_atividades = [
                {'Atividades': 'DE ED. FÍS', 'Nota': gera_lista('DE ED. FIS')[i], 'Trimestre':gera_lista('trimestre')[i]},
                {'Atividades': 'PO', 'Nota': gera_lista('PO')[i], 'Trimestre':gera_lista('trimestre')[i]},
            ]
        elif ((disciplina == 'INGLÊS') | 
              (disciplina == 'ESPANHOL') | 
              (selecao['turma_x'].str.contains('3|4|5'))).any():
            lista_atividades = [
                {'Atividades': 'AA1', 'Nota': gera_lista('AA1')[i], 'Trimestre':gera_lista('trimestre')[i]},
                {'Atividades': 'TE', 'Nota': gera_lista('TE')[i], 'Trimestre':gera_lista('trimestre')[i]},
                {'Atividades': 'DE', 'Nota': gera_lista('DE')[i], 'Trimestre':gera_lista('trimestre')[i]},
            ]
        else:
            lista_atividades = [
                {'Atividades': 'AA1', 'Nota': gera_lista('AA1')[i], 'Trimestre':gera_lista('trimestre')[i]},
                {'Atividades': 'AA2', 'Nota': gera_lista('AA2')[i], 'Trimestre':gera_lista('trimestre')[i]},
                {'Atividades': 'TE', 'Nota': gera_lista('TE')[i], 'Trimestre':gera_lista('trimestre')[i]},
                {'Atividades': 'DE', 'Nota': gera_lista('DE')[i],'Trimestre':gera_lista('trimestre')[i]},
            ]
        return lista_atividades

data = []
for i in range(len(selecao)):
    if gera_lista('disciplina')[i] == 'ARTE':
        data.append(
            {
                'Nome':gera_lista('nome_x')[i],
                'Média': gera_lista('media')[i],
                'Disciplina':gera_lista('disciplina')[i],
                'Trimestre':gera_lista('trimestre')[i],
                'callRecords': gera_atividades(gera_lista('disciplina')[i]) + 
                               gera_fechamento_tri(gera_lista('disciplina')[i], 
                                                   gera_lista('trimestre')[i], 
                                                   gera_lista('media')[i])
            }
        )
    elif gera_lista('disciplina')[i] == 'EDUCAÇÃO FÍSICA':
        data.append(
            {
                'Nome':gera_lista('nome_x')[i],
                'Média': gera_lista('media')[i],
                'Disciplina':gera_lista('disciplina')[i],
                'Trimestre':gera_lista('trimestre')[i],
                'callRecords': gera_atividades(gera_lista('disciplina')[i]) + 
                               gera_fechamento_tri(gera_lista('disciplina')[i], 
                                                   gera_lista('trimestre')[i], 
                                                   gera_lista('media')[i])

            }
        )
    elif ((gera_lista('disciplina')[i] == 'INGLÊS') | 
          (gera_lista('disciplina')[i] == 'ESPANHOL') | 
          (selecao['turma_x'].str.contains('3|4|5'))).any() :
        data.append(
            {
                'Nome':gera_lista('nome_x')[i],
                'Média': gera_lista('media')[i],
                'Disciplina':gera_lista('disciplina')[i],
                'Trimestre':gera_lista('trimestre')[i],
                'callRecords': gera_atividades(gera_lista('disciplina')[i]) +
                               gera_fechamento_tri(gera_lista('disciplina')[i], 
                                                   gera_lista('trimestre')[i], 
                                                   gera_lista('media')[i]),
            }
        )
    else:
        data.append(
            {
                'Nome':gera_lista('nome_x')[i],
                'Média': gera_lista('media')[i],
                'Disciplina':gera_lista('disciplina')[i],
                'Trimestre':gera_lista('trimestre')[i],
                'callRecords':gera_atividades(gera_lista('disciplina')[i]) + 
                              gera_fechamento_tri(gera_lista('disciplina')[i], 
                                                   gera_lista('trimestre')[i], 
                                                   gera_lista('media')[i])

            }
        )

js_code_style = JsCode("""
    function(params) {
        if (params.value >= 7) {
            return { color: 'green'}
        } else {
            return { color: 'red'}
        }
    }
""")

gridOptions = {
    'masterDetail': True,
    'columnDefs': [
        {
            'field': 'Nome',
            'cellRenderer': 'agGroupCellRenderer',
        },
        {'field': 'Disciplina'},
        {'field': 'Média', 'cellStyle': js_code_style, 'type':"numberColumnFilter"},
        {'field':'Trimestre', 'type':"numberColumnFilter"}
    ],
    'detailCellRendererParams': {
        'detailGridOptions': {
            'columnDefs': [
                {'field': 'Atividades'},
                {'field': 'Nota'},
                {'field': 'Trimestre'}
            ],
        },
        'getDetailRowData': JsCode(
            """function (params) {
                params.successCallback(params.data.callRecords);
        }"""
        ),
    },
    'rowData': data,
}

AgGrid(
    None,
    gridOptions=gridOptions,
    allow_unsafe_jscode=True,
)

st.html('<h2>Alunos que estão devendo nota</h2>')

st.dataframe(media_parcial_abaixo[['nome_x', 'turma_x', 'disciplina', 'mediaparcial']], hide_index = True)