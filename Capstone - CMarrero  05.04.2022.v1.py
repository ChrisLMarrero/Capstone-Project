#!/usr/bin/env python
# coding: utf-8

# Creator: Christopher Marrero

# Capstone Project 2022 Data Analytics Class      
# Title: NY Chemical Dependence Treatment Admissions for age 55 and older
# 

# To create awareness on the substance abuse crisis which is demolishing our older population, there is a stigma between substance abuse and the younger population. My goal with this analysis is to provide information that shows that substance abuse is an issue amongst not only young adults but also individuals that are 55 years or older. Hopefully, this data can motivate groups to spend time in the NYC area and advocate for early  substance abuse prevention. 
# 

# Questions that i would like to asnwer.     
# 1.Which are the top 2 substances causing the Admissions ?        
# 2.Which were the years with the most and least admissions ?      
# 3.Which county has the most and least  admissions ?       
# 4.How are the Admissions distributed amongst Males/Females ?      
# 5.What are the type of facilities receiving the admissions ?     
# 

# In[1]:


#Code to expand the margin of the Jupyter Notebook. This allows for better viewing of code. 

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))


# In[2]:


# Python Library imports to complete the data analysis. 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from IPython.display import display_html 


# In[3]:


#Source - catalog.data.gov
# Title - Chemical Dependence Treatment Program Admissions for 55 and Older: Beginning 2007

dataset= pd.read_csv ('https://data.ny.gov/api/views/5xvm-4zc6/rows.csv')


# In[5]:


# code to review Data Frame at a glance and understand basic data column/row composition in order to understand how to approach the Analysis

dataset.head()


# In[6]:


#code to retrieve the data type of each column and select the type of aggregation. Also, to understand if the is Null values on the data.

dataset.info()


# In[7]:


#code to run a quick statistical analysis on the data. 

dataset.describe()


# In[8]:


#code to drop column 'Service Type' from the data frame since it will not be used on the analysis. 

dataset.drop('Service Type', axis=1, inplace=True)


# In[9]:


#code to turn the column 'Year' to a string since no aggregation is needed on this column and would need it to be discrete for better data analysis. Per dataset.decribe() it is being read as an integer.

dataset['Year'] = dataset["Year"].apply(str)


# In[10]:


# Code to get a list of all available counties in the data frame
# According to the .Value_Counts () - there is a total of 62 counties on the dataset. The focus of the analysis will be based on the 5 NYC Counties (Brooklyn, Bronx, Manhattan, Queens & Staten Island).

dataset['County of Residence'].value_counts()


# In[12]:


#Code to rename counties. The dataset provides the formal name of the counties. This replace will allow me to update the name to their more known names. 

dataset['County of Residence'].replace({'New York':'Manhattan'}, inplace = True)
dataset['County of Residence'].replace({'Kings':'Brooklyn'}, inplace = True)
dataset['County of Residence'].replace({'Richmond':'Staten Island'}, inplace = True)


# In[13]:


#Code to determine the type of substances causing the admissions in the facilities. 

dataset['Primary Substance Group'].value_counts()


# In[14]:


#Code to clean up the names of the Substances to a more cleaner format. 

dataset['Primary Substance Group'].replace({'Cocaine incl Crack':'Cocaine/Crack'}, inplace = True)
dataset['Primary Substance Group'].replace({'Other Opioids':'Opioids'}, inplace = True)
dataset['Primary Substance Group'].replace({'Marijuana incl Hashish':'Marijuana'}, inplace = True)
dataset['Primary Substance Group'].replace({'All Others':'Other'}, inplace = True)


# In[15]:


#Code to create a list of  the New York City 5 counties that will be composing the analysis.

searchfor = ['Bronx','Brooklyn','Manhattan','Queens','Staten Island']


# In[16]:


#Code to exclude all other counties from the data frame and only keep the ones declared on the 'Search For' list. this would allow for the analysis to focus on the 5 counties which is part of the Healthfirst network. 

dataset1 = dataset[dataset['County of Residence'].str.contains('|'.join(searchfor))]


# In[18]:


#Code to run a statical analysis on the Admission by Year to answer question 2 (Which were the years with the most and least admissions ?)  also to see the YoY trend of admissions over the course of 14 Years. 

