import csv
import sys
import os


def safe_int(value):
    """
    Converting a string value to an integer safely.
    Handling edge cases like 'N/A', empty strings, or decimals like '150.0'
    by returning 0 instead of crashing the program.
    """
    try:
        return int(float(value))  # using float() first to handle decimal strings
    except (ValueError, TypeError):
        return 0


def load_raw_data(filename):
    """
    Opening the CSV file and loading every row into a list of dictionaries.
    Each key mapping to a column header and each value holding the raw string
    from that cell. Validating the file exists and contains required columns
    before proceeding.
    """
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        print("Make sure 'twitter_dataset.csv' is in the same folder as this script.")
        sys.exit(1)

    raw_tweets = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Checking that all required columns exist before reading any data
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


def clean_data(tweets):
    """
    QUEST 1: Auditing and cleaning the raw tweet data.
    Removing any tweet missing a Text field since it is unrecoverable.
    Replacing missing or non-numeric Likes and Retweets values with '0'.
    Printing a summary of all rows removed or fields patched.
    """
    clean_tweets = []
    removed = 0  # tracking how many tweets are dropped due to missing Text
    fixed = 0    # tracking how many fields are patched with '0'

    for tweet in tweets:
        # Checking if Text exists and contains actual content
        text_value = tweet.get('Text', '')
        if not text_value or text_value.strip() == '':
            removed += 1
            continue  # skipping this tweet — missing Text is unrecoverable

        # Validating Likes — catching empty strings and non-numeric values
        likes_value = tweet.get('Likes', '').strip()
        try:
            int(float(likes_value))
        except (ValueError, TypeError):
            tweet['Likes'] = '0'  # replacing bad value with safe default
            fixed += 1

        # Validating Retweets — applying the same safe replacement logic
        retweets_value = tweet.get('Retweets', '').strip()
        try:
            int(float(retweets_value))
        except (ValueError, TypeError):
            tweet['Retweets'] = '0'
            fixed += 1

        # Adding the tweet to the clean list after passing all checks
        clean_tweets.append(tweet)

    print("[Quest 1] Data Audit Complete")
    print(f"  Rows removed   (missing Text)        : {removed}")
    print(f"  Fields patched (bad Likes/Retweets)  : {fixed}")
    print(f"  Clean tweets remaining               : {len(clean_tweets)}")
    print()

    return clean_tweets


def find_viral_tweet(tweets):
    """
    QUEST 2: Finding the tweet with the highest number of Likes.
    Looping through every tweet manually and tracking the current maximum
    without using Python's built-in max() function.
    Printing the Username, Likes count, and Text of the winning tweet.
    """
    if len(tweets) == 0:
        print("[Quest 2] No tweets available to analyse.\n")
        return None

    # Assuming the first tweet is the most viral as a starting reference point
    viral = tweets[0]
    current_max = safe_int(tweets[0]['Likes'])

    # Comparing each remaining tweet against the current maximum — O(n)
    for i in range(1, len(tweets)):
        tweet_likes = safe_int(tweets[i]['Likes'])

        # Updating the tracker whenever a higher Likes count is found
        if tweet_likes > current_max:
            current_max = tweet_likes
            viral = tweets[i]

    print("[Quest 2] Most Viral Tweet")
    print(f"  Username : {viral.get('Username', 'N/A')}")
    print(f"  Likes    : {safe_int(viral['Likes']):,}")
    print(f"  Text     : {viral.get('Text', 'N/A')}")
    print()

    return viral


def merge_sort(tweets):
    """
    Recursively dividing the tweet list in half until each piece holds
    one element, then merging the pieces back together in descending
    order by the pre-computed '_likes' key.
    Running at O(n log n) — log n levels of splitting, n comparisons per level.
    """
    # Returning immediately when the list is already trivially sorted
    if len(tweets) <= 1:
        return tweets

    # Splitting the list into two equal halves
    mid   = len(tweets) // 2
    left  = merge_sort(tweets[:mid])   # recursively sorting the left half
    right = merge_sort(tweets[mid:])   # recursively sorting the right half

    # Merging the two sorted halves back into one sorted list
    merged = []
    i = 0  # pointer advancing through the left half
    j = 0  # pointer advancing through the right half

    # Picking the larger Likes value first to produce descending order
    while i < len(left) and j < len(right):
        if left[i]['_likes'] >= right[j]['_likes']:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Appending any remaining elements from the left half
    while i < len(left):
        merged.append(left[i])
        i += 1

    # Appending any remaining elements from the right half
    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged


def custom_sort_by_likes(tweets):
    """
    QUEST 3: Sorting all tweets by Likes in descending order using Merge Sort.
    Pre-computing integer Likes values once before sorting to avoid calling
    safe_int() millions of times inside the recursive comparisons.
    Cleaning up the temporary key after sorting and printing the Top 10 results.

    Complexity: O(n log n) — significantly faster than Selection Sort O(n²).
    On 10,000 tweets: ~130,000 comparisons vs ~50,000,000 with Selection Sort.
    """
    # Pre-converting Likes to integers exactly once — O(n)
    # Storing as '_likes' so the merge step reuses it without re-converting
    for tweet in tweets:
        tweet['_likes'] = safe_int(tweet['Likes'])

    # Running Merge Sort on the pre-computed values
    sorted_tweets = merge_sort(tweets)

    # Removing the temporary '_likes' key now that sorting is complete
    for tweet in sorted_tweets:
        del tweet['_likes']

    # Slicing the top 10 for display
    top_10 = sorted_tweets[:10]

    print("[Quest 3] Top 10 Most Liked Tweets")
    for rank, tweet in enumerate(top_10, start=1):
        username     = tweet.get('Username', 'N/A')
        likes        = safe_int(tweet['Likes'])
        # Truncating long tweet text to keep the output readable
        text_preview = tweet.get('Text', '')[:70] + ('...' if len(tweet.get('Text', '')) > 70 else '')
        print(f"  {rank:>2}. @{username} — {likes:,} likes")
        print(f"      {text_preview}")
    print()

    return sorted_tweets


def search_tweets(tweets, keyword):
    """
    QUEST 4: Searching for a keyword across all tweets and extracting matches.
    Building a brand-new list using .append() for every tweet containing
    the keyword. Printing the total match count using len() followed by
    the full text of each matching tweet.
    """
    if len(tweets) == 0:
        print("[Quest 4] No tweets available to search.\n")
        return []

    keyword_lower = keyword.lower()  # normalising to lowercase for case-insensitive matching
    results = []                     # building a new list to collect all matches

    # Iterating through every tweet and checking for a keyword match — O(n)
    for tweet in tweets:
        tweet_text = tweet.get('Text', '').lower()
        if keyword_lower in tweet_text:
            results.append(tweet)  # adding matching tweet to the results list

    print(f"[Quest 4] Search Results for '{keyword}'")
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


if __name__ == "__main__":
    """
    Running the full pipeline in order:
    Loading raw data → Cleaning → Finding viral tweet → Sorting → Searching.
    """
    print("\nWelcome to the Social Media Data Detective!")

    # Loading raw messy data from the CSV file
    dataset = load_raw_data("twitter_dataset.csv")
    print(f"Loaded {len(dataset)} raw tweets from 'twitter_dataset.csv'.\n")

    # Running Quest 1 — cleaning and auditing the data
    clean_dataset = clean_data(dataset)

    # Stopping early if cleaning leaves no usable tweets
    if len(clean_dataset) == 0:
        print("Error: No valid tweets remained after cleaning. Exiting.")
        sys.exit(1)

    # Running Quest 2 — finding the most viral tweet
    find_viral_tweet(clean_dataset)

    # Running Quest 3 — sorting by Likes and displaying the top 10
    sorted_dataset = custom_sort_by_likes(clean_dataset)

    # Running Quest 4 — searching tweets by user-provided keyword
    while True:
        keyword = input("Enter a keyword to search tweets (cannot be empty): ").strip()
        if keyword == '':
            print("  Please enter at least one character.\n")
        else:
            break

    search_tweets(sorted_dataset, keyword)

    print("Analysis complete. Goodbye!")