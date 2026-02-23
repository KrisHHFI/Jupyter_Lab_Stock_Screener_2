from IPython.display import display

from utils.formatting.truncate_two_decimals import truncate_two_decimals


def _format_cell_value(value):
    if isinstance(value, float):
        return f"{truncate_two_decimals(value):.2f}"
    return value


def display_styled_table(df):
    """Display a bordered, notebook-friendly styled table."""
    if hasattr(df, "map"):
        formatted_df = df.map(_format_cell_value)
    else:
        formatted_df = df.applymap(_format_cell_value)

    styled = (
        formatted_df.style.hide(axis="index")
        .set_properties(**{"text-align": "left", "padding": "6px"})
        .set_table_styles(
            [
                {"selector": "table", "props": "border-collapse: collapse; width: 100%;"},
                {
                    "selector": "th",
                    "props": "border: 1px solid #888; background-color: #ffffff; color: #000000; text-align: left; padding: 6px;",
                },
                {"selector": "td", "props": "border: 1px solid #888; padding: 6px;"},
            ]
        )
    )
    display(styled)
