import tweepy
import datetime
import time
import configparser
import pytz

# Read API credentials from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

API_KEY = config.get("twitter", "API_KEY")
API_SECRET_KEY = config.get("twitter", "API_SECRET_KEY")
ACCESS_TOKEN = config.get("twitter", "ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = config.get("twitter", "ACCESS_TOKEN_SECRET")
BEARER_TOKEN = config.get("twitter", "BEARER_TOKEN")

# Authenticate to Twitter API v2
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True,
)

# Calculate the cutoff date
now = datetime.datetime.now(datetime.timezone.utc)
cutoff_date = now - datetime.timedelta(days=30)


# Function to delete old tweets using API v2
def delete_old_tweets_v2():
    try:
        user_id = client.get_me().data.id

        # Fetch tweets using Paginator
        paginator = tweepy.Paginator(
            client.get_users_tweets,
            id=user_id,
            tweet_fields=["created_at"],
            max_results=100,
        )

        deleted_count = 0
        total_checked = 0

        for response in paginator:
            tweets = response.data
            if not tweets:
                break

            for tweet in tweets:
                total_checked += 1
                tweet_date = tweet.created_at.replace(tzinfo=None).astimezone(datetime.timezone.utc)

                if tweet_date < cutoff_date:
                    print(f"Deleting tweet ID {tweet.id} from {tweet_date}")
                    try:
                        client.delete_tweet(tweet.id)
                        deleted_count += 1
                        # Sleep to avoid hitting rate limits
                        time.sleep(1)
                    except tweepy.TweepyException as e:
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
    delete_old_tweets_v2()
