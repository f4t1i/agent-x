# Production Refactoring Plan

## Übersicht

Dieser Plan beschreibt, wie die aktuelle Single-File Implementation (`agent.py` - 1177 Zeilen) in eine modulare Production-Struktur umgewandelt werden kann.

**Status:** OPTIONAL - Die aktuelle Single-File Lösung funktioniert perfekt für den Use Case.

**Wann refactoren?**
- Bei Erweiterung auf 2000+ Zeilen
- Bei Team-Entwicklung (mehrere Entwickler)
- Bei Cloud-Deployment mit Microservices
- Bei Unit-Testing Anforderungen

---

## Ziel-Struktur

```
agent-x/
├── agent.py                    # Main entry point (100 Zeilen)
├── config.json
├── requirements.txt
├── .env.example
│
├── core/
│   ├── __init__.py
│   └── agent.py               # XPostingAgent Hauptklasse (200 Zeilen)
│
├── modules/
│   ├── __init__.py
│   ├── cognitive.py           # Dimension 1: ContentSummarizer, ThreadGenerator
│   ├── temporal.py            # Dimension 2: TrendMonitor, SmartScheduler
│   ├── social.py              # Dimension 3: ReplyHandler, InfluencerOrbit
│   └── memory.py              # Dimension 4: RAGMemory, FeedbackLoop
│
├── config/
│   ├── __init__.py
│   └── models.py              # Alle Pydantic Models
│
├── utils/
│   ├── __init__.py
│   ├── logging.py             # Logging Setup
│   └── helpers.py             # Helper-Funktionen
│
├── data/                      # Runtime data (gitignored)
│   ├── vectordb/
│   ├── engagement_history.json
│   └── performance_data.json
│
├── logs/                      # Logs (gitignored)
│   └── agent.log
│
├── tests/                     # Unit Tests
│   ├── __init__.py
│   ├── test_cognitive.py
│   ├── test_temporal.py
│   ├── test_social.py
│   └── test_memory.py
│
└── docs/
    ├── CLAUDE.md
    ├── HYPER_AGENT.md
    ├── README.md
    └── REPO_TOUR.md
```

---

## Schritt-für-Schritt Refactoring

### Phase 1: Vorbereitung (15 Min)

**1.1 Ordnerstruktur erstellen**
```bash
mkdir -p core modules config utils tests docs
touch core/__init__.py modules/__init__.py config/__init__.py utils/__init__.py tests/__init__.py
```

**1.2 Dokumentation verschieben**
```bash
mv CLAUDE.md HYPER_AGENT.md REPO_TOUR.md README.md docs/
```

**1.3 .gitignore erweitern**
```bash
# Zu .gitignore hinzufügen:
data/
logs/
*.pyc
__pycache__/
.pytest_cache/
*.egg-info/
```

---

### Phase 2: Config Models auslagern (20 Min)

**Datei: `config/models.py`**

Verschiebe alle Pydantic Models:
- `AgentConfig`
- `PostingConfig`
- `ClaudeConfig`
- `InteractionConfig`
- `MemoryConfig`
- `LoggingConfig`
- `Config`
- `Metrics`

```python
# config/models.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AgentConfig(BaseModel):
    """Agent configuration model."""
    name: str = "X Hyper-Agent"
    version: str = "2.0.0"
    enabled: bool = True
    personality_temperature: float = 0.7

# ... alle anderen Models
```

**Import in agent.py ändern:**
```python
from config.models import Config, Metrics, AgentConfig, PostingConfig, ClaudeConfig
```

---

### Phase 3: Dimension 1 - Cognitive Resonance (30 Min)

**Datei: `modules/cognitive.py`**

```python
"""
Dimension 1: Cognitive Resonance
- ContentSummarizer
- ThreadGenerator
"""

import logging
import re
from typing import Optional, List
import requests
from anthropic import Anthropic
from bs4 import BeautifulSoup
from newspaper import Article


class ContentSummarizer:
    """Summarizes URLs, articles, and threads using Claude."""

    def __init__(self, claude_client: Anthropic, logger: logging.Logger):
        self.claude_client = claude_client
        self.logger = logger

    # ... rest of implementation (Zeilen 129-207 aus agent.py)


class ThreadGenerator:
    """Generates threads with Hook-Body-CTA architecture."""

    def __init__(self, claude_client: Anthropic, logger: logging.Logger):
        self.claude_client = claude_client
        self.logger = logger

    # ... rest of implementation (Zeilen 210-262 aus agent.py)
```

