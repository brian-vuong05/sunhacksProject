from flask import Flask, render_template
from collections import Counter

from requests import request

from fetch_reviews import fetch_yelp_reviews
from pull_reviews import get_data
import json
import requests

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)