from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#create a flask
app = Flask(__name__)

#use PyMongo to establish mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#route to render index.html template using data from Mongo
@app.route("/")
def home():

    #find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()

    #return template and data
    return render_template("index.html", Mars=destination_data)


#route that will trigger the scrape
@app.route("/scrape")
def scrape():

    #run the scrape
    mars_data = scrape_mars.Scrape_All()

    #update the Mongo database using update and upsert=True
    mongo.db.collection.update_one({}, {"$set": mars_data}, upsert=True)

    #redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
