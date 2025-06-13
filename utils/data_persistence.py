import pandas as pd
import os
from datetime import datetime
import streamlit as st
from .supabase_backend import (
    load_assessments_from_supabase,
    save_assessment_to_supabase,
    is_supabase_available
)

def get_user_data_file():
    """Get the user data CSV file path based on user ID."""
    user_id = st.session_state.get('current_user_id', 'default_user')
    
    # Create data directory if it doesn't exist
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    return os.path.join(data_dir, f"user_data_{user_id}.csv")

def save_assessment_history():
    """Save assessment history to CSV file."""
    if 'assessment_history' not in st.session_state:
        return
    
    history = st.session_state.assessment_history
    if not history:
        return
    
    # Convert assessment history to DataFrame
    data = []
    for assessment in history:
        data.append({
            'date': assessment['date'].isoformat(),
            'subject': assessment['subject'],
            'difficulty': assessment['difficulty'],
            'score': assessment['score'],
            'correct_answers': assessment['correct_answers'],
            'total_questions': assessment['total_questions'],
            'duration_seconds': assessment['duration'].total_seconds()
        })
    
    df = pd.DataFrame(data)
    file_path = get_user_data_file()
    
    try:
        df.to_csv(file_path, index=False)
    except Exception as e:
        st.error(f"Fehler beim Speichern der Daten: {e}")

def load_assessment_history():
    """Load assessment history from Supabase or CSV file."""
    user_id = st.session_state.get('current_user_id', 'default_user')
    
    # Try Supabase first (for cloud deployment)
    if is_supabase_available():
        return load_assessments_from_supabase(user_id)
    
    # Fallback to local CSV (for local development)
    file_path = get_user_data_file()
    
    if not os.path.exists(file_path):
        return []
    
    try:
        df = pd.read_csv(file_path)
        history = []
        
        for _, row in df.iterrows():
            assessment = {
                'date': datetime.fromisoformat(row['date']),
                'subject': row['subject'],
                'difficulty': row['difficulty'],
                'score': row['score'],
                'correct_answers': row['correct_answers'],
                'total_questions': row['total_questions'],
                'duration': pd.Timedelta(seconds=row['duration_seconds']),
                'results': []
            }
            history.append(assessment)
        
        return history
    
    except Exception as e:
        st.error(f"Fehler beim Laden der Daten: {e}")
        return []

def initialize_user_data():
    """Initialize user data by loading from CSV if available."""
    current_user_id = st.session_state.get('current_user_id')
    
    if current_user_id:
        last_loaded_user = st.session_state.get('last_loaded_user_id')
        has_assessment_history = 'assessment_history' in st.session_state
        assessment_history_length = len(st.session_state.get('assessment_history', []))
        
        if last_loaded_user != current_user_id or not has_assessment_history or assessment_history_length == 0:
            st.session_state.pop('assessment_history', None)
            
            history = load_assessment_history()
            
            if history:
                st.session_state.assessment_history = history
            else:
                st.session_state.assessment_history = []
            
            st.session_state.last_loaded_user_id = current_user_id
            st.session_state.data_loaded = True

def auto_save_assessment(assessment_result):
    """Automatically save assessment when completed."""
    if 'assessment_history' not in st.session_state:
        st.session_state.assessment_history = []
    
    st.session_state.assessment_history.append(assessment_result)
    
    user_id = st.session_state.get('current_user_id', 'default_user')
    
    # Try Supabase first
    if is_supabase_available():
        save_assessment_to_supabase(user_id, assessment_result)
    else:
        # Fallback to local CSV
        save_assessment_history()
