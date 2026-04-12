import streamlit as st

st.title("🤝 UW iStartup Matcher")
st.write("If you can see this, your development environment is ready!")

# Simple input test
name = st.text_input("What is your name?")
if name:
    st.write(f"Hello {name}, let's find you a co-founder.")