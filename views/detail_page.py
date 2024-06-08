import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from streamlit_plotly_events import plotly_events
from st_click_detector import click_detector
import datetime  # Necessary import for handling datetime
from utils import save_tag, update_text

def display():
    st.button('Back', on_click=lambda: st.session_state.update(Page_now='Patient_page'))
    if st.session_state.Detail_Page == 'basic_page':
        display_basic_page()
    elif st.session_state.Detail_Page == 'drug_page':
        display_drug_page()
    elif st.session_state.Detail_Page == 'urine_page':
        display_urine_page()
    elif st.session_state.Detail_Page == 'gcs_page':
        display_gcs_page()
    elif st.session_state.Detail_Page == 'o2_therapy':
        display_o2_therapy_page()
    elif st.session_state.Detail_Page == 'text_input':
        display_text_input_page()
    else:
        st.session_state.Detail_Page = False

def display_basic_page():
    if str(st.session_state.ID) in st.session_state.data_df_discharge.index:
        basic_info_table = st.session_state.data_df_discharge[
            st.session_state.data_df_discharge['subject_ID'] == st.session_state.ID
        ]
        st.write(st.session_state.ID)
        for col in basic_info_table.index:
            st.subheader(col)
            st.write(basic_info_table[col])
    else:
        st.session_state.Detail_Page = False

def display_drug_page():
    drug_table = st.session_state.data_df_duration.set_index('category').loc['Medications'].set_index('subject_id')
    drug_table = drug_table[(drug_table['endtime'] < st.session_state.now)]
    if st.session_state.ID in drug_table.index:
        drug_table['time_set'] = [i.date() for i in drug_table['starttime']]
        drug_table['days'] = [(st.session_state.date_now - i).days for i in drug_table['time_set']]
        drug_table = drug_table[(drug_table['days'] >= 0)]
        Drug_selected = st.selectbox('Drug', drug_table['label'].unique())
        drug_table = drug_table[(drug_table['label'] == Drug_selected)]
        drug_table['duration'] = [i - j for i, j in zip(drug_table['endtime'], drug_table['starttime'])]
        drug_table['amount'] = drug_table['amount'].astype(float)
        min_date = drug_table['starttime'].min() - datetime.timedelta(days=1)
        max_date = drug_table['endtime'].max() + datetime.timedelta(days=1)
        fig = go.Figure()
        col_scalebar, col_minplot = st.columns([7, 3])
        x_min = col_scalebar.slider('start', min_value=min_date.date(), max_value=max_date.date(), value=min_date.date())
        x_max = col_scalebar.slider('start', min_value=min_date.date(), max_value=max_date.date(), value=max_date.date())
        v_min = drug_table['amount'].min() - 5
        v_max = drug_table['amount'].max() + 5
        if x_min > x_max:
            x_max = x_min + datetime.timedelta(days=1)
        fig.update_xaxes(range=[x_min, x_max])
        fig.update_yaxes(range=[v_min, v_max])
        fig.update_layout(showlegend=False, height=400, width=550, margin=dict(l=20, r=20, t=20, b=20))
        for i in range(len(drug_table)):
            fig.add_trace(go.Line(x=[drug_table['starttime'].iloc[i], drug_table['endtime'].iloc[i]], y=[drug_table['amount'].iloc[i], drug_table['amount'].iloc[i]]))
        selected_points = st.plotly_chart(fig, theme=None)
        fig2 = go.Figure(fig)
        fig2.update_xaxes(range=[min_date, max_date])
        fig2.add_trace(go.Scatter(x=[x_min, x_min, x_max, x_max], y=[v_min, v_max, v_max, v_min], fill="toself", fillcolor="rgba(255,255,255,0.2)", line=dict(color="rgba(0,100,80,0.2)")))
        fig2.update_xaxes(showline=False)
        fig2.update_yaxes(showline=False)
        fig2.update_layout(showlegend=False, height=150, width=150, margin=dict(l=0, r=0, t=0, b=0))
        with col_minplot:
            st.plotly_chart(fig2, theme=None)
    else:
        st.session_state.Detail_Page = False

