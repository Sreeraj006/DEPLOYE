import csv
import random
import difflib

class FinanceKnowledgeBot:
    def __init__(self, dataset_path):
        self.qa_pairs = self.load_knowledge_base(dataset_path)
        self.intent_keywords = {
            "saving": ["save", "saving", "savings", "how to save"],
            "spending": ["reduce spending", "cut expenses", "spending habits", "unnecessary expenses"],
            "budget": ["budget", "track expenses", "monthly plan", "plan expenses"],
            "investment": ["invest", "investment", "mutual fund", "sip", "stocks", "gold", "bonds", "equity"],
            "emergency": ["emergency fund", "unexpected cost", "contingency"],
            "debt": ["debt", "loan", "clear debt", "pay off"],
            "stock": ["stock", "share", "trading", "stock market", "nifty", "sensex"],
            "apps": ["app", "groww", "zerodha", "money manager", "upstox"]
        }

    def load_knowledge_base(self, path):
        data = []
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    question = row["Query"].strip().lower()
                    answer = row["Answer"].strip()
                    data.append({"query": question, "answer": answer})
        except FileNotFoundError:
            print("❌ CSV file not found. Please check the path.")
        return data

    def match_intent(self, user_input):
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in user_input:
                    return intent
        return None

    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        matched_intent = self.match_intent(user_input)

        if matched_intent:
            related_answers = [
                qa["answer"] for qa in self.qa_pairs
                if any(keyword in qa["query"] for keyword in self.intent_keywords[matched_intent])
            ]
            if related_answers:
                return random.choice(related_answers)

        queries = [qa["query"] for qa in self.qa_pairs]
        closest_matches = difflib.get_close_matches(user_input, queries, n=1, cutoff=0.5)
        if closest_matches:
            match_query = closest_matches[0]
            for qa in self.qa_pairs:
                if qa["query"] == match_query:
                    return qa["answer"]

        return random.choice([qa["answer"] for qa in self.qa_pairs])
