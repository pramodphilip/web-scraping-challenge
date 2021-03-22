from flask import Flask, render_template
import pymongo
import scrape_mars 

app = Flask(__name__,template_folder='templates')

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db

@app.route("/")
def home():
    facts = db.mars.find()
    return render_template("index.html",facts=facts)

@app.route("/scrape")
def scraper():
    db.mars.drop()

    info = scrape_mars.scrape()

    db.mars.insert(info)
    

if __name__ == "__main__":
    app.run(debug=True)
