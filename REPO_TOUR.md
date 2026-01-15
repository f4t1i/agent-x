# Agent - X Posting Automation mit Claude Code

## 🎯 Projekt-Übersicht

Dieses Repository enthält einen intelligenten Agent, der automatisiert Beiträge auf X (ehemals Twitter) postet. Der Agent nutzt **Claude Code** und das **Claude SDK** zur intelligenten Beitragsgenerierung und Automatisierung.

---

## 📋 Inhaltsverzeichnis

1. [Einführung](#einführung)
2. [Anforderungen](#anforderungen)
3. [Installation](#installation)
4. [Claude SDK Setup](#claude-sdk-setup)
5. [Konfiguration](#konfiguration)
6. [Verwendung](#verwendung)
7. [Agent-Funktionalität](#agent-funktionalität)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Einführung

Der **Agent** ist eine Python-basierte Anwendung, die:

- ✅ Automatisch Beiträge auf X postet
- ✅ Claude Code zur intelligenten Beitragsgenerierung nutzt
- ✅ Das Claude SDK für API-Kommunikation verwendet
- ✅ Zeitgesteuerte Posting-Zyklen unterstützt
- ✅ Beitrags-Historie und Metriken verwaltet

### Warum Claude Code und Claude SDK?

**Claude Code** ermöglicht es dem Agent, komplexe Aufgaben zu verstehen und zu automatisieren, während das **Claude SDK** die nahtlose Integration mit der Claude API ermöglicht.

---

## 📦 Anforderungen

Bevor du den Agent einrichtest, stelle sicher, dass folgende Anforderungen erfüllt sind:

### System-Anforderungen
- Python 3.9 oder höher
- pip (Python Package Manager)
- Git
- Eine aktive Internetverbindung

### Externe Anforderungen
- **Claude API Key** (von Anthropic)
- **X API Credentials** (API Key, API Secret, Access Token, Access Token Secret)
- Ein X Developer Account

---

## 🔧 Installation

### Schritt 1: Repository klonen

```bash
git clone https://github.com/yourusername/Agent.git
cd Agent
```

### Schritt 2: Virtuelle Umgebung erstellen

```bash
python3 -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate
```

### Schritt 3: Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

---

## 🤖 Claude SDK Setup

### Schritt 1: Claude SDK herunterladen

Das Claude SDK wird automatisch mit den Abhängigkeiten installiert. Falls du es manuell installieren möchtest:

```bash
pip install anthropic
```

### Schritt 2: Claude API Key konfigurieren

Dein Claude API Key muss in den Umgebungsvariablen gespeichert werden:

```bash
export CLAUDE_API_KEY="your-api-key-here"
```

Oder erstelle eine `.env` Datei im Projektverzeichnis:

```env
CLAUDE_API_KEY=your-api-key-here
X_API_KEY=your-x-api-key
X_API_SECRET=your-x-api-secret
X_ACCESS_TOKEN=your-access-token
X_ACCESS_TOKEN_SECRET=your-access-token-secret
```

### Schritt 3: Claude Code aktivieren

Der Agent nutzt Claude Code automatisch für die Beitragsgenerierung. Stelle sicher, dass dein API Key die erforderlichen Berechtigungen hat.

---

## ⚙️ Konfiguration

### `config.json` - Agent-Konfiguration

Erstelle eine `config.json` Datei im Projektverzeichnis:

```json
{
  "agent": {
    "name": "X Posting Agent",
    "version": "1.0.0",
    "enabled": true
  },
  "posting": {
    "interval_hours": 4,
    "posts_per_cycle": 1,
    "max_posts_per_day": 6,
    "content_type": "mixed"
  },
  "claude": {
    "model": "claude-3-5-sonnet",
    "temperature": 0.7,
    "max_tokens": 280,
    "use_code_interpreter": true
  },
  "x_api": {
    "api_version": "2",
    "rate_limit_handling": "queue"
  },
  "logging": {
    "level": "INFO",
    "file": "logs/agent.log"
  }
}
```

### Posting-Kategorien

Der Agent kann verschiedene Arten von Beiträgen generieren:

- **Tech News**: Technologie-Updates und Trends
- **Tips & Tricks**: Praktische Tipps für Entwickler
- **Inspiration**: Motivierende Zitate und Gedanken
- **Mixed**: Zufällige Auswahl aus allen Kategorien

---

## 💻 Verwendung

### Agent starten

```bash
python agent.py
```

### Agent im Hintergrund ausführen (Linux/Mac)

```bash
nohup python agent.py > agent.log 2>&1 &
```

### Agent als Systemdienst (Linux)

Erstelle `/etc/systemd/system/x-agent.service`:

```ini
[Unit]
Description=X Posting Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/Agent
ExecStart=/path/to/Agent/venv/bin/python agent.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Dann aktivieren:

```bash
sudo systemctl enable x-agent
sudo systemctl start x-agent
```

---

## 🤖 Agent-Funktionalität

### Wie der Agent funktioniert

```
┌─────────────────────────────────────────┐
│   Agent Startup                         │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Claude SDK initialisieren             │
│   (API Key laden)                       │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Warte auf Posting-Intervall           │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Claude Code aufrufen                  │
│   (Beitrag generieren)                  │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Beitrag validieren                    │
│   (Länge, Inhalt, Hashtags)             │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   X API aufrufen                        │
│   (Beitrag posten)                      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Erfolg protokollieren                 │
│   (Metriken speichern)                  │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Zurück zu Schritt 3                   │
└─────────────────────────────────────────┘
```

### Claude Code Integration

Der Agent nutzt Claude Code für:

- **Intelligente Beitragsgenerierung**: Erstellt relevante, ansprechende Inhalte
- **Hashtag-Optimierung**: Generiert relevante Hashtags basierend auf Inhalten
- **Sentiment-Analyse**: Stellt sicher, dass Beiträge positiv und engagierend sind
- **Trend-Analyse**: Berücksichtigt aktuelle Trends bei der Beitragserstellung

### Claude SDK Methoden

```python
from anthropic import Anthropic

client = Anthropic()

# Beitrag generieren
response = client.messages.create(
    model="claude-3-5-sonnet",
    max_tokens=280,
    messages=[
        {
            "role": "user",
            "content": "Generiere einen ansprechenden X-Beitrag über KI-Trends"
        }
    ]
)

post_content = response.content[0].text
```

---

## 📊 Monitoring und Logs

### Log-Dateien

Der Agent speichert Logs in `logs/agent.log`:

```
[2024-01-15 10:30:45] INFO: Agent gestartet
[2024-01-15 10:30:46] INFO: Claude SDK initialisiert
[2024-01-15 10:35:12] INFO: Beitrag generiert: "Künstliche Intelligenz..."
[2024-01-15 10:35:15] INFO: Beitrag erfolgreich gepostet (ID: 1234567890)
[2024-01-15 10:35:16] INFO: Nächstes Posting in 4 Stunden
```

### Metriken

Der Agent verwaltet Metriken in `metrics.json`:

```json
{
  "total_posts": 42,
  "successful_posts": 40,
  "failed_posts": 2,
  "average_engagement": 125,
  "uptime_hours": 336,
  "last_post": "2024-01-15T10:35:15Z"
}
```

---

## 🔐 Sicherheit

### Best Practices

1. **Niemals API Keys in Code hardcoden** - Nutze Umgebungsvariablen oder `.env` Dateien
2. **`.env` Datei in `.gitignore` hinzufügen**:
   ```
   .env
   .env.local
   venv/
   logs/
   ```

3. **API Keys regelmäßig rotieren**
4. **Logs regelmäßig überprüfen** auf verdächtige Aktivitäten
5. **Rate Limits beachten** - X API hat Limitierungen

---

## 🐛 Troubleshooting

### Problem: "Claude API Key nicht gefunden"

**Lösung**: Stelle sicher, dass die Umgebungsvariable korrekt gesetzt ist:

```bash
echo $CLAUDE_API_KEY
```

### Problem: "X API Authentifizierung fehlgeschlagen"

**Lösung**: Überprüfe deine X API Credentials in der `.env` Datei

### Problem: "Beitrag zu lang (>280 Zeichen)"

**Lösung**: Der Agent sollte dies automatisch handhaben, aber überprüfe die `max_tokens` Einstellung in `config.json`

### Problem: "Rate Limit überschritten"

**Lösung**: Erhöhe das `interval_hours` in der Konfiguration

---

## 📚 Weitere Ressourcen

- [Claude API Dokumentation](https://docs.anthropic.com)
- [Claude SDK GitHub](https://github.com/anthropics/anthropic-sdk-python)
- [X API Dokumentation](https://developer.twitter.com/en/docs)
- [Python Anthropic SDK](https://pypi.org/project/anthropic/)

---

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe `LICENSE` für Details.

---

## 🤝 Beitragen

Beiträge sind willkommen! Bitte erstelle einen Pull Request mit deinen Verbesserungen.

---

## 📞 Support

Bei Fragen oder Problemen, erstelle bitte ein GitHub Issue.

---

**Viel Erfolg mit deinem Agent! 🚀**
