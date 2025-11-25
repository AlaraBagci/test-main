import streamlit as st
import requests

# The address where your api.py is running
API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Flask + Streamlit App")

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

st.title("Flask & Streamlit Connect TEST")

# --- Helper Functions to talk to API ---
def api_login(username, password):
    try:
        resp = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Error: Flask API is not running."}

def api_register(username, password):
    try:
        resp = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Error: Flask API is not running."}

# --- App Logic ---

if st.session_state['logged_in']:
    st.success(f"✅ Logged in as: {st.session_state['username']}")
    st.write("Streamlit is successfully talking to the Flask API. TEST ENV!!!!")
    
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

else:
    tab1, tab2 = st.tabs(["Login", "Register"])

    # Login Tab
    with tab1:
        st.subheader("Login via API")
        with st.form("login_form"):
            user = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            btn = st.form_submit_button("Login")

            if btn:
                result = api_login(user, pw)
                if result['success']:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = user
                    st.rerun()
                else:
                    st.error(result['message'])

    # Register Tab
    with tab2:
        st.subheader("Register via API")
        with st.form("reg_form"):
            new_user = st.text_input("New Username")
            new_pw = st.text_input("New Password", type="password")
            reg_btn = st.form_submit_button("Register")

            if reg_btn:
                result = api_register(new_user, new_pw)
                if result['success']:
                    st.success(result['message'])
                else:
                    st.error(result['message'])