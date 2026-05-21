# Lab 1: The Social Media Data Detective

## Project Structure

```
lab1_Pirate13Thebes/
├── data-detective.py      # Main Python script (all 4 quests)
├── feed-analyzer.sh       # Bash script (Quest 3 shell version)
├── twitter_dataset.csv    # Dataset (download from Kaggle)
└── README.md              # This file
```

## Prerequisites

- Python 3.x
- A Unix/Linux/macOS terminal (or Git Bash on Windows) for the shell script
- `twitter_dataset.csv` downloaded from (https://www.kaggle.com/datasets/goyaladi/twitter-dataset?select=twitter_dataset.csv) and placed in the same folder

## Usage Instructions

### Python Script (`data-detective.py`)

1. Place `twitter_dataset.csv` in the same directory as `data-detective.py`.
2. Run the script:
   ```bash
   python data-detective.py
   ```
3. The script will automatically:
   - **Quest 1** — Clean and audit the data (remove missing tweets, patch missing fields)
   - **Quest 2** — Find and display the most viral tweet by Likes
   - **Quest 3** — Sort all tweets by Likes (highest to lowest) and display the Top 10
4. When prompted, type a keyword and press Enter to search tweets (e.g. `Python`, `love`, `AI`).

### Bash Script (`feed-analyzer.sh`)

Run the shell script with the CSV file as an argument:

```bash
bash feed-analyzer.sh twitter_dataset.csv
```

This will display the **Top 5 Most Active Users** and their post counts directly in the terminal.

## How the Custom Sorting Algorithm Works

The script uses **Selection Sort**: on each pass through the list, it scans the unsorted portion to find the tweet with the highest number of Likes, then swaps it into the correct front position repeating until the entire list is ordered from highest to lowest without using any built-in `.sort()` or `sorted()` function. This approach has a time complexity of O(n²), making the comparison logic explicit and fully transparent for educational purposes.
