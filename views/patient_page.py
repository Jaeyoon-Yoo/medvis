import streamlit as st

def display():
    st.write(st.session_state.ID)
    cols_page = st.columns(3)
    cols_page[0].button('basic_page', on_click=lambda: st.session_state.update(Detail_Page='basic_page', Page_now='Detail_page'))
    cols_page[1].button('drug_page', on_click=lambda: st.session_state.update(Detail_Page='drug_page', Page_now='Detail_page'))
    cols_page[2].button('urine_page', on_click=lambda: st.session_state.update(Detail_Page='urine_page', Page_now='Detail_page'))
    cols_page[0].button('gcs_page', on_click=lambda: st.session_state.update(Detail_Page='gcs_page', Page_now='Detail_page'))
    cols_page[1].button('o2_therapy', on_click=lambda: st.session_state.update(Detail_Page='o2_therapy', Page_now='Detail_page'))
    cols_page[2].button('text_input', on_click=lambda: st.session_state.update(Detail_Page='text_input', Page_now='Detail_page'))
    st.button('back', on_click=lambda: st.session_state.update(Page_now='Main_page'))
