

from nicegui.html import ins
from supabase import create_client # type: ignore
import os
from dotenv import load_dotenv

load_dotenv()

# Your existing env vars
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key) # type: ignore
supabase.rest_url = url # type: ignore

# Select all users
def select_all_users():
    response = supabase.table("users").select("*").execute()
    # print(response.data)
    return response.data



# Insert a user
def insert_a_user(name):
    response = supabase.table("users").insert({"name": name}).execute()
    return response.data


# Update a user
def update_user(user_id, new_name):
    response = supabase.table("users").update({"name": new_name}).eq("id", user_id).execute()
    return response.data

# Delete a user
def delete_user(user_id):
    response = supabase.table("users").delete().eq("id", user_id).execute()
    return response.data
print("\nInserting users...\n")
insert_a_user("testuser")
insert_a_user("me")
insert_a_user("samujele")

print(select_all_users()) 




# old code using requests library to interact with supabase rest api, now using the official supabase client library for python
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()
# url = os.getenv("SUPABASE_URL")
# key = os.getenv("SUPABASE_KEY")



# headers = {"Authorization": f"Bearer {key}"}
# def insert_a_user():
#     # Insert
#     requests.post(f"{url}/users", headers=headers, json={"name": "samujele"})
# insert_a_user()

# ## write me a select statement

# def select_all_users():
#     # Select all
#     data = requests.get(f"{url}/users", headers=headers).json()
#     print(data)
# print(select_all_users())

# def delete_all_users():
#     # # Delete
#     data = requests.get(f"{url}/users?id",headers=headers).json()
#     print(data)
#     for i in data:
#         # requests.delete(f"{url}/users?id=eq.1", headers=headers)
#         requests.delete(f"{url}/users?id=eq.{i["id"]}", headers=headers)