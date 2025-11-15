LangChain MCP Multi-Server Integration
A comprehensive Model Context Protocol (MCP) implementation that integrates multiple data sources and services with LangChain agents for intelligent data processing and storage.

🚀 Features
Multi-Server Architecture: Weather, Stocks, MongoDB, and Elasticsearch servers
AI Agent Integration: LangChain agent that intelligently uses all available tools
Automatic Data Storage: Conversations and data automatically stored in Elasticsearch
Real-time Data: Live weather alerts and stock portfolio data
Secure Configuration: Credentials managed via .netrc files
📋 Prerequisites
Python 3.8+
Elasticsearch running on localhost:9200
MongoDB running on localhost:27017 (optional)
Kite Connect API account for stock data
LLM API access (OpenAI-compatible endpoint)
🛠️ Installation
Clone the repository:
git clone https://github.com/vamsivenkat987/langchain_mcp_server.git
cd langchain_mcp_server/mcp
Install dependencies:
pip install langchain-mcp-adapters langchain-openai elasticsearch pymongo kiteconnect requests
Start required services:
# Start Elasticsearch
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.11.0

# Start MongoDB (optional)
docker run -d -p 27017:27017 mongo:latest
⚙️ Configuration
Create a .netrc file in the project directory:

machine llm.model
login your_api_key_here
password https://your-llm-endpoint-here

machine stocks.data
login your_kite_api_key
password your_kite_api_secret
account your_kite_access_token
🏃‍♂️ Usage
Quick Start
python3 mcp_client.py
Individual Server Testing
# Test weather server
python3 weather_server.py

# Test stock server
python3 stocks_server.py

# Test Elasticsearch server
python3 elastic_search_server.py

# Test MongoDB server
python3 mongo_server.py
🔧 Available Tools
Weather Server (weather_server.py)
get_alerts(state) - Get active weather alerts for a US state
Uses National Weather Service API
Stock Server (stocks_server.py)
get_holdings() - Retrieve current stock portfolio from Kite Connect
Requires valid Kite Connect session
Elasticsearch Server (elastic_search_server.py)
add_document(document, index, doc_id) - Store documents in Elasticsearch
Automatic timestamp and UUID generation
JSON parsing for string inputs
MongoDB Server (mongo_server.py)
add_conversation_data(user_content, ai_content) - Store conversations
add_customer_data(name, age) - Store customer information
📁 Project Structure
mcp/
├── mcp_client.py              # Main LangChain agent client
├── weather_server.py          # Weather alerts MCP server
├── stocks_server.py           # Stock portfolio MCP server
├── elastic_search_server.py   # Elasticsearch MCP server
├── mongo_server.py            # MongoDB MCP server
├── test_elastic_search.py     # Elasticsearch testing utilities
├── test_kite.py              # Kite Connect authentication flow
├── test_mcp.py               # MCP server testing
├── .netrc                    # API credentials (create this)
├── oneEGaDCA.crt            # SSL certificate
└── README.md                 # This file
🤖 AI Agent Workflow
The LangChain agent follows this workflow:

Process User Query: Understand what the user is asking for
Call Appropriate Tools:
Weather queries → get_alerts(state)
Stock queries → get_holdings()
Provide Natural Response: Answer user's question in plain language
Store Data: Automatically save conversation and data to Elasticsearch
📊 Data Storage
Elasticsearch Indices
conversations - User queries and AI responses
weather - Weather alert data
stocks - Stock portfolio information
customer_data - Customer information
MongoDB Collections
conversations - Chat history
customers - Customer data
🔐 Security Features
Credentials stored in .netrc files (not in code)
SSL certificate support
Environment variable configuration
Secure API token handling
🔍 Example Queries
"Get me the current weather alerts for New York"
"What are my stock holdings?"
"Is there any connection between my stock portfolio and weather in NY?"
"Show me the weather in California and save the data"
🐛 Troubleshooting
Common Issues
Elasticsearch Connection Error

Ensure Elasticsearch is running on localhost:9200
Check if the service is accessible: curl http://localhost:9200
Kite Connect Authentication

Verify API credentials in .netrc
Check if access token is valid (tokens expire daily)
MCP Server Errors

Check server logs for detailed error messages
Ensure all dependencies are installed
LLM Timeout Errors

Increase timeout in mcp_client.py
Try using streaming instead of ainvoke
📝 API Documentation
Weather Server
Endpoint: National Weather Service API
Rate Limits: No authentication required
Data Format: JSON weather alerts
Stock Server
Endpoint: Kite Connect API
Authentication: API key + secret + access token
Rate Limits: As per Zerodha limits
Data Format: Portfolio holdings with P&L
🤝 Contributing
Fork the repository
Create a feature branch
Make your changes
Add tests if applicable
Submit a pull request
🆘 Support
For issues and questions:

Create an issue on GitHub
Check the troubleshooting section
Review server logs for detailed error information
🔄 Version History
v1.0.0 - Initial release with multi-server MCP integration
v1.1.0 - Added automatic data storage and improved error handling
v1.2.0 - Enhanced authentication and security features
