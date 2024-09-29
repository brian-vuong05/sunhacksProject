import json
from pymongo import MongoClient
import asyncio

# MongoDB connection string
MONGODB_URI = 'mongodb+srv://Brian:Password123@cluster0.rbw81.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
async def read_reviews_from_mongodb():
    client = MongoClient(MONGODB_URI)
    try:
        database = client['reviewsDB']
        collection = database['yelpReviews']
        # Query to fetch all reviews
        reviews_cursor = collection.find({})

        # Parse the reviews into a list
        reviews = []
        for review in reviews_cursor:
            parsed_review = {
                'business_name': review.get('business_name', 'No business name available'),
                'review_text': review.get('review_text', 'No review text available'),
                'rating': review.get('rating', 'No rating available'),
                'user_name': review.get('user_name', 'Anonymous'),
                'date': review.get('date', 'No date available'),
                'location': review.get('location', 'No location available'),
                'place_id': review.get('place_id', 'No place ID available')
            }
            reviews.append(parsed_review)

        return reviews
    except Exception as error:
        print('Error reading from MongoDB:', error)
    finally:
        client.close()

async def save_reviews_to_file(file_path: str, data: list[dict]):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        print(f"Reviews saved to {file_path}")
    except Exception as error:
        print(f"Error writing to file: {file_path}", error)

async def read_reviews_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reviews_array = json.load(file)
        return reviews_array
    except Exception as error:
        print(f"Error reading from file: {file_path}", error)

async def get_data(file_path):
    # Step 1: Read reviews from MongoDB and save to JSON file
    reviews = await read_reviews_from_mongodb()
    print(reviews)
    if not reviews:
        print('No reviews found.')
        return

    #file_path = './data.json'
    await save_reviews_to_file(file_path, reviews)
