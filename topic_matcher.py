"""
topic_matcher.py - Classify each bullet point into a topic using the Gemini model.
"""

import json
from prompts import TOPIC_MATCHING_PROMPT


# Always appends "other" as a fallback option
def load_topics(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    topic_names = [item["topic"] for item in data]

    topic_names.append("other")

    return topic_names


def match_topic(bullet_text, topics_list, model):
    """Ask Gemini to classify a single bullet point into one of the available topics."""
    topics_text = "\n".join(f"- {topic}" for topic in topics_list)

    prompt = TOPIC_MATCHING_PROMPT.format(bullet=bullet_text, topics_list=topics_text)

    try:
        response = model.generate_content(prompt)
        parsed = json.loads(response.text)
        topic = parsed.get("topic", "other").strip()

        # If the model returned a topic not in our list, fall back to "other"
        if topic not in topics_list:
            print(f"Warning: model returned unknown topic '{topic}', using 'other'.")
            return "other"

        return topic

    except Exception as e:
        print(f"Error in match_topic: {e}")
        return "other"


def match_all_bullets(bullets, topics_list, model):
    """Classify every bullet point in the list into a topic."""
    total = len(bullets)

    for index, item in enumerate(bullets, start=1):
        print(f"Classificando bullet {index}/{total}...")
        topic = match_topic(item["bullet"], topics_list, model)
        item["macro_topic"] = topic

    return bullets
