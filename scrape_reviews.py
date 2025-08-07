#!/usr/bin/env python3
import json
import time
from datetime import datetime
from google_play_scraper import app, reviews_all
import argparse

def scrape_app_reviews(app_id, lang='en', country='us', output_file=None):
    """
    Scrape all available reviews for a Google Play Store app.
    
    Args:
        app_id: The app's package name (e.g., 'com.whatsapp')
        lang: Language code (default: 'en')
        country: Country code (default: 'us')
        output_file: Output file path (optional)
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

    print("\nFetching all reviews...")
    start_time = time.time()
    
    try:
        # Get all available reviews
        from google_play_scraper import Sort
        all_reviews = reviews_all(
            app_id,
            sleep_milliseconds=100,  # Be respectful to the server
            lang=lang,
            country=country,
            sort=Sort.NEWEST  # Use enum instead of string
        )
        
        end_time = time.time()
        print(f"Fetched {len(all_reviews)} reviews in {end_time - start_time:.2f} seconds")
        
        # Process reviews data
        processed_reviews = []
        for review in all_reviews:
            processed_review = {
                'reviewId': review['reviewId'],
                'userName': review['userName'],
                'userImage': review['userImage'],
                'content': review['content'],
                'score': review['score'],
                'thumbsUpCount': review['thumbsUpCount'],
                'reviewCreatedVersion': review['reviewCreatedVersion'],
                'at': review['at'].isoformat() if review['at'] else None,
                'replyContent': review['replyContent'],
                'repliedAt': review['repliedAt'].isoformat() if review['repliedAt'] else None
            }
            processed_reviews.append(processed_review)
        
        # Create final dataset
        dataset = {
            'app_info': {
                'app_id': app_id,
                'title': app_info['title'],
                'developer': app_info['developer'],
                'score': app_info['score'],
                'reviews_count': app_info['reviews'],
                'scraped_at': datetime.now().isoformat(),
                'scraped_reviews_count': len(processed_reviews)
            },
            'reviews': processed_reviews
        }
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, ensure_ascii=False, indent=2)
            print(f"Reviews saved to: {output_file}")
        
        return dataset
        
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Scrape Google Play Store app reviews')
    parser.add_argument('app_id', help='App package name (e.g., com.whatsapp)')
    parser.add_argument('--lang', default='en', help='Language code (default: en)')
    parser.add_argument('--country', default='us', help='Country code (default: us)')
    parser.add_argument('--output', help='Output JSON file path')
    
    args = parser.parse_args()
    
    output_file = args.output
    if not output_file:
        output_file = f"{args.app_id}_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    dataset = scrape_app_reviews(args.app_id, args.lang, args.country, output_file)
    
    if dataset:
        print("\nScraping completed successfully!")
        print(f"Total reviews scraped: {len(dataset['reviews'])}")
        
        # Show some statistics
        if dataset['reviews']:
            ratings = [r['score'] for r in dataset['reviews']]
            avg_rating = sum(ratings) / len(ratings)
            print(f"Average rating: {avg_rating:.2f}")
            
            rating_counts = {}
            for rating in ratings:
                rating_counts[rating] = rating_counts.get(rating, 0) + 1
            
            print("Rating distribution:")
            for rating in sorted(rating_counts.keys()):
                print(f"  {rating} stars: {rating_counts[rating]} reviews")
    else:
        print("Scraping failed!")

if __name__ == "__main__":
    main()