from kiteconnect import KiteConnect
import logging
from mcp.server.fastmcp import FastMCP
import netrc
import os

# Initialize FastMCP server
mcp = FastMCP("stocks")

netrc_path = os.path.abspath('./.netrc')
secrets = netrc.netrc(netrc_path)
secret_configuration = secrets.authenticators('stocks.data')
kite = KiteConnect(api_key=secret_configuration[0])

kite.set_access_token(secret_configuration[1])

def format_holdings(x: dict) -> str:
    return f"""
tradingsymbol: {x.get('tradingsymbol')}
instrument_token: {x.get('instrument_token')}
isin: {x.get('isin')}
quantity: {x.get('quantity')}
average_price: {x.get('average_price')}
last_price: {x.get('last_price')}
close_price: {x.get('close_price')}
pnl: {x.get('pnl')}
day_change_percentage: {x.get('day_change_percentage')}
"""

@mcp.tool()
async def get_holdings(**kwargs) -> str:
    """Get holdings from the Kite account."""
    logging.info("---------------------------------------------------")
    logging.info("Processing request")

    try:
        holdings = kite.holdings() + kite.mf_holdings()
    except Exception as e:
        logging.error(f"Error fetching holdings: {e}")
        return f"❌ Error fetching holdings: {e}"

    if not holdings:
        return "No holdings found."

    list_holdings = [format_holdings(x) for x in holdings]
    logging.info("Holdings fetched successfully.")
    a = "\n---\n".join(list_holdings)
    # logging.info(a)
    return a

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
