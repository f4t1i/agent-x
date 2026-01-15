#!/usr/bin/env python3
"""
Agent - Automated X Posting with Claude Code

This agent automatically generates and posts content to X (formerly Twitter)
using Claude Code and the Claude SDK.
"""

import json
import logging
import os
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import schedule
import time
import tweepy
from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pythonjsonlogger import jsonlogger

# Load environment variables
load_dotenv()


class AgentConfig(BaseModel):
    """Agent configuration model."""
    name: str = "X Posting Agent"
    version: str = "1.0.0"
    enabled: bool = True


class PostingConfig(BaseModel):
    """Posting configuration model."""
    interval_hours: int = 4
    posts_per_cycle: int = 1
    max_posts_per_day: int = 6
    content_type: str = "mixed"


class ClaudeConfig(BaseModel):
    """Claude configuration model."""
    model: str = "claude-3-5-sonnet-20241022"
    temperature: float = 0.7
    max_tokens: int = 280
    use_code_interpreter: bool = True


class LoggingConfig(BaseModel):
    """Logging configuration model."""
    level: str = "INFO"
    file: str = "logs/agent.log"


class Config(BaseModel):
    """Main configuration model."""
    agent: AgentConfig = Field(default_factory=AgentConfig)
    posting: PostingConfig = Field(default_factory=PostingConfig)
    claude: ClaudeConfig = Field(default_factory=ClaudeConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


class Metrics(BaseModel):
    """Metrics tracking model."""
    total_posts: int = 0
    successful_posts: int = 0
    failed_posts: int = 0
    average_engagement: float = 0.0
    uptime_hours: float = 0.0
    last_post: Optional[str] = None


class XPostingAgent:
    """Main agent class for automated X posting."""

    CONTENT_PROMPTS = {
        "tech_news": "Generiere einen kurzen, informativen X-Beitrag (max 280 Zeichen) über aktuelle KI- oder Technologie-Trends. Der Beitrag sollte interessant und informativ sein. Füge 2-3 relevante Hashtags hinzu.",
        "tips_tricks": "Generiere einen hilfreichen X-Beitrag (max 280 Zeichen) mit einem praktischen Tipp für Entwickler oder Tech-Enthusiasten. Der Tipp sollte konkret und umsetzbar sein. Füge 2-3 relevante Hashtags hinzu.",
        "inspiration": "Generiere einen motivierenden X-Beitrag (max 280 Zeichen) über Innovation, Technologie oder persönliches Wachstum. Der Beitrag sollte inspirierend und positiv sein. Füge 2-3 relevante Hashtags hinzu.",
    }

    def __init__(self, config_path: str = "config.json"):
        """Initialize the X Posting Agent."""
        self.config = self._load_config(config_path)
        self.metrics = self._load_metrics()
        self.logger = self._setup_logging()
        self.claude_client: Optional[Anthropic] = None
        self.x_client: Optional[tweepy.Client] = None
        self.start_time = datetime.now()
        self.posts_today = 0
        self.last_post_date: Optional[str] = None

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

        # Create logs directory if it doesn't exist
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

    def _get_content_type(self) -> str:
        """Get the content type for the next post."""
        if self.config.posting.content_type == "mixed":
            return random.choice(list(self.CONTENT_PROMPTS.keys()))
        return self.config.posting.content_type

    def _generate_post_content(self) -> Optional[str]:
        """Generate post content using Claude."""
        if not self.claude_client:
            self.logger.error("Claude Client nicht initialisiert")
            return None

        content_type = self._get_content_type()
        prompt = self.CONTENT_PROMPTS.get(content_type, self.CONTENT_PROMPTS["tech_news"])

        try:
            response = self.claude_client.messages.create(
                model=self.config.claude.model,
                max_tokens=self.config.claude.max_tokens,
                temperature=self.config.claude.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            content = response.content[0].text
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
            self.logger.warning(f"Beitrag zu lang ({len(content)} Zeichen), wird gekürzt")
            return False

        return True

    def _post_to_x(self, content: str) -> bool:
        """Post content to X."""
        if not self.x_client:
            self.logger.error("X Client nicht initialisiert")
            return False

        try:
            response = self.x_client.create_tweet(text=content)
            tweet_id = response.data.get("id") if response.data else "unknown"
            self.logger.info(f"Beitrag erfolgreich gepostet (ID: {tweet_id})")
            return True

        except Exception as e:
            self.logger.error(f"Fehler beim Posten: {e}")
            return False

    def _update_metrics(self, success: bool) -> None:
        """Update metrics after posting."""
        self.metrics.total_posts += 1

        if success:
            self.metrics.successful_posts += 1
            self.metrics.last_post = datetime.now().isoformat()
        else:
            self.metrics.failed_posts += 1

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

        for _ in range(self.config.posting.posts_per_cycle):
            if not self._can_post():
                break

            # Generate content
            content = self._generate_post_content()
            if not content:
                self._update_metrics(False)
                continue

            # Validate content
            if not self._validate_post(content):
                # Try to regenerate
                content = self._generate_post_content()
                if not content or not self._validate_post(content):
                    self._update_metrics(False)
                    continue

            # Post to X
            success = self._post_to_x(content)
            self._update_metrics(success)

            if success:
                self.posts_today += 1

        next_post = self.config.posting.interval_hours
        self.logger.info(f"Nächstes Posting in {next_post} Stunden")

    def run(self) -> None:
        """Run the agent."""
        self.logger.info(f"Agent gestartet: {self.config.agent.name} v{self.config.agent.version}")

        # Initialize clients
        if not self._init_claude_client():
            self.logger.error("Konnte Claude Client nicht initialisieren. Beende...")
            sys.exit(1)

        if not self._init_x_client():
            self.logger.error("Konnte X Client nicht initialisieren. Beende...")
            sys.exit(1)

        # Run initial posting cycle
        self.post_cycle()

        # Schedule regular posting cycles
        schedule.every(self.config.posting.interval_hours).hours.do(self.post_cycle)

        self.logger.info("Agent läuft. Drücke Ctrl+C zum Beenden.")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("Agent wird beendet...")
            self._save_metrics()
            self.logger.info("Agent beendet.")


def main():
    """Main entry point."""
    agent = XPostingAgent()
    agent.run()


if __name__ == "__main__":
    main()
