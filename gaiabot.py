import requests
import random
import time
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)

# Configuration
BASE_URL = "https://celestia.gaia.domains"
MODEL = "qwen2-7b-instruct"
MAX_RETRIES = 100  # Essentially infinite retries
RETRY_DELAY = 5  # Seconds between retries
QUESTION_DELAY = 1  # Seconds between successful questions

QUESTIONS = [
    "What is no-code?",
    "Why use no-code for websites?",
    "Which no-code tools are popular for websites?",
    "What to look for in a no-code platform?",
    "How to start a no-code website?",
    "How to add pages in no-code?",
    "How to customize a no-code site's look?",
    "Can no-code integrate with other services?",
    "How to make a no-code site mobile-friendly?",
    "How to launch a site with no-code?",
    "Can no-code handle e-commerce?",
    "What are no-code platform limitations?",
    "How to manage SEO on a no-code site?",
    "Where to learn about no-code web building?",
    "Can professionals help with no-code websites?",
    "How much does no-code website building cost?",
    "Can I use custom domains with no-code?",
    "How to get support for no-code issues?",
    "How to update a no-code website?",
    "Examples of no-code built websites?",
    "What types of sites can no-code build?",
    "How to add custom code in no-code?",
    "How to add forms using no-code?",
    "What hosting options does no-code offer?",
    "How to create a landing page with no-code?",
    "How to ensure site accessibility with no-code?",
    "How to manage media in no-code?",
    "How to add a blog with no-code?",
    "Can no-code build business websites?",
    "How to add email forms with no-code?",
    "How to track analytics in no-code?",
    "Can no-code make a portfolio site?",
    "How to integrate social media with no-code?",
    "Can no-code be used for non-profits?",
    "How to add search functionality in no-code?",
    "How to secure a no-code website?",
    "How to publish a site with no-code?",
    "How to add payments with no-code?",
    "Can no-code make local business sites?",
    "How to optimize speed in no-code?",
    "How to add a favicon in no-code?",
    "How to add Google Maps with no-code?",
    "How to integrate email marketing in no-code?",
    "How to add reviews with no-code?",
    "How to add a contact form in no-code?",
    "Where to find no-code troubleshooting help?",
    "Can no-code create community websites?",
    "How to add a photo gallery with no-code?",
    "How to customize fonts with no-code?",
    "How to use no-code for app development?",
    "What are the benefits of no-code apps?",
    "What kinds of apps can no-code make?",
    "Which no-code platforms are best for apps?",
    "How to pick a no-code app platform?",
    "How to start designing an app with no-code?",
    "How to manage data in no-code apps?",
    "How to integrate services in no-code apps?",
    "How to customize app UI with no-code?",
    "How to manage users in no-code apps?",
    "How to secure no-code apps?",
    "How to authenticate users in no-code apps?",
    "How to test no-code apps?",
    "How to deploy no-code apps?",
    "How to migrate data in no-code apps?",
    "Can I add custom code to no-code apps?",
    "How to add user content in no-code apps?",
    "How to scale no-code apps?",
    "Can no-code make mobile apps?",
    "How to handle payments in no-code apps?",
    "How to send notifications in no-code apps?",
    "How to use push notifications in no-code?",
    "How to track usage in no-code apps?",
    "How to handle errors in no-code apps?",
    "How to gather feedback on no-code apps?",
    "How to integrate APIs in no-code apps?",
    "Where to learn more about no-code apps?",
    "How to manage databases in no-code apps?",
    "Can no-code make real-time apps?",
    "How to manage roles in no-code apps?",
    "How to ensure privacy in no-code apps?",
    "How to collaborate on no-code projects?",
    "How to backup no-code apps?",
    "How to maintain no-code apps?",
    "Can no-code make enterprise apps?",
    "How to integrate with other systems in no-code?",
    "How to link to social media in no-code apps?",
    "How to optimize no-code app performance?",
    "How to engage users in no-code apps?",
    "How to segment users in no-code apps?",
    "How to personalize no-code apps?",
    "How to onboard users in no-code apps?",
    "How to retain users in no-code apps?",
    "How to support users in no-code apps?",
    "How to integrate CRM in no-code apps?",
    "How to use marketing automation in no-code?",
    "How to localize no-code apps?",
    "How to comply with data laws in no-code?",
    "How to visualize data in no-code apps?",
    "How to manage file storage in no-code apps?",
    "How to manage tasks in no-code apps?"
]

def chat_with_ai(api_key: str, question: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = [
        {"role": "user", "content": question}
    ]

    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    for attempt in range(MAX_RETRIES):
        try:
            logging.info(f"Attempt {attempt+1} for question: {question[:50]}...")
            response = requests.post(
                f"{BASE_URL}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]

            logging.warning(f"API Error ({response.status_code}): {response.text}")
            time.sleep(RETRY_DELAY)

        except Exception as e:
            logging.error(f"Request failed: {str(e)}")
            time.sleep(RETRY_DELAY)

    raise Exception("Max retries exceeded")

def run_bot(api_key: str):
    while True:  # Outer loop to repeat the questions indefinitely
        random.shuffle(QUESTIONS)
        logging.info(f"Starting chatbot with {len(QUESTIONS)} questions in random order")

        for i, question in enumerate(QUESTIONS, 1):
            logging.info(f"\nProcessing question {i}/{len(QUESTIONS)}")
            logging.info(f"Question: {question}")

            start_time = time.time()
            try:
                response = chat_with_ai(api_key, question)
                elapsed = time.time() - start_time

                # Print the entire response
                print(f"Answer to '{question[:50]}...':\n{response}")

                logging.info(f"Received full response in {elapsed:.2f}s")
                logging.info(f"Response length: {len(response)} characters")

                # Ensure the script waits for the full response before proceeding
                time.sleep(QUESTION_DELAY)  # Wait before asking next question

            except Exception as e:
                logging.error(f"Failed to process question: {str(e)}")
                continue

def main():
    print("Title: GaiaAI Chatbot")
    print("Twitter: https://x.com/0xMoei")
    api_key = input("Enter your API key: ")
    run_bot(api_key)

if __name__ == "__main__":
    main()
