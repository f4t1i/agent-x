# X (Twitter) API Einrichtung - Vollständige Anleitung

## Übersicht

Dieser Guide führt dich durch die komplette Einrichtung der X API für den Hyper-Agent.

**Zeitaufwand:** 15-20 Minuten
**Kosten:** Free Tier verfügbar (sehr limitiert), empfohlen: Basic Tier $100/Monat

---

## Schritt 1: Developer Account erstellen

### 1.1 Account beantragen

1. **Gehe zu:** https://developer.x.com (ehemals developer.twitter.com)
2. **Login:** Melde dich mit deinem X-Account an
3. **Apply for Access:** Klicke auf "Sign up for Free Account"

### 1.2 Formular ausfüllen

Du musst folgende Informationen angeben:

**Verwendungszweck:**
```
I'm building an AI-powered social media automation agent for personal/business use.
The agent will:
- Post original content about [deine Nische, z.B. "AI and Technology"]
- Reply to mentions automatically
- Analyze engagement metrics
- Interact with influencer posts

Estimated monthly tweets: ~200-500 (6 posts/day + replies)
```

**Wichtig:**
- ✅ Sei ehrlich über den Verwendungszweck
- ✅ Erwähne, dass es für persönlichen/Business-Account ist
- ❌ Schreibe NICHT über Spam oder Bots
- ❌ Erwähne keine Massen-Automatisierung

### 1.3 Bestätigung abwarten

- X prüft deinen Antrag (meist **innerhalb von 24 Stunden**)
- Du erhältst eine Email mit Bestätigung
- Bei Ablehnung: Antrag mit mehr Details neu stellen

---

## Schritt 2: App erstellen

### 2.1 Neues Projekt & App anlegen

1. **Im Developer Portal:** https://developer.x.com/en/portal/dashboard
2. **Create Project:**
   - Name: `X Hyper-Agent`
   - Use case: `Making a bot`
   - Description: `AI-powered content creation and engagement automation`

3. **Create App:**
   - App name: `hyper-agent-prod` (muss unique sein!)
   - Environment: `Production`

### 2.2 API Keys generieren

Nach der App-Erstellung erhältst du **sofort**:

```
✅ API Key (Consumer Key):        xyz123...
✅ API Secret (Consumer Secret):  abc456...
✅ Bearer Token:                  AAAAAAA...
```

**⚠️ WICHTIG:** Speichere diese sofort! Sie werden **nur einmal** angezeigt!

### 2.3 Access Token & Secret generieren

1. Gehe zu: **App Settings** → **Keys and Tokens**
2. Unter **Authentication Tokens:**
   - Klicke auf **"Generate"** bei **Access Token and Secret**

Du erhältst:

```
✅ Access Token:        1234567890-xyz...
✅ Access Token Secret: abcdef123...
```

**Alle 4 Credentials notieren:**
```bash
API_KEY=xyz123...
API_SECRET=abc456...
ACCESS_TOKEN=1234567890-xyz...
ACCESS_TOKEN_SECRET=abcdef123...
```

---

## Schritt 3: Permissions konfigurieren

### 3.1 App Permissions setzen

1. **Im Developer Portal:** App Settings → User authentication settings
2. **Set up** klicken
3. **App permissions** wählen:
   - ✅ **Read and Write** (ERFORDERLICH für Posting!)
   - ❌ NICHT nur "Read" (sonst kann der Agent nicht posten)

4. **Type of App:**
   - ✅ **Native App** (oder Web App)

5. **App info:**
   - Callback URL: `http://localhost:3000/callback` (falls OAuth 2.0)
   - Website URL: Deine Website oder `https://example.com`

6. **Save** klicken

### 3.2 Tokens regenerieren (WICHTIG!)

**Nach dem Ändern der Permissions:**

⚠️ **Du MUSST Access Token & Secret neu generieren!**

1. Gehe zu **Keys and Tokens**
2. **Regenerate** bei Access Token and Secret
3. Neue Tokens kopieren und speichern

**Warum?** Alte Tokens haben noch die alten Permissions!

---

## Schritt 4: API Tier wählen

### API Tiers Übersicht (Stand 2026)

| Feature | Free Tier | Basic ($100/mo) | Pro ($5,000/mo) |
|---------|-----------|-----------------|-----------------|
| **Tweets lesen** | 1.500/Monat | 10.000/Monat | 1 Mio/Monat |
| **Tweets posten** | ❌ 0 | 3.000/Monat | 300.000/Monat |
| **App Limit** | 1 App | 2 Apps | 5 Apps |
| **Elevated Access** | ❌ | ✅ | ✅ |
| **Trends API** | ❌ | ❌ | ✅ |

### Empfehlung für den Hyper-Agent:

**Minimum:** **Basic Tier ($100/Monat)**

**Warum?**
- ✅ **3.000 Posts/Monat** = 100 Posts/Tag (ausreichend für 6 Posts/Tag)
- ✅ **Elevated Access** für bessere Rate Limits
- ✅ **Read and Write** Permissions
- ❌ Free Tier erlaubt **KEIN Posting** (nur Lesen!)

