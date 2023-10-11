# 1 Importing necessary libraries
import pandas as pd # for Data Wrangling (Cleaning, Exploring and Manipulating) and Data Analysis
import numpy as np # for working with Arrays, if any necessary arises
import matplotlib.pyplot as plt # for Data Visualization in analysis
import seaborn as sns # for Data Visualization in analysis
import datetime # for manipulating date and time object data
import warnings # to ignore the unncessary warnings
warnings.filterwarnings('ignore')

# 2 Lodaindg Data
control_df = pd.read_csv('control_group.csv', sep = ';')
test_df = pd.read_csv('test_group.csv', sep = ';')

control_df.head()
test_df.head()

# 3 Data Preparation
# 3.1 Renaming the columns
control_df.columns = ['Campaign Name', 'Date', 'Amount Spent', 'Number of Impressions', 'Number of Reach', 
                      'Website Clicks', 'Searches Received', 'Content Viewed', 'Added to Cart', 'Purchases']
test_df.columns = ['Campaign Name', 'Date', 'Amount Spent', 'Number of Impressions', 'Number of Reach', 
                      'Website Clicks', 'Searches Received', 'Content Viewed', 'Added to Cart', 'Purchases']
# 3.2  Exploring the data and change to desired datatypes
control_df.info() # to explore the data and their datatypes with ".info()"
test_df.info() # "Date" feature is shown as object datatype --> change this to "date time" for both datasets

control_df['Date'] = pd.to_datetime(control_df['Date'], format = '%d.%m.%Y')
test_df['Date'] = pd.to_datetime(test_df['Date'], format = '%d.%m.%Y')
print(control_df.dtypes)
print(test_df.dtypes)

# 3.3 Checking for missing values and to impute mean value of the feature in the missing value
control_df.isnull().sum() # to check for missing values
test_df.isnull().sum()

control_df['Number of Impressions'].fillna(value=control_df['Number of Impressions'].mean(), inplace=True)
control_df['Number of Reach'].fillna(value=control_df['Number of Reach'].mean(), inplace=True)
control_df['Website Clicks'].fillna(value=control_df['Website Clicks'].mean(), inplace=True)
control_df['Searches Received'].fillna(value=control_df['Searches Received'].mean(), inplace=True)
control_df['Content Viewed'].fillna(value=control_df['Content Viewed'].mean(), inplace=True)
control_df['Added to Cart'].fillna(value=control_df['Added to Cart'].mean(), inplace=True)
control_df['Purchases'].fillna(value=control_df['Purchases'].mean(), inplace=True)

# 3.4   Merge both datasets into one dataframe named as "df"
df = control_df.merge(test_df, how='outer').sort_values(['Date']) # the how='outer' parameter specifies that an outer join should be used, which means that all rows from both dataframes will be included in the merged dataframe, and any missing values will be filled with NaN.
df = df.reset_index(drop = True) # The reset_index() method is used to reset the index of a dataframe, and the drop parameter is set to True to drop the original index. The resulting dataframe has a new index that starts from 0 and increases by 1 for each row.

# 3.5 Perform descriptive analysis
df.describe()

# 4 AB Testing to find best marketing strategy
# 4.1 Calculation of metrics needed
# Click Through Rate:
df['CTR'] = (df['Website Clicks']/df['Number of Impressions']) * 100
# Cost Per Click:
df['CPC'] = df['Amount Spent']/df['Website Clicks']
# Conversion Rate:
df['conversion_rate'] = (df['Purchases'] / df['Website Clicks']) * 100
# Cost Per Conversion:
df['cost_per_conversion'] = df['Amount Spent'] / df['Purchases']
# Added to Cart Rate:
df['ACR'] = (df['Added to Cart'] / df['Website Clicks']) * 100
# Cost Per Impressions:
df['CPM'] = (df['Amount Spent']/df['Number of Impressions']) * 1000

