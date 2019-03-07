#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd
import numpy as np
df = pd.read_csv('C:\\Users\\Mike friend\\Desktop\\Full_Crime_Data.csv', sep=',')


# In[119]:


df.head(10)
#Modified lat and long cut off each decimal degree at 4 places not rounded to prevent further distortion.
#this removes about 180 feet of accuracy in each direction but still gives us detailed enough location for census block info
lat_long=df[['Modified_Lat','Modified_Long']]


# In[120]:


lat_long.head(10)


# In[29]:


lat_long=lat_long.drop_duplicates()


# In[30]:


lat_long.shape


# In[76]:


# testing before massive data set test_set=lat_long.head(100)
#Pulls the census block from the FCC app
'''
import requests
from bs4 import BeautifulSoup
import time
storage_dict= {}


fcc_string1="https://geo.fcc.gov/api/census/block/find?latitude="
fcc_string2="&longitude="
fcc_string3="&showall=true&format=xml"
for index,row in lat_long.iterrows():

    new_url=fcc_string1+str(row[0])+fcc_string2+str(row[1])+fcc_string3
    page = requests.get(new_url)

    soup = BeautifulSoup(page.text, 'html.parser')
#to stop timeout requests pause for a quarter second
    time.sleep(.25)
    block=soup.find_all('block')[0]
    split_value=str(block).split('"')
    return_value=split_value[3]
    key=str(row[0])+'_'+str(row[1])
    storage_dict[key]=return_value
    
'''


# In[77]:


#new_df_dict = pd.DataFrame.from_dict(storage_dict, orient="index")


# In[79]:


#new_df_dict.to_csv('C:\\Users\\Mike friend\\Desktop\\census_block_scraped.csv')


# In[121]:


census_scrape = pd.read_csv('C:\\Users\\Mike friend\\Desktop\\census_block_scraped.csv')


# In[122]:


df['census_key']=df['Modified_Lat'].map(str)+'_'+df['Modified_Long'].map(str)


# In[123]:


census_scrape.head(1)


# In[124]:


df_merged=pd.merge(df,census_scrape, on='census_key')


# In[127]:


df_cleaned_data=df_merged[['Occur Date','UCR Literal','Tract_block']]
df_cleaned_data.head(2)
crime_categorization_dict={'LARCENY-NON VEHICLE':'PROP',
'BURGLARY-NONRES':'PROP',
'ROBBERY-RESIDENCE':'PERSONAL',
'LARCENY-FROM VEHICLE':'PROP',
'BURGLARY-RESIDENCE':'PROP',
'AUTO THEFT':'PERSONAL',
'AGG ASSAULT':'PERSONAL',
'ROBBERY-PEDESTRIAN':'PERSONAL',
'HOMICIDE':'HOMICIDE',
'ROBBERY-COMMERCIAL':'PERSONAL',
'MANSLAUGHTER':'HOMICIDE'
                          }
#Map crime types to generalized categories
df_cleaned_data['crime_cat']=df_cleaned_data['UCR Literal'].map(crime_categorization_dict)


# In[128]:



print(df_cleaned_data.head(3))


# In[129]:


dummy_variables=pd.get_dummies(df_cleaned_data['crime_cat'])


# In[130]:


df_cleaned_code=df_cleaned_data.merge(dummy_variables,left_index=True,right_index=True)


# In[131]:


print(df_cleaned_code.head(3))


# In[132]:


df_cleaned_code['Occur Date']=pd.to_datetime(df_cleaned_code['Occur Date'])

#link to get census block and tract from fips
#http://proximityone.com/geo_blocks.htm


# In[133]:


df_cleaned_code['quarter']=df_cleaned_code['Occur Date'].dt.to_period("Q")


# In[134]:


df_cleaned_code.head(3)


# In[138]:


grouped_data=df_cleaned_code.groupby(['Tract_block','quarter'])[["HOMICIDE","PERSONAL","PROP"]].sum()


# In[140]:


grouped_data.head(10)


# In[141]:


grouped_data.to_csv('C:\\Users\\Mike friend\\Desktop\\grouped_data.csv')


# In[ ]:




