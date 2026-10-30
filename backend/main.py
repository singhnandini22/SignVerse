from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import sqlite3
import secrets
import os
import sys

import cv2
import numpy as np

from pwdlib import PasswordHash

from backend.database import create_users_table, get_connection


# Make the existing image-processing pipeline importable when FastAPI
# is started from the SignVerse project root.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_PROCESSING_DIR = os.path.join(PROJECT_ROOT, "image_processing")
if IMAGE_PROCESSING_DIR not in sys.path:
    sys.path.insert(0, IMAGE_PROCESSING_DIR)

from predict import ISLRecognizer


# =========================================
# CREATE FASTAPI APP
# =========================================

app = FastAPI()


# =========================================
# CORS
# =========================================
# This allows the HTML frontend to communicate
# with the FastAPI backend running on port 8000.

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================
# PASSWORD HASHING
# =========================================

password_hash = PasswordHash.recommended()


# =========================================
# DATABASE SETUP
# =========================================

create_users_table()


def update_old_database():

    connection = get_connection()

    cursor = connection.cursor()

    # Get existing columns
    cursor.execute("PRAGMA table_info(users)")

    columns = cursor.fetchall()

    column_names = [column["name"] for column in columns]


    # Add phone column if it does not exist
    if "phone" not in column_names:

        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN phone TEXT NOT NULL DEFAULT ''
        """)


    # Add age column if it does not exist
    if "age" not in column_names:

        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN age INTEGER NOT NULL DEFAULT 0
        """)


    # Add level column if it does not exist
    if "level" not in column_names:

        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN level INTEGER DEFAULT 1
        """)


    # Add XP column if it does not exist
    if "xp" not in column_names:

        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN xp INTEGER DEFAULT 0
        """)


    # Add letters progress column if it does not exist
    if "letters_progress" not in column_names:

        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN letters_progress INTEGER DEFAULT 0
        """)


    # Add numbers progress column if it does not exist
    if "numbers_progress" not in column_names:

        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN numbers_progress INTEGER DEFAULT 0
        """)


    connection.commit()

    connection.close()


# Update an older existing database
update_old_database()


# =========================================
# SIGNUP DATA
# =========================================

class SignupData(BaseModel):

    name: str

    email: EmailStr

    password: str

    phone: str

    age: int


# =========================================
# LOGIN DATA
# =========================================

class LoginData(BaseModel):

    email: EmailStr

    password: str


# =========================================
# HOME
# =========================================

@app.get("/")
def home():

    return {
        "message": "SignVerse backend is running!"
    }


# =========================================
# SIGNUP
# =========================================

@app.post("/signup")
def signup(user: SignupData):

    # -------------------------------------
    # NAME VALIDATION
    # -------------------------------------

    name = user.name.strip()

    if name == "":

        raise HTTPException(
            status_code=400,
            detail="Name is required."
        )


    if len(name) < 2:

        raise HTTPException(
            status_code=400,
            detail="Name must contain at least 2 characters."
        )


    # -------------------------------------
    # PASSWORD VALIDATION
    # -------------------------------------

    if len(user.password) < 6:

        raise HTTPException(
            status_code=400,
            detail="Password must be at least 6 characters long."
        )


    # -------------------------------------
    # PHONE VALIDATION
    # -------------------------------------

    phone = user.phone.strip()

    if phone == "":

        raise HTTPException(
            status_code=400,
            detail="Phone number is required."
        )


    if not phone.isdigit() or len(phone) != 10:

        raise HTTPException(
            status_code=400,
            detail="Phone number must contain exactly 10 digits."
        )


    # -------------------------------------
    # AGE VALIDATION
    # -------------------------------------

    if user.age < 1 or user.age > 120:

        raise HTTPException(
            status_code=400,
            detail="Age must be between 1 and 120."
        )


    # -------------------------------------
    # DATABASE CONNECTION
    # -------------------------------------

    connection = get_connection()

    cursor = connection.cursor()


    try:

        # ---------------------------------
        # CHECK EMAIL
        # ---------------------------------

        cursor.execute(
            "SELECT id FROM users WHERE email = ?",
            (str(user.email).lower(),)
        )

        existing_user = cursor.fetchone()


        if existing_user:

            raise HTTPException(
                status_code=400,
                detail="An account with this email already exists."
            )


        # ---------------------------------
        # HASH PASSWORD
        # ---------------------------------

        hashed_password = password_hash.hash(
            user.password
        )


        # ---------------------------------
        # INSERT USER
        # ---------------------------------

        cursor.execute("""
            INSERT INTO users
            (
                name,
                email,
                password,
                phone,
                age
            )
            VALUES (?, ?, ?, ?, ?)
        """, (

            name,

            str(user.email).lower(),

            hashed_password,

            phone,

            user.age

        ))


        connection.commit()


        user_id = cursor.lastrowid


    except HTTPException:

        connection.close()

        raise


    except sqlite3.IntegrityError:

        connection.close()

        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists."
        )


    except Exception as error:

        connection.close()

        print("Signup database error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to create account. Please try again."
        )


    connection.close()


    # -------------------------------------
    # SUCCESS RESPONSE
    # -------------------------------------

    return {

        "message": "Account created successfully!",

        "user_id": user_id

    }


# =========================================
# LOGIN
# =========================================

@app.post("/login")
def login(user: LoginData):

    email = str(user.email).lower()


    # -------------------------------------
    # DATABASE CONNECTION
    # -------------------------------------

    connection = get_connection()

    cursor = connection.cursor()


    # -------------------------------------
    # FIND USER
    # -------------------------------------

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            password,
            phone,
            age,
            level,
            xp,
            letters_progress,
            numbers_progress
        FROM users
        WHERE email = ?
    """, (email,))


    existing_user = cursor.fetchone()


    # -------------------------------------
    # USER NOT FOUND
    # -------------------------------------

    if not existing_user:

        connection.close()

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )


    # -------------------------------------
    # CHECK PASSWORD
    # -------------------------------------

    password_is_correct = password_hash.verify(
        user.password,
        existing_user["password"]
    )


    if not password_is_correct:

        connection.close()

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )


    # -------------------------------------
    # CREATE SIMPLE ACCESS TOKEN
    # -------------------------------------

    access_token = secrets.token_urlsafe(32)


    # -------------------------------------
    # USER DATA
    # -------------------------------------

    user_data = {

        "id": existing_user["id"],

        "name": existing_user["name"],

        "email": existing_user["email"],

        "phone": existing_user["phone"],

        "age": existing_user["age"],

        "level": existing_user["level"],

        "xp": existing_user["xp"],

        "letters_progress":
            existing_user["letters_progress"],

        "numbers_progress":
            existing_user["numbers_progress"]

    }


    connection.close()


    # -------------------------------------
    # LOGIN SUCCESS
    # -------------------------------------

    return {

        "message": "Login successful!",

        "access_token": access_token,

        "user": user_data

    }


    # =========================================
# UPDATE LEARNING PROGRESS
# =========================================

class ProgressData(BaseModel):

    user_id: int

    learning_type: str

    item: str


@app.post("/progress")
def update_progress(progress: ProgressData):

    # -------------------------------------
    # VALIDATE LEARNING TYPE
    # -------------------------------------

    if progress.learning_type not in ["letters", "numbers"]:

        raise HTTPException(
            status_code=400,
            detail="Invalid learning type."
        )


    # -------------------------------------
    # DATABASE CONNECTION
    # -------------------------------------

    connection = get_connection()

    cursor = connection.cursor()


    # -------------------------------------
    # FIND USER
    # -------------------------------------

    cursor.execute(
        "SELECT id, letters_progress, numbers_progress FROM users WHERE id = ?",
        (progress.user_id,)
    )

    user = cursor.fetchone()


    if not user:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )


    # -------------------------------------
    # CALCULATE COMPLETED ITEM
    # -------------------------------------

    if progress.learning_type == "letters":

        item = progress.item.upper()

        if (
            len(item) != 1
            or not ("A" <= item <= "Z")
        ):

            connection.close()

            raise HTTPException(
                status_code=400,
                detail="Invalid letter."
            )

        completed_items = (
            ord(item) - ord("A") + 1
        )

        total_items = 26

        current_progress = (
            user["letters_progress"] or 0
        )

        new_progress = round(
            (completed_items / total_items) * 100
        )

        # Never decrease existing progress
        new_progress = max(
            current_progress,
            new_progress
        )

        cursor.execute(
            """
            UPDATE users
            SET letters_progress = ?
            WHERE id = ?
            """,
            (
                new_progress,
                progress.user_id
            )
        )


    else:

        item = progress.item.strip()

        if (
            not item.isdigit()
            or int(item) < 1
            or int(item) > 10
        ):

            connection.close()

            raise HTTPException(
                status_code=400,
                detail="Invalid number."
            )

        completed_items = int(item)

        total_items = 10

        current_progress = (
            user["numbers_progress"] or 0
        )

        new_progress = round(
            (completed_items / total_items) * 100
        )

        # Never decrease existing progress
        new_progress = max(
            current_progress,
            new_progress
        )

        cursor.execute(
            """
            UPDATE users
            SET numbers_progress = ?
            WHERE id = ?
            """,
            (
                new_progress,
                progress.user_id
            )
        )


    # -------------------------------------
    # SAVE CHANGES
    # -------------------------------------

    connection.commit()


    # -------------------------------------
    # GET UPDATED PROGRESS
    # -------------------------------------

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            phone,
            age,
            level,
            xp,
            letters_progress,
            numbers_progress
        FROM users
        WHERE id = ?
        """,
        (progress.user_id,)
    )

    updated_user = cursor.fetchone()

    connection.close()


    # -------------------------------------
    # RETURN UPDATED USER DATA
    # -------------------------------------

    return {

        "message": "Progress updated successfully.",

        "user": {

            "id": updated_user["id"],

            "name": updated_user["name"],

            "email": updated_user["email"],

            "phone": updated_user["phone"],

            "age": updated_user["age"],

            "level": updated_user["level"],

            "xp": updated_user["xp"],

            "letters_progress":
                updated_user["letters_progress"],

            "numbers_progress":
                updated_user["numbers_progress"]
        }
    }

# =========================================
# IMAGE SIGN RECOGNITION
# =========================================

# Load the trained recognizer only when the first prediction is requested.
# This avoids loading the large model for requests that only use login/signup.
recognizer = None


def get_recognizer():
    global recognizer
    if recognizer is None:
        recognizer = ISLRecognizer()
    return recognizer


@app.post("/recognize")
async def recognize_sign(file: UploadFile = File(...)):
    """Receive one webcam frame and return the predicted sign."""
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image captured from the webcam."
        )

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="The uploaded image is empty.")

    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(status_code=400, detail="Could not read the uploaded image.")

    try:
        result = get_recognizer().predict_frame(frame)
        return result
    except Exception as error:
        print("Sign recognition error:", error)
        raise HTTPException(
            status_code=500,
            detail="Sign recognition failed. Check the backend terminal for details."
        )


@app.on_event("shutdown")
def close_recognizer():
    """Release MediaPipe resources when the backend shuts down."""
    global recognizer
    if recognizer is not None:
        recognizer.close()
        recognizer = None
