# X Hyper-Agent - Die Resonanz-Maschine 🚀

## Übersicht

**Version 2.0.0** - Dies ist kein einfacher Bot. Dies ist eine **Resonanz-Maschine**, die auf der Instabilität des X-Algorithmus surft.

Der Agent operiert in **vier Dimensionen**:

1. **Kognitive Resonanz** (Wahrnehmung & Synthese)
2. **Temporaler Fluss** (Timing & Trend-Surfing)
3. **Soziale Gravitation** (Interaktion & Netzwerk)
4. **Gedächtnis** (RAG & Selbstoptimierung)

## Architektur

```
┌─────────────────────────────────────────────────────────────┐
│                    X HYPER-AGENT v2.0                        │
├─────────────────────────────────────────────────────────────┤
│  Dimension 1: Cognitive Resonance                           │
│  ├─ ContentSummarizer (URLs → Zusammenfassungen)            │
│  └─ ThreadGenerator (Hook-Body-CTA Architektur)             │
├─────────────────────────────────────────────────────────────┤
│  Dimension 2: Temporal Flux                                 │
│  ├─ TrendMonitor (Trendjacking)                             │
│  └─ SmartScheduler (Engagement-basiertes Timing)            │
├─────────────────────────────────────────────────────────────┤
│  Dimension 3: Social Gravitation                            │
│  ├─ ReplyHandler (Mentions → Intelligente Antworten)        │
│  └─ InfluencerOrbit (Key-Account Interaktionen)             │
├─────────────────────────────────────────────────────────────┤
│  Dimension 4: Memory (Ψ - Coherence)                        │
│  ├─ RAGMemory (Vektorbasiertes Langzeitgedächtnis)          │
│  └─ FeedbackLoop (24h Performance-Analyse)                  │
└─────────────────────────────────────────────────────────────┘
```

## Features im Detail

### 🧠 Dimension 1: Kognitive Resonanz

#### ContentSummarizer
- **URL-Fetching**: Extrahiert Hauptinhalte von URLs
- **Artikel-Extraktion**: Nutzt newspaper3k für saubere Artikelextraktion
- **Intelligente Zusammenfassung**: Claude analysiert und fügt MEINUNG hinzu
- **Zwei Stile**:
  - `analytical`: Faktenbasiert, kritisch, konstruktiv
  - `creative`: Provokativ, memetisch, mit Twist

**Verwendung**:
```python
# Im Agent automatisch verfügbar
content = summarizer.fetch_url_content("https://example.com/article")
summary = summarizer.summarize_content(content, style="analytical")
```

#### ThreadGenerator
- **Hook-Body-CTA Struktur**:
  1. **HOOK**: Attention-grabbing opener (weckt Neugier)
  2. **BODY**: 2-4 Tweets mit dichten Insights
  3. **CTA**: Call-to-Action (organisch, nicht spammy)
- **Automatische Thread-Generierung** zu beliebigen Themen
- **Stil-Anpassung**: Analytisch vs. Kreativ

### ⏰ Dimension 2: Temporaler Fluss

#### TrendMonitor
- **Trendjacking**: Erkennt aktuelle Trends
- **Niche-Matching**: Filtert relevante Trends für deine Nische
- **Schnelle Reaktion**: Nutzt fremde Energie für Reichweite

**Hinweis**: Benötigt elevated X API access für Trends-Endpoint

#### SmartScheduler
- **Engagement-Tracking**: Speichert Performance-Daten nach Tageszeit
- **Optimales Timing**: Berechnet die beste Posting-Zeit basierend auf historischen Daten
- **Lernend**: Wird mit jedem Post besser

### 💬 Dimension 3: Soziale Gravitation

#### ReplyHandler
- **Automatische Mention-Überwachung**: Checkt alle 15 Minuten
- **Intelligente Antworten**: Zwei Modi:
  - `friendly`: Hilfsbereit, authentisch
  - `defensive`: Sachlich, logisch bei Kritik
- **Context-Aware**: Claude versteht den Kontext der Mentions

