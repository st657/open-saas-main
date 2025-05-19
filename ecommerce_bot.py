import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import json
import os

creds_json = os.getenv('GOOGLE_CREDENTIALS')
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("DiscountGalaFAQ").sheet1

# Load FAQ data
def load_faq():
    faq_data = sheet.get_all_records()
    return {item['Question'].lower(): item['Answer'] for item in faq_data}

# Search for answer in FAQ
def find_answer(question):
    faq = load_faq()
    question = question.lower().strip()
    
    # Look for exact or partial matches
    for q, a in faq.items():
        if re.search(r'\b' + re.escape(question) + r'\b', q) or question in q:
            return a
    return "I'm sorry, I couldn't find an answer to your question. Please contact support@discountgala.com for assistance."

# Bot response function
def bot_response(user_input):
    response = find_answer(user_input)
    return f"Discount Gala Support: {response}"

# Example usage
if __name__ == "__main__":
    print("Welcome to Discount Gala E-Commerce Support Bot!")
    while True:
        user_input = input("Ask a question (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        print(bot_response(user_input))