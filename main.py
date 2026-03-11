"""
Entry point for the transcript-to-bullet pipeline.

  1. Place transcript file inside the data/ folder as raw_transcripts.xlsx.
  2. Make sure possible_topics.json is filled with your list of topics.
  3. Run: python main.py
"""

import sys
from config import (
    GEMINI_API_KEY,
    EVAL_THRESHOLD,
    MAX_RETRIES,
    INPUT_FILE,
    OUTPUT_DIR,
    TOPICS_FILE,
    SENTIMENTS,
    get_gemini_client,
)
from data_io import read_transcripts, write_output
from bullet_engine import extract_bullets, refine_bullets, should_skip
from topic_matcher import load_topics, match_all_bullets
from eval_judge import evaluate_bullets


def process_company(company_data, topics_list, model):
    """Run extraction, evaluation, refinement, and topic classification for one company row."""
    company_name = company_data["company"]
    all_results = []

    for sentiment in SENTIMENTS:
        transcript = company_data[sentiment]

        print(f"  Sentiment: {sentiment} ({len(str(transcript))} chars)")

        # Skip if the text has no useful content
        if should_skip(transcript):
            print(f"  → Skipping (no content)")
            continue

        # First extraction pass
        bullets = extract_bullets(transcript, sentiment, model)
        print(f"  → {len(bullets)} bullets extracted")

        # Evaluation and refinement loop
        evaluation = evaluate_bullets(transcript, sentiment, bullets, model)
        score = evaluation["score"]
        missing_topics = evaluation["missing_topics"]
        print(f"  → Score: {score}")

        for attempt in range(1, MAX_RETRIES + 1):
            if score >= EVAL_THRESHOLD:
                break

            print(
                f"  → Score {score} < {EVAL_THRESHOLD}, refining... (attempt {attempt}/{MAX_RETRIES})"
            )

            # Ask the model to generate bullets for the missing topics
            new_bullets = refine_bullets(
                transcript, sentiment, bullets, missing_topics, model
            )

            # Combine new bullets with the ones we already have
            bullets = bullets + new_bullets

            # Re-evaluate with the updated bullet list
            evaluation = evaluate_bullets(transcript, sentiment, bullets, model)
            score = evaluation["score"]
            missing_topics = evaluation["missing_topics"]
            print(f"  → Score: {score}")

        print(f"  → {len(bullets)} bullets approved for {sentiment}")

        # Topic classification
        classified = match_all_bullets(bullets, topics_list, model)

        # Build output rows
        for item in classified:
            all_results.append(
                {
                    "company": company_name,
                    "bullet_point": item["bullet"],
                    "macro_topic": item["macro_topic"],
                    "sentiment": sentiment,
                }
            )

    return all_results


def main():

    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found. Check your .env file.")
        sys.exit(1)

    model = get_gemini_client()

    transcripts = read_transcripts(INPUT_FILE)
    if not transcripts:
        print(f"Error: no companies found in '{INPUT_FILE}'. Check the file.")
        sys.exit(1)

    topics_list = load_topics(TOPICS_FILE)

    all_results = []

    for company_data in transcripts:
        print(f"Processing company: {company_data['company']}...")
        company_results = process_company(company_data, topics_list, model)
        all_results.extend(company_results)

    output_path = write_output(all_results, OUTPUT_DIR)

    total_companies = len(transcripts)
    total_bullets = len(all_results)
    print(f"Pipeline complete! {total_bullets} bullets saved to {output_path}")
    print(f"({total_companies} companies processed)")


if __name__ == "__main__":
    main()
