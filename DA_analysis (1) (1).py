#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('newdatasetlib.csv')

# Preliminary data check
print(data.info())
print(data.head())


# In[2]:


# Check for missing data
sns.heatmap(data.isnull(), cbar=False, cmap='viridis')
plt.title('Missing Data Matrix')
plt.show()


# In[4]:


# Load the dataset again to ensure it's fresh for this operation.
data = pd.read_csv('newdatasetlib.csv')

# Check the data types of the columns we're interested in
data_types = data.dtypes
print(data_types)

# If the columns are not of object type (which are usually strings), 
# we need to convert them to strings before replacing commas and converting to numeric.
cols_to_clean = ['B2.9  Total Operating Revenues', 'F2.1.P  No. of programs held annually']
for col in cols_to_clean:
    if data[col].dtype == 'object':
        data[col] = pd.to_numeric(data[col].str.replace(',', ''), errors='coerce')
    else:
        data[col] = pd.to_numeric(data[col], errors='coerce')

# Now that the data is cleaned, let's generate the correlation matrix.
correlation_matrix = data[cols_to_clean].corr()

# Output the data types and the correlation matrix
correlation_matrix


# In[6]:


# Load the dataset again
data = pd.read_csv('newdatasetlib.csv')

# Check the data types of the columns of interest
data_types_before = data.dtypes

# Conditionally convert columns to numeric if they are not already
# Convert 'B2.9 Total Operating Revenues' if it's not numeric
if not pd.api.types.is_numeric_dtype(data['B2.9  Total Operating Revenues']):
    data['B2.9  Total Operating Revenues'] = pd.to_numeric(data['B2.9  Total Operating Revenues'].str.replace(',', ''), errors='coerce')

# Convert 'A1.14 No. of Active Library Cardholders' if it's not numeric
if not pd.api.types.is_numeric_dtype(data['A1.14  No. of Active Library Cardholders']):
    data['A1.14  No. of Active Library Cardholders'] = pd.to_numeric(data['A1.14  No. of Active Library Cardholders'].str.replace(',', ''), errors='coerce')

# Check the data types after conversion
data_types_after = data.dtypes

# Create the scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='B2.9  Total Operating Revenues', y='A1.14  No. of Active Library Cardholders')
plt.title('Scatter Plot of Total Operating Revenues vs. Number of Active Library Cardholders')
plt.xlabel('Total Operating Revenues')
plt.ylabel('Number of Active Library Cardholders')
plt.show()

# Output the data types for verification
data_types_before, data_types_after



# In[7]:


# Create a scatter plot to explore the relationship between 'Number of Programs Held Annually' 
# and 'Number of Active Library Cardholders'.

# Before plotting, let's ensure the 'F2.1.P No. of programs held annually' column is in a numeric format.
if not pd.api.types.is_numeric_dtype(data['F2.1.P  No. of programs held annually']):
    data['F2.1.P  No. of programs held annually'] = pd.to_numeric(data['F2.1.P  No. of programs held annually'].str.replace(',', ''), errors='coerce')

# Now, let's create the scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='F2.1.P  No. of programs held annually', y='A1.14  No. of Active Library Cardholders')
plt.title('Scatter Plot of Number of Programs Held Annually vs. Number of Active Library Cardholders')
plt.xlabel('Number of Programs Held Annually')
plt.ylabel('Number of Active Library Cardholders')
plt.show()



# In[9]:


from scipy import stats
import numpy as np
# Calculate IQR and Z-score for relevant columns
columns_to_analyze = ['B2.9  Total Operating Revenues', 'F2.1.P  No. of programs held annually', 'A1.14  No. of Active Library Cardholders']

# Statistical Summary
statistical_summary = data[columns_to_analyze].describe()

# IQR Method
Q1 = data[columns_to_analyze].quantile(0.25)
Q3 = data[columns_to_analyze].quantile(0.75)
IQR = Q3 - Q1
outliers_iqr = ((data[columns_to_analyze] < (Q1 - 1.5 * IQR)) | (data[columns_to_analyze] > (Q3 + 1.5 * IQR)))

# Z-Score Analysis
z_scores = np.abs(stats.zscore(data[columns_to_analyze].dropna()))
outliers_z_score = (z_scores > 3)

# Visualize with Boxplots
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 6))
for i, col in enumerate(columns_to_analyze):
    sns.boxplot(x=data[col], ax=axes[i])
    axes[i].set_title(f'Boxplot of {col}')
plt.tight_layout()
plt.show()

(statistical_summary, outliers_iqr.sum(), outliers_z_score.sum())



# In[ ]:




