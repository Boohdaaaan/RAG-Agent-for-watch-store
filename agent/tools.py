import re
import sqlite3 as sq
from langchain.agents import tool
from langchain.tools.retriever import create_retriever_tool
from data_loader import db


def format_phone(phone_number: str) -> str:
    """
    Validates and formats a given phone number to the standard Ukrainian format: +380 (XX) XXX XX XX.

    Parameters:
    phone_number (str): A string representation of the phone number to be validated and formatted.

    Returns:
    str: The formatted phone number in the standard Ukrainian format or an error message if the input is invalid.
    """
    # Remove all non-digit characters
    cleaned_number = re.sub(r'\D', '', phone_number)

    # Prepend '380' if the number is domestic (10 digits)
    if len(cleaned_number) == 10:
        cleaned_number = '38' + cleaned_number

    # Check if the cleaned number has the correct length (12 digits) and starts with '380'
    if len(cleaned_number) == 12 and cleaned_number.startswith('380'):
        # Format the number
        formatted_number = f"+{cleaned_number[:3]} ({cleaned_number[3:5]}) {cleaned_number[5:8]} {cleaned_number[8:10]} {cleaned_number[10:]}"
    else:
        # Return an error message if the number does not meet the criteria
        return "Invalid format"

    return formatted_number


retriever = db.as_retriever()
info_retriever = create_retriever_tool(
    retriever,
    "Information_retriever",
    "Searches and returns information about watches and shop.",
)


# Define a tool for placing an order
@tool
def order_placement(user_name: str = "", user_surname: str = "", phone_number: str = "", city: str = "",
                    watch_model: str = ""):
    """
    Useful when user want to order watch.
    Retrieves username, surname, phone number, city for product delivery and watch model.
    If user don't provide not enough data, keep default values.

    Parameters:
    - user_name (str): The first name of the user placing the order.
    - user_surname (str): The surname of the user placing the order.
    - phone_number (str): The contact phone number of the user.
    - city (str): The city where the product (watch) will be delivered.
    - watch_model (str): The specific watch model or name the user wishes to order.
    """

    # Format the phone number
    phone_number = format_phone(phone_number)

    # Check if all necessary data is provided
    for data_field in [user_name, user_surname, phone_number, city, watch_model]:
        if data_field == "":
            return "You don't provide all necessary data."

            # Connect to the database and insert the order information
    with sq.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO orders (name, surname, phone, city, model) VALUES (?, ?, ?, ?, ?)",
            (user_name, user_surname, phone_number, city, watch_model)
        )


# Define a tool for saving feedback
@tool
def feedback_saver(user_feedback: str, feedback_sentiment: str):
    """
    Called when the user leaves a review or feedback.
    When user thanks or points out the bad aspects of the store.
    When the user is satisfied or dissatisfied with the work of the store.

    Parameters:
    - user_feedback (str): The feedback or review provided by the user.
    - feedback_sentiment (str): The sentiment of the feedback. Can be either 'positive' or 'negative'.
    """

    # Connect to the database and insert the feedback information
    with sq.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO feedback_records (feedback_text, feedback_sentiment) VALUES (?, ?)",
            (user_feedback, feedback_sentiment)
        )
