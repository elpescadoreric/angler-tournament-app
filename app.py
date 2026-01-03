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
    st.session_state.catches = []
if 'pending_catches' not in st.session_state:
    st.session_state.pending_catches = {}
if 'wristband_color' not in st.session_state:
    st.session_state.wristband_color = {"Everyday Angler Charter Tournament": "Red"}

# Counties
COUNTIES = ["Palm Beach", "Broward", "Miami-Dade"]

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
        'phone': "",
        'email': "",
        'website': "",
        'instagram': "",
        'facebook': "",
        'tiktok': "",
        'youtube': "",
        'x': "",
        'bio': "",
        'city': "",
        'state': "",
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
                'phone': "",
                'email': "",
                'website': "",
                'instagram': "",
                'facebook': "",
                'tiktok': "",
                'youtube': "",
                'x': "",
                'bio': "",
                'city': "Palm Beach",
                'state': "Florida",
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
                'phone': "",
                'email': "",
                'website': "",
                'instagram': "",
                'facebook': "",
                'tiktok': "",
                'youtube': "",
                'x': "",
                'bio': "",
                'city': "",
                'state': "",
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

    tabs = st.tabs(["My Profile", "Live Catch Feed", "Captains Directory", "Events", "My Events"])

    with tabs[0]:
        # Username header
        st.header(st.session_state.logged_user)

        # Centered profile picture section
        col_center = st.columns([1, 2, 1])[1]
        with col_center:
            uploaded_pic = None
            if user_data.get('picture') is None:
                uploaded_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png", "jpeg"])
            else:
                st.image(user_data['picture'], width=200)
                if st.button("Change Profile Picture"):
                    uploaded_pic = st.file_uploader("Upload New Profile Picture", type=["jpg", "png", "jpeg"], key="new_pic")

            if uploaded_pic:
                fixed_img = fix_image_orientation(uploaded_pic)
                user_data['picture'] = fixed_img
                st.success("Profile picture updated!")
                st.rerun()

        # City/State centered below picture (for Captains)
        if user_data['role'] == "Captain":
            col_city_state = st.columns([1, 2, 1])[1]
            with col_city_state:
                st.subheader(f"{user_data.get('city', '')}, {user_data.get('state', '')}")

        # Rest of profile fields
        user_data['phone'] = st.text_input("Phone Number", value=user_data.get('phone', ""))
        user_data['email'] = st.text_input("Email Address", value=user_data.get('email', ""))
        user_data['website'] = st.text_input("Website", value=user_data.get('website', ""))
        st.subheader("Social Media")
        user_data['instagram'] = st.text_input("Instagram URL", value=user_data.get('instagram', ""))
        if user_data['instagram']:
            st.markdown(f"[![Instagram](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/20px-Instagram_icon.png)]({user_data['instagram']})", unsafe_allow_html=True)
        user_data['facebook'] = st.text_input("Facebook URL", value=user_data.get('facebook', ""))
        if user_data['facebook']:
            st.markdown(f"[![Facebook](https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Facebook_f_logo_%282019%29.svg/20px-Facebook_f_logo_%282019%29.svg.png)]({user_data['facebook']})", unsafe_allow_html=True)
        user_data['tiktok'] = st.text_input("TikTok URL", value=user_data.get('tiktok', ""))
        if user_data['tiktok']:
            st.markdown(f"[![TikTok](https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/TikTok_logo.svg/20px-TikTok_logo.svg.png)]({user_data['tiktok']})", unsafe_allow_html=True)
        user_data['youtube'] = st.text_input("YouTube URL", value=user_data.get('youtube', ""))
        if user_data['youtube']:
            st.markdown(f"[![YouTube](https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/YouTube_full-color_icon_%282017%29.svg/20px-YouTube_full-color_icon_%282017%29.svg.png)]({user_data['youtube']})", unsafe_allow_html=True)
        user_data['x'] = st.text_input("X URL", value=user_data.get('x', ""))
        if user_data['x']:
            st.markdown(f"[![X](https://upload.wikimedia.org/wikipedia/en/thumb/6/60/Twitter_bird_logo_2012.svg/20px-Twitter_bird_logo_2012.svg.png)]({user_data['x']})", unsafe_allow_html=True)
        user_data['bio'] = st.text_area("Bio", value=user_data.get('bio', ""))
        if user_data['role'] == "Captain":
            col_city_state = st.columns(2)
            with col_city_state[0]:
                user_data['city'] = st.text_input("City", value=user_data.get('city', ""))
            with col_city_state[1]:
                user_data['state'] = st.text_input("State", value=user_data.get('state', ""))
        if st.button("Save Profile"):
            st.success("Profile saved successfully!")

    # Other tabs (Live Catch Feed, Captains Directory, Events, My Events) – unchanged

st.caption("Everyday Angler App – Your home for charter tournaments | Tight lines!")
