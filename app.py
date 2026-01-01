import streamlit as st
import pandas as pd
from datetime import datetime

# In-memory storage (same as before)
# ... (keep all your storage dicts)

# Logo
LOGO_URL = "https://i.imgur.com/RgxPgmP.png"

# (Keep your full lists and functions)

# App UI
st.set_page_config(page_title="Everyday Angler App", layout="wide")

# Logo top left (only after login)
if 'logged_user' in st.session_state:
    col_logo, col_title = st.columns([1, 5])
    with col_logo:
        st.image(LOGO_URL, width=150)
    with col_title:
        st.title("Everyday Angler App")
else:
    st.title("Everyday Angler App")

if 'logged_user' not in st.session_state:
    st.header("Quick Demo Mode (for testing)")
    col_demo1, col_demo2 = st.columns(2)
    with col_demo1:
        if st.button("Login as Test Captain"):
            st.session_state.logged_user = "testcaptain"
            st.session_state.role = "Captain"
            st.session_state.user_data = {'role': "Captain", 'active': True}
            st.rerun()
    with col_demo2:
        if st.button("Login as Test Angler/Team"):
            st.session_state.logged_user = "testangler"
            st.session_state.role = "Angler/Team"
            st.session_state.user_data = {'role': "Angler/Team", 'active': True}
            st.rerun()

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.header("Login")
        # ... (login form)
    with col2:
        st.header("Register")
        # ... (register form with password confirmation)

else:
    # Logged in view (profile as default tab, etc.)
    # ... (rest of your app code)

st.caption("Everyday Angler App – Your home for charter tournaments | Tight lines!")
