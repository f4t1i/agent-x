#!/usr/bin/env python3
"""
Agent - Hyper-Intelligent X Posting Agent with Resonance Engine

This agent is not a bot - it's a Resonance Machine.
It operates in four dimensions: Perception, Synthesis, Interaction, and Memory.

Architecture:
- Dimension 1: Cognitive Resonance (Content Generator + Thread Weaver)
- Dimension 2: Temporal Flux (Trendjacking + Smart Scheduling)
- Dimension 3: Social Gravitation (Interaction + Influencer Orbiting)
- Dimension 4: Memory (RAG + Self-Optimization)
"""

import json
import logging
import os
import random
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from urllib.parse import urlparse

import chromadb
import feedparser
import numpy as np
import pandas as pd
import requests
import schedule
import tweepy
from anthropic import Anthropic
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from newspaper import Article
from pydantic import BaseModel, Field
from pythonjsonlogger import jsonlogger
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()


# ============================================================================
# CONFIGURATION MODELS
# ============================================================================

class AgentConfig(BaseModel):
    """Agent configuration model."""
    name: str = "X Hyper-Agent"
    version: str = "2.0.0"
    enabled: bool = True
    personality_temperature: float = 0.7  # Low=Analytical, High=Creative


class PostingConfig(BaseModel):
    """Posting configuration model."""
    interval_hours: int = 4
    posts_per_cycle: int = 1
    max_posts_per_day: int = 6
    content_type: str = "mixed"
    enable_threads: bool = True
    enable_images: bool = False


class ClaudeConfig(BaseModel):
    """Claude configuration model."""
    model: str = "claude-3-5-sonnet-20241022"
    temperature: float = 0.7
    max_tokens: int = 4096
    use_code_interpreter: bool = True


class InteractionConfig(BaseModel):
    """Interaction configuration model."""
    enable_replies: bool = True
    enable_trendjacking: bool = True
    enable_influencer_orbit: bool = True
    reply_check_interval_minutes: int = 15
    influencer_accounts: List[str] = Field(default_factory=list)
    trendjacking_keywords: List[str] = Field(default_factory=list)


class MemoryConfig(BaseModel):
    """Memory configuration model."""
    enable_rag: bool = True
    enable_feedback_loop: bool = True
    vector_db_path: str = "./data/vectordb"
    feedback_check_hours: int = 24


class LoggingConfig(BaseModel):
    """Logging configuration model."""
    level: str = "INFO"
    file: str = "logs/agent.log"


class Config(BaseModel):
    """Main configuration model."""
    agent: AgentConfig = Field(default_factory=AgentConfig)
    posting: PostingConfig = Field(default_factory=PostingConfig)
    claude: ClaudeConfig = Field(default_factory=ClaudeConfig)
    interaction: InteractionConfig = Field(default_factory=InteractionConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


class Metrics(BaseModel):
    """Metrics tracking model."""
    total_posts: int = 0
    successful_posts: int = 0
    failed_posts: int = 0
    total_replies: int = 0
    total_trendjacks: int = 0
    total_orbit_interactions: int = 0
    average_engagement: float = 0.0
    best_performing_post: Optional[Dict[str, Any]] = None
    uptime_hours: float = 0.0
    last_post: Optional[str] = None


# ============================================================================
# DIMENSION 1: COGNITIVE RESONANCE
# ============================================================================

class ContentSummarizer:
    """Summarizes URLs, articles, and threads using Claude."""

    def __init__(self, claude_client: Anthropic, logger: logging.Logger):
        self.claude_client = claude_client
        self.logger = logger

    def fetch_url_content(self, url: str) -> Optional[str]:
        """Fetch and extract main content from URL."""
        try:
            # Use newspaper3k for article extraction
            article = Article(url)
            article.download()
            article.parse()

            content = f"Title: {article.title}\n\n{article.text}"
            self.logger.info(f"Fetched content from {url} ({len(content)} chars)")
            return content

        except Exception as e:
            self.logger.error(f"Failed to fetch URL {url}: {e}")
            # Fallback to simple requests
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.content, 'lxml')

                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()

                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)

                return text[:5000]  # Limit to 5000 chars

            except Exception as e2:
                self.logger.error(f"Fallback fetch also failed: {e2}")
                return None

    def summarize_content(self, content: str, style: str = "analytical") -> Optional[str]:
        """Summarize content with Claude and add opinion."""
        if not content:
            return None

        # Adjust prompt based on style
        if style == "analytical":
            prompt = f"""Analysiere und fasse den folgenden Inhalt zusammen.
            Extrahiere die wichtigsten Insights und füge DEINE MEINUNG hinzu (kritisch, aber konstruktiv).
            Format: 2-3 prägnante Sätze, die für einen X-Post geeignet sind (max 250 Zeichen).

            Inhalt:
            {content[:3000]}
            """
        else:  # creative/provocative
            prompt = f"""Lies den folgenden Inhalt und erstelle einen provokanten, memetischen Take darauf.
            Sei witzig, scharf, aber intelligent. Füge einen unerwarteten Twist hinzu.
            Format: 2-3 Sätze für X (max 250 Zeichen).

            Inhalt:
            {content[:3000]}
            """

        try:
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                temperature=0.8 if style != "analytical" else 0.6,
                messages=[{"role": "user", "content": prompt}]
            )

            summary = response.content[0].text
            self.logger.info(f"Generated {style} summary: {summary[:50]}...")
            return summary

        except Exception as e:
            self.logger.error(f"Summarization failed: {e}")
            return None


