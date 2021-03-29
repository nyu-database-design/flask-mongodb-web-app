#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
import pymongo
import datetime
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

#import cgitb
#cgitb.enable()

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# grab database credentials from environment variables
mongo_host = os.getenv('MONGO_HOST')
mongo_user = os.getenv('MONGO_USER')
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_dbname = os.getenv('MONGO_DBNAME')

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/read')
def read():
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
    return render_template('create.html')


@app.route('/create', methods=['POST'])
def create_post():
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
    connection = pymongo.MongoClient(mongo_host, 27017, username=mongo_user,
                                     password=mongo_password,
                                     authSource=mongo_dbname)
    collection = connection[mongo_dbname]["exampleapp"]
    doc = collection.find_one({"_id": ObjectId(mongoid)})
    # print(doc)
    return render_template('edit.html',mongoid=mongoid, doc=doc)


@app.route('/edit/<mongoid>', methods=['POST'])
def edit_post(mongoid):
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
