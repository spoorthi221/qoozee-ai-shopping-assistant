import csv

# --- LOAD PRODUCTS ---
def load_products(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

# --- SHOW CART ---
def show_cart(cart_ids, products):
    print("🛒 Your Cart:")
    total = 0
    for pid in cart_ids:
        for product in products:
            if product['product_id'] == str(pid):
                print(f"- {product['product_name']} | ₹{product['price']} | ⭐ {product['rating']}")
                total += float(product['price'])
    print(f"Total: ₹{total}")

# --- SEARCH FUNCTION ---
def search_products(category, max_price, products):
    print(f"\n🔍 Products in '{category}' under ₹{max_price}:")
    found = False
    for product in products:
        if (product['category'].lower() == category.lower() and 
            float(product['price']) <= max_price):
            print(f"- {product['product_name']} | ₹{product['price']} | ⭐ {product['rating']}")
            found = True
    if not found:
        print("No products found in this range.")
        
def compare_products(name1, name2, products):
    product1 = None
    product2 = None

    for product in products:
      if name1.lower() in product['product_name'].lower():
        product1 = product
      elif name2.lower() in product['product_name'].lower():
        product2 = product
 
    if not product1 or not product2:
        print("❌ One or both products not found.")
        return

    # Show both products
    print("\n🆚 Product Comparison:\n")
    print(f"1️⃣ {product1['product_name']}")
    print(f"   - Price: ₹{product1['price']}")
    print(f"   - Rating: ⭐ {product1['rating']}")
    print(f"   - Category: {product1['category']}\n")

    print(f"2️⃣ {product2['product_name']}")
    print(f"   - Price: ₹{product2['price']}")
    print(f"   - Rating: ⭐ {product2['rating']}")
    print(f"   - Category: {product2['category']}\n")

    # Suggest based on rating first, then price
    rating1 = float(product1['rating'])
    rating2 = float(product2['rating'])

    if rating1 > rating2:
        better = product1['product_name']
    elif rating2 > rating1:
        better = product2['product_name']
    else:  # if same rating, choose the cheaper one
        price1 = float(product1['price'])
        price2 = float(product2['price'])
        better = product1['product_name'] if price1 < price2 else product2['product_name']

    print(f"💡 Suggestion: Go for '{better}' – it offers better value!")
    
def parse_comparison_input(user_input, products):
    # Convert to lowercase and clean up
    user_input = user_input.lower().replace("should i buy", "").replace("?", "").replace("the", "").strip()

    # Split by connectors
    if " or " in user_input:
        parts = user_input.split(" or ")
    elif " vs " in user_input:
        parts = user_input.split(" vs ")
    else:
        print("❌ Couldn't detect two products to compare.")
        return

    if len(parts) != 2:
        print("❌ Please mention exactly two products.")
        return

    name1 = parts[0].strip()
    name2 = parts[1].strip()

    compare_products(name1, name2, products)

 


# --- MAIN ---
if __name__ == "__main__":
    products = load_products('products.csv')
    cart = [101, 105]
    show_cart(cart, products)
    print("\n---")
    search_products("Electronics", 1000, products)
    print("\n---")
    user_input = input("\n🤖 Ask something like 'Should I buy the hoodie or blender?':\n> ")
    parse_comparison_input(user_input, products)

  


