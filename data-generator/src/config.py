# data_generator/src/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# --- Event Hubs Configuration ---
EVENTHUB_CONNECTION_STR = os.environ.get("EVENTHUB_CONNECTION_STR")
EVENTHUB_NAME = os.environ.get("EVENTHUB_NAME")

# --- Simulation Parameters ---
NUM_USERS = 200 
MAX_EVENTS_PER_BATCH = 75 
SLEEP_INTERVAL_SECONDS = 0.3 

# --- Core Data Lists ---
PAGES = ["/", "/products", "/about", "/contact", "/cart", "/checkout", "/purchase_success"]

# --- NEW: Product Categories and Specific Products (with Brand & Price) ---
PRODUCT_CATEGORIES = [
    "Laptops", "Smartphones", "Headphones", "Monitors",
    "Keyboards", "Mice", "Speakers", "Cameras", "Wearables"
]

PRODUCTS_BY_CATEGORY = {
    "Laptops": [
        {"id": "LAPTOP-XPS15-2024", "name": "Dell XPS 15 (2024)", "brand": "Dell", "price": 1899.99, "stock": 50},
        {"id": "LAPTOP-MBOOK-AIR-M3", "name": "MacBook Air M3", "brand": "Apple", "price": 1199.00, "stock": 120},
        {"id": "LAPTOP-SURFACE-PRO10", "name": "Microsoft Surface Pro 10", "brand": "Microsoft", "price": 1099.00, "stock": 70},
        {"id": "LAPTOP-ZENBOOK-14", "name": "ASUS ZenBook 14 OLED", "brand": "ASUS", "price": 999.00, "stock": 90},
        {"id": "LAPTOP-IDEAPAD-GAMING", "name": "Lenovo IdeaPad Gaming 3", "brand": "Lenovo", "price": 849.00, "stock": 60}
    ],
    "Smartphones": [
        {"id": "PHONE-IPHONE15", "name": "iPhone 15 Pro", "brand": "Apple", "price": 999.00, "stock": 200},
        {"id": "PHONE-SAMSUNG-S24", "name": "Samsung Galaxy S24 Ultra", "brand": "Samsung", "price": 1299.00, "stock": 180},
        {"id": "PHONE-PIXEL8", "name": "Google Pixel 8 Pro", "brand": "Google", "price": 799.00, "stock": 150},
        {"id": "PHONE-ONEPLUS-12", "name": "OnePlus 12", "brand": "OnePlus", "price": 799.00, "stock": 100},
        {"id": "PHONE-XIAOMI-14", "name": "Xiaomi 14 Ultra", "brand": "Xiaomi", "price": 999.00, "stock": 80}
    ],
    "Headphones": [
        {"id": "HP-SONY-WH1000XM5", "name": "Sony WH-1000XM5", "brand": "Sony", "price": 349.00, "stock": 300},
        {"id": "HP-BOSE-QC45", "name": "Bose QuietComfort 45", "brand": "Bose", "price": 279.00, "stock": 250},
        {"id": "HP-AIRPODS-MAX", "name": "AirPods Max", "brand": "Apple", "price": 549.00, "stock": 100},
        {"id": "HP-SENNH-HD660S2", "name": "Sennheiser HD 660S2", "brand": "Sennheiser", "price": 599.00, "stock": 50},
        {"id": "HP-JBL-TUNE760NC", "name": "JBL Tune 760NC", "brand": "JBL", "price": 129.00, "stock": 400}
    ],
    "Monitors": [
        {"id": "MON-DELL-U2723QE", "name": "Dell UltraSharp U2723QE", "brand": "Dell", "price": 599.00, "stock": 100},
        {"id": "MON-LG-27GN95R", "name": "LG UltraGear 27GN95R", "brand": "LG", "price": 799.00, "stock": 80},
        {"id": "MON-SAMSUNG-G9", "name": "Samsung Odyssey G9", "brand": "Samsung", "price": 1299.00, "stock": 40}
    ],
    "Keyboards": [
        {"id": "KB-LOGI-MXKEYS", "name": "Logitech MX Keys S", "brand": "Logitech", "price": 109.00, "stock": 200},
        {"id": "KB-RAZER-BWV3", "name": "Razer BlackWidow V3", "brand": "Razer", "price": 139.00, "stock": 150}
    ],
    "Mice": [
        {"id": "MOUSE-LOGI-MXMASTER3S", "name": "Logitech MX Master 3S", "brand": "Logitech", "price": 99.00, "stock": 250},
        {"id": "MOUSE-RAZER-DEATHADDER", "name": "Razer DeathAdder V3", "brand": "Razer", "price": 69.00, "stock": 180}
    ],
    "Speakers": [
        {"id": "SPK-BOSE-SOUNDLINKFLEX", "name": "Bose SoundLink Flex", "brand": "Bose", "price": 149.00, "stock": 120},
        {"id": "SPK-JBL-FLIP6", "name": "JBL Flip 6", "brand": "JBL", "price": 109.00, "stock": 150}
    ],
    "Cameras": [
        {"id": "CAM-SONY-A7IV", "name": "Sony Alpha a7 IV", "brand": "Sony", "price": 2499.00, "stock": 30},
        {"id": "CAM-CANON-R6II", "name": "Canon EOS R6 Mark II", "brand": "Canon", "price": 2299.00, "stock": 25}
    ],
    "Wearables": [
        {"id": "WEAR-APPLE-WATCH9", "name": "Apple Watch Series 9", "brand": "Apple", "price": 399.00, "stock": 200},
        {"id": "WEAR-SAMSUNG-WATCH6", "name": "Samsung Galaxy Watch 6", "brand": "Samsung", "price": 299.00, "stock": 180}
    ]
}


