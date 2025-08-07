# Gemini Reviews - Split Files

The Google Gemini app reviews have been split into multiple files due to GitHub's 100MB file size limit.

## File Structure

**Original Data**: 323,069 reviews (155.9MB)  
**Split into**: 2 chunks

### Files:
- `gemini_reviews_part_01_of_02.json` - Reviews 1-186,543 (89.0MB)
- `gemini_reviews_part_02_of_02.json` - Reviews 186,544-323,069 (66.9MB)

## File Format

Each chunk maintains the same JSON structure as other review files:

```json
{
  "app_info": {
    "app_id": "com.google.android.apps.bard",
    "title": "Google Gemini",
    "developer": "Google LLC",
    "score": 4.5434294,
    "reviews_count": 67261,
    "scraped_at": "2025-08-06T22:36:27.486374",
    "scraped_reviews_count": 323069,
    "chunk_info": {
      "chunk_number": 1,
      "total_chunks": 2,
      "reviews_in_chunk": 186543,
      "review_range": "1-186543"
    }
  },
  "reviews": [...]
}
```

## Usage

To combine all chunks back into a single dataset:

```python
import json

all_reviews = []
chunk_files = [
    "gemini_reviews_part_01_of_02.json",
    "gemini_reviews_part_02_of_02.json"
]

for chunk_file in chunk_files:
    with open(chunk_file, 'r', encoding='utf-8') as f:
        chunk_data = json.load(f)
        all_reviews.extend(chunk_data['reviews'])

# Use the app_info from the first chunk (without chunk_info)
with open(chunk_files[0], 'r', encoding='utf-8') as f:
    first_chunk = json.load(f)
    app_info = first_chunk['app_info'].copy()
    del app_info['chunk_info']  # Remove chunk-specific info

complete_dataset = {
    'app_info': app_info,
    'reviews': all_reviews
}
```

## Split Script

The splitting was done using `split_gemini_reviews.py` with a target chunk size of 90MB to ensure files stay well under GitHub's 100MB limit.