from agents.faq_agent import FAQAgent
from agents.gpt_agent import GPTAgent

class ADKRunner:
    def __init__(self):
        self.faq_agent = FAQAgent("data/faq.json")
        self.gpt_agent = GPTAgent()

    # Changed to an asynchronous method
    async def route_query(self, query):
        # Step 1: Try FAQ Agent (assuming FAQAgent.get_answer is synchronous)
        faq_answer = self.faq_agent.get_answer(query)
        if faq_answer and "Sorry, I couldn't find an answer" not in faq_answer:
            return {"source": "faq", "answer": faq_answer}

        # Step 2: Fall back to GPT Agent
        # Corrected: await the asynchronous method call
        gpt_answer = await self.gpt_agent.get_answer(query)
        return {"source": "gpt", "answer": gpt_answer}