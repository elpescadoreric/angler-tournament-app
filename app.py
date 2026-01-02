import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ExifTags

# In-memory storage
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

# Logo
LOGO_URL = "https://i.imgur.com/RgxPgmP.png"

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
        'active': True,
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

# Fix image orientation
def fix_image_orientation(uploaded_file):
    if uploaded_file is None:
        return None
    image = Image.open(uploaded_file)
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            if orientation in exif:
                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
    except:
        pass
    return image

# App UI
st.set_page_config(page_title="Everyday Angler App", layout="wide")

if st.session_state.logged_user:
    col_logo, col_title = st.columns([1, 5])
    with col_logo:
        st.image(LOGO_URL, width=150)
    with col_title:
        st.title("Everyday Angler App")
else:
    st.title("Everyday Angler App")

if st.session_state.logged_user is None:
    st.subheader("Quick Test Logins")
    col_demo1, col_demo2 = st.columns(2)
    with col_demo1:
        if st.button("Test as Captain"):
            st.session_state.logged_user = "testcaptain"
            st.session_state.role = "Captain"
            st.session_state.user_data = {
                'role': "Captain",
                'active': True,
                'picture': None,
                'contact': "",
                'booking_link': "",
                'bio': "",
                'events': []
            }
            st.rerun()
    with col_demo2:
        if st.button("Test as Angler/Team"):
            st.session_state.logged_user = "testangler"
            st.session_state.role = "Angler/Team"
            st.session_state.user_data = {
                'role': "Angler/Team",
                'active': True,
                'picture': None,
                'contact': "",
                'booking_link': "",
                'bio': "",
                'events': []
            }
            st.rerun()

    st.divider()

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
            if role == "Captain":
                st.markdown("**All captains must agree to adhere to all local, state, and federal laws while participating in any Everyday Angler App tournament. Any false information provided will be prosecuted to the fullest extent.**")
                agree = st.checkbox("I agree to the above statement")
            reg_sub = st.form_submit_button("Register")
            if reg_sub:
                if role == "Captain" and not agree:
                    st.error("You must agree to the statement")
                elif register(new_user, new_pass, confirm_pass, role):
                    st.success("Registered! Log in to complete your profile.")
else:
    user_data = st.session_state.user_data
    st.success(f"Logged in as **{st.session_state.logged_user}** ({user_data['role']})")
    if st.button("Logout"):
        st.session_state.logged_user = None
        st.session_state.role = None
        st.rerun()

    tabs = st.tabs(["Profile", "Events", "My Events"])

    with tabs[0]:
        st.header("Your Profile")
        uploaded_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png", "jpeg"])
        if uploaded_pic:
            fixed_img = fix_image_orientation(uploaded_pic)
            user_data['picture'] = fixed_img
            st.success("Profile picture updated!")
        if user_data.get('picture'):
            st.image(user_data['picture'], width=150)
        user_data['contact'] = st.text_input("Contact Info", value=user_data.get('contact', ""))
        user_data['booking_link'] = st.text_input("Booking Link", value=user_data.get('booking_link', ""))
        user_data['bio'] = st.text_area("Bio", value=user_data.get('bio', ""))
        if st.button("Save Profile"):
            st.success("Profile saved successfully!")

    # Events and My Events tabs (same as before)

st.caption("Everyday Angler App – Your home for charter tournaments | Tight lines!")
