from pymongo import MongoClient
from pymongo.errors import PyMongoError
import bcrypt
from datetime import datetime, timedelta

# MongoDB connection URI
uri = "use your mongodb connection string here"
client = None

def db_conn():
    try:
        global client
        client = MongoClient(uri)
        client.admin.command('ping')
        return True
    except PyMongoError as e:
        return False

def authenticate_user(email, password):
    try:
        db = client["billboardgenie"]
        users_collection = db["users"]
        user = users_collection.find_one({"email": email})

        if user:
            hashed_password = user.get("password", "")
            # Check if the input password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return user, ""  # Return the user data or whatever is needed upon successful authentication
            else:
                return None, "Incorrect password"
        else:
            return None, "User not found"
    except PyMongoError as e:
        return False, "No Internet. Please check your connection"

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def signup_user(fullname, email, phone, password, billboard_location, cpm, monthly_cost):
    try:
        hashed = hash_password(password)
        db = client["billboardgenie"]
        users_collection = db["users"]
        billboards_collection = db["billboards"]

        # Insert new user and billboard data
        user_data = {
            "fullname": fullname,
            "email": email,
            "phone": phone,
            "password": hashed
        }
        billboard_data = {
            "email": email,
            "billboard_location": billboard_location,
            "cpm": cpm,
            "monthly_cost": monthly_cost
        }

        users_collection.insert_one(user_data)
        billboards_collection.insert_one(billboard_data)
        return True, "Signup successful! Please login to continue."
    except PyMongoError as e:
        return False, "No Internet. Please check your connection"
    
def exising_email(email):
    db = client["billboardgenie"]
    users_collection = db["users"]
    
    user = users_collection.find_one({"email": email})

    if user:
        return False, "Email already exists", user
    
    else:
        return True, ""
    
def update_db_password(email, password):
    db = client["billboardgenie"]
    users_collection = db["users"]
    
    hashed_password = hash_password(password)

    result = users_collection.update_one(
        {"email": email},
        {"$set": {"password": hashed_password}}
        )

    if result.modified_count > 0:
        return True
    else:
        return False
    
def insert_counts_data(email, car_count, motorcycle_count, bus_count, truck_count, total_count, date):
    db = client["billboardgenie"]
    billboards_collection = db["billboards"]
    counts_collection = db["counts"]

    billboard = billboards_collection.find_one({"email": email})
    # Get the current date
    # current_date = datetime(2024, 1, 1)  # Starting date

    # days_to_add = days

    # # Add the calculated days to the current date
    # target_date = current_date + timedelta(days=days_to_add)

    # # Create the timestamp string using the target date
    # timestamp = target_date.isoformat()

    data = {
        "email": email,
        "billboard_location": billboard['billboard_location'],
        "timestamp": date,
        "car_count": car_count,
        "motorcycle_count": motorcycle_count,
        "bus_count": bus_count,
        "truck_count": truck_count,
        "total_count": total_count
    }
    try:
        counts_collection.insert_one(data)
        return True, "Data inserted successfully"
    except Exception as e:
        return False, "Error inserting data"