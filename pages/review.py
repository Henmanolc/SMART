import streamlit as st
import pandas as pd
from datetime import datetime

def render_review_page():
    """Render the review page showing assessment history and detailed analysis."""
    st.header("📊 Review & Analyse")
    
    # Recent assessments
    st.subheader("Aktuelle Assessments")
    
    if 'assessment_history' in st.session_state and st.session_state.assessment_history:
        # Convert assessment history to DataFrame
        history_data = []
        for assessment in st.session_state.assessment_history:
            history_data.append({
                'Datum': assessment['date'].strftime('%d.%m.%Y %H:%M'),
                'Modul': assessment['subject'],
                'Ergebnis': f"{assessment['score']:.0f}%",
                'Fragen': f"{assessment['correct_answers']}/{assessment['total_questions']}",
                'Dauer': str(assessment['duration']).split('.')[0]
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True)
        
        # Performance analysis
        if len(st.session_state.assessment_history) >= 2:
            st.subheader("Leistungsanalyse")
            
            # Calculate performance by module
            module_performance = {}
            for assessment in st.session_state.assessment_history:
                module = assessment['subject']
                if module not in module_performance:
                    module_performance[module] = []
                module_performance[module].append(assessment['score'])
            
            # Display module performance
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Durchschnittsergebnisse pro Modul:**")
                for module, scores in module_performance.items():
                    avg_score = sum(scores) / len(scores)
                    st.write(f"• {module}: {avg_score:.0f}%")
            
            with col2:
                st.write("**Verbesserungstrend:**")
                latest_scores = [a['score'] for a in st.session_state.assessment_history[-3:]]
                if len(latest_scores) >= 2:
                    trend = latest_scores[-1] - latest_scores[0]
                    if trend > 0:
                        st.success(f"📈 Verbesserung: +{trend:.0f}%")
                    elif trend < 0:
                        st.error(f"📉 Verschlechterung: {trend:.0f}%")
                    else:
                        st.info("➡️ Gleichbleibend")
        
        # Show detailed review of last assessment if available
        if 'last_assessment_result' in st.session_state:
            _render_last_assessment_review()
            
    else:
        # Sample data for demonstration when no real data exists
        st.info("Noch keine Assessments absolviert. Starten Sie Ihr erstes Assessment!")
        
        sample_data = pd.DataFrame({
            'Datum': [datetime.now().strftime('%d.%m.%Y')] * 3,
            'Modul': [
                'Grundeinrichtung System', 
                'Artikelkonfiguration', 
                'Zahlungsoptionen'
            ],
            'Ergebnis': ['85%', '92%', '78%'],
            'Fragen': ['5/6', '11/12', '7/9'],
            'Dauer': ['3 Min', '8 Min', '6 Min']
        })
        
        st.dataframe(sample_data, use_container_width=True)
        st.caption("*Beispieldaten - Ihre echten Ergebnisse werden hier angezeigt*")

def _render_last_assessment_review():
    """Render detailed review of the last assessment."""
    st.markdown("---")
    st.subheader("📚 Letztes Assessment im Detail")
    
    result = st.session_state.last_assessment_result
    
    # Results header with celebration
    if result['score'] >= 80:
        st.success("🎉 Hervorragend!")
        result_emoji = "🏆"
        result_color = "#28a745"
    elif result['score'] >= 60:
        st.warning("👍 Gut gemacht!")
        result_emoji = "🥈"
        result_color = "#ffc107"
    else:
        st.error("📚 Weiter üben!")
        result_emoji = "📖"
        result_color = "#dc3545"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background-color: {result_color}20; border-radius: 15px; margin: 20px 0;">
    <h1 style="color: {result_color}; margin: 0;">{result_emoji} Assessment Review</h1>
    <h2 style="margin: 10px 0; color: {result_color};">{result['score']:.0f}%</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed metrics
    st.markdown("### 📊 Ergebnisse im Detail")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Gesamtergebnis", 
            f"{result['score']:.0f}%",
            delta=f"{result['score']-75:.0f}%" if result['score'] >= 75 else None
        )
    
    with col2:
        st.metric(
            "Richtige Antworten", 
            f"{result['correct_answers']}/{result['total_questions']}"
        )
    
    with col3:
        st.metric(
            "Benötigte Zeit", 
            str(result['duration']).split('.')[0]
        )
    
    with col4:
        # Safe calculation of average difficulty with fallback
        try:
            avg_difficulty = sum(r.get('difficulty', 1) for r in result['results']) / len(result['results'])
            st.metric(
                "⭐ Ø Schwierigkeit", 
                f"{avg_difficulty:.1f}"
            )
        except (KeyError, ZeroDivisionError):
            st.metric(
                "⭐ Ø Schwierigkeit", 
                "N/A"
            )
    
    # Performance breakdown
    st.markdown("### 📈 Leistungsanalyse")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance by difficulty - with error handling
        st.write("**Leistung nach Schwierigkeitsgrad:**")
        diff_performance = {}
        for r in result['results']:
            diff = r.get('difficulty', 1)  # Use get() with default
            if diff not in diff_performance:
                diff_performance[diff] = {'correct': 0, 'total': 0}
            diff_performance[diff]['total'] += 1
            if r['is_correct']:
                diff_performance[diff]['correct'] += 1
        
        for diff in sorted(diff_performance.keys()):
            perf = diff_performance[diff]
            percentage = (perf['correct'] / perf['total']) * 100
            stars = "⭐" * diff
            st.write(f"{stars}: {perf['correct']}/{perf['total']} ({percentage:.0f}%)")
    
    with col2:
        # Quick stats
        st.write("**Zusammenfassung:**")
        st.write(f"• Modul: {result['subject']}")
        # Safe access to difficulty with fallback
        difficulty_level = result.get('difficulty', 'N/A')
        if difficulty_level != 'N/A':
            st.write(f"• Schwierigkeitsgrad: bis {difficulty_level} ⭐")
        else:
            st.write(f"• Schwierigkeitsgrad: N/A")
        st.write(f"• Datum: {result['date'].strftime('%d.%m.%Y %H:%M')}")
        
        # Performance rating
        if result['score'] >= 90:
            st.write("• Bewertung: ⭐⭐⭐ Excellent")
        elif result['score'] >= 80:
            st.write("• Bewertung: ⭐⭐ Sehr gut")
        elif result['score'] >= 70:
            st.write("• Bewertung: ⭐ Gut")
        else:
            st.write("• Bewertung: Verbesserung möglich")
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Neues Assessment", type="primary", use_container_width=True):
            del st.session_state.last_assessment_result
            if 'show_detailed_results' in st.session_state:
                del st.session_state.show_detailed_results
            st.rerun()
    
    with col2:
        if st.button("📊 Detaillierte Auswertung", use_container_width=True):
            st.session_state.show_detailed_results = not st.session_state.get('show_detailed_results', False)
            st.rerun()
    
    with col3:
        if st.button("🏠 Zur Startseite", use_container_width=True):
            # Navigate to home page (this would need navigation state management)
            st.rerun()
    
    # Detailed results (show if requested)
    if st.session_state.get('show_detailed_results', False):
        st.markdown("---")
        st.markdown("### 🔍 Frage-für-Frage Analyse")
        
        for i, question_result in enumerate(result['results']):
            icon = "✅" if question_result['is_correct'] else "❌"
            status = "Richtig" if question_result['is_correct'] else "Falsch"
            
            with st.expander(f"Frage {i+1} - {icon} {status}"):
                st.markdown(f"**{question_result['question']}**")
                # Safe access to difficulty
                difficulty = question_result.get('difficulty', 1)
                st.write(f"**Schwierigkeit:** {'⭐' * difficulty}")
                st.write("")
                st.write(f"**Ihre Antwort:** {question_result['user_answer']}")
                
                if not question_result['is_correct']:
                    st.error(f"**Richtige Antwort:** {question_result['correct_answer']}")
                else:
                    st.success("**Richtig beantwortet!** ✅")
                
                if question_result['explanation']:
                    st.info(f"💡 **Erklärung:** {question_result['explanation']}")
                
                if question_result['tips']:
                    st.write("**📝 Tipps für die Zukunft:**")
                    for tip in question_result['tips']:
                        st.write(f"• {tip}")
