import pandas as pd

from utils.formatting.truncate_two_decimals import truncate_two_decimals
from utils.printing.display_styled_table import display_styled_table
from utils.printing.print_header import print_header


def print_stock_info(stock_data):
    """Print ranked screener result information in a clean, readable format."""
    result_metric_key = stock_data.get("result_metric_key", "pe_ratio")
    result_metric_label = stock_data.get("result_metric_label", "P/E Ratio")
    result_columns = stock_data.get("result_columns")

    print_header("Stock Screener", main_header=True)

    print_header("Filters")

    display_styled_table(
        pd.DataFrame(
            (
                [
                    ["Filter Region", stock_data["region_filter"]],
                    ["Filter Industry", stock_data["industry_filter"]],
                    ["Filter Min Market Cap", stock_data["min_market_cap_filter"]],
                ]
                + ([
                    ["Filter Analyst Rating", stock_data.get("analyst_rating_filter", "N/A")],
                ] if "analyst_rating_filter" in stock_data else [])
                + ([
                    ["Filter Next Tier Down", stock_data.get("analyst_rating_next_tier", "Disabled")],
                ] if "analyst_rating_next_tier" in stock_data else [])
                + ([
                    ["Hidden Columns", stock_data.get("hidden_columns_summary", "None")],
                ] if "hidden_columns_summary" in stock_data else [])
            ),
            columns=["Metric", "Value"],
        )
    )

    print_header("Sorting")
    display_styled_table(
        pd.DataFrame(
            [
                ["Sorted By", stock_data["sorting_field"]],
                ["Direction", stock_data["sorting_direction"]],
            ],
            columns=["Metric", "Value"],
        )
    )

    print_header("Results")

    if result_columns:
        ranked_table = pd.DataFrame(
            [
                [item.get(col["key"], "N/A") for col in result_columns]
                for item in stock_data["stocks"]
            ],
            columns=[col["label"] for col in result_columns],
        )
    else:
        ranked_table = pd.DataFrame(
            [
                [
                    item["company_name"],
                    truncate_two_decimals(item["pe_ratio"])
                    if result_metric_key == "pe_ratio"
                    else item.get(result_metric_key, "N/A"),
                ]
                for item in stock_data["stocks"]
            ],
            columns=["Name", result_metric_label],
        )

    display_styled_table(ranked_table)
