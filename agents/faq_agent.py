import json
import difflib
import os

class FAQAgent:
    def __init__(self, faq_path='data/faq.json'):
        self.faq_data = self.load_faq(faq_path)

    def load_faq(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"FAQ file not found at: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Auto-fix in case it's a list of strings (JSON strings instead of dicts)
            if isinstance(data, list) and all(isinstance(item, str) for item in data):
                try:
                    data = [json.loads(item) for item in data]
                except json.JSONDecodeError:
                    raise ValueError("FAQ file contains invalid JSON strings inside the list.")

            if not all(isinstance(item, dict) and 'question' in item and 'answer' in item for item in data):
                raise ValueError("FAQ data must be a list of objects with 'question' and 'answer' keys.")

            return data

    def get_answer(self, user_question):
        questions = [item['question'] for item in self.faq_data]
        matches = difflib.get_close_matches(user_question, questions, n=1, cutoff=0.6)
        if matches:
            matched_question = matches[0]
            for item in self.faq_data:
                if item['question'] == matched_question:
                    return item['answer']
        return "Sorry, I couldn't find an answer to that question."


