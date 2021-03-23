# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars 

# Creates application
app = Flask(__name__)

# setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Home Route
@app.route("/")
def home():
    # Grabs document from mars collection
    facts = mongo.db.mars.find_one()
    # Renders index.html, includes facts document to be used in index.html
    return render_template("index.html",facts=facts)

# Scrape Route
@app.route("/scrape")
def scraper():

    # Accesses mars collection
    mars = mongo.db.mars

    # Calls scrape function to gather new information
    scrape_data = scrape_mars.scrape()

    # Inserts newly formed dictionary of updated Mars information
    mars.update({}, scrape_data, upsert=True)

    # Returns to home route
    return redirect("/", code=302)

# Runs application
if __name__ == "__main__":
    app.run(debug=True)
