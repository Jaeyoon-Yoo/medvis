import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from streamlit_plotly_events import plotly_events
from st_click_detector import click_detector
import pandas as pd
import datetime
import os
import numpy as np
import time
import re
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

def save_tag(tag_name):
    
    st.session_state.tag_df.loc[st.session_state.tag_df['tag_name']==tag_name,'tag_text'] = st.session_state.get(f'tag_text_{tag_name}')
    st.session_state.tag_df.to_csv('tables/tag_folder/tags.csv',index = False)


    
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
    # Tag_load
    st.session_state.tag_df = pd.read_csv('tables/tag_folder/tags.csv')
    # Table load
    for file_name in os.listdir('tables'):
        if file_name.endswith('.csv'):
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
    st.session_state.data_df_point['charttime'] = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M") if i.count(":") == 1 else datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in st.session_state.data_df_point['charttime']]
    st.session_state.data_df_duration['starttime'] = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M") if i.count(":") == 1 else datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in st.session_state.data_df_duration['starttime']]
    st.session_state.data_df_duration['endtime'] = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M") if i.count(":") == 1 else datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in st.session_state.data_df_duration['endtime']]
    
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

st.session_state.time_now = st.sidebar.time_input('time now',
                                                  value = st.session_state.time_now)
st.session_state.now = datetime.datetime.combine(st.session_state.date_now ,st.session_state.time_now)
btn_main_page = st.sidebar.button('Main_page', on_click = lambda: st.session_state.update(Page_now='Main_page'))
btn_time_add = st.sidebar.button('time_ongoing')
if btn_time_add:
        st.session_state.time_now = (datetime.datetime.combine(datetime.date.today(), st.session_state.time_now) + datetime.timedelta(minutes = 5)).time()
if st.session_state.Page_now == 'Main_page':
    Main_page.title('Ongoing_process')
    st.write(st.session_state.time_now)
    st.session_state.ID = False
    table_sub = st.session_state.data_df_duration[(st.session_state.data_df_duration['ordercategorydescription']=='Continuous Med')].dropna(how='all').set_index('subject_id')
    for ID in st.session_state.ID_list:
        Box_sub = st.empty()
        Box_sub.button(str(ID), on_click = lambda ID=ID: load_patient_page(str(ID)))
        table_selected = table_sub[(table_sub.index==ID)*(table_sub['starttime']<st.session_state.now)*(table_sub['endtime']>st.session_state.now)]
        st.write(len(table_selected))
        # st.table(table_selected)
        if len(table_selected):
            # st.table(table_selected)
            cols = st.columns(len(table_selected))
            for i in range(len(table_selected)):
                with cols[i]:
                    target = table_selected.iloc[i]
                    target_ontime = st.session_state.now-target.starttime
                    target_amount_now = float(target.rate)*(target_ontime.total_seconds()/3600)
                    target_amount_total = float(target.amount)
                    if target_amount_now <= target_amount_total:
                        fig_sub = go.Figure()
                        fig_sub.update_layout(showlegend=False,height=100,width = 20,margin=dict(l=20, r=20, t=20, b=20))
                        fig_sub.update_xaxes(range=[-0.2,0.2],showline=False,visible=False)
                        fig_sub.update_yaxes(range=[0,target_amount_total],showline=False)
                        fig_sub.add_bar(x = [0], y = [target_amount_now])
                        st.write(target.label,fig_sub)
