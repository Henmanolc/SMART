import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_persistence import save_assessment_history

def render_settings_page():
    """Render the settings page with all configuration options."""
    st.header("⚙️ Einstellungen")
    
    # Check if user is logged in
    if not st.session_state.get('current_user_id'):
        st.warning("Bitte melde dich zuerst an, um auf die Einstellungen zuzugreifen.")
        return
    
    # User info (read-only)
    st.subheader("Benutzerinformationen")
    user_name = st.session_state.get('user_name', 'Unbekannt')
    user_email = st.session_state.get('user_email', 'Unbekannt')
    user_id = st.session_state.get('current_user_id', 'Unbekannt')
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Name", value=user_name, disabled=True)
        st.text_input("Benutzer-ID", value=user_id, disabled=True)
    with col2:
        st.text_input("Email", value=user_email, disabled=True)
    
    # User preferences
    st.subheader("Benutzereinstellungen")
    
    user_name = st.text_input("Name", value=st.session_state.get('user_name', ''), placeholder="Geben Sie Ihren Namen ein")
    if user_name != st.session_state.get('user_name', ''):
        st.session_state.user_name = user_name
        # Save data when user name changes
        save_assessment_history()
    
    # Language settings
    language = st.selectbox("Sprache", ["Deutsch", "English"], index=0)
    
    # Notification settings
    st.subheader("Benachrichtigungen")
    daily_reminder = st.checkbox("Tägliche Lernerinnerungen", value=st.session_state.get('daily_reminder', False))
    weekly_summary = st.checkbox("Wöchentliche Fortschrittszusammenfassung", value=st.session_state.get('weekly_summary', True))
    module_completion = st.checkbox("Benachrichtigung bei Modulabschluss", value=st.session_state.get('module_completion', True))
    
    # Assessment preferences
    st.subheader("Assessment-Einstellungen")
    default_difficulty = st.slider("Standard-Schwierigkeitsgrad", 1, 5, st.session_state.get('default_difficulty', 3))
    auto_save = st.checkbox("Fortschritt automatisch speichern", value=st.session_state.get('auto_save', True))
    show_explanations = st.checkbox("Erklärungen nach Antworten zeigen", value=st.session_state.get('show_explanations', True))
    
    # Data management
    st.subheader("Datenmanagement")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Fortschritt zurücksetzen", type="secondary"):
            if 'assessment_history' in st.session_state:
                del st.session_state.assessment_history
            if 'last_assessment_result' in st.session_state:
                del st.session_state.last_assessment_result
            st.success("Fortschritt zurückgesetzt!")
            st.rerun()
    
    with col2:
        if 'assessment_history' in st.session_state and st.session_state.assessment_history:
            if st.button("Daten exportieren"):
                # Create export data
                export_data = pd.DataFrame([
                    {
                        'Datum': a['date'].strftime('%d.%m.%Y %H:%M'),
                        'Modul': a['subject'],
                        'Ergebnis': f"{a['score']:.1f}%",
                        'Richtige_Antworten': a['correct_answers'],
                        'Gesamte_Fragen': a['total_questions'],
                        'Dauer': str(a['duration']).split('.')[0]
                    }
                    for a in st.session_state.assessment_history
                ])
                
                # Get user id
                user_id = st.session_state.get('current_user_id', '').strip()
                
                csv = export_data.to_csv(index=False)
                st.download_button(
                    label="CSV herunterladen",
                    data=csv,
                    file_name=f"smart_assessment_data_{user_id}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

    if st.button("Einstellungen speichern"):
        # Save settings to session state
        st.session_state.daily_reminder = daily_reminder
        st.session_state.weekly_summary = weekly_summary
        st.session_state.module_completion = module_completion
        st.session_state.default_difficulty = default_difficulty
        st.session_state.auto_save = auto_save
        st.session_state.show_explanations = show_explanations
        
        st.success("Einstellungen erfolgreich gespeichert!")
