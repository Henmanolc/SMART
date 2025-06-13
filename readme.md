# SMART: Sides Mastery Assessment & Review Tool

Ein interaktives Schulungssystem für Restaurant- und Kassensystem-Administration mit Fokus auf Sides-POS-Systeme.

## 🚀 Features

### 📚 Assessment System
- **Modulare Fragen**: 10+ verschiedene Themenbereiche (Grundeinrichtung, Artikelkonfiguration, Zahlungsoptionen, etc.)
- **Schwierigkeitsgrade**: Anpassbare Schwierigkeitsstufen (1-5 Sterne)
- **Intelligente Fragenselektion**: Automatische Auswahl von bis zu 20 Fragen pro Assessment
- **Echtzeitfeedback**: Sofortige Bewertung mit detaillierter Analyse
- **Tipps-System**: Kollabierbare Hilfestellungen während der Assessments
- **Detaillierte Ergebnisse**: Frage-für-Frage Auswertung mit Erklärungen und Tipps

### 👤 Benutzerverwaltung
- **Passwort-basierte Authentifizierung**: Sichere Anmeldung mit Name und Passwort
- **Account-Erstellung**: Registrierung mit Name, E-Mail und Passwort (mit Bestätigung)
- **Multi-User-Support**: Mehrere Benutzer können das System nutzen
- **Cloud-Datenspeicherung**: Supabase Backend für persistente Daten
- **Session-Management**: Automatische Abmeldung und sichere Sitzungsverwaltung
- **Passwort-Sicherheit**: Mindestlänge von 4 Zeichen erforderlich

### 📊 Datenmanagement
- **Supabase Backend**: Cloud-basierte PostgreSQL-Datenbank
- **Hybrid-Ansatz**: Automatischer Fallback auf lokale CSV-Dateien
- **Automatische Backups**: Daten werden nach jedem Assessment gespeichert
- **Export-Funktion**: CSV-Export der Assessment-Daten
- **Skalierbar**: Unterstützt unbegrenzte Benutzer und Assessments

### 🛠️ Technische Struktur

```
smart.py                 # Hauptanwendung und Navigation
├── pages/
│   ├── assessment.py    # Assessment-Durchführung
│   ├── progress.py      # Fortschrittsverfolgung
│   └── settings.py      # Benutzereinstellungen
├── utils/
│   ├── data_persistence.py  # Hybrid-Datenspeicherung
│   ├── user_management.py   # Benutzerverwaltung
│   ├── supabase_backend.py  # Supabase-Integration
│   └── questionLoader.py    # Fragen-Management
```

### 📊 Datenarchitektur

**Cloud-First mit Fallback:**
- **Primär**: Supabase (PostgreSQL) für Produktionsumgebung
- **Fallback**: Lokale CSV-Dateien für Entwicklung/Offline-Betrieb

```
Supabase Tables:
├── users (id, name, email, password, user_id, created_at)
└── assessments (id, user_id, date, subject, difficulty, score, etc.)

Local Fallback:
├── data/users.csv
└── data/user_data_{user_id}.csv
```

## 📝 Installation & Setup

### Voraussetzungen
```bash
pip install -r requirements.txt
```

**Dependencies:**
- `streamlit>=1.28.0`
- `pandas>=1.5.0`
- `supabase>=1.0.0,<2.0.0`

