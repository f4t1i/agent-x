#!/usr/bin/env python3
"""
Test X API Connection
Verifies that your X API credentials are correctly configured.
"""

import os
import sys
from dotenv import load_dotenv
import tweepy

# Load environment variables
load_dotenv()

def test_connection():
    """Test X API connection and display account info."""

    print("🔍 Loading X API credentials from .env...")

    # Load credentials
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    # Validate credentials exist
    missing = []
    if not api_key:
        missing.append("X_API_KEY")
    if not api_secret:
        missing.append("X_API_SECRET")
    if not access_token:
        missing.append("X_ACCESS_TOKEN")
    if not access_token_secret:
        missing.append("X_ACCESS_TOKEN_SECRET")

    if missing:
        print(f"❌ Missing credentials in .env file:")
        for key in missing:
            print(f"   - {key}")
        print("\n💡 Make sure you have copied .env.example to .env and filled in all values.")
        sys.exit(1)

    print("✅ All credentials found in .env")

    # Initialize X API client
    print("\n🔌 Connecting to X API...")

    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

        # Test connection by getting authenticated user info
        me = client.get_me()

        if not me.data:
            print("❌ Connection failed: No user data returned")
            sys.exit(1)

        print("✅ Connection successful!\n")
        print("📱 Account Information:")
        print(f"   Username: @{me.data.username}")
        print(f"   Name: {me.data.name}")
        print(f"   ID: {me.data.id}")

        # Check permissions
        print("\n🔑 Testing permissions...")

        # Try to get own tweets (requires read permission)
        try:
            tweets = client.get_users_tweets(
                id=me.data.id,
                max_results=5
            )
            print("   ✅ Read permission: OK")
        except Exception as e:
            print(f"   ❌ Read permission: FAILED ({e})")

        # Note: We don't actually post to test write permission
        # User needs to test this manually or with agent
        print("   ⚠️  Write permission: NOT TESTED (would require actual posting)")
        print("      To verify write permission, run the agent and check if it can post.")

        print("\n✅ All tests passed!")
        print("\n🚀 Your X API is ready to use with the Hyper-Agent!")

    except tweepy.errors.Unauthorized as e:
        print(f"❌ Authentication failed!")
        print(f"   Error: {e}")
        print("\n💡 Possible causes:")
        print("   1. API keys are incorrect")
        print("   2. Access token/secret are invalid")
        print("   3. App permissions not set correctly")
        print("\n🔧 Solutions:")
        print("   1. Double-check all credentials in .env")
        print("   2. Regenerate Access Token & Secret in Developer Portal")
        print("   3. Ensure app has 'Read and Write' permissions")
        sys.exit(1)

    except tweepy.errors.Forbidden as e:
        print(f"❌ Permission denied!")
        print(f"   Error: {e}")
        print("\n💡 Possible causes:")
        print("   1. App permissions set to 'Read-only'")
        print("   2. Access tokens not regenerated after permission change")
        print("\n🔧 Solutions:")
        print("   1. Go to Developer Portal → App Settings")
        print("   2. Set permissions to 'Read and Write'")
        print("   3. REGENERATE Access Token & Secret")
        print("   4. Update .env with new tokens")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("\n💡 Check:")
        print("   1. Internet connection")
        print("   2. X API status: https://api.twitterstat.us/")
        print("   3. Developer Portal: https://developer.x.com/")
        sys.exit(1)


if __name__ == "__main__":
    print("=" * 60)
    print("  X API Connection Test")
    print("=" * 60)
    print()

    test_connection()
