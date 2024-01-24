from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_tweets(hashtag, tweet_count=20):
    # Initialize the WebDriver with the ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Assuming you have already logged in manually
        # Navigate to the hashtag page
        driver.get(f'https://twitter.com/search?q=%23{hashtag}&src=typed_query&f=live')

        # Collect tweets
        tweets = []
        while len(tweets) < tweet_count:
            # Wait for tweets to be loaded
            WebDriverWait(driver, 100).until(
                EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid="tweet"]'))
            )

            # Find tweet elements
            tweet_elements = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]//div[@lang]')

            # Extract text from each tweet element
            for element in tweet_elements:
                if len(tweets) < tweet_count:
                    tweets.append(element.text)
                else:
                    break

            # Scroll down to load more tweets
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        return tweets

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

# Usage example
tweets = scrape_tweets('BPL2024', 20)
for tweet in tweets:
    print(tweet)
