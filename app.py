import streamlit as st
import pandas as pd
from datetime import datetime

# In-memory storage
if 'users' not in st.session_state:
    st.session_state.users = {}  # {username: {'password': pw, 'role': role, 'active': bool, 'mariner_num': str, 'credentials': str, 'picture': str, 'contact': str, 'booking_link': str, 'bio': str}}
if 'daily_anglers' not in st.session_state:
    st.session_state.daily_anglers = []
if 'catches' not in st.session_state:
    st.session_state.catches = []
if 'pending_catches' not in st.session_state:
    st.session_state.pending_catches = []
if 'wristband_color' not in st.session_state:
    st.session_state.wristband_color = "Red"

# Weigh-in locations (full list)
WEIGH_IN_LOCATIONS = [
    "Sailfish Marina Resort (Singer Island)",
    "Riviera Beach Marina Village",
    "Boynton Harbor Marina",
    "Palm Beach Yacht Center (Lantana)",
    "Two Georges Waterfront Grille (Boynton Beach)",
    "Banana Boat (Boynton Beach)",
    "Old Key Lime House (Lantana)",
    "Frigate’s Waterfront Bar & Grill (North Palm Beach)",
    "Prime Catch (Boynton Beach)",
    "Waterway Cafe (Palm Beach Gardens)",
    "Seasons 52 (Palm Beach Gardens)",
    "The River House (Palm Beach Gardens)",
    "Sands Harbor Resort & Marina (Pompano Beach)",
    "PORT 32 Lighthouse Point Marina",
    "Taha Marine Center (Pompano Beach)",
    "The Cove Marina / Two Georges at the Cove (Deerfield Beach)",
    "Shooters Waterfront (Fort Lauderdale)",
    "Boatyard (Fort Lauderdale)",
    "Coconuts (Fort Lauderdale)",
    "Rustic Inn Crabhouse (Fort Lauderdale)",
    "15th Street Fisheries (Fort Lauderdale)",
    "Southport Raw Bar (Fort Lauderdale)",
    "Kaluz Restaurant (Fort Lauderdale)",
    "Boathouse at the Riverside (Fort Lauderdale)",
    "Homestead Bayfront Marina",
    "Black Point Marina (Cutler Bay)",
    "Haulover Marine Center / Bill Bird Marina",
    "Crandon Park Marina (Key Biscayne)",
    "Matheson Hammock Marina (Coral Gables)",
    "Dinner Key Marina (Coconut Grove)",
    "Rusty Pelican (Key Biscayne)",
    "Monty's Raw Bar (Coconut Grove)",
    "Shuckers Waterfront Bar & Grill (North Bay Village)",
    "Garcia's Seafood Grille & Fish Market (Miami River)",
    "Boater's Grill (Key Biscayne)",
    "American Social (Brickell)",
    "Billy's Stone Crab Restaurant (Hollywood)",
    "Seaspice Brasserie & Lounge (Miami River)"
]

SPECIES_OPTIONS = [
    "King Mackerel",
    "Spanish Mackerel",
    "Wahoo",
    "Dolphin/Mahi Mahi",
    "Black Fin Tuna",
    "Other - Captain's Choice Award Entry"
]

# Simple login/register
if 'logged_user' not in st.session_state:
    st.session_state.logged_user = None
    st.session_state.role = None

def register(username, password, role):
    if username in st.session_state.users:
        st.error("Username taken")
        return False
    st.session_state.users[username] = {
        'password': password,
        'role': role,
        'active': True if role == "Angler/Team" else False,  # Captain inactive until credentials
        'mariner_num': "",
        'credentials': None,
        'picture': None,
        'contact': "",
        'booking_link': "",
        'bio': ""
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
st.set_page_config(page_title="Everyday Angler Charter Tournament", layout="wide")
st.image("https://via.placeholder.com/800x200?text=Everyday+Angler+Charter+Tournament+Logo", use_column_width=True)
st.title("Everyday Angler Charter Tournament")

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
            role = st.selectbox("Role", ["Angler/Team", "Captain"])
            reg_sub = st.form_submit_button("Register")
            if reg_sub:
                if register(new_user, new_pass, role):
                    st.success("Registered! Log in to complete your profile.")
else:
    user_data = st.session_state.user_data = st.session_state.users[st.session_state.logged_user]
    st.success(f"Logged in as **{st.session_state.logged_user}** ({user_data['role']})")
    if st.button("Logout"):
        st.session_state.logged_user = None
        st.session_state.role = None
        st.rerun()

    # Captain status check
    if user_data['role'] == "Captain" and not user_data.get('active', False):
        st.warning("**Captain Inactive** – Upload credentials in Profile to activate and submit catches")

    tabs = st.tabs(["Profile", "Daily Registration" if user_data['role'] == "Angler/Team" else "Submit Catch", "Pending Approvals" if user_data['role'] == "Captain" else "Leaderboards", "Leaderboards"])

    with tabs[0]:
        st.header("Your Profile")
        uploaded_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png"])
        if uploaded_pic:
            user_data['picture'] = uploaded_pic.name
        if user_data.get('picture'):
            st.image("https://via.placeholder.com/150?text=Profile+Pic", width=150)  # Replace with real in production
        user_data['contact'] = st.text_input("Contact Info", user_data.get('contact', ""))
        user_data['booking_link'] = st.text_input("Booking Link", user_data.get('booking_link', ""))
        user_data['bio'] = st.text_area("Bio", user_data.get('bio', ""))
        if user_data['role'] == "Captain":
            user_data['mariner_num'] = st.text_input("Merchant Mariner Number", user_data.get('mariner_num', ""))
            credentials = st.file_uploader("Upload Credentials", type=["jpg", "png", "pdf"])
            if credentials:
                user_data['credentials'] = credentials.name
                user_data['active'] = True
                st.success("Credentials uploaded – Captain now active!")
        if st.button("Save Profile"):
            st.success("Profile updated!")

    # Rest of app (daily registration, submit catch, approvals, leaderboards – same as last stable version)

st.caption("Year-long tournament: Feb 1 – Nov 30, 2026 | Registration/Entry must be received before exiting the inlet | All catches require landing + weigh-in videos showing daily wristband | Tight lines!")
