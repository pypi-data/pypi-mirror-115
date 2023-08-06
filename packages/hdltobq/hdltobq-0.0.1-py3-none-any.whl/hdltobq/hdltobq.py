"""
This library will be used to connect to BQ from DataLake
"""
###And Data Can be transported from DL to BQ in one GO
#!/usr/bin/env python
# coding: utf-8

# #### <b>SAP HANA Data Lake and BQ Interaction

# ##### <i>import the required libraries

import os
import logging
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
from google.api_core.exceptions import Conflict


# #### <B>Insert Data into BQ - Create Dataset and table & insert some information

# In[ ]:
class BQConnect:
    """
    BQConnect for Connect and Update
    """
    DATASET_ID = ' '
    def __init__(self, bq_dataset: str, bq_project: str, bq_credentials: str):
        self.bq_dataset = bq_dataset
        self.bq_project = bq_project
        self.bq_credentials = bq_credentials
        self.gac = 'GOOGLE_APPLICATION_CREDENTIALS'
        logging.info('Initialization done Successfully')
    @staticmethod
    def connect2bq(bq):
        """
        Connect to BQ
        """
        logging.info('Connection Inititated')
        os.environ[bq.gac] = bq.bq_credentials
        bq_client = bigquery.Client()
        if bq_client is not None:
            bq_ds = bq_client.dataset(bq.bq_dataset)
        return bq_client, bq_ds
    @staticmethod
    def gcp2df(sql, bq_client):
        """
        Convert to Dataframe
        """
        try:
            query = bq_client.query(sql)
            res = query.result()
            return res.to_dataframe()
        except BadRequest as excp:
            print(excp["message"])
    #### Create table in bq from HANA Data Lake
    @staticmethod
    def create_dataset(bq_client, ds_id: str):
        """
        Create Dataset from SAP HANA DL to BQ
        """
        BQConnect.DATASET_ID = ds_id
        logging.info('Beginning BigQuery initialization.')
        ###Check if dataset already exist
        try:
            print('Creating DataSet.....')
            bq_res = bq_client.create_dataset(ds_id) ###HANA DATA Lake
            BQConnect.bq_dataset = ds_id
            print('Created.. Thanks')
        except Conflict:
            logging.critical('Dataset %s already exists, not creating.', ds_id)
            return 'Error'
    @staticmethod
    def create_tab(bq_client, res, tab_id: str):
        """
        Replicate table and Schema
        """
        print('Started Creating table.....')
        tab_id = bq_client.project + '.' + BQConnect.DATASET_ID + '.' + tab_id
        print(tab_id)
        table = ''
        table = bigquery.Table(tab_id, schema=BQConnect.get_schema(res))
        try:
            table = bq_client.create_table(table)  # Make an API request
            print('Table created Successfully', tab_id)
            return "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
        except Conflict:
            logging.critical('Dataset %s already exists, not creating.', tab_id)
    @staticmethod
    def get_schema(res):
        """
        Prepare a Compatible Schema
        """
        schema = []
        print('Preparing Schema...')
        for i in res.columns:
            if res[i].dtype == 'int64':
                lv_type = 'INT64'
            if res[i].dtype == 'object':
                lv_type = 'STRING'
            if res[i].dtype == 'datetime64':
                print('hi')
                lv_type = 'TIMESTAMP'
            if res[i].dtype == 'int64':
                lv_type = 'INT64'
            if res[i].dtype == 'int64':
                lv_type = 'INT64'
            if 'datetime64' in str(res[i].dtype):
                lv_type = 'TIMESTAMP'
            if res[i].dtype == 'float64':
                lv_type = 'FLOAT'
            j = i
            i = i.replace(" ", "")
            lv_field = bigquery.SchemaField(i, lv_type)
            schema.append(lv_field)
            res.rename(columns={j:i}, inplace=True)
        print('Ready.....')
        return schema


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:
