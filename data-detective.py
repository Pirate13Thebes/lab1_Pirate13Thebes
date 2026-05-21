import csv
import sys
import os

# ─────────────────────────────────────────────────────────────
# HELPER: Safe integer conversion
# CSV files store everything as strings. This helper tries to
# convert a value to int; if it fails (e.g. "N/A", "abc"),
# it returns 0 instead of crashing the program.
# ─────────────────────────────────────────────────────────────
def safe_int(value):
    try:
        return int(float(value))  # float() first handles cases like "150.0"
    except (ValueError, TypeError):
        return 0


# ─────────────────────────────────────────────────────────────
# LOAD RAW DATA
# Opens the CSV file and reads every row into a list of
# dictionaries. Each key is a column header, each value is
# the raw string from that cell.
# ─────────────────────────────────────────────────────────────
def load_raw_data(filename):
    # Check the file actually exists before trying to open it
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        print("Make sure 'twitter_dataset.csv' is in the same folder as this script.")
        sys.exit(1)

    raw_tweets = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Validate that the CSV has the required columns
            required_columns = {'Text', 'Likes', 'Retweets', 'Username'}
            if not required_columns.issubset(set(reader.fieldnames or [])):
                missing = required_columns - set(reader.fieldnames or [])
                print(f"Error: CSV is missing required columns: {missing}")
                sys.exit(1)

            for row in reader:
                raw_tweets.append(row)

    except Exception as e:
        print(f"Error: Could not read the file. Details: {e}")
        sys.exit(1)

    return raw_tweets


# ─────────────────────────────────────────────────────────────
# QUEST 1: THE DATA AUDITOR — Handle Missing Fields
# Rules:
#   - If a tweet has no Text (missing or blank), remove it.
#   - If Likes or Retweets is missing, blank, or non-numeric,
#     replace it with '0'.
#   - Print a summary of all rows removed or fixed.
# ─────────────────────────────────────────────────────────────
def clean_data(tweets):
    clean_tweets = []
    removed = 0   # counter for tweets dropped due to missing Text
    fixed = 0     # counter for fields patched with '0'

    for tweet in tweets:
        # ── Check Text ────────────────────────────────────────
        # .get() safely returns None if the key doesn't exist at all
        text_value = tweet.get('Text', '')

        # Strip whitespace; treat blank strings the same as missing
        if not text_value or text_value.strip() == '':
            removed += 1
            continue  # skip this tweet entirely

        # ── Check Likes ───────────────────────────────────────
        likes_value = tweet.get('Likes', '')
        if not likes_value or likes_value.strip() == '' or safe_int(likes_value) == 0 and likes_value.strip() not in ('0', '0.0'):
            # Also catch non-numeric strings like "N/A"
            try:
                int(float(likes_value))
            except (ValueError, TypeError):
                tweet['Likes'] = '0'
                fixed += 1
        if not likes_value or likes_value.strip() == '':
            tweet['Likes'] = '0'
            fixed += 1

        # ── Check Retweets ────────────────────────────────────
        retweets_value = tweet.get('Retweets', '')
        if not retweets_value or retweets_value.strip() == '':
            tweet['Retweets'] = '0'
            fixed += 1
        else:
            # Catch non-numeric Retweets values
            try:
                int(float(retweets_value))
            except (ValueError, TypeError):
                tweet['Retweets'] = '0'
                fixed += 1

        # This tweet passed all checks — add it to the clean list
        clean_tweets.append(tweet)

    # ── Print audit summary ───────────────────────────────────
    print("=" * 55)
    print("[Quest 1] Data Audit Complete")
    print("=" * 55)
    print(f"  Rows removed  (missing Text)          : {removed}")
    print(f"  Fields patched (missing Likes/Retweets): {fixed}")
    print(f"  Clean tweets remaining                 : {len(clean_tweets)}")
    print()

    return clean_tweets


# ─────────────────────────────────────────────────────────────
# QUEST 2: THE VIRAL POST — Find the Maximum Likes
# Rules:
#   - No max() function allowed.
#   - Manually loop through every tweet keeping track of
#     the current highest-likes tweet seen so far.
#   - Print Username, Likes, and Text of the winner.
# ─────────────────────────────────────────────────────────────
def find_viral_tweet(tweets):
    # Guard: nothing to search if the list is empty
    if len(tweets) == 0:
        print("[Quest 2] No tweets available to analyse.\n")
        return None

    # Assume the very first tweet is the most viral to start
    viral = tweets[0]
    current_max = safe_int(tweets[0]['Likes'])

    # Loop from the second tweet onward
    for i in range(1, len(tweets)):
        tweet_likes = safe_int(tweets[i]['Likes'])

        # If this tweet beats the current record, update our tracker
        if tweet_likes > current_max:
            current_max = tweet_likes
            viral = tweets[i]

    print("=" * 55)
    print("[Quest 2] Most Viral Tweet")
    print("=" * 55)
    print(f"  Username : {viral.get('Username', 'N/A')}")
    print(f"  Likes    : {safe_int(viral['Likes']):,}")
    print(f"  Text     : {viral.get('Text', 'N/A')}")
    print()

    return viral