**Import:**
```python
from modules.cognitive import ContentSummarizer, ThreadGenerator
```

---

### Phase 4: Dimension 2 - Temporal Flux (30 Min)

**Datei: `modules/temporal.py`**

```python
"""
Dimension 2: Temporal Flux
- TrendMonitor
- SmartScheduler
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
import tweepy


class TrendMonitor:
    """Monitors X trends and enables trendjacking."""

    def __init__(self, x_client: tweepy.Client, logger: logging.Logger):
        self.x_client = x_client
        self.logger = logger

    # ... rest of implementation (Zeilen 269-299 aus agent.py)


class SmartScheduler:
    """Analyzes engagement data and optimizes posting times."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.engagement_history: List[Dict[str, Any]] = []
        self.load_history()

    # ... rest of implementation (Zeilen 302-355 aus agent.py)
```

**Import:**
```python
from modules.temporal import TrendMonitor, SmartScheduler
```

---

### Phase 5: Dimension 3 - Social Gravitation (30 Min)

**Datei: `modules/social.py`**

```python
"""
Dimension 3: Social Gravitation
- ReplyHandler
- InfluencerOrbit
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import tweepy
from anthropic import Anthropic


class ReplyHandler:
    """Handles replies to mentions and comments."""

    def __init__(self, x_client: tweepy.Client, claude_client: Anthropic, logger: logging.Logger):
        self.x_client = x_client
        self.claude_client = claude_client
        self.logger = logger
        self.last_mention_id: Optional[str] = None

    # ... rest of implementation (Zeilen 362-441 aus agent.py)


class InfluencerOrbit:
    """Monitors and interacts with key influencers in your niche."""

    def __init__(self, x_client: tweepy.Client, claude_client: Anthropic, logger: logging.Logger):
        self.x_client = x_client
        self.claude_client = claude_client
        self.logger = logger

    # ... rest of implementation (Zeilen 444-543 aus agent.py)
```

**Import:**
```python
from modules.social import ReplyHandler, InfluencerOrbit
```

---

### Phase 6: Dimension 4 - Memory (30 Min)

**Datei: `modules/memory.py`**

```python
"""
Dimension 4: Memory (Ψ - Coherence)
- RAGMemory
- FeedbackLoop
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
import tweepy
import chromadb
from sentence_transformers import SentenceTransformer


class RAGMemory:
    """Vector-based long-term memory using ChromaDB."""

    def __init__(self, db_path: str, logger: logging.Logger):
        self.logger = logger
        self.db_path = db_path
        self.client = None
        self.collection = None
        self.embedder = None
        self.initialize()

    # ... rest of implementation (Zeilen 550-631 aus agent.py)


class FeedbackLoop:
    """Analyzes post performance and optimizes strategy."""

    def __init__(self, x_client: tweepy.Client, logger: logging.Logger):
        self.x_client = x_client
        self.logger = logger
        self.performance_data: List[Dict[str, Any]] = []
        self.load_performance_data()

    # ... rest of implementation (Zeilen 634-734 aus agent.py)
```

**Import:**
```python
from modules.memory import RAGMemory, FeedbackLoop
```

---

### Phase 7: Utils auslagern (20 Min)

**Datei: `utils/logging.py`**

```python
"""Logging utilities."""

import logging
from pathlib import Path
from pythonjsonlogger import jsonlogger


def setup_logging(log_file: str, log_level: str) -> logging.Logger:
    """Set up logging configuration."""
    logger = logging.getLogger("XPostingAgent")
    logger.setLevel(getattr(logging, log_level))

    # Create logs directory
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # File handler with JSON formatting
    file_handler = logging.FileHandler(log_file)
    file_formatter = jsonlogger.JsonFormatter(
        "%(timestamp)s %(level)s %(name)s %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
```

**Import:**
```python
from utils.logging import setup_logging
```

