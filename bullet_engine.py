"""
bullet_engine.py - Extract bullet points from transcripts using the Gemini model.
"""

import json
from config import SKIP_VALUES
from prompts import BULLET_EXTRACTION_PROMPT, BULLET_REFINEMENT_PROMPT


def _parse_json_response(text):
    """Try to parse a JSON string returned by the Gemini model."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Remove markdown code block markers if present and try again
        cleaned = (
            text.strip()
            .removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return None


# Returns True if the text is empty or a known placeholder value
def should_skip(text):
    if text is None:
        return True
    return str(text).strip() in SKIP_VALUES


def extract_bullets(transcript, sentiment, model):
    """Send a transcript to Gemini and return a list of bullet-point dicts for the given sentiment."""
    prompt = BULLET_EXTRACTION_PROMPT.format(sentiment=sentiment, transcript=transcript)

    try:
        response = model.generate_content(prompt)
        result = _parse_json_response(response.text)

        if result is None:
            print(
                f"Warning: could not parse JSON response for sentiment '{sentiment}'."
            )
            print(f"Raw response: {response.text[:200]}")
            return []

        return result

    except Exception as error:
        print(f"Error calling Gemini in extract_bullets: {error}")
        return []


def refine_bullets(transcript, sentiment, previous_bullets, missing_topics, model):
    """Ask Gemini to generate new bullets covering topics that were missed in the first extraction pass."""
    previous_bullets_text = "\n".join(f"- {b['bullet']}" for b in previous_bullets)
    missing_topics_text = "\n".join(f"- {topic}" for topic in missing_topics)

    prompt = BULLET_REFINEMENT_PROMPT.format(
        sentiment=sentiment,
        transcript=transcript,
        previous_bullets=previous_bullets_text,
        missing_topics=missing_topics_text,
    )

    try:
        response = model.generate_content(prompt)
        result = _parse_json_response(response.text)

        if result is None:
            print(
                f"Warning: could not parse JSON response in refine_bullets for sentiment '{sentiment}'."
            )
            print(f"Raw response: {response.text[:200]}")
            return []

        return result

    except Exception as error:
        print(f"Error calling Gemini in refine_bullets: {error}")
        return []
