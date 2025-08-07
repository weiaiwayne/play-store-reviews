#!/usr/bin/env python3
import json
import os
import math

def split_gemini_reviews(input_file, max_size_mb=90):
    """
    Split Gemini reviews JSON file into smaller chunks to stay under GitHub's file size limit.
    
    Args:
        input_file: Path to the large Gemini reviews JSON file
        max_size_mb: Maximum size per chunk in MB (default: 90MB to stay under 100MB limit)
    """
    
    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    app_info = data['app_info']
    reviews = data['reviews']
    total_reviews = len(reviews)
    
    print(f"Total reviews: {total_reviews}")
    
    # Calculate approximate reviews per chunk based on file size
    current_size_mb = os.path.getsize(input_file) / (1024 * 1024)
    reviews_per_chunk = int((max_size_mb / current_size_mb) * total_reviews)
    num_chunks = math.ceil(total_reviews / reviews_per_chunk)
    
    print(f"Current file size: {current_size_mb:.1f}MB")
    print(f"Target chunk size: {max_size_mb}MB")
    print(f"Reviews per chunk: {reviews_per_chunk}")
    print(f"Number of chunks: {num_chunks}")
    
    # Split reviews into chunks
    for chunk_num in range(num_chunks):
        start_idx = chunk_num * reviews_per_chunk
        end_idx = min((chunk_num + 1) * reviews_per_chunk, total_reviews)
        chunk_reviews = reviews[start_idx:end_idx]
        
        # Create chunk data structure
        chunk_data = {
            'app_info': {
                **app_info,
                'chunk_info': {
                    'chunk_number': chunk_num + 1,
                    'total_chunks': num_chunks,
                    'reviews_in_chunk': len(chunk_reviews),
                    'review_range': f"{start_idx + 1}-{end_idx}"
                }
            },
            'reviews': chunk_reviews
        }
        
        # Save chunk
        chunk_filename = f"gemini_reviews_part_{chunk_num + 1:02d}_of_{num_chunks:02d}.json"
        with open(chunk_filename, 'w', encoding='utf-8') as f:
            json.dump(chunk_data, f, ensure_ascii=False, indent=2)
        
        chunk_size_mb = os.path.getsize(chunk_filename) / (1024 * 1024)
        print(f"Created {chunk_filename}: {len(chunk_reviews)} reviews, {chunk_size_mb:.1f}MB")
    
    print(f"\nSuccessfully split {total_reviews} reviews into {num_chunks} chunks")
    return num_chunks

if __name__ == "__main__":
    split_gemini_reviews("gemini_reviews.json")