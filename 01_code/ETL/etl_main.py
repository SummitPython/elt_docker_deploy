#!/usr/bin/env python
# coding: utf-8

# !pip install requests

# !pip install pandas

# ##### Importando libs

# In[88]:


import pandas as pd
import requests
import json
import math
import os
import re


# In[89]:


from json import JSONDecodeError


# ##### Definindo parâmetros da chamada

# In[90]:


payload = {}
headers = {'Cookie': ''}


# ##### Definindo url e enviando chamada

# In[91]:


url_raw = "https://brasil.io/api/dataset/covid19/caso_full/data/?page="
url_base = "https://brasil.io/api/dataset/covid19/caso_full/data/?page=1"
response_url_base = requests.request("GET", url_base, headers=headers, data = payload)


# ### Carregando o resultado da chamada
# ##### A disponibilidade do link é sempre verificada 

# In[92]:


data = json.loads(response_url_base.text.encode('utf8').decode('utf8'))     if response_url_base.status_code == 200         else print('Escrever Log')


# ### Como há paginação da API e os dados crescem a cada dia, foi adicionado um um variável verificadora do link "final" da API

# In[93]:


page_final = math.ceil(data['count']/len(data['results']))

url_final = "https://brasil.io/api/dataset/covid19/caso_full/data/?page=" + str(page_final) + ""

print(url_final)


# In[94]:


data['next'], data['previous']


# In[95]:


response_url_final = requests.request("GET", url_final, headers=headers, data = payload)
data_final = json.loads(response_url_final.text.encode('utf8').decode('utf8'))
data_final['next'], data_final['previous']


# ### Salvando o resultado da requisição em formato csv, na qual estava em formato json
# ##### O arquivo apenas será salve caso ele não exista

# In[96]:


pd.DataFrame.from_dict(data['results'])    .to_csv(os.getcwd() + '\\DataFrame\\01_RAW\\' + re.sub('[^a-zA-Z0-9 \n\.]', '_', url_base) + '.csv', index = False)         if not re.sub('[^a-zA-Z0-9 \n\.]', '_', url_base) + '.csv' in os.listdir(path = os.getcwd() + '\\DataFrame\\01_raw')             else  print('DataFrame já carregado')


# In[97]:


link_num = 0
link_num_begin = 0
link_num_end = 10


# In[98]:


try:
    while link_num_begin < link_num_end:
        for link_num in range(1, page_final + 1):

            if re.sub('[^a-zA-Z0-9 \n\.]', '_', url_raw + str(link_num)) + '.csv' in os.listdir(path = os.getcwd() + '\\DataFrame\\01_raw'):
                print('DataFrame já carregado', end = '\n')
            else:
                response_url_link_num = requests.request("GET", url_raw + str(link_num), headers=headers, data = payload)
                data_link_num = json.loads(response_url_link_num.text.encode('utf8').decode('utf8')) if response_url_link_num.status_code == 200 else print('Escrever Log')

                print(url_raw + str(link_num))

                pd.DataFrame.from_dict(data_link_num['results'])                    .to_csv(os.getcwd() + '\\DataFrame\\01_raw\\' + re.sub('[^a-zA-Z0-9 \n\.]', '_', url_raw + str(link_num)) + '.csv', index = False)                         if not re.sub('[^a-zA-Z0-9 \n\.]', '_', url_raw + str(link_num)) + '.csv' in os.listdir(path = os.getcwd() + '\\DataFrame\\01_raw') else                             print('DataFrame já carregado', end = '\n\n')

            link_num_begin = link_num_begin + 1

            if link_num_begin == link_num_end:
                break
                
except(TypeError, ConnectionError, JSONDecodeError, ConnectTimeout, HTTPError, ReadTimeout, Timeout, requests.exceptions.RequestException):
    pass

finally:
    print('Execução Terminada')


# ### Caso de uso tendo coomo base a url final

# In[99]:


data_link = ''

try:
    while data_link != None:
        for link_num in range(page_final - 1, page_final + 1):

            if re.sub('[^a-zA-Z0-9 \n\.]', '_', url_raw + str(link_num)) + '.csv' in os.listdir(path = os.getcwd() + '\\DataFrame\\01_raw'):
                print('DataFrame já carregado', end = '\n')
                
                response_url_link_num = requests.request("GET", url_raw + str(link_num), headers=headers, data = payload)
                data_link_num = json.loads(response_url_link_num.text.encode('utf8').decode('utf8')) if response_url_link_num.status_code == 200 else print('Escrever Log')
                data_link = data_link_num['next']
                

            else:
                response_url_link_num = requests.request("GET", url_raw + str(link_num), headers=headers, data = payload)
                data_link_num = json.loads(response_url_link_num.text.encode('utf8').decode('utf8')) if response_url_link_num.status_code == 200 else print('Escrever Log')
                data_link = data_link_num['next']
                
                print(url_raw + str(link_num))

                pd.DataFrame.from_dict(data_link_num['results'])                    .to_csv(os.getcwd() + '\\DataFrame\\01_raw\\' + re.sub('[^a-zA-Z0-9 \n\.]', '_', url_raw + str(link_num)) + '.csv', index = False)                         if not re.sub('[^a-zA-Z0-9 \n\.]', '_', url_raw + str(link_num)) + '.csv' in os.listdir(path = os.getcwd() + '\\DataFrame\\01_raw') else                             print('DataFrame já carregado', end = '\n\n')


                if data_link_num['next'] == None:
                    break
                
except(TypeError, ConnectionError, JSONDecodeError, ConnectTimeout, HTTPError, ReadTimeout, Timeout, requests.exceptions.RequestException):
    pass

finally:
    print('Execução Terminada')


# In[100]:


data_link is None


# ### 

# ##### Crição de uma lista ordenada dos arquivos csv salvos na raw

# In[159]:


maindir = os.getcwd()
search_dir = os.getcwd() + '\\DataFrame\\01_raw'
os.chdir(search_dir)

files = filter(os.path.isfile, os.listdir(search_dir)) #selecionando apenas arquivos
files = [os.path.join(search_dir, f) for f in files] #adiciona o diretório completo em uma lista
files.sort(key=lambda x: os.path.getmtime(x)) #ordernacao por ondem de data/hora
files = [f.replace(search_dir + '\\', '') for f in files] 

os.chdir(maindir)


# In[160]:


norm = lambda y: y.replace('.csv', '').replace('.', '_')


# In[168]:


tabelas = {}

for x in range(files.index(files[0]), (files.index(files[-1]) + 1)):

    tabelas['' + files[x].replace('.csv', '') + ''] = pd.read_csv(search_dir + '\\' + files[x], delimiter=',')

files2order = [f.replace('.csv', '') for f in files]

for key in files2order:
    tabelas[key] = tabelas.pop(key)
    
for key_rename in list(tabelas):
    tabelas[key_rename.replace('.', '_')] = tabelas.pop(key_rename)
    
locals().update(tabelas) #transformando valores do dicionário em variáveis locais


# ___________________________________________________________________________________________________________________________

# In[187]:


https___brasil_io_api_dataset_covid19_caso_full_data__page_274.head()


# ### Dividir por estados

# In[ ]:





# dash.plotly.com
# 
# elt_main.py
# 
# show_df.py
