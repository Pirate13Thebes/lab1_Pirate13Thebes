#!/bin/bash
# ─────────────────────────────────────────────────────────────
# feed-analyzer.sh
# Analyzes twitter_dataset.csv to display the Top 5 Most Active Users.
# Usage: bash feed-analyzer.sh twitter_dataset.csv
# ─────────────────────────────────────────────────────────────

FILE=${1:-twitter_dataset.csv}

# Check the file exists before proceeding
if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found."
    echo "Usage: bash feed-analyzer.sh twitter_dataset.csv"
    exit 1
fi

echo "======================================="
echo " Top 5 Most Active Users in: $FILE"
echo "======================================="

# Pipeline explanation:
# tail -n +2        → skip the header row
# cut -d',' -f2     → extract the 2nd column (Username)
# sort              → sort usernames alphabetically (required by uniq)
# uniq -c           → count consecutive identical usernames
# sort -rn          → sort numerically in reverse (highest count first)
# head -5           → keep only the top 5
tail -n +2 "$FILE" | cut -d',' -f2 | sort | uniq -c | sort -rn | head -5

echo "======================================="
