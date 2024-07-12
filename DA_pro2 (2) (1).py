#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd

data_2017 = pd.read_csv('2017.csv')
data_2018 = pd.read_csv('2018.csv')
data_2019 = pd.read_csv('2019.csv')
data_2020 = pd.read_csv('2020.csv')





# In[5]:


combined_data = pd.concat([data_2017, data_2018, data_2019, data_2020])


# In[7]:


import pandas as pd

# Step 1: Selecting Relevant Columns
relevant_columns = [
    'Survey Year From', 'Library Full Name', 'A1.10 City/Town', 
    'A1.14  No. of Active Library Cardholders', 
    'F2.1.P  No. of programs held annually', 
    'B2.9  Total Operating Revenues'
]
new_data = combined_data[relevant_columns]
# Step 2: Cleaning the Data
# Convert numeric columns to appropriate data types and handle missing values
numeric_columns = ['A1.14  No. of Active Library Cardholders', 'F2.1.P  No. of programs held annually', 'B2.9  Total Operating Revenues']
new_data[numeric_columns] = new_data[numeric_columns].apply(pd.to_numeric, errors='coerce')
new_data.fillna(0, inplace=True)  # Replace NaN with 0

# Step 3: Saving the New Datasheet
new_data.to_csv('new_threee_datasheet.csv', index=False)


# In[8]:


# Group the data by 'City/Town' and 'Survey Year From' and count the unique libraries.
library_counts = combined_data.groupby(['A1.10 City/Town', 'Survey Year From'])['Library Full Name'].nunique().reset_index()

# Now, we will create a pivot table with 'City/Town' as the index and the years as columns to show the counts.
# We fill any missing values with 0, assuming that no record means no library.
library_pivot = library_counts.pivot_table(index='A1.10 City/Town', 
                                           columns='Survey Year From', 
                                           values='Library Full Name', 
                                           aggfunc='sum').fillna(0)

# The pivot table is now ready to be displayed. Here, we'll simply print it out.
library_pivot


# In[50]:


# Sum the number of libraries in each city across all years.
city_library_totals = data.groupby('A1.10 City/Town')['Library Full Name'].nunique()

# Now let's create a pie chart for this data. Given the potential number of cities, we'll limit the chart to the top 10 cities.
top_cities = city_library_totals.nlargest(10)

# Create the pie chart
plt.figure(figsize=(8, 8))
top_cities.plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title('Top 10 Cities/Towns by Number of Libraries (2017-2020)')
plt.ylabel('')  # Removing the y-label as it's not needed for pie charts
plt.show()



# In[27]:


# Clean the 'A1.14 No. of Active Library Cardholders' column
combined_data['A1.14  No. of Active Library Cardholders'] = combined_data['A1.14  No. of Active Library Cardholders'] \
    .replace({',': ''}, regex=True).astype(float)
#Creating pivot table 
pivot_table = combined_data.pivot_table(
    index='Library Full Name',
    columns='Survey Year From',
    values='A1.14  No. of Active Library Cardholders',
    aggfunc='sum',
    fill_value=0
)
# Reset the index so 'Library Full Name' is a column and not the index
pivot_table.reset_index(inplace=True)
# Display the pivot table
pivot_table.head()  # Show the first few rows of the pivot table


# In[49]:


# Sum the 'No. of Active Library Cardholders' for each year.
yearly_totals = combined_data.groupby('Survey Year From')['A1.14  No. of Active Library Cardholders'].sum()

# Now let's create a pie chart for this data
plt.figure(figsize=(8, 8))
yearly_totals.plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title('Total Number of Active Cardholders by Year (2017-2020)')
plt.ylabel('')  # Removing the y-label as it's not needed for pie charts
plt.show()



# In[44]:


# Let's first read the data from the CSV file to ensure we're working with the correct dataset.
data = pd.read_csv('newdatasetlib.csv')
data['B2.9  Total Operating Revenues'] = data['B2.9  Total Operating Revenues'] \
    .str.replace(',', '') \
    .astype(float)
# Now we'll filter the DataFrame to include only the years 2017-2020.
years_of_interest = [2017, 2018, 2019, 2020]
data_filtered = data[data['Survey Year From'].isin(years_of_interest)]
# Next, we'll group the data by 'Library Full Name' and calculate the average operating revenue.
average_revenue = data_filtered.groupby('Library Full Name')['B2.9  Total Operating Revenues'] \
    .mean().nlargest(10)
average_revenue
average_revenue_df=average_revenue.reset_index()
average_revenue_df.rename(columns={'B2.9  Total Operating Revenues': 'Average Total Operating Revenues'}, inplace=True)
average_revenue_df


# In[48]:


import matplotlib.pyplot as plt


# Calculate the average Total Operating Revenues for each library
average_revenues = data.groupby('Library Full Name')['B2.9  Total Operating Revenues'].mean()

# Get the top 10 libraries
top_10_revenues = average_revenues.nlargest(10)

# Visualize the top 10 libraries with the highest average Total Operating Revenues
plt.figure(figsize=(12, 8))
top_10_revenues.plot(kind='bar', color='skyblue')
plt.title('Top 10 Libraries with the Highest Average Total Operating Revenues (2017-2020)')
plt.xlabel('Library Full Name')
plt.ylabel('Average Total Operating Revenues')
plt.xticks(rotation=45, ha='right')
plt.show()



# In[45]:


# Clean the 'F2.1.P No. of programs held annually' column by removing commas and converting to numeric
new_data['F2.1.P  No. of programs held annually'] = new_data['F2.1.P  No. of programs held annually'] \
    .replace({',': ''}, regex=True).astype(float)

# Clean the 'A1.14 No. of Active Library Cardholders' column by removing commas and converting to numeric
new_data['A1.14  No. of Active Library Cardholders'] = new_data['A1.14  No. of Active Library Cardholders'] \
    .replace({',': ''}, regex=True).astype(float)

# Create the new metric: 'Programs per Active Cardholder'
# Avoid division by zero by adding a small number (epsilon) to the denominator
epsilon = 1e-5
new_data['Programs per Active Cardholder'] = new_data['F2.1.P  No. of programs held annually'] / \
                                                  (new_data['A1.14  No. of Active Library Cardholders'] + epsilon)

# Display the first few rows of the DataFrame to verify the new metric
new_data[['Library Full Name', 'F2.1.P  No. of programs held annually', 'A1.14  No. of Active Library Cardholders', 'Programs per Active Cardholder']].head()


# In[46]:


# Filter out unrealistic values by setting a threshold.
realistic_threshold = 10  # This is an arbitrary threshold for the sake of the example.
realistic_data = new_data[new_data['Programs per Active Cardholder'] < realistic_threshold]

# Now find the top performers with the highest 'Programs per Active Cardholder' values within the realistic range.
top_performers_realistic = realistic_data.nlargest(5, 'Programs per Active Cardholder')

# Display the top performers
top_performers_realistic[['Library Full Name', 'Programs per Active Cardholder']]



# In[ ]:




