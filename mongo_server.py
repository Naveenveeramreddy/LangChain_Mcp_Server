from pymongo import MongoClient
from mcp.server.fastmcp import FastMCP
import logging
import json
from datetime import datetime

mcp = FastMCP("mongodb")

# Keep client as global to maintain connection
client = None

def connect_mongodb():
    global client
    try:
        if client is None:
            client = MongoClient("mongodb://localhost:27017/")
        db = client["myDatabase"]
        return db["customers"]
    except Exception as e:
        return None

@mcp.tool()
async def add_customer_data(customer) -> str:
    logging.info("---------------------------------------------------")
    logging.info("Processing request add_customer_data")
    collection = connect_mongodb()
    if collection is None:
        return "No database connection"
    result = collection.insert_one(customer)
    return "Inserted id: {}".format(result.inserted_id)

@mcp.tool()
async def add_conversation_data(user_content: str, ai_content: str) -> str:
    logging.info("---------------------------------------------------")
    logging.info("Processing request add_conversation_data")
    collection = connect_mongodb()
    if collection is None:
        return "No database connection"
    conversation = {
        "user_message": user_content,
        "ai_message": ai_content,
        "timestamp": datetime.now()
    }
    result = collection.insert_one(conversation)
    return f"Conversation saved: {result.inserted_id}"

@mcp.tool()
async def get_customer_data(name: str):
    collection = connect_mongodb()
    if collection is None:
        return "No datatbase is found"
    return collection.find_one({"name": name})

def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    # add_customer_data({"name": "John Doe", "age": 30})
    main()
