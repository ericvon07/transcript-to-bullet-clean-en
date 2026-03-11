"""Evaluate how well the extracted bullets cover the transcript."""

import json
from prompts import EVAL_PROMPT


def evaluate_bullets(transcript, sentiment, bullets, model):
    """Ask Gemini to score bullet coverage against the transcript and return any missing topics."""
    bullets_text = "\n".join(f"- {b['bullet']}" for b in bullets)

    prompt = EVAL_PROMPT.format(
        sentiment=sentiment, transcript=transcript, bullets=bullets_text
    )

    try:
        response = model.generate_content(prompt)
        parsed = json.loads(response.text)

        score = parsed.get("score", 0.0)
        missing_topics = parsed.get("missing_topics", [])

        score = max(0.0, min(1.0, float(score)))

        return {"score": score, "missing_topics": missing_topics}

    except Exception as error:
        # TODO: switch to proper logging
        print(f"Error in evaluate_bullets: {error}")
        return {"score": 0.0, "missing_topics": ["erro no parse"]}
