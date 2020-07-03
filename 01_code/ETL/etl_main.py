#!/usr/bin/env python
# coding: utf-8

# !pip install requests

# !pip install pandas

# ##### Importando libs

# In[1]:


import pandas as pd
import requests
import json
import math
import os
import re


# In[2]:


from json import JSONDecodeError


# ##### Definindo parâmetros da chamada

# In[3]:


payload = {}
headers = {'Cookie': ''}


# ##### Definindo url e enviando chamada

# In[4]:


url_raw = "https://brasil.io/api/dataset/covid19/caso_full/data/?page="
url_base = "https://brasil.io/api/dataset/covid19/caso_full/data/?page=1"
response_url_base = requests.request("GET", url_base, headers=headers, data = payload)


# ### Definindo diretório de trabalho e função nome diretório

# In[5]:


RAW_DIR_PATH = os.getenv("RAW_DIR_PATH", os.path.join(os.getcwd(), 'DataFrame', '01_RAW'))
RAW_DIR = lambda x: os.path.join(RAW_DIR_PATH, re.sub('[^a-zA-Z0-9 \n\.]', '_', x + '.csv'))

TRUSTED_DIR_PATH = os.getenv("TRUSTED_DIR_PATH", os.path.join(os.getcwd(), 'DataFrame', '02_TRUSTED'))


# ### Carregando o resultado da chamada
# ##### A disponibilidade do link é sempre verificada 

# In[6]:


data = json.loads(response_url_base.text.encode('utf8').decode('utf8'))     if response_url_base.status_code == 200         else print('Escrever Log')


# ### Como há paginação da API e os dados crescem a cada dia, foi adicionado um um variável verificadora do link "final" da API

# In[7]:


page_final = math.ceil(data['count']/len(data['results']))

url_final = "https://brasil.io/api/dataset/covid19/caso_full/data/?page=" + str(page_final) + ""

print(url_final)


# In[8]:


data['next'], data['previous']


# In[9]:


response_url_final = requests.request("GET", url_final, headers=headers, data = payload)
data_final = json.loads(response_url_final.text.encode('utf8').decode('utf8'))
data_final['next'], data_final['previous']


# ### Salvando o resultado da requisição em formato csv, na qual estava em formato json
# ##### O arquivo apenas será salve caso ele não exista

# In[10]:


RAW_DIR_FILE = RAW_DIR(os.path.join(re.sub('[^a-zA-Z0-9 \n\.]', '_', url_base)))

pd.DataFrame.from_dict(data['results'])    .to_csv(RAW_DIR_FILE, index = False)         if not re.sub('[^a-zA-Z0-9 \n\.]', '_', url_base) + '.csv' in os.listdir(RAW_DIR_PATH)             else  print('DataFrame já carregado')


# In[11]:


link_num = 0
link_num_begin = 1
link_num_end = 10


try:
    while link_num_begin < link_num_end:
        for link_num in range(link_num_begin, link_num_end):

            if re.sub('[^a-zA-Z0-9 \n\.]', '_', url_raw + str(link_num)) + '.csv' in os.listdir(RAW_DIR_PATH):
                print('DataFrame já carregado', end = '\n')
            else:
                response_url_link_num = requests.request("GET", url_raw + str(link_num), headers=headers, data = payload)
                data_link_num = json.loads(response_url_link_num.text.encode('utf8').decode('utf8')) if response_url_link_num.status_code == 200 else print('Escrever Log')

                print(url_raw + str(link_num))

                pd.DataFrame.from_dict(data_link_num['results'])                    .to_csv(RAW_DIR(url_raw + str(link_num)), index = False)                         if not re.sub('[^a-zA-Z0-9 \n\.]', '_', url_raw + str(link_num)) + '.csv' in os.listdir(RAW_DIR_PATH) else                             print('DataFrame já carregado', end = '\n\n')

            link_num_begin = link_num_begin + 1

            if link_num_begin == link_num_end:
                break
                
except(TypeError, ConnectionError, JSONDecodeError, requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError, requests.exceptions.ReadTimeout, requests.exceptions.Timeout, requests.exceptions.RequestException):
    pass

finally:
    print('Execução Terminada')


# ### Caso de uso tendo como base a url final

# In[12]:


data_link = ''

try:
    while data_link != None:
        for link_num in range(page_final - 1, page_final + 1):

            if re.sub('[^a-zA-Z0-9 \n\.]', '_', url_raw + str(link_num)) + '.csv' in os.listdir(RAW_DIR_PATH):
                print('DataFrame já carregado', end = '\n')
                
                response_url_link_num = requests.request("GET", url_raw + str(link_num), headers=headers, data = payload)
                data_link_num = json.loads(response_url_link_num.text.encode('utf8').decode('utf8')) if response_url_link_num.status_code == 200 else print('Escrever Log')
                data_link = data_link_num['next']
                

            else:
                response_url_link_num = requests.request("GET", url_raw + str(link_num), headers=headers, data = payload)
                data_link_num = json.loads(response_url_link_num.text.encode('utf8').decode('utf8')) if response_url_link_num.status_code == 200 else print('Escrever Log')
                data_link = data_link_num['next']
                
                print(url_raw + str(link_num))

                pd.DataFrame.from_dict(data_link_num['results'])                    .to_csv(RAW_DIR(url_raw + str(link_num)) + '.csv', index = False)                         if not re.sub('[^a-zA-Z0-9 \n\.]', '_', url_raw + str(link_num)) + '.csv' in os.listdir(RAW_DIR_PATH) else                             print('DataFrame já carregado', end = '\n\n')


                if data_link_num['next'] == None:
                    break
                
except(TypeError, ConnectionError, JSONDecodeError, requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError, requests.exceptions.ReadTimeout, requests.exceptions.Timeout, requests.exceptions.RequestException):
    pass

finally:
    print('Execução Terminada')


# In[13]:


data_link is None


# ##### Crição de uma lista ordenada dos arquivos csv salvos na raw

# In[14]:


maindir = os.getcwd()
os.chdir(RAW_DIR_PATH)

files = filter(os.path.isfile, os.listdir(RAW_DIR_PATH)) #selecionando apenas arquivos
files = [os.path.join(RAW_DIR_PATH, f) for f in files] #adiciona o diretório completo em uma lista
files.sort(key=lambda x: os.path.getmtime(x)) #ordernacao por ondem de data/hora
files = [f.replace(RAW_DIR_PATH + os.path.sep, '') for f in files] #linux

os.chdir(maindir)


# In[15]:


norm = lambda y: y.replace('.csv', '').replace('.', '_')


# In[16]:


tabelas = {}

for x in range(files.index(files[0]), (files.index(files[-1]) + 1)):

    tabelas['' + files[x].replace('.csv', '') + ''] = pd.read_csv(RAW_DIR_PATH + os.path.sep + files[x], delimiter=',')

files2order = [f.replace('.csv', '') for f in files]

for key in files2order:
    tabelas[key] = tabelas.pop(key)
    
for key_rename in list(tabelas):
    tabelas[key_rename.replace('.', '_')] = tabelas.pop(key_rename)
    
locals().update(tabelas) #transformando valores do dicionário em variáveis locais


# ___________________________________________________________________________________________________________________________

# ### Empilhando os Dados Baixados

# In[17]:


df = pd.DataFrame(None, columns = list(eval(list(tabelas.keys())[0]).head()[0:0]))


# In[18]:


for f in range(0, len(tabelas)):
    df = df.append(eval(list(tabelas)[f]))
    
df = df.reset_index()

del df['index']


# In[19]:


df.to_csv(os.path.join(TRUSTED_DIR_PATH, 'all.csv'), index = False)


# ### Dividir por estados

# In[20]:


for s in set(df.state):
    df[df.state == s].to_csv(os.path.join(TRUSTED_DIR_PATH, str(s.lower()) + '.csv'), index = False)


# dash.plotly.com
# 
# elt_main.py
# 
# show_df.py
