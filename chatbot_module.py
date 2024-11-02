import os
import requests
from dotenv import load_dotenv
load_dotenv()


class Chatbot:
    def __init__(self, website_url):
        self.website_url = website_url

    def get_response(self, user_input, conversation_history):
        history_text = ""
        for idx, message in enumerate(conversation_history):
            if message['sender'] == 'user':
                history_text += f"You: {message['message']}\n\n"
            else:
                history_text += f"Bot: {message['message']}\n\n"

        prompt = f"""
        You are a customer representative chatbot for a company. You are tasked with providing customer support.
        Based on the provided content, generate a detailed and informative response to the user's query. 
        Ensure the response is relevant and directly addresses the user's question. 
        Generate response in less than 40 words. 
        Always answer the question within the context of the business and the information provided below.
        
        Content: {open('content.txt').read()}
        
        Conversation History: {history_text}
        
        User Query: {user_input}
                 
        """

        # Initialize the OpenAI API
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("API key for OpenAI is not set.")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + api_key
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_tokens": 4095,
            }
        ).json()
        print(f"Openai response is - {response}")

        if response.get("choices"):
            responseText = response["choices"][0]["message"]["content"]
            # print(f"Generated summary is - {responseText}")
        else:
            responseText = "No response from OpenAI."
        return responseText
