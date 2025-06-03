#!/usr/bin/env python
# coding: utf-8

# # How Do People Die in the USA? A Visualization of Mortality

# **Death** is a difficult topic, but it is crucial for government, healthcare, economy, and medicine. Understanding how people die can lead to changes in research funding or strengthening preventive measures against certain contemporary diseases.
# 
# In the USA, **Centers for Disease Control and Prevention (CDC)** collected [mortality data](https://wonder.cdc.gov/ucd-icd10.html) from 1999 to 2015. The data is rich in demographic information, including age at death, the disease causing it, gender, race, and geographical location (city/state).
# 
# This data will help us answer many **questions about death**:
# - What are the leading causes of death in the USA?
# - Are men or women more likely to die? Does it depend on the cause of death? Or the age?
# - Which causes of death are becoming more or less common over time?

# ## Import library **Matplotlib**

# To begin with, I installed all the necessary libraries for constructing graphs.

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')

import sys


# ## Data Output

# First, I open file `deaths.csv`:

# In[3]:


df = pd.read_csv("data/deaths.csv", encoding='GBK') 
df


# ## Data Exploring

# #### Top 10 lines:

# In[3]:


df.head(10)


# #### The bottom 5 rows:

# In[5]:


df.tail(5)


# #### Range of age values in the data:

# In[6]:


df.Age.describe()


# #### Years represented in the dataset:

# In[7]:


df['Year'].unique()


# #### Are both genders represented in the dataset?

# In[8]:


df['Gender'].unique()


# #### Key statistical characteristics of the number of deaths:

# In[9]:


count_deaths = df['Deaths'].count()
print('Number of deaths:', count_deaths)
mean_deaths = df['Deaths'].mean()
print('The average number of deaths:', mean_deaths)
std_deaths = df['Deaths'].std()
print('Standard deviation:', std_deaths)
min_deaths = df['Deaths'].min()
print('Minimum number of deaths:', min_deaths)
max_deaths = df['Deaths'].max()
print('Maximum number of deaths:', max_deaths)


# #### Causes of death represented in the dataset:

# In[10]:


causes = pd.DataFrame(df['Cause'].unique(), columns=['Death Cause'])
causes = causes.sort_values(by='Death Cause')
causes.index = range(0, len(causes)) 
causes


# ## Deaths: by year

# In[11]:


df.head(3)


# #### The total number of deaths recorded for 2005, 2010, and 2015?

# First, I grouped the data by years, then separately, I determined the total deaths by year based on the **Deaths** column.

# In[12]:


by_year = df.groupby("Year").Deaths.sum()
by_year


# After grouping, building plots is easy. Using **`.plot()`**, I just need to choose the type of plot:

# In[14]:


df.groupby("Year")\
.Deaths\
.sum()\
.plot(kind="bar")


# ## Divide the data by years

# First of all, narrow down my investigation to **fatalities for the year 2015**.

# ## Deaths: Men vs Women

# Which gender had the highest mortality rate in 2015?

# In[15]:


df2015 = df[df.Year == 2015]

df2015\
.groupby("Gender")\
.Deaths\
.sum()


# #### Now, I create a simple bar chart to compare the total number of deaths by gender.

# In[17]:


df2015\
.groupby("Gender")\
.Deaths\
.sum()\
.plot(kind="bar", color=["red", "blue"])


# ## Mortality: by age

# What caused people to die in 2015?

# In[18]:


causes = df2015.groupby('Cause')['Deaths'].sum().reset_index()
causes


# Or in another way:

# In[19]:


causes.set_index('Cause').plot(kind='bar', color='olive', figsize=[40, 10])


# <font color="green"> **Conclusions**:</font>
# 1. The most prevalent diseases - heart disease, malignant neoplasms.
# 2. The least prevalent - acute poliomyelitis; arthropod-borne viral encephalitis; measles; scarlet fever and diphtheria. </font>

# ## Mortality: by age and gender

# #### Does gender affect the age of death?

# In[20]:


df2015\
.groupby(["Age", "Gender"])\
.Deaths\
.sum()


# #### Create two subplots - one for female and one for male mortality by age accordingly.

# In[21]:


df2015\
.groupby(["Age", "Gender"])\
.Deaths\
.sum()\
.unstack(1)\
.plot(kind="bar", color=["red", "blue"], figsize=[18, 10], subplots=True)


# <font color="green"> **Conclusions**: </font>
# 1. First months of life: males (higher mortality).
# 2. Up to 13 years old: approximately the same.
# 3. Up to 84 years old: males (higher mortality).
# 4. Up to 100 years old: females (higher mortality).

# In[22]:


df2015\
.groupby(["Age", "Gender"])\
.Deaths\
.sum()\
.unstack(1)\
.plot(kind="bar", color=["red", "blue"], figsize=[18, 10], stacked=True)