class ThreadGenerator:
    """Generates threads with Hook-Body-CTA architecture."""

    def __init__(self, claude_client: Anthropic, logger: logging.Logger):
        self.claude_client = claude_client
        self.logger = logger

    def generate_thread(self, topic: str, style: str = "mixed") -> List[str]:
        """Generate a thread with Hook-Body-CTA structure."""

        prompt = f"""Erstelle einen X-Thread (3-5 Tweets) zum Thema: "{topic}"

        Struktur:
        1. HOOK: Attention-grabbing opener (max 280 Zeichen) - muss Neugier wecken
        2-4. BODY: Informative, dichte Insights (je max 280 Zeichen)
        5. CTA: Call-to-Action, organisch, nicht spammy (max 280 Zeichen)

        Stil: {'Provokativ und memetisch' if style == 'creative' else 'Analytisch und faktisch'}

        Format: Nummeriere die Tweets als [1/5], [2/5], etc.
        """

        try:
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                temperature=0.8 if style == "creative" else 0.6,
                messages=[{"role": "user", "content": prompt}]
            )

            thread_text = response.content[0].text

            # Parse tweets from response
            tweets = []
            for line in thread_text.split('\n'):
                line = line.strip()
                # Look for patterns like [1/5], 1., 1), etc.
                if re.match(r'^[\[\(]?\d+[/\.\):\]]', line):
                    # Remove the numbering
                    tweet = re.sub(r'^[\[\(]?\d+[/\.\):\]\s]+', '', line)
                    if tweet and len(tweet) <= 280:
                        tweets.append(tweet)

            if not tweets:
                # Fallback: split by length
                tweets = [thread_text[i:i+270] for i in range(0, len(thread_text), 270)][:5]

            self.logger.info(f"Generated thread with {len(tweets)} tweets")
            return tweets[:5]  # Max 5 tweets

        except Exception as e:
            self.logger.error(f"Thread generation failed: {e}")
            return []


# ============================================================================
# DIMENSION 2: TEMPORAL FLUX
# ============================================================================

class TrendMonitor:
    """Monitors X trends and enables trendjacking."""

    def __init__(self, x_client: tweepy.Client, logger: logging.Logger):
        self.x_client = x_client
        self.logger = logger

    def get_trending_topics(self, woeid: int = 1) -> List[Dict[str, Any]]:
        """Get trending topics (WOEID 1 = Worldwide)."""
        try:
            # Note: Twitter API v2 doesn't have trends endpoint in free tier
            # This is a placeholder for premium access
            self.logger.warning("Trends API requires elevated access")
            return []

        except Exception as e:
            self.logger.error(f"Failed to fetch trends: {e}")
            return []

    def match_trends_to_niche(self, trends: List[str], niche_keywords: List[str]) -> List[str]:
        """Match trending topics to your niche."""
        matched = []

        for trend in trends:
            for keyword in niche_keywords:
                if keyword.lower() in trend.lower():
                    matched.append(trend)
                    break

        self.logger.info(f"Matched {len(matched)} trends to niche")
        return matched


