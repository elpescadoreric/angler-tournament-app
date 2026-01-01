import streamlit as st
from streamlit_oauth import OAuth2Component
import pandas as pd
from datetime import datetime
import extra_streamlit_components as stx

# OAuth setup
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
GOOGLE_REDIRECT_URI = "https://angler-tournament-app.streamlit.app/"

oauth2 = OAuth2Component(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, "https://accounts.google.com/o/oauth2/auth", "https://oauth2.googleapis.com/token", "https://openid.connect/userinfo", GOOGLE_REDIRECT_URI)

# In-memory storage
if 'users' not in st.session_state:
    st.session_state.users = {}
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

# App UI
st.set_page_config(page_title="Everyday Angler Charter Tournament", layout="wide")
st.title("🎣 Everyday Angler Charter Tournament")

# Google Login
if st.query_params.get("code"):
    result = oauth2.authorize()
    if result.get("token"):
        user_info = result["user_info"]
        email = user_info["email"]
        name = user_info["name"]
        picture = user_info.get("picture")
        if email not in st.session_state.users:
            role = "Angler/Team"  # Default – can change in profile
            st.session_state.users[email] = {
                'name': name,
                'email': email,
                'picture': picture,
                'role': role,
                'active': False if role == "Captain" else True,
                'contact': "",
                'booking_link': "",
                'bio': "",
                'mariner_num': "",
                'credentials': None
            }
        st.session_state.logged_user = email
        st.session_state.user_data = st.session_state.users[email]
        st.rerun()

if 'logged_user' not in st.session_state:
    st.header("Login with Google")
    url = oauth2.get_authorize_url()
    st.markdown(f"[Login with Google]({url})")
else:
    user_data = st.session_state.user_data = st.session_state.users[st.session_state.logged_user]
    st.image(user_data.get("picture", "https://via.placeholder.com/150"), width=100)
    st.success(f"Logged in as **{user_data['name']}** ({user_data['role']})")
    if st.button("Logout"):
        st.session_state.logged_user = None
        st.rerun()

    tabs = st.tabs(["Profile", "Daily Registration" if user_data['role'] == "Angler/Team" else "Submit Catch", "Pending Approvals" if user_data['role'] == "Captain" else "Leaderboards", "Leaderboards"])

    with tabs[0]:
        st.header("Your Profile")
        st.write(f"Name: {user_data['name']}")
        st.write(f"Email: {user_data['email']}")
        st.write(f"Role: {user_data['role']}")
        if user_data['role'] == "Captain":
            st.write("**Captain Status**: " + ("Active" if user_data.get('active') else "Inactive – upload credentials to activate"))
        # Editable fields
        user_data['contact'] = st.text_input("Contact Info (phone/email)", user_data.get('contact', ""))
        user_data['booking_link'] = st.text_input("Booking Link", user_data.get('booking_link', ""))
        user_data['bio'] = st.text_area("Bio/About", user_data.get('bio', ""))
        uploaded_pic = st.file_uploader("Update Profile Picture", type=["jpg", "png"])
        if uploaded_pic:
            user_data['picture'] = uploaded_pic.name  # In real app, upload to cloud
        if user_data['role'] == "Captain":
            user_data['mariner_num'] = st.text_input("Merchant Mariner Number", user_data.get('mariner_num', ""))
            credentials = st.file_uploader("Upload Credentials", type=["jpg", "png", "pdf"])
            if credentials:
                user_data['credentials'] = credentials.name
                user_data['active'] = True
                st.success("Credentials uploaded – Captain status active!")
        if st.button("Save Profile"):
            st.success("Profile updated!")

    # Rest of app (daily registration, submit catch, approvals, leaderboards – same as last working version)

st.caption("Year-long tournament: Feb 1 – Nov 30, 2026 | Registration/Entry must be received before exiting the inlet | All catches require landing + weigh-in videos showing daily wristband | Tight lines!")
