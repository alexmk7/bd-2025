#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlalchemy
import random
from sqlalchemy.sql import text

from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from datetime import datetime as dt

es = Elasticsearch("http://elasticsearch:9200")
engine = sqlalchemy.create_engine(
    "postgresql+psycopg://user1:password1@db:5432/mydb"
)
app = Flask(__name__)


#NB: DONT USE IT IN REAL LIFE!!!
@app.route("/db")
def db():
    with engine.begin() as conn:
        conn.execute(
            text(
            """
                CREATE TABLE IF NOT EXISTS my_table(
                    name VARCHAR(40),
                    age INT
                );
            """
            )
        )

        conn.execute(
            text(
                """
                    INSERT INTO my_table (name, age) VALUES (:name, :age);
                """
            ), {
                "name": str(dt.now()),
                "age": random.randint(20, 40),
            } 
        )

        return [
            (row.name, row.age)
            for row in conn.execute(text("""SELECT * FROM my_table;"""))
        ]


#NB: DONT USE IT IN REAL LIFE!!!
@app.route("/add")
def add():
    text = request.args.get("text", "") # VERY BAD

    doc = {"title": str(dt.now()), "text": text}

    res = es.index(index="test-index", body=doc)
    return jsonify(res.body)


@app.route("/search")
def search():
    text = request.args.get("text", "")

    res = es.search(index="test-index", body={"query": {"match": {"text": text}}})
    return jsonify(res.body)


app.run("0.0.0.0", port=8989, debug=True)
