import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
import os

def get_supabase_client() -> Client:
    """Initialize Supabase client."""
    try:
        # Try to get credentials from Streamlit secrets (for cloud deployment)
        if hasattr(st, 'secrets') and 'supabase' in st.secrets:
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["anon_key"]
        else:
            # For local development - you'll need to set these
            url = os.getenv("SUPABASE_URL", "YOUR_SUPABASE_URL_HERE")
            key = os.getenv("SUPABASE_ANON_KEY", "YOUR_SUPABASE_ANON_KEY_HERE")
        
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        st.error(f"Supabase connection failed: {e}")
        return None

def is_supabase_available():
    """Check if Supabase backend is available."""
    client = get_supabase_client()
    return client is not None

def load_users_from_supabase():
    """Load all users from Supabase."""
    client = get_supabase_client()
    if not client:
        return pd.DataFrame(columns=['name', 'email', 'password', 'created_date', 'user_id'])
    
    try:
        response = client.table('users').select('*').execute()
        
        if not hasattr(response, 'data') or not response.data:
            return pd.DataFrame(columns=['name', 'email', 'password', 'created_date', 'user_id'])
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(response.data)
        # Rename created_at to created_date for compatibility
        if 'created_at' in df.columns:
            df['created_date'] = df['created_at']
        
        # Ensure all required columns exist
        required_cols = ['name', 'email', 'password', 'created_date', 'user_id']
        for col in required_cols:
            if col not in df.columns:
                df[col] = ''
        
        return df[required_cols]
    
    except Exception as e:
        st.warning(f"Could not load users from Supabase: {e}")
        return pd.DataFrame(columns=['name', 'email', 'password', 'created_date', 'user_id'])

def save_user_to_supabase(name, email, password, user_id):
    """Save new user to Supabase."""
    client = get_supabase_client()
    if not client:
        return False
    
    try:
        # Check if user_id already exists
        existing_check = client.table('users').select('user_id').eq('user_id', user_id).execute()
        if existing_check.data:
            st.error(f"User ID {user_id} already exists in Supabase")
            return False
        
        response = client.table('users').insert({
            'name': name,
            'email': email,
            'password': password,  # Plain text for development
            'user_id': user_id
        }).execute()
        
        if hasattr(response, 'data') and response.data:
            st.success(f"User {name} saved to Supabase successfully!")
            return True
        else:
            st.error("No data returned from Supabase insert")
            return False
    
    except Exception as e:
        # More detailed error information
        error_msg = str(e)
        st.error(f"Error saving user to Supabase: {error_msg}")
        
        # Check if it's a duplicate key error
        if 'duplicate key' in error_msg.lower() or 'unique constraint' in error_msg.lower():
            st.error("User with this email or user_id already exists")
        
        return False

def load_assessments_from_supabase(user_id):
    """Load assessment history for specific user from Supabase."""
    client = get_supabase_client()
    if not client:
        return []
    
    try:
        # First check if table exists and has required columns
        response = client.table('assessments').select('user_id').limit(1).execute()
        
        # Now get actual data
        response = client.table('assessments').select('*').eq('user_id', user_id).execute()
        
        user_assessments = []
        for record in response.data:
            # Handle different date formats
            date_str = record['date']
            if 'T' in date_str:
                if date_str.endswith('Z'):
                    date_str = date_str.replace('Z', '+00:00')
                assessment_date = datetime.fromisoformat(date_str)
            else:
                assessment_date = datetime.fromisoformat(date_str)
            
            assessment = {
                'date': assessment_date,
                'subject': record['subject'],
                'difficulty': record['difficulty'],
                'score': float(record['score']),
                'correct_answers': record['correct_answers'],
                'total_questions': record['total_questions'],
                'duration': pd.Timedelta(seconds=record['duration_seconds']),
                'results': []  # Detailed results not stored in summary
            }
            user_assessments.append(assessment)
        
        return user_assessments
    
    except Exception as e:
        error_msg = str(e)
        if 'column' in error_msg and 'does not exist' in error_msg:
            st.warning("Assessment table structure needs to be updated. Please check Supabase table columns.")
        else:
            st.warning(f"Could not load assessments from Supabase: {e}")
        return []

def save_assessment_to_supabase(user_id, assessment_result):
    """Save assessment result to Supabase."""
    client = get_supabase_client()
    if not client:
        return False
    
    try:
        response = client.table('assessments').insert({
            'user_id': user_id,
            'date': assessment_result['date'].isoformat(),
            'subject': assessment_result['subject'],
            'difficulty': assessment_result['difficulty'],
            'score': assessment_result['score'],
            'correct_answers': assessment_result['correct_answers'],
            'total_questions': assessment_result['total_questions'],
            'duration_seconds': assessment_result['duration'].total_seconds()
        }).execute()
        
        return len(response.data) > 0
    
    except Exception as e:
        st.error(f"Error saving assessment to Supabase: {e}")
        return False
