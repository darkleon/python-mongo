from db import order_collections, user_collections

def add_order(email, product, price):
    user = user_collections.find_one({"email": email})
    if user is None:
        print(f"User with email {email} not found")
        return
    order = {
        "user_id": user["_id"],
        "product": product,
        "price": price,
        "discount": 0
    }
    
    result = order_collections.insert_one(order)
    print(f"Order add successfully with id {result.inserted_id}")

def get_orders(email):
    user = user_collections.find_one({"email": email})
    if user is None:
        print(f"The user with email {email} not found")
        return
    orders = order_collections.find({"user_id": user["_id"]})
    
    for order in orders:
        print(f"The user {email} has ordered {order['product']} at price {order['price']}")
    

add_order("alice@example.com", "Laptop", 1200)
add_order("bob@example.com", "Smartphone", 800)
add_order("alice@example.com", "Headphones", 100)

get_orders("alice@example.com")