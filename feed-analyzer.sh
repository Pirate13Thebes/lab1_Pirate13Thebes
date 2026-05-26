#!/bin/bash
# Analysing twitter_dataset.csv to display the Top 5 Most Active Users.
# Usage: bash feed-analyzer.sh twitter_dataset.csv

FILE=${1:-twitter_dataset.csv}

# Checking if the file exists before proceeding
if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found."
    echo "Usage: bash feed-analyzer.sh twitter_dataset.csv"
    exit 1
fi

echo "Top 5 Most Active Users in: $FILE"

# Skipping the header row with tail, extracting the Username column with cut,
# sorting alphabetically for uniq, counting occurrences with uniq -c,
# sorting by highest count, and keeping only the top 5 with head
tail -n +2 "$FILE" | cut -d',' -f2 | sort | uniq -c | sort -rn | head -5