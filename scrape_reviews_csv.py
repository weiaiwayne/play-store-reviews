#!/usr/bin/env python3
import csv
import json
import time
from datetime import datetime
from google_play_scraper import app, reviews, Sort
import argparse

def scrape_app_reviews(app_id, lang='en', country='us', max_reviews=10000, output_file=None):
    """
    Scrape reviews for a Google Play Store app and save as CSV.
    
    Args:
        app_id: The app's package name (e.g., 'com.whatsapp')
        lang: Language code (default: 'en')
        country: Country code (default: 'us')
        max_reviews: Maximum number of reviews to fetch (default: 10000)
        output_file: Output CSV file path (optional)
    """
    
    print(f"Fetching app info for: {app_id}")
    try:
        app_info = app(app_id, lang=lang, country=country)
        print(f"App: {app_info['title']}")
        print(f"Developer: {app_info['developer']}")
        print(f"Rating: {app_info['score']}")
        print(f"Reviews count: {app_info['reviews']}")
    except Exception as e:
        print(f"Error fetching app info: {e}")
        return None

    print(f"\nFetching up to {max_reviews} reviews...")
    start_time = time.time()
    
    all_reviews = []
    continuation_token = None
    batch_size = 200  # Reviews per batch
    
    try:
        while len(all_reviews) < max_reviews:
            remaining = min(batch_size, max_reviews - len(all_reviews))
            print(f"Fetching batch... (total so far: {len(all_reviews)})")
            
            result, continuation_token = reviews(
                app_id,
                lang=lang,
                country=country,
                sort=Sort.NEWEST,
                count=remaining,
                continuation_token=continuation_token
            )
            
            if not result:
                print("No more reviews available")
                break
                
            all_reviews.extend(result)
            
            if not continuation_token:
                print("No more reviews available (no continuation token)")
                break
                
            # Be respectful to the server
            time.sleep(0.5)
        
        end_time = time.time()
        print(f"Fetched {len(all_reviews)} reviews in {end_time - start_time:.2f} seconds")
        
        # Save to CSV
        if not output_file:
            output_file = f"{app_id}_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'reviewId', 'userName', 'content', 'score', 'thumbsUpCount',
                'reviewCreatedVersion', 'at', 'replyContent', 'repliedAt'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for review in all_reviews:
                writer.writerow({
                    'reviewId': review['reviewId'],
                    'userName': review['userName'],
                    'content': review['content'],
                    'score': review['score'],
                    'thumbsUpCount': review['thumbsUpCount'],
                    'reviewCreatedVersion': review['reviewCreatedVersion'],
                    'at': review['at'].isoformat() if review['at'] else '',
                    'replyContent': review['replyContent'] or '',
                    'repliedAt': review['repliedAt'].isoformat() if review['repliedAt'] else ''
                })
        
        print(f"Reviews saved to: {output_file}")
        
        # Show statistics
        if all_reviews:
            ratings = [r['score'] for r in all_reviews]
            avg_rating = sum(ratings) / len(ratings)
            print(f"Average rating: {avg_rating:.2f}")
            
            rating_counts = {}
            for rating in ratings:
                rating_counts[rating] = rating_counts.get(rating, 0) + 1
            
            print("Rating distribution:")
            for rating in sorted(rating_counts.keys()):
                print(f"  {rating} stars: {rating_counts[rating]} reviews")
        
        return all_reviews
        
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Scrape Google Play Store app reviews to CSV')
    parser.add_argument('app_id', help='App package name (e.g., com.whatsapp)')
    parser.add_argument('--lang', default='en', help='Language code (default: en)')
    parser.add_argument('--country', default='us', help='Country code (default: us)')
    parser.add_argument('--max-reviews', type=int, default=10000, help='Maximum reviews to fetch (default: 10000)')
    parser.add_argument('--output', help='Output CSV file path')
    
    args = parser.parse_args()
    
    reviews_data = scrape_app_reviews(
        args.app_id, 
        args.lang, 
        args.country, 
        args.max_reviews,
        args.output
    )
    
    if reviews_data:
        print(f"\nScraping completed successfully! Total reviews: {len(reviews_data)}")
    else:
        print("Scraping failed!")

if __name__ == "__main__":
    main()