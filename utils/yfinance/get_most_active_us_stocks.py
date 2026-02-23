import yfinance as yf

from utils.const.filters import ALLOWED_US_EXCHANGE_CODES, INFO_ENRICH_LIMIT_FILTER, REGION_FILTER, SCREEN_SIZE_FILTER, TOP_N_FILTER
from utils.formatting.format_compact_number import format_compact_number
from utils.formatting.format_timestamp import format_timestamp
from utils.yfinance.call_tracker.log_yfinance_call import log_yfinance_call
from utils.yfinance.enrich_with_info import enrich_with_info
from utils.yfinance.map_quote_to_stock_data import map_quote_to_stock_data


HIDDEN_RESULT_COLUMNS = {
    "cryptoTradeable",
    "currency",
    "displayName",
    "dividendDate",
    "dividendRate",
    "dividendYield",
    "earningsCallTimestampEnd",
    "earningsCallTimestampStart",
    "earningsTimestamp",
    "earningsTimestampEnd",
    "earningsTimestampStart",
    "exchange",
    "exchangeDataDelayedBy",
    "exchangeTimezoneName",
    "exchangeTimezoneShortName",
    "financialCurrency",
    "fullExchangeName",
    "gmtOffSetMilliseconds",
    "hasPrePostMarketData",
    "ipoExpectedDate",
    "isEarningsDateEstimate",
    "language",
    "longName",
    "market",
    "marketState",
    "messageBoardId",
    "nameChangeDate",
    "prevName",
    "quoteType",
    "region",
}


def _format_volume(value):
    if isinstance(value, (int, float)):
        return f"{int(value):,}"
    return "N/A"


def _format_percent(value):
    if isinstance(value, (int, float)):
        return f"{value:.2f}%"
    return "N/A"


def _extract_rating_tier(rating_value):
    rating_text = str(rating_value or "").strip()
    if "-" not in rating_text:
        return ""
    return rating_text.split("-", 1)[1].strip().lower()


def _extract_rating_score(rating_value):
    rating_text = str(rating_value or "").strip()
    if not rating_text:
        return float("inf")

    prefix = rating_text.split("-", 1)[0].strip()
    try:
        return float(prefix)
    except (TypeError, ValueError):
        return float("inf")


def _volume_value(quote):
    raw = quote.get("regularMarketVolume", quote.get("dayVolume", 0))
    if isinstance(raw, (int, float)):
        return float(raw)
    return 0.0


def _format_quote_value(key, value):
    compact_key_parts = ("cap", "volume", "shares", "revenue")
    key_text = str(key).lower()

    timestamp_like_key = (
        "timestamp" in key_text
        or "date" in key_text
        or key_text.endswith("time")
    )

    if timestamp_like_key:
        return format_timestamp(value)

    if isinstance(value, (int, float)) and any(part in key_text for part in compact_key_parts):
        return format_compact_number(value)
    return value


def get_most_active_us_stocks(
    top_n=TOP_N_FILTER,
    screen_size=SCREEN_SIZE_FILTER,
    verify_with_info=False,
    info_enrich_limit=INFO_ENRICH_LIMIT_FILTER,
    analyst_rating_filter=None,
    include_next_tier_down=False,
):
    log_yfinance_call("yf.screen(query='most_actives')")
    result = yf.screen("most_actives", count=max(screen_size, top_n))

    quotes = result.get("quotes", [])
    us_exchange_quotes = [
        quote
        for quote in quotes
        if str(quote.get("exchange", "")).upper() in ALLOWED_US_EXCHANGE_CODES
    ]

    analyst_filter_display = analyst_rating_filter or "N/A"

    if analyst_rating_filter:
        requested_rating = str(analyst_rating_filter).strip()
        base_tier = _extract_rating_tier(requested_rating)
        allowed_tiers = {base_tier} if base_tier else set()

        if include_next_tier_down:
            tier_order = {
                "strong buy": "buy",
                "buy": "hold",
                "hold": "underperform",
                "underperform": "sell",
            }
            next_tier = tier_order.get(base_tier)
            if next_tier:
                allowed_tiers.add(next_tier)

        us_exchange_quotes = [
            quote
            for quote in us_exchange_quotes
            if _extract_rating_tier(quote.get("averageAnalystRating", "")) in allowed_tiers
        ]

        tier_rank = {"strong buy": 0, "buy": 1, "hold": 2, "underperform": 3, "sell": 4}

        analyst_filter_display = " | ".join(
            tier.title()
            for tier in sorted(
                allowed_tiers,
                key=lambda tier: tier_rank.get(tier, 99),
            )
        )

        us_exchange_quotes.sort(
            key=lambda quote: (
                tier_rank.get(_extract_rating_tier(quote.get("averageAnalystRating", "")), 99),
                _extract_rating_score(quote.get("averageAnalystRating", "")),
                -_volume_value(quote),
            )
        )
    else:
        us_exchange_quotes.sort(key=lambda quote: -_volume_value(quote))

    if not us_exchange_quotes:
        raise ValueError("No US most-active stocks were returned by the screener.")

    quote_keys = sorted(
        {
            key
            for quote in us_exchange_quotes[:top_n]
            for key in quote.keys()
        }
    )
    visible_quote_keys = [key for key in quote_keys if key not in HIDDEN_RESULT_COLUMNS]
    hidden_quote_keys = [key for key in quote_keys if key in HIDDEN_RESULT_COLUMNS]

    ranked_stocks = []
    for idx, quote in enumerate(us_exchange_quotes[:top_n], start=1):
        stock_row = map_quote_to_stock_data(quote, rank=idx)
        for key in quote_keys:
            stock_row[key] = _format_quote_value(key, quote.get(key, "N/A"))

        stock_row["price"] = stock_row.get("current_price", "N/A")
        stock_row["change_percent"] = _format_percent(quote.get("regularMarketChangePercent", "N/A"))
        stock_row["activity_volume"] = _format_volume(
            quote.get("regularMarketVolume", quote.get("dayVolume", "N/A"))
        )
        stock_row["avg_volume_3m"] = _format_volume(quote.get("averageDailyVolume3Month", "N/A"))

        if verify_with_info and idx <= info_enrich_limit:
            stock_row = enrich_with_info(stock_row, quote)

        ranked_stocks.append(stock_row)

    return {
        "top_n": top_n,
        "region_filter": REGION_FILTER.upper(),
        "industry_filter": "Most Active (Yahoo preset)",
        "min_market_cap_filter": "N/A",
        "sorting_field": "Analyst Rating Strength then Regular Market Volume"
        if analyst_rating_filter
        else "Regular Market Volume",
        "sorting_direction": "Strongest tier first, then ascending score, then descending volume"
        if analyst_rating_filter
        else "Descending",
        "analyst_rating_filter": analyst_filter_display,
        "analyst_rating_next_tier": "Enabled" if include_next_tier_down else "Disabled",
        "hidden_columns_summary": ", ".join(hidden_quote_keys) if hidden_quote_keys else "None",
        "result_metric_key": "activity_volume",
        "result_metric_label": "Volume",
        "result_columns": [
            {"label": "Name", "key": "company_name"},
            *[{"label": key, "key": key} for key in visible_quote_keys],
        ],
        "stocks": ranked_stocks,
    }