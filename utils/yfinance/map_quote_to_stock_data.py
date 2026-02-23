from utils.formatting.format_compact_number import format_compact_number
from utils.formatting.truncate_two_decimals import truncate_two_decimals


def map_quote_to_stock_data(quote, rank):
    symbol = quote.get("symbol", "N/A")
    return {
        "rank": rank,
        "company_name": quote.get("shortName", symbol),
        "symbol": symbol,
        "current_price": truncate_two_decimals(quote.get("regularMarketPrice", "N/A")),
        "market_cap": format_compact_number(quote.get("marketCap", "N/A")),
        "company_revenue": format_compact_number(
            quote.get("totalRevenue", quote.get("annualRevenue", quote.get("revenue", "N/A")))
        ),
        "pe_ratio": truncate_two_decimals(quote.get("trailingPE", "N/A")),
    }
