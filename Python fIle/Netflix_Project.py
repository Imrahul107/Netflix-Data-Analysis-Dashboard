import pandas as pd
import numpy as np

# Read Excel file
df = pd.read_excel('Netflix_Unclean_Project.xlsx')

# print(df.head())
# print(df.tail())
# print(df.shape)
# print(df.columns)
# print(df.info())

# remove extra space-----------
# df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
# print(df.isnull().sum())


# Check duplicate data
print(df.duplicated().sum())

# Remove duplicate rows
df.drop_duplicates(inplace=True)

print(df.duplicated().sum())


# dirty values.......
df.replace(
    ['N/A', 'null', '', ' '],
    np.nan,
    inplace=True
)

print(df.isnull().sum())


# proper case all column---------

text_columns = [
    'Customer_Name',
    'Title',
    'Content_Type',
    'Genre',
    'Country',
    'Subscription_Plan',
    'Device',
    'Payment_Method',
    'Account_Status'
]

# Convert text columns to Proper Case
df[text_columns] = df[text_columns].apply(
    lambda x: x.str.replace(r'\s+', ' ', regex=True).str.strip().str.title()
)


# kisi column ki value count kro------------
print(df['Country'].value_counts())




# numerica calumn text solution------

numerical_columns = [
    'Age',
    'Watch_Hours',
    'Monthly_Fee',
    'Movies_Watched',
    'Episodes_Watched',
    'Avg_Rating',
    'Monthly_Sessions',
    'Download_Count'
]

for col in numerical_columns:
    df[col]=pd.to_numeric(df[col],errors='coerce')



# age correction--
df=df[(df['Age']>=18)&(df['Age']<=100)]
print(df['Age'].describe())

# negative data in watch horse----
df=df[df['Watch_Hours']>0]
df=df[df['Monthly_Fee']>0]

# print(df.columns.tolist())

# date cleaning
df['Last_Watch_Date']=pd.to_datetime(df['Last_Watch_Date'],errors='coerce')
df['Join_Date']=pd.to_datetime(df['Join_Date'],errors='coerce')

# # # Save cleaned file
# df.to_excel("Netflix_cleaned1.xlsx", index=False)



# missing stirng value---
print(df.isnull().sum())
missing_string=['Genre','Country','Device','Payment_Method']
df[missing_string]=df[missing_string].fillna('unknown_value')
print(df.isnull().sum())

# feature Engineering ( column se hi new column  create krna)---
df['Customer_Revenue']=df['Monthly_Fee']*df['Monthly_Sessions']
df['Engagement_Score']=df['Watch_Hours']+df['Monthly_Sessions']+df['Download_Count']

# special category column create---
bin=[0,25,50,100,np.inf]
label=['Low','Medium','High','Very High']
df['Watch_Category']=pd.cut(df['Watch_Hours'],bins=bin,labels=label)
print(df.tail())
print(df['Watch_Category'].value_counts())

# create Age-Group coulumn---
bin=[17,25,35,50,100]
label=['17-25','25-35','35-50','50+']
df['Age_Group']=pd.cut(df['Age'],bins=bin,labels=label)
print(df.tail())
print(df['Age_Group'].value_counts())

# Account Active Flag----
df['Active_Flag']=np.where(df['Account_Status']=='Active',1,0)

# final data check--
print(df.info())
print(df.isnull().sum())
print(df.duplicated().sum())

# clean csv file export--
df.to_excel("Netflix clean project.xlsx",index=False)
df.to_csv("Netflix clean project.csv",index=False)

# export to sql
from sqlalchemy import create_engine
engine=create_engine('mysql+pymysql://root:@localhost/Netflix_db')
df.to_sql(
    'netflix_customers',
    con=engine,
    if_exists='replace',
    index=False
)

print(df.shape)