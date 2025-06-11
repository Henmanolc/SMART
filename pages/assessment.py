import streamlit as st
import os
import random
from datetime import datetime
from utils.data_persistence import auto_save_assessment

def render_assessment_page(question_loader):
    """Render the assessment page with setup, questions, and results screens."""
    st.header("📝 Assessment Center")
    
    # Check if questions directory exists
    if not os.path.exists("questions"):
        st.error("Fragen-Ordner 'questions' nicht gefunden. Bitte erstellen Sie den Ordner und fügen Sie Fragen-Dateien hinzu.")
        st.info("Erstellen Sie den Ordner 'questions' und fügen Sie Markdown-Dateien mit Fragen hinzu.")
        st.stop()
    
    # Load available modules from question files
    available_modules = question_loader.get_available_modules()
    
    if not available_modules:
        st.warning("Keine Fragen-Module gefunden. Bitte überprüfen Sie den 'questions' Ordner und fügen Sie Markdown-Dateien hinzu.")
        st.info("""
        **So erstellen Sie Fragen-Module:**
        1. Erstellen Sie eine .md Datei im 'questions' Ordner
        2. Verwenden Sie das vorgegebene Markdown-Format
        3. Beispiel: `Grundeinrichtung_System.md`
        """)
        st.stop()
    
    # Determine which screen to show
    assessment_screen = "setup"  # Default to setup
    
    if 'current_assessment' in st.session_state:
        assessment_screen = "questions"
    elif 'last_assessment_result' in st.session_state:
        assessment_screen = "results"
    
    # === SETUP SCREEN ===
    if assessment_screen == "setup":
                       
        # Module selection with padding
        col1, col2, col3 = st.columns([2, 0.2, 1])
        
        with col1:
            subject = st.selectbox(
                "📚 Wähle das Modul:",
                available_modules,
                help="Wähle das Modul aus, das Du testen möchtest"
            )
        
        with col2:
            # Empty column for padding
            st.write("")
        
        with col3:
            difficulty = st.slider(
                "🎯 Maximaler Schwierigkeitsgrad", 
                1, 5, 3,
                help="Fragen bis zu diesem Schwierigkeitsgrad werden einbezogen"
            )
        
        # Load questions for selected module
        module_data = question_loader.load_module_questions(subject)
        available_questions = module_data.get('questions', [])
        
        if not available_questions:
            st.error(f"❌ Keine Fragen für Modul '{subject}' gefunden.")
            st.info("Überprüfen Sie die Markdown-Datei auf korrekte Formatierung.")
            st.stop()
        
        # Filter questions by difficulty
        filtered_questions = question_loader.filter_questions_by_difficulty(
            available_questions, 1, difficulty
        )
        
        if not filtered_questions:
            st.error(f"❌ Keine Fragen für Schwierigkeitsgrad 1-{difficulty} gefunden.")
            st.stop()
        
        # Assessment preview
        st.markdown("### 📋 Assessment-Übersicht")
        
        col1, col2, col3, col4, col5 = st.columns([1, 0.2, 1, 0.2, 1])
        
        with col1:
            st.info(f"**Verfügbare Fragen**\n{len(available_questions)}")
        
        with col3:
            num_questions = min(20, len(filtered_questions))
            st.info(f"**Fragen im Test**\n{num_questions}")
        
        with col5:
            est_time = f"{num_questions * 1.5:.0f} Min"
            st.info(f"**Geschätzte Dauer**\n{est_time}")
        
        # Show difficulty distribution
        if filtered_questions:
            st.markdown("### 📊 Schwierigkeitsverteilung")
            diff_counts = {}
            for q in filtered_questions:
                diff = q.get('difficulty', 1)
                diff_counts[diff] = diff_counts.get(diff, 0) + 1
            
            diff_cols = st.columns(5)
            for i, level in enumerate(range(1, 6)):
                with diff_cols[i]:
                    count = diff_counts.get(level, 0)
                    if count > 0:
                        st.metric(f"⭐ {level}", count)
                    else:
                        st.metric(f"⭐ {level}", "0", delta=None)
        
        # Warnings and info
        if len(filtered_questions) < 20:
            st.warning(f"⚠️ Nur {len(filtered_questions)} Fragen für den gewählten Schwierigkeitsgrad verfügbar. Es werden alle verfügbaren Fragen verwendet.")
        
        st.markdown("---")
        
        # Start button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Assessment starten", type="primary", use_container_width=True, key="start_assessment"):
                num_questions = min(20, len(filtered_questions))
                selected_questions = random.sample(filtered_questions, num_questions)
                st.session_state.current_assessment = {
                    'questions': selected_questions,
                    'current_question': 0,
                    'answers': {},
                    'start_time': datetime.now(),
                    'subject': subject,
                    'difficulty': difficulty
                }
                # Clear any previous results
                if 'last_assessment_result' in st.session_state:
                    del st.session_state.last_assessment_result
                st.rerun()
    
    # === QUESTIONS SCREEN ===
    elif assessment_screen == "questions":
        assessment = st.session_state.current_assessment
        current_q_idx = assessment['current_question']
        total_questions = len(assessment['questions'])
        
        if current_q_idx < total_questions:
            question = assessment['questions'][current_q_idx]
            
            # Header with progress
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.metric("Frage", f"{current_q_idx + 1}/{total_questions}")
            with col2:
                progress = (current_q_idx + 1) / total_questions
                st.progress(progress, text=f"Fortschritt: {progress:.0%}")
            with col3:
                elapsed = datetime.now() - assessment['start_time']
                st.metric("Zeit", str(elapsed).split('.')[0])
            
            st.markdown("---")
            
            # Question content
            st.markdown(f"## Frage {current_q_idx + 1}")
            
            # Difficulty and question
            difficulty_stars = "⭐" * question.get('difficulty', 1)
            st.markdown(f"**Schwierigkeit:** {difficulty_stars}")
            st.write("")
            
            # Question text in a highlighted box
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;">
            <h4 style="margin-top: 0;">{question['question']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            
            # Answer options
            user_answer = st.radio(
                "**Wählen Sie eine Antwort:**",
                question['options'],
                key=f"q_{current_q_idx}_{question.get('id', 0)}"
            )
            
            st.markdown("---")
            
            # Navigation buttons
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if current_q_idx > 0:
                    if st.button("⬅️ Zurück", use_container_width=True, type="secondary"):
                        assessment['current_question'] -= 1
                        st.rerun()
            
            with col2:
                is_last_question = current_q_idx >= total_questions - 1
                button_text = "🏁 Assessment beenden" if is_last_question else "➡️ Nächste Frage"
                
                if st.button(button_text, type="primary", use_container_width=True):
                    assessment['answers'][current_q_idx] = user_answer
                    
                    if not is_last_question:
                        assessment['current_question'] += 1
                        st.rerun()
                    else:
                        # Calculate final results and store them
                        correct_answers = 0
                        total_questions = len(assessment['answers'])
                        results = []
                        
                        for i, answer in assessment['answers'].items():
                            question_obj = assessment['questions'][i]
                            is_correct = answer.split(')')[0].strip() == question_obj['correct']
                            if is_correct:
                                correct_answers += 1
                            
                            results.append({
                                'question': question_obj['question'],
                                'user_answer': answer,
                                'correct_answer': question_obj['correct'],
                                'is_correct': is_correct,
                                'explanation': question_obj.get('explanation', ''),
                                'tips': question_obj.get('tips', []),
                                'difficulty': question_obj.get('difficulty', 1)
                            })
                        
                        score = (correct_answers / total_questions) * 100
                        duration = datetime.now() - assessment['start_time']
                        
                        # Store results
                        assessment_result = {
                            'subject': assessment['subject'],
                            'difficulty': assessment['difficulty'],
                            'score': score,
                            'correct_answers': correct_answers,
                            'total_questions': total_questions,
                            'duration': duration,
                            'date': datetime.now(),
                            'results': results
                        }
                        
                        # Save assessment BEFORE setting session state
                        auto_save_assessment(assessment_result)
                        
                        # Now set session state and navigate
                        st.session_state.last_assessment_result = assessment_result
                        
                        # Clean up current assessment
                        del st.session_state.current_assessment
                        st.rerun()

            with col3:
                if st.button("❌ Abbrechen", use_container_width=True, type="secondary"):
                    del st.session_state.current_assessment
                    st.rerun()

    # === RESULTS SCREEN ===
    elif assessment_screen == "results":
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
        <h1 style="color: {result_color}; margin: 0;">{result_emoji} Assessment abgeschlossen!</h1>
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
            if st.button("📊 Detaillierte Auswertung", use_container_width=True, type="secondary"):
                st.session_state.show_detailed_results = not st.session_state.get('show_detailed_results', False)
                st.rerun()
        
        with col3:
            if st.button("📈 Fortschritt anzeigen", use_container_width=True, type="secondary"):
                # Clear current results and navigate to progress page
                del st.session_state.last_assessment_result
                if 'show_detailed_results' in st.session_state:
                    del st.session_state.show_detailed_results
                # This will cause the page to rerun and show the main navigation
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