import streamlit as st
import pandas as pd
from datetime import datetime

# In-memory storage (same as before)
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'events' not in st.session_state:
    st.session_state.events = {
        "Everyday Angler Charter Tournament": {
            'description': 'Year-long charter tournament in Palm Beach, Broward, and Miami-Dade counties. Pelagic and Reef divisions.',
            'start': 'February 1, 2026',
            'end': 'November 30, 2026',
            'registered_users': []
        }
    }
if 'user_events' not in st.session_state:
    st.session_state.user_events = {}
if 'daily_anglers' not in st.session_state:
    st.session_state.daily_anglers = {}
if 'catches' not in st.session_state:
    st.session_state.catches = {}
if 'pending_catches' not in st.session_state:
    st.session_state.pending_catches = {}
if 'wristband_color' not in st.session_state:
    st.session_state.wristband_color = {"Everyday Angler Charter Tournament": "Red"}

# Working logo URL
LOGO_URL = "https://i.imgur.com/RgxPgmP.png"

# (Keep your full WEIGH_IN_LOCATIONS and SPECIES_OPTIONS lists here – same as before)

# Simple login/register (same as last working version)
# ... (register/login functions – unchanged)

# App UI
st.set_page_config(page_title="Everyday Angler App", layout="wide")

# Logo top left
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image(LOGO_URL, width=150)
with col_title:
    st.title("Everyday Angler App")

# Rest of the app (login/register, events page, profile, my events – same as last version)

st.caption("Everyday Angler App – Your home for charter tournaments | Tight lines!")
