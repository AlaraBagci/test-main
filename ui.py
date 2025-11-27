import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="University System", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = None

# --- LOGIN PAGE ---
if not st.session_state['logged_in']:
    st.title("🔐 University System Login")
    with st.form("login_form"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password") # Privacy Masking
        if st.form_submit_button("Login"):
            try:
                res = requests.post(f"{API_URL}/login", json={"username": u, "password": p}).json()
                if res.get('success'):
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = res.get('role')
                    st.rerun()
                else:
                    st.error(res.get('message'))
            except:
                st.error("Cannot connect to API.")

# --- ADMIN PANEL ---
elif st.session_state['role'] == 'admin':
    st.markdown("### 🛠️ Administrator Panel")
    st.info("System Maintenance Mode")
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

# --- PROFESSOR / OFFICER DASHBOARD ---
elif st.session_state['role'] in ['professor', 'officer']:
    st.markdown(f"### 🎓 {st.session_state['role'].capitalize()} Dashboard")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔄 Reset & Generate Demo Data"):
            requests.post(f"{API_URL}/generate_data")
            st.success("Data Refreshed!")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    with col2:
        st.subheader("⚠️ At-Risk Students")
        try:
            data = requests.get(f"{API_URL}/dashboard").json()
            if data:
                df = pd.DataFrame(data)
                def color_risk(val):
                    return 'color: red' if val == 'Critical' else 'color: orange' if val == 'Warning' else 'color: green'
                st.dataframe(df.style.map(color_risk, subset=['status']))
                
                # Visualization
                st.divider()
                st.subheader("📈 Deep Dive")
                selected_student = st.selectbox("Select Student", df['name'])
                student_id = df[df['name'] == selected_student].iloc[0]['id']
                
                hist_data = requests.get(f"{API_URL}/student/{student_id}").json()
                if hist_data:
                    st.line_chart(pd.DataFrame(hist_data), x='week', y=['stress_level', 'hours_sleep'])
            else:
                st.info("Database empty. Click 'Reset & Generate Demo Data'.")
        except:
            st.error("Error fetching data.")