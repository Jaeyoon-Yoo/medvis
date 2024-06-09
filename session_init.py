import streamlit as st
import datetime
import pandas as pd
import os

def initialize_session():
    if 'Detail_Page' not in st.session_state:
        st.session_state.Detail_Page = False
    if 'Page_now' not in st.session_state:
        st.session_state.Page_now = 'Main_page'
    if 'ID' not in st.session_state:
        st.session_state.ID = False
    if 'Ongoing' not in st.session_state:
        st.session_state.time_now = datetime.datetime.now().time()
        st.session_state.Ongoing = True
        st.session_state.data_df_point = pd.DataFrame()
        st.session_state.data_df_duration = pd.DataFrame()
        st.session_state.text_df = pd.read_csv('tables/tag_folder/text_histories.csv', dtype=str)
        st.session_state.tag_df = pd.read_csv('tables/tag_folder/tags.csv', dtype=str)
        for file_name in os.listdir('tables'):
            if file_name.endswith('.csv'):
                data_sub = pd.read_csv('tables/' + file_name, dtype=str)
                data_sub['File_name'] = file_name
                if file_name == 'discharge.csv':
                    st.session_state.data_df_discharge = data_sub.dropna(how='all')
                elif 'charttime' in data_sub.columns:
                    st.session_state.data_df_point = pd.concat([st.session_state.data_df_point, data_sub.dropna(how='all')], axis=0)
                elif 'starttime' in data_sub.columns:
                    st.session_state.data_df_duration = pd.concat([st.session_state.data_df_duration, data_sub.dropna(how='all')], axis=0)
                else:
                    st.write('Error: ', file_name)
        st.session_state.data_df_point['charttime'] = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M") if i.count(":") == 1 else datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in st.session_state.data_df_point['charttime']]
        # st.session_state.data_df_point['charttime'] = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M") if i.count(":") == 1 else datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in st.session_state.data_df_point['charttime']]
        st.session_state.data_df_duration['starttime'] = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M") if i.count(":") == 1 else datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in st.session_state.data_df_duration['starttime']]
        st.session_state.data_df_duration['endtime'] = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M") if i.count(":") == 1 else datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in st.session_state.data_df_duration['endtime']]
        st.session_state.ID_list = set(st.session_state.data_df_discharge['subject_id']) | set(st.session_state.data_df_point['subject_id']) | set(st.session_state.data_df_duration['subject_id'])
        st.session_state.ID_list = sorted(list(st.session_state.ID_list))
        st.session_state.Cate_duration = set(st.session_state.data_df_duration['category'])
        st.session_state.Cate_point = set(st.session_state.data_df_point['category'])
        st.write(st.session_state.Cate_duration, st.session_state.Cate_point)
