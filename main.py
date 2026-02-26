import json

def load_data():
    with open("users.json") as u:
        users = json.load(u)
    with open("roles.json") as r:
        roles = json.load(r)
    return users, roles

def check_access(username, action):
    users, roles = load_data()

    for user in users["users"]:
        if user["username"] == username:
            role = user["role"]
            permissions = roles["roles"][role]

            if action in permissions:
                print("Access Granted")
            else:
                print("Access Denied")
            return

    print("User not found")

if __name__ == "__main__":
    username = input("Enter username: ")
    action = input("Enter action (read/write/delete): ")
    check_access(username, action)
  
