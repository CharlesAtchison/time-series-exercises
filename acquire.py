#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests, json, os, io
import pandas as pd


# ### 1. Using the code from the lesson as a guide and the REST API from https://python.zgulde.net/api/v1/items as we did in the lesson, create a dataframe named `items` that has all of the data for items.

# In[5]:


def get_items_data():
    url = 'https://python.zgulde.net/api/v1/items'
    response = requests.get(url)

    filename = 'items.csv'
    if os.path.isfile(filename):
        items = pd.read_csv(filename, index_col=[0])
    else:
        if response.ok:
            data = response.json()
            items = pd.DataFrame(data['payload']['items'])
            items.to_csv(filenamename)
        else:
            print(response.status_codeus_code)
    return items


# ### 2. Do the same thing, but for `stores` (https://python.zgulde.net/api/v1/stores)

# In[6]:


def get_stores_data():
    url = 'https://python.zgulde.net/api/v1/stores'
    response = requests.get(url)

    filename = 'stores.csv'

    if os.path.isfile(filename):
        stores = pd.read_csv(filename, index_col=[0])
    else:
        if response.ok:
            data = response.json()
            stores = pd.DataFrame(data['payload']['stores'])
            stores.to_csv(filename)
        else:
            print(response.status_codeus_code)
    return stores


# ### 3a. Extract the data for `sales` (https://python.zgulde.net/api/v1/sales). There are a lot of pages of data here, so your code will need to be a little more complex. Your code should continue fetching data from the next page until all of the data is extracted.
# 
# ### 3b. Save the data in your files to local csv files so that it will be faster to access in the future.
# 

# In[7]:


def get_sales_data():
    url = 'https://python.zgulde.net/api/v1/sales'
    response = requests.get(url)

    filename = 'sales.csv'
    if os.path.isfile(filename):
        sales = pd.read_csv(filename, index_col=[0])
    else:
        if response.ok:
            extracted_data = list()
            payload = response.json()['payload']
            max_page = payload['max_page']
            for n in range(max_page):
                extracted_data.extend(payload['sales'])
                try:
                    new_url = url[:25] + payload['next_page']
                    print(new_url)
                    response = requests.get(new_url)
                    payload = response.json()['payload']
                except:
                    pass
                
            sales = pd.DataFrame(extracted_data)
            sales.to_csv(filename)

        else:
            print(response.status_codeus_code)
    return sales

sales = get_sales_data()


# ### 4. Combine the data from your three separate dataframes into one large dataframe.

# In[8]:


def fetch_sales_data():
    filename = 'sales_data.csv'
    if os.path.isfile(filename):
        df = pd.read_csv(filename, index_col=[0])
    else:
        sales = get_sales_data()
        items = get_items_data()
        stores = get_stores_data()
        sales = sales.rename(columns={'store': 'store_id', 'item': 'item_id'})
        df = sales.join(stores.set_index('store_id'), on='store_id')
        df = df.join(items.set_index('item_id'), on='item_id')
        df.to_csv(filename)
    return df


# ### 5. Acquire the Open Power Systems Data for Germany, which has been rapidly expanding its renewable energy production in recent years. The data set includes country-wide totals of electricity consumption, wind power production, and solar power production for 2006-2017. You can get the data here: https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv

# In[93]:


def fetch_power_data():
    url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
    response = requests.get(url)
    filename = 'power_data.csv'
    if os.path.isfile(filename):
        df = pd.read_csv(filename, index_col=[0])
    else:
        if response.ok:
            data = response._content
            print(data)
            df = pd.read_csv(io.BytesIO(data), encoding='utf8')
            df.to_csv(filename)
        else:
            print(response.status_code)
    return df


# In[ ]:


def fetch_tsa_item_demand_data():
    
    filename = 'tsa_item_demand.csv'
    if os.path.isfile(filename):
        df = pd.read_csv(filename, index_col=[0])
    else:
        def get_connection(db, user=env.user, host=env.host, password = env.password):
            return f'mysql+pymysql://{user}:{password}@{host}/{db}'
        query = '''
        SELECT stores.*, items.*, sales.sale_date, sales.sale_amount
        FROM sales
        JOIN stores
        USING (store_id)
        JOIN items
        USING (item_id);
        '''
        df = pd.read_sql(query, con=get_connection('tsa_item_demand'))
        df.sale_date = pd.to_datetime(df.sale_date)
        df.to_csv(filename)
    return df

