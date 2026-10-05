from prometheus_client import Counter, Gauge, Histogram


REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
)

ACTIVE_CARS = Gauge(
    "active_cars",
    "Number of active cars",
)

ONGOING_RENTALS = Gauge(
    "ongoing_rentals",
    "Number of ongoing rentals",
)

REQUEST_TIME = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
)