# ─────────────────────────────────────────────────────────────
# QUEST 3: THE ALGORITHM BUILDER — Custom Sort (Selection Sort)
# Rules:
#   - No .sort(), sorted() allowed.
#   - Implement Selection Sort descending by Likes.
#   - Print only the Top 10 results.
#
# How Selection Sort works:
#   On each outer pass i, scan the unsorted portion (i to end)
#   to find the index of the tweet with the most likes.
#   Swap that tweet into position i.
#   After n passes, the list is fully sorted highest → lowest.
# ─────────────────────────────────────────────────────────────
def custom_sort_by_likes(tweets):
    n = len(tweets)

    # Outer loop: each iteration "locks in" one position from the front
    for i in range(n):
        # Assume the current position holds the maximum
        max_index = i

        # Inner loop: scan everything to the right of position i
        for j in range(i + 1, n):
            # Convert to int for a correct numeric comparison
            # (string comparison would make "90" > "100" — wrong!)
            if safe_int(tweets[j]['Likes']) > safe_int(tweets[max_index]['Likes']):
                max_index = j  # found a new candidate for maximum

        # Swap the found maximum into position i
        tweets[i], tweets[max_index] = tweets[max_index], tweets[i]

    # Slice the first 10 tweets for display
    top_10 = tweets[:10]

    print("=" * 55)
    print("[Quest 3] Top 10 Most Liked Tweets")
    print("=" * 55)
    for rank, tweet in enumerate(top_10, start=1):
        username = tweet.get('Username', 'N/A')
        likes    = safe_int(tweet['Likes'])
        # Truncate long tweet text so the output stays readable
        text_preview = tweet.get('Text', '')[:70] + ('...' if len(tweet.get('Text', '')) > 70 else '')
        print(f"  {rank:>2}. @{username} — {likes:,} likes")
        print(f"      {text_preview}")
    print()

    return tweets


# ─────────────────────────────────────────────────────────────
# QUEST 4: THE CONTENT FILTER — Search & Extract
# Rules:
#   - Ask the user for a keyword.
#   - Build a brand-new list of matching tweets using .append().
#   - Print len() of results, then the tweets themselves.
#   - Input must not be empty.
# ─────────────────────────────────────────────────────────────
def search_tweets(tweets, keyword):
    # Guard: empty dataset
    if len(tweets) == 0:
        print("[Quest 4] No tweets available to search.\n")
        return []

    keyword_lower = keyword.lower()  # normalise to lowercase for case-insensitive match
    results = []                     # brand-new list to collect matches

    # Iterate through every tweet and check if the keyword appears in Text
    for tweet in tweets:
        tweet_text = tweet.get('Text', '').lower()
        if keyword_lower in tweet_text:
            results.append(tweet)   # add to new list if it matches

    print("=" * 55)
    print(f"[Quest 4] Search Results for '{keyword}'")
    print("=" * 55)
    print(f"  {len(results)} tweet(s) matched out of {len(tweets)} total.\n")

    if len(results) == 0:
        print("  No tweets found containing that keyword.")
    else:
        for tweet in results:
            username = tweet.get('Username', 'N/A')
            text     = tweet.get('Text', 'N/A')
            print(f"  @{username}: {text}")
    print()

    return results


# ─────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# Orchestrates the full pipeline:
#   Load → Clean → Find Viral → Sort → Search
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\nWelcome to the Social Media Data Detective!")
    print("=" * 55)

    # ── Step 1: Load raw messy data ───────────────────────────
    dataset = load_raw_data("twitter_dataset.csv")
    print(f"Loaded {len(dataset)} raw tweets from 'twitter_dataset.csv'.\n")

    # ── Step 2: Quest 1 — Clean the data ─────────────────────
    clean_dataset = clean_data(dataset)

    # Guard: stop early if cleaning left nothing to work with
    if len(clean_dataset) == 0:
        print("Error: No valid tweets remained after cleaning. Exiting.")
        sys.exit(1)

    # ── Step 3: Quest 2 — Find the most viral tweet ───────────
    find_viral_tweet(clean_dataset)

    # ── Step 4: Quest 3 — Sort by likes and show top 10 ──────
    # Note: custom_sort_by_likes sorts the list in place and returns it
    sorted_dataset = custom_sort_by_likes(clean_dataset)

    # ── Step 5: Quest 4 — Keyword search ─────────────────────
    # Keep asking until the user provides a non-empty keyword
    while True:
        keyword = input("Enter a keyword to search tweets (cannot be empty): ").strip()
        if keyword == '':
            print("  Please enter at least one character.\n")
        else:
            break

    search_tweets(sorted_dataset, keyword)

    print("Analysis complete. Goodbye!")