#Below data shows that 2007 is the year with least admissions & 2019 sustained the highest admissions. also the trend shows a steady growth of admissions into Substance abuse facilities. 

tableyear = dataset1.groupby(['Year']).agg({'Admissions':[np.mean, np.sum, np.min, np.max]})
dataset1.groupby(['Year'])['Admissions'].sum().plot.barh(width=0.5,color=['purple'],title='Sum of admissions by year')
print(tableyear)


# In[19]:


#Code to run a statical analysis on the admissions by counties to answer question 3. (Which county has the most and least admissions ?). 

#Below data shows that Manhattan has the highest  admission ( 75,194 ) of all the counties. Staten Island has the least admissions (12,678).

tablecounty = dataset1.groupby(['County of Residence']).agg({'Admissions':[np.mean, np.sum, np.min, np.max]})
dataset1.groupby(['County of Residence'])['Admissions'].sum().plot.barh(width=0.5,color=['blue'],title='Sum of Admissions by county')
print(tablecounty)


# In[20]:


#Code to run a statical analysis on the admissions by Gender to answer question 4.( How are the Admissions distributed amongst Males/Females ?)

# Below data shows that Females have the least amount of admissions at (44,844 ). Males have the most admissions at a total of (196,431 ) 
#This large difference opens the door to a future analysis of why is the Gender admission distribution so one sided. 

tablegender = dataset1.groupby(['Gender']).agg({'Admissions':[np.mean, np.sum, np.min, np.max]})
dataset1.groupby(['Gender'])['Admissions'].sum().plot.barh(width=0.3,color=['orange'],title='Sum of Admissions by county')
print(tablegender)


# In[21]:


#Code to run a statical analysis on the admissions by substance  to answer question 1.( Which are the top 2 substances causing the Admissions ?)

# Below data shows that Alcohol (138,411) & Heroin (61,338)  are the top 2 leading substances of the course of 14 Years. 

tabletype = dataset1.groupby(['Primary Substance Group']).agg({'Admissions':[np.mean, np.sum, np.min, np.max]})
dataset1.groupby(['Primary Substance Group'])['Admissions'].sum().plot.barh(width=0.5,color=['gray'],title='Sum of Substance Type')
print(tabletype)


# In[22]:


#Code to run a statical analysis on the admissions by Facility type  to answer question 5. (What are the type of facilities receiving the admissions ?) 

# Below data shows that there are 6 different types of facilities receiving the admissions. Crisis Facilities receive the most admissions at (109,025)

tablecategory = dataset1.groupby(['Program Category']).agg({'Admissions':[np.mean, np.sum, np.min, np.max]})
dataset1.groupby(['Program Category'])['Admissions'].sum().plot.barh(width=0.7,color=['green'],title='Sum of Program')
print(tablecategory)


# In[23]:


#Code below to understand how admission is distributed by Substance, County and gender. 

dataset1.groupby(['Primary Substance Group','County of Residence','Gender']).agg({'Admissions':[np.mean, np.sum, np.max]})


# #Conclusion       
# The analysis determined that our 55 or older population in NYC is undergoing substance abuse issues. With Alcohol (138,411) and Heroin (61,338)  being the top 2 leading substances. Over the course of 14 years, Manhattan is the county with the highest total admissions of 37.17% - 75,194. Unfortunately, 45.19%  - 709,025 of all admissions are at a crisis/potential overdose state. 2007 was the year with the least admissions at 11,782 & 2019 sustained the highest amount of admissions at 24,922. 
# 
# One of the biggest take away from the analysis is the large difference between Male/Female admissions. The Male population is > 80% of all admissions. This also opens the door to a study of why the large gap between the genders. 
#  
# Hopefully, data like this can initiate programs that can assist the prevention of Substance abuse cases within NYC. This would be in the interest of insurance companies such as Health First since although we offer benefits to our Medicare members preventing these admissions can assist with long term cost sustained by the company since overdose and/or sustained usage of this drugs can lead to long term effects and health complications
# 

# In[ ]:


#Code to Extract the Cleaned up data and load into a visualtion tool such as Tableau to create a dynamic dashboard. 

dataset1.to_excel(r'C:\Users\CMarrero\OneDrive - Healthfirst\Desktop\Capstone\CapstoneExtract.xlsx', index = False)

