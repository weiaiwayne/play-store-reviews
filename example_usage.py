#!/usr/bin/env python3
"""
Example usage of the Google Play Store review scraper.
"""

from scrape_reviews import scrape_app_reviews

# Example 1: Scrape WhatsApp reviews
print("Example 1: Scraping WhatsApp reviews...")
whatsapp_reviews = scrape_app_reviews(
    app_id='com.whatsapp',
    lang='en',
    country='us',
    output_file='whatsapp_reviews.json'
)

# Example 2: Scrape Instagram reviews
print("\nExample 2: Scraping Instagram reviews...")
instagram_reviews = scrape_app_reviews(
    app_id='com.instagram.android',
    lang='en',
    country='us',
    output_file='instagram_reviews.json'
)

# Example 3: Scrape reviews in different language/country
print("\nExample 3: Scraping TikTok reviews in Spanish...")
tiktok_reviews = scrape_app_reviews(
    app_id='com.zhiliaoapp.musically',
    lang='es',
    country='es',
    output_file='tiktok_reviews_es.json'
)

print("\nAll examples completed!")