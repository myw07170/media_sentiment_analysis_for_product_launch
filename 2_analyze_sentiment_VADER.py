import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- Configuration ---
INPUT_FILENAME = "raw_articles.json"
OUTPUT_FILENAME = "processed_articles_vader.csv" # Use a new name for the output file

def analyze_sentiment_vader(text: str, analyzer: SentimentIntensityAnalyzer) -> float:
    """
    Analyzes the sentiment of a given text using the VADER library.

    Args:
        text: The text content to analyze.
        analyzer: An instance of the SentimentIntensityAnalyzer.

    Returns:
        The compound sentiment score, ranging from -1 (most negative) to 1 (most positive).
    """
    if not isinstance(text, str) or not text.strip():
        return 0.0
        
    # The polarity_scores() method returns a dictionary.
    # The 'compound' score is a single, normalized metric.
    sentiment_dict = analyzer.polarity_scores(text)
    return sentiment_dict['compound']

def categorize_sentiment(score: float) -> str:
    """
    Categorizes a sentiment score into 'Positive', 'Negative', or 'Neutral'.
    (This function is the same as before, but we use a wider threshold for VADER)
    
    Args:
        score: The sentiment score.

    Returns:
        The sentiment category as a string.
    """
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# --- Main Script Logic ---
if __name__ == "__main__":
    print(f"🚀 Starting sentiment analysis process with VADER for '{INPUT_FILENAME}'...")

    if not os.path.exists(INPUT_FILENAME):
        print(f"❌ Error: Input file not found at '{INPUT_FILENAME}'. Please run collect_data.py first.")
        exit()

    # 1. Load the raw data
    df = pd.read_json(INPUT_FILENAME)
    print(f"✅ Loaded {len(df)} articles from '{INPUT_FILENAME}'.")

    # 2. Initialize the VADER analyzer
    vader_analyzer = SentimentIntensityAnalyzer()
    print("✅ VADER sentiment analyzer initialized.")

    # 3. Apply the sentiment analysis function to each article
    print("\nAnalyzing article sentiments with VADER...")
    # The .apply() method is an efficient way to process each row
    df['sentiment_score'] = df.apply(
        lambda row: analyze_sentiment_vader(f"{row['title']}. {row['body']}", vader_analyzer),
        axis=1
    )
    print("✅ Sentiment scores calculated.")

    # 4. Categorize the sentiment based on the score
    df['sentiment_category'] = df['sentiment_score'].apply(categorize_sentiment)
    print("✅ Sentiment categories assigned.")

    # 5. Save the enriched DataFrame to a new CSV file
    try:
        df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
        print(f"\n🎉 Success! Enriched data saved to '{OUTPUT_FILENAME}'.")
    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")