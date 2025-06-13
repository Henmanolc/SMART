# start with: streamlit run smart.py
# open browser and go to: http://localhost:8501
# This script provides a Streamlit-based assessment and review tool for restaurant and POS system administration training.
# It includes modules for system setup, article configuration, payment options, hardware setup, and more.
# Supports German language training content with assessment tracking and progress monitoring.
# (c) 2025 Henry Bischoff / Sebatian Pechhold SIDES, Last updated: 2025-06-10

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import random
from utils.questionLoader import QuestionLoader

# Import page modules
from pages.settings import render_settings_page
from pages.progress import render_progress_page
from pages.assessment import render_assessment_page

# Import data persistence utilities
from utils.data_persistence import initialize_user_data
from utils.user_management import render_user_selection

# Page configuration
st.set_page_config(
    page_title="SMART - Sides Mastery Assessment & Review Tool",
    page_icon="📚",
    layout="wide"
)

# Load custom CSS from external file
def load_css(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file {file_name} not found. Using default styling.")

# Apply custom styling
load_css('assets/styles.css')

# Initialize question loader
@st.cache_resource
def get_question_loader():
    return QuestionLoader()

question_loader = get_question_loader()

# Sidebar navigation
st.sidebar.title("Navigation")

# Add user selection to sidebar
render_user_selection()

# Only show navigation if user is logged in
if st.session_state.get('current_user_id'):
    page = st.sidebar.selectbox(
        "Bereich auswählen:",
        ["Home", "Assessment", "Progress Tracking", "Settings"]
    )
else:
    page = None

# Initialize user data persistence only if user is logged in
if st.session_state.get('current_user_id'):
    initialize_user_data()

# Main title with logo
try:
    # Create title with logo - better mobile layout
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image("assets/SIDES_bw.png", width=55)
    with col2:
        st.markdown('<h1 style="margin-top: 0; padding-top: 0; padding-left: 10px;">SMART: Sides Mastery Assessment & Review Tool</h1>', unsafe_allow_html=True)
except FileNotFoundError:
    # Fallback if logo file doesn't exist
    st.title("📚 SMART: Sides Mastery Assessment & Review Tool")

# Authentication check and user-specific content
if not st.session_state.get('current_user_id'):
    # Show general information about SMART for unauthenticated users
    st.header("Willkommen bei SMART")
    st.write("""
    Das Sides Mastery Assessment & Review Tool hilft dir dabei, dein **Wissen über unsere Produkte** zu testen und zu verbessern. 
    Dieses interaktive **Schulungssystem** wurde speziell für Mitarbeiter entwickelt, die mit den unterschiedlichen Sides-Produkten arbeiten und ihre **Fachkompetenz** in verschiedenen Bereichen wie Systemkonfiguration, Artikelmanagement, Ecommerce und Zahlungsabwicklung vertiefen möchten. 
    Durch **strukturierte Assessments** mit verschiedenen Schwierigkeitsgraden kannst du deinen **Lernfortschritt** verfolgen und gezielt an deinen Schwächen arbeiten. 
    Das Tool bietet **detailliertes Feedback** zu deinen Antworten und hilft dir dabei, komplexe Systemzusammenhänge besser zu verstehen.
    """)

    st.subheader("**Verfügbare Module:**")

    # Create 3 columns for the module list
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        - 🏪 Grundeinrichtung System & Administration
        - 📦 Artikelkonfiguration & Warengruppen
        - 💳 Zahlungsoptionen & Payment-Provider
        - 🖥️ Hardware-Konfiguration (Drucker, Display)
        """)

    with col2:
        st.markdown("""
        - 🧾 POS-System & Bestellabwicklung
        - 🚚 Liefermanagement & DaaS Integration
        - 👨‍🍳 Kitchen Manager & Küchenverwaltung
        - 🏆 Loyalty Programme & Kundenbindung
        """)

    with col3:
        st.markdown("""
        - 📱 Webshop, App & Self-Order Terminal
        - 📊 Warenwirtschaft & Lagerverwaltung
        """)

    st.markdown("---")
    st.header("🔐 Anmeldung erforderlich")
    st.info("Bitte melde Dich in der Seitenleiste an oder erstelle einen neuen Account.")
    st.write("Nach der Anmeldung hast Du Zugang zu:")
    st.write("- 📝 **Assessment Center** - Interaktive Tests zu verschiedenen Modulen")
    st.write("- 📊 **Progress Tracking** - Verfolge Deinen Lernfortschritt")
    st.write("- ⚙️ **Settings** - Personalisiere Deine Einstellungen")
    st.stop()

# Home page content for authenticated users
if page == "Home":
    st.header("Willkommen bei SMART")
    st.write("""
    Das Sides Mastery Assessment & Review Tool hilft dir dabei, dein **Wissen über unsere Produkte** zu testen und zu verbessern. 
    Dieses interaktive **Schulungssystem** wurde speziell für Mitarbeiter entwickelt, die mit den unterschiedlichen Sides-Produkten arbeiten und ihre **Fachkompetenz** in verschiedenen Bereichen wie Systemkonfiguration, Artikelmanagement, Ecommerce und Zahlungsabwicklung vertiefen möchten. 
    Durch **strukturierte Assessments** mit verschiedenen Schwierigkeitsgraden kannst du deinen **Lernfortschritt** verfolgen und gezielt an deinen Schwächen arbeiten. 
    Das Tool bietet **detailliertes Feedback** zu deinen Antworten und hilft dir dabei, komplexe Systemzusammenhänge besser zu verstehen.
    """)
    
    st.subheader("**Verfügbare Module:**")
    
    # Create 3 columns for the module list
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        - 🏪 Grundeinrichtung System & Administration
        - 📦 Artikelkonfiguration & Warengruppen
        - 💳 Zahlungsoptionen & Payment-Provider
        - 🖥️ Hardware-Konfiguration (Drucker, Display)
        """)
    
    with col2:
        st.markdown("""
        - 🧾 POS-System & Bestellabwicklung
        - 🚚 Liefermanagement & DaaS Integration
        - 👨‍🍳 Kitchen Manager & Küchenverwaltung
        - 🏆 Loyalty Programme & Kundenbindung
        """)
    
    with col3:
        st.markdown("""
        - 📱 Webshop, App & Self-Order Terminal
        - 📊 Warenwirtschaft & Lagerverwaltung
        """)

    st.markdown("---")

    # User-specific metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        completed_assessments = len(st.session_state.get('assessment_history', []))
        st.metric("Absolvierte Tests", str(completed_assessments))
    
    with col2:
        if 'assessment_history' in st.session_state and st.session_state.assessment_history:
            avg_score = sum(a['score'] for a in st.session_state.assessment_history) / len(st.session_state.assessment_history)
            st.metric("Durchschnittsergebnis", f"{avg_score:.0f}%")
        else:
            st.metric("Durchschnittsergebnis", "0%")
    
    with col3:
        st.metric("Lernstreak", "0 Tage")

    st.markdown("---")

    # Display available modules from question files in collapsible section
    available_modules = question_loader.get_available_modules()
    if available_modules:
        with st.expander("📚 Verfügbare Fragen-Module anzeigen", expanded=False):
            for module in available_modules:
                module_data = question_loader.load_module_questions(module)
                question_count = len(module_data.get('questions', []))
                difficulty_range = "N/A"
                if question_count > 0:
                    difficulties = [q.get('difficulty', 1) for q in module_data['questions']]
                    difficulty_range = f"{min(difficulties)}-{max(difficulties)}"
                st.write(f"• {module} ({question_count} Fragen, Schwierigkeit: {difficulty_range})")

# Assessment page
elif page == "Assessment":
    render_assessment_page(question_loader)

# Progress Tracking page (now includes review functionality)
elif page == "Progress Tracking":
    render_progress_page(question_loader)

# Settings page
elif page == "Settings":
    render_settings_page()

# Footer
st.markdown("---")
st.markdown("*SMART: Sides Mastery Assessment & Review Tool v1.0 - Restaurant & POS System Training*")
