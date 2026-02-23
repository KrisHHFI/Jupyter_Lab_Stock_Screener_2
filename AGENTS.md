# BasicStockData4 — Agent Notes

## Project Overview
This project is a modular Python + Jupyter workflow for querying and displaying stock information with yfinance.

Main flow:
- Cell 1 in `main.ipynb` runs the app flow.
- Data is fetched from Yahoo Finance via `yfinance` screener (+ optional ticker verification).
- Text output and call-usage rendering are handled by separate function modules.

## Coding Rules
- Keep the code modular.
- Each function should be in its own file.
- Notebook cells should stay thin and primarily orchestrate imports + function calls.
- Prefer clear, descriptive file names that match the function they contain.
- Every utility/function file must be declared in this AGENTS.md file.
- Whenever a file is added, removed, or renamed, update all relevant AGENTS.md sections immediately (Current Function File Pattern, Folder Structure, and File Responsibilities).

## Git / Sensitive Data Rules
- This repository will be published to GitHub, so never commit secrets or private data.
- Keep sensitive files out of git using `.gitignore` (API keys, tokens, credentials, private exports, and local environment files such as `.env*`).
- Before pushing, verify staged files do not include secrets, local paths, or personal/sensitive notebook outputs.
- If a sensitive file is accidentally tracked, remove it from the index (for example with `git rm --cached <path>`) and keep it ignored going forward.

## VS Code Notebook Output Settings
- Keep notebook output readable in VS Code by using workspace settings in `.vscode/settings.json`.
- Current settings used by this project:
	- `notebook.output.textLineLimit = 0`
	- `notebook.output.scrolling = true`

## Notebook Execution Rule
- After implementing notebook-related code/output changes, restart the notebook kernel and rerun from Cell 1 so outputs reflect a clean state.

## Current Function File Pattern
Examples in this project:
- `utils/yfinance/get_most_active_us_stocks.py`
- `utils/yfinance/map_quote_to_stock_data.py`
- `utils/yfinance/enrich_with_info.py`
- `utils/yfinance/call_tracker/reset_yfinance_call_count.py`
- `utils/yfinance/call_tracker/set_yfinance_call_delay.py`
- `utils/yfinance/call_tracker/increment_yfinance_call_count.py`
- `utils/yfinance/call_tracker/log_yfinance_call.py`
- `utils/yfinance/call_tracker/get_yfinance_call_log.py`
- `utils/yfinance/call_tracker/get_yfinance_call_count.py`
- `utils/yfinance/call_tracker/timestamp_now.py`
- `utils/yfinance/call_tracker/state.py`
- `utils/const/filters.py`
- `utils/const/sorting.py`
- `utils/printing/display_styled_table.py`
- `utils/printing/print_header.py`
- `utils/printing/print_stock_info.py`
- `utils/printing/print_data_collected.py`
- `utils/formatting/format_compact_number.py`
- `utils/formatting/format_timestamp.py`
- `utils/formatting/truncate_two_decimals.py`

## Folder Structure
```text
BasicStockData4/
├── main.ipynb
├── AGENTS.md
├── .vscode/
│   └── settings.json
├── __pycache__/
└── utils/
	├── __init__.py
	├── __pycache__/
	├── const/
	│	├── __init__.py
	│	├── filters.py
	│	└── sorting.py
	├── yfinance/
	│	├── __init__.py
	│	├── enrich_with_info.py
	│	├── get_most_active_us_stocks.py
	│	├── map_quote_to_stock_data.py
	│	└── call_tracker/
	│		├── __init__.py
	│		├── state.py
	│		├── timestamp_now.py
	│		├── reset_yfinance_call_count.py
	│		├── set_yfinance_call_delay.py
	│		├── increment_yfinance_call_count.py
	│		├── log_yfinance_call.py
	│		├── get_yfinance_call_log.py
	│		└── get_yfinance_call_count.py
	├── printing/
	│	├── __init__.py
	│	├── display_styled_table.py
	│	├── print_header.py
	│	├── print_stock_info.py
	│	└── print_data_collected.py
	├── formatting/
	│	├── __init__.py
	│	├── format_compact_number.py
	│	├── format_timestamp.py
	│	└── truncate_two_decimals.py
	└── points/
		└── __init__.py
```

## File Responsibilities
- `main.ipynb`: Thin orchestration only (imports + top-level calls).
- `.vscode/settings.json`: Workspace notebook output settings (line-limit and scrolling behavior).
- `utils/const/filters.py`: Global screener filter constants (region, industry, market cap, top-n, and screen size).
- `utils/const/sorting.py`: Global sorting constants (display labels and Yahoo sort key/direction).
- `utils/yfinance/get_most_active_us_stocks.py`: Fetches top-N most-active US stocks using Yahoo's predefined `most_actives` screener preset.
- `utils/yfinance/map_quote_to_stock_data.py`: Maps screener quote objects into normalized stock rows.
- `utils/yfinance/enrich_with_info.py`: Optionally enriches screener rows with ticker info fields.
- `utils/yfinance/call_tracker/state.py`: Shared in-memory state for yfinance call tracking.
- `utils/yfinance/call_tracker/timestamp_now.py`: Generates timestamps for call log entries.
- `utils/yfinance/call_tracker/reset_yfinance_call_count.py`: Resets tracked call count and log.
- `utils/yfinance/call_tracker/set_yfinance_call_delay.py`: Sets delay seconds between tracked calls.
- `utils/yfinance/call_tracker/increment_yfinance_call_count.py`: Increments and returns tracked call count.
- `utils/yfinance/call_tracker/log_yfinance_call.py`: Applies delay and appends timestamped call log entries.
- `utils/yfinance/call_tracker/get_yfinance_call_log.py`: Returns tracked call log entries.
- `utils/yfinance/call_tracker/get_yfinance_call_count.py`: Returns current tracked call count.
- `utils/printing/display_styled_table.py`: Displays bordered, notebook-friendly styled DataFrame tables.
- `utils/printing/print_header.py`: Prints consistent section headers used in console output.
- `utils/printing/print_stock_info.py`: Console/text presentation of screener result fields.
- `utils/printing/print_data_collected.py`: Prints call counts, delay settings, timestamp, and yfinance call log.
- `utils/formatting/format_compact_number.py`: Compact numeric formatting helper used for market cap/volume/revenue-style values.
- `utils/formatting/format_timestamp.py`: Shared timestamp formatting helper for call logs and metadata output.
- `utils/formatting/truncate_two_decimals.py`: Numeric truncation helper used across modules.
