import streamlit as st
import pandas as pd
from datetime import datetime

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

# Functions
def register(username, password, confirm_password, role='Angler'):
    if len(password) < 6:
        st.error("Password must be at least 6 characters")
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

def submit_catch(user, division, species, weight):
    st.session_state.catches.append({
        'user': user,
        'division': division,
        'species': species.lower(),
        'weight': weight,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    })

def get_leaderboard(division):
    df = pd.DataFrame([c for c in st.session_state.catches if c['division'] == division])
    if df.empty:
        return pd.DataFrame(columns=['User', 'Species', 'Weight (lbs)', 'Date'])
    # Sailfish +10 lb bonus
    df['adj_weight'] = df.apply(lambda row: row['weight'] + 10 if 'sailfish' in row['species'] else row['weight'], axis=1)
    df = df.sort_values('adj_weight', ascending=False)[['user', 'species', 'adj_weight', 'date']]
    return df.rename(columns={'user': 'User', 'species': 'Species', 'adj_weight': 'Weight (lbs)', 'date': 'Date'}).head(20)

def add_post(user, content):
    st.session_state.posts.append({
        'user': user,
        'content': content,
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
            new_pass = st.text_input("New Password", type="password")
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
        division = st.selectbox("Division", ["Pelagic", "Reef"])
        species = st.selectbox("Species", SPECIES_OPTIONS)
        weight = st.number_input("Weight (lbs)", min_value=0.0, step=0.1)
        if st.button("Submit Catch"):
            submit_catch(st.session_state.logged_user, division, species, weight)
            st.success("Catch submitted! Check the leaderboard.")

    with tabs[1]:
        st.header("Live Leaderboards")
        div = st.selectbox("Select Division", ["Pelagic", "Reef"])
        leaderboard = get_leaderboard(div)
        st.dataframe(leaderboard, use_container_width=True)

    with tabs[2]:
        st.header("Social Feed")
        content = st.text_area("Share your fishing story or big catch!")
        if st.button("Post"):
            add_post(st.session_state.logged_user, content)
            st.success("Posted!")
        st.write("### Recent Posts")
        for post in reversed(st.session_state.posts[-20:]):
            st.write(f"**{post['user']}** – {post['date']}")
            st.write(post['content'])
            st.divider()

st.caption("Year-long tournament: Feb 1 – Nov 30, 2026 | Tight lines!")
