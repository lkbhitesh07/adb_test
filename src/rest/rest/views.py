from bson import ObjectId
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from pymongo import MongoClient

# Define constants and configuration
MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"
DATABASE_NAME = 'test_db'
COLLECTION_NAME = 'todo'
TODO_DOCUMENT_ID = 'todo_id'

class TodoListView(APIView):

    def get(self, request):
        """
        Retrieve all todo items from the MongoDB collection.
        """
        # Connect to the MongoDB database
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        db_todo_collection = db[COLLECTION_NAME]

        # Query the document with a custom_id
        query = {'custom_id': TODO_DOCUMENT_ID}
        document = db_todo_collection.find_one(query)

        # Return the todo items as a JSON response
        if document:
            todo_data = document['todo_items']
            return Response({'todo_data': todo_data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No todo items found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        Add a new todo item to the MongoDB collection.
        """
        try:
            # Extract the todo item from the request data
            todo_to_be_added = request.data.get('todo')

            # Connect to the MongoDB database
            client = MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            db_todo_collection = db[COLLECTION_NAME]

            # Query the document with a custom_id
            query = {'custom_id': TODO_DOCUMENT_ID}
            document = db_todo_collection.find_one(query)

            if document:
                # If the document exists, update the todo items
                updated_todo_items = document['todo_items']
                updated_todo_items.append(todo_to_be_added)

                # Update the existing document
                query = {
                    'custom_id': TODO_DOCUMENT_ID,
                }
                updated_values = {
                    'custom_id': TODO_DOCUMENT_ID,
                    'todo_items': updated_todo_items
                }
                db_todo_collection.update_one(query, {'$set': updated_values})
            else:
                # If the document does not exist, create a new one
                data_to_insert = {
                    'custom_id': TODO_DOCUMENT_ID,
                    'todo_items': [todo_to_be_added]
                }
                db_todo_collection.insert_one(data_to_insert)

            return Response(
                {
                    'message': 'Data added successfully.',
                    'data': todo_to_be_added
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            error_message = str(e)
            return Response(
                {'message': error_message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
