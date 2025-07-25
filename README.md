# NuGenomics Assistant

This project provides a multi-agent AI assistant for NuGenomics, handling FAQs and general genetic wellness information through a web interface.

## Features

* **Customer Support Agent:** Answers NuGenomics FAQs.
* **Genetic Wellness Agent:** Uses Google Gemini 1.5 Flash for general genetic wellness queries.
* **Intelligent Routing:** Automatically directs queries to the appropriate agent.
* **Web Interface:** Flask-based, responsive UI with interactive, clickable FAQs.

## Project Structure

.
├── .env                  # API key configuration
├── web_app.py            # Main Flask app
├── requirements.txt      # Python dependencies
├── data/
│   └── faq.json          # FAQ knowledge base
├── agents/
│   ├── faq_agent.py      # FAQ logic
│   └── gpt_agent.py      # Gemini integration
├── multi_tool_agent/
│   └── adk_runner.py     # Query routing
├── templates/
│   └── index.html        # Frontend HTML
└── static/
└── style.css         # Frontend CSS


## Setup Instructions

1.  **Clone:** `git clone https://github.com/Jes087/NuGenomics-Assistant`
2.  **Navigate:** `cd NuGenomicsAssistant`
3.  **Virtual Environment:** `python -m venv .venv` then activate (`.\.venv\Scripts\activate` or `source .venv/bin/activate`).
4.  **Install Dependencies:** `pip install -r requirements.txt` and `pip install Flask[async]`.
5.  **Gemini API Key:** Obtain a key from [Google AI Studio](https://aistudio.google.com/). Create a `.env` file in the project root: `GOOGLE_API_KEY=YOUR_API_KEY_HERE`. **(Do not commit .env)**

## How to Run

1.  Activate your virtual environment.
2.  Run: `python web_app.py`
3.  Open `http://127.0.0.1:5000` in your browser.

## Testing Protocol

**Objective:** Verify correct query routing and accurate responses from both agents, and frontend functionality.

**Test Cases Summary:**

* **FAQ Agent:**
    * Direct FAQ match (e.g., "What is genetic predispostion?").
    * Close FAQ match (e.g., "Do I need a gym membership?").
    * Clicking a displayed FAQ.
* **GPT Agent (Fallback):**
    * General genetic wellness question (e.g., "What is personalized nutrition?").
* **Edge Cases:**
    * Out-of-scope questions (e.g., "What is the capital of France?").
    * Nonsense input.
* **Frontend UI/UX:**
    * Random FAQ display on load.
    * Loading spinner behavior.
    * "View More FAQs" link functionality.
    * Responsiveness on different screen sizes.

*(For detailed expected outcomes, refer to the screen recording demonstration.)*

## Architecture Overview

Queries are handled by `web_app.py` via `ADKRunner`. `ADKRunner` first attempts to match the query with `faq_agent.py` (using `difflib.get_close_matches` with `cutoff=0.6`). If no FAQ match is found, the query falls back to `gpt_agent.py`, which uses the Google Agent Development Kit to interact with Gemini 1.5 Flash for general genetic wellness information. The frontend provides an interactive, responsive user experience.

## AI Assistance Disclosure

Google Gemini (as an AI Assistant) was used for debugging, code refinement, CSS generation, and documentation.
