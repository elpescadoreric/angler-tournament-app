import streamlit as st
import pandas as pd
from datetime import datetime

# In-memory storage
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'daily_anglers' not in st.session_state:
    st.session_state.daily_anglers = []
if 'catches' not in st.session_state:
    st.session_state.catches = []  # Now list of dicts with bag support
if 'pending_catches' not in st.session_state:
    st.session_state.pending_catches = []
if 'wristband_color' not in st.session_state:
    st.session_state.wristband_color = "Red"  # Admin can change

# Weigh-in locations (kept full list)
WEIGH_IN_LOCATIONS = [ ... ]  # Your full list from before

SPECIES_OPTIONS = [
    "King Mackerel",
    "Spanish Mackerel",
    "Wahoo",
    "Dolphin/Mahi Mahi",
    "Black Fin Tuna",
    "Other - Captain's Choice Award Entry"
]

# Simple login/register (same as last working version)
# ... (register/login functions from previous – kept identical)

# App Branding
st.set_page_config(page_title="Everyday Angler Charter Tournament", layout="wide")
st.image("https://via.placeholder.com/800x200?text=Everyday+Angler+Charter+Tournament+Logo", use_column_width=True)  # Replace with your logo URL
st.title("🎣 Everyday Angler Charter Tournament")

if st.session_state.logged_user is None:
    # Login/Register (same as before)
    # ...

else:
    st.success(f"Logged in as **{st.session_state.logged_user}** ({st.session_state.role})")
    if st.button("Logout"):
        st.session_state.logged_user = None
        st.session_state.role = None
        st.rerun()

    # Admin wristband color (only visible to first user or add admin role later)
    if st.session_state.logged_user == "admin":  # Change to your username for admin
        st.sidebar.header("Admin Tools")
        new_color = st.sidebar.text_input("Today's Wristband Color", value=st.session_state.wristband_color)
        if st.sidebar.button("Update Color"):
            st.session_state.wristband_color = new_color
            st.sidebar.success("Updated!")

    tabs = st.tabs(["Profile", "Daily Registration" if st.session_state.role == "Angler/Team" else "Submit Catch", "Pending Approvals" if st.session_state.role == "Captain" else "Leaderboards", "Leaderboards"])

    with tabs[0]:
        st.header("Your Profile")
        # ... (same as before)

    if st.session_state.role == "Angler/Team":
        with tabs[1]:
            st.header("Daily Registration")
            st.info(f"Today's wristband color: **{st.session_state.wristband_color}**")
            # ... (registration button)

    elif st.session_state.role == "Captain":
        with tabs[1]:
            st.header("Submit Catch")
            st.info(f"Today's wristband color: **{st.session_state.wristband_color}**")
            with st.form("submit_catch", clear_on_submit=True):
                division = st.selectbox("Division", ["Pelagic", "Reef"])
                angler_name = st.selectbox("Angler/Team Name", st.session_state.daily_anglers or ["No registration yet"])
                certifying_captain = st.text_input("Certifying Captain", value=st.session_state.logged_user, disabled=True)
                weigh_in_location = st.selectbox("Weigh-In Location", WEIGH_IN_LOCATIONS)
                st.subheader("3-Fish Bag Entry (up to 3 fish)")
                bag_fish = []
                for i in range(3):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        species = st.selectbox(f"Fish {i+1} Species", SPECIES_OPTIONS, key=f"species_{i}")
                    with col2:
                        weight = st.number_input(f"Fish {i+1} Weight (lbs)", min_value=0.0, step=0.1, key=f"weight_{i}")
                    with col3:
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
                submitted = st.form_submit_button("Submit for Approval")
                if submitted:
                    # Validation + add to pending
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
                    st.success("Catch submitted for your approval!")

        with tabs[2]:
            st.header("Pending Approvals")
            for i, catch in enumerate(st.session_state.pending_catches):
                if catch['captain'] == st.session_state.logged_user:
                    st.write(f"Angler: {catch['angler']} | Bag Weight: {catch['total_weight']:.2f} lbs | Date: {catch['date']}")
                    col_approve, col_reject = st.columns(2)
                    if col_approve.button("Approve", key=f"approve_{i}"):
                        st.session_state.catches.append(catch)
                        catch['status'] = "Approved"
                        st.success("Approved!")
                        st.rerun()
                    if col_reject.button("Reject", key=f"reject_{i}"):
                        catch['status'] = "Rejected"
                        st.info("Rejected")
                        st.rerun()

    with tabs[-1]:
        st.header("Live Leaderboards")
        div = st.selectbox("Division", ["Pelagic", "Reef"])
        approved_catches = [c for c in st.session_state.catches if c['division'] == div and c['status'] == "Approved"]
        if approved_catches:
            df = pd.DataFrame(approved_catches)
            df = df.sort_values('total_weight', ascending=False)
            for _, row in df.iterrows():
                with st.expander(f"{row['angler']} - {row['total_weight']:.2f} lbs - {row['date']}"):
                    st.write(f"Captain: {row['captain']} | Weigh-In: {row['weigh_in']}")
                    st.write("Bag Fish:")
                    for fish in row['bag']:
                        st.write(f"- {fish['species']}: {fish['weight']:.2f} lbs")
                    colv1, colv2 = st.columns(2)
                    with colv1:
                        if row['landing_video'] != "Missing":
                            st.video("https://via.placeholder.com/150?text=Landing+Video")  # Replace with real upload playback later
                    with colv2:
                        if row['weighin_video'] != "Missing":
                            st.video("https://via.placeholder.com/150?text=Weigh-in+Video")
        else:
            st.info("No approved catches yet")

st.caption("Year-long tournament: Feb 1 – Nov 30, 2026 | Registration/Entry must be received before exiting the inlet | All catches require landing + weigh-in videos showing daily wristband | Tight lines!")
