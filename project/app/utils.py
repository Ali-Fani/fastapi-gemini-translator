# def translate_simple_text(text: str,source_laugeage: str, target_language: str)->str | None:
#     try:
#         translator = Translator()
#         translator.raise_Exception = True
#         print(len(text))
#         time.sleep(2)
#         result = translator.translate(text, dest=target_language)
#         print(result)
#         return result.text
#     except Exception as e:
#         print(f"An error occurred while translating the text: {e}")
#         return None
from functools import lru_cache
import urllib.parse
import html

import os
import time
import google.generativeai as genai
from bs4 import BeautifulSoup, FeatureNotFound
import sentry_sdk

from config.config import Settings

@lru_cache
def get_settings():
    return Settings()

def translate(rich_text: str, src_lang: str, dest_lang: str) -> str:
    response_object = {"status": "", "token_count": 0,"translated_text":""}

    # Check for API key existence
    api_key = get_settings().google_api_key
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not found.")
    print(api_key)
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.0-pro')
        chat = model.start_chat(history=[])
        # chat.send_message(f"Translate the text from {src_lang} to {dest_lang}")
    except Exception as e:
        # Handle exceptions related to API connection or usage
        print(e)
        raise ConnectionError(f"Failed to connect to genai API: {e}")
    
    try:
        soup = BeautifulSoup(rich_text, "html.parser")
    except FeatureNotFound as e:
        # Handle exceptions related to BeautifulSoup parser
        raise ValueError(f"Failed to parse HTML content: {e}")

    for text in soup.findAll(string=True, recursive=True):
        if text.strip():
            prompt = f"{text.strip()}"
            retry_attempts = 3  # Set the number of retry attempts
            for attempt in range(retry_attempts):
                try:
                    prompt_decode = urllib.parse.unquote_plus(prompt)
                    print(prompt_decode)
                    response = chat.send_message(f"Translate the text from {src_lang} to {dest_lang}: {prompt_decode}")
                    print(html.unescape(response.text))
                    text.replaceWith(html.unescape(response.text))
                    break  # Break the loop if the request was successful
                except Exception as e:
                    if '429' in str(e):  # Check if the error code 429 is in the exception message
                        if attempt < retry_attempts - 1:  # Check if more retries are allowed
                            print(f"Rate limit exceeded, retrying in 60 seconds... Attempt {attempt + 1}/{retry_attempts}")
                            time.sleep(5)  # Wait for 60 seconds before retrying
                        else:
                            print("Max retry attempts reached. Failed to translate text due to rate limiting.")
                            response_object["status"] = "error"
                            return response_object
                    else:
                        print(f"Error during translation: {e}")
                        response_object["status"] = "error"
                        return response_object
    token_count = model.count_tokens(chat.history).total_tokens
    sentry_sdk.metrics.incr("total_tokens_used", token_count, tags={"kind": "usage"})
    response_object["status"] = "success"
    response_object["token_count"] = token_count
    response_object["translated_text"] = str(soup)
    return response_object