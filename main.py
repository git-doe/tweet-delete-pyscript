import time
import tweepy

# Replace these with YOUR credentials from the twitter Dev Portal
BEARER_TOKEN = ""
API_KEY = ""
API_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def delete_all_tweets():
    # Fetch the authenticated user's ID
    me = client.get_me()
    user_id = me.data.id
    print(f"Authenticated as @{me.data.username} (ID: {user_id})\n")

    deleted_count = 0

    while True:
        # Fetch up to 100 recent tweets at a time
        tweets = client.get_users_tweets(id=user_id, max_results=100)

        if not tweets.data:
            print("No more tweets found to delete.")
            break

        for tweet in tweets.data:
            try:
                client.delete_tweet(tweet.id)
                deleted_count += 1
                print(f"[{deleted_count}] Deleted Tweet ID: {tweet.id}")
                
                # Small pause to help avoid aggressive rate limits
                time.sleep(0.5)

            except tweepy.TooManyRequests:
                print("Rate limit reached. Waiting 15 minutes before retrying...")
                time.sleep(15 * 60)
            except Exception as e:
                print(f"Failed to delete Tweet {tweet.id}: {e}")

    print(f"\nFinished! Total tweets deleted: {deleted_count}")

if __name__ == "__main__":
    delete_all_tweets()
