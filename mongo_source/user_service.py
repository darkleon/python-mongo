from db import user_collections

def add_user(name, email, age):
    user = {
        "name": name,
        "email": email,
        "age": age
    }
    result = user_collections.insert_one(user)
    print(f"User {name} added successfully with id {result.inserted_id}")

add_user("Alice", "alice@example.com", 30)
add_user("Bob", "bob@example.com", 25)