# 4.2.1 Calculate the average Click Through Rate, group it by the type of ad campaigns
campaign_ctr = df.groupby('Campaign Name')['CTR'].mean().reset_index() #  if you want to use the grouped DataFrame further, you need to reset the index to make the grouping columns as regular columns.
# 4.2.2 Find out and plot which campaign performs better
values = campaign_ctr['CTR']
labels = campaign_ctr['Campaign Name']
colors = ['Pink', 'Red']
plt.figure(figuresize=(10,6))
plt.pie(values, labels = labels, colors = colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('CTR Comparison')
plt.show()

# 4.3.1 Calculate the average Cost Per Click, group it by the type of ad campaigns
campaign_cpc = df.groupby('Campaign Name')['CPC'].mean().reset_index()
campaign_cpc
# 4.3.2 Find out and plot which campaign performs better
values = campaign_cpc['CPC']
labels = campaign_cpc['Campaign Name']
colors = ['Pink', 'Red']
plt.figure(figsize=(10,6))
plt.pie(values, labels = labels, colors = colors, autopct= '%1.1f%%', shadow=True, startangle=140)
plt.title('CPC Comparison')
plt.show()

# 4.4.1 Compare the conversion rate of both the ad campaigns
campaign_conversion = df.groupby('Campaign Name')['conversion_rate'].mean().reset_index()
campaign_conversion
# 4.4.2 Find out and plot which campaign performs better
values = campaign_conversion['conversion_rate']
labels = campaign_conversion['Campaign Name']
colors = ['Pink', 'Red']
plt.figure(figsize=(10,6))
plt.pie(values, labels = labels, colors = colors, autopct= '%1.1f%%', shadow=True, startangle=140)
plt.title('Conversion Rate Comparison')
plt.show()

# 4.5.1 Compare the average amout paid for each conversion of visiting customers to an actual customer of both the campaigns
campaign_cost_of_conversion = df.groupby('Campaign Name')['cost_per_conversion'].mean().reset_index()
campaign_cost_of_conversion
# 4.5.2 Find out and plot which campaign performs better
values = campaign_cost_of_conversion['cost_per_conversion']
labels = campaign_cost_of_conversion['Campaign Name']
colors = ['Pink', 'Red']
plt.figure(figsize=(10,6))
plt.pie(values, labels = labels, colors = colors, autopct= '%1.1f%%', shadow=True, startangle=140)
plt.title('Cost Per Conversion Comparison')
plt.show()

# 4.6.1 to see which campaign shows better ACR: the rate at which visiting customers add at least one product to their cart
campaign_acr = df.groupby('Campaign Name')['ACR'].mean().reset_index()
campaign_acr
# 4.6.2 Find out and plot which campaign performs better
values = campaign_acr['ACR']
labels = campaign_acr['Campaign Name']
colors = ['Pink', 'Red']
plt.figure(figsize=(10,6))
plt.pie(values, labels = labels, colors = colors, autopct= '%1.1f%%', shadow=True, startangle=140)
plt.title('ACR Comparison')
plt.show()

# 4.7.1 the Cost per 1000 imperssions of both the ad campaigns
campaign_cpm = df.groupby('Campaign Name')['CPM'].mean().reset_index()
campaign_cpm
# 4.7.2 Find out and plot which campaign performs better
values = campaign_cpm['CPM']
labels = campaign_cpm['Campaign Name']
colors = ['Pink', 'Red']
plt.figure(figsize=(10,6))
plt.pie(values, labels = labels, colors = colors, autopct= '%1.1f%%', shadow=True, startangle=140)
plt.title('CPM Comparison')
plt.show()

# 5 Additional Analysis
# 5.1.1 To study 'Reach' of both campaigns
campaigns = df['Campaign Name'].unique()
campaigns
campaign_reach = df.groupby('Campaign Name')['Number of Reach'].mean().reset_index()
campaign_reach
# 5.1.2 Find out and plot which campaign performs better
plt.figure(figsize=(10,6))

for campaign in campaigns:
    campaign_data = df[df['Campaign Name'] == campaign]
    plt.plot(campaign_data['Date'], campaign_data['Number of Reach'], marker = 'o', 
             linestyle = '-', label =f'{campaign}')
plt.xlabel('Date')
plt.ylabel('Campaigns')
plt.title('Reach Comparison')
plt.legend()
plt.show()

# 5.2.1 To study 'Searches Received' of both campaigns
campaign_searches = df.groupby('Campaign Name')['Searches Received'].mean().reset_index()
campaign_searches
# 5.2.2 Find out and plot which campaign performs better
plt.figure(figsize=(10,6))

for campaign in campaigns:
    campaign_data = df[df['Campaign Name'] == campaign]
    plt.plot(campaign_data['Date'], campaign_data['Searches Received'], marker = 'o', 
             linestyle = '-', label =f'{campaign}')
plt.xlabel('Date')
plt.ylabel('Campaigns')
plt.title('Searches Comparison')
plt.legend()
plt.show()

# 5.3.1 To study 'Content Viewed' of both campaigns
campaign_views = df.groupby('Campaign Name')['Content Viewed'].mean().reset_index()
campaign_views
# 5.3.2 Find out and plot which campaign performs better
plt.figure(figsize=(10,6))

for campaign in campaigns:
    campaign_data = df[df['Campaign Name'] == campaign]
    plt.plot(campaign_data['Date'], campaign_data['Content Viewed'], marker = 'o', 
             linestyle = '-', label =f'{campaign}')
plt.xlabel('Date')
plt.ylabel('Campaigns')
plt.title('Views Comparison')
plt.legend()
plt.show()