elif st.session_state.Page_now == 'Patient_page':
    st.write(st.session_state.ID)
    cols_page= st.columns(3)
    cols_page[0].button('basic_page', on_click = lambda: detail_patient_page('basic_page'))
    cols_page[1].button('drug_page', on_click = lambda: detail_patient_page('drug_page'))
    cols_page[2].button('urine_page', on_click = lambda: detail_patient_page('urine_page'))
    cols_page[0].button('gcs_page', on_click = lambda: detail_patient_page('gcs_page'))
    cols_page[1].button('o2_therapy', on_click = lambda: detail_patient_page('o2_therapy'))
    cols_page[2].button('text_input', on_click = lambda: detail_patient_page('text_input'))
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
        drug_table = drug_table[(drug_table['endtime']<st.session_state.now)]
        if st.session_state.ID in drug_table.index:
            drug_table['time_set'] = [i.date() for i in drug_table['starttime']]
            drug_table['days'] = [(st.session_state.date_now-i).days for i in drug_table['time_set']]
            drug_table = drug_table[(drug_table['days']>=0)]
            Drug_selected = st.selectbox('Drug', drug_table['label'].unique())
            drug_table = drug_table[(drug_table['label']==Drug_selected)]
            drug_table['duration'] = [i-j for i,j in zip(drug_table['endtime'],drug_table['starttime'])]
            drug_table['amount'] = drug_table['amount'].astype(float)
            min_date = drug_table['starttime'].min()-datetime.timedelta(days=1)
            max_date = drug_table['endtime'].max()+datetime.timedelta(days=1)
            fig = go.Figure()
            col_scalebar,col_minplot = st.columns([7,3])
            x_min = col_scalebar.slider('start',min_value = min_date.date(), max_value = max_date.date(), value = min_date.date())
            x_max = col_scalebar.slider('start',min_value = min_date.date(), max_value = max_date.date(), value = max_date.date())
            v_min = drug_table['amount'].min()-5
            v_max = drug_table['amount'].max()+5
            if x_min > x_max:
                x_max =  x_min+datetime.timedelta(days=1)
            fig.update_xaxes(range=[x_min,x_max])
            fig.update_yaxes(range=[v_min,v_max])
            fig.update_layout(showlegend=False,height=400,width = 550,margin=dict(l=20, r=20, t=20, b=20))
            for i in range(len(drug_table)):
                fig.add_trace(go.Line(x=[drug_table['starttime'].iloc[i],drug_table['endtime'].iloc[i]], y=[drug_table['amount'].iloc[i],drug_table['amount'].iloc[i]]))
            selected_points = st.plotly_chart(fig, theme=None)
            fig2 = go.Figure(fig)
            fig2.update_xaxes(range=[min_date,max_date])
            fig2.add_trace(go.Scatter(x=[x_min,x_min,x_max,x_max], y=[v_min,v_max,v_max,v_min], fill="toself",fillcolor="rgba(255,255,255,0.2)", line=dict(color="rgba(0,100,80,0.2)")))
            fig2.update_xaxes(showline=False)
            fig2.update_yaxes(showline=False)
            fig2.update_layout(showlegend=False,height=150,width = 150,margin=dict(l=0, r=0, t=0, b=0))
            with col_minplot:
                st.plotly_chart(fig2, theme=None)
        else:
            st.session_state.Detail_Page = False

        
    elif st.session_state.Detail_Page == 'urine_page':
        table_sub = st.session_state.data_df_duration[st.session_state.data_df_duration.label.isin(['Propofol'])].set_index('subject_id').loc[[st.session_state.ID]]
        table_sub = table_sub[(table_sub['endtime']<st.session_state.now)]
        table_sub = table_sub.sort_values(by='starttime')
        
        fig = px.scatter(table_sub, x="starttime", y="amount", title='amount of urine input', labels={'x':'time', 'y':'amount'} )
        selected_points = plotly_events(fig)
        st.slider('start')
    elif st.session_state.Detail_Page == 'gcs_page':
        table_sub = st.session_state.data_df_point.set_index('subject_id').loc[st.session_state.ID].sort_values(by= 'charttime')
        table_sub = table_sub[(table_sub['charttime']<st.session_state.now)]
        table_sub = table_sub[table_sub['File_name']=='gcs.csv']
        table_sub = table_sub.pivot(index = 'charttime', columns = 'label', values = 'value')
        table_sub = table_sub[(table_sub.index<st.session_state.now)*(table_sub.index>=st.session_state.now-datetime.timedelta(days= 7))]
        st.subheader('GCS current')
        st.table(table_sub.iloc[-1:,:])
        st.subheader('GCS recent history')
        st.table(table_sub[::-1])
    elif st.session_state.Detail_Page == 'o2_therapy':
        table_sub = st.session_state.data_df_point.set_index('subject_id').loc[st.session_state.ID].sort_values(by= 'charttime')
        table_sub = table_sub[table_sub['File_name']=='selection_o2_therapy.csv']
        table_sub = table_sub[(table_sub['charttime']<st.session_state.now)]
        table_text = table_sub[table_sub['param_type']=='Text'].fillna('')
        table_text = table_text.groupby(['charttime','label'], as_index = False).agg({'value': '\n'.join})
        table_text = table_text.pivot(index = 'charttime', columns = 'label', values = 'value')
        table_text = table_text[(table_text.index<st.session_state.now)*(table_text.index>=st.session_state.now-datetime.timedelta(days= 7))]
        st.table(table_text.iloc[-1:,:])
        table_numeric = table_sub[table_sub['param_type']=='Numeric']
        table_numeric = table_numeric.pivot(index = 'charttime', columns = 'label', values = 'value').fillna('')
        st.table(table_numeric.iloc[-1:,:])
        st.subheader('O2 therapy history')
        col_o2 = st.columns(2)
        with col_o2[0]:
            st.subheader('O2 therapy text')
            st.table(table_text[::-1])
        
        with col_o2[1]:
            st.subheader('O2 therapy recent history')
            st.table(table_numeric[::-1])
    elif st.session_state.Detail_Page == 'text_input':
        if "text_in" not in st.session_state:
            st.session_state.text_in = ''
        if "clicked_link" not in st.session_state:
            st.session_state.clicked_link = ''
        if "text_written" not in st.session_state:
            st.session_state.text_written = 0
        
        text_loc = st.empty()
        if st.session_state.text_written == 1:
            with text_loc:
                clicked = click_detector(st.session_state.converted_text, key = 'click_detector')
            if clicked =="Modify":
                st.session_state.text_written = 1-st.session_state.text_written
                st.rerun()
            elif clicked == '':
                pass
            else:
                # tags
                print(f'run tag: {clicked}')
                if f'tag_text_{clicked}' not in st.session_state:
                    if clicked in st.session_state.tag_df['tag_name'].values:
                        tag_text = st.session_state.tag_df[st.session_state.tag_df['tag_name']==clicked]['tag_text'].values[0]
                    else:
                        st.session_state.tag_df.loc[len(st.session_state.tag_df)] = [clicked,'']
                        tag_text = ''
                    st.text_area('-',value = tag_text, key = f'tag_text_{clicked}',on_change = lambda: save_tag(clicked))    
        else:
            st.button('return', on_click = lambda : update_text())
            text_loc.text_area('',value = st.session_state.text_in, key='text_in_area', on_change= lambda : update_text())

    else:
        st.session_state.Detail_Page = False
    
def convert_to_clickable_links(text):
    def link_replacer(match):
        link_text = match.group(1)
        st.session_state.hidden_input = link_text
        return f'<a href="#" id = {link_text}>{link_text}</a>'
    pattern = re.compile(r'\[\[(.*?)\]\]')
    return '<a href="#" id = "Modify">[Mod] | </a>'+pattern.sub(link_replacer, text)

def update_text():
    st.session_state.text_in = st.session_state.text_in_area
    st.session_state.converted_text = convert_to_clickable_links(st.session_state.text_in)
    st.session_state.text_written = 1
