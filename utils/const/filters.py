REGION_FILTER = "us"
INDUSTRY_FILTERS = [
	"Discount Stores",
	"Grocery Stores",
	"Food Distribution",
	"Restaurants",
	"Specialty Retail",
	"Department Stores",
	"Packaged Foods",
]
INDUSTRY_LABEL = ", ".join(INDUSTRY_FILTERS)
MIN_MARKET_CAP_FILTER = 100_000_000
TOP_N_FILTER = 200
SCREEN_SIZE_FILTER = 250
POINTS_THRESHOLD = 20
INFO_ENRICH_LIMIT_FILTER = 25

ALLOWED_US_EXCHANGE_CODES = [
	"NMS",  # Nasdaq Global Select
	"NGM",  # Nasdaq Global Market
	"NCM",  # Nasdaq Capital Market
	"NYQ",  # NYSE
	"ASE",  # NYSE American
]
