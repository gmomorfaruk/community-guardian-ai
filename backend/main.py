from fastapi import FastAPI, HTTPException, Body
from passlib.context import CryptContext
import socketio

from models import UserSchema
# We now import the function, not the collection object
from database import get_user_collection

app = FastAPI()

# --- WebSocket Setup ---
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# --- Password Hashing Setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# --- API Endpoints ---

@app.get("/")
def read_root():
    # The connection success message will now appear in the terminal when you first run this
    try:
        get_user_collection()
        return {"message": "Community Guardian AI Backend is running! Database connection test successful."}
    except Exception as e:
        return {"message": f"Backend is running, but database connection failed: {e}"}


@app.post("/register")
async def register_user(user: UserSchema = Body(...)):
    # Get a fresh collection object for this request
    user_collection = get_user_collection()

    # Check if user already exists
    try:
        existing_user = await user_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error checking user: {e}")


    # Hash the password before saving
    user.password = get_password_hash(user.password)

    # Convert user model to dictionary
    user_dict = user.dict()

    # Insert new user into the database
    try:
        await user_collection.insert_one(user_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error saving user: {e}")

    # Remove password from the response for security
    del user_dict["password"]

    return {"message": "User registered successfully!", "user": user_dict}


# --- WebSocket Event Handlers ---
@sio.event
async def connect(sid, environ):
    print(f"A user connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"A user disconnected: {sid}")

@sio.on('panic')
async def handle_panic(sid, data):
    print(f"Panic button pressed by user: {sid}")