class SmartScheduler:
    """Analyzes engagement data and optimizes posting times."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.engagement_history: List[Dict[str, Any]] = []
        self.load_history()

    def load_history(self):
        """Load engagement history from file."""
        try:
            history_file = Path("data/engagement_history.json")
            if history_file.exists():
                with open(history_file, 'r') as f:
                    self.engagement_history = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load engagement history: {e}")

    def save_history(self):
        """Save engagement history to file."""
        try:
            history_file = Path("data/engagement_history.json")
            history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(history_file, 'w') as f:
                json.dump(self.engagement_history, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save engagement history: {e}")

    def record_post(self, post_time: datetime, engagement: Dict[str, int]):
        """Record a post and its engagement."""
        self.engagement_history.append({
            "timestamp": post_time.isoformat(),
            "hour": post_time.hour,
            "day_of_week": post_time.weekday(),
            "likes": engagement.get("likes", 0),
            "retweets": engagement.get("retweets", 0),
            "replies": engagement.get("replies", 0),
        })
        self.save_history()

    def get_optimal_time(self) -> Optional[int]:
        """Calculate optimal posting hour based on history."""
        if len(self.engagement_history) < 10:
            return None  # Not enough data

        df = pd.DataFrame(self.engagement_history)
        df['total_engagement'] = df['likes'] + df['retweets'] * 2 + df['replies'] * 3

        # Group by hour and calculate average engagement
        hourly_avg = df.groupby('hour')['total_engagement'].mean()
        optimal_hour = hourly_avg.idxmax()

        self.logger.info(f"Optimal posting hour: {optimal_hour}:00")
        return int(optimal_hour)


# ============================================================================
# DIMENSION 3: SOCIAL GRAVITATION
# ============================================================================

class ReplyHandler:
    """Handles replies to mentions and comments."""

    def __init__(self, x_client: tweepy.Client, claude_client: Anthropic, logger: logging.Logger):
        self.x_client = x_client
        self.claude_client = claude_client
        self.logger = logger
        self.last_mention_id: Optional[str] = None

    def check_mentions(self) -> List[Dict[str, Any]]:
        """Check for new mentions."""
        try:
            # Get authenticated user's mentions
            mentions = self.x_client.get_users_mentions(
                id=self.get_my_user_id(),
                since_id=self.last_mention_id,
                max_results=10
            )

            if not mentions.data:
                return []

            # Update last seen ID
            self.last_mention_id = mentions.data[0].id

            return [{"id": tweet.id, "text": tweet.text} for tweet in mentions.data]

        except Exception as e:
            self.logger.error(f"Failed to check mentions: {e}")
            return []

    def get_my_user_id(self) -> str:
        """Get authenticated user's ID."""
        try:
            me = self.x_client.get_me()
            return me.data.id
        except Exception as e:
            self.logger.error(f"Failed to get user ID: {e}")
            return ""

    def generate_reply(self, mention_text: str, mode: str = "friendly") -> Optional[str]:
        """Generate a reply using Claude."""

        if mode == "friendly":
            prompt = f"""Jemand hat mich auf X erwähnt. Erstelle eine freundliche, hilfreiche Antwort (max 280 Zeichen).

            Mention: "{mention_text}"

            Stil: Authentisch, hilfsbereit, nicht zu förmlich."""
        else:  # defensive/debate
            prompt = f"""Jemand hat kritisch auf meinen Beitrag reagiert. Erstelle eine logische, respektvolle Gegenargumentation (max 280 Zeichen).

            Kritik: "{mention_text}"

            Stil: Sachlich, logisch, ohne persönlich zu werden."""

        try:
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            reply = response.content[0].text
            return reply if len(reply) <= 280 else reply[:277] + "..."

        except Exception as e:
            self.logger.error(f"Reply generation failed: {e}")
            return None

    def post_reply(self, tweet_id: str, reply_text: str) -> bool:
        """Post a reply to a tweet."""
        try:
            self.x_client.create_tweet(text=reply_text, in_reply_to_tweet_id=tweet_id)
            self.logger.info(f"Posted reply to {tweet_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to post reply: {e}")
            return False