---

### Phase 8: Core Agent Klasse (30 Min)

**Datei: `core/agent.py`**

```python
"""
Core Agent Class - Orchestrates all 4 dimensions.
"""

import json
import logging
import os
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

import schedule
import tweepy
from anthropic import Anthropic

from config.models import Config, Metrics
from modules.cognitive import ContentSummarizer, ThreadGenerator
from modules.temporal import TrendMonitor, SmartScheduler
from modules.social import ReplyHandler, InfluencerOrbit
from modules.memory import RAGMemory, FeedbackLoop
from utils.logging import setup_logging


class XPostingAgent:
    """Hyper-Intelligent X Posting Agent - The Resonance Machine."""

    CONTENT_PROMPTS = {
        "tech_news": "Generiere einen kurzen, informativen X-Beitrag...",
        "tips_tricks": "Generiere einen hilfreichen X-Beitrag...",
        "inspiration": "Generiere einen motivierenden X-Beitrag...",
        "summary": "Fasse einen Artikel zusammen...",
    }

    def __init__(self, config_path: str = "config.json"):
        """Initialize the X Posting Agent."""
        self.config = self._load_config(config_path)
        self.metrics = self._load_metrics()
        self.logger = setup_logging(
            self.config.logging.file,
            self.config.logging.level
        )

        # Core clients
        self.claude_client: Optional[Anthropic] = None
        self.x_client: Optional[tweepy.Client] = None

        # Advanced modules
        self.content_summarizer: Optional[ContentSummarizer] = None
        self.thread_generator: Optional[ThreadGenerator] = None
        self.trend_monitor: Optional[TrendMonitor] = None
        self.smart_scheduler: Optional[SmartScheduler] = None
        self.reply_handler: Optional[ReplyHandler] = None
        self.influencer_orbit: Optional[InfluencerOrbit] = None
        self.rag_memory: Optional[RAGMemory] = None
        self.feedback_loop: Optional[FeedbackLoop] = None

        # State
        self.start_time = datetime.now()
        self.posts_today = 0
        self.last_post_date: Optional[str] = None
        self.pending_posts: List[Dict[str, Any]] = []

    # ... alle Methoden aus agent.py (Zeilen 777-1167)

    def run(self) -> None:
        """Run the agent."""
        # ... Implementation
```

---

### Phase 9: Main Entry Point (10 Min)

**Datei: `agent.py` (NEU - nur 20 Zeilen!)**

```python
#!/usr/bin/env python3
"""
X Hyper-Agent - Main Entry Point
The Resonance Machine
"""

from core.agent import XPostingAgent


def main():
    """Main entry point."""
    agent = XPostingAgent()
    agent.run()


if __name__ == "__main__":
    main()
```

---

### Phase 10: Unit Tests (Optional, 60 Min)

**Datei: `tests/test_cognitive.py`**

```python
"""Tests for Dimension 1: Cognitive Resonance."""

import pytest
from unittest.mock import Mock, patch
from modules.cognitive import ContentSummarizer, ThreadGenerator


class TestContentSummarizer:
    """Test ContentSummarizer class."""

    def test_fetch_url_content(self):
        """Test URL fetching."""
        claude_client = Mock()
        logger = Mock()
        summarizer = ContentSummarizer(claude_client, logger)

        # Mock the Article class
        with patch('modules.cognitive.Article') as mock_article:
            mock_article.return_value.title = "Test Title"
            mock_article.return_value.text = "Test content"

            content = summarizer.fetch_url_content("https://example.com")

            assert "Test Title" in content
            assert "Test content" in content

    def test_summarize_content_analytical(self):
        """Test analytical summarization."""
        # Implementation
        pass


class TestThreadGenerator:
    """Test ThreadGenerator class."""

    def test_generate_thread(self):
        """Test thread generation."""
        # Implementation
        pass
```

**Ähnlich für:**
- `tests/test_temporal.py`
- `tests/test_social.py`
- `tests/test_memory.py`

**Test ausführen:**
```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=modules
```

---

## Migration-Script

**Datei: `scripts/migrate_to_modules.py`**