# --- NEW: Event Types (includes 'checkout') ---
EVENT_TYPES = ["page_view", "add_to_cart", "remove_from_cart", "purchase", "search", "checkout"]

# --- NEW: Event Transition Probabilities ---
# Defines the likelihood of moving from one event type to another.
# Sum of probabilities for each state should be 1.0
EVENT_TRANSITION_PROBABILITIES = {
    "START_SESSION": { # Initial state when a new session begins
        "page_view": 0.8,
        "search": 0.2,
    },
    "page_view": {
        "page_view": 0.6,          # Continue Browse (different page/product)
        "add_to_cart": 0.2,        # Add current viewed product (if applicable)
        "search": 0.1,             # Search from current page
        "end_session": 0.1         # User leaves
    },
    "add_to_cart": {
        "page_view": 0.4,          # Continue Browse after adding
        "checkout": 0.4,           # Proceed to checkout
        "remove_from_cart": 0.1,   # remove frm cart
        "end_session": 0.1         # User leaves
    },
    "remove_from_cart": {
        "page_view": 0.7,
        "add_to_cart": 0.2,        # Add something else or original back
        "end_session": 0.1
    },
    "search": {
        "page_view": 0.7,          # View search results
        "search": 0.2,             # Refine search
        "end_session": 0.1
    },
    "checkout": {
        "purchase": 0.7,           # Successful purchase
        "page_view": 0.2,          # Abandon checkout to browse
        "end_session": 0.1         # Abandon checkout and leave
    },
    "purchase": {                  # After purchase, likely success page or end session
        "page_view": 0.9,          # browse again (e.g., for accessories)
        "end_session": 0.1
    }
}


REFERRAL_SOURCES = {
    "organic_search": 0.4,
    "direct": 0.2,
    "social_media": 0.15,
    "paid_ad": 0.15,
    "email_campaign": 0.1
}

DEVICE_TYPES = {
    "Desktop": 0.6,
    "Mobile": 0.3,
    "Tablet": 0.1
}

GEO_LOCATIONS = {
    "USA": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "India": ["Mumbai", "Bengaluru", "Delhi", "Chennai", "Hyderabad"],
    "Germany": ["Berlin", "Munich", "Hamburg", "Frankfurt"],
    "UK": ["London", "Manchester", "Birmingham"],
    "Australia": ["Sydney", "Melbourne", "Brisbane"]
}

BROWSER_TYPES = ["Chrome", "Firefox", "Safari", "Edge"]
OS_TYPES = ["Windows", "macOS", "Linux", "Android", "iOS"]


if not EVENTHUB_CONNECTION_STR or not EVENTHUB_NAME:
    raise ValueError("EVENTHUB_CONNECTION_STR and EVENTHUB_NAME must be set in .env file or as environment variables.")

ALL_PRODUCT_IDS = [p["id"] for category_prods in PRODUCTS_BY_CATEGORY.values() for p in category_prods]