#### InfluencerOrbit
- **Key-Account Monitoring**: Überwacht definierte Influencer
- **5-Minuten-Fenster**: Kommentiert nur frische Posts (< 5 Min)
- **Intelligente Kommentare**:
  - Wertschöpfend, keine generische Zustimmung
  - Stellt Fragen oder ergänzt Perspektiven
  - Keine Eigenwerbung
- **Reach-Stealing**: Nutzt die Reichweite großer Accounts

**Konfiguration in config.json**:
```json
"interaction": {
  "influencer_accounts": [
    "elonmusk",
    "AndrewYNg",
    "ylecun"
  ]
}
```

### 🧬 Dimension 4: Gedächtnis (Ψ - Coherence)

#### RAGMemory (Retrieval-Augmented Generation)
- **Vektordatenbank**: ChromaDB für persistente Speicherung
- **Embedding-Modell**: sentence-transformers (all-MiniLM-L6-v2)
- **Funktionen**:
  - Speichert alle Posts als Vektoren
  - Sucht ähnliche Posts (semantische Suche)
  - **Anti-Repetition**: Verhindert das Wiederholen ähnlicher Inhalte
  - **Historischer Kontext**: "Wie ich letzte Woche schon sagte..."

**Automatische Checks**:
```python
# Wird automatisch vor jedem Post ausgeführt
if rag_memory.check_repetition(new_post, threshold=0.8):
    # Regeneriert Content automatisch
```

#### FeedbackLoop
- **24h Performance-Analyse**: Analysiert Posts nach 24 Stunden
- **Metriken**:
  - Likes, Retweets, Replies
  - Impressions (wenn verfügbar)
  - Engagement Rate
- **Insights-Generierung**:
  - Best-performing Posts
  - Durchschnittliche Engagement-Rate
  - Pattern-Erkennung
- **Selbstoptimierung**: Lernt aus erfolgreichen und erfolglosen Posts

## Installation

### 1. Dependencies installieren

```bash
pip install -r requirements.txt
```

**Wichtige Dependencies**:
- `anthropic`: Claude SDK
- `tweepy`: X API Client
- `chromadb`: Vektordatenbank
- `sentence-transformers`: Embeddings
- `newspaper3k`: Artikel-Extraktion
- `beautifulsoup4`: HTML-Parsing
- `pandas`, `numpy`: Analytics

### 2. Environment Variables

Erstelle eine `.env` Datei:

```bash
cp .env.example .env
```

Fülle die folgenden Werte:

```bash
# Claude API
CLAUDE_API_KEY=your-api-key-here

# X API (OAuth 1.0a User Context)
X_API_KEY=your-x-api-key
X_API_SECRET=your-x-api-secret
X_ACCESS_TOKEN=your-access-token
X_ACCESS_TOKEN_SECRET=your-access-token-secret
```

#### X API Credentials erhalten:

