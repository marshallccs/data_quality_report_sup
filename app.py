import streamlit as st
from st_aggrid import AgGrid, ColumnsAutoSizeMode
from data_quality import get_data, get_data_quality_table

#set page
st.set_page_config(page_title="2024 Reporting", page_icon="🌎", layout="wide")

# Set page header
st.image('CCS-Logo.png')
st.header('SUPERGROUP - Data Quality 2024 Report', divider='blue')
st.header('')

df = get_data()

dealer = st.multiselect(
    label='Filter Dealer',
    options=(df['de_DealerName'].sort_values(ascending=True)).unique().tolist(),
    default=(df['de_DealerName'].sort_values(ascending=True)).unique().tolist()
)

min_date = df['ac_ActionDate'].min()
max_date = df['ac_ActionDate'].max()

st.markdown('Filter the start and end period for the report')
start_date = st.date_input('Start Date', value=min_date, min_value=min_date, max_value=max_date)
end_date = st.date_input('End Date', value=max_date, min_value=min_date, max_value=max_date)



df_selection = df.query(
    "de_DealerName==@dealer & ac_ActionDate>=@start_date & ac_ActionDate<=@end_date"
)

def percentage_values(df, action_type):
    df = df.loc[df['ActionType'] == action_type].copy()
    df['Cell Percent'] = round((df['Cell'] / df['Total Records']) * 100, 2)
    df['Email Percent'] = round((df['Email Address'] / df['Total Records']) * 100, 2)
    cell_check = df['Cell Percent'].sum()
    email_check = df['Email Percent'].sum()
    cell_percent = df['% Cell'].sum()
    email_percent = df['% Email Address'].sum()

    cell_text = ''
    email_text = ''
    if cell_check >= 80.00:
        cell_text = f' - For {action_type}, The cell quality is at {cell_percent}, which is great.'
    elif cell_check >= 60.00:
        cell_text = f' - For {action_type}, The cell quality is at {cell_percent}, and needs some improvement.'
    else:
        cell_text = f' - For {action_type}, The cell quality is at {cell_percent}, and needs urgent attention.'

    if email_check >= 80.00:
        email_text = f'The email quality is at {email_percent}, and is good for marketing contactability.'
    elif email_check >= 60.00:
        email_text = f'The email quality is at {email_percent}, and needs some improvement.'
    else:
        email_text = f'The email quality is at {email_percent}, and needs urgent attention.'

    st.markdown(f'{cell_text} {email_text}')
    

def dq_overview(df):
    # Data Quality table
    dq = get_data_quality_table(df, 'ActionType', 0)
    # Add markdown with analysis
    min_year = start_date.strftime('%B-%Y')
    max_year = end_date.strftime('%B-%Y')
    total_actions = dq['Total Records'].sum()
    st.subheader(f'Data Quality Overview Report {min_year} - {max_year}')
    st.markdown(f'The below table shows an overview of all actions imported and the state of the quality between {min_year} and {max_year}, per action type.')
    st.markdown(f" - Over this period there were {total_actions} actions imported into Drivers'Cirle.")
    percentage_values(dq, 'New Sale')
    percentage_values(dq, 'Used Sale')
    percentage_values(dq, 'Service')
    
    AgGrid(dq, height=150, fit_columns_on_grid_load=ColumnsAutoSizeMode.FIT_CONTENTS)

def dq_by_executive(df):
    # Data Quality table
    st.subheader(f'Data Quality by Executive / Advisor')
    st.markdown('The below table provides the incoming data quality breakdown by the service / sales advisor.')
    change_action_type = st.radio(
        label='Choose Action Type:',
        options=['New Sales', 'Used Sales', 'Service'],
    )
    action_type = ''
    if change_action_type == 'New Sales':
        dq = get_data_quality_table(df, 'sa_SalesExecutiveName', 1)
        action_type = 'New Sales Executive'
    elif change_action_type == 'Used Sales':
        dq = get_data_quality_table(df, 'sa_SalesExecutiveName', 2)
        action_type = 'Used Sales Executive'
    else:
        dq = get_data_quality_table(df, 'se_ServiceAdvisorName', 3)
        action_type = 'Service Advisor'
    # Add markdown with analysis
    min_year = start_date.strftime('%B-%Y')
    max_year = end_date.strftime('%B-%Y')
    st.markdown(f' - {action_type} breakdown {min_year} - {max_year}')
    AgGrid(dq, height=500, fit_columns_on_grid_load=ColumnsAutoSizeMode.FIT_CONTENTS)

dq_overview(df_selection)
st.header('')
dq_by_executive(df_selection)