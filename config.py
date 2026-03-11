"""
Project settings and environment variables.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-2.5-pro"

# tweak these if needed
EVAL_THRESHOLD = 0.7

MAX_RETRIES = 2

INPUT_FILE = "data/raw_transcripts.xlsx"

OUTPUT_DIR = "outputs/"

TOPICS_FILE = "possible_topics.json"

SENTIMENTS = ["positive", "negative", "dealbreaker"]

SKIP_VALUES = ["n.a.", "n.a", "none", "NONE", "N.A.", ""]


# response_mime_type forces the model to return only valid JSON w/o markdown, no extra text
def get_gemini_client():
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        generation_config=genai.GenerationConfig(response_mime_type="application/json"),
    )
