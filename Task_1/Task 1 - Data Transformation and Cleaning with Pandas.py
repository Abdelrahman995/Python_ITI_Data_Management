#!/usr/bin/env python
# coding: utf-8

# ### Step 0
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.

# In[1]:


import os 
import numpy as np
import pandas as pd
os.getcwd()


# In[2]:



# Let's investigate the dataset at first
energy = pd.read_excel('data/Energy Indicators.xls',     
                                skiprows = [i for i in range(1,18)]+[i for i in range(245,284)],        
                                header = 0)
# View info
energy.info()           # 18 -> 245   =  227     # number of rows that we need


# In[3]:


energy


# In[4]:


energy = energy.drop(columns =['Unnamed: 0','Unnamed: 2'])


# In[5]:


energy


# In[6]:


energy.rename(columns = {'Unnamed: 1' : 'Country', 'Unnamed: 3': 'Energy Supply', 'Unnamed: 4': 'Energy Supply per Capita', 'Unnamed: 5': '% Renewable'}, inplace = True)
energy


# In[7]:


energy.isnull().sum()


# ### Replacing ... with NaN

# In[8]:


energy = energy.replace(to_replace = "..." , value = np.nan)
energy
            


# In[9]:


energy.isnull().sum()


# In[10]:


energy = energy.replace(to_replace = "Republic of Korea" , value = "South Korea")
energy = energy.replace(to_replace = "United States of America" , value = "United States")
energy = energy.replace(to_replace = "United Kingdom of Great Britain and Northern Ireland" , value = "United Kingdom")
energy = energy.replace(to_replace = "China, Hong Kong Special Administrative Region" , value = "Hong Kong")


# In[11]:


new_country =[]
for i in energy['Country']:
    if "(" in i:
        new_country.append(i[:i.index("(")-1])   # because it has a space before (  from begin to (
        continue
    new_country.append(i)
energy['Country'] = new_country

for i in energy['Country']:
    print(i)


# In[12]:


energy


# ### Step 1
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>

# In[13]:


GDP = pd.read_csv('data/world_bank.csv',     
                                skiprows = [i for i in range(0,4)],        
                                header = 0)
# View info
#world_bank.info()       
GDP.head(3)


# In[14]:


GDP['Country Name'] = GDP['Country Name'].replace('Korea, Rep.','South Korea')
GDP['Country Name'] = GDP['Country Name'].replace('Iran, Islamic Rep.','Iran')
GDP['Country Name'] = GDP['Country Name'].replace('Hong Kong SAR, China','Hong Kong')


# ### Step 2
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.

# In[15]:


ScimEn = pd.read_excel('data/scimagojr-3.xlsx')
ScimEn.head(3)    


# ### Step 3
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This step should yeild a DataFrame with 20 columns and 15 entries.*

# In[16]:


GDP = GDP[['Country Name','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
GDP.columns = ['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015'] #only last 10 years
ScimEn_m = ScimEn[:15]
GDP.head(3)


# In[17]:


ScimEn_m.head(3)   #Only first 15 rows


# In[18]:


energy.head(3)


# In[19]:


df_temp = pd.merge(ScimEn_m,energy,how='inner',left_on='Country',right_on='Country')
df_final = pd.merge(df_temp,GDP,how='inner',left_on='Country',right_on='Country')#left_on specifiec merge col name in left df
df_final = df_final.set_index('Country')                                #right_on specifiec merge col name in right df
df_final.head(3) 


# In[20]:


df_final.shape     # 20 columns and 15 entries    Same ^_^


# ### Step 4
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This step should yield a single number.*

# In[21]:


ScimEn_temp = pd.read_excel('data/scimagojr-3.xlsx')
df_temp = pd.merge(ScimEn_temp,energy,how='inner',left_on='Country',right_on='Country')
df_final_temp = pd.merge(df_temp,GDP,how='inner',left_on='Country',right_on='Country')#left_on specifiec merge col name in left df
df_final_temp.shape
print("entries lose " , 162-15)


# ### Step 5
# 
# #### Answer the following questions in the context of only the top 15 countries by Scimagojr Rank 
# 
# 
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This step should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[22]:


avgGDP = df_final[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].mean(axis=1).rename('avgGDP').sort_values(ascending=False)
avgGDP                      # AVERAGE  GDP  each country  on last 10 years


# ### Step  6
# What is the mean `Energy Supply per Capita`?
# 
# *This step should return a single number.*

# In[23]:


df_final['Energy Supply per Capita'].mean()


# ### Step 7
# What country has the maximum % Renewable and what is the percentage?
# 
# *This step should return a tuple with the name of the country and the percentage.*

# In[24]:


max_renewable = max(df_final['% Renewable'])
indx = 0 
for i in df_final ['% Renewable']:
    if i == max_renewable:
        df_final['Rank'][indx]
    else:
        indx = indx + 1 
Contry = df_final.index[indx] 
ans = ()
ans = (Contry,max_renewable)
print(ans , type(ans))


# ### Step 8
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This step should return a tuple with the name of the country and the ratio.*

# In[25]:


df_final['Citation Ratio'] = df_final['Self-citations']/df_final['Citations']
ans = df_final[df_final['Citation Ratio'] == max(df_final['Citation Ratio'])]
#print(ans, type(ans))
print("Country : ", ans.index.tolist()[0] ,"      "," Max Value : ", ans['Citation Ratio'].tolist()[0])


# ### Step 9
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This step should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[26]:


df_final['HighRenew'] = [1 if x >= df_final['% Renewable'].median() else 0 for x in df_final['% Renewable']]
df_final['HighRenew']


# ### Step 10
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[27]:


ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

df_final = df_final.reset_index()
for country in df_final['Country'] :
    df_final['Continent'] = ContinentDict[country]                    # making col  continent 

df_final['Continent']= df_final['Country'].map(ContinentDict)
df_final['Population'] = (df_final['Energy Supply'] / df_final['Energy Supply per Capita']).astype(float)

PopSize = df_final.groupby('Continent').agg({'Continent':np.size})  # PopSize is DF contain each continent size 
PopSum = df_final.groupby('Continent').agg({'Population':np.sum})
PopMean = df_final.groupby('Continent').agg({'Population':np.average})
PopStd = df_final.groupby('Continent').agg({'Population':np.std})     

PopTotal = pd.concat([PopSize,PopSum,PopMean,PopStd],axis=1)
PopTotal.columns = ['size', 'sum', 'mean', 'std']
PopTotal

