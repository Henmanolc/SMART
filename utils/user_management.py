import pandas as pd
import os
import streamlit as st
from datetime import datetime
from .supabase_backend import (
    load_users_from_supabase,
    save_user_to_supabase,
    is_supabase_available
)

# TODO: Implement password hashing for production security
# Currently passwords are stored as plain text for development convenience
# This allows administrators to see/reset passwords when users forget them
# In a production environment, passwords should be hashed using bcrypt or similar

def get_users_file():
    """Get the users registry file path."""
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return os.path.join(data_dir, "users.csv")

def load_users():
    """Load all registered users from Supabase or local CSV."""
    # Try Supabase first (for cloud deployment)
    if is_supabase_available():
        return load_users_from_supabase()
    
    # Fallback to local CSV (for local development)
    users_file = get_users_file()
    if not os.path.exists(users_file):
        return pd.DataFrame(columns=['name', 'email', 'password', 'created_date', 'user_id'])
    
    try:
        df = pd.read_csv(users_file)
        # Add password column if it doesn't exist (backward compatibility)
        if 'password' not in df.columns:
            df['password'] = ''
        return df
    except Exception:
        return pd.DataFrame(columns=['name', 'email', 'password', 'created_date', 'user_id'])

def save_users(users_df):
    """Save users registry."""
    users_file = get_users_file()
    try:
        users_df.to_csv(users_file, index=False)
        return True
    except Exception as e:
        st.error(f"Fehler beim Speichern der Benutzer: {e}")
        return False

def create_user(name, email, password):
    """Create a new user account with password."""
    users_df = load_users()
    
    # Check if email already exists
    if email in users_df['email'].values:
        return False, "Email bereits registriert"
    
    # Check if name already exists
    if name in users_df['name'].values:
        return False, "Name bereits registriert"
    
    # Generate user ID
    user_id = f"user_{len(users_df) + 1:04d}"
    
    # Try to save to Supabase first
    if is_supabase_available():
        if save_user_to_supabase(name, email, password, user_id):
            return True, user_id
        else:
            return False, "Fehler beim Speichern in Supabase"
    
    # Fallback to local CSV
    new_user = pd.DataFrame({
        'name': [name],
        'email': [email],
        'password': [password],  # Plain text storage for development
        'created_date': [datetime.now().isoformat()],
        'user_id': [user_id]
    })
    
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    
    if save_users(users_df):
        return True, user_id
    else:
        return False, "Fehler beim Speichern"

def authenticate_user(name, password):
    """Authenticate user with name and password.
    
    Note: Uses plain text password comparison for development.
    TODO: Implement secure password hashing/verification for production.
    """
    users_df = load_users()
    # Plain text password comparison (TODO: use hashed comparison in production)
    user_row = users_df[(users_df['name'] == name) & (users_df['password'] == password)]
    
    if user_row.empty:
        return None
    
    return {
        'name': user_row.iloc[0]['name'],
        'email': user_row.iloc[0]['email'],
        'user_id': user_row.iloc[0]['user_id'],
        'created_date': user_row.iloc[0]['created_date']
    }

def get_user_by_id(user_id):
    """Get user information by user ID."""
    users_df = load_users()
    user_row = users_df[users_df['user_id'] == user_id]
    
    if user_row.empty:
        return None
    
    return {
        'name': user_row.iloc[0]['name'],
        'email': user_row.iloc[0]['email'],
        'user_id': user_row.iloc[0]['user_id'],
        'created_date': user_row.iloc[0]['created_date']
    }

def render_user_selection():
    """Render user login or creation interface."""
    st.sidebar.subheader("👤 Benutzer")
    
    users_df = load_users()
    current_user_id = st.session_state.get('current_user_id', None)
    
    # Show current user info if logged in
    if current_user_id:
        user_info = get_user_by_id(current_user_id)
        if user_info:
            st.sidebar.info(f"Angemeldet als: **{user_info['name']}**")
            if st.sidebar.button("Abmelden", key="logout"):
                # Clear session state
                st.session_state.pop('current_user_id', None)
                st.session_state.pop('user_name', None)
                st.session_state.pop('user_email', None)
                st.session_state.pop('assessment_history', None)
                st.session_state.pop('data_loaded', None)
                st.session_state.pop('last_loaded_user_id', None)
                st.rerun()
        st.sidebar.markdown("---")
        return
    
    # Login form
    with st.sidebar.form("login_form"):
        st.write("**Anmelden:**")
        login_name = st.text_input("Name", key="login_name")
        login_password = st.text_input("Passwort", type="password", key="login_password")
        
        if st.form_submit_button("Anmelden"):
            if login_name and login_password:
                user_info = authenticate_user(login_name, login_password)
                if user_info:
                    st.session_state.current_user_id = user_info['user_id']
                    st.session_state.user_name = user_info['name']
                    st.session_state.user_email = user_info['email']
                    
                    # Clear data loading flags to force reload
                    st.session_state.pop('assessment_history', None)
                    st.session_state.pop('data_loaded', None)
                    st.session_state.pop('last_loaded_user_id', None)
                    st.success(f"Willkommen, {user_info['name']}!")
                    st.rerun()
                else:
                    st.error("Ungültiger Name oder Passwort")
            else:
                st.error("Bitte Name und Passwort eingeben")
    
    # Create user section
    expand_create = users_df.empty
    with st.sidebar.expander("Neuen Benutzer erstellen", expanded=expand_create):
        with st.form("create_user_form"):
            name = st.text_input("Name", key="new_user_name")
            email = st.text_input("Email", key="new_user_email")
            password = st.text_input("Passwort", type="password", key="new_user_password")
            password_confirm = st.text_input("Passwort bestätigen", type="password", key="new_user_password_confirm")
            
            if st.form_submit_button("Account erstellen"):
                if name and email and password and password_confirm:
                    if password != password_confirm:
                        st.error("Passwörter stimmen nicht überein")
                    elif len(password) < 4:
                        st.error("Passwort muss mindestens 4 Zeichen lang sein")
                    else:
                        success, result = create_user(name, email, password)
                        if success:
                            st.session_state.current_user_id = result
                            user_info = get_user_by_id(result)
                            st.session_state.user_name = user_info['name']
                            st.session_state.user_email = user_info['email']
                            st.success(f"Account erstellt! Benutzer-ID: {result}")
                            st.rerun()
                        else:
                            st.error(result)
                else:
                    st.error("Bitte alle Felder ausfüllen")
    
    st.sidebar.markdown("---")
