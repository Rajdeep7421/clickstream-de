# data_generator/src/event_generator.py

import uuid
import datetime
import random
import json
from src import config 

user_sessions = {} 
# {user_id: {
#    "session_id": "...",
#    "last_page": "...",
#    "cart_items": [], # Stores full product objects now
#    "last_event_type": "START_SESSION", # Initial state for transitions
#    "current_product_viewed": None, # The product they are currently viewing/interacting with
#    "is_new_user": True/False,
#    "referral_source": "...",
#    "device_type": "...",
#    "geo_country": "...",
#    "geo_city": "..."
# }}

def _generate_user_id():
    """Generates a unique user ID."""
    return f"user_{uuid.uuid4().hex[:8]}"

def _choose_from_weighted_dict(weights_dict):
    """Chooses an item from a dictionary where values are weights."""
    items = list(weights_dict.keys())
    weights = list(weights_dict.values())
    return random.choices(items, weights=weights, k=1)[0]

def _get_or_create_session(user_id):
    """
    Retrieves an existing user session or creates a new one.
    Simulates a new session with a 15% chance for existing users.
    """
    if user_id not in user_sessions:
        # New user always starts a new session
        is_new_user = True
        referral_source = _choose_from_weighted_dict(config.REFERRAL_SOURCES)
        device_type = _choose_from_weighted_dict(config.DEVICE_TYPES)
        geo_country = random.choice(list(config.GEO_LOCATIONS.keys()))
        geo_city = random.choice(config.GEO_LOCATIONS[geo_country])
        os = random.choice(config.OS_TYPES)
        browser = random.choice(config.BROWSER_TYPES)
    elif random.random() < 0.05: # 5% chance for existing user to start a new session
        is_new_user = False # Still an existing user, just new session
        referral_source = _choose_from_weighted_dict(config.REFERRAL_SOURCES)
        device_type = _choose_from_weighted_dict(config.DEVICE_TYPES)
        geo_country = user_sessions[user_id]["geo_country"]
        geo_city = user_sessions[user_id]["geo_city"]
        os = random.choice(config.OS_TYPES)
        browser = random.choice(config.BROWSER_TYPES)
    else:
        # Continue existing session
        return user_sessions[user_id]

    session_id = f"session_{uuid.uuid4().hex[:12]}"
    user_sessions[user_id] = {
        "session_id": session_id,
        "last_page": random.choice(config.PAGES), # Initial page for new session
        "cart_items": [],
        "last_event_type": "START_SESSION", # Set initial state for transitions
        "current_product_viewed": None,
        "is_new_user": is_new_user,
        "referral_source": referral_source,
        "device_type": device_type,
        "geo_country": geo_country,
        "geo_city": geo_city,
        "os": os,
        "browser": browser
    }
    return user_sessions[user_id]