class InfluencerOrbit:
    """Monitors and interacts with key influencers in your niche."""

    def __init__(self, x_client: tweepy.Client, claude_client: Anthropic, logger: logging.Logger):
        self.x_client = x_client
        self.claude_client = claude_client
        self.logger = logger

    def get_user_recent_tweets(self, username: str, count: int = 5) -> List[Dict[str, Any]]:
        """Get recent tweets from a user."""
        try:
            # Get user ID first
            user = self.x_client.get_user(username=username)
            if not user.data:
                return []

            # Get their recent tweets
            tweets = self.x_client.get_users_tweets(
                id=user.data.id,
                max_results=count,
                tweet_fields=['created_at']
            )

            if not tweets.data:
                return []

            return [
                {
                    "id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at
                }
                for tweet in tweets.data
            ]

        except Exception as e:
            self.logger.error(f"Failed to get tweets from @{username}: {e}")
            return []

    def generate_intelligent_comment(self, tweet_text: str) -> Optional[str]:
        """Generate an intelligent, non-spammy comment."""

        prompt = f"""Ein Influencer hat gepostet. Erstelle einen intelligenten, wertschöpfenden Kommentar (max 280 Zeichen).

        Tweet: "{tweet_text}"

        Anforderungen:
        - Füge einen eigenen Gedanken oder Insight hinzu
        - Keine generische Zustimmung ("Great post!")
        - Keine Eigenwerbung
        - Stelle eine interessante Frage ODER ergänze eine Perspektive
        """

        try:
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            comment = response.content[0].text
            return comment if len(comment) <= 280 else comment[:277] + "..."

        except Exception as e:
            self.logger.error(f"Comment generation failed: {e}")
            return None

    def orbit_influencer(self, username: str) -> bool:
        """Interact with an influencer's recent post."""
        tweets = self.get_user_recent_tweets(username, count=1)

        if not tweets:
            return False

        latest_tweet = tweets[0]

        # Only interact if tweet is less than 5 minutes old (steal reach)
        if latest_tweet['created_at']:
            tweet_age = datetime.now(latest_tweet['created_at'].tzinfo) - latest_tweet['created_at']
            if tweet_age.total_seconds() > 300:  # 5 minutes
                self.logger.info(f"Tweet from @{username} is too old, skipping")
                return False

        comment = self.generate_intelligent_comment(latest_tweet['text'])

        if not comment:
            return False

        try:
            self.x_client.create_tweet(
                text=comment,
                in_reply_to_tweet_id=latest_tweet['id']
            )
            self.logger.info(f"Orbited @{username} successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to orbit @{username}: {e}")
            return False


# ============================================================================
# DIMENSION 4: MEMORY (Ψ - Coherence)
# ============================================================================

