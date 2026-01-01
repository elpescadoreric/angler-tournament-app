import streamlit as st
import pandas as pd
from datetime import datetime
import re
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# In-memory storage (for prototype – upgrade to DB later)
if 'users' not in st.session_state:
    st.session_state.users = {}  # {username: {'password': ..., 'role': ..., 'daily_registered': False}}
if 'daily_anglers' not in st.session_state:
    st.session_state.daily_anglers = []  # list of angler names registered today
if 'catches' not in st.session_state:
    st.session_state.catches = []
if 'posts' not in st.session_state:
    st.session_state.posts = []

# Weigh-in locations from our early list
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

# Species list
SPECIES_OPTIONS = [
    "King Mackerel",
    "Spanish Mackerel",
    "Wahoo",
    "Dolphin/Mahi Mahi",
    "Black Fin Tuna",
    "Other - Captain's Choice Award Entry"
]

# Password validation
def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters"
    if not re.search(r"\d.*\d", password):
        return "Password must contain at least 2 numbers"
    if not re.search(r"[a-z].*[a-z]", password):
        return "Password must contain at least 2 lowercase letters"
    if not re.search(r"[A-Z].*[A-Z]", password):
        return "Password must contain at least 2 uppercase letters"
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?].*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        return "Password must contain at least 2 special characters"
    return None

# Mock OAuth config for Google/Facebook (in production, use real credentials)
names = ["Test User"]
usernames = ["testuser"]
passwords = ["test123!Ab"]  # Hashed in real app

config = {'credentials': {'usernames': {usernames[0]: {'name': names[0], 'password': stauth.Hasher(passwords).generate()[0]}}}}
authenticator = stauth.Authenticate(config['credentials'], "tournament", "auth", cookie_expiry_days=30)

# App UI
st.set_page_config(page_title="Everyday Angler Charter Tournament", layout="wide")
st.title("🎣 Everyday Angler Charter Tournament")

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.success(f"Logged in as **{name}**")
    authenticator.logout('Logout', 'sidebar')

    if st.session_state.role == "Captain":
        tabs = st.tabs(["Submit Catch", "Leaderboards", "Social Feed"])

        with tabs[0]:
            st.header("Submit Catch")
            st.info("**Required**: Two videos – 1. Landing (show angler with daily colored wristband) 2. Weigh-in (show at least 1 team member with daily colored wristband, walk into scale, clear weight). Min 5 seconds each.")
            st.warning("Registration/Entry must be received before exiting the inlet the day of fishing.")
            with st.form("submit_catch", clear_on_submit=True):
                division = st.selectbox("Division", ["Pelagic", "Reef"])
                species = st.selectbox("Species", SPECIES_OPTIONS)
                angler_name = st.selectbox("Angler Name (must have registered today)", st.session_state.daily_anglers or ["No anglers registered today"])
                certifying_captain = st.text_input("Certifying Captain's Name", value=st.session_state.logged_user, disabled=True)
                weight = st.number_input("Weight (lbs)", min_value=0.0, step=0.1)
                weigh_in_location = st.selectbox("Weigh-In Location", WEIGH_IN_LOCATIONS)
                colv1, colv2 = st.columns(2)
                with colv1:
                    landing_video = st.file_uploader("1. Landing Video (show wristband)", type=["mp4", "mov", "avi"])
                with colv2:
                    weighin_video = st.file_uploader("2. Weigh-in Video (show wristband + scale)", type=["mp4", "mov", "avi"])
                submitted = st.form_submit_button("Submit Catch")
                if submitted:
                    if certifying_captain != st.session_state.logged_user:
                        st.error("Certifying Captain must match logged-in user")
                    elif angler_name == "No anglers registered today":
                        st.error("Angler must register for today first")
                    elif landing_video and landing_video.size < 500000:
                        st.error("Landing video too short")
                    elif weighin_video and weighin_video.size < 500000:
                        st.error("Weigh-in video too short")
                    else:
                        # Double confirmation
                        if st.button("Confirm Submission (Final Step)"):
                            st.session_state.catches.append({
                                'user': st.session_state.logged_user,
                                'division': division,
                                'species': species,
                                'weight': weight,
                                'angler_name': angler_name,
                                'certifying_captain': certifying_captain,
                                'weigh_in_location': weigh_in_location,
                                'landing_video': landing_video.name if landing_video else "Missing",
                                'weighin_video': weighin_video.name if weighin_video else "Missing",
                                'date': datetime.now().strftime("%Y-%m-%d %H:%M")
                            })
                            st.success("Catch submitted successfully!")

        # Leaderboard and Social Feed tabs (same as before)

    elif st.session_state.role == "Angler":
        st.header("Daily Registration")
        st.info("Register for today so your Captain can submit your catch")
        if st.button("Register for Today"):
            if st.session_state.logged_user not in st.session_state.daily_anglers:
                st.session_state.daily_anglers.append(st.session_state.logged_user)
                st.success("Registered for today!")
            else:
                st.info("Already registered today")

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")

# Google/Facebook login buttons (mock – real OAuth in production)
st.markdown("### Or sign in with")
colg, colf = st.columns(2)
with colg:
    st.markdown("[Google Login](#)")  # Replace with real OAuth link
with colf:
    st.markdown("[Facebook Login](#)")  # Replace with real OAuth link

st.caption("Year-long tournament: Feb 1 – Nov 30, 2026 | Registration/Entry must be received before exiting the inlet the day of fishing | All catches require landing + weigh-in videos showing daily wristband and clear scale reading | Tight lines!")
