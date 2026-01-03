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

    # Tabs with Submit Catch tab only for Captains
    tab_names = ["My Profile", "Live Catch Feed", "Captains Directory", "Events", "My Events"]
    if st.session_state.role == "Captain":
        tab_names.insert(1, "Submit Catch")
    tabs = st.tabs(tab_names)

    # My Profile
    with tabs[0]:
        st.header("Your Profile")
        uploaded_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png", "jpeg"])
        if uploaded_pic:
            fixed_img = fix_image_orientation(uploaded_pic)
            user_data['picture'] = fixed_img
            st.success("Profile picture updated!")
        if user_data.get('picture'):
            st.image(user_data['picture'], width=150)
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
        if st.button("Save Profile"):
            st.success("Profile saved successfully!")

    # Submit Catch tab (only for Captains)
    if st.session_state.role == "Captain":
        with tabs[1]:
            st.header("Submit Catch")
            st.info(f"Today's wristband color: **{st.session_state.wristband_color.get('Everyday Angler Charter Tournament', 'Red')}**")
            with st.form("submit_catch", clear_on_submit=True):
                division = st.selectbox("Division", ["Pelagic", "Reef"])
                species = st.selectbox("Species", SPECIES_OPTIONS)
                angler_name = st.selectbox("Angler/Team Name", st.session_state.daily_anglers or ["No registration yet"])
                certifying_captain = st.text_input("Certifying Captain", value=st.session_state.logged_user, disabled=True)
                weight = st.number_input("Weight (lbs)", min_value=0.0, step=0.1)
                weigh_in_location = st.selectbox("Weigh-In Location", WEIGH_IN_LOCATIONS)
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
                        st.session_state.catches.append({
                            'captain': st.session_state.logged_user,
                            'angler': angler_name,
                            'division': division,
                            'species': species,
                            'weight': weight,
                            'weigh_in': weigh_in_location,
                            'landing_video': landing_video.name if landing_video else "Missing",
                            'weighin_video': weighin_video.name if weighin_video else "Missing",
                            'date': datetime.now().strftime("%Y-%m-%d")
                        })
                        st.success("Catch submitted successfully!")

    # Live Catch Feed
    tab_index = 1 if st.session_state.role == "Angler/Team" else 2
    with tabs[tab_index]:
        st.header("Live Catch Feed")
        if st.session_state.catches:
            for catch in reversed(st.session_state.catches):
                with st.expander(f"{catch['angler']} – {catch['weight']:.2f} lbs – {catch['species']} – {catch['date']}"):
                    st.write(f"Captain: {catch['captain']} | Weigh-In: {catch['weigh_in']}")
                    colv1, colv2 = st.columns(2)
                    with colv1:
                        if catch['landing_video'] != "Missing":
                            st.video("https://via.placeholder.com/150?text=Landing+Video")
                        else:
                            st.info("Landing video missing")
                    with colv2:
                        if catch['weighin_video'] != "Missing":
                            st.video("https://via.placeholder.com/150?text=Weigh-in+Video")
                        else:
                            st.info("Weigh-in video missing")
        else:
            st.info("No catches yet – be the first!")

    # Captains Directory
    tab_index = 2 if st.session_state.role == "Angler/Team" else 3
    with tabs[tab_index]:
        st.header("Captains Directory")
        county_filter = st.selectbox("Filter by County", ["All"] + COUNTIES)
        captains = [u for u in st.session_state.users.values() if u['role'] == "Captain"]
        if county_filter != "All":
            captains = [c for c in captains if c.get('county') == county_filter]
        for captain in captains:
            username = [k for k, v in st.session_state.users.items() if v == captain][0]
            with st.expander(f"{username} – {captain.get('county', 'N/A')}, {captain.get('state', 'FL')}"):
                if captain.get('picture'):
                    st.image(captain['picture'], width=150)
                st.write(f"Phone: {captain.get('phone', 'N/A')}")
                st.write(f"Email: {captain.get('email', 'N/A')}")
                st.write(f"Website: {captain.get('website', 'N/A')}")
                st.write(f"Bio: {captain.get('bio', 'N/A')}")
                st.subheader("Social")
                if captain.get('instagram'):
                    st.markdown(f"[![Instagram](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/20px-Instagram_icon.png)]({captain['instagram']})", unsafe_allow_html=True)
                if captain.get('facebook'):
                    st.markdown(f"[![Facebook](https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Facebook_f_logo_%282019%29.svg/20px-Facebook_f_logo_%282019%29.svg.png)]({captain['facebook']})", unsafe_allow_html=True)
                if captain.get('tiktok'):
                    st.markdown(f"[![TikTok](https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/TikTok_logo.svg/20px-TikTok_logo.svg.png)]({captain['tiktok']})", unsafe_allow_html=True)
                if captain.get('youtube'):
                    st.markdown(f"[![YouTube](https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/YouTube_full-color_icon_%282017%29.svg/20px-YouTube_full-color_icon_%282017%29.svg.png)]({captain['youtube']})", unsafe_allow_html=True)
                if captain.get('x'):
                    st.markdown(f"[![X](https://upload.wikimedia.org/wikipedia/en/thumb/6/60/Twitter_bird_logo_2012.svg/20px-Twitter_bird_logo_2012.svg.png)]({captain['x']})", unsafe_allow_html=True)

    # Events
    tab_index = 3 if st.session_state.role == "Angler/Team" else 4
    with tabs[tab_index]:
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

    # My Events
    tab_index = 4 if st.session_state.role == "Angler/Team" else 5
    with tabs[tab_index]:
        st.header("My Events")
        if user_data['events']:
            for event in user_data['events']:
                event_data = st.session_state.events[event]
                with st.expander(event):
                    st.write(event_data['description'])
                    st.write(f"Start: {event_data['start']} | End: {event_data['end']}")
                    st.info("Event features (daily registration, catch submission, leaderboards) coming soon!")
        else:
            st.info("Join an event from the Events tab")

st.caption("Everyday Angler App – Your home for charter tournaments | Tight lines!")
