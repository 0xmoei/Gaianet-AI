# Title: GaiaAI Chatbot
# Created by: Moei
# Twitter: https://x.com/0xMoei

# The script will print the credit part and ask for the API key

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
    "What is a neural network?",
    "What is RNA?",
    "What is deep learning?",
    "What is a black hole?",
    "What is a star?",
    "What is dopamine?",
    "What is algorithmic fairness?",
    "What is turbulence?",
    "What is a circular economy?",
    "What is plasma in fusion research?",
    "What is the role of mitochondria?",
    "What is superposition in quantum mechanics?",
    "What is the Big Bang theory?",
    "What is cellular respiration?",
    "What is a VPN?",
    "What is a biosphere?",
    "What is a Calabi-Yau manifold?",
    "What is the hippocampus?",
    "What is NP-complete?",
    "What is ocean acidification?",
    "What is electrical resistance?",
    "What is a neurodegenerative disease?",
    "What is entanglement in quantum computing?",
    "What is neurofeedback?",
    "What is artificial general intelligence?",
    "What are monoclonal antibodies?",
    "What is cosmic microwave background?",
    "What is a quantum circuit?",
    "What is gene editing?",
    "What is a singularity in astrophysics?"
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
    print("Created by: Moei")
    print("Twitter: https://x.com/0xMoei")
    api_key = input("Enter your API key: ")
    run_bot(api_key)

if __name__ == "__main__":
    main()
