import streamlit as st
import plotly.express as px
from streamlit_plotly_events import plotly_events
import pandas as pd
import datetime
import os
import numpy as np

# initiate

def load_patient_page(ID):
    
    st.session_state.update(ID = str(ID))
    st.session_state.update(Page_now = 'Patient_page')
def detail_patient_page(Page_name):
    st.session_state.update(Detail_Page = Page_name)
    st.session_state.update(Page_now = 'Detail_page')
def Recent_events(ID):
    # Drug
    drug_table = st.table(st.session_state.data_df_duration.set_index('category').loc['Medications']).set_index('subject_id')
    if str(ID) in drug_table.index:
        drug_table['time_set'] = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M").date() for i in drug_table['charttime']]
        st.write(drug_table['time_set'])
        drug_table = drug_table[(drug_table['time_set']<st.session_state.date_now)*(drug_table['time_set']>st.session_state.date_now-datetime.timedelta(days= 14))]
        return drug_table
    else:
        return pd.DataFrame()
    
if 'Detail_Page' not in st.session_state:
    st.session_state.Detail_Page = False
if 'Page_now' not in st.session_state:
    st.session_state.Page_now = 'Main_page'
if 'ID' not in st.session_state:
    st.session_state.ID = False
if 'Ongoing' not in st.session_state:
    st.session_state.Ongoing = True
    st.session_state.data_df_point = pd.DataFrame()
    st.session_state.data_df_duration = pd.DataFrame()
    # Table load
    for file_name in os.listdir('tables'):
        data_sub = pd.read_csv('tables/'+file_name, dtype = str)
        data_sub['File_name'] = file_name
        if file_name == 'discharge.csv':   
            st.session_state.data_df_discharge = data_sub.dropna(how='all')
        elif 'charttime' in data_sub.columns:
            st.session_state.data_df_point = pd.concat([st.session_state.data_df_point,data_sub.dropna(how='all')], axis = 0)
        elif 'starttime' in data_sub.columns:
            st.session_state.data_df_duration = pd.concat([st.session_state.data_df_duration,data_sub.dropna(how='all')], axis = 0)
        else:
            st.write('Error: ',file_name)
    st.session_state.ID_list = set(st.session_state.data_df_discharge['subject_id'])|set(st.session_state.data_df_point['subject_id'])|set(st.session_state.data_df_duration['subject_id'])
    st.session_state.ID_list = list(st.session_state.ID_list)
    st.session_state.Cate_duration = set(st.session_state.data_df_duration['category'])
    st.session_state.Cate_point = set(st.session_state.data_df_point['category'])
    st.write(st.session_state.Cate_duration,st.session_state.Cate_point)
# Sidebar
Main_page = st.empty()
Main_page.title('Hello World!')
st.sidebar.title('this is sidebar')
st.session_state.date_now = st.sidebar.date_input('date now',
                                                  value = datetime.datetime.strptime(st.session_state.data_df_discharge['charttime'].max(), "%Y-%m-%d %H:%M"))
st.session_state.time_now = st.sidebar.time_input('time now')

btn_main_page = st.sidebar.button('Main_page', on_click = lambda: st.session_state.update(Page_now='Main_page'))
    
if st.session_state.Page_now == 'Main_page':
    col1,col2 = st.columns([2,8])
    st.session_state.ID = False
    for ID in st.session_state.ID_list:
        col1.button(str(ID), on_click = lambda ID=ID: load_patient_page(str(ID)))
    for ID in st.session_state.ID_list:
        # events = Recent_events(str(ID))
        # col2.table(events)
        pass
elif st.session_state.Page_now == 'Patient_page':
    st.write(st.session_state.ID)
    col1, col2, col3 = st.columns(3)
    col1.button('basic_page', on_click = lambda: detail_patient_page('basic_page'))
    col2.button('drug_page', on_click = lambda: detail_patient_page('drug_page'))
    col3.button('urine_page', on_click = lambda: detail_patient_page('urine_page'))
    st.button('back', on_click = lambda: st.session_state.update(Page_now='Main_page'))
    
elif st.session_state.Page_now == 'Detail_page':
    st.button('Back', on_click = lambda: st.session_state.update(Page_now='Patient_page'))
    if st.session_state.Detail_Page == 'basic_page':
        # print(st.session_state.ID,st.session_state.table_discharge.index)
        if str(st.session_state.ID) in st.session_state.data_df_discharge.index:
            basic_info_table = st.session_state.data_df_discharge[st.session_state.data_df_discharge['subject_ID'] == st.session_state.ID]
            st.write(st.session_state.ID)
            for col in basic_info_table.index:
                st.subheader(col)
                st.write(basic_info_table[col])
        else:
            st.session_state.Detail_Page = False
            
    elif st.session_state.Detail_Page == 'drug_page':
        drug_table = st.session_state.data_df_duration.set_index('category').loc['Medications'].set_index('subject_id')
        if st.session_state.ID in drug_table.index:
            drug_table['time_set'] = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S").date() for i in drug_table['starttime']]
            drug_table['days'] = [(st.session_state.date_now-i).days for i in drug_table['time_set']]
            st.write(drug_table['days'])
            st.table(drug_table[(drug_table['days']>=0)*(drug_table['days']<2)][['label','starttime','endtime','amount','days']])
        else:
            st.session_state.Detail_Page = False

        
    elif st.session_state.Detail_Page == 'urine_page':
        table_sub = st.session_state.data_df_duration[st.session_state.data_df_duration.label.isin(['Propofol'])].set_index('subject_id').loc[st.session_state.ID].sort_values(by= 'starttime')
        fig = px.scatter(table_sub, x="starttime", y="amount", title='amount of urine input', labels={'x':'time', 'y':'amount'} )
        selected_points = plotly_events(fig)
        
    else:
        st.session_state.Detail_Page = False