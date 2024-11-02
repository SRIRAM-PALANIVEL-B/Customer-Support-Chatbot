import os
import requests
import streamlit as st
from chatbot_module import Chatbot  # Ensure this imports your modified chatbot class
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/56.0.2924.76 Safari/537.36',
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "https://www.google.com/"
}

# Function to scrape content from website URL
def scrapeContent(url):
    if not url.startswith("https://") and not url.startswith("http://"):
        url = "https://" + url
    res = requests.get(url, headers=headers, timeout=180)
    if str(res.status_code).startswith("4"):
        return None
    soup = BeautifulSoup(res.content, 'html.parser')

    for tag in soup.find_all():
        for style in ['style', 'class']:
            del tag[style]

    tags_to_extract = ['p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', "li"]
    contentChecker = []
    extracted_content = ' '
    for tag in soup.find_all(tags_to_extract):
        temp = tag.get_text(strip=True)
        temp = temp.replace('\xa0', ' ').replace("Â", ' ').strip()
        if temp not in contentChecker:
            contentChecker.append(temp)
            extracted_content += " {}".format(temp)

    content = extracted_content.replace("\n", ' ')
    with open('content.txt', 'w') as file:
        file.write(content)
    return content

# Display input form for website URL
def display_input_form():
    st.title('Customer Support Chatbot Application')
    st.header('Enter Website URL to Scrape')
    website_url = st.text_input('Enter Website URL')
    if st.button('Submit'):
        try:
            content = scrapeContent(website_url)
            if content:
                st.session_state.website_url = website_url
                st.experimental_rerun()
            else:
                st.error('Invalid URL. Please enter a valid website URL.')
                st.stop()
        except Exception as e:
            st.error(f'An error occurred: {e}')
            st.stop()

# Display chatbot interface with conversation history
def display_chatbot_interface():
    st.title('Customer Support Chatbot')
    st.header('Chat Interface')

    website_url = st.session_state.website_url
    chatbot = Chatbot(website_url)

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    conversation_history = st.session_state.conversation_history
    user_input = st.text_input('You:', key='user_input')

    if st.button('Send'):
        bot_response = chatbot.get_response(user_input, conversation_history)
        conversation_history.append({'sender': 'user', 'message': user_input})
        conversation_history.append({'sender': 'bot', 'message': bot_response})

        st.session_state.conversation_history = conversation_history

    st.subheader('Conversation History:')
    history_text = ""
    for idx, message in enumerate(conversation_history):
        if message['sender'] == 'user':
            history_text += f"You: {message['message']}\n\n"
        else:
            history_text += f"Bot: {message['message']}\n\n"

    st.text_area(label='Chat History', value=history_text, height=400, max_chars=None, key=None)

# Chatbot class with API response logging for debugging
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

        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("API key for OpenAI is not set.")

        # API call with response logging
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

        st.write(response)  # Log the response for debugging

        if response.get("choices"):
            responseText = response["choices"][0]["message"]["content"]
        else:
            responseText = "No response from OpenAI."
        return responseText

# Main function to control flow
def main():
    if 'website_url' not in st.session_state:
        display_input_form()
    else:
        display_chatbot_interface()

if __name__ == '__main__':
    main()
