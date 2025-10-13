import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Configuration ---
# 💡 Change this to 'processed_articles.csv' if you used the Google API output
INPUT_FILENAME = "processed_articles_vader.csv" 
OUTPUT_CHART_FILENAME = "sentiment_trend_chart.png"

def generate_visuals_and_report():
    """
    Loads processed data, aggregates it by day, creates a trend chart,
    and prints a summary report.
    """
    print(f"🚀 Starting Phase 4: Aggregation and Visualization for '{INPUT_FILENAME}'...")

    # 1. Load the processed data
    if not os.path.exists(INPUT_FILENAME):
        print(f"❌ Error: Input file not found at '{INPUT_FILENAME}'. Please run the analysis script first.")
        return

    df = pd.read_csv(INPUT_FILENAME)
    print(f"✅ Loaded {len(df)} processed articles.")

    # 2. Data Preparation: Convert 'date' column to datetime objects
    # This is crucial for correct time-based sorting and plotting.
    df['date'] = pd.to_datetime(df['date'])
    print("✅ Converted 'date' column to datetime objects.")

    # 3. Aggregation: Group by date and sentiment, then count articles
    # We group by the date part of the datetime and the category.
    # .size() counts the number of articles in each group.
    # .unstack(fill_value=0) pivots the sentiment categories into columns.
    daily_sentiment_counts = df.groupby([df['date'].dt.date, 'sentiment_category']).size().unstack(fill_value=0)
    
    # Ensure all three sentiment columns exist, adding any that are missing with a value of 0
    for sentiment in ['Positive', 'Negative', 'Neutral']:
        if sentiment not in daily_sentiment_counts.columns:
            daily_sentiment_counts[sentiment] = 0
            
    print("✅ Aggregated daily sentiment counts:")
    print(daily_sentiment_counts)

    # 4. Visualization: Create and save the line chart
    print(f"\n📈 Generating plot and saving to '{OUTPUT_CHART_FILENAME}'...")
    
    # Use seaborn for a nice visual style
    sns.set_theme(style="whitegrid", palette="colorblind")
    plt.figure(figsize=(12, 7)) # Set the figure size for better readability

    # Plot each sentiment category as a line
    plt.plot(daily_sentiment_counts.index, daily_sentiment_counts['Positive'], label='Positive', marker='o', linestyle='-')
    plt.plot(daily_sentiment_counts.index, daily_sentiment_counts['Neutral'], label='Neutral', marker='s', linestyle='--')
    plt.plot(daily_sentiment_counts.index, daily_sentiment_counts['Negative'], label='Negative', marker='x', linestyle=':')

    # Add titles and labels for clarity
    plt.title('Daily Media Sentiment Trend for Product Launch', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Articles', fontsize=12)
    
    # Improve date formatting on the x-axis
    plt.xticks(rotation=45, ha="right")
    plt.legend(title='Sentiment')
    plt.tight_layout() # Adjust plot to ensure everything fits without overlapping

    # Save the figure to a file
    plt.savefig(OUTPUT_CHART_FILENAME)
    print("✅ Chart saved successfully.")
    # plt.show() # Uncomment this line if you want to display the plot immediately

    # 5. Reporting: Calculate and print key metrics
    print("\n--- Summary Report ---")
    
    # Overall sentiment distribution
    total_articles = len(df)
    sentiment_distribution = df['sentiment_category'].value_counts()
    sentiment_percentages = df['sentiment_category'].value_counts(normalize=True) * 100
    
    print("\nOverall Sentiment Distribution:")
    for sentiment, count in sentiment_distribution.items():
        print(f"  - {sentiment}: {count} articles ({sentiment_percentages[sentiment]:.2f}%)")
    
    print(f"\nTotal Articles Analyzed: {total_articles}")
    print("\n🎉 Phase 4 complete!")


# --- Run the main function ---
if __name__ == "__main__":
    generate_visuals_and_report()