### Supabase Setup
1. **Erstelle Supabase Projekt** auf [supabase.com](https://supabase.com)
2. **Erstelle Tabellen:**
   ```sql
   -- Users table
   CREATE TABLE users (
     id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
     name text NOT NULL,
     email text UNIQUE NOT NULL,
     password text NOT NULL,
     user_id text UNIQUE NOT NULL,
     created_at timestamptz DEFAULT now()
   );
   
   -- Assessments table
   CREATE TABLE assessments (
     id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
     user_id text NOT NULL,
     date timestamptz NOT NULL,
     subject text NOT NULL,
     difficulty int4 NOT NULL,
     score float8 NOT NULL,
     correct_answers int4 NOT NULL,
     total_questions int4 NOT NULL,
     duration_seconds float8 NOT NULL,
     created_at timestamptz DEFAULT now()
   );
   ```
3. **Deaktiviere RLS** für beide Tabellen (oder erstelle entsprechende Policies)

### Lokale Entwicklung
Erstelle `.streamlit/secrets.toml`:
```toml
[supabase]
url = "https://your-project.supabase.co"
anon_key = "your-anon-key"
```

### Produktionsdeployment
Füge in Streamlit Cloud Secrets hinzu:
```toml
[supabase]
url = "https://your-project.supabase.co"
anon_key = "your-anon-key"
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

### Für Lernende
1. **Account erstellen**: Name, E-Mail und Passwort eingeben
2. **Anmelden**: Mit persönlichen Zugangsdaten
3. **Assessment starten**: Modul und Schwierigkeitsgrad wählen
4. **Tipps nutzen**: Bei schwierigen Fragen Hilfestellungen einblenden
5. **Fortschritt verfolgen**: Persönliche Statistiken einsehen
6. **Daten exportieren**: CSV-Export für eigene Auswertungen

### Für Administratoren
1. **Fragen verwalten**: Markdown-Dateien im `questions/` Ordner
2. **Supabase Dashboard**: Direkter Zugriff auf Benutzerdaten
3. **System-Monitoring**: Logs in Streamlit Cloud

## 🔧 Sicherheit & Datenschutz

### Entwicklungsversion
- **Passwörter**: Unverschlüsselt gespeichert (für einfache Administration)
- **Zugriff**: Direkter Datenbankzugriff über Supabase Dashboard
- **Backup**: Automatischer Fallback auf lokale Dateien

### Produktionsempfehlungen
- [ ] Passwort-Hashing implementieren (bcrypt)
- [ ] Rate-Limiting für Login-Versuche
- [ ] Audit-Logging für kritische Aktionen
- [ ] HTTPS-Only Deployment

## 🌐 Deployment

### Streamlit Cloud
1. **Repository**: Pushe Code zu GitHub
2. **App erstellen**: Auf [share.streamlit.io](https://share.streamlit.io)
3. **Secrets konfigurieren**: Supabase-Credentials hinzufügen
4. **Domain**: Automatische .streamlit.app URL

### Skalierung
- **Benutzer**: Unbegrenzt (Supabase Free Tier: 500MB)
- **Assessments**: Unbegrenzt (abhängig von Speicherplatz)
- **Concurrent Users**: Bis zu 1000 (Streamlit Cloud Limit)

## 📊 Datenformat

### Supabase Schema
```sql
-- Beispiel-Daten
users:
  id: uuid
  name: "Max Mustermann"
  email: "max@example.com"
  password: "securepass123"
  user_id: "user_0001"
  created_at: "2025-01-15T10:00:00Z"

assessments:
  id: uuid
  user_id: "user_0001"
  date: "2025-01-15T10:30:00Z"
  subject: "Artikelkonfiguration"
  difficulty: 3
  score: 85.0
  correct_answers: 17
  total_questions: 20
  duration_seconds: 300.5
```

## 🚀 Performance

### Optimierungen
- **Supabase**: Globales CDN für schnelle Datenbankzugriffe
- **Streamlit Caching**: Question Loader wird gecacht
- **Hybrid Storage**: Lokaler Fallback verhindert Ausfälle
- **Lazy Loading**: Daten werden nur bei Bedarf geladen

### Monitoring
- **Streamlit Cloud**: Automatisches Performance-Monitoring
- **Supabase**: Built-in Database-Metriken
- **Error Tracking**: Detaillierte Fehlermeldungen

---

*SMART v2.0 - Cloud-Native Training Platform - Entwickelt für Sides System-Training*
