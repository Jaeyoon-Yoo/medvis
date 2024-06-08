import streamlit as st
import plotly.graph_objects as go
import datetime  # Necessary import for handling datetime
from utils import load_patient_page

def display():
    st.title('Ongoing Process')
    st.write(st.session_state.time_now)
    st.session_state.ID = False
    table_sub = st.session_state.data_df_duration[
        (st.session_state.data_df_duration['ordercategorydescription'] == 'Continuous Med')
    ].dropna(how='all').set_index('subject_id')
    for ID in st.session_state.ID_list:
        Box_sub = st.empty()
        Box_sub.button(str(ID), on_click=lambda ID=ID: load_patient_page(str(ID)))
        table_selected = table_sub[
            (table_sub.index == ID) *
            (table_sub['starttime'] < st.session_state.now) *
            (table_sub['endtime'] > st.session_state.now)
        ]
        st.write(len(table_selected))
        if len(table_selected):
            cols = st.columns(len(table_selected))
            for i in range(len(table_selected)):
                with cols[i]:
                    target = table_selected.iloc[i]
                    target_ontime = st.session_state.now - target.starttime
                    target_amount_now = float(target.rate) * (target_ontime.total_seconds() / 3600)
                    target_amount_total = float(target.amount)
                    if target_amount_now <= target_amount_total:
                        fig_sub = go.Figure()
                        fig_sub.update_layout(showlegend=False, height=100, width=20, margin=dict(l=20, r=20, t=20, b=20))
                        fig_sub.update_xaxes(range=[-0.2, 0.2], showline=False, visible=False)
                        fig_sub.update_yaxes(range=[0, target_amount_total], showline=False)
                        fig_sub.add_bar(x=[0], y=[target_amount_now])
                        st.write(target.label, fig_sub)
