#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
import pymongo
import datetime
from bson.objectid import ObjectId
import os

# load credentials and configuration options from .env file
import credentials
config = credentials.get()
mongo_host = config['MONGO_HOST']
mongo_user = config['MONGO_USER']
mongo_password = config['MONGO_PASSWORD']
mongo_dbname = config['MONGO_DBNAME']
mode = config['FLASK_ENV']

# instantiate the app
app = Flask(__name__)
# turn on debugging if in development mode
if mode == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

# set up the routes

@app.route('/')
def home():
    """
    Route for the home page
    """
    return render_template('index.html')


@app.route('/read')
def read():
    """
    Route for GET requests to the read page.
    Displays some information for the user with links to other pages.
    """
    connection = pymongo.MongoClient(mongo_host, 27017, 
                                    username=mongo_user,
                                    password=mongo_password,
                                    authSource=mongo_dbname)
    collection = connection[mongo_dbname]["exampleapp"]
    docs = collection.find({})
    rows = []
    for doc in docs:
        rows.append(doc)
    return render_template('read.html', rows=rows)


@app.route('/create')
def create():
    """
    Route for GET requests to the create page.
    Displays a form users can fill out to create a new document.
    """
    return render_template('create.html')


@app.route('/create', methods=['POST'])
def create_post():
    """
    Route for POST requests to the create page.
    Accepts the form submission data for a new document and saves the document to the database.
    """
    name = request.form['fname']
    message = request.form['fmessage']

    connection = pymongo.MongoClient(mongo_host, 27017, username=mongo_user,
                                     password=mongo_password,
                                     authSource=mongo_dbname)
    collection = connection[mongo_dbname]["exampleapp"]
    dt = datetime.datetime.now()
    dt_fmt = dt.strftime("%H:%M on %d %B %Y")
    doc_to_insert = {"name": name, "message": message, "time": dt_fmt}
    collection.insert(doc_to_insert)

    return redirect(url_for('read'))


@app.route('/edit/<mongoid>')
def edit(mongoid):
    """
    Route for GET requests to the edit page.
    Displays a form users can fill out to edit an existing record.
    """
    connection = pymongo.MongoClient(mongo_host, 27017, username=mongo_user,
                                     password=mongo_password,
                                     authSource=mongo_dbname)
    collection = connection[mongo_dbname]["exampleapp"]
    doc = collection.find_one({"_id": ObjectId(mongoid)})
    # print(doc)
    return render_template('edit.html',mongoid=mongoid, doc=doc)


@app.route('/edit/<mongoid>', methods=['POST'])
def edit_post(mongoid):
    """
    Route for POST requests to the edit page.
    Accepts the form submission data for the specified document and updates the document in the database.
    """
    name = request.form['fname']
    message = request.form['fmessage']

    connection = pymongo.MongoClient(mongo_host, 27017, username=mongo_user,
                                     password=mongo_password,
                                     authSource=mongo_dbname)
    collection = connection[mongo_dbname]["exampleapp"]
    dt = datetime.datetime.now()
    dt_fmt = dt.strftime("%H:%M on %d %B %Y")
    doc_to_insert = {"_id": ObjectId(mongoid), "name": name, "message": message, "time": dt_fmt}
    collection.find_one_and_replace({"_id": ObjectId(mongoid)}, doc_to_insert)

    return redirect(url_for('read'))


@app.route('/delete/<mongoid>')
def delete(mongoid):
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the read page.
    """
    connection = pymongo.MongoClient(mongo_host, 27017, username=mongo_user,
                                     password=mongo_password,
                                     authSource=mongo_dbname)
    collection = connection[mongo_dbname]["exampleapp"]
    collection.find_one_and_delete({"_id": ObjectId(mongoid)})
    return redirect(url_for('read'))


if __name__ == "__main__":
    #import logging
    #logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(debug = True)
