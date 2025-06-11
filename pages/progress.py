import streamlit as st
from datetime import datetime, timedelta

def render_progress_page(question_loader):
    """Render the progress tracking page with learning goals and achievements."""
    st.header("📈 Fortschrittsverfolgung & Review")
    
    # Check if user is logged in
    if not st.session_state.get('current_user_id'):
        st.warning("Bitte melde dich zuerst an, um deinen Fortschritt zu sehen.")
        return

    # Get assessment history
    history = st.session_state.get('assessment_history', [])
    
    # === REVIEW SECTION ===
    if history:
                
        # Summary statistics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Gesamt Assessments", len(history))
        
        with col2:
            avg_score = sum(a['score'] for a in history) / len(history)
            st.metric("Durchschnittsscore", f"{avg_score:.1f}%")
        
        with col3:
            best_score = max(a['score'] for a in history)
            st.metric("Bester Score", f"{best_score:.0f}%")
        
        with col4:
            modules_covered = len(set(a['subject'] for a in history))
            st.metric("Module absolviert", modules_covered)
        
        with col5:
            # Performance trend as fifth tile
            if len(history) >= 2:
                recent_scores = [a['score'] for a in sorted(history, key=lambda x: x['date'])[-5:]]
                if recent_scores[-1] > recent_scores[0]:
                    trend_text = "Aufwärts 📈"
                elif recent_scores[-1] < recent_scores[0]:
                    trend_text = "Abwärts 📉"
                else:
                    trend_text = "Stabil ➡️"
            else:
                trend_text = "N/A"
            st.metric("Trend", trend_text)

        # Achievements icons section
        st.markdown("### 🏆 Achievements")
        
        # Get all achievements
        achievements = [
            # Basic achievements
            {"emoji": "🎯", "name": "Erstes Assessment", "desc": "Assessment-Neuling abgeschlossen", "condition": len(history) >= 1},
            {"emoji": "🔥", "name": "Assessment-Serie", "desc": "3 Assessments in Folge", "condition": len(history) >= 3},
            {"emoji": "💎", "name": "Assessment-Veteran", "desc": "10 Assessments abgeschlossen", "condition": len(history) >= 10},
            {"emoji": "👑", "name": "Assessment-König", "desc": "25 Assessments gemeistert", "condition": len(history) >= 25},
            
            # Score-based achievements
            {"emoji": "⭐", "name": "Perfektionist", "desc": "90%+ Punktzahl erreicht", "condition": any(a['score'] >= 90 for a in history)},
            {"emoji": "🏆", "name": "Konsistenz-Champion", "desc": "3x über 90% Punktzahl", "condition": len([a for a in history if a['score'] >= 90]) >= 3},
            {"emoji": "💯", "name": "Flawless Victory", "desc": "100% Punktzahl erreicht", "condition": any(a['score'] == 100 for a in history)},
            
            # Module-based achievements
            {"emoji": "📚", "name": "Multi-Talent", "desc": "2 verschiedene Module", "condition": len(set(a['subject'] for a in history)) >= 2},
            {"emoji": "🎓", "name": "Wissensdurst", "desc": "5 verschiedene Module", "condition": len(set(a['subject'] for a in history)) >= 5},
            {"emoji": "🧠", "name": "Master-Student", "desc": "8 verschiedene Module", "condition": len(set(a['subject'] for a in history)) >= 8},
            
            # Speed achievements
            {"emoji": "⚡", "name": "Blitzschnell", "desc": "Assessment unter 5 Minuten", "condition": any(a['duration'].total_seconds() < 300 for a in history)},
            
            # Streak achievements
            {"emoji": "🔗", "name": "Learning Streak", "desc": "5 Assessments in Serie", "condition": len(history) >= 5},
            
            # Weekly achievements
            {"emoji": "📅", "name": "Wochenkrieger", "desc": "7+ Assessments pro Woche", "condition": len(history) >= 7},
        ]
        
        # Display achievement icons in a horizontal layout with hover titles
        icon_display = ""
        for achievement in achievements:
            if achievement["condition"]:
                # Achieved - full color with hover title
                icon_display += f"<span title='{achievement['name']}: {achievement['desc']}' style='cursor: help;'>{achievement['emoji']}</span> "
            else:
                # Not achieved - lighter color with hover title
                icon_display += f"<span title='{achievement['name']}: {achievement['desc']}' style='opacity: 0.3; filter: grayscale(50%); cursor: help;'>{achievement['emoji']}</span> "
        
        st.markdown(f"<div style='font-size: 2em; line-height: 1.5;'>{icon_display}</div>", unsafe_allow_html=True)
        
        st.markdown("---")

        # === EXISTING PROGRESS SECTION ===
        # Progress bars at the top
        st.subheader("Aktueller Fortschritt")
        
        if 'assessment_history' in st.session_state and st.session_state.assessment_history:
            history = st.session_state.assessment_history
            
            # Weekly progress (assessments this week)
            weekly_assessments = len(history)  # Simplified - would need actual date filtering
            st.progress(min(weekly_assessments / 5, 1.0), text=f"Wöchentliches Ziel: {weekly_assessments}/5 Assessments")
            
            # Average score progress
            avg_score = sum(a['score'] for a in history) / len(history)
            st.progress(avg_score / 100, text=f"Durchschnittsergebnis: {avg_score:.0f}%/90%")
            
            # Module coverage
            available_modules = question_loader.get_available_modules()
            covered_modules = len(set(a['subject'] for a in history))
            module_coverage = covered_modules / len(available_modules) if available_modules else 0
            st.progress(module_coverage, text=f"Module erforscht: {covered_modules}/{len(available_modules)}")
        else:
            st.progress(0.0, text="Wöchentliches Ziel: 0/5 Assessments")
            st.progress(0.0, text="Durchschnittsergebnis: 0%/90%")
            st.progress(0.0, text="Module erforscht: 0/verfügbar")

        st.markdown("---")

                # Recent assessments table
        st.markdown("### 📋 Letzte Assessments")
        
        # Convert to display format
        display_data = []
        for assessment in sorted(history, key=lambda x: x['date'], reverse=True)[:10]:
            display_data.append({
                'Datum': assessment['date'].strftime('%d.%m.%Y %H:%M'),
                'Modul': assessment['subject'],
                'Score': f"{assessment['score']:.0f}%",
                'Fragen': f"{assessment['correct_answers']}/{assessment['total_questions']}",
                'Dauer': str(assessment['duration']).split('.')[0],
                'Schwierigkeit': f"bis {assessment['difficulty']} ⭐"
            })
        
        if display_data:
            st.dataframe(display_data, use_container_width=True)

        st.markdown("---")
        
        # Performance trends
        
        if len(history) >= 2:
            # Simple trend analysis (remove the info box since it's now in the tile)
            # Module performance
            module_performance = {}
            for assessment in history:
                module = assessment['subject']
                if module not in module_performance:
                    module_performance[module] = []
                module_performance[module].append(assessment['score'])
            
            st.markdown("### 📚 Leistung nach Modulen")
            for module, scores in module_performance.items():
                avg_score = sum(scores) / len(scores)
                best_score = max(scores)
                attempts = len(scores)
                st.write(f"**{module}**: {avg_score:.1f}% Ø ({attempts} Versuche, Bestwert: {best_score:.0f}%)")
        
        st.markdown("---")
    
    else:
        st.info("📝 Noch keine Assessments absolviert. Starte dein erstes Assessment!")
        st.markdown("---")

    # === LEARNING GOALS SECTION ===
    
    # Achievements section
    st.subheader("Errungenschaften")
    
    # Get assessment history
    history = st.session_state.get('assessment_history', [])
    
    # Define all possible achievements with their conditions
    achievements = [
        # Basic achievements
        {"emoji": "🎯", "name": "Erstes Assessment", "desc": "Assessment-Neuling abgeschlossen", "condition": len(history) >= 1},
        {"emoji": "🔥", "name": "Assessment-Serie", "desc": "3 Assessments in Folge", "condition": len(history) >= 3},
        {"emoji": "💎", "name": "Assessment-Veteran", "desc": "10 Assessments abgeschlossen", "condition": len(history) >= 10},
        {"emoji": "👑", "name": "Assessment-König", "desc": "25 Assessments gemeistert", "condition": len(history) >= 25},
        
        # Score-based achievements
        {"emoji": "⭐", "name": "Perfektionist", "desc": "90%+ Punktzahl erreicht", "condition": any(a['score'] >= 90 for a in history)},
        {"emoji": "🏆", "name": "Konsistenz-Champion", "desc": "3x über 90% Punktzahl", "condition": len([a for a in history if a['score'] >= 90]) >= 3},
        {"emoji": "💯", "name": "Flawless Victory", "desc": "100% Punktzahl erreicht", "condition": any(a['score'] == 100 for a in history)},
        
        # Module-based achievements
        {"emoji": "📚", "name": "Multi-Talent", "desc": "2 verschiedene Module", "condition": len(set(a['subject'] for a in history)) >= 2},
        {"emoji": "🎓", "name": "Wissensdurst", "desc": "5 verschiedene Module", "condition": len(set(a['subject'] for a in history)) >= 5},
        {"emoji": "🧠", "name": "Master-Student", "desc": "8 verschiedene Module", "condition": len(set(a['subject'] for a in history)) >= 8},
        
        # Speed achievements
        {"emoji": "⚡", "name": "Blitzschnell", "desc": "Assessment unter 5 Minuten", "condition": any(a['duration'].total_seconds() < 300 for a in history)},
        
        # Streak achievements
        {"emoji": "🔗", "name": "Learning Streak", "desc": "5 Assessments in Serie", "condition": len(history) >= 5},
        
        # Weekly achievements
        {"emoji": "📅", "name": "Wochenkrieger", "desc": "7+ Assessments pro Woche", "condition": len(history) >= 7},
    ]
    
    # Display achievements in 3 columns
    achievements_per_col = len(achievements) // 3
    remainder = len(achievements) % 3
    
    col1, col2, col3 = st.columns(3)
    
    # First column
    with col1:
        end_idx = achievements_per_col + (1 if remainder > 0 else 0)
        for achievement in achievements[:end_idx]:
            if achievement["condition"]:
                st.markdown(f"**{achievement['emoji']} {achievement['name']}** ✅")
                st.caption(achievement['desc'])
            else:
                st.markdown(f"<span style='color: #888; opacity: 0.6'>{achievement['emoji']} **{achievement['name']}** 🔒</span>", unsafe_allow_html=True)
                st.caption(achievement['desc'])
    
    # Second column
    with col2:
        start_idx = end_idx
        end_idx = start_idx + achievements_per_col + (1 if remainder > 1 else 0)
        for achievement in achievements[start_idx:end_idx]:
            if achievement["condition"]:
                st.markdown(f"**{achievement['emoji']} {achievement['name']}** ✅")
                st.caption(achievement['desc'])
            else:
                st.markdown(f"<span style='color: #888; opacity: 0.6'>{achievement['emoji']} **{achievement['name']}** 🔒</span>", unsafe_allow_html=True)
                st.caption(achievement['desc'])
    
    # Third column
    with col3:
        start_idx = end_idx
        for achievement in achievements[start_idx:]:
            if achievement["condition"]:
                st.markdown(f"**{achievement['emoji']} {achievement['name']}** ✅")
                st.caption(achievement['desc'])
            else:
                st.markdown(f"<span style='color: #888; opacity: 0.6'>{achievement['emoji']} **{achievement['name']}** 🔒</span>", unsafe_allow_html=True)
                st.caption(achievement['desc'])

    if not history:
        st.info("💡 Starte dein erstes Assessment, um Errungenschaften freizuschalten!")
