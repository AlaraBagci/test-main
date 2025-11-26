import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="OOP Login System")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

st.title("🛡️ Professional OOP Login")

def api_request(endpoint, username, password):
    try:
        response = requests.post(
            f"{API_URL}/{endpoint}", 
            json={"username": username, "password": password}
        )
        # Try to parse JSON. If it fails, it means the server crashed.
        try:
            return response.json()
        except json.JSONDecodeError:
            # Return the raw error text from the server
            return {"success": False, "message": f"Server Error (Not JSON): {response.text}"}
            
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "🚨 Connection Error: Is api.py running?"}

# --- App Logic ---

if st.session_state['logged_in']:
    st.success(f"Welcome, {st.session_state['username']}!")
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()
else:
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                res = api_request("login", u, p)
                if res['success']:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = u
                    st.rerun()
                else:
                    st.error(res['message'])

    with tab2:
        with st.form("reg"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Register"):
                res = api_request("register", u, p)
                if res['success']:
                    st.success(res['message'])
                else:
                    st.error(res['message'])