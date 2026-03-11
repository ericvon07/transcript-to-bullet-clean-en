"""
All prompt templates used to talk to the Gemini model.

Each template is a plain string with {placeholders} that get filled in
before the prompt is sent to the model.
"""

# Used in the first pass to extract bullet points from a transcript.
# The model reads the raw text and returns a JSON list of bullet points.
# Models' answers were kept in Portuguese on purpose to keep our real use case

BULLET_EXTRACTION_PROMPT = """
You are an analyst specialized in extracting key points from meeting transcripts about companies.

Your task is to extract bullet points from the text below, focusing on the {sentiment} aspects of the company.

Rules:
- Each bullet must be ONE concise and self-contained sentence.
- Include only information relevant to the "{sentiment}" sentiment.
- ALWAYS respond in Portuguese, even if the text is in English.
- Return ONLY valid JSON, with no markdown and no explanations, in the format:
  [{{"bullet": "texto do bullet point"}}]
- If the text does not contain relevant content for the "{sentiment}" sentiment, return: []

Transcript:
{transcript}
"""

# Used when the eval judge says the coverage is not good enough.
# The model already extracted some bullets, but topics might be still missing.
# This prompt asks the model to generate only the missing bullets.
# Models' answers were kept in Portuguese on purpose to keep our real use case
BULLET_REFINEMENT_PROMPT = """
You are an analyst specialized in extracting key points from meeting transcripts about companies.

Your task is to extract bullet points from the text below, focusing on the {sentiment} aspects of the company.

You have already extracted these bullets previously:
{previous_bullets}

However, the following topics were not covered:
{missing_topics}

Generate additional bullets that cover these missing topics.
Return ONLY the NEW bullets — do not repeat the previous ones.

Rules:
- Each bullet must be ONE concise and self-contained sentence.
- ALWAYS respond in Portuguese, even if the text is in English.
- Return ONLY valid JSON, with no markdown and no explanations, in the format:
  [{{"bullet": "texto do bullet point"}}]
- If there is no relevant content for the missing topics, return: []

Transcript:
{transcript}
"""

# Used to classify a single bullet point into one of the available topics.
# The model receives the bullet and the full topic list, and picks the best match.
# Models' answers were kept in Portuguese on purpose to keep our real use case
TOPIC_MATCHING_PROMPT = """
Classify the bullet point below into the most appropriate topic from the provided list.

Bullet point:
{bullet}

Available topics:
{topics_list}

Rules:
- Choose the topic that best represents the content of the bullet point.
- If no topic is suitable, use "other".
- Return ONLY valid JSON, with no markdown and no explanations, in the format:
  {{"topic": "nome_do_topico"}}
- ALWAYS respond in Portuguese when generating any natural-language content, but keep the topic value exactly as defined in the provided topic list.
"""

# Used by the eval judge to check if the extracted bullets cover the transcript well.
# The model compares the bullets against the original text and returns a score.
# Models' answers were kept in Portuguese on purpose to keep our real use case
EVAL_PROMPT = """
Compare the bullet points below with the original transcript.

Evaluate whether all relevant topics mentioned in the transcript were covered by the bullets,
considering only the {sentiment} aspects of the company.

Transcript:
{transcript}

Extracted bullet points:
{bullets}

Return ONLY valid JSON, with no markdown and no explanations, in the format:
{{"score": 0.85, "missing_topics": ["topico1", "topico2"]}}

Rules:
- score: a number from 0 to 1, where 1 means full coverage of the relevant topics.
- missing_topics: a list of important subjects from the transcript that were NOT covered by the bullets.
- If the score is greater than or equal to 0.7, return missing_topics as an empty list: []
- ALWAYS respond in Portuguese when generating any natural-language content.
"""