**Berechnung:**
```
6 Posts/Tag × 30 Tage = 180 Posts/Monat
+ ~50 Replies/Monat
+ ~30 Influencer-Kommentare/Monat
= ~260 Posts/Monat ✅ Passt in Basic Tier
```

### Basic Tier beantragen:

1. **Developer Portal:** Billing → Subscribe to Basic
2. Kreditkarte hinterlegen
3. $100/Monat wird abgebucht

---

## Schritt 5: API Keys in den Agent einbinden

### 5.1 `.env` Datei erstellen

Im `agent-x` Repository:

```bash
cd agent-x
cp .env.example .env
nano .env  # oder vim, code, etc.
```

### 5.2 Credentials eintragen

```bash
# Claude API
CLAUDE_API_KEY=sk-ant-api03-...

# X API (OAuth 1.0a User Context)
X_API_KEY=xyz123...                     # Dein API Key
X_API_SECRET=abc456...                   # Dein API Secret
X_ACCESS_TOKEN=1234567890-xyz...        # Dein Access Token
X_ACCESS_TOKEN_SECRET=abcdef123...      # Dein Access Token Secret
```

### 5.3 Sicherheit überprüfen

**Stelle sicher:**

```bash
# .env darf NICHT in Git sein!
cat .gitignore | grep ".env"
# Sollte ausgeben: .env

# Permissions setzen (nur du kannst lesen)
chmod 600 .env
```

---

## Schritt 6: Verbindung testen

### 6.1 Test-Script ausführen

Erstelle `test_x_api.py`:

```python
#!/usr/bin/env python3
"""Test X API connection."""

import os
from dotenv import load_dotenv
import tweepy

load_dotenv()

# Load credentials
api_key = os.getenv("X_API_KEY")
api_secret = os.getenv("X_API_SECRET")
access_token = os.getenv("X_ACCESS_TOKEN")
access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

# Initialize client
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Test connection
try:
    me = client.get_me()
    print(f"✅ Connection successful!")
    print(f"📱 Authenticated as: @{me.data.username}")
    print(f"👤 Name: {me.data.name}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

**Ausführen:**

```bash
python test_x_api.py
```

**Erwartete Ausgabe:**

```
✅ Connection successful!
📱 Authenticated as: @your_username
👤 Name: Your Name
```

### 6.2 Posting-Test (Optional)

**⚠️ ACHTUNG:** Postet tatsächlich auf X!

```python
# Test posting
try:
    response = client.create_tweet(text="🤖 Testing my Hyper-Agent! #AI #Automation")
    print(f"✅ Tweet posted! ID: {response.data['id']}")
except Exception as e:
    print(f"❌ Posting failed: {e}")
```

---

## Häufige Probleme & Lösungen

### Problem 1: "403 Forbidden" beim Posten

**Ursache:** Permissions sind falsch oder Tokens nicht regeneriert

**Lösung:**
1. App Settings → User authentication settings
2. Stelle sicher: **Read and Write** ist aktiviert
3. **Regeneriere Access Token & Secret**
4. Trage neue Tokens in `.env` ein

---

### Problem 2: "429 Too Many Requests"

**Ursache:** Rate Limit überschritten

**Lösung:**
```python
# Prüfe dein Rate Limit:
rate_limit = client.get_rate_limit_status()
print(rate_limit)

# Reduziere Posts in config.json:
{
  "posting": {
    "max_posts_per_day": 3  # Statt 6
  }
}
```

---

### Problem 3: "401 Unauthorized"

**Ursache:** API Keys falsch oder abgelaufen

**Lösung:**
1. Überprüfe `.env` Datei auf Tippfehler
2. Stelle sicher, keine Leerzeichen vor/nach Keys
3. Regeneriere Keys im Developer Portal
4. Starte Agent neu

---

### Problem 4: "Read-Only Application"

**Ursache:** App hat nur Read-Permissions

**Lösung:**
1. App Settings → User authentication settings
2. Ändere zu **Read and Write**
3. **WICHTIG:** Regeneriere Access Token & Secret!
4. Neue Tokens in `.env` eintragen

---

## Kosten-Kalkulation

### Beispiel: Hyper-Agent mit Basic Tier

**Monatliche Kosten:**

| Service | Kosten |
|---------|--------|
| X API Basic Tier | $100/Monat |
| Claude API (6 Posts/Tag + Replies) | ~$15-20/Monat |
| **GESAMT** | **~$115-120/Monat** |

**API Call Breakdown (Monat):**

```
Content-Generierung:
- 180 Posts × 300 Tokens = 54.000 Tokens
- 50 Replies × 200 Tokens = 10.000 Tokens
- 30 Summaries × 500 Tokens = 15.000 Tokens
- 20 Threads × 800 Tokens = 16.000 Tokens
= 95.000 Tokens ≈ $0.30 Input + $1.50 Output = $1.80

X API Posts:
- 180 Posts
- 50 Replies
- 30 Influencer-Kommentare
= 260 API Calls (passt in Basic: 3.000/Monat)

