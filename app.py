# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    news_title = scrape_mars.find_latest_news_title()
    news_description = scrape_mars.find_latest_news_description()
    feature_image = scrape_mars.find_feature_image()
    weather = scrape_mars.find_most_recent_weather_tweet()

    # Store results into a dictionary
    mars = {
        "title": news_title,
        "description": news_description,
        "feature_image": feature_image,
        "weather": weather
    }

    # Insert forecast into database
    mongo.db.collection.insert_one(mars)

    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
