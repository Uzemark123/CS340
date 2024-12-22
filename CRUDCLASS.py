#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:46:27 2024

@author: ubaidahallahk_snhu
"""
from collections import Counter
from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        self.USER = 'aacuser'
        self.PASS = 'SNHU1234'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 32420
        DB = 'AAC'
        COL = 'animals'

        self.client = None
        self.database = None
        self.collection = None

    def authenticate(self, username, password):

        if username == self.USER and password == self.PASS:
            self.connect_to_mongo()  # Establish the MongoDB connection
            print("Login successful! You are connected to MongoDB.")
            return True
        else:
            print("Invalid username or password.")
            return False

    def connect_to_mongo(self):
        """ Establish MongoDB connection after successful authentication """
        if self.client is None:  # Check if a connection already exists
            self.client = MongoClient(
                'mongodb://%s:%s@%s:%d' % (self.USER, self.PASS,
                                           'nv-desktop-services.apporto.com', 32420)
            )
            self.database = self.client['AAC']
            self.collection = self.database['animals']
            print(
                "MongoDB connection established. You can now proceed with CRUD operations.")

    def create(self, data):
        if data is not None:
            try:  # Attempt to insert the data into the 'animals' collection
                result = self.database.animals.insert_one(
                    data)  # data should be dictionary

                # Check if the insert operation was acknowledged by MongoDB
                if result.acknowledged:
                    return True
                else:
                    return False
            except Exception as e:   # Handle any exceptions that occur during the insert operation
                print(f"Error inserting document: {e}")
                return False

        else:  # Raise an exception if no data is provided
            raise Exception("Nothing to save, because data parameter is empty")

    def query(self, query, projection=None):
        try:
            # Executes a query to find documents returns a cursor
            cursor = self.collection.find(query, projection)

            # Convert the cursor to a list of documents
            result = list(cursor)

            if result:
                return result
            else:
                return []
        except Exception as e:
            # Print any errors that occur
            print(f"Error querying documents: {e}")
            return []  # Return an empty list if an exception occurs

    def update(self, dbquery, dbupdate):
        try:
            # Check if the inputs are valid (non-empty dictionaries)
            if not dbquery or not isinstance(dbquery, dict):
                raise ValueError("dbquery must be a non-empty dictionary")
            if not dbupdate or not isinstance(dbupdate, dict):
                raise ValueError("dbupdate must be a non-empty dictionary")

            # Perform the update operation
            result = self.collection.update_many(dbquery, dbupdate)

            # Check if any documents were modified
            if result.modified_count > 0:
                return result.modified_count
            else:
                return "No record found matching the query"

        except ValueError as ve:
            print(f"ValueError: {ve}")
            return 0  # Return 0 to indicate no documents were updated
        except Exception as e:
            print(f"Error occurred while updating documents: {e}")
            return 0  # Return 0 to indicate no documents were updated

    def delete(self, dbdelete):
        try:
            # Check if the input is valid (non-empty dictionary)
            if not dbdelete or not isinstance(dbdelete, dict):
                raise ValueError("dbdelete must be a non-empty dictionary")

            # Perform the delete operation
            result = self.collection.delete_many(dbdelete)

            return result.deleted_count

        except ValueError as ve:
            print(f"ValueError: {ve}")
            return 0  # Return 0 to indicate no documents were deleted
        except Exception as e:
            print(f"Error occurred while deleting documents: {e}")
            return 0  # Return 0 to indicate no documents were deleted

    def query_water_rescue(self):
        query = {
        "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
        "sex_upon_outcome": "Intact Female",
        "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
    
        try:
            # Call the query method with the specific parameters
            result = self.query(query)
            return result
        except Exception as e:
            # Handle exceptions and print error message
            print(f"Error in query_water_rescue: {e}")
            return []  # Return an empty list if an exception occurs

    def query_mountain_rescue(self):
        query = {
            "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
    
        try:
            # Call the query method with the specific parameters
            result = self.query(query)
            return result
        except Exception as e:
            # Handle exceptions and print error message
            print(f"Error in query_mountain_rescue: {e}")
            return []  # Return an empty list if an exception occurs

    def query_disaster_rescue(self):
        query = {
            "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}
        }
        
        try:
            # Call the query method with the specific parameters
            result = self.query(query)
            return result
        except Exception as e:
            # Handle exceptions and print error message
            print(f"Error in query_disaster_rescue: {e}")
            return []  # Return an empty list if an exception occurs
