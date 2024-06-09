import streamlit as st
import datetime
import pandas as pd
import re

def load_patient_page(ID):
    st.session_state.update(ID=str(ID))
    st.session_state.update(Page_now='Patient_page')

def detail_patient_page(Page_name):
    st.session_state.update(Detail_Page=Page_name)
    st.session_state.update(Page_now='Detail_page')

def Recent_events(ID):
    drug_table = st.table(st.session_state.data_df_duration.set_index('category').loc['Medications']).set_index('subject_id')
    if str(ID) in drug_table.index:
        drug_table['time_set'] = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M").date() for i in drug_table['charttime']]
        st.write(drug_table['time_set'])
        drug_table = drug_table[(drug_table['time_set'] < st.session_state.date_now) * (drug_table['time_set'] > st.session_state.date_now - datetime.timedelta(days=14))]
        return drug_table
    else:
        return pd.DataFrame()

def save_tag(tag_name):
    st.session_state.tag_df.loc[st.session_state.tag_df['tag_name'] == tag_name, 'tag_text'] = st.session_state.get(f'tag_text_{tag_name}')
    st.session_state.tag_df.to_csv('tables/tag_folder/tags.csv', index=False)

def convert_to_clickable_links(text):
    def link_replacer(match):
        link_text = match.group(1)
        st.session_state.hidden_input = link_text
        return f'<a href="#" id={link_text}>{link_text}</a>'
    pattern = re.compile(r'\[\[(.*?)\]\]')
    return '<a href="#" id="Modify">[Modify] | </a> <a href="#" id="Add">[Add]</a> | <a href="#" id="Remove">[Remove]</a> | ' + pattern.sub(link_replacer, text)

def update_text():
    st.session_state.text_in = st.session_state.text_in_area
    st.session_state.converted_text = convert_to_clickable_links(st.session_state.text_in)
    st.session_state.text_written = 1

def text_to_formatted_text(text):
    return convert_to_clickable_links(text)