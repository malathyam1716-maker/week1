import requests
from config.settings import settings

def extract_users():
    limit = 10
    skip = 0
    all_users = []

    while True:
        response = requests.get(
            settings.dummy_json_url,
            params={"limit": limit, "skip": skip}
        )

        data = response.json()

        users = data["users"]

        if not users:
            break
        
        # Perform DB operations here (e.g., insert users into the database)
        all_users.extend(users)

        skip += limit

    return all_users

users = extract_users()

print("Total Users:", len(users))
