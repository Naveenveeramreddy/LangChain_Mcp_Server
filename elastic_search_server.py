from elasticsearch import Elasticsearch
from mcp.server.fastmcp import FastMCP
import asyncio
import logging
import uuid
from datetime import datetime

# Connect to your local Elasticsearch
es = Elasticsearch("http://localhost:9200")
mcp = FastMCP("elasticsearch")

@mcp.tool()
async def add_document(document, index: str = "logs", doc_id: str = None):
    """Add a document to Elasticsearch"""
    logging.info("------------------------add_document------------------------------------------")
    try:
        # Handle string input by parsing JSON
        if isinstance(document, str):
            import json
            try:
                document = json.loads(document.replace("'", '"'))  # Fix single quotes
            except json.JSONDecodeError:
                document = {"content": document, "timestamp": datetime.now().isoformat()}
        # Ensure document is not empty
        if not document:
            document = {"empty_document": True, "timestamp": datetime.now().isoformat()}
        if doc_id is None:
            doc_id = str(uuid.uuid4())
        logging.info(f"Final document to index: {document}")
        result = es.index(index=index, document=document, id=doc_id)
        logging.info(f"Elasticsearch result: {result}")
        return "Document added successfully"
    except Exception as e:
        logging.error(f"Error: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def update_document(doc_id, document, index = "logs"):
    """Update an existing document"""
    logging.info("------------------------update_document------------------------------------------")
    try:
        a = es.update(index=index, id=doc_id, doc=document)
        logging.info(f"Elasticsearch result: {a}")
        return "Document updated successfully"
    except Exception as e:
        logging.error(f"Error: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def delete_document(doc_id, index = "logs"):
    """Delete a document by ID"""
    logging.info("------------------------delete_document------------------------------------------")
    try:
        a = es.delete(index=index, id=doc_id)
        logging.info(f"Elasticsearch result: {a}")
        return "Document deleted successfully"
    except Exception as e:
        logging.error(f"Error: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def show_documents(index = "logs", query=None):
    """Show documents from index with optional query"""
    logging.info("------------------------show_documents------------------------------------------")
    try:
        if query:
            a =  es.search(index=index, query=query)
        a = es.search(index=index, query={"match_all": {}})
        logging.info(f"Elasticsearch result: {a}")
        return "Extracted document successfully"
    except Exception as e:
        logging.error(f"Error: {e}")
        return f"Error: {str(e)}"

def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
