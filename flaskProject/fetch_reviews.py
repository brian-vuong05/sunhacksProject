import requests
from pymongo import MongoClient

# SerpAPI key and MongoDB connection string
SERP_API_KEY = 'de65dd2835925cf6b83f0c60fa0e65c92d7d4621b1ae1a39df5e14a0608d69fa'  # Replace with your actual SerpAPI API key
MONGODB_URI = 'mongodb+srv://ssarvesh20000:DYL0X8ncmkcW30Na@cluster0.rbw81.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'


def fetch_yelp_place_id(business_name, location):
    url = f"https://serpapi.com/search.json?engine=yelp&find_desc={business_name}&find_loc={location}&api_key={SERP_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        organic_results = data.get('organic_results', [])

        if not organic_results:
            print('No businesses found for the given name and location.')
            return None

        business = organic_results[0]
        place_id = business.get('place_ids', [None])[0]

        if place_id:
            print(f"Found place_id for {business['title']}: {place_id}")
            return place_id
        else:
            print('No place_id found for the business.')
            return None
    except Exception as error:
        print('Error fetching Yelp business from SerpAPI:', error)
        return None


def fetch_yelp_reviews(place_id):
    reviews = []
    start = 0

    try:
        while True:
            url = f"https://serpapi.com/search.json?engine=yelp_reviews&place_id={place_id}&start={start}&api_key={SERP_API_KEY}"
            response = requests.get(url)
            data = response.json()

            print('Response from SerpAPI:', data)

            review_results = data.get('reviews', [])
            if not review_results:
                break

            reviews.extend(review_results)
            start += 10

            if 'next' not in data:
                break
    except Exception as error:
        print(f"Error fetching reviews for place_id {place_id}:", error)

    return reviews


def store_reviews_in_mongodb(reviews, business_name, location):
    client = MongoClient(MONGODB_URI)

    try:
        db = client['reviewsDB']
        collection = db['yelpReviews']

        for review in reviews:
            print('Review to be inserted:', review)

            review_document = {
                'business_name': business_name,
                'review_text': review.get('comment', {}).get('text') or review.get('snippet',
                                                                                   'No review text available'),
                'rating': review.get('rating', 'No rating available'),
                'user_name': review.get('user', {}).get('name', 'Anonymous'),
                'date': review.get('date') or review.get('time_created', 'No date available'),
                'location': location,
                'place_id': review.get('place_id', 'No place ID available')
            }

            print('Document to be inserted into MongoDB:', review_document)

            try:
                collection.insert_one(review_document)
                print('Inserted successfully:', review_document)
            except Exception as insert_error:
                print('Error inserting document into MongoDB:', insert_error)

        print(f"{len(reviews)} reviews inserted into MongoDB.")
    except Exception as error:
        print('Error connecting to MongoDB or inserting reviews:', error)
    finally:
        client.close()


def main():
    business_name = 'Donhao'  # Name of the business
    location = 'Danville, CA'  # Location of the business

    # Step 1: Fetch Yelp business place_id
    place_id = fetch_yelp_place_id(business_name, location)

    if not place_id:
        print('Place ID not found. Exiting.')
        return

    # Step 2: Fetch Yelp reviews for the business
    reviews = fetch_yelp_reviews(place_id)

    if not reviews:
        print('No reviews found.')
        return

    # Step 3: Store the reviews in MongoDB
    store_reviews_in_mongodb(reviews, business_name, location)

    print('Reviews successfully fetched and stored.')


if __name__ == "__main__":
    main()