"""
This file contains HTML components for the Qoozee shopping assistant.
These components can be rendered using Streamlit's st.markdown() with unsafe_allow_html=True.
"""

# Header components
def app_header():
    """Return the app header HTML."""
    return """
    <div class="app-header">
        <h1>✨ Qoozee AI Shopping Assistant ✨</h1>
        <p class="app-subtitle">your AI shopping bestie</p>
    </div>
    """

def user_profile(username="Spoorthi", premium=True):
    """Return the user profile HTML for the sidebar."""
    premium_badge = '⭐ Premium Member' if premium else 'Member'
    first_letter = username[0].upper()
    
    return f"""
    <div class="user-profile">
        <div class="avatar">
            <span>{first_letter}</span>
        </div>
        <div class="user-info">
            <p class="user-name">{username}</p>
            <p class="user-status">{premium_badge}</p>
        </div>
    </div>
    """

def stat_counter(label, value, color="#FF9EAA"):
    """Return a stat counter HTML for the sidebar."""
    return f"""
    <div class="stat-container">
        <span class="stat-label">{label}</span>
        <span class="stat-value" style="background-color: {color};">{value}</span>
    </div>
    """

# Product and cart components
def product_card(product):
    """Return a product card HTML."""
    return f"""
    <div class="product-card">
        <h3>✨ {product['product_name']}</h3>
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 10px 0;">
            <span class="price-tag">₹{product['price']}</span>
            <span class="star-rating">⭐ {product['rating']}</span>
        </div>
        <span class="category-badge">{product['category']}</span>
    </div>
    """

def cart_item(item):
    """Return a cart item HTML."""
    return f"""
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
    """

def total_price(amount):
    """Return the total price HTML."""
    return f"""
    <div class="total-price">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>Bag Total:</span>
            <span>₹{amount:.2f}</span>
        </div>
    </div>
    """

def empty_cart():
    """Return the empty cart HTML."""
    return """
    <div style="text-align: center; padding: 30px 0;">
        <img src="https://cdn-icons-png.flaticon.com/512/2038/2038854.png" width="100">
        <h3>Your bag is empty!</h3>
        <p>Add some cute stuff and come back 💕</p>
    </div>
    """

def no_results():
    """Return the no results HTML."""
    return """
    <div style="text-align: center; padding: 40px 0;">
        <img src="https://cdn-icons-png.flaticon.com/512/6134/6134065.png" width="100">
        <h3>No results found</h3>
        <p>Try different search terms or filters 💫</p>
    </div>
    """

# AI components
def ai_thinking():
    """Return the AI thinking animation HTML."""
    return """
    <div style="text-align: center; padding: 10px 0;">
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
        <p style="color: #888; font-size: 14px;">Thinking...</p>
    </div>
    """

def chat_message(message, is_user=True):
    """Return a chat message HTML."""
    if is_user:
        return f"""
        <div class="user-query">
            <p style="margin: 0; color: #333; font-size: 15px;">{message}</p>
        </div>
        """
    else:
        return f"""
        <div class="ai-response">
            <p style="margin: 0; color: #333; font-size: 15px; white-space: pre-line;">{message}</p>
        </div>
        """

def ai_suggestion_prompts():
    """Return suggestion prompts for the AI chat."""
    return """
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="60">
        <p style="color: #666;">Try asking me these:</p>
    </div>
    <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 20px;">
        <div style="background-color: #F0F0F0; padding: 8px 15px; border-radius: 20px; font-size: 14px;">What's trending now?</div>
        <div style="background-color: #F0F0F0; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Best gift under ₹500?</div>
        <div style="background-color: #F0F0F0; padding: 8px 15px; border-radius: 20px; font-size: 14px;">How to style a hoodie?</div>
        <div style="background-color: #F0F0F0; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Is pink in fashion?</div>
    </div>
    """

# Order components
def order_confirmation(order_id, date, total):
    """Return the order confirmation HTML."""
    return f"""
    <div class="order-success">
        <img src="https://cdn-icons-png.flaticon.com/512/5610/5610944.png" width="100">
        <h2 style="color: #4CAF50; margin: 20px 0;">Order Placed Successfully! 🎉</h2>
        <p style="color: #555;">Thank you for shopping with Qoozee!</p>
        <p><strong>Order ID:</strong> QZ-{order_id}</p>
        <p><strong>Date:</strong> {date}</p>
        <p><strong>Total Amount:</strong> ₹{total:.2f}</p>
    </div>
    """

def order_details(order):
    """Return the order details HTML."""
    return f"""
    <div class="order-details">
        <h3 style="text-align: center;">Order Details</h3>
        
        <div style="display: flex; justify-content: space-between; margin: 20px 0;">
            <div>
                <p style="color: #888; margin: 0; font-size: 14px;">Order ID</p>
                <p style="font-weight: bold; margin: 5px 0;">QZ-{order['order_id']}</p>
            </div>
            <div>
                <p style="color: #888; margin: 0; font-size: 14px;">Order Date</p>
                <p style="font-weight: bold; margin: 5px 0;">{order['date']}</p>
            </div>
        </div>
        
        <div style="background-color: #F9F9F9; border-radius: 12px; padding: 15px; margin: 20px 0;">
            <h4 style="margin-top: 0;">Shipping Details</h4>
            <p style="margin: 5px 0;"><strong>Name:</strong> {order['name']}</p>
            <p style="margin: 5px 0;"><strong>Address:</strong> {order['address']}</p>
            <p style="margin: 5px 0;"><strong>Payment Method:</strong> {order['payment_method']}</p>
        </div>
        
        <div style="margin: 20px 0;">
            <h4>Delivery Information</h4>
            <div style="background: linear-gradient(90deg, #FF9EAA, #9D65C9); color: white; border-radius: 12px; padding: 15px; text-align: center;">
                <p style="margin: 0; font-size: 14px;">Estimated Delivery Date</p>
                <p style="font-weight: bold; margin: 5px 0; font-size: 18px;">{order['delivery_date']}</p>
            </div>
        </div>
    </div>
    """

def order_item(item):
    """Return an ordered item HTML."""
    return f"""
    <div style="background-color: #F9F9F9; border-radius: 12px; padding: 15px; margin: 10px 0; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <p style="margin: 0; font-weight: bold;">{item['product_name']}</p>
            <p style="margin: 5px 0; color: #888; font-size: 14px;">{item['category']}</p>
        </div>
        <div>
            <p style="margin: 0; font-weight: bold; color: #FF9EAA;">₹{item['price']}</p>
        </div>
    </div>
    """

# Miscellaneous components
def section_header(title, color="#FF9EAA", icon=""):
    """Return a section header HTML."""
    return f"""
    <div style="background-color: #F9F9F9; border-radius: 16px; padding: 20px; margin-bottom: 20px;">
        <h4 style="margin-top: 0; color: {color};">{icon} {title}</h4>
    </div>
    """

def footer():
    """Return the footer HTML."""
    return """
    <div class="footer">
        <p>Qoozee AI Shopping Assistant | Made with 💖</p>
    </div>
    """

def load_css():
    """Return the HTML to load the external CSS file."""
    return """
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    """