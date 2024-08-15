
import pandas as pd
import numpy as np
import streamlit as st
# path = '/Users/marshallr/Documents/CCS_Data_Explore/streamlit_app_dev/'

@st.cache_data
def get_data():
    # data = pd.read_csv(f'{path}supergroup_data_quality2024.csv', encoding='latin-1', low_memory=False)
    data = pd.read_csv('supergroup_data_quality2024.csv', encoding='latin-1', low_memory=False)
    data['ac_ActionDate'] = pd.to_datetime(data['ac_ActionDate'], dayfirst=True)
    data['sa_SalesExecutiveName'] = np.where(data['sa_SalesExecutiveName'].isna(), 'Unknown', data['sa_SalesExecutiveName'])
    data['se_ServiceAdvisorName'] = np.where(data['se_ServiceAdvisorName'].isna(), 'Unknown', data['se_ServiceAdvisorName'])
    return data

@st.cache_data
def data_quality_figures(df, group_by_name, column_name, action_type=0):
    if action_type != 0:
        df = df.loc[df['ac_ActionType'] == action_type]

    if column_name == group_by_name:
        results = pd.DataFrame(df.groupby(group_by_name)[column_name].value_counts()).reset_index()
        results.rename(columns={'count': 'Total Records'}, inplace=True)
        return results
    else:
        results = pd.DataFrame(df.groupby(group_by_name)[column_name].value_counts()).reset_index()
        results = results.drop(columns=column_name)
        results.rename(columns={'count': column_name}, inplace=True)
        return results

@st.cache_data
def get_data_quality_table(df, groupby_name, action_type):
    total_records = data_quality_figures(df, groupby_name, groupby_name, action_type)
    surname = data_quality_figures(df, groupby_name, 'SurnameCompany', action_type)
    home = data_quality_figures(df, groupby_name, 'Home', action_type)
    work = data_quality_figures(df, groupby_name, 'Work', action_type)
    cell = data_quality_figures(df, groupby_name, 'Cell', action_type)
    other_tel = data_quality_figures(df, groupby_name, 'Other Tel', action_type)
    email_address = data_quality_figures(df, groupby_name, 'Email Address', action_type)
    total_records = total_records.merge(surname, on=groupby_name, how='left')
    total_records = total_records.merge(home, on=groupby_name, how='left')
    total_records = total_records.merge(work, on=groupby_name, how='left')
    total_records = total_records.merge(cell, on=groupby_name, how='left')
    total_records = total_records.merge(other_tel, on=groupby_name, how='left')
    total_records = total_records.merge(email_address, on=groupby_name, how='left')

    total_records['% Surname'] = np.where(total_records['SurnameCompany'].isna(), '0.00 %', (round((total_records['SurnameCompany'] / total_records['Total Records']) * 100, 2)).astype(str) + ' %')
    total_records['% Home'] = np.where(total_records['Home'].isna(), '0.00 %', (round((total_records['Home'] / total_records['Total Records']) * 100, 2)).astype(str) + ' %')
    total_records['% Work'] = np.where(total_records['Work'].isna(), '0.00 %', (round((total_records['Work'] / total_records['Total Records']) * 100, 2)).astype(str) + ' %')
    total_records['% Cell'] = np.where(total_records['Cell'].isna(), '0.00 %', (round((total_records['Cell'] / total_records['Total Records']) * 100, 2)).astype(str) + ' %')
    total_records['% Other Tel'] = np.where(total_records['Other Tel'].isna(), '0.00 %', (round((total_records['Other Tel'] / total_records['Total Records']) * 100, 2)).astype(str) + ' %')
    total_records['% Email Address'] = np.where(total_records['Email Address'].isna(), '0.00 %', (round((total_records['Email Address'] / total_records['Total Records']) * 100, 2)).astype(str) + ' %')
    total_records = total_records[[groupby_name, 'Total Records', 'SurnameCompany', '% Surname', 'Home', '% Home', 'Work', '% Work', 'Cell', '% Cell', 'Other Tel', '% Other Tel', 'Email Address', '% Email Address']]
    return total_records