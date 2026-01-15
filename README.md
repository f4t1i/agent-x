# X Hyper-Agent v2.0 - The Resonance Machine 🚀

A powerful, intelligent 4-dimensional agent that automatically creates, posts, and optimizes content on X (formerly Twitter) using Claude 3.5 Sonnet and advanced AI techniques.

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. **Set up X API:** Follow [X_API_SETUP.md](X_API_SETUP.md) (requires Basic Tier $100/mo)
4. Set up your Claude API Key in `.env`
5. Test connection: `python test_x_api.py`
6. Run: `python agent.py`

## Documentation

- 🚀 **[X_API_SETUP.md](X_API_SETUP.md)** - Complete X API setup guide (START HERE!)
- 📖 **[HYPER_AGENT.md](HYPER_AGENT.md)** - Technical documentation & features
- 📋 **[CLAUDE.md](CLAUDE.md)** - Mission briefing & implementation log
- 🗺️ **[REPO_TOUR.md](REPO_TOUR.md)** - Repository walkthrough
- 🏗️ **[PRODUCTION_REFACTORING_PLAN.md](PRODUCTION_REFACTORING_PLAN.md)** - Modularization guide

## Features - The 4 Dimensions

### 🧠 Dimension 1: Cognitive Resonance
- ✅ URL Summarization with Opinion (newspaper3k + Claude)
- ✅ Thread Generator with Hook-Body-CTA architecture
- ✅ 3 Content Types: tech_news, tips_tricks, inspiration
- ✅ Personality Temperature (analytical vs creative)

### ⏰ Dimension 2: Temporal Flux
- ✅ Trendjacking (real-time trend monitoring)
- ✅ Smart Scheduling (engagement-based optimal timing)
- ✅ Historical analytics with pandas

### 💬 Dimension 3: Social Gravitation
- ✅ Auto-Reply to Mentions (friendly/defensive modes)
- ✅ Influencer Orbiting (5-min window for reach-stealing)
- ✅ Intelligent comment generation (no spam)

### 🧬 Dimension 4: Memory (Ψ - Coherence)
- ✅ RAG Memory (ChromaDB vector database)
- ✅ Anti-Repetition (semantic similarity checks)
- ✅ Feedback Loop (24h performance analysis)
- ✅ Self-Optimization (learns from engagement)

### 🛡️ Production-Ready
- 🔐 Secure credential management (.env)
- 📊 Comprehensive metrics & JSON logging
- 🛡️ Rate limit handling
- ⚡ 1177 lines of production code

## Requirements

- Python 3.9+
- Claude API Key (~$10-20/month)
- **X API Basic Tier ($100/month)** - Free tier does NOT allow posting!
- ChromaDB for vector memory
- 17 specialized classes across 4 dimensions

## License

MIT