# I would combine the two graphs... 
# However, it's not very informative because it's difficult to compare male and female indicators in a single bar chart.

# <font color="green"> **That would be suitable for**: </font>
# 1. Comparison of one characteristic across different types.
# 2. Sales of different types of products across different points.

# #### Since `Age` is a continuous variable, it would be appropriate to use a line plot for comparison.

# In[23]:


df2015\
.groupby(["Age", "Gender"])\
.Deaths\
.sum()\
.unstack(1)\
.plot(kind="line", figsize=[18, 10], subplots=True)


# Now, using only lines, it's easy to compare the difference between genders by age on **one line graph**.

# In[25]:


df2015\
.groupby(["Age", "Gender"])\
.Deaths\
.sum()\
.unstack(1)\
.plot(kind="line", color=["red", "blue"], figsize=[18, 6], title = "Deaths in 2015 by Age and Gender")

plt.ylabel('Deaths')
plt.show()


# ## Mortality: Top causes of death in 2015

# In[30]:


df2015\
.groupby(["Cause"])\
.agg({'Deaths' : 'sum'}).sort_values('Deaths', ascending=True)\
.plot(kind="barh", legend=False, color="black", figsize=[9, 12])


# #### Top 10 most prevalent causes of mortality:

# In[31]:


df2015\
.groupby(['Cause'])\
.agg({'Deaths' : 'sum'})\
.sort_values('Deaths', ascending=True) [-10:]\
.plot(kind="barh", legend=False, color="black", figsize=[9, 12])


# ## Mortality: Top causes of death by age

# In[32]:


df\
.groupby(["Cause","Year"])\
.agg({'Deaths': 'sum'})\
.sort_values('Deaths', ascending = False)\
.unstack(1)\
.plot(kind="barh", legend=True, figsize=[10, 24])


# The visualization above contains a lot of information (perhaps too much). However, it's easy to notice that **mortality due to HIV infection has been decreasing every 5 years, starting from 2005!**

# ## Mortality: Causes of death by gender

# In[33]:


df\
.groupby(['Cause', 'Gender'])\
.agg({'Deaths': 'sum'})\
.sort_values('Deaths', ascending=True)\
.unstack(1)\
.plot(kind='barh', legend=True, figsize=[10, 24])


# ## Mortality: Causes of death by age

# Since the dataset contains a large number of causes of death, I've selected only a few for visualization:
# 
# - "Alzheimer's disease"
# - "Diseases of heart"
# - "Malignant neoplasms"
# - "Accidents (unintentional injuries)"

# In[34]:


clist = ["Alzheimer's disease", 
         "Diseases of heart", 
         "Malignant neoplasms", 
         "Accidents (unintentional injuries)"]

df2015_clist = df2015[df2015["Cause"].isin(clist)] #isin

df2015_clist\
.groupby(["Age", "Cause"])\
.agg({'Deaths': 'sum'})\
.sort_values('Deaths', ascending=False)\
.unstack(1)\
.plot(kind="line", legend=True, figsize=[10, 6])


# <font color="green"> **Conclusions**: </font>
# 1. Mortality due to unintentional injuries is almost constant.
# 2. Mortality due to Alzheimer's disease remains constant until 70 years old, then increases until 90 years old, and decreases afterward.
# 3. Mortality due to heart diseases increases from 19 years old to 90. It then sharply decreases after 90.
# 4. Mortality due to malignant neoplasms increases from 20 years old to 70. It then sharply decreases after 70.

# ## Mortality: causes of death by gender and age

# Creating such a visualization is quite challenging because there are 2 genders x 3 years x 51 causes of death. It's practically impossible to represent all this data on one graph and analyze it.
# 
# The best approach would be to visualize only a portion of the data or just the most interesting information.

# In[36]:


clist = df.Cause.unique()[:5]

for cause in clist:
    df2015_clist = df2015[df2015["Cause"].isin([cause])]
    
    df2015_clist\
    .groupby(["Age", "Gender"])\
    .agg({'Deaths': 'sum'})\
    .unstack([1])\
    .plot(kind="line", legend=True, color=('r', 'b'), figsize=[10, 8], title=str(cause))


# <font color="green">**Overall conclusions**:</font>
# 1. The most common causes of death across all years are heart diseases and malignant neoplasms.
# 2. The least common are acute poliomyelitis; arthropod-borne viral encephalitis; measles; scarlet fever; and diphtheria.
# 3. The number of deaths is generally higher among men than women.
# 4. Mortality due to unintentional injuries remains almost constant throughout life, depending on Alzheimer's disease, heart diseases, and neoplasms.
# 5. Higher mortality is observed among both men and women from 75 to 100 years old.
