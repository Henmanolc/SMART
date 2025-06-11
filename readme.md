# SMART: Sides Mastery Assessment & Review Tool

Ein interaktives Schulungssystem für Restaurant- und Kassensystem-Administration mit Fokus auf Sides-POS-Systeme.

## 🚀 Features

### 📚 Assessment System
- **Modulare Fragen**: 10+ verschiedene Themenbereiche (Grundeinrichtung, Artikelkonfiguration, Zahlungsoptionen, etc.)
- **Schwierigkeitsgrade**: Anpassbare Schwierigkeitsstufen (1-5 Sterne)
- **Intelligente Fragenselektion**: Automatische Auswahl von bis zu 20 Fragen pro Assessment
  - **Maximum 20 Fragen**: Assessments sind auf maximal 20 Fragen begrenzt
  - **Zufällige Auswahl**: Bei mehr als 20 verfügbaren Fragen wird eine zufällige Stichprobe gezogen
  - **Schwierigkeitsfilter**: Nur Fragen innerhalb des gewählten Schwierigkeitsbereichs werden berücksichtigt
  - **Wiederholbarkeit**: Jeder Assessment-Durchlauf kann unterschiedliche Fragen enthalten
- **Echtzeitfeedback**: Sofortige Bewertung mit detaillierter Analyse
- **Detaillierte Ergebnisse**: Frage-für-Frage Auswertung mit Erklärungen und Tipps

### 👤 Benutzerverwaltung
- **Einfache Registrierung**: Nur Name und E-Mail erforderlich
- **Multi-User-Support**: Mehrere Benutzer können das System nutzen
- **Persistente Daten**: Fortschritt wird automatisch gespeichert
- **Geräteübergreifend**: Zugriff von jedem Computer durch Benutzerauswahl

### 🏆 Gamification & Progress Tracking
- **Achievement-System**: 13 verschiedene Errungenschaften
  - Grundlagen: Erstes Assessment, Assessment-Serie, Assessment-Veteran, Assessment-König
  - Leistung: Perfektionist, Konsistenz-Champion, Flawless Victory
  - Vielfalt: Multi-Talent, Wissensdurst, Master-Student
  - Geschwindigkeit: Blitzschnell
  - Aktivität: Learning Streak, Wochenkrieger
- **Fortschrittsanzeige**: Visuelle Progress-Bars für verschiedene Ziele
- **Statistiken**: Durchschnittsergebnisse, absolvierte Tests, Modulabdeckung

### 📊 Datenmanagement
- **CSV-basierte Speicherung**: Keine Datenbank erforderlich
- **Automatische Backups**: Daten werden nach jedem Assessment gespeichert
- **Export-Funktion**: CSV-Export der Assessment-Daten
- **Datentrennung**: Separate Dateien für jeden Benutzer

## 🛠️ Technische Struktur

### Hauptkomponenten
```
smart.py                 # Hauptanwendung und Navigation
├── pages/
│   ├── assessment.py    # Assessment-Durchführung
│   ├── progress.py      # Fortschrittsverfolgung
│   └── settings.py      # Benutzereinstellungen
├── utils/
│   ├── data_persistence.py  # Datenspeicherung
│   ├── user_management.py   # Benutzerverwaltung
│   └── questionLoader.py    # Fragen-Management
```

### Datenstruktur
```
data/
├── users.csv                    # Benutzerregister
└── user_data_{user_id}.csv      # Individuelle Assessment-Daten
```

### Frontend
- **Streamlit**: Moderne Web-UI
- **Responsive Design**: Optimiert für verschiedene Bildschirmgrößen
- **Custom CSS**: Professionelles Styling
- **Intuitive Navigation**: Sidebar-Navigation mit Dropdown

## 📝 Installation & Setup

### Voraussetzungen
```bash
# Mit requirements.txt (empfohlen)
pip install -r requirements.txt

# Oder manuell
pip install streamlit pandas
```

### Verzeichnisstruktur erstellen
```
SMART/
├── smart.py
├── requirements.txt     # Python-Dependencies
├── pages/
├── utils/
├── assets/
│   ├── styles.css
│   └── sides_bw.png
├── questions/           # Fragen-Markdown-Dateien
└── data/               # Wird automatisch erstellt
```

### Starten
```bash
streamlit run smart.py
```

## 📖 Fragen-Format

Fragen werden als Markdown-Dateien im `questions/` Ordner gespeichert:

```markdown
# Modulname

## Metadata
- Category: Kategoriename
- Author: Autorname
- Version: 1.0

## Question 1
**Difficulty:** 2
**Question:** Wie konfiguriert man...?
**Options:**
- A) Option 1
- B) Option 2  
- C) Option 3
- D) Option 4
**Correct:** A
**Explanation:** Detaillierte Erklärung...
**Tips:**
- Tipp 1
- Tipp 2
```

## 🎯 Verwendung

