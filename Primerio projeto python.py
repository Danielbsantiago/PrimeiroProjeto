# %%


#abrir a planilha e tratar os dados, criar indicadores

#salvar os dados e enviar por email

# %%
#Entrar no site do cvm e baixar uma planilha

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

#entrando no site da cvm
navegador = webdriver.Chrome()
navegador.get('https://dados.cvm.gov.br/dataset/fi-doc-inf_diario/resource/2bbbb7ad-5201-4f68-a36c-506cbc8248b1')


# %%
#Baixando o boletim diário cvm
botao_boletim = navegador.find_element(By. XPATH, 'https://dados.cvm.gov.br/dataset/fi-doc-inf_diario/resource/2bbbb7ad-5201-4f68-a36c-506cbc8248b1').click()
navegador.close()   

# %%
#abrir a planilha
import pandas as pd
df = pd.read_csv(r'C:\Users\Usuario\Downloads\inf_diario_fi_202606.zip', compression='zip', sep=';', encoding='utf-8')

pd.set_option('display.float_format', '{:,.2f}'.format)
display(df)

# %%
# tratar os dados, criar indicadores
df_analise = df.drop(columns=['TP_FUNDO_CLASSE'])
df_analise = df_analise.drop(columns=['ID_SUBCLASSE'])
df_analise = df_analise.rename(columns={'CNPJ_FUNDO_CLASSE' : 'CNPJ', 'DT_COMPTC' : 'DATA','VL_TOTAL': 'VALOR _TOTAL','VL_QUOTA': 'VALOR QUOTA',
                               'VL_PATRIM_LIQ': 'VALOR_PATRIMONIAL','CAPTC_DIA': 'CAPTAÇÃO_DIA','RESG_DIA' : 'RESGATE_DIA','NR_COTST' : 'NÚMERO_COTISTAS'})

#transformando a coluna data de str para datetime
df_analise['DATA'] = pd.to_datetime(df_analise['DATA'], format= "%Y-%m-%d")
display(df_analise)

# %%
#baixando tabela para csv
df_analise.to_csv("fundos_cmv_3.csv", sep=";", decimal='.', index=False)

# %%
#lendo tabela de cnpj
nomes_cnpj = pd.read_csv('cad_fi.csv', sep=";", encoding='latin1')

# %%
#limpando tabela do cnpj
df_cnpj = nomes_cnpj.drop(columns=["INVEST_CEMPR_EXTER", "CLASSE_ANBIMA", "CONTROLADOR", "CNPJ_CONTROLADOR", "CUSTODIANTE","CNPJ_CUSTODIANTE", "AUDITOR", "CNPJ_AUDITOR", "GESTOR", "CPF_CNPJ_GESTOR", "PF_PJ_GESTOR", "ADMIN", "CNPJ_ADMIN", "DIRETOR", "DT_PATRIM_LIQ", "VL_PATRIM_LIQ", "INF_TAXA_ADM", "TAXA_ADM", "INF_TAXA_PERFM", "TAXA_PERFM", "DT_INI_ATIV" , "PF_PJ_GESTOR", "ADMIN", "CNPJ_ADMIN", "DIRETOR", "DT_PATRIM_LIQ", "VL_PATRIM_LIQ", "INF_TAXA_ADM", "TAXA_ADM", "INF_TAXA_PERFM", "TAXA_PERFM", "DT_INI_ATIV","ENTID_INVEST", "PUBLICO_ALVO","TRIB_LPRAZO", "FUNDO_EXCLUSIVO", "FUNDO_COTAS", "CONDOM", "RENTAB_FUNDO", "DT_INI_CLASSE", "CLASSE", "DT_FIM_EXERC", "DT_INI_EXERC"])
df_cnpj = df_cnpj.rename(columns={"CNPJ_FUNDO" : "CNPJ"})
display(df_cnpj)


# %%
#juantando as tabelas pelo cnpj
df_final = df_analise.merge(df_cnpj, on="CNPJ", how="left")
df_final = df_final.drop(columns=['TP_FUNDO'])
display(df_final)


# %%
df_final["CAPTAÇÃO_LIQUIDA"] = df_final["CAPTAÇÃO_DIA"] - df_final["RESGATE_DIA"]
display(df_final)

# %%
df_final.to_csv("df_final.csv", sep=";", index=False)
#transformando data em formato tipo data 
df_final["DATA"] = pd.to_datetime(df_final["DATA"]).dt.date
df_final["DT_REG"] = pd.to_datetime(df_final["DT_REG"]).dt.date
df_final["DT_INI_SIT"] = pd.to_datetime(df_final["DT_INI_SIT"]).dt.date
df_final["DT_CANCEL"] = pd.to_datetime(df_final["DT_CANCEL"]).dt.date

#transformando arquivo em csv
df_final.to_csv("df_final2.csv", sep=";", index=False)


# %%



