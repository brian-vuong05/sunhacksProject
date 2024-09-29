from flask import Flask, render_template, request, redirect, url_for, flash
from collections import Counter

from requests import request

from fetch_reviews import fetch_yelp_place_id, fetch_yelp_reviews
from pull_reviews import get_data
import json
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)


@app.route('/')
def index():
    # Load data from JSON file
    reviews = load_data()

    # Count the occurrences of each rating
    rating_counts = Counter(review['rating'] for review in reviews)

    # Prepare data for the chart
    labels = list(range(1, 6))  # 1 to 5 stars
    data = [rating_counts[i] for i in labels]

    return render_template('index.html', labels=labels, data=data)

@app.route('/fetch_reviews', methods=['POST'])
def fetch_reviews():
    business_name = request.form.get('businessName')  # Get the business name from the form
    location = request.form.get('location')  # Get the location from the form

    if business_name and location:
        try:
            # Call your function to scrape and upload to MongoDB
            place_id = fetch_yelp_place_id(business_name, location)  # Adjust this function as needed
            fetch_yelp_reviews(place_id)  # Fetch reviews using the place ID
            get_data()  # Fetch the reviews and create the JSON file
            flash('Reviews fetched and uploaded successfully!', 'success')
        except Exception as e:
            flash(f'Error fetching reviews: {str(e)}', 'danger')
    else:
        flash('Please provide both business name and location!', 'danger')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)