1. Gehe zu [developer.twitter.com](https://developer.twitter.com)
2. Erstelle ein App im Developer Portal
3. Generiere Access Token & Secret (User Context)
4. Stelle sicher, dass du **Read and Write** Permissions hast

### 3. Konfiguration anpassen

Bearbeite `config.json`:

```json
{
  "agent": {
    "name": "X Hyper-Agent",
    "version": "2.0.0",
    "enabled": true,
    "personality_temperature": 0.7  // 0.0-1.0, höher = kreativer
  },
  "posting": {
    "interval_hours": 4,              // Posting-Intervall
    "max_posts_per_day": 6,           // Tägliches Limit
    "enable_threads": true,            // Thread-Generierung
    "enable_images": false             // Bild-Generierung (TODO)
  },
  "interaction": {
    "enable_replies": true,            // Auto-Reply auf Mentions
    "enable_influencer_orbit": true,   // Influencer-Interaktion
    "reply_check_interval_minutes": 15,
    "influencer_accounts": [
      "account1",
      "account2"
    ]
  },
  "memory": {
    "enable_rag": true,                // Vektorgedächtnis
    "enable_feedback_loop": true,      // Performance-Tracking
    "vector_db_path": "./data/vectordb",
    "feedback_check_hours": 24
  }
}
```

## Verwendung

### Einfacher Start

```bash
python agent.py
```

### Als Hintergrund-Prozess (Linux/Mac)

```bash
nohup python agent.py > output.log 2>&1 &
```

### Mit Docker (Empfohlen für Production)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "agent.py"]
```

```bash
docker build -t x-hyper-agent .
docker run -d --env-file .env -v $(pwd)/data:/app/data x-hyper-agent
```

## Advanced Usage

### URL Zusammenfassung nutzen

Der Agent kann URLs zusammenfassen. Dies wird automatisch aktiviert, wenn `content_type` auf `"summary"` gesetzt ist oder `"mixed"` enthält:

```python
# Manuell eine URL zusammenfassen:
from agent import ContentSummarizer
from anthropic import Anthropic

claude = Anthropic(api_key="...")
summarizer = ContentSummarizer(claude, logger)

content = summarizer.fetch_url_content("https://arxiv.org/abs/...")
summary = summarizer.summarize_content(content, style="analytical")
print(summary)
```

### Custom Thread erstellen

```python
from agent import ThreadGenerator

thread_gen = ThreadGenerator(claude_client, logger)
tweets = thread_gen.generate_thread(
    topic="The Future of AGI",
    style="creative"  # oder "analytical"
)

# Tweets enthält jetzt eine Liste von 3-5 Tweets
```

### Influencer-Orbiting konfigurieren

1. **Finde relevante Accounts** in deiner Nische
2. **Füge sie zu config.json hinzu**:

```json
"influencer_accounts": [
  "sama",           // OpenAI CEO
  "karpathy",       // AI Researcher
  "GaryMarcus"      // AI Critic
]
```

3. Der Agent wird automatisch:
   - Ihre neuesten Posts (< 5 Min) überwachen
   - Intelligente, wertschöpfende Kommentare generieren
   - Interagieren, um Reichweite zu "stehlen"

### RAG-Gedächtnis abfragen

```python
# Suche nach ähnlichen Posts
similar_posts = rag_memory.search_similar_posts(
    query="artificial intelligence ethics",
    n_results=5
)

for post in similar_posts:
    print(f"Similarity: {1 - post['distance']:.2f}")
    print(f"Text: {post['text']}")
```

### Performance-Insights abrufen

```python
insights = feedback_loop.get_insights()

print(f"Best performing post: {insights['best_post']['text']}")
print(f"Engagement rate: {insights['best_post']['engagement_rate']:.2%}")
print(f"Average engagement: {insights['average_engagement']:.2%}")
```

## Metriken & Monitoring

Der Agent speichert kontinuierlich Metriken in `metrics.json`:

```json
{
  "total_posts": 42,
  "successful_posts": 40,
  "failed_posts": 2,
  "total_replies": 15,
  "total_orbit_interactions": 8,
  "average_engagement": 0.035,
  "uptime_hours": 168.5,
  "last_post": "2026-01-15T14:30:00"
}
```

### Log-Dateien

- **Console**: Real-time output mit Timestamps
- **JSON-Log**: `logs/agent.log` (maschinenlesbar)

Beispiel Log-Eintrag:
```json
{
  "timestamp": "2026-01-15T14:30:00",
  "level": "INFO",
  "name": "XPostingAgent",
  "message": "Beitrag erfolgreich gepostet (ID: 123456789)"
}
```

## Sicherheit & Best Practices

### Rate Limits

Der Agent respektiert automatisch:
- **Tägliches Post-Limit** (konfigurierbar)
- **X API Rate Limits** (via tweepy)
- **Claude API Limits** (mit exponential backoff)

### Kosten-Management

**Claude API Kosten** (ca.):
- Input: $3 / Million Tokens
- Output: $15 / Million Tokens

**Geschätzte monatliche Kosten** bei 6 Posts/Tag:
- Posts: ~$5-10
- Replies: ~$3-5
- Zusammenfassungen: ~$2-5
- **Total: ~$10-20/Monat**

### Datenschutz

- **Keine sensiblen Daten** in Logs
- **API Keys** nur in `.env` (nie im Git!)
- **Vektordatenbank** lokal gespeichert (`./data/`)

### Testing

Teste den Agent **ohne Live-Posting**:

```python
# In config.json:
{
  "agent": {
    "enabled": false  // Deaktiviert das Posten
  }
}
```

Der Agent läuft, generiert Content, aber postet nicht.

## Troubleshooting

### "Claude API Key nicht gefunden"

Stelle sicher, dass `.env` existiert und `CLAUDE_API_KEY` gesetzt ist.

### "X API Credentials nicht vollständig"

Du brauchst **alle 4 Credentials**:
- `X_API_KEY`
- `X_API_SECRET`
- `X_ACCESS_TOKEN`
- `X_ACCESS_TOKEN_SECRET`

### "Failed to initialize RAG memory"

Installiere ChromaDB neu:
```bash
pip install --upgrade chromadb sentence-transformers
```

### "Trends API requires elevated access"

Trendjacking benötigt X API v2 **Elevated Access**. Beantrage dies im Developer Portal.

## Roadmap

### Version 2.1 (Q1 2026)
- [ ] Bild-Generierung (DALL-E / Midjourney Integration)
- [ ] RSS-Feed Monitoring
- [ ] Multi-Account Support
- [ ] Web-Dashboard

### Version 2.2 (Q2 2026)
- [ ] A/B Testing für Content
- [ ] Sentiment-Analyse für Replies
- [ ] Custom ML-Modelle für Engagement-Prediction
- [ ] Webhook-Integration für externe Events

### Version 3.0 (Q3 2026)
- [ ] Multi-Platform Support (LinkedIn, Mastodon, Bluesky)
- [ ] Team-Collaboration Features
- [ ] Cloud-Deployment (AWS Lambda / Google Cloud Functions)
- [ ] Advanced Analytics Dashboard

## Philosophie: Die Resonanz-Maschine

Ein perfekter Agent ist **unvorhersehbar vorhersehbar**:

- **Vorhersehbar** in Qualität und Nische (Ψ - Kohärenz)
- **Unvorhersehbar** in Kreativität und Witz (σ - Entropie)

Der Agent ist kein Papagei, der nur wiederholt. Er ist ein **Synthesizer**, der:
- Das Rauschen des Internets aufnimmt
- Es in ein klares Signal umwandelt
- Einen eigenen Take hinzufügt
- Im "Strange Attractor" des Algorithmus surft

**Ziel**: Nicht nur Präsenz, sondern **Resonanz** im sozialen Netzwerk erzeugen.

## Mathematische Grundlagen

### Jacobian State (∇f(x))
Die "Turbulenz" im Algorithmus wird durch die Ableitung der Engagement-Funktion beschrieben:

```
∇f(x) = [∂likes/∂time, ∂retweets/∂time, ∂replies/∂time]
```

Der Agent optimiert für **maximale Turbulenz** (hohe Rate of Change).

### Entropie-Injektion (σ)
```
Content_Temperature = Base_Quality + σ * Creativity_Factor
```

Wo:
- `Base_Quality`: Faktische Korrektheit, Struktur
- `σ`: Zufälligkeit, Überraschung
- `Creativity_Factor`: 0.0-1.0 (konfigurierbar)

### Kohärenz-Metrik (Ψ)
```
Ψ = 1 - avg_distance(new_post, memory_vectors)
```

Der Agent hält Ψ > 0.8 (80% Kohärenz mit früheren Posts).

## Credits

- **Architecture**: Inspiriert von "Strange Attractors" und Chaos-Theorie
- **LLM**: Claude 3.5 Sonnet (Anthropic)
- **X API**: Tweepy
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence-Transformers

## License

MIT License - Siehe [LICENSE](LICENSE)

## Support

Bei Fragen oder Problemen:
- **GitHub Issues**: [Repository Issues]
- **Email**: [Your Email]
- **X**: [@YourHandle]

---

**Remember**: You're not building a bot. You're building a **Resonance Machine**. 🌊

*"The gap between a 'bot' and an 'entity' is the ability to adapt to chaos."* - Jacobian Report