```python
#!/usr/bin/env python3
"""
Migration script to refactor agent.py into modules.
"""

import os
import shutil
from pathlib import Path


def create_structure():
    """Create folder structure."""
    folders = [
        'core',
        'modules',
        'config',
        'utils',
        'tests',
        'docs',
        'data',
        'logs'
    ]

    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
        init_file = Path(folder) / '__init__.py'
        if folder not in ['data', 'logs', 'docs']:
            init_file.touch()

    print("✅ Folder structure created")


def move_docs():
    """Move documentation files."""
    docs = ['CLAUDE.md', 'HYPER_AGENT.md', 'REPO_TOUR.md', 'README.md']

    for doc in docs:
        if Path(doc).exists():
            shutil.move(doc, f'docs/{doc}')

    print("✅ Documentation moved to docs/")


def backup_original():
    """Backup original agent.py."""
    if Path('agent.py').exists():
        shutil.copy('agent.py', 'agent.py.backup')
        print("✅ agent.py backed up to agent.py.backup")


if __name__ == "__main__":
    print("🚀 Starting migration...")
    create_structure()
    move_docs()
    backup_original()
    print("✅ Migration preparation complete!")
    print("\nNext steps:")
    print("1. Manually extract classes to respective module files")
    print("2. Update imports in core/agent.py")
    print("3. Create new agent.py entry point")
    print("4. Test with: python agent.py")
```

**Ausführen:**
```bash
python scripts/migrate_to_modules.py
```

---

## Vorteile der Modularen Struktur

### 1. **Wartbarkeit**
- Jede Datei hat klare Verantwortung
- Einfacher zu navigieren (200 Zeilen vs 1177)
- Schnellere Code-Reviews

### 2. **Testing**
- Unit Tests pro Modul möglich
- Mocking einfacher
- Test Coverage messbar

### 3. **Team-Entwicklung**
- Mehrere Entwickler können parallel arbeiten
- Weniger Merge-Konflikte
- Klare Code-Ownership

### 4. **Erweiterbarkeit**
- Neue Dimensions einfach hinzufügen
- Plugin-Architektur möglich
- A/B Testing für einzelne Module

### 5. **Cloud-Deployment**
- Module als separate Lambda Functions
- Microservices-Architektur
- Horizontal skalierbar

---

## Rollback-Plan

Falls Probleme auftreten:

```bash
# 1. Original wiederherstellen
mv agent.py.backup agent.py

# 2. Module löschen
rm -rf core/ modules/ config/ utils/ tests/

# 3. Docs zurück
mv docs/* .
rmdir docs/
```

---

## Zeitaufwand

| Phase | Aufwand | Priorität |
|-------|---------|-----------|
| Phase 1-2: Setup + Config | 35 Min | Hoch |
| Phase 3-6: Module extrahieren | 120 Min | Hoch |
| Phase 7-8: Utils + Core | 50 Min | Mittel |
| Phase 9: Entry Point | 10 Min | Hoch |
| Phase 10: Tests | 60 Min | Niedrig (Optional) |
| **GESAMT** | **4-5 Stunden** | |

---

## Empfehlung

**JETZT:** Behalte die Single-File Lösung bei ✅
- Funktioniert perfekt
- Einfach zu deployen
- Kein Overhead

**REFACTOR WENN:**
- Code > 2000 Zeilen
- Team > 1 Person
- Unit Tests benötigt
- Microservices gewünscht

---

## Checkliste für Refactoring

- [ ] Backup erstellen (`agent.py.backup`)
- [ ] Ordnerstruktur anlegen
- [ ] Config Models auslagern (`config/models.py`)
- [ ] Module extrahieren (cognitive, temporal, social, memory)
- [ ] Utils auslagern (`utils/logging.py`)
- [ ] Core Agent anpassen (`core/agent.py`)
- [ ] Neuen Entry Point erstellen (`agent.py`)
- [ ] Alle Imports aktualisieren
- [ ] Tests schreiben (optional)
- [ ] Funktionstests durchführen
- [ ] Dokumentation aktualisieren
- [ ] Git commit & push

---

**Status:** PLAN BEREIT - Implementation bei Bedarf durchführen

**Erstellt:** 2026-01-15
**Version:** 1.0.0
