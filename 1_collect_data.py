import requests
import json
import time
import os
from dotenv import load_dotenv

# --- Load environment variables from the .env file ---
load_dotenv()

# --- Configuration ---
# Securely get the API key from environment variables
API_KEY = os.getenv("NEWSAPI_AI_KEY")
API_URL = "https://eventregistry.org/api/v1/article/getArticles"

# Check if the API key was loaded
if not API_KEY:
    print("❌ Error: API key not found. Please ensure your .env file contains 'NEWSAPI_AI_KEY=YOUR_KEY'.")
    exit() # Exit the script if the key is missing

# Define the search parameters based on your requirements
# 💡 Replace "New Fictional Product" with the actual product name or search term.
#    For exact phrases, wrap in quotes: e.g., "\"Aperture Science Portal Gun\""
KEYWORD = "iPhone 17" 
START_DATE = "2025-09-22"
END_DATE = "2025-10-05"
SOURCE_LOCATION_URI = "http://en.wikipedia.org/wiki/United_States" # URI for the US
ARTICLES_PER_PAGE = 100 # Maximum allowed by the API

def fetch_all_articles():
    """
    Fetches articles page by page from NewsAPI.ai and saves them to a JSON file.
    """
    print("🚀 Starting data collection process...")

    all_articles = []
    current_page = 1
    
    while True:
        print(f"Fetching page {current_page}...")
        
        payload = {
            "action": "getArticles",
            "keyword": KEYWORD,
            "lang": "eng", # Specify English language
            "articlesPage": current_page,
            "articlesCount": ARTICLES_PER_PAGE,
            "articlesSortBy": "date",
            "articlesSortByAsc": False,
            "articlesArticleBodyLen": -1, # Get the full body of the article
            "resultType": "articles",
            "dataType": ["news", "pr"], # Search for news and press releases
            "apiKey": API_KEY,
            "forceMaxDataTimeWindow": 31,
            "dateStart": START_DATE,
            "dateEnd": END_DATE,
            "sourceLocationUri": SOURCE_LOCATION_URI
        }
        
        try:
            response = requests.get(API_URL, params=payload)
            
            # Check for a successful response (HTTP 200)
            if response.status_code != 200:
                print(f"❌ Error: Received status code {response.status_code}")
                print(f"Response: {response.text}")
                break
                
            data = response.json()
            articles_on_page = data.get("articles", {}).get("results", [])
            
            # If the current page has no articles, we've reached the end
            if not articles_on_page:
                print("✅ No more articles found. Reached the last page.")
                break
            
            all_articles.extend(articles_on_page)
            print(f"Found {len(articles_on_page)} articles on this page. Total collected: {len(all_articles)}")
            
            current_page += 1
            time.sleep(1) # Be polite to the API, wait 1 second between requests

        except requests.exceptions.RequestException as e:
            print(f"❌ A network error occurred: {e}")
            break
        except json.JSONDecodeError:
            print("❌ Failed to decode JSON from response. The API might be down or returned an error page.")
            break
            
    # --- Save the collected data ---
    if all_articles:
        output_filename = "raw_articles.json"
        print(f"\n💾 Saving {len(all_articles)} articles to {output_filename}...")
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(all_articles, f, indent=4, ensure_ascii=False)
        print("🎉 Data collection complete and saved successfully!")
    else:
        print("\n🤷 No articles were found for the given criteria.")

# --- Run the main function ---
if __name__ == "__main__":
    fetch_all_articles()