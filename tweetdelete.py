import tweepy
import datetime
import time
import configparser
import os

# Read API credentials from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

API_KEY = config.get("twitter", "API_KEY")
API_SECRET_KEY = config.get("twitter", "API_SECRET_KEY")
ACCESS_TOKEN = config.get("twitter", "ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = config.get("twitter", "ACCESS_TOKEN_SECRET")

print(f"API_KEY: {API_KEY}")

# Authenticate to Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Calculate the cutoff date
now = datetime.datetime.now(datetime.timezone.utc)
cutoff_date = now - datetime.timedelta(days=30)


# Function to delete old tweets
def delete_old_tweets():
    try:
        # Fetch tweets (up to the most recent 3,200 tweets)
        tweets = tweepy.Cursor(api.user_timeline, tweet_mode="extended").items()

        deleted_count = 0
        total_checked = 0

        for tweet in tweets:
            total_checked += 1
            tweet_date = tweet.created_at

            if tweet_date < cutoff_date:
                print(f"Deleting tweet ID {tweet.id} from {tweet_date}")
                try:
                    api.destroy_status(tweet.id)
                    deleted_count += 1
                    # Sleep to avoid hitting rate limits (adjust if necessary)
                    time.sleep(1)
                except tweepy.TweepError as e:
                    print(f"Error deleting tweet ID {tweet.id}: {e}")
            else:
                print(f"Keeping tweet ID {tweet.id} from {tweet_date}")

        print(f"\nSummary:")
        print(f"Total tweets checked: {total_checked}")
        print(f"Total tweets deleted: {deleted_count}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Run the function
if __name__ == "__main__":
    delete_old_tweets()
