# transcript-to-bullet

Reads company meeting transcripts from an Excel spreadsheet, uses Google Gemini to extract the key points as bullet points, and classifies each bullet into a topic. Positive aspects, negative aspects, and dealbreakers are processed independently, with an automatic evaluation and refinement loop to ensure coverage.

---

### Setup

Install dependencies and add your Gemini API key to a `.env` file:

```bash
pip install -r requirements.txt
cp .env.example .env   # then paste your key into GEMINI_API_KEY
```

---

### Usage

Place `raw_transcripts.xlsx` in the `data/` folder and run:

```bash
python main.py
```

The output is saved to `outputs/output_YYYYMMDD_HHMMSS.xlsx` with columns: `company`, `bullet_point`, `macro_topic`, `sentiment`.

---

### Input format

The spreadsheet must have these columns:

| company | positive_points | negative_points | dealbreakers |
|---------|----------------|----------------|--------------|

Empty cells or cells containing `n.a.` are skipped automatically.

---

### Project structure

```
transcript-to-bullet/
├── main.py               # Entry point — orchestrates the full pipeline
├── config.py             # Settings and Gemini client setup
├── data_io.py            # Reads the input xlsx and writes the output xlsx
├── bullet_engine.py      # Extracts and refines bullet points using Gemini
├── topic_matcher.py      # Classifies each bullet into a topic
├── eval_judge.py         # Evaluates bullet coverage (score 0–1)
├── prompts.py            # All prompt templates used with Gemini
├── possible_topics.json  # List of possible topics for classification
├── requirements.txt      # Project dependencies
├── .env.example          # Template for the environment variables file
├── data/                 # Place your raw_transcripts.xlsx here
└── outputs/              # Result files are saved here
```
