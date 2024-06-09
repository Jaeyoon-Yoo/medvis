import streamlit as st
import datetime
from session_init import initialize_session
from views import main_page, patient_page, detail_page

# Initialize session state
st.set_page_config(layout="wide")
initialize_session()

# Sidebar
st.sidebar.title('This is the sidebar')

def handle_toggle_change():
    st.session_state.Page_now = 'Main_page' if st.session_state.overview else 'Patient_page'

# Create the toggle button
st.sidebar.toggle(
    "Overview", 
    key='overview',
    value=st.session_state.Page_now == 'Main_page',
    on_change=handle_toggle_change
)

# if st.session_state.Page_now == 'Patient_page':
st.session_state.ID = st.sidebar.selectbox('Select Patient ID', st.session_state.ID_list)
st.session_state.date_now = st.sidebar.date_input('Date now', value=datetime.datetime.strptime(st.session_state.data_df_discharge['charttime'].max(), "%Y-%m-%d %H:%M"))
st.session_state.time_now = st.sidebar.time_input('Time now', value=st.session_state.time_now)
st.session_state.now = datetime.datetime.combine(st.session_state.date_now, st.session_state.time_now)

# if st.sidebar.button('Main page'):
#     st.session_state.Page_now = 'Main_page'

if st.sidebar.button('Time ongoing'):
    st.session_state.time_now = (datetime.datetime.combine(datetime.date.today(), st.session_state.time_now) + datetime.timedelta(minutes=5)).time()

# Page navigation logic
if st.session_state.Page_now == 'Main_page':
    main_page.display()
elif st.session_state.Page_now == 'Patient_page':
    patient_page.display()
elif st.session_state.Page_now == 'Detail_page':
    detail_page.display()

# import streamlit as st
# import datetime
# from session_init import initialize_session
# from views import main_page, patient_page, detail_page

# # Initialize session state
# initialize_session()

# # Sidebar
# st.sidebar.title('This is the sidebar')
# st.session_state.selected_id = st.sidebar.selectbox('Select Patient ID', st.session_state.ID_list)

# st.session_state.date_now = st.sidebar.date_input('Date now', value=datetime.datetime.strptime(st.session_state.data_df_discharge['charttime'].max(), "%Y-%m-%d %H:%M"))
# st.session_state.time_now = st.sidebar.time_input('Time now', value=st.session_state.time_now)
# st.session_state.now = datetime.datetime.combine(st.session_state.date_now, st.session_state.time_now)

# if st.sidebar.button('Main page'):
#     st.session_state.Page_now = 'Main_page'

# if st.sidebar.button('Time ongoing'):
#     st.session_state.time_now = (datetime.datetime.combine(datetime.date.today(), st.session_state.time_now) + datetime.timedelta(minutes=5)).time()

# # Page navigation logic
# if st.session_state.Page_now == 'Main_page':
#     main_page.display()
# elif st.session_state.Page_now == 'Patient_page':
#     patient_page.display()
# elif st.session_state.Page_now == 'Detail_page':
#     detail_page.display()
