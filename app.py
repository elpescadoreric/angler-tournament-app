import streamlit as st
import pandas as pd
from datetime import datetime

# In-memory storage
if 'users' not in st.session_state:
    st.session_state.users = {}  # {username: {'password': pw, 'role': 'Angler' or 'Captain'}}
if 'daily_anglers' not in st.session_state:
    st.session_state.daily_anglers = []  # Anglers registered for today
if 'catches' not in st.session_state:
    st.session_state.catches = []

# Weigh-in locations (from our early list)
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
    st.session_state.users[username] = {'password': password, 'role': role}
    return True

def login(username, password):
    user = st.session_state.users.get(username)
    if user and user['password'] == password:
        st.session_state.logged_user = username
        st.session_state.role = user['role']
        return True
    return False

# App UI
st.set_page_config(page_title="Everyday Angler Charter Tournament", layout="wide")
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
            role = st.selectbox("Role", ["Angler", "Captain"])
            reg_sub = st.form_submit_button("Register")
            if reg_sub:
                if register(new_user, new_pass, role):
                    st.success("Registered! Now log in.")
else:
    st.success(f"Logged in as **{st.session_state.logged_user}** ({st.session_state.role})")
    if st.button("Logout"):
        st.session_state.logged_user = None
        st.session_state.role = None
        st.rerun()

    if st.session_state.role == "Angler":
        st.header("Daily Registration")
        st.info("Register for today so your Captain can submit your catch")
        st.warning("Registration/Entry must be received before exiting the inlet the day of fishing.")
        if st.button("Register for Today"):
            if st.session_state.logged_user not in st.session_state.daily_anglers:
                st.session_state.daily_anglers.append(st.session_state.logged_user)
                st.success("You are now registered for today!")
            else:
                st.info("You are already registered today")

    elif st.session_state.role == "Captain":
        tabs = st.tabs(["Submit Catch", "Leaderboards"])

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
                confirm_password = st.text_input("Re-enter your password to confirm submission", type="password")
                submitted = st.form_submit_button("Submit Catch")
                if submitted:
                    if angler_name == "No anglers registered today":
                        st.error("No anglers registered today")
                    elif certifying_captain != st.session_state.logged_user:
                        st.error("Certifying Captain must be you")
                    elif st.session_state.users[st.session_state.logged_user]['password'] != confirm_password:
                        st.error("Password incorrect – submission canceled")
                    elif landing_video and landing_video.size < 500000:
                        st.error("Landing video too short")
                    elif weighin_video and weighin_video.size < 500000:
                        st.error("Weigh-in video too short")
                    else:
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

        with tabs[1]:
            st.header("Live Leaderboards")
            div = st.selectbox("Select Division", ["Pelagic", "Reef"])
            df = pd.DataFrame([c for c in st.session_state.catches if c['division'] == div])
            if not df.empty:
                df['adj_weight'] = df.apply(lambda row: row['weight'] + 10 if 'sailfish' in row['species'].lower() else row['weight'], axis=1)
                df = df.sort_values('adj_weight', ascending=False)
                df['species'] = df['species'].str.title()
                st.dataframe(df[['angler_name', 'certifying_captain', 'species', 'adj_weight', 'weigh_in_location', 'date']].rename(
                    columns={'angler_name': 'Angler', 'certifying_captain': 'Certifying Captain', 'species': 'Species', 'adj_weight': 'Weight (lbs)', 'weigh_in_location': 'Weigh-In Location', 'date': 'Date'}
                ), use_container_width=True)
            else:
                st.info("No catches yet in this division")

st.caption("Year-long tournament: Feb 1 – Nov 30, 2026 | Registration/Entry must be received before exiting the inlet the day of fishing | All catches require landing + weigh-in videos showing daily wristband and clear scale reading | Tight lines!")
