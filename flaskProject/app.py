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
    try:
        # Get the business name and location from the form
        business_name = request.form['businessName']
        location = request.form['location']

        # Call your function to scrape and upload to MongoDB
        fetch_yelp_reviews(fetch_yelp_place_id(business_name, location))  # Adjust this if necessary
        get_data()  # Fetch the reviews and create the JSON file

        flash('Reviews fetched and uploaded successfully!', 'success')
    except Exception as e:
        flash(f'Error fetching reviews: {str(e)}', 'danger')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)