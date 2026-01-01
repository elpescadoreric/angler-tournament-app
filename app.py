import streamlit as st
import pandas as pd
from datetime import datetime

# In-memory storage
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'events' not in st.session_state:
    st.session_state.events = {
        "Everyday Angler Charter Tournament": {
            'description': 'Year-long charter tournament in Palm Beach, Broward, Miami-Dade. Pelagic & Reef divisions.',
            'start': 'Feb 1, 2026',
            'end': 'Nov 30, 2026',
            'registered_users': []
        }
    }
if 'user_events' not in st.session_state:
    st.session_state.user_events = {}  # {username: [event_names]}
if 'daily_anglers' not in st.session_state:
    st.session_state.daily_anglers = {}
if 'catches' not in st.session_state:
    st.session_state.catches = {}
if 'pending_catches' not in st.session_state:
    st.session_state.pending_catches = {}
if 'wristband_color' not in st.session_state:
    st.session_state.wristband_color = {"Everyday Angler Charter Tournament": "Red"}

# Logo (your uploaded image)
LOGO_URL = "https://files.oaiusercontent.com/file-...your-image-id..."  # Replace with actual hosted URL or use st.image with bytes if needed

# Weigh-in locations (full list)
WEIGH_IN_LOCATIONS = [ ... ]  # Your full list

SPECIES_OPTIONS = [ ... ]  # Your list

# Login/Register
if 'logged_user' not in st.session_state:
    st.session_state.logged_user = None
    st.session_state.role = None

def register(username, password, confirm_password, role):
    if password != confirm_password:
        st.error("Passwords do not match")
        return False
    if username in st.session_state.users:
        st.error("Username taken")
        return False
    st.session_state.users[username] = {
        'password': password,
        'role': role,
        'active': True if role == "Angler/Team" else False,
        'mariner_num': "",
        'credentials': None,
        'picture': None,
        'contact': "",
        'booking_link': "",
        'bio': "",
        'events': []
    }
    return True

def login(username, password):
    user = st.session_state.users.get(username)
    if user and user['password'] == password:
        st.session_state.logged_user = username
        st.session_state.role = user['role']
        st.session_state.user_data = user
        return True
    return False

# App UI
st.set_page_config(page_title="Everyday Angler App", layout="wide")
col1, col2 = st.columns([1, 4])
with col1:
    st.image(LOGO_URL, width=150)
with col2:
    st.title("Everyday Angler App")

if st.session_state.logged_user is None:
    col1, col2 = st.columns(2)
    with col1:
        st.header("Login")
        with st.form("login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if login(username, password):
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    with col2:
        st.header("Register")
        with st.form("register"):
            new_user = st.text_input("New Username")
            new_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            role = st.selectbox("Role", ["Angler/Team", "Captain"])
            reg_sub = st.form_submit_button("Register")
            if reg_sub:
                if register(new_user, new_pass, confirm_pass, role):
                    st.success("Registered! Log in to join events.")
else:
    user_data = st.session_state.user_data = st.session_state.users[st.session_state.logged_user]
    st.success(f"Logged in as **{st.session_state.logged_user}** ({user_data['role']})")
    if st.button("Logout"):
        st.session_state.logged_user = None
        st.session_state.role = None
        st.rerun()

    tabs = st.tabs(["Events", "Profile", "My Events"])

    with tabs[0]:
        st.header("Available Events")
        for event_name, event_data in st.session_state.events.items():
            with st.expander(event_name):
                st.write(event_data['description'])
                st.write(f"Start: {event_data['start']} | End: {event_data['end']}")
                if st.session_state.logged_user in event_data['registered_users']:
                    st.success("You are registered for this event")
                else:
                    if st.button(f"Register for {event_name}", key=event_name):
                        event_data['registered_users'].append(st.session_state.logged_user)
                        user_data['events'].append(event_name)
                        st.success(f"Registered for {event_name}!")

    with tabs[1]:
        st.header("Your Profile")
        # Profile editing (same as before)

    with tabs[2]:
        st.header("My Events")
        if user_data['events']:
            for event in user_data['events']:
                st.write(f"**{event}** – Active")
                # Event-specific tabs (daily registration, submit catch, etc.)
        else:
            st.info("Join an event from the Events tab")

st.caption("Everyday Angler App – Home for multiple tournaments | Tight lines!")
