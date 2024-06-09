import streamlit as st
from views.detail_page import  (
    display_basic_page, 
    display_drug_page, 
    display_urine_page, 
    display_gcs_page, 
    display_o2_therapy_page, 
    display_text_input_page, 
)
def display():
    st.write(f"Selected Patient ID: {st.session_state.ID}")

    x, y = st.columns([5,5])

    with x:
        st.header("Drug")
        display_drug_page()
    
    with y:
        st.header("Urine")
        display_urine_page()
    st.header("GCS")
    display_gcs_page()
    st.header("O2")

    display_o2_therapy_page()
    display_text_input_page()


    # cols_page = st.columns(3)
    # cols_page[0].button('Basic page', on_click=lambda: st.session_state.update(Detail_Page='basic_page', Page_now='Detail_page'))
    # cols_page[1].button('Drug page', on_click=lambda: st.session_state.update(Detail_Page='drug_page', Page_now='Detail_page'))
    # cols_page[2].button('Urine page', on_click=lambda: st.session_state.update(Detail_Page='urine_page', Page_now='Detail_page'))
    # cols_page[0].button('GCS page', on_click=lambda: st.session_state.update(Detail_Page='gcs_page', Page_now='Detail_page'))
    # cols_page[1].button('O2 therapy', on_click=lambda: st.session_state.update(Detail_Page='o2_therapy', Page_now='Detail_page'))
    # cols_page[2].button('Text input', on_click=lambda: st.session_state.update(Detail_Page='text_input', Page_now='Detail_page'))
    # st.button('Back', on_click=lambda: st.session_state.update(Page_now='Main_page'))



