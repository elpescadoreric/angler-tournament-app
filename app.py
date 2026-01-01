import streamlit as st

st.set_page_config(page_title="Everyday Angler Charter Tournament")

st.title("Everyday Angler Charter Tournament App")

st.write("Welcome! The app is live and working.")

st.write("We can now add login, catch uploads, leaderboards, and social feed step by step.")

name = st.text_input("Test it – type your name")
if name:
    st.write(f"Hello {name}! Ready to build the full tournament app?")
