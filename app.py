import streamlit as st
import pandas as pd
from datetime import datetime

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

# Weigh-in locations (your full list – shortened here for space, paste the full one)
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

def register(username, password, role, mariner_num="", credentials_file=None):
    if username in st.session_state.users:
        st.error("Username taken")
        return False
    if role == "Captain":
        if not mariner_num or not credentials_file:
            st.error("Captains must provide Mariner Number and credentials")
            return False
    st.session_state.users[username] = {
        'password': password,
        'role': role,
        'mariner_num': mariner_num if role == "Captain" else None,
        'credentials': credentials_file.name if credentials_file else None
    }
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
st.image("https://via.placeholder.com/800x200?text=Everyday+Angler+Charter+Tournament+Logo", use_column_width=True)
st.title("🎣 Everyday Angler Charter Tournament")

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
            mariner_num = ""
            credentials_file = None
            if role == "Captain":
                mariner_num = st.text_input("Merchant Mariner Number (required)")
                credentials_file = st.file_uploader("Upload Credentials (required)", type=["jpg", "png", "pdf"])
            reg_sub = st.form_submit_button("Register")
            if reg_sub:
                if register(new_user, new_pass, role, mariner_num, credentials_file):
                    st.success("Registered! Now log in.")
else:
    st.success(f"Logged in as **{st.session_state.logged_user}** ({st.session_state.role})")
    if st.button("Logout"):
        st.session_state.logged_user = None
        st.session_state.role = None
        st.rerun()

    # Admin wristband color
    if st.session_state.logged_user == "admin":  # Change "admin" to your username
        st.sidebar.header("Admin Tools")
        new_color = st.sidebar.text_input("Today's Wristband Color", value=st.session_state.wristband_color)
        if st.sidebar.button("Update Color"):
            st.session_state.wristband_color = new_color
            st.sidebar.success("Color updated!")

    tabs = st.tabs(["Profile", "Daily Registration" if st.session_state.role == "Angler/Team" else "Submit Catch", "Pending Approvals" if st.session_state.role == "Captain" else "Leaderboards", "Leaderboards"])

    with tabs[0]:
        st.header("Your Profile")
        user_data = st.session_state.users[st.session_state.logged_user]
        st.write(f"Username: {st.session_state.logged_user}")
        st.write(f"Role: {user_data['role']}")
        if user_data['role'] == "Captain":
            st.write(f"Merchant Mariner Number: {user_data['mariner_num']}")
            st.write(f"Credentials: {user_data['credentials']}")

    if st.session_state.role == "Angler/Team":
        with tabs[1]:
            st.header("Daily Registration")
            st.info(f"Today's wristband color: **{st.session_state.wristband_color}**")
            st.warning("Registration/Entry must be received before exiting the inlet the day of fishing.")
            if st.button("Register for Today"):
                if st.session_state.logged_user not in st.session_state.daily_anglers:
                    st.session_state.daily_anglers.append(st.session_state.logged_user)
                    st.success("You are now registered for today!")
                else:
                    st.info("You are already registered today")

    if st.session_state.role == "Captain":
        with tabs[1]:
            st.header("Submit Catch")
            st.info(f"Today's wristband color: **{st.session_state.wristband_color}**")
            st.warning("Registration/Entry must be received before exiting the inlet the day of fishing.")
            with st.form("submit_catch", clear_on_submit=True):
                division = st.selectbox("Division", ["Pelagic", "Reef"])
                angler_name = st.selectbox("Angler/Team Name", st.session_state.daily_anglers or ["No registration yet"])
                certifying_captain = st.text_input("Certifying Captain", value=st.session_state.logged_user, disabled=True)
                weigh_in_location = st.selectbox("Weigh-In Location", WEIGH_IN_LOCATIONS)
                st.subheader("3-Fish Bag Entry")
                bag_fish = []
                for i in range(3):
                    col1, col2 = st.columns(2)
                    with col1:
                        species = st.selectbox(f"Fish {i+1} Species", SPECIES_OPTIONS, key=f"species_{i}")
                    with col2:
                        weight = st.number_input(f"Fish {i+1} Weight (lbs)", min_value=0.0, step=0.1, key=f"weight_{i}")
                    if weight > 0:
                        bag_fish.append({"species": species, "weight": weight})
                total_bag_weight = sum(f['weight'] for f in bag_fish)
                st.write(f"**Total Bag Weight**: {total_bag_weight:.2f} lbs")
                colv1, colv2 = st.columns(2)
                with colv1:
                    landing_video = st.file_uploader("Landing Video (show wristband)", type=["mp4", "mov"])
                with colv2:
                    weighin_video = st.file_uploader("Weigh-in Video (show wristband + scale)", type=["mp4", "mov"])
                confirm_password = st.text_input("Re-enter password to confirm", type="password")
                submitted = st.form_submit_button("Submit Catch")
                if submitted:
                    if angler_name == "No registration yet":
                        st.error("Angler must register first")
                    elif certifying_captain != st.session_state.logged_user:
                        st.error("Certifying Captain must be you")
                    elif st.session_state.users[st.session_state.logged_user]['password'] != confirm_password:
                        st.error("Password incorrect")
                    elif landing_video and landing_video.size < 500000:
                        st.error("Landing video too short")
                    elif weighin_video and weighin_video.size < 500000:
                        st.error("Weigh-in video too short")
                    else:
                        st.session_state.pending_catches.append({
                            'captain': st.session_state.logged_user,
                            'angler': angler_name,
                            'division': division,
                            'bag': bag_fish,
                            'total_weight': total_bag_weight,
                            'weigh_in': weigh_in_location,
                            'landing_video': landing_video.name if landing_video else "Missing",
                            'weighin_video': weighin_video.name if weighin_video else "Missing",
                            'status': "Pending",
                            'date': datetime.now().strftime("%Y-%m-%d")
                        })
                        st.success("Catch submitted – awaiting your approval!")

        with tabs[2]:
            st.header("Pending Approvals")
            pending = [c for c in st.session_state.pending_catches if c['captain'] == st.session_state.logged_user and c['status'] == "Pending"]
            if pending:
                for i, catch in enumerate(pending):
                    with st.expander(f"{catch['angler']} – {catch['total_weight']:.2f} lbs – {catch['date']}"):
                        st.write(f"Division: {catch['division']} | Weigh-In: {catch['weigh_in']}")
                        st.write("Bag:")
                        for f in catch['bag']:
                            st.write(f"- {f['species']}: {f['weight']:.2f} lbs")
                        col_a, col_r = st.columns(2)
                        if col_a.button("Approve", key=f"approve_{i}"):
                            catch['status'] = "Approved"
                            st.session_state.catches.append(catch)
                            st.success("Approved!")
                            st.rerun()
                        if col_r.button("Reject", key=f"reject_{i}"):
                            catch['status'] = "Rejected"
                            st.info("Rejected")
                            st.rerun()
            else:
                st.info("No pending catches")

    with tabs[-1]:
        st.header("Live Leaderboards")
        div = st.selectbox("Division", ["Pelagic", "Reef"])
        approved = [c for c in st.session_state.catches if c['division'] == div and c['status'] == "Approved"]
        if approved:
            df = pd.DataFrame(approved)
            df = df.sort_values('total_weight', ascending=False)
            for _, row in df.iterrows():
                with st.expander(f"{row['angler']} – {row['total_weight']:.2f} lbs – {row['date']}"):
                    st.write(f"Captain: {row['captain']} | Weigh-In: {row['weigh_in']}")
                    st.write("Bag Fish:")
                    for f in row['bag']:
                        st.write(f"- {f['species']}: {f['weight']:.2f} lbs")
                    colv1, colv2 = st.columns(2)
                    with colv1:
                        st.video("https://via.placeholder.com/150?text=Landing+Video")  # Replace later
                    with colv2:
                        st.video("https://via.placeholder.com/150?text=Weigh-in+Video")
        else:
            st.info("No approved catches yet")

st.caption("Year-long tournament: Feb 1 – Nov 30, 2026 | Registration/Entry must be received before exiting the inlet | All catches require landing + weigh-in videos showing daily wristband | Tight lines!")
