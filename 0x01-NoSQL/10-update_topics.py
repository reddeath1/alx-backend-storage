#!/usr/bin/env python3
"""
Changes all topics of  schooll document based on the name
Prototype: def update_topics(mongo_collection, name, topics):
mongo_collection will be the pymongo object
name (String) will be the school name to update
topics (list of strings) will be the list of topics in the school
"""


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
