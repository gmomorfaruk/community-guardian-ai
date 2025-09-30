import os
import motor.motor_asyncio
from dotenv import load_dotenv
import certifi

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

def get_user_collection():
    """
    Creates a new database client and returns the user collection.
    """
    if not MONGO_DETAILS:
        raise ValueError("MONGO_DETAILS environment variable not found.")

    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(
            MONGO_DETAILS,
            tlsCAFile=certifi.where()
        )
        db = client.cga_db
        return db.get_collection("users")
    except Exception as e:
        # We'll print the error here to see if connection fails at this point
        print(f"❌ Error creating new motor client: {e}")
        raise
