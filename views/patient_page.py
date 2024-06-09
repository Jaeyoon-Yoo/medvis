import streamlit as st

def display():
    st.write(f"Selected Patient ID: {st.session_state.ID}")
    cols_page = st.columns(3)
    cols_page[0].button('Basic page', on_click=lambda: st.session_state.update(Detail_Page='basic_page', Page_now='Detail_page'))
    cols_page[1].button('Drug page', on_click=lambda: st.session_state.update(Detail_Page='drug_page', Page_now='Detail_page'))
    cols_page[2].button('Urine page', on_click=lambda: st.session_state.update(Detail_Page='urine_page', Page_now='Detail_page'))
    cols_page[0].button('GCS page', on_click=lambda: st.session_state.update(Detail_Page='gcs_page', Page_now='Detail_page'))
    cols_page[1].button('O2 therapy', on_click=lambda: st.session_state.update(Detail_Page='o2_therapy', Page_now='Detail_page'))
    cols_page[2].button('Text input', on_click=lambda: st.session_state.update(Detail_Page='text_input', Page_now='Detail_page'))
    # st.button('Back', on_click=lambda: st.session_state.update(Page_now='Main_page'))
