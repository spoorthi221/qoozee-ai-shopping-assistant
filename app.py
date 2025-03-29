import streamlit as st
import csv
import requests
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Set, Optional, Union, Tuple
import html_components as html

# --- Data Models and Types ---
ProductType = Dict[str, str]
CartType = List[int]
BehaviorType = Dict[str, Union[Set[str], List[str]]]

# --- Load CSS ---
def load_css():
    """Load custom CSS from a file or use inline CSS."""
    try:
        with open('static/styles.css', 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # If file not found, use inline CSS
        st.markdown("""
        <style>
        /* Main theme colors */
        :root {
            --qoozee-pink: #FF9EAA;
            --qoozee-light-pink: #FFD1D9;
            --qoozee-purple: #9D65C9;
            --qoozee-yellow: #FFD166;
            --qoozee-teal: #2EC4B6;
        }
        
        /* Product card */
        .product-card {
            background-color: black;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            border: 1px solid #F0F0F0;
            margin-bottom: 20px;
            color: white;
        }
        
        /* Cart item */
        .cart-item {
            background-color: #222222;
            border-radius: 16px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 5px solid var(--qoozee-pink);
            color: white;
        }
        
        /* Price tag */
        .price-tag {
            background-color: #333333;
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
        }
        
        /* Star rating */
        .star-rating {
            color: var(--qoozee-yellow);
            font-weight: bold;
        }
        
        /* Category badge */
        .category-badge {
            background-color: #444444;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            margin-right: 5px;
            color: white;
        }
        
        /* Total price */
        .total-price {
            background: linear-gradient(90deg, var(--qoozee-pink), var(--qoozee-purple));
            color: white;
            padding: 10px 20px;
            border-radius: 50px;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
        }
        
        /* Header styling */
        h1, h2, h3, h4, h5 {
            color: white;
        }
        
        .app-subtitle {
            text-align: center;
            color: #888;
            margin-top: -15px;
            margin-bottom: 30px;
        }
        
        /* User profile */
        .user-profile {
            background-color: #222222;
            border-radius: 16px;
            padding: 15px;
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            color: white;
        }
        
        .avatar {
            background-color: var(--qoozee-pink);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-right: 10px;
            color: white;
            font-weight: bold;
        }
        
        /* Button styling */
        .stButton > button {
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* AI response */
        .ai-response {
            background-color: #222222;
            padding: 15px;
            border-radius: 20px 20px 5px 20px;
            max-width: 80%;
            align-self: flex-end;
            margin: 10px 0 10px auto;
            color: white;
        }
        
        /* User query */
        .user-query {
            background-color: #333333;
            padding: 15px;
            border-radius: 20px 20px 20px 5px;
            max-width: 80%;
            align-self: flex-start;
            margin: 10px 0;
            color: white;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 50px;
            color: #888;
            padding: 20px 0;
            border-top: 1px solid #333333;
        }
        
        /* Dark theme overrides */
        body {
            background-color: #121212;
            color: white;
        }
        
        /* Section headers */
        .section-header {
            background-color: #222222;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            color: white;
        }
        
        /* Order details */
        .order-details {
            background-color: #222222;
            border-radius: 16px;
            padding: 20px;
            margin: 20px 0;
            color: white;
        }
        
        /* Order success */
        .order-success {
            background-color: #1E2E1E;
            border-radius: 16px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
            border: 2px solid #2A4A2A;
            color: white;
        }
        
        /* Streamlit element overrides */
        .css-1l4y4fc, .css-1wmy9lf, .css-k3w14i {
            background-color: #222222;
            color: white;
        }
        
        .st-dk, .st-d0, .st-d1, .st-d3 {
            border-color: #333333;
        }
        
        [data-baseweb="tab"] {
            color: white !important;
        }
        
        [data-baseweb="tab-list"] {
            background-color: #222222 !important;
        }
        
        [aria-selected="true"] {
            background-color: #333333 !important;
            color: var(--qoozee-pink) !important;
        }
        </style>
        """, unsafe_allow_html=True)

# --- Load product data from CSV ---
@st.cache_data(ttl=60)  # Cache expires after 60 seconds
def load_products(filename: str) -> List[ProductType]:
    """Load and cache product data from CSV file."""
    try:
        mod_time = os.path.getmtime(filename)
    except:
        mod_time = 0
        
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            products = list(reader)
            print(f"Loaded {len(products)} products from {filename}")
            return products
    except FileNotFoundError:
        print(f"Product file '{filename}' not found. Using sample data.")
        # Return sample data for demo
        return [
            {"product_id": "101", "product_name": "Oversized Hoodie - Pink", "price": "999", "rating": "4.5", "category": "Clothing"},
            {"product_id": "102", "product_name": "Smartphone Stand", "price": "499", "rating": "4.2", "category": "Electronics"},
            {"product_id": "103", "product_name": "Coffee Mug - Ceramic", "price": "299", "rating": "4.8", "category": "Home Decor"},
            {"product_id": "104", "product_name": "Wireless Earbuds", "price": "1499", "rating": "4.6", "category": "Electronics"},
            {"product_id": "105", "product_name": "Throw Pillow Cover", "price": "399", "rating": "4.3", "category": "Home Decor"},
            {"product_id": "106", "product_name": "Denim Jacket", "price": "1299", "rating": "4.4", "category": "Clothing"}
        ]
    except Exception as e:
        print(f"Error loading products: {str(e)}")
        return []

# --- Cart Operations ---
def get_cart_products(cart_ids: CartType, products: List[ProductType]) -> Tuple[List[ProductType], float]:
    """Get products in cart and calculate total price."""
    # Create a lookup dictionary for faster access
    product_lookup = {int(product['product_id']): product for product in products}
    
    cart_products = []
    total = 0.0
    
    for pid in cart_ids:
        if pid in product_lookup:
            product = product_lookup[pid]
            cart_products.append(product)
            total += float(product['price'])
    
    return cart_products, total

def show_cart(cart_ids: CartType, products: List[ProductType]) -> None:
    """Display cart items and total."""
    cart_products, total = get_cart_products(cart_ids, products)
    
    st.markdown("<h2>🛒 Your Shopping Bag</h2>", unsafe_allow_html=True)
    
    if not cart_products:
        st.markdown("""
        <div style="text-align: center; padding: 30px 0; background-color: #222222; border-radius: 16px;">
            <img src="https://cdn-icons-png.flaticon.com/512/2038/2038854.png" width="100">
            <h3>Your bag is empty!</h3>
            <p>Add some cute stuff and come back 💕</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display number of items
    st.markdown(f"<p style='color: #888;'>{len(cart_products)} items in your bag</p>", unsafe_allow_html=True)
    
    # Cart items
    for item in cart_products:
        st.markdown(f"""
        <div class="cart-item">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4>{item['product_name']}</h4>
                    <div style="display: flex; gap: 10px; margin-top: 5px;">
                        <span class="price-tag">₹{item['price']}</span>
                        <span class="star-rating">⭐ {item['rating']}</span>
                        <span class="category-badge">{item['category']}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Remove button
        if st.button("✖️ Remove", key=f"remove_{item['product_id']}", type="secondary"):
            st.session_state.cart.remove(int(item['product_id']))
            st.session_state.behavior["removed_products"].append(item['product_name'])
            st.toast(f"Removed: {item['product_name']}", icon="🗑️")
            st.rerun()
    
    # Total price
    st.markdown(f"""
    <div class="total-price">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>Bag Total:</span>
            <span>₹{total:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Checkout buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("🛍️ Continue Shopping", key="continue_shopping")
    with col2:
        st.button("💳 Checkout Now", key="proceed_checkout", type="primary")

# --- Product Display ---
def display_product_card(product: ProductType) -> None:
    """Display a product card with add to cart button."""
    product_id = int(product['product_id'])
    
    # Display the product card
    st.markdown(f"""
    <div class="product-card">
        <h4>✨ {product['product_name']}</h4>
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 10px 0;">
            <span class="price-tag">₹{product['price']}</span>
            <span class="star-rating">⭐ {product['rating']}</span>
        </div>
        <span class="category-badge">{product['category']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Add action buttons
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.button("👀 Quick View", key=f"view_{product_id}")
    
    with col2:
        # Check if already in cart
        in_cart = product_id in st.session_state.cart
        button_text = "🛒 Added" if in_cart else "🛒 Add"
        button_type = "secondary" if in_cart else "primary"
        
        if st.button(button_text, key=f"add_{product_id}", disabled=in_cart, type=button_type):
            st.session_state.cart.append(product_id)
            st.session_state.behavior["added_products"].append(product['product_name'])
            st.toast(f"Added to cart: {product['product_name']}", icon="✅")
            st.rerun()

# --- Product Search and Filtering ---
def search_products(products: List[ProductType], category: Optional[str] = None, 
                    max_price: Optional[float] = None, search_term: Optional[str] = None) -> List[ProductType]:
    """Search and filter products based on criteria."""
    filtered_products = []
    
    for product in products:
        # Apply category filter if provided
        if category and category.lower() != "all" and product['category'].lower() != category.lower():
            continue
            
        # Apply price filter if provided
        if max_price and float(product['price']) > max_price:
            continue
            
        # Apply search term filter if provided
        if search_term and search_term.lower() not in product['product_name'].lower():
            continue
            
        filtered_products.append(product)
        
    return filtered_products

# --- Product Comparison --- 
def find_product_by_name(name: str, products: List[ProductType]) -> Optional[ProductType]:
    """Find a product by its name (partial match)."""
    for product in products:
        if name.lower() in product['product_name'].lower():
            return product
    return None

def compare_products(name1: str, name2: str, products: List[ProductType]) -> None:
    """Compare two products and give recommendation."""
    product1 = find_product_by_name(name1, products)
    product2 = find_product_by_name(name2, products)

    if not product1 or not product2:
        st.error("❌ One or both products not found.")
        return

    # Track comparison in behavior
    st.session_state.behavior["compared_products"].append([product1['product_name'], product2['product_name']])

    # Show both products in styled cards
    st.markdown("<h3>✨ Product Comparison</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="background-color: #222222; border-radius: 16px; padding: 20px; height: 100%; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 2px solid #FFD1D9;">
            <h4 style="color: #FF9EAA;">{product1['product_name']}</h4>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <span class="price-tag">₹{product1['price']}</span>
                <span class="star-rating">⭐ {product1['rating']}</span>
            </div>
            <p style="color: #aaa; font-size: 14px; margin-bottom: 15px;">Category: {product1['category']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🛒 Add to Bag", key=f"compare_add_{product1['product_id']}"):
            st.session_state.cart.append(int(product1['product_id']))
            st.session_state.behavior["added_products"].append(product1['product_name'])
            st.toast(f"Added to cart: {product1['product_name']}", icon="✅")
            st.rerun()

    with col2:
        st.markdown(f"""
        <div style="background-color: #222222; border-radius: 16px; padding: 20px; height: 100%; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 2px solid #D1F0FF;">
            <h4 style="color: #2EC4B6;">{product2['product_name']}</h4>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <span class="price-tag">₹{product2['price']}</span>
                <span class="star-rating">⭐ {product2['rating']}</span>
            </div>
            <p style="color: #aaa; font-size: 14px; margin-bottom: 15px;">Category: {product2['category']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🛒 Add to Bag", key=f"compare_add_{product2['product_id']}"):
            st.session_state.cart.append(int(product2['product_id']))
            st.session_state.behavior["added_products"].append(product2['product_name'])
            st.toast(f"Added to cart: {product2['product_name']}", icon="✅")
            st.rerun()

    # Calculate recommendation
    rating1 = float(product1['rating'])
    rating2 = float(product2['rating'])
    price1 = float(product1['price'])
    price2 = float(product2['price'])

    # Calculate value ratio (rating/price)
    value_ratio1 = rating1 / price1
    value_ratio2 = rating2 / price2

    if value_ratio1 > value_ratio2:
        better = product1['product_name']
        reason = "higher rating-to-price ratio"
        winner_side = "left"
    elif value_ratio2 > value_ratio1:
        better = product2['product_name']
        reason = "higher rating-to-price ratio"
        winner_side = "right"
    elif rating1 > rating2:
        better = product1['product_name']
        reason = "higher rating"
        winner_side = "left"
    elif rating2 > rating1:
        better = product2['product_name']
        reason = "higher rating"
        winner_side = "right"
    else:
        better = product1['product_name'] if price1 < price2 else product2['product_name']
        reason = "lower price"
        winner_side = "left" if price1 < price2 else "right"

    # Show recommendation
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #FF9EAA, #9D65C9); color: white; border-radius: 16px; padding: 20px; margin-top: 20px; text-align: center;">
        <h4 style="margin-top: 0;">✨ Qoozee AI Recommends ✨</h4>
        <p style="font-size: 18px; font-weight: bold; margin: 10px 0;">{better}</p>
        <p>This product offers better value due to its {reason}!</p>
        <div style="background-color: #222222; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 10px auto;">
            <span style="color: #FF9EAA; font-weight: bold;">{"←" if winner_side == "left" else "→"}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Natural Language Processing ---
def parse_and_compare_input(user_input: str, products: List[ProductType]) -> None:
    """Parse natural language comparison query and compare products."""
    # Clean up user input
    user_input = user_input.lower()
    for word in ["should i buy", "compare", "?", "the"]:
        user_input = user_input.replace(word, "")
    user_input = user_input.strip()

    # Extract product names
    if " or " in user_input:
        parts = user_input.split(" or ")
    elif " vs " in user_input:
        parts = user_input.split(" vs ")
    else:
        st.warning("❌ Please mention exactly two products using 'or' or 'vs'")
        return

    if len(parts) != 2:
        st.warning("❌ Couldn't extract two product names.")
        return

    name1 = parts[0].strip()
    name2 = parts[1].strip()

    compare_products(name1, name2, products)

# --- LLM Integration ---
def ask_ai(prompt: str) -> str:
    """Send a prompt to AI and get a response."""
    try:
        # Try to call Ollama LLaMA
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=10  # Shorter timeout to fail faster
        )
        response.raise_for_status()
        return response.json().get("response", "No response from AI.")
    except:
        # Fall back to pre-defined responses
        responses = [
            "Based on your requirements, I'd recommend the Wireless Earbuds. They have excellent sound quality, long battery life, and are perfect for your needs.",
            "The Minimalist Wall Clock would be a perfect addition to your home decor. Its clean design and reliable mechanism make it a great value purchase.",
            "I'd suggest the Memory Foam Pillow. It provides excellent support for a good night's sleep and has consistently high ratings from customers.",
            "For your budget, the Smart LED Bulb offers the best value. It's energy-efficient, long-lasting, and can be controlled from your smartphone.",
            "The Stainless Steel Water Bottle is my recommendation. It's durable, keeps drinks at the right temperature for hours, and is environmentally friendly."
        ]
        return random.choice(responses)

# --- Prompt Generators ---
def get_persona_product_prompt(products: List[ProductType], persona: Optional[str] = None, 
                              category: Optional[str] = None, max_price: Optional[float] = None) -> str:
    """Generate a personalized prompt for product recommendations."""
    filtered_products = search_products(products, category, max_price)[:10]  # Limit to 10 products
    
    if not filtered_products:
        return "There are no products matching your criteria."
    
    prompt = "You are a smart shopping assistant helping someone find a product.\n"
    if persona:
        prompt += f"The customer is: {persona}\n"
    
    prompt += "Here is a list of available products:\n\n"
    for product in filtered_products:
        prompt += f"- {product['product_name']} | ₹{product['price']} | ⭐ {product['rating']} | {product['category']}\n"
    
    prompt += "\nBased on the customer's needs and preferences, recommend the best product. "
    prompt += "Explain why it's a good fit for them specifically."
    
    return prompt

def get_cart_based_suggestion_prompt(cart: CartType, products: List[ProductType]) -> str:
    """Generate a prompt for recommendations based on cart contents."""
    # Get cart products
    cart_products, _ = get_cart_products(cart, products)
    
    if not cart_products:
        return "The cart is empty. Please add some products first."
    
    # Get products not in cart
    cart_ids = set(cart)
    other_products = [p for p in products if int(p['product_id']) not in cart_ids][:5]  # Limit to 5 products
    
    # Format cart list
    cart_desc = "\n".join(f"- {p['product_name']} | ₹{p['price']} | {p['category']}" 
                        for p in cart_products)

    # Format remaining product list
    other_desc = "\n".join(f"- {p['product_name']} | ₹{p['price']} | {p['category']}" 
                         for p in other_products)

    prompt = f"""
Based on these items in the customer's cart:
{cart_desc}

Suggest 1-2 of these products that would complement the cart items well:
{other_desc}

Explain why each suggestion pairs well with the existing cart items.
"""
    return prompt

# --- UI Components ---
def sidebar_menu() -> None:
    """Create sidebar navigation menu with Gen Z aesthetic."""
    # Custom styling for sidebar header
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #FF9EAA; font-weight: 800;">✨ Qoozee ✨</h1>
        <p style="color: #888; margin-top: -15px;">your AI shopping bestie</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User profile with avatar
    st.sidebar.markdown("""
    <div class="user-profile">
        <div class="avatar">
            <span>S</span>
        </div>
        <div>
            <p style="margin: 0; font-weight: bold;">Spoorthi</p>
            <p style="margin: 0; font-size: 12px; color: #888;">⭐ Premium Member</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Cart summary with cute icon
    cart_size = len(st.session_state.cart)
    st.sidebar.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <span style="font-weight: bold; font-size: 16px;">🛍️ Your Bag</span>
        <span style="background-color: #FF9EAA; color: white; padding: 2px 8px; border-radius: 20px; font-size: 12px;">{cart_size}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Order history with cute styling
    orders_count = len(st.session_state.orders)
    st.sidebar.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <span style="font-weight: bold; font-size: 16px;">🎁 Your Orders</span>
        <span style="background-color: #9D65C9; color: white; padding: 2px 8px; border-radius: 20px; font-size: 12px;">{orders_count}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Show latest order if exists
    if orders_count > 0:
        latest_order = st.session_state.orders[-1]
        st.sidebar.markdown(f"""
        <div style="background-color: #333333; border-radius: 12px; padding: 12px; margin-bottom: 20px; border-left: 3px solid #9D65C9;">
            <p style="font-size: 12px; color: #888; margin: 0;">Latest Order</p>
            <p style="margin: 5px 0; font-weight: bold;">QZ-{latest_order['order_id']}</p>
            <p style="margin: 0; color: #FF9EAA; font-weight: bold;">₹{latest_order['total']:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add a visual separator
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    
    # Activity stats
    st.sidebar.markdown("<p style='font-weight: bold; font-size: 16px;'>📊 Your Activity</p>", unsafe_allow_html=True)
    
    # Create a grid of stats
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        viewed_count = len(st.session_state.behavior['viewed_products'])
        st.markdown(f"""
        <div style="text-align: center;">
            <p style="color: #888; font-size: 12px; margin: 0;">Viewed</p>
            <p style="font-weight: bold; font-size: 20px; color: #2EC4B6; margin: 0;">{viewed_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        added_count = len(st.session_state.behavior['added_products'])
        st.markdown(f"""
        <div style="text-align: center;">
            <p style="color: #888; font-size: 12px; margin: 0;">Added</p>
            <p style="font-weight: bold; font-size: 20px; color: #FF9EAA; margin: 0;">{added_count}</p>
        </div>
        """, unsafe_allow_html=True)
        
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        removed_count = len(st.session_state.behavior['removed_products'])
        st.markdown(f"""
        <div style="text-align: center;">
            <p style="color: #888; font-size: 12px; margin: 0;">Removed</p>
            <p style="font-weight: bold; font-size: 20px; color: #9D65C9; margin: 0;">{removed_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Show purchased count if exists
        purchased_count = 0
        if "purchased_products" in st.session_state.behavior:
            purchased_count = len(st.session_state.behavior["purchased_products"])
        
        st.markdown(f"""
        <div style="text-align: center;">
            <p style="color: #888; font-size: 12px; margin: 0;">Purchased</p>
            <p style="font-weight: bold; font-size: 20px; color: #FFD166; margin: 0;">{purchased_count}</p>
        </div>
        """, unsafe_allow_html=True)

def main() -> None:
    """Main application function."""
    st.set_page_config(
        page_title="Qoozee AI Shopping Assistant",
        page_icon="🛍️",
        layout="wide"
    )
    
    # Load CSS
    load_css()
    
    # Display the styled header
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <h1 style="color: #FF9EAA; font-size: 2.2rem;">✨ Qoozee AI Shopping Assistant ✨</h1>
        <p style="color: #888; margin-top: -10px;">your AI shopping bestie</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "cart" not in st.session_state:
        st.session_state.cart = [101, 105]  # Default cart items
    
    if "behavior" not in st.session_state:
        st.session_state.behavior = {
            "viewed_categories": set(),
            "viewed_products": [],
            "added_products": [],
            "removed_products": [],
            "compared_products": []
        }
    
    # Initialize orders list
    if "orders" not in st.session_state:
        st.session_state.orders = []
        
    # Initialize checkout state
    if "checkout_complete" not in st.session_state:
        st.session_state.checkout_complete = False
    
    # Load products
    products = load_products("products.csv")
    if not products:
        st.error("Unable to load products. Using sample data.")
    
    # Setup sidebar
    sidebar_menu()
    
    # Main content as tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🛒 Your Cart", 
        "🔍 Browse Products", 
        "🅾️ Compare Products", 
        "💡 AI Recommendations",
        "💳 Checkout"
    ])
    
    # Tab 1: Cart
    with tab1:
        show_cart(st.session_state.cart, products)
    
    # Tab 2: Browse Products
    with tab2:
        st.markdown("<h2>🔍 Discover Products</h2>", unsafe_allow_html=True)
        
        # Create styled filter section
        st.markdown("""
        <div style="background-color: #222222; border-radius: 16px; padding: 20px; margin-bottom: 20px;">
            <h4 style="margin-top: 0;">✨ Filter Options</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Create filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("<p style='color: #888; font-size: 14px; margin-bottom: 5px;'>Category</p>", unsafe_allow_html=True)
            
            # Get unique categories from products
            categories = ["All"] + sorted(list(set(p["category"] for p in products if "category" in p)))
            category = st.selectbox("", categories, label_visibility="collapsed")
            
        with col2:
            st.markdown("<p style='color: #888; font-size: 14px; margin-bottom: 5px;'>Price Range</p>", unsafe_allow_html=True)
            
            # Find max price in products for slider
            max_price_in_data = 5000
            if products:
                try:
                    max_price_in_data = max(float(p["price"]) for p in products if "price" in p)
                except:
                    pass
                
            max_price = st.slider("", 0, int(max_price_in_data), int(max_price_in_data), label_visibility="collapsed")
            
        with col3:
            st.markdown("<p style='color: #888; font-size: 14px; margin-bottom: 5px;'>Search</p>", unsafe_allow_html=True)
            search_term = st.text_input("", placeholder="Type what you're looking for...", label_visibility="collapsed")
        
        # Search button
        search_button = st.button("🔎 Find Products", key="search_button", type="primary")
        
        # Get default products to display
        if not search_button:
            default_filtered = search_products(products, None, max_price_in_data, None)
            display_count = min(20, len(default_filtered))
            
            # Display initial products
            if default_filtered:
                st.markdown(f"""
                <div style="background-color: #333333; border-radius: 30px; padding: 8px 16px; display: inline-block; margin: 20px 0;">
                    <span style="color: white; font-weight: bold;">Showing {display_count} of {len(default_filtered)} products</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Create a grid layout for products
                cols = st.columns(2)
                for i, product in enumerate(default_filtered[:display_count]):
                    # Track product views
                    st.session_state.behavior["viewed_categories"].add(product.get('category', 'Unknown'))
                    st.session_state.behavior["viewed_products"].append(product.get('product_name', 'Unknown'))
                    
                    # Display product in alternating columns
                    with cols[i % 2]:
                        display_product_card(product)
        
        # Search logic
        if search_button:
            cat = None if category == "All" else category
            filtered = search_products(products, cat, max_price, search_term)
            
            if filtered:
                # Results count
                st.markdown(f"""
                <div style="background-color: #333333; border-radius: 30px; padding: 8px 16px; display: inline-block; margin: 20px 0;">
                    <span style="color: white; font-weight: bold;">Found {len(filtered)} products</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Create a grid layout for products
                cols = st.columns(2)
                for i, product in enumerate(filtered):
                    # Track product views
                    st.session_state.behavior["viewed_categories"].add(product.get('category', 'Unknown'))
                    st.session_state.behavior["viewed_products"].append(product.get('product_name', 'Unknown'))
                    
                    # Display product in alternating columns
                    with cols[i % 2]:
                        display_product_card(product)
            else:
                # No results found
                st.markdown("""
                <div style="text-align: center; padding: 40px 0; background-color: #222222; border-radius: 16px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/6134/6134065.png" width="100">
                    <h3>No results found</h3>
                    <p>Try different search terms or filters 💫</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Tab 3: Compare Products
    with tab3:
        st.markdown("<h2>✨ Compare Products</h2>", unsafe_allow_html=True)
        
        # Styled direct comparison section
        st.markdown("""
        <div style="background-color: #222222; border-radius: 16px; padding: 20px; margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #FF9EAA;">👯‍♀️ Direct Comparison</h4>
            <p style="color: #888; font-size: 14px;">Compare any two products and get a smart recommendation!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<p style='color: #888; font-size: 14px; margin-bottom: 5px;'>First Product</p>", unsafe_allow_html=True)
            name1 = st.text_input("", placeholder="e.g., Pink Hoodie", key="compare_name1", label_visibility="collapsed")
        with col2:
            st.markdown("<p style='color: #888; font-size: 14px; margin-bottom: 5px;'>Second Product</p>", unsafe_allow_html=True)
            name2 = st.text_input("", placeholder="e.g., Blender", key="compare_name2", label_visibility="collapsed")
        
        # VS icon in the middle
        st.markdown("""
        <div style="text-align: center; margin: 10px 0;">
            <div style="display: inline-block; background-color: #FF9EAA; color: white; width: 40px; height: 40px; border-radius: 50%; line-height: 40px;">
                VS
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Compare button with better styling
        if st.button("✨ Compare Now", key="compare_button", type="primary"):
            if name1 and name2:
                compare_products(name1, name2, products)
            else:
                # Cute error message
                st.markdown("""
                <div style="background-color: #333333; border-radius: 16px; padding: 20px; text-align: center; margin: 20px 0;">
                    <img src="https://cdn-icons-png.flaticon.com/512/7486/7486754.png" width="60">
                    <h4 style="color: #FF9EAA;">Oops! Please enter both product names</h4>
                    <p style="color: #aaa;">We need to know what you want to compare! 💕</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Natural language comparison section
        st.markdown("""
        <div style="background-color: #222222; border-radius: 16px; padding: 20px; margin: 30px 0 20px 0;">
            <h4 style="margin-top: 0; color: #2EC4B6;">💬 Ask in Your Own Words</h4>
            <p style="color: #888; font-size: 14px;">Just type naturally like you'd ask a friend!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat-like input
        user_query = st.text_input("", 
                                 placeholder="Example: Should I buy the hoodie or the blender?", 
                                 key="nl_query",
                                 label_visibility="collapsed")
        
        if st.button("🧠 Ask AI", key="ask_ai_button", type="primary"):
            if user_query:
                parse_and_compare_input(user_query, products)
            else:
                # Cute prompt
                st.markdown("""
                <div style="text-align: center; padding: 20px 0;">
                    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="80">
                    <p style="color: #888;">Ask me anything like "Should I buy X or Y?" 💭</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Tab 4: AI Recommendations
    with tab4:
        st.markdown("<h2>🧠 Smart Recommendations</h2>", unsafe_allow_html=True)
        
        # Create styled recommendation section
        st.markdown("""
        <div style="background-color: #222222; border-radius: 16px; padding: 20px; position: relative; overflow: hidden; margin-bottom: 30px;">
            <div style="position: absolute; right: 20px; top: 20px; background-color: #FF9EAA; width: 60px; height: 60px; border-radius: 50%; display: flex; justify-content: center; align-items: center;">
                <span style="font-size: 30px;">🎁</span>
            </div>
            <h4 style="color: #FF9EAA; margin-top: 0; width: 80%;">Personalized Product Picks</h4>
            <p style="color: #888; font-size: 14px; width: 80%;">Get recommendations based on who you're shopping for!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Product recommendations with improved styling
        st.markdown("<h4 style='margin-top: 0;'>👩‍👧‍👦 Who are you shopping for?</h4>", unsafe_allow_html=True)
        
        # Text input for persona
        persona = st.text_input("", 
                               placeholder="Tell us about who you're shopping for...", 
                               key="persona_input", 
                               label_visibility="collapsed")
        
        # Category selection with styling
        st.markdown("<h4>🛍️ Choose a category</h4>", unsafe_allow_html=True)
        
        # Category selection
        categories = ["All"] + sorted(list(set(p["category"] for p in products if "category" in p)))
        rec_category = st.selectbox("Choose category:", categories, key="rec_category")
            
        # Show selected category with nice styling
        st.markdown(f"""
        <div style="background-color: #333333; border-radius: 30px; padding: 5px 15px; display: inline-block; margin: 10px 0;">
            <span style="color: white; font-weight: bold;">Category: {rec_category}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Budget slider with stylish display
        st.markdown("<h4>💰 What's your budget?</h4>", unsafe_allow_html=True)
        
        # Find max price for budget slider
        max_price_in_data = 5000
        if products:
            try:
                max_price_in_data = max(float(p["price"]) for p in products if "price" in p)
            except:
                pass
                
        rec_budget = st.slider("", 0, int(max_price_in_data), 1000, step=500, label_visibility="collapsed")
        
        # Fancy price display
        st.markdown(f"""
        <div style="text-align: center; margin: 10px 0;">
            <div style="background: linear-gradient(90deg, #FF9EAA, #9D65C9); color: white; border-radius: 30px; padding: 8px 20px; display: inline-block;">
                <span style="font-weight: bold;">Budget: ₹{rec_budget}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get recommendations button
        if st.button("✨ Get Smart Picks", key="recommend_button", type="primary"):
            with st.spinner(""):
                # Display a stylish loading animation
                st.markdown("""
                <div style="text-align: center; padding: 10px 0;">
                    <div style="display: flex; justify-content: center; gap: 8px;">
                        <span style="width: 10px; height: 10px; background-color: #FF9EAA; border-radius: 50%; animation: bounce 1.5s infinite ease-in-out;"></span>
                        <span style="width: 10px; height: 10px; background-color: #FF9EAA; border-radius: 50%; animation: bounce 1.5s infinite ease-in-out; animation-delay: 0.2s;"></span>
                        <span style="width: 10px; height: 10px; background-color: #FF9EAA; border-radius: 50%; animation: bounce 1.5s infinite ease-in-out; animation-delay: 0.4s;"></span>
                    </div>
                    <p style="color: #888; font-size: 14px;">Thinking...</p>
                </div>
                <style>
                @keyframes bounce {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-10px); }
                }
                </style>
                """, unsafe_allow_html=True)
                
                cat = None if rec_category == "All" else rec_category
                prompt = get_persona_product_prompt(products, persona, cat, rec_budget)
                ai_response = ask_ai(prompt)
                
                # Display recommendation in a fancy card
                st.markdown(f"""
                <div style="background-color: #222222; border-radius: 16px; padding: 20px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 2px solid #FFD1D9;">
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="background-color: #FFD1D9; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-right: 15px;">
                            <span style="font-size: 20px;">🧠</span>
                        </div>
                        <h4 style="margin: 0; color: #FF9EAA;">AI Recommendation</h4>
                    </div>
                    <p style="white-space: pre-line; color: white;">{ai_response}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Cart-based recommendations section
        st.markdown("""
        <div style="background-color: #222222; border-radius: 16px; padding: 20px; margin: 30px 0 20px 0;">
            <h4 style="margin-top: 0; color: #2EC4B6;">🛒 Based on Your Cart</h4>
            <p style="color: #888; font-size: 14px;">Let AI suggest products that go well with your current bag items!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show current cart items in a horizontal scroll
        cart_products, _ = get_cart_products(st.session_state.cart, products)
        if cart_products:
            st.markdown("<p style='color: #888; font-size: 14px;'>Currently in your bag:</p>", unsafe_allow_html=True)
            
            for item in cart_products[:5]:  # Show up to 5 items
                st.markdown(f"""
                <div style="background-color: #333333; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                    <p style="margin: 0; font-weight: bold; font-size: 14px; color: white;">{item['product_name']}</p>
                    <p style="margin: 5px 0; color: #FF9EAA; font-weight: bold;">₹{item['price']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("✨ Suggest Matching Items", key="cart_suggestions_button", type="primary"):
                with st.spinner(""):
                    # Show a cute loading animation
                    st.markdown("""
                    <div style="text-align: center; padding: 10px 0;">
                        <div style="display: flex; justify-content: center; gap: 8px;">
                            <span style="width: 10px; height: 10px; background-color: #FF9EAA; border-radius: 50%; animation: bounce 1.5s infinite ease-in-out;"></span>
                            <span style="width: 10px; height: 10px; background-color: #FF9EAA; border-radius: 50%; animation: bounce 1.5s infinite ease-in-out; animation-delay: 0.2s;"></span>
                            <span style="width: 10px; height: 10px; background-color: #FF9EAA; border-radius: 50%; animation: bounce 1.5s infinite ease-in-out; animation-delay: 0.4s;"></span>
                        </div>
                        <p style="color: #888; font-size: 14px;">Finding perfect matches...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    prompt = get_cart_based_suggestion_prompt(st.session_state.cart, products)
                    response = ask_ai(prompt)
                    
                    # Display recommendation in a fancy card
                    st.markdown(f"""
                    <div style="background-color: #222222; border-radius: 16px; padding: 20px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 2px solid #2EC4B6;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: #D1F0FF; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-right: 15px;">
                                <span style="font-size: 20px;">💫</span>
                            </div>
                            <h4 style="margin: 0; color: #2EC4B6;">Perfect Pairings</h4>
                        </div>
                        <p style="white-space: pre-line; color: white;">{response}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            # Cute empty state
            st.markdown("""
            <div style="text-align: center; padding: 30px 0; background-color: #222222; border-radius: 16px;">
                <img src="https://cdn-icons-png.flaticon.com/512/2038/2038854.png" width="100">
                <h3>Your bag is empty!</h3>
                <p style="color: #aaa;">Add some cute stuff first ✨</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Ask anything section
        st.markdown("""
        <div style="background-color: #222222; border-radius: 16px; padding: 20px; margin: 30px 0 20px 0;">
            <h4 style="margin-top: 0;">🔮 Ask Me Anything</h4>
            <p style="color: #888; font-size: 14px;">Get shopping advice or product recommendations!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat-like UI for AI assistant
        llama_query = st.text_input("", 
                                  placeholder="Ask me anything about shopping or products...", 
                                  key="llama_query",
                                  label_visibility="collapsed")
        
        if st.button("💬 Ask Now", key="ask_llama_button", type="primary"):
            if llama_query:
                with st.spinner(""):
                    # Show thinking animation
                    st.markdown("""
                    <div style="text-align: center; padding: 10px 0;">
                        <div style="display: flex; justify-content: center; gap: 8px;">
                            <span style="width: 10px; height: 10px; background-color: #FF9EAA; border-radius: 50%; animation: bounce 1.5s infinite ease-in-out;"></span>
                            <span style="width: 10px; height: 10px; background-color: #FF9EAA; border-radius: 50%; animation: bounce 1.5s infinite ease-in-out; animation-delay: 0.2s;"></span>
                            <span style="width: 10px; height: 10px; background-color: #FF9EAA; border-radius: 50%; animation: bounce 1.5s infinite ease-in-out; animation-delay: 0.4s;"></span>
                        </div>
                        <p style="color: #888; font-size: 14px;">Thinking...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    ai_response = ask_ai(llama_query)
                    
                    # Display in chat format
                    st.markdown(f"""
                    <div class="user-query">
                        <p style="margin: 0;">{llama_query}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="ai-response">
                        <p style="margin: 0; white-space: pre-line;">{ai_response}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Prompt suggestions
                st.markdown("""
                <div style="text-align: center; padding: 20px 0;">
                    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="60">
                    <p style="color: #888;">Try asking me these:</p>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 20px;">
                    <div style="background-color: #333333; padding: 8px 15px; border-radius: 20px; font-size: 14px; color: white;">What's trending now?</div>
                    <div style="background-color: #333333; padding: 8px 15px; border-radius: 20px; font-size: 14px; color: white;">Best gift under ₹500?</div>
                    <div style="background-color: #333333; padding: 8px 15px; border-radius: 20px; font-size: 14px; color: white;">How to style a hoodie?</div>
                    <div style="background-color: #333333; padding: 8px 15px; border-radius: 20px; font-size: 14px; color: white;">Is pink in fashion?</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Tab 5: Checkout
    with tab5:
        st.markdown("<h2>💳 Checkout</h2>", unsafe_allow_html=True)
        
        # Check if checkout is complete and show confirmation
        if st.session_state.checkout_complete:
            # Get the latest order for display
            if st.session_state.orders:
                latest_order = st.session_state.orders[-1]
                
                # Order confirmation
                st.markdown(f"""
                <div style="background-color: #1E2E1E; border-radius: 16px; padding: 30px; text-align: center; margin: 20px 0; border: 2px solid #2A4A2A;">
                    <img src="https://cdn-icons-png.flaticon.com/512/5610/5610944.png" width="100">
                    <h2 style="color: #4CAF50; margin: 20px 0;">Order Placed Successfully! 🎉</h2>
                    <p style="color: #aaa;">Thank you for shopping with Qoozee!</p>
                    <p><strong>Order ID:</strong> QZ-{latest_order['order_id']}</p>
                    <p><strong>Date:</strong> {latest_order['date']}</p>
                    <p><strong>Total Amount:</strong> ₹{latest_order['total']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Order details
                st.markdown(f"""
                <div style="background-color: #222222; border-radius: 16px; padding: 20px; margin: 20px 0;">
                    <h3 style="text-align: center;">Order Details</h3>
                    
                    <div style="display: flex; justify-content: space-between; margin: 20px 0;">
                        <div>
                            <p style="color: #888; margin: 0; font-size: 14px;">Shipping Details</p>
                            <p style="font-weight: bold; margin: 5px 0;">{latest_order['name']}</p>
                            <p style="color: #aaa;">{latest_order['address']}</p>
                            <p style="color: #aaa;">Payment: {latest_order['payment_method']}</p>
                        </div>
                        <div>
                            <p style="color: #888; margin: 0; font-size: 14px;">Delivery Date</p>
                            <p style="font-weight: bold; margin: 5px 0; color: #4CAF50;">{latest_order['delivery_date']}</p>
                        </div>
                    </div>
                    
                    <h4>Ordered Items</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Display ordered items
                for item in latest_order['items']:
                    st.markdown(f"""
                    <div style="background-color: #333333; border-radius: 12px; padding: 15px; margin: 10px 0; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <p style="margin: 0; font-weight: bold; color: white;">{item['product_name']}</p>
                            <p style="margin: 5px 0; color: #aaa; font-size: 14px;">{item['category']}</p>
                        </div>
                        <div>
                            <p style="margin: 0; font-weight: bold; color: #FF9EAA;">₹{item['price']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Order total
                st.markdown(f"""
                <div style="margin: 20px 0; text-align: right;">
                    <p style="color: #888; font-size: 14px; margin: 5px 0;">Subtotal</p>
                    <p style="font-weight: bold; font-size: 24px; color: #FF9EAA; margin: 5px 0;">₹{latest_order['total']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Continue shopping button
                if st.button("🛍️ Continue Shopping", type="primary"):
                    st.session_state.checkout_complete = False
                    st.rerun()
                
            else:
                st.error("Order information not found!")
                
        else:
            # Regular checkout flow
            cart_products, total = get_cart_products(st.session_state.cart, products)
            
            if not cart_products:
                # Empty cart message
                st.markdown("""
                <div style="text-align: center; padding: 30px 0; background-color: #222222; border-radius: 16px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/2038/2038854.png" width="100">
                    <h3>Your bag is empty</h3>
                    <p style="color: #aaa;">Add some cute stuff before checkout! 💕</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Browse products button
                if st.button("🛍️ Browse Products", type="primary"):
                    # Switch to products tab
                    st.rerun()
            else:
                # Create two columns for checkout layout
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    # Customer Information Form with styled sections
                    st.markdown("<h3>📝 Shipping Information</h3>", unsafe_allow_html=True)
                    
                    # Create a form with better styling
                    with st.form(key="checkout_form"):
                        # Personal details section
                        st.markdown("""
                        <div style="background-color: #222222; border-radius: 12px; padding: 15px; margin-bottom: 20px;">
                            <h4 style="margin-top: 0; color: #FF9EAA;">👤 Personal Details</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        name = st.text_input("Full Name*", placeholder="Enter your full name")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            email = st.text_input("Email Address*", placeholder="Enter your email")
                        with col2:
                            phone = st.text_input("Phone Number*", placeholder="Enter your phone number")
                        
                        # Address section
                        st.markdown("""
                        <div style="background-color: #222222; border-radius: 12px; padding: 15px; margin: 20px 0;">
                            <h4 style="margin-top: 0; color: #2EC4B6;">📍 Delivery Address</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        address = st.text_area("Delivery Address*", placeholder="Enter your complete delivery address")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            city = st.text_input("City*", placeholder="Enter your city")
                        with col2:
                            pincode = st.text_input("Pincode*", placeholder="Enter your pincode")
                        
                        # Payment method section
                        st.markdown("""
                        <div style="background-color: #222222; border-radius: 12px; padding: 15px; margin: 20px 0;">
                            <h4 style="margin-top: 0; color: #FFD166;">💳 Payment Method</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Payment method options
                        payment_method = st.selectbox(
                            "Choose Payment Method*",
                            ["Cash on Delivery", "Credit/Debit Card", "UPI", "Net Banking"]
                        )
                        
                        # Terms and conditions
                        st.markdown("<br>", unsafe_allow_html=True)
                        terms = st.checkbox("I agree to the Terms and Conditions")
                        
                        # Submit button
                        submit_button = st.form_submit_button("Place Order")
                        
                        if submit_button:
                            # Form validation
                            if not (name and email and phone and address and city and pincode):
                                st.error("Please fill in all required fields!")
                            elif not terms:
                                st.error("Please agree to the Terms and Conditions!")
                            else:
                                # Process order
                                import random
                                import datetime
                                from datetime import timedelta
                                
                                # Generate random order ID
                                order_id = random.randint(100000, 999999)
                                
                                # Get current date
                                now = datetime.datetime.now()
                                today = now.strftime("%Y-%m-%d %H:%M:%S")
                                
                                # Calculate estimated delivery (3-5 days from now)
                                delivery_days = random.randint(3, 5)
                                delivery_date = (now + timedelta(days=delivery_days)).strftime("%A, %d %B %Y")
                                
                                # Create order object
                                order = {
                                    "order_id": order_id,
                                    "date": today,
                                    "name": name,
                                    "email": email,
                                    "phone": phone,
                                    "address": f"{address}, {city} - {pincode}",
                                    "payment_method": payment_method,
                                    "items": cart_products,
                                    "total": total,
                                    "delivery_date": delivery_date
                                }
                                
                                # Save order to session state
                                st.session_state.orders.append(order)
                                
                                # Clear cart
                                purchased_items = st.session_state.cart.copy()
                                st.session_state.cart = []
                                
                                # Update behavior - track purchased items
                                if "purchased_products" not in st.session_state.behavior:
                                    st.session_state.behavior["purchased_products"] = []
                                
                                for pid in purchased_items:
                                    for product in products:
                                        if int(product['product_id']) == pid:
                                            st.session_state.behavior["purchased_products"].append(product['product_name'])
                                
                                # Set checkout complete flag
                                st.session_state.checkout_complete = True
                                
                                # Refresh page to show confirmation
                                st.rerun()
                
                # Right column - Order summary
                with col2:
                    st.markdown("""
                    <div style="background-color: #222222; border-radius: 16px; padding: 20px; height: 100%;">
                        <h3 style="margin-top: 0;">🧾 Order Summary</h3>
                    """, unsafe_allow_html=True)
                    
                    # Show cart items in summary
                    for item in cart_products:
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; margin: 10px 0; padding-bottom: 10px; border-bottom: 1px dashed #444444;">
                            <div style="max-width: 70%;">
                                <p style="margin: 0; font-size: 14px; font-weight: bold; color: white;">{item['product_name']}</p>
                                <p style="margin: 0; font-size: 12px; color: #888;">{item['category']}</p>
                            </div>
                            <p style="margin: 0; font-weight: bold; color: #FF9EAA;">₹{item['price']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Calculate additional values for better UX
                    subtotal = total
                    shipping = 0 if total > 500 else 50
                    gst = round(subtotal * 0.18, 2)
                    final_total = subtotal + shipping + gst
                    
                    # Display price breakdown
                    st.markdown(f"""
                        <div style="margin: 20px 0;">
                            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                                <p style="margin: 0; color: #888;">Subtotal</p>
                                <p style="margin: 0; font-weight: bold; color: white;">₹{subtotal:.2f}</p>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                                <p style="margin: 0; color: #888;">Shipping</p>
                                <p style="margin: 0; font-weight: bold; color: white;">{f"₹{shipping:.2f}" if shipping > 0 else "<span style='color: #4CAF50;'>FREE</span>"}</p>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                                <p style="margin: 0; color: #888;">GST (18%)</p>
                                <p style="margin: 0; font-weight: bold; color: white;">₹{gst:.2f}</p>
                            </div>
                        </div>
                        
                        <div style="background: linear-gradient(90deg, #FF9EAA, #9D65C9); color: white; border-radius: 12px; padding: 15px; margin: 20px 0;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <p style="margin: 0;">Total</p>
                                <p style="margin: 0; font-weight: bold; font-size: 18px;">₹{final_total:.2f}</p>
                            </div>
                        </div>
                        
                        <div style="margin: 20px 0;">
                            <p style="text-align: center; color: #888; font-size: 12px;">Estimated delivery in 3-5 business days</p>
                            <p style="text-align: center; color: #FF9EAA; font-size: 12px; font-weight: bold;">Free shipping on orders above ₹500!</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Developer Tools (hidden in expander)
    with st.expander("🛠️ Developer Tools", expanded=False):
        st.markdown("### 📊 User Behavior Log")
        st.write("**Viewed Categories:**", list(st.session_state.behavior["viewed_categories"]))
        st.write("**Viewed Products:**", st.session_state.behavior["viewed_products"][-10:])  # Show last 10
        st.write("**Added to Cart:**", st.session_state.behavior["added_products"])
        st.write("**Removed from Cart:**", st.session_state.behavior["removed_products"])
        st.write("**Compared Products:**", st.session_state.behavior["compared_products"])
        
        # Show orders log
        st.markdown("### 📦 Order History")
        if st.session_state.orders:
            for idx, order in enumerate(st.session_state.orders):
                st.write(f"**Order #{idx+1}:** ID: QZ-{order['order_id']}, Total: ₹{order['total']:.2f}, Date: {order['date']}")
            
            # Option to clear orders
            if st.button("Clear Order History"):
                st.session_state.orders = []
                st.success("Order history cleared!")
                st.rerun()
        else:
            st.write("No orders placed yet.")
        
        # Clear data buttons
        if st.button("Clear Session Data"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("Session data cleared!")
            st.rerun()

        # Show initial products button
        if st.button("Show All Products on Load"):
            if 'show_all_products' not in st.session_state:
                st.session_state.show_all_products = True
            else:
                st.session_state.show_all_products = not st.session_state.show_all_products
            st.success(f"{'Enabled' if st.session_state.get('show_all_products', True) else 'Disabled'} showing all products on load")
            st.rerun()
    
    # Display footer
    st.markdown("""
    <div class="footer">
        <p>Qoozee AI Shopping Assistant | Made with 💖</p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()