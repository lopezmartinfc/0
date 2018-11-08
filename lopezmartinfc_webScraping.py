#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import sys
import csv
import re


# # Web Scraping

# In[2]:


from requests import get
url = 'https://www.imdb.com/search/title?release_date=2018&sort=num_votes,desc&page=1'


# In[3]:


response = get (url)
print (response.text[:500])


# ## BeautifulSoup para analizar el contenido HTML

# In[5]:


from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, 'html.parser')
type (soup)


# In[6]:


peliculas_containers = soup.find_all('div', class_='lister-item mode-advanced')
print(type(peliculas_containers))
print(len(peliculas_containers))


# In[7]:


primera  = peliculas_containers[0]
primera


# In[8]:


primera.div


# In[9]:


primera.a


# In[10]:


primera.h3


# In[11]:


primera.h3.a


# El nombre de la primera película que aparece en la web

# In[12]:


primera.h3.a.text


# In[13]:


primer_anio = primera.h3.find('span', class_= 'lister-item-year text-muted unbold')
primer_anio


# In[ ]:


Y su año


# In[14]:


primer_anio = primer_anio.text
primer_anio


# In[ ]:


Calificación de la primera película


# In[15]:


primera.strong

primera_imdb = float(primera.strong.text)
primera_imdb


# In[ ]:


El metastore 


# In[16]:


primera_mscore = primera.find('span', class_ = 'metascore favorable')

primera_mscore = int(primera_mscore.text)
print(primera_mscore)


# In[18]:


primera_votes = primera.find('span', attrs = {'name':'nv'})
primera_votes


# In[ ]:


Número de votos


# In[20]:


primera_votes['data-value']


# In[21]:


primera_votes = int(primera_votes['data-value'])


# In[ ]:


Declaración de las variables para crear depués el datastore


# In[27]:


nombres = []
anios = []
imdb_ratings = []
metascores = []
votes = []

for container in peliculas_containers:

    
    if container.find('div', class_ = 'ratings-metascore') is not None:

       
        nombre = container.h3.a.text
        nombres.append(nombre)

        
        anio = container.h3.find('span', class_ = 'lister-item-year').text
        anios.append(anio)

        
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        
        m_score = container.find('span', class_ = 'metascore').text
        metascores.append(int(m_score))

        
        vote = container.find('span', attrs = {'name':'nv'})['data-value']
        votes.append(int(vote))




# In[32]:


import pandas as pd

df_movies = pd.DataFrame({'movie': nombres,
                       'year': anios,
                       'imdb': imdb_ratings,
                       'metascore': metascores,
                       'votes': votes})
print(df_movies.info())
df_movies


# Exportación de los datos a csv

# In[33]:


df_movies.to_csv('movies.csv')

