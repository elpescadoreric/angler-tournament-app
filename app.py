import streamlit as st
import pandas as pd
from datetime import datetime
import re

# In-memory storage
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'catches' not in st.session_state:
    st.session_state.catches = []
if 'posts' not in st.session_state:
    st.session_state.posts = []

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

# Functions
def register(username, password, confirm_password, role='Angler'):
    error = validate_password(password)
    if error:
        st.error(error)
        return False
    if password != confirm_password:
        st.error("Passwords do not match")
        return False
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

def submit_catch(user, division, species, weight, angler_name, certifying_captain, landing_video, weighin_video):
    if landing_video and landing_video.size < 500000:
        st.error("Landing video too short – must be at least 5 seconds")
        return False
    if weighin_video and weighin_video.size < 500000:
        st.error("Weigh-in video too short – must be at least 5 seconds")
        return False
    st.session_state.catches.append({
        'user': user,
        'division': division,
        'species': species,
        'weight': weight,
        'angler_name': angler_name,
        'certifying_captain': certifying_captain,
        'landing_video': landing_video.name if landing_video else "Missing",
        'weighin_video': weighin_video.name if weighin_video else "Missing",
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    return True

def get_leaderboard(division):
    df = pd.DataFrame([c for c in st.session_state.catches if c['division'] == division])
    if df.empty:
        return pd.DataFrame(columns=['Angler', 'Certifying Captain', 'Species', 'Weight (lbs)', 'Landing Video', 'Weigh-in Video', 'Date'])
    df['adj_weight'] = df.apply(lambda row: row['weight'] + 10 if 'sailfish' in row['species'].lower() else row['weight'], axis=1)
    df = df.sort_values('adj_weight', ascending=False)
    df['species'] = df['species'].str.title()
    df['Landing Video'] = df['landing_video'].apply(lambda x: f"[View](https://via.placeholder.com/150?text=Landing+Video+{x})" if x != "Missing" else "Missing")
    df['Weigh-in Video'] = df['weighin_video'].apply(lambda x: f"[View](https://via.placeholder.com/150?text=Weigh-in+Video+{x})" if x != "Missing" else "Missing")
    return df[['angler_name', 'certifying_captain', 'species', 'adj_weight', 'Landing Video', 'Weigh-in Video', 'date']].rename(
        columns={'angler_name': 'Angler', 'certifying_captain': 'Certifying Captain', 'species': 'Species', 'adj_weight': 'Weight (lbs)', 'date': 'Date'}
    ).head(20)

def add_post(user, content, media=None):
    media_name = media.name if media else None
    st.session_state.posts.append({
        'user': user,
        'content': content,
        'media': media_name,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    })

# App UI
st.set_page_config(page_title="Everyday Angler Charter Tournament", layout="wide")
st.title("🎣 Everyday Angler Charter Tournament")

if 'logged_user' not in st.session_state:
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
            new_pass = st.text_input("New Password (min 8 chars, 2 nums, 2 lower, 2 upper, 2 special)", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            role = st.selectbox("Role", ["Angler", "Captain"])
            reg_sub = st.form_submit_button("Register")
            if reg_sub:
                if register(new_user, new_pass, confirm_pass, role):
                    st.success("Registered! Now log in.")
else:
    st.success(f"Logged in as **{st.session_state.logged_user}** ({st.session_state.role})")
    if st.button("Logout"):
        del st.session_state.logged_user
        del st.session_state.role
        st.rerun()

    tabs = st.tabs(["Submit Catch", "Leaderboards", "Social Feed"])

    with tabs[0]:
        st.header("Submit Catch")
        st.info("**Required**: Two videos – 1. Landing (show angler with daily colored wristband) 2. Weigh-in (show at least 1 team member with daily colored wristband, walk into scale, clear weight). Min 5 seconds each.")
        with st.form("submit_catch", clear_on_submit=True):
            division = st.selectbox("Division", ["Pelagic", "Reef"])
            species = st.selectbox("Species", SPECIES_OPTIONS)
            angler_name = st.text_input("Angler Name (who caught the fish)")
            certifying_captain = st.text_input("Certifying Captain's Name")
            weight = st.number_input("Weight (lbs)", min_value=0.0, step=0.1)
            colv1, colv2 = st.columns(2)
            with colv1:
                landing_video = st.file_uploader("1. Landing Video (show wristband)", type=["mp4", "mov", "avi"])
            with colv2:
                weighin_video = st.file_uploader("2. Weigh-in Video (show wristband + scale)", type=["mp4", "mov", "avi"])
            submitted = st.form_submit_button("Submit Catch")
            if submitted:
                if submit_catch(st.session_state.logged_user, division, species, weight, angler_name, certifying_captain, landing_video, weighin_video):
                    st.success("Catch submitted successfully! Form cleared for next entry.")

    with tabs[1]:
        st.header("Live Leaderboards")
        div = st.selectbox("Select Division", ["Pelagic", "Reef"])
        leaderboard = get_leaderboard(div)
        st.markdown(leaderboard.to_html(escape=False, index=False), unsafe_allow_html=True)

    with tabs[2]:
        st.header("Social Feed")
        content = st.text_area("Share your story or big catch!")
        media = st.file_uploader("Add photo/video", type=["jpg", "png", "mp4", "mov"], key="social")
        if st.button("Post"):
            add_post(st.session_state.logged_user, content, media)
            st.success("Posted!")
        st.write("### Recent Posts")
        for post in reversed(st.session_state.posts[-20:]):
            st.write(f"**{post['user']}** – {post['date']}")
            st.write(post['content'])
            if post['media']:
                st.write(f"Attached: {post['media']}")
            st.divider()

st.caption("Year-long tournament: Feb 1 – Nov 30, 2026 | All catches require landing + weigh-in videos showing daily wristband and clear scale reading | Tight lines!")