class RAGMemory:
    """Vector-based long-term memory using ChromaDB."""

    def __init__(self, db_path: str, logger: logging.Logger):
        self.logger = logger
        self.db_path = db_path
        self.client = None
        self.collection = None
        self.embedder = None
        self.initialize()

    def initialize(self):
        """Initialize ChromaDB and sentence transformer."""
        try:
            Path(self.db_path).mkdir(parents=True, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.db_path)
            self.collection = self.client.get_or_create_collection(
                name="agent_memory",
                metadata={"description": "Long-term memory for X agent"}
            )

            # Load sentence transformer for embeddings
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

            self.logger.info("RAG Memory initialized")

        except Exception as e:
            self.logger.error(f"Failed to initialize RAG memory: {e}")

    def store_post(self, post_text: str, post_id: str, metadata: Dict[str, Any]):
        """Store a post in vector memory."""
        try:
            embedding = self.embedder.encode(post_text).tolist()

            self.collection.add(
                embeddings=[embedding],
                documents=[post_text],
                ids=[post_id],
                metadatas=[metadata]
            )

            self.logger.info(f"Stored post {post_id} in memory")

        except Exception as e:
            self.logger.error(f"Failed to store post: {e}")

    def search_similar_posts(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for similar posts in memory."""
        try:
            query_embedding = self.embedder.encode(query).tolist()

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )

            similar_posts = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    similar_posts.append({
                        "text": doc,
                        "distance": results['distances'][0][i] if 'distances' in results else None,
                        "metadata": results['metadatas'][0][i] if 'metadatas' in results else {}
                    })

            return similar_posts

        except Exception as e:
            self.logger.error(f"Failed to search memory: {e}")
            return []

    def check_repetition(self, new_post: str, threshold: float = 0.8) -> bool:
        """Check if we're about to repeat ourselves."""
        similar = self.search_similar_posts(new_post, n_results=1)

        if similar and similar[0]['distance'] is not None:
            similarity = 1 - similar[0]['distance']  # Convert distance to similarity
            if similarity > threshold:
                self.logger.warning(f"Post too similar to previous content (similarity: {similarity:.2f})")
                return True

        return False


class FeedbackLoop:
    """Analyzes post performance and optimizes strategy."""

    def __init__(self, x_client: tweepy.Client, logger: logging.Logger):
        self.x_client = x_client
        self.logger = logger
        self.performance_data: List[Dict[str, Any]] = []
        self.load_performance_data()

    def load_performance_data(self):
        """Load performance data from file."""
        try:
            perf_file = Path("data/performance_data.json")
            if perf_file.exists():
                with open(perf_file, 'r') as f:
                    self.performance_data = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load performance data: {e}")

    def save_performance_data(self):
        """Save performance data to file."""
        try:
            perf_file = Path("data/performance_data.json")
            perf_file.parent.mkdir(parents=True, exist_ok=True)
            with open(perf_file, 'w') as f:
                json.dump(self.performance_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save performance data: {e}")

    def analyze_post(self, post_id: str, post_text: str, post_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch and analyze a post's performance after 24h."""
        try:
            # Get tweet details
            tweet = self.x_client.get_tweet(
                id=post_id,
                tweet_fields=['public_metrics']
            )

            if not tweet.data:
                return {}

            metrics = tweet.data.public_metrics

            performance = {
                "post_id": post_id,
                "text": post_text,
                "likes": metrics.get('like_count', 0),
                "retweets": metrics.get('retweet_count', 0),
                "replies": metrics.get('reply_count', 0),
                "impressions": metrics.get('impression_count', 0),
                "engagement_rate": self.calculate_engagement_rate(metrics),
                "metadata": post_metadata,
                "analyzed_at": datetime.now().isoformat()
            }

            self.performance_data.append(performance)
            self.save_performance_data()

            self.logger.info(f"Analyzed post {post_id}: {performance['engagement_rate']:.2%} engagement")
            return performance

        except Exception as e:
            self.logger.error(f"Failed to analyze post {post_id}: {e}")
            return {}

    def calculate_engagement_rate(self, metrics: Dict[str, int]) -> float:
        """Calculate engagement rate."""
        impressions = metrics.get('impression_count', 0)
        if impressions == 0:
            return 0.0

        engagements = (
            metrics.get('like_count', 0) +
            metrics.get('retweet_count', 0) * 2 +
            metrics.get('reply_count', 0) * 3
        )

        return engagements / impressions

    def get_insights(self) -> Dict[str, Any]:
        """Extract insights from performance data."""
        if len(self.performance_data) < 5:
            return {"status": "insufficient_data"}

        df = pd.DataFrame(self.performance_data)

        # Find best performing content type
        best_post = df.loc[df['engagement_rate'].idxmax()]

        # Calculate averages by content type if available
        insights = {
            "best_post": {
                "text": best_post['text'][:50],
                "engagement_rate": best_post['engagement_rate']
            },
            "average_engagement": df['engagement_rate'].mean(),
            "total_analyzed": len(self.performance_data)
        }

        self.logger.info(f"Generated insights: {insights['average_engagement']:.2%} avg engagement")
        return insights


# ============================================================================
# MAIN AGENT CLASS
# ============================================================================

class XPostingAgent:
    """Hyper-Intelligent X Posting Agent - The Resonance Machine."""

    CONTENT_PROMPTS = {
        "tech_news": "Generiere einen kurzen, informativen X-Beitrag (max 280 Zeichen) über aktuelle KI- oder Technologie-Trends. Der Beitrag sollte interessant und informativ sein. Füge 2-3 relevante Hashtags hinzu.",
        "tips_tricks": "Generiere einen hilfreichen X-Beitrag (max 280 Zeichen) mit einem praktischen Tipp für Entwickler oder Tech-Enthusiasten. Der Tipp sollte konkret und umsetzbar sein. Füge 2-3 relevante Hashtags hinzu.",
        "inspiration": "Generiere einen motivierenden X-Beitrag (max 280 Zeichen) über Innovation, Technologie oder persönliches Wachstum. Der Beitrag sollte inspirierend und positiv sein. Füge 2-3 relevante Hashtags hinzu.",
        "summary": "Fasse einen Artikel zusammen und teile deine Meinung (max 280 Zeichen). Sei kritisch und füge Kontext hinzu.",
    }

    def __init__(self, config_path: str = "config.json"):
        """Initialize the X Posting Agent."""
        self.config = self._load_config(config_path)
        self.metrics = self._load_metrics()
        self.logger = self._setup_logging()

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
        self.pending_posts: List[Dict[str, Any]] = []  # For 24h feedback

    def _load_config(self, config_path: str) -> Config:
        """Load configuration from JSON file."""
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Config(**data)
        return Config()

    def _load_metrics(self) -> Metrics:
        """Load metrics from JSON file."""
        metrics_file = Path("metrics.json")
        if metrics_file.exists():
            with open(metrics_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Metrics(**data)
        return Metrics()

    def _save_metrics(self) -> None:
        """Save metrics to JSON file."""
        with open("metrics.json", "w", encoding="utf-8") as f:
            json.dump(self.metrics.model_dump(), f, indent=2)

    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger("XPostingAgent")
        logger.setLevel(getattr(logging, self.config.logging.level))

        # Create logs directory
        log_path = Path(self.config.logging.file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # File handler with JSON formatting
        file_handler = logging.FileHandler(self.config.logging.file)
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

    def _init_claude_client(self) -> bool:
        """Initialize the Claude API client."""
        api_key = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            self.logger.error("Claude API Key nicht gefunden. Bitte CLAUDE_API_KEY setzen.")
            return False

        try:
            self.claude_client = Anthropic(api_key=api_key)
            self.logger.info("Claude SDK erfolgreich initialisiert")
            return True
        except Exception as e:
            self.logger.error(f"Fehler bei Claude SDK Initialisierung: {e}")
            return False

    def _init_x_client(self) -> bool:
        """Initialize the X API client."""
        api_key = os.getenv("X_API_KEY")
        api_secret = os.getenv("X_API_SECRET")
        access_token = os.getenv("X_ACCESS_TOKEN")
        access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

        if not all([api_key, api_secret, access_token, access_token_secret]):
            self.logger.error("X API Credentials nicht vollständig. Bitte alle X_* Variablen setzen.")
            return False

        try:
            self.x_client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
            self.logger.info("X API Client erfolgreich initialisiert")
            return True
        except Exception as e:
            self.logger.error(f"Fehler bei X API Initialisierung: {e}")
            return False

    def _init_advanced_modules(self):
        """Initialize advanced modules."""
        try:
            # Dimension 1: Cognitive Resonance
            self.content_summarizer = ContentSummarizer(self.claude_client, self.logger)
            self.thread_generator = ThreadGenerator(self.claude_client, self.logger)

            # Dimension 2: Temporal Flux
            self.trend_monitor = TrendMonitor(self.x_client, self.logger)
            self.smart_scheduler = SmartScheduler(self.logger)

            # Dimension 3: Social Gravitation
            if self.config.interaction.enable_replies:
                self.reply_handler = ReplyHandler(self.x_client, self.claude_client, self.logger)

            if self.config.interaction.enable_influencer_orbit:
                self.influencer_orbit = InfluencerOrbit(self.x_client, self.claude_client, self.logger)

            # Dimension 4: Memory
            if self.config.memory.enable_rag:
                self.rag_memory = RAGMemory(self.config.memory.vector_db_path, self.logger)

            if self.config.memory.enable_feedback_loop:
                self.feedback_loop = FeedbackLoop(self.x_client, self.logger)

            self.logger.info("Advanced modules initialized")

        except Exception as e:
            self.logger.error(f"Failed to initialize some modules: {e}")

    def _get_content_type(self) -> str:
        """Get the content type for the next post."""
        if self.config.posting.content_type == "mixed":
            return random.choice(list(self.CONTENT_PROMPTS.keys()))
        return self.config.posting.content_type

    def _generate_post_content(self, content_type: Optional[str] = None) -> Optional[str]:
        """Generate post content using Claude."""
        if not self.claude_client:
            self.logger.error("Claude Client nicht initialisiert")
            return None

        content_type = content_type or self._get_content_type()
        prompt = self.CONTENT_PROMPTS.get(content_type, self.CONTENT_PROMPTS["tech_news"])

        try:
            response = self.claude_client.messages.create(
                model=self.config.claude.model,
                max_tokens=self.config.claude.max_tokens,
                temperature=self.config.claude.temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text

            # Check for repetition in memory
            if self.rag_memory and self.rag_memory.check_repetition(content):
                self.logger.warning("Content too similar to previous posts, regenerating...")
                return self._generate_post_content(content_type)

            self.logger.info(f"Beitrag generiert ({content_type}): {content[:50]}...")
            return content

        except Exception as e:
            self.logger.error(f"Fehler bei Beitragsgenerierung: {e}")
            return None

    def _validate_post(self, content: str) -> bool:
        """Validate post content before posting."""
        if not content:
            return False

        if len(content) > 280:
            self.logger.warning(f"Beitrag zu lang ({len(content)} Zeichen)")
            return False

        return True

    def _post_to_x(self, content: str, in_reply_to: Optional[str] = None) -> Optional[str]:
        """Post content to X. Returns tweet ID if successful."""
        if not self.x_client:
            self.logger.error("X Client nicht initialisiert")
            return None

        try:
            kwargs = {"text": content}
            if in_reply_to:
                kwargs["in_reply_to_tweet_id"] = in_reply_to

            response = self.x_client.create_tweet(**kwargs)
            tweet_id = response.data.get("id") if response.data else None

            if tweet_id:
                self.logger.info(f"Beitrag erfolgreich gepostet (ID: {tweet_id})")

                # Store in RAG memory
                if self.rag_memory:
                    self.rag_memory.store_post(
                        content,
                        str(tweet_id),
                        {"posted_at": datetime.now().isoformat(), "type": "post"}
                    )

                # Add to pending posts for feedback
                self.pending_posts.append({
                    "id": tweet_id,
                    "text": content,
                    "posted_at": datetime.now(),
                    "metadata": {}
                })

            return tweet_id

        except Exception as e:
            self.logger.error(f"Fehler beim Posten: {e}")
            return None

    def _post_thread(self, tweets: List[str]) -> bool:
        """Post a thread to X."""
        if not tweets:
            return False

        previous_tweet_id = None

        for i, tweet in enumerate(tweets):
            tweet_id = self._post_to_x(tweet, in_reply_to=previous_tweet_id)

            if not tweet_id:
                self.logger.error(f"Failed to post tweet {i+1}/{len(tweets)}")
                return False

            previous_tweet_id = tweet_id
            time.sleep(2)  # Small delay between tweets

        self.logger.info(f"Thread posted successfully ({len(tweets)} tweets)")
        return True

    def _update_metrics(self, success: bool, interaction_type: str = "post") -> None:
        """Update metrics after action."""
        if interaction_type == "post":
            self.metrics.total_posts += 1
            if success:
                self.metrics.successful_posts += 1
                self.metrics.last_post = datetime.now().isoformat()
            else:
                self.metrics.failed_posts += 1

        elif interaction_type == "reply":
            self.metrics.total_replies += 1

        elif interaction_type == "trendjack":
            self.metrics.total_trendjacks += 1

        elif interaction_type == "orbit":
            self.metrics.total_orbit_interactions += 1

        # Update uptime
        uptime = datetime.now() - self.start_time
        self.metrics.uptime_hours = round(uptime.total_seconds() / 3600, 2)

        self._save_metrics()

    def _reset_daily_counter(self) -> None:
        """Reset daily post counter if it's a new day."""
        today = datetime.now().strftime("%Y-%m-%d")
        if self.last_post_date != today:
            self.posts_today = 0
            self.last_post_date = today

    def _can_post(self) -> bool:
        """Check if agent can post (respects daily limit)."""
        self._reset_daily_counter()
        return self.posts_today < self.config.posting.max_posts_per_day

    def post_cycle(self) -> None:
        """Execute a posting cycle."""
        if not self.config.agent.enabled:
            self.logger.info("Agent ist deaktiviert")
            return

        if not self._can_post():
            self.logger.info(f"Tägliches Limit erreicht ({self.config.posting.max_posts_per_day} Posts)")
            return

        self.logger.info("Starte Posting-Zyklus...")

        # Decide between single post or thread
        use_thread = self.config.posting.enable_threads and random.random() > 0.7

        if use_thread:
            # Generate and post a thread
            topic = random.choice([
                "KI-Entwicklungen",
                "Developer Productivity",
                "Future of Tech",
                "Programming Best Practices"
            ])

            tweets = self.thread_generator.generate_thread(topic)
            success = self._post_thread(tweets)
            self._update_metrics(success, "post")

            if success:
                self.posts_today += 1

        else:
            # Generate and post single tweet
            content = self._generate_post_content()

            if not content or not self._validate_post(content):
                self._update_metrics(False, "post")
                return

            tweet_id = self._post_to_x(content)
            success = tweet_id is not None
            self._update_metrics(success, "post")

            if success:
                self.posts_today += 1

    def interaction_cycle(self) -> None:
        """Execute interaction cycle (replies, orbiting)."""

        # Check and reply to mentions
        if self.reply_handler:
            mentions = self.reply_handler.check_mentions()
            for mention in mentions[:3]:  # Limit to 3 per cycle
                reply = self.reply_handler.generate_reply(mention['text'])
                if reply:
                    success = self.reply_handler.post_reply(mention['id'], reply)
                    self._update_metrics(success, "reply")

        # Orbit influencers
        if self.influencer_orbit and self.config.interaction.influencer_accounts:
            influencer = random.choice(self.config.interaction.influencer_accounts)
            success = self.influencer_orbit.orbit_influencer(influencer)
            if success:
                self._update_metrics(True, "orbit")

    def feedback_cycle(self) -> None:
        """Execute feedback cycle (analyze old posts)."""
        if not self.feedback_loop:
            return

        # Check posts that are 24h old
        now = datetime.now()
        posts_to_analyze = [
            p for p in self.pending_posts
            if (now - p['posted_at']).total_seconds() >= 86400  # 24 hours
        ]

        for post in posts_to_analyze:
            self.feedback_loop.analyze_post(post['id'], post['text'], post['metadata'])
            self.pending_posts.remove(post)

        # Get insights
        if len(self.feedback_loop.performance_data) >= 5:
            insights = self.feedback_loop.get_insights()
            self.logger.info(f"Feedback insights: {insights}")

    def run(self) -> None:
        """Run the agent."""
        self.logger.info(f"🚀 Agent gestartet: {self.config.agent.name} v{self.config.agent.version}")

        # Initialize clients
        if not self._init_claude_client():
            self.logger.error("Konnte Claude Client nicht initialisieren. Beende...")
            sys.exit(1)

        if not self._init_x_client():
            self.logger.error("Konnte X Client nicht initialisieren. Beende...")
            sys.exit(1)

        # Initialize advanced modules
        self._init_advanced_modules()

        # Run initial posting cycle
        self.post_cycle()

        # Schedule regular cycles
        schedule.every(self.config.posting.interval_hours).hours.do(self.post_cycle)

        if self.config.interaction.enable_replies or self.config.interaction.enable_influencer_orbit:
            schedule.every(self.config.interaction.reply_check_interval_minutes).minutes.do(self.interaction_cycle)

        if self.config.memory.enable_feedback_loop:
            schedule.every(self.config.memory.feedback_check_hours).hours.do(self.feedback_cycle)

        self.logger.info("🎯 Agent läuft. Drücke Ctrl+C zum Beenden.")
        self.logger.info(f"📊 Posting: alle {self.config.posting.interval_hours}h")
        self.logger.info(f"💬 Interaktion: alle {self.config.interaction.reply_check_interval_minutes}min")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("Agent wird beendet...")
            self._save_metrics()
            self.logger.info("✅ Agent beendet.")


def main():
    """Main entry point."""
    agent = XPostingAgent()
    agent.run()


if __name__ == "__main__":
    main()