def display_urine_page():
    table_sub = st.session_state.data_df_duration[st.session_state.data_df_duration.label.isin(['Propofol'])].set_index('subject_id').loc[[st.session_state.ID]]
    table_sub = table_sub[(table_sub['endtime'] < st.session_state.now)]
    table_sub = table_sub.sort_values(by='starttime')
    fig = px.scatter(table_sub, x="starttime", y="amount", title='amount of urine input', labels={'x': 'time', 'y': 'amount'})
    selected_points = plotly_events(fig)
    st.slider('start')

def display_gcs_page():
    table_sub = st.session_state.data_df_point.set_index('subject_id').loc[st.session_state.ID].sort_values(by='charttime')
    table_sub = table_sub[(table_sub['charttime'] < st.session_state.now)]
    table_sub = table_sub[table_sub['File_name'] == 'gcs.csv']
    table_sub = table_sub.pivot(index='charttime', columns='label', values='value')
    table_sub = table_sub[(table_sub.index < st.session_state.now) * (table_sub.index >= st.session_state.now - datetime.timedelta(days=7))]
    st.subheader('GCS current')
    st.table(table_sub.iloc[-1:, :])
    st.subheader('GCS recent history')
    st.table(table_sub[::-1])

def display_o2_therapy_page():
    table_sub = st.session_state.data_df_point.set_index('subject_id').loc[st.session_state.ID].sort_values(by='charttime')
    table_sub = table_sub[table_sub['File_name'] == 'selection_o2_therapy.csv']
    table_sub = table_sub[(table_sub['charttime'] < st.session_state.now)]
    table_text = table_sub[table_sub['param_type'] == 'Text'].fillna('')
    table_text = table_text.groupby(['charttime', 'label'], as_index=False).agg({'value': '\n'.join})
    table_text = table_text.pivot(index='charttime', columns='label', values='value')
    table_text = table_text[(table_text.index < st.session_state.now) * (table_text.index >= st.session_state.now - datetime.timedelta(days=7))]
    st.table(table_text.iloc[-1:, :])
    table_numeric = table_sub[table_sub['param_type'] == 'Numeric']
    table_numeric = table_numeric.pivot(index='charttime', columns='label', values='value').fillna('')
    st.table(table_numeric.iloc[-1:, :])
    st.subheader('O2 therapy history')
    col_o2 = st.columns(2)
    with col_o2[0]:
        st.subheader('O2 therapy text')
        st.table(table_text[::-1])
    with col_o2[1]:
        st.subheader('O2 therapy recent history')
        st.table(table_numeric[::-1])

def display_text_input_page():
    if "text_in" not in st.session_state:
        st.session_state.text_in = ''
    if "clicked_link" not in st.session_state:
        st.session_state.clicked_link = ''
    if "text_written" not in st.session_state:
        st.session_state.text_written = 0
    text_loc = st.empty()
    if st.session_state.text_written == 1:
        with text_loc:
            clicked = click_detector(st.session_state.converted_text, key='click_detector')
        if clicked == "Modify":
            st.session_state.text_written = 1 - st.session_state.text_written
            st.rerun()
        elif clicked == '':
            pass
        else:
            if f'tag_text_{clicked}' not in st.session_state:
                if clicked in st.session_state.tag_df['tag_name'].values:
                    tag_text = st.session_state.tag_df[st.session_state.tag_df['tag_name'] == clicked]['tag_text'].values[0]
                else:
                    st.session_state.tag_df.loc[len(st.session_state.tag_df)] = [clicked, '']
                    tag_text = ''
                st.text_area('-', value=tag_text, key=f'tag_text_{clicked}', on_change=lambda: save_tag(clicked))
    else:
        st.button('return', on_click=lambda: update_text())
        text_loc.text_area('', value=st.session_state.text_in, key='text_in_area', on_change=lambda: update_text())