def generate_clickstream_event():
    """
    Generates a single simulated clickstream event with more realistic logic.
    """
    # Select a user, mixing existing with a small chance of new ones
    active_users = list(user_sessions.keys())
    if not active_users: # Handle initial startup with no users
        user_id = _generate_user_id()
    else:
        user_id_options = active_users + [_generate_user_id() for _ in range(5)]
        user_id = random.choice(user_id_options)

    user_state = _get_or_create_session(user_id)

    timestamp = datetime.datetime.utcnow().isoformat() + "Z"


    prev_event_type = user_state["last_event_type"]
    possible_next_events = config.EVENT_TRANSITION_PROBABILITIES.get(prev_event_type, config.EVENT_TRANSITION_PROBABILITIES["page_view"]) # Default to page_view if unknown
    event_type = _choose_from_weighted_dict(possible_next_events)

    page_url = user_state["last_page"]
    product_id_value = None
    product_name_value = None
    product_brand_value = None
    product_price_value = None
    product_category_value = None

    # Logic for product and page context
    selected_product_obj = None

    if event_type == "page_view":
        # Simulate Browse: either a general page, a category page, or a specific product page
        # 60% chance for general page view
        if random.random() < 0.6: 
            page_url = random.choice([p for p in config.PAGES if p not in ["/products", "/cart", "/checkout", "/purchase_success"]])
            user_state["current_product_viewed"] = None # Clear product context if not product page
        else: 
            product_category_value = random.choice(config.PRODUCT_CATEGORIES)
            selected_product_obj = random.choice(config.PRODUCTS_BY_CATEGORY[product_category_value])
            page_url = f"/products/{selected_product_obj['id']}" # Specific product page URL
            user_state["current_product_viewed"] = selected_product_obj # Store for next action
            

    elif event_type == "add_to_cart":
        if user_state["current_product_viewed"]:
            # User adds the product they just viewed
            selected_product_obj = user_state["current_product_viewed"]
        else:
            # If no product in context (e.g., came from search/direct), pick a random product
            random_category = random.choice(config.PRODUCT_CATEGORIES)
            selected_product_obj = random.choice(config.PRODUCTS_BY_CATEGORY[random_category])
        user_state["cart_items"].append(selected_product_obj)
        page_url = "/cart" # Assume user navigates to cart or stays on product page
        user_state["current_product_viewed"] = None # Product added, context might shift

    elif event_type == "remove_from_cart":
        if user_state["cart_items"]:
            # Remove a random item from cart if it's not empty
            removed_product = user_state["cart_items"].pop(random.randrange(len(user_state["cart_items"])))
            selected_product_obj = removed_product # The one that was removed
            page_url = "/cart"
        else:
            # Revert to page view if no items to remove to keep behavior realistic
            event_type = "page_view"
            page_url = random.choice(config.PAGES)
            user_state["current_product_viewed"] = None

    elif event_type == "checkout":
        if user_state["cart_items"]:
            page_url = "/checkout"
            user_state["current_product_viewed"] = None # Clear product context
        else:
            # Revert to page view if no items to checkout
            event_type = "page_view"
            page_url = random.choice(config.PAGES)
            user_state["current_product_viewed"] = None

    elif event_type == "purchase":
        if user_state["cart_items"]:
            # For purchase, 'product_id' becomes a list of IDs, and 'category' becomes 'Mixed'
            product_id_value = [item["id"] for item in user_state["cart_items"]]
            product_name_value = [item["name"] for item in user_state["cart_items"]]
            product_brand_value = list(set(item["brand"] for item in user_state["cart_items"])) # Unique brands
            product_price_value = round(sum(item["price"] for item in user_state["cart_items"]), 2) # Total purchase value
            product_category_value = "Mixed" # Represents multiple categories in one purchase
            page_url = "/purchase_success"
            user_state["cart_items"] = [] # Clear cart after purchase
            user_state["current_product_viewed"] = None
        else:
            # Revert to page view if no items to purchase
            event_type = "page_view"
            page_url = random.choice(config.PAGES)
            user_state["current_product_viewed"] = None

    elif event_type == "search":
        page_url = "/search_results"
        user_state["current_product_viewed"] = None
        # Could add a 'search_query' field here for more realism

    # Populate product details for single-item events (not purchase)
    if selected_product_obj and event_type not in ["purchase"]:
        product_id_value = [selected_product_obj["id"]]
        product_name_value = [selected_product_obj["name"]]
        product_brand_value = [selected_product_obj["brand"]]
        product_price_value = [selected_product_obj["price"]]
        # Find the category for the selected product object
        for cat, prods in config.PRODUCTS_BY_CATEGORY.items():
            if selected_product_obj in prods:
                product_category_value = cat
                break


    event = {
        "user_id": user_id,
        "session_id": user_state["session_id"],
        "timestamp": timestamp,
        "event_type": event_type,
        "page_url": page_url,
        "product_id": product_id_value,        # Specific model ID (list for purchase)
        "product_name": product_name_value,     # Product full name (list for purchase)
        "product_brand": product_brand_value,   # Product brand (list for purchase)
        "product_price": product_price_value,   # Product price (total for purchase)
        "category": product_category_value,     # Broader category (Mixed for purchase)
        "browser": user_state["browser"],
        "os": user_state["os"],
        "ip_address": f"192.168.{random.randint(0,255)}.{random.randint(0,255)}",
        "referral_source": user_state["referral_source"],
        "device_type": user_state["device_type"],
        "geo_country": user_state["geo_country"],
        "geo_city": user_state["geo_city"],
        "is_new_user": user_state["is_new_user"],
        "cart_size": len(user_state["cart_items"]) # Current items in cart for this event
    }

    # Update user state for next event generation
    user_state["last_page"] = page_url
    user_state["last_event_type"] = event_type
    # current_product_viewed is handled within the event_type logic

    return event

# Initialize some starting users for the simulation
for _ in range(config.NUM_USERS):
    _get_or_create_session(_generate_user_id())