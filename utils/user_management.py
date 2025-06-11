import pandas as pd
import os
import streamlit as st
from datetime import datetime

def get_users_file():
    """Get the users registry file path."""
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return os.path.join(data_dir, "users.csv")

def load_users():
    """Load all registered users."""
    users_file = get_users_file()
    if not os.path.exists(users_file):
        return pd.DataFrame(columns=['name', 'email', 'created_date', 'user_id'])
    
    try:
        return pd.read_csv(users_file)
    except Exception:
        return pd.DataFrame(columns=['name', 'email', 'created_date', 'user_id'])

def save_users(users_df):
    """Save users registry."""
    users_file = get_users_file()
    try:
        users_df.to_csv(users_file, index=False)
        return True
    except Exception as e:
        st.error(f"Fehler beim Speichern der Benutzer: {e}")
        return False

def create_user(name, email):
    """Create a new user account."""
    users_df = load_users()
    
    # Check if email already exists
    if email in users_df['email'].values:
        return False, "Email bereits registriert"
    
    # Generate user ID
    user_id = f"user_{len(users_df) + 1:04d}"
    
    # Add new user
    new_user = pd.DataFrame({
        'name': [name],
        'email': [email],
        'created_date': [datetime.now().isoformat()],
        'user_id': [user_id]
    })
    
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    
    if save_users(users_df):
        return True, user_id
    else:
        return False, "Fehler beim Speichern"

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
    """Render user selection or creation interface."""
    #st.sidebar.markdown("---")
    st.sidebar.subheader("👤 Benutzer")
    
    users_df = load_users()
    current_user_id = st.session_state.get('current_user_id', None)
    
    # Always show user selection dropdown if users exist
    if not users_df.empty:
        # Create user display list
        user_options = ["Benutzer auswählen..."] + [
            f"{row['name']} ({row['email']})" 
            for _, row in users_df.iterrows()
        ]
        
        # Find current selection index
        selected_index = 0
        if current_user_id:
            for i, (_, row) in enumerate(users_df.iterrows()):
                if row['user_id'] == current_user_id:
                    selected_index = i + 1
                    break
        
        selected_option = st.sidebar.selectbox(
            "Benutzer wählen:",
            user_options,
            index=selected_index,
            key="user_selection"
        )
        
        # Handle user selection
        if selected_option != "Benutzer auswählen...":
            # Extract email from selection
            email = selected_option.split('(')[1].split(')')[0]
            user_row = users_df[users_df['email'] == email].iloc[0]
            
            # Update session state if different user selected
            if st.session_state.get('current_user_id') != user_row['user_id']:
                st.session_state.current_user_id = user_row['user_id']
                st.session_state.user_name = user_row['name']
                st.session_state.user_email = user_row['email']
                
                # Clear data loading flags to force reload
                st.session_state.pop('assessment_history', None)
                st.session_state.pop('data_loaded', None)
                st.session_state.pop('last_loaded_user_id', None)
                st.rerun()
    
    # Show create user section (always visible, expanded if no users exist)
    expand_create = users_df.empty
    with st.sidebar.expander("Neuen Benutzer erstellen", expanded=expand_create):
        name = st.text_input("Name", key="new_user_name")
        email = st.text_input("Email", key="new_user_email")
        
        if st.button("Account erstellen", key="create_account"):
            if name and email:
                success, result = create_user(name, email)
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
                st.error("Bitte Name und Email eingeben")
    
    # Show current user info
    if st.session_state.get('current_user_id'):
        user_info = get_user_by_id(st.session_state.current_user_id)
        if user_info:
            st.sidebar.info(f"Angemeldet als: **{user_info['name']}**")
    st.sidebar.markdown("---")