### Für Product Manager
Als Product Manager spielen wir eine entscheidende Rolle bei der Pflege und Erweiterung des SMART-Systems:

#### 📝 Fragenpool-Management
- **Neue Features**: Bei der Entwicklung neuer Features sollten entsprechende Fragen erstellt werden
- **Feature-Updates**: Bestehende Fragen aktualisieren, wenn sich Funktionalitäten ändern
- **Wissensabfrage**: Fragen zu kritischen Features erstellen, die das Team beherrschen sollte
- **Best Practices**: Häufige Anwendungsfälle und Troubleshooting-Szenarien einarbeiten

#### 🔄 Wartungszyklen
- **Quarterly Reviews**: Vierteljährliche Überprüfung der Fragen auf Aktualität
- **Release-Updates**: Nach größeren Releases neue Fragen hinzufügen
- **Feedback Integration**: Erkenntnisse aus Support-Tickets in Fragen umwandeln
- **Team-Input**: Feedback von Kollegen zu schwierigen Themen sammeln

#### 📋 Fragen-Kategorien priorisieren
- **Kritische Features**: Kernfunktionalitäten mit hoher Priorität
- **Neue Features**: Aktuelle Entwicklungen zeitnah integrieren
- **Edge Cases**: Seltene aber wichtige Anwendungsfälle abdecken
- **Integration Points**: Schnittstellen und Abhängigkeiten zwischen Systemen

### Für Administratoren
1. **Fragen erstellen**: Markdown-Dateien im `questions/` Ordner
2. **Benutzer verwalten**: Über die Sidebar-Benutzerauswahl
3. **Fortschritt überwachen**: Export-Funktion in den Einstellungen

### Für Lernende
1. **Anmelden**: Name und E-Mail in der Sidebar eingeben
2. **Assessment starten**: Modul und Schwierigkeit wählen
   - **Modulauswahl**: Gewünschtes Themengebiet auswählen
   - **Schwierigkeitsgrad**: Maximale Schwierigkeitsstufe festlegen (1-5 Sterne)
   - **Fragenauswahl**: System wählt automatisch bis zu 20 zufällige Fragen aus dem gefilterten Pool
3. **Fortschritt verfolgen**: Progress Tracking Seite besuchen (enthält Review-Funktionalität)
4. **Achievements sammeln**: Verschiedene Ziele erreichen

## 🔧 Konfiguration

### Einstellungen
- **Schwierigkeitsgrad**: Standard-Schwierigkeitsstufe
- **Benachrichtigungen**: E-Mail-Erinnerungen (geplant)
- **Auto-Save**: Automatisches Speichern des Fortschritts
- **Erklärungen**: Zeige Erklärungen nach Antworten

### Anpassungen
- **Styling**: `assets/styles.css` bearbeiten
- **Logo**: `assets/sides_bw.png` ersetzen
- **Module**: Neue Markdown-Dateien im `questions/` Ordner

## 🌐 Deployment

### Web-Hosting
Das System ist web-hosting-ready:
- Keine Datenbank erforderlich
- CSV-basierte Datenspeicherung
- Streamlit Cloud kompatibel

### Sicherheit
- Keine Passwörter erforderlich
- Einfache Benutzeridentifikation über Name/E-Mail
- Lokale Datenspeicherung

## 📊 Datenformat

### Assessment-Daten
```csv
date,subject,difficulty,score,correct_answers,total_questions,duration_seconds
2025-01-11T10:30:00,Artikelkonfiguration,3,85.0,17,20,300.5
```

### Benutzer-Daten
```csv
name,email,created_date,user_id
Max Mustermann,max@example.com,2025-01-11T09:00:00,user_0001
```

## 🎨 UI-Features

### Responsive Design
- **Sidebar-Navigation**: Kompakte Benutzerführung
- **Progress-Bars**: Visuelle Fortschrittsanzeige
- **Achievement-Badges**: Gamification-Elemente
- **Metriken**: Übersichtliche Statistiken

### Accessibility
- **Emoji-Icons**: Intuitive Symbolik
- **Klare Struktur**: Logische Informationsarchitektur
- **Feedback-System**: Sofortige Rückmeldungen

## 🔄 Roadmap

### Geplante Features
- [ ] E-Mail-Benachrichtigungen
- [ ] Erweiterte Statistiken
- [ ] Team-Funktionen
- [ ] Mobile App
- [ ] API-Integration

### Bekannte Limitationen
- Einfache Benutzerauthentifizierung
- CSV-basierte Speicherung (skalierbar bis ~1000 Benutzer)
- Keine Echtzeitaktualisierung zwischen Benutzern

## 📞 Support

Bei Fragen oder Problemen:
1. README.md durchlesen
2. Code-Kommentare prüfen
3. Issues auf GitHub erstellen

---

*SMART v1.0 - Entwickelt für Sides ystem-Training*