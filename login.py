import os
import streamlit as st
import ast
import secrets
from google.auth import default
CREDENTIAL, PROJECT_ID = default()
keys = ast.literal_eval(os.environ.get("credentials", ""))

if keys:
    username = keys['username']
    password = keys['password']

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        correct_username = secrets.compare_digest(st.session_state["username"], username)
        correct_password = secrets.compare_digest(st.session_state['password'], password)
        if correct_password and correct_username:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()

