import streamlit as st
import plotly.graph_objects as go
import datetime  # Necessary import for handling datetime
from utils import load_patient_page
import pandas as pd

def display():
    st.title('Ongoing Process')
    st.session_state.ID = False
    table_sub = st.session_state.data_df_duration[
        (st.session_state.data_df_duration['ordercategorydescription'] == 'Continuous Med')
    ].dropna(how='all').set_index('subject_id')
    st.markdown(
        """
        <style>
        .scrolling-wrapper {
            overflow-x: auto;
            display: flex;
            flex-wrap: nowrap;
            padding: 10px;
            border: 1px solid #ccc;
        }
        .chart-container {
            flex: 0 0 auto;
            width: 220px;
            margin-right: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    upcoming_events = []
    table_selected = table_sub[
        (table_sub['starttime'] < st.session_state.now) &
        (table_sub['endtime'] + pd.Timedelta(hours=1) > st.session_state.now)
    ].sort_values(by='starttime', ascending=True).reset_index(drop=False)
    for i, target in enumerate(table_selected.itertuples()):
        if target.rateuom == 'mcg/kg/min':
            target_rate = float(target.rate) * float(target.patientweight) / 1000 * 60
        elif target.rateuom == 'mcg/hour':
            target_rate = float(target.rate) / 1000
        else:
            target_rate = float(target.rate)
        target_ontime = st.session_state.now - target.starttime
        target_minutes = target_ontime.total_seconds() / 60
        target_amount_now = float(target_rate) * (target_ontime.total_seconds() / 3600)
        target_amount_total = float(target.amount)
        total_duration_minutes = (target.endtime - target.starttime).total_seconds() / 60
        
        if target_amount_now <= target_amount_total + float(target_rate) * (900 / 3600):
            if target_amount_now >= target_amount_total - float(target_rate) * (900 / 3600):
                upcoming_events.append(f"{target.subject_id} | {target.label} | {max(0,int(total_duration_minutes-target_minutes))} min left")
    for event in upcoming_events:
        st.markdown(f'<p style="font-size:24px;color:orange;">⚠️ {event}</p>', unsafe_allow_html=True)
    st.write("<hr>", unsafe_allow_html=True)
    for ID in st.session_state.ID_list:
        # 각 ID에 대해 컬럼 생성
        cols = st.columns([1, 2, 2, 5])  # 버튼 | 수혈 | 수액 | 기타

        with cols[0]:
            Btn_sub = st.button(str(ID), on_click=lambda ID=ID: load_patient_page(str(ID)))

        table_selected = table_sub[
            (table_sub.index == ID) &
            (table_sub['starttime'] < st.session_state.now) &
            (table_sub['endtime'] + pd.Timedelta(hours=1) > st.session_state.now)
        ]
        table_selected = table_selected.sort_values(by='starttime', ascending=True)
        
        with cols[1]:
            st.write('electrolyte')
            table_selected_sub = table_selected[table_selected['File_name'] == 'input_electrolyte.csv']
            if len(table_selected_sub):
                target = table_selected_sub.iloc[-1]
                make_pie_chart(target)
        with cols[2]:
            st.write('transfusion')
            table_selected_sub = table_selected[table_selected['File_name'] == 'input_transfusion.csv']
            if len(table_selected_sub):
                target = table_selected_sub.iloc[-1]
                make_pie_chart(target)
        
        with cols[3]:
            st.write('others')
            table_selected_sub = table_selected[table_selected['File_name'].isin(['input_analgesic_drug.csv', 'input_antibiotic_drug.csv'])].sort_values(by='label', ascending=True)
            if len(table_selected_sub):
                table_dict = {'drug_name': [], 'target_now': [], 'target_total': [],'target_total_minutes': [], 'target_now_minutes': []}
                for i, target in enumerate(table_selected_sub.itertuples()):
                    if target.rateuom == 'mcg/kg/min':
                        target_rate = float(target.rate) * float(target.patientweight) / 1000 * 60
                    elif target.rateuom == 'mcg/hour':
                        target_rate = float(target.rate) / 1000
                    else:
                        target_rate = float(target.rate)
                    target_ontime = st.session_state.now - target.starttime
                    target_minutes = target_ontime.total_seconds() / 60
                    target_amount_now = float(target_rate) * (target_ontime.total_seconds() / 3600)
                    target_amount_total = float(target.amount)
                    total_duration_minutes = (target.endtime - target.starttime).total_seconds() / 60
                    
                    if target_amount_now <= target_amount_total + float(target_rate) * (900 / 3600):
                        table_dict['drug_name'].append(target.label)
                        table_dict['target_now'].append(target_amount_now)
                        table_dict['target_total'].append(target_amount_total)
                        table_dict['target_total_minutes'].append(total_duration_minutes)
                        table_dict['target_now_minutes'].append(target_minutes)
                if len(table_dict['drug_name']):
                    make_bar_plot(table_dict)
                    
                    
        st.write("<hr>", unsafe_allow_html=True)

        
def make_pie_chart(target):
    # 단위를 mg/hour로 통일  
    if target.rateuom == 'mcg/kg/min':
        target_rate = float(target.rate) * float(target.weight) / 1000 * 60
    elif target.rateuom == 'mcg/hour':
        target_rate = float(target.rate) / 1000
    else:
        target_rate = float(target.rate)
    target_ontime = st.session_state.now - target.starttime
    target_minutes = target_ontime.total_seconds() / 60
    target_amount_now = float(target_rate) * (target_ontime.total_seconds() / 3600)
    
    target_amount_total_plus = float(target.amount) + float(target_rate) * (900 / 3600)
    target_amount_total = float(target.amount)
    total_duration_minutes = (target.endtime - target.starttime).total_seconds() / 60
    if target_amount_now <= target_amount_total_plus:
        
        pie_colors = ['#1f77b4', '#ff7f0e']  # 기본 색상

        # 15분 전부터 색상 변경
        if target_amount_now >= target_amount_total - float(target_rate) * (900 / 3600):
            pie_colors = ['#d62728', '#ff7f0e']  # 변경된 색상

        fig_sub = go.Figure()
        fig_sub.add_trace(go.Pie(
            labels=['Delivered', 'Remaining'],
            values=[target_amount_now, max(target_amount_total - target_amount_now, 0)],
            hole=0.5,
            sort=False,
            marker=dict(colors=pie_colors)
        ))
        fig_sub.update_layout(
            showlegend=False,
            height=200,
            width=200,
            margin=dict(l=20, r=20, t=20, b=20),
            annotations=[dict(
                text=f"<b>{target.label}</b>",
                x=0.5,
                y=0.5,
                font_size=12,
                showarrow=False,
                xanchor='center',
                yanchor='middle'
            )]
        )
        st.plotly_chart(fig_sub, use_container_width=True)
        if int(target_minutes) < int(total_duration_minutes):
            st.markdown(f"<p style='text-align: center'><b>{target.label}</b><br><b>{int(target_minutes)} min</b> out of <b>{int(total_duration_minutes)} min</b></p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='text-align: center'><b>{target.label}</b><br><b>{int(total_duration_minutes)} min Done!!</b></p>", unsafe_allow_html=True)
            
def make_bar_plot(table_dict):
    fig = go.Figure()
    for drug_name, target_now, target_total, target_total_minutes,target_now_minutes in zip(table_dict['drug_name'], table_dict['target_now'], table_dict['target_total'], table_dict['target_total_minutes'], table_dict['target_now_minutes']):
        remaining_minutes = max(0,int(target_total_minutes - target_now_minutes))
        bar_color = 'red' if remaining_minutes <= 15 else 'blue'
        fig.add_trace(go.Bar(
            y=[drug_name],
            x=[1],
            name=drug_name,
            orientation='h',  # 가로 막대 그래프 설정
            marker=dict(color='rgba(0,0,0,0)', line=dict(color='black', width=2))
        ))
        fig.add_trace(go.Bar(
            y=[drug_name],
            x=[min(1,target_now / target_total)],
            name=drug_name,
            text=[f'{min(1,(target_now / target_total)) * 100:.1f}%'],
            textposition='auto',
            orientation='h',  # 가로 막대 그래프 설정
            marker_color=bar_color
        ))
        fig.add_shape(
            type='line',
            x0=1, x1=1, y0=drug_name, y1=drug_name,
            line=dict(color='Red', width=2)
        )

        # Add a text label for the total duration at x=1
        fig.add_annotation(
            x=1, y=drug_name,
            text=f'{int(target_total_minutes)} min',
            showarrow=False,
            xanchor='left',
            yanchor='middle',
            font=dict(size=15, color='black')
        )
        fig.add_annotation(
            x=min(1,target_now / target_total),
            y=drug_name,
            text=f'{remaining_minutes} min',
            showarrow=False,
            xanchor='left',
            yanchor='bottom',
            font=dict(size=15, color='black')
        )


    fig.update_layout(
        xaxis_title='Progress (%)',
        xaxis=dict(autorange=True),
        yaxis=dict(autorange=True),
        height=400,
        width=400,
        showlegend=False,
        barmode='overlay'
    )

    st.plotly_chart(fig)