GESAMT: ~$102-105/Monat
```

### Kosten sparen:

**Option 1:** Weniger Posts
```json
{
  "posting": {
    "max_posts_per_day": 3  // Statt 6
  }
}
```
→ Spart ~50% X API Calls, Claude API Kosten halbiert

**Option 2:** Selective Features
```json
{
  "interaction": {
    "enable_replies": false,           // Spart Replies
    "enable_influencer_orbit": false   // Spart Kommentare
  }
}
```

---

## OAuth Versionen Vergleich

### OAuth 1.0a (Empfohlen für Hyper-Agent)

**✅ Vorteile:**
- Einfacheres Setup (nur 4 Keys)
- Funktioniert mit `tweepy.Client` out-of-the-box
- Keine Redirect-URLs nötig
- Perfekt für Server-Side Apps

**❌ Nachteile:**
- Älterer Standard
- Weniger flexibel

### OAuth 2.0

**✅ Vorteile:**
- Moderner Standard
- Mehr Flexibilität
- Refresh Tokens

**❌ Nachteile:**
- Komplexeres Setup
- Benötigt Callback-URLs
- Mehr Code für Token-Management

**Für den Hyper-Agent:** **OAuth 1.0a** ist völlig ausreichend!

---

## Security Best Practices

### 1. API Keys schützen

```bash
# .env NIEMALS committen!
echo ".env" >> .gitignore

# Permissions setzen
chmod 600 .env

# Überprüfen
git status  # .env sollte NICHT erscheinen
```

### 2. Secrets Manager (Production)

Für Production-Deployment:

**AWS Secrets Manager:**
```python
import boto3

secret = boto3.client('secretsmanager').get_secret_value(
    SecretId='prod/agent-x/x-api-keys'
)
credentials = json.loads(secret['SecretString'])
```

**Google Cloud Secret Manager:**
```python
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
response = client.access_secret_version(
    name="projects/PROJECT_ID/secrets/x-api-keys/versions/latest"
)
credentials = json.loads(response.payload.data.decode('UTF-8'))
```

### 3. Key Rotation

**Regel:** Rotiere API Keys alle 90 Tage

```bash
# 1. Generiere neue Keys im Developer Portal
# 2. Update .env mit neuen Keys
# 3. Teste Verbindung
# 4. Lösche alte Keys im Portal
```

### 4. Rate Limit Monitoring

```python
# In agent.py hinzufügen:
def check_rate_limits(self):
    """Check remaining rate limits."""
    limits = self.x_client.get_rate_limit_status()
    remaining = limits['resources']['tweets']['/tweets']['remaining']

    if remaining < 10:
        self.logger.warning(f"Rate limit low: {remaining} remaining")
```

---

## Elevated Access beantragen (Optional)

### Was ist Elevated Access?

- Höhere Rate Limits
- Zugriff auf mehr API Endpoints
- Bessere Performance

### Wie beantragen?

1. **Developer Portal** → Products → Premium
2. **Apply for Elevated Access**
3. Begründung:
```
I'm building an AI-powered social media automation tool for personal use.
The agent needs elevated access for:
- Higher rate limits for posting and reading
- Access to trends API for trendjacking
- Better analytics capabilities

Estimated usage:
- 200-300 posts per month
- 500 read operations per day
- Analytics queries: 100/day
```

4. Warte auf Genehmigung (~2-3 Tage)

---

## Troubleshooting Checkliste

Wenn der Agent nicht funktioniert:

- [ ] Developer Account erstellt und bestätigt?
- [ ] App erstellt im Developer Portal?
- [ ] **Read and Write** Permissions gesetzt?
- [ ] Access Token & Secret **nach** Permission-Änderung regeneriert?
- [ ] Alle 4 Credentials in `.env` eingetragen?
- [ ] Keine Leerzeichen in `.env` Keys?
- [ ] `.env` Datei im richtigen Verzeichnis?
- [ ] `tweepy>=4.14.0` installiert? (`pip install -r requirements.txt`)
- [ ] Basic Tier abonniert? (Free Tier kann nicht posten!)
- [ ] Test-Script erfolgreich ausgeführt?

---

## Nächste Schritte

Nach erfolgreicher X API Einrichtung:

1. ✅ **Claude API einrichten** (siehe HYPER_AGENT.md)
2. ✅ **Agent starten:** `python agent.py`
3. ✅ **Ersten Post manuell testen**
4. ✅ **Logs überwachen:** `tail -f logs/agent.log`
5. ✅ **Metrics checken:** `cat metrics.json`

---

## Hilfreiche Links

- **Developer Portal:** https://developer.x.com/en/portal/dashboard
- **API Dokumentation:** https://developer.x.com/en/docs/twitter-api
- **Tweepy Docs:** https://docs.tweepy.org/
- **Rate Limits:** https://developer.x.com/en/docs/twitter-api/rate-limits
- **Pricing:** https://developer.x.com/en/products/twitter-api

---

## Support

Bei Problemen:

1. **X API Status:** https://api.twitterstat.us/
2. **Tweepy GitHub Issues:** https://github.com/tweepy/tweepy/issues
3. **Developer Forum:** https://twittercommunity.com/

---

**Erstellt:** 2026-01-15
**Version:** 1.0.0
**Status:** Production-Ready
