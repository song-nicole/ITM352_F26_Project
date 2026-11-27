import json
from pathlib import Path

#Access data from the JSON files
users_json = Path(__file__).parent / "userDATA" / "users.json"
def load_users():
    with open(users_json, "r") as file:
        return json.load(file)

#Save data to JSON files
def save_users(users):
    with open(users_json, "w") as file:
        json.dump(users, file